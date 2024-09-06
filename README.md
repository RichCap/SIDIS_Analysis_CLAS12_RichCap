# SIDIS_Analysis_CLAS12_RichCap
Analysis code for multidimensional SIDIS Analysis of CLAS12 data


## To-do List (General)
This list will be updated as items are completed. Items here may not always relate to the code in the Github repository.
- [ ] Unfolding Tests:
    - [x] 1) Plot the fit parameters B, C as functions of z and pT
    - [x] 2) Replace the experimental data with MC data to test if the unfolding procedures reproduce the generated data properly
    - [x] 3) Calculate (1 + B*cos(phi) + C*cos(2*phi)) from theory and rewieght the response matrices to test modulations in generated phi_h
        * [x] Test this with the test (2) above
    - [ ] 4) Calculate Luminosity to start implementing proper normalization procedures during unfolding
- [ ] Multidimensional Unfolding Tests:
    - [x] 1) Tested up to 2D (Finished [x])
    - [x] 2) Tested up to 3D (Finished [x])
    - [x] 3) Tested up to 5D (Finished [ ])
        * [x] Started
        * [x] Working Bin-by-Bin (identical to other versions)
        * [x] Working Bayesian Method
            * [ ] Perform test to find the ideal number of iterations for unfolding with 5D Response Matrix
- [ ] Radiative Corrections:
    - [ ] 1) Need to find new Monte Carlo files with radiative effects included
        * [ ] Need to test and compare the new Monte Carlo with the current one (at generator level)
    - [ ] 2) Run new event generator through GEMC for reconstructed distribution
    - [ ] 3) Use new files to perform radiative corrections 

### Systematic Uncertainties 'To Do' List:
 1) [ ] Track Reconstruction Efficiency (HERMES/Rebecca estimated based on a detector variable - must investigate if a similar one exists in CLAS12)
 2) [ ] PID - Handled within Unfolding (check impact on moments)
 3) [ ] phi_h binning (currently 24 bins per 360 degrees - adjust and check impact)
     * [ ] Also vary the other kinematic bins to see impact of shifting Q2, y, z, and pT (vary individually)
 4) [ ] Bin statistics (HERMES/Rebecca had a method to evaluate what constituted poor statistics)
 5) [ ] Closure tests (self-evaluations of unfolding)
 6) [ ] Impact of higher terms (i.e., add cos(3phi), cos(4phi), and/or sin(phi) to fit functions to evaluate the impact on cos(phi) and cos(2phi)
     * The extra moments should (ideally) be consistent with 0
 7) [ ] Model Dependence Including:
     * [ ] Monte Carlo simulator (clasdis vs pythia)
     * [ ] Background Subtraction (background identification is reliant on the reliablity of the MC)
     * [ ] MC Smearing/Momentum/Energy Loss Corrections
     * [ ] Type of Unfolding (i.e., Bin-by-Bin vs Bayesian - Includes the dimensions used within unfolding including: 1D, 3D, and 5D Response Matrices)
 8) [ ] Fiducial Cuts (vary the different cuts to see the impact of tighter/looser/no cut - variation can depend on the cuts)
 9) [ ] Proton Tagging/Cuts (for Vector Meson Corrections)
     * Impact may be analyzed in a sub-section of the overall kinematic region due to impact to statistics/kinematic coverage
     * [ ] Look for how others handled rho extraction
10) [ ] Number of Bayesian Iterations
11) [ ] Radiative Effects
12) [ ] Sector Dependence


---



## Detailed Commit Updates:

### Update on 7-8-2024:
* Updated File_Name_Updates.md and removed the file notes moved to that file
* Other Updates have been noted within these note or in the individual commits


### Update on 5-30-2024:
* Notes regarding commit related to running 'New_Sector_Cut_Test_V1':
    * Ran 'Background_Tests' versions 1-4 (completed V1 and V2, but will reset makeROOT_epip_SIDIS_histos_new.py and ExtraAnalysisCodeValues.py to complete V3 and V4)
    * Ran 'New_Sector_Cut_Test_V1' which included the addition of the 'New_Fiducial_Sector_Cuts' for testing the additional fiducial cuts based on Hx and Hy
        * Ran with sector-dependent cuts/plots
        * Reset all background cuts that were being toggled in the 'Background_Tests'
    * Added new jupyter-notebook (Working_on_Hx_Hy_Plots.ipynb) to create the 'New_Fiducial_Sector_Cuts' used in 'New_Sector_Cut_Test_V1'

### Update on 5-24-2024:
* Notes regarding Sort_RooUnfold_SIDIS_richcap.py:
    * Error was discovered related to organizing the results of the Sim_Test options
        * Caused the directory/text file to be renamed while moving files
        * Issue was fixed by making it so that only PNG files with 'Sim_Test' in their names will be renamed
* git commit notes for makeROOT_epip_SIDIS_histos_new.py:
    * About to run Extra_Name = "5D_Unfold_Test_V7_"
    * Discovered (and fixed) an issue with the background cuts
        * The condition (PID_el != 11 && PID_pip != 211) missed events where only one particle's PID was wrong (or 0)
        * Condition has now been updated to be (PID_el != 11 || PID_pip != 211) instead
    * Added the Hx vs Hy plots but only for Q2-y Bin All (Bin -1)
        * Also does not run while smearing
        * Should/will be used to check edge cuts to (hopefully) improve agreement between data and MC
    * Removed the production of the old construction of the 3D response matrix (now just using the variable definitions like the 5D response matrix)
* git commit notes for ExtraAnalysisCodeValues.py:
    * Discovered (and fixed) an issue with the background cuts
        * The condition (PID_el != 11 && PID_pip != 211) missed events where only one particle's PID was wrong (or 0)
        * Condition has now been updated to be (PID_el != 11 || PID_pip != 211) instead
* git commit notes for all sbatch_SIDIS_(...).sh Files:
    * Added "#SBATCH --constraint=el7"
    * Running '5D_Unfold_Test_V7'
        * Not running Sim_Test again (yet)

### Update on 5-23-2024:
* ADDING NEW FILE: Fit_Parameter_Comparison.ipynb
    * Meant to help search and evaluate the Parameter text files
    * Still in early test phase
* git commit notes for RooUnfold_SIDIS_richcap.py:
    * Added several 'raise TypeError()' instead of 'FAIL' or 'STOP' (meant to stop the code from running when encountering certain specific errors)
    * Modified code related to Sim_Test
        * Plotting the 'tdf' distributions where the 'SVD' method used to be drawn in the smaller individual images
        * Removed ability to smear during the simulated unfolding tests (not necessary)
        * Added the background distribution to the simulated 'rdf' plots since with the background identified, the plot to be unfolded should also include those distributions as well
        * Running Sim_Test with Pass 2
* git commit notes for sbatch_SIDIS_unfold_python.sh:
    * Running Sim_Test with Pass 2
    * No need to run the smeared option for Sim_Test
* git commit notes for Bayes_RooUnfold_SIDIS_Iteration_Test.py:
    * Running Sim_Test for Pass 2
    * Added a few lines to more readily delete unnecessary histograms/objects to try to save a little more memory
    * Added 'sys.stdout.flush()' to (hopefully) have the .out log files update more often so that more information about the code's progress/crash point may be observed
* git commit notes for bayes_RooUnfold_SIDIS_Iteration_Test.sh:
    * Increased memory request from 18000 to 19000
        * Hoping that the few updates to Bayes_RooUnfold_SIDIS_Iteration_Test.py might make it more efficient, but still requesting a bit more in the hopes that it further improves the chances of success
* git commit notes for sbatch_SIDIS_python_gen_MC_Pass2.sh/sbatch_SIDIS_python_matching_MC_Pass2.sh
    * Running modulated MC test for Pass 2
* git commit notes for Analysis_Notebook_SIDIS_richcap.ipynb
    * General update (no changes)

### Update on 5-22-2024:
* git commit notes for RooUnfold_SIDIS_richcap.py:
    * Added the new 3D response matrix method for unfolding (now working)
        * The original method is now named "Old" in all titles
        * Multi_Dim_Option for the new 3D response matrix is "3D" while the old option remains "Only"
        * Currently not running the old method anymore
    * Modified the Bin-by-Bin Correction to now use the RooUnfold version of the corrected plots
        * Have not yet checked to make sure that the methods are still identical (must do only to ensure that there are no bugs in the correction methods)
* git commit notes for sbatch_SIDIS_unfold_python.sh:
    * Running with txt file output for the fit parameters (changed from 'no_txt' option to 'no_stat' option)
    * Added more mem-per-cpu (required for making the txt files)
    * Added #SBATCH --constraint=el7 to force the sbatch job to run on the same network that I usually used
        * The ifarm updates have switched to el9 as the default which is not currently compatible with this code
* git commit notes for Bayes_RooUnfold_SIDIS_Iteration_Test.py:
    * Added the function for Multi3D_Slice() (Commented out since it is not in use)
    * Added functions/images to show the change in bin content/error between bayesian iterations
    * Running tests with the bayesian iterations
        * See notes on bayes_RooUnfold_SIDIS_Iteration_Test.sh
        * Will likely be trying to improve memory efficiency where possible in future updates
* git commit notes for bayes_RooUnfold_SIDIS_Iteration_Test.sh:
    * Running tests with more memory requested (able to run but still runs out of memory before the script finishes)
    * Similar update as sbatch_SIDIS_unfold_python.sh regarding #SBATCH --constraint=el7


### Update on 5-17-2024:
* git commit notes for RooUnfold_SIDIS_richcap.py:
    * Removed Draw_2D_Histograms_Simple(…) (now just using Draw_2D_Histograms_Simple_New(…))
    * Cleaned up/Updated Large_Individual_Bin_Images(…)/Draw_2D_Histograms_Simple_New(…)
        * Removed old comments
        * Fixed bug(s) related to bins/missing mass cut lines not being drawn in some images
        * Added MC Background plots to Large_Individual_Bin_Images(…) 
            * Switched places with Acceptance/Response matrix which is now drawn next to the Q2-xB plot
        * Made the horizontal size of the images controlled by these functions bigger
            * Was ‘Size_X=2400’ —> Now is ‘Size_X=2600’
    * Working on the newer method of performing the 3D unfolding (based on method used for the creation of the 5D response matricies)
        * Work-in-progress
        * Added (but not using) Multi3D_Slice(...) function
    * Added notification of what Pass version is in use that can be seen while the code is running (shows just before which files are loaded)
* For other commit note for other files other than RooUnfold_SIDIS_richcap.py, see the individual commits


### Update on 5-15-2024:
* Many notes made within individual files or in the git commit notes
    * Following update is not comprehensive towards all updates made since last note below (i.e., Update on 9-6-2023)
* Main update note here is for RooUnfold_SIDIS_richcap.py as of its last commit prior to this note. Noteworthy changes being committed are as follows:
    * Removed some unnecessary imports
    * Added 5D unfolding via sliced Response Matrices
        * Constructing a full 5D Response Matrix with a TH2D histogram was proving to be too memory demanding, so these slices are saved instead to be reconstructed later (saves on memormy when writing the histograms)
    * Using files with Common_Name = "5D_Unfold_Test_V3_All", "5D_Unfold_Test_V4_All", and "5D_Unfold_Test_V5_All" for Pass 1 and Pass 2
        * Different file versions were used for rdf, gdf, and mdf due to differences and bug fixes in each datatype
    * 5D Response Matrix does not flip the TH2D's axis (assumes that the generated events are already on the x-axis)
    * Added plot option for showing the background events (only)
        * Still in the testing phase (has been seen working for the 5D plots but issues with the lower dimensions have not yet been confirmed as being resolved - current test should demonstrate whether the problems have all been fixed)
    * Added the 5D-Multidimensional Rebuild Function (Rebuild_Matrix_5D(...))
    * Trying to fix issue with showing the total number of entries in individual histograms (some are being drawn in less than ideal locations)
        * Fit Parameters are now being shown in the proper locations but some statboxes that just show the number of events are still being drawn over more useful information

### Update on 9-6-2023:
* Some updates were not listed in these notes (see code and individual commits for more details)
    * Updated File_Name_Updates.md with the File name updates (still in makeROOT_epip_SIDIS_histos_new.py as well)
* Updated some of the "To-do" items above (not adding new items at this time)
* Deleting some old root files from the repository which are no longer in use
* File name "Gen_Cuts_V7_" had issues with the new 'Gen_MM_Cut' variable that was added (caused issues with the multidimensional closure tests)
    * The multidimensional histograms for the "Gen_Cuts_V7_" files cannnot be trusted
    * This was the same update that the MC Modulations were added
* Added new txt files which are made to record the kinematic comparisons when RooUnfold_SIDIS_richcap.py is made
    * RooUnfold_SIDIS_richcap_sort.py does not (currently) sort these files
    * Code written to help read these files is being tested in Analysis_Notebook_SIDIS_richcap.ipynb
* File name is now up to "Gen_Cuts_V8_"
    * Code has not yet finished testing this version of the files



### Update on 6-20-2023:
* External issues on work directory is putting a limit on the number of files that can be made and saved
    * This update is mainly meant to prevent any important file from being lost
    * All files that were modified were committed even if updates are minimal/unnoted
* File name is now up to "Gen_Cuts_V2_"

### Update on 6-15-2023:
* Running multiple versions of the multidimensional unfolding (testing up to 5D)
* Starting to implement new smearing function
* Testing new Missing Mass Cuts to the generated events
* File name is now up to "Gen_Cuts_V1_"


### Update on 6-2-2023:
* Updated the code to use Q2-y bins and fixed many issues with the code
    * Q2-xB bins are still not working as of this update, with the problem being the 'TH2Poly' object which consumes a lot of memory and takes to much extra time to create for each event (must fix by finding a way to create it once and use the same 'TH2Poly' object for each event in the dataframe)
    

### Update on 4-21-2023:
* Updated the 'makeROOT_epip_SIDIS_histos_new.py' code (removed a lot of unnecessary code among other changes)
    * See "File_Name_Updates.md" for more details
* Updated the 'RooUnfold_SIDIS_richcap.py' code a little to improve the visual appearance of the images
    * Will likely require some new rewrites to clean up the code soon (there are a lot of commented/inefficient examples of code which could be cleaned up in a later update)
        * This note is not something new, but rather is included here to add to the To-do list above (not significant enough to add as a priority at this time)


### Update on 4-16-2023:
* Added new markdown file called "File_Name_Updates.md" which will contain the individual update notes for each file made by the python code
    * Many (now older) updates are included in the python code where 'Extra_Name' is defined (notes about other files are not detailed as much at the time of this commit)
* Updated To-do List above
* Not (currently) committed changes to some files such as "Analysis_Notebook_SIDIS_richcap.ipynb" or "RooUnfold_SIDIS_richcap.py"
    * Have not checked what these changes are in a long enough time that additional reviews will be done to make sure the updates committed work as intended
* Preparing for new updates for post-Collaboration+APS meetings (saving updates before making major changes while 'cleaning-up' the code)


### Update on 3-9-2023:
* Updated up to the APS analysis note (see individual files for more details - from 'Unfolding_Tests_V14_' to 'Multi_Dimension_Unfold_V3_')
* Working on Multi-dimensional unfolding plots


### Update on 2-15-2023:
* Added new python code to create and sort images for the different unfolding methods
* Updated how images are saved to make it easier to upload to the (new) webpage
* Making updates (in-progress) for "Unfolding_Tests_V14_" including:
    * New Smearing function
    * Fixing issues with the (new) multidimension variable creation function
    * Changing the phase space histograms (in 'Mom_Cor_Code') to include the particle momentum instead of the sector information


### Update on 12-1-2022:
* Made major revisions to the jupyter notebook and python code within the new files called "Analysis_Notebook_SIDIS_richcap.ipynb" and "makeROOT_epip_SIDIS_histos_new.py"
    * This update is in effect as of the file for: Extra_Name = "Unfolding_Tests_V2_"
    * The new code uses different naming schemes to save the histograms


### Update on 11-14-2022:
* Moved all code to the work directory due to corrupted git file
* Added the .gitignore file
* Will be reworking the Jupyter notebook (cleaner version will be "SIDIS_rga_richcap_python_new.ipynb")


### Update on 11-3-2022:
* Groovy Code moved to work directory (safer than keeping these files on the volatile directory)
* Filtered unmatched events from the "normal" 2D Response Matrices (necessary for proper matrix construction when not using pre-defined bin numbers)
* Code created AFTER the DNP/CLAS Collaboration meeting(s) will have the name: "Unfolding_Tests_V#_"


### Update on 9-22-2022:
* Updated to Extra_Name = "Mom_Cor_Response_Matrix_V5_"
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

### Update on 9-15-2022:
* Updated to Extra_Name = "Mom_Cor_Response_Matrix_V3_"
* Added (initial/incomplete) Unfolding procedure to jupyter file

### Update on 9-7-2022:
#### Python Code Updates:
* Made improvements/additions to bin migration (now the better version will be response matrix)
* Cleaned up some unused code
* Began to add options for multi-dimensional binnings that require both the Q2-xB and z-pT bins be defined

Note on this commit: Data files used for this analysis have been lost. Must recover before running again

### Update on 8-24-2022:
#### Python Code Updates:
* Ran ∆P plots based on the REC-to-GEN MC matching
* Improved naming of histograms (their object names in the TFile)
* Added 'W' and 'Bin_4D' histograms
* Extra_Name = "Mom_Cor_Delta_P_Studies_" output files added
#### Jupyter Code Updates:
* Added more to the Missing Mass Histograms
    * Working towards integrating parts of the momentum correction code (from exclusive reactions) to this code
    

### Update on 8-21-2022:
#### Python Code Updates:
* Needed to rerun MC REC files (out-of-memory error)
    * Reduced number of options to improve memory-consumption
        * Removed multiple Bin Test option (Bin Migration V3 only - uses same number of bins used in regular histograms)
        * Removed Missing Mass histograms that would be produced when matching effiecency is considered (i.e., 'pdf' option is skipped for these histograms)
        * Removed histograms which are purely used to show 1D matching effeciency (not acceptance matrix)
* Removed old binning scheme options that were not being used
* Extra_Name = "Bin_Test_Mom_Cor_Studies_" output files added (MC REC files are named "Bin_Test_Mom_Cor_Studies_V2_" due to the memory errors mentioned above)


### Update on 8-20-2022:
#### Python Code Updates:
* Added More Cut options
    * 'Complete' Cut option applies all cuts (including new Q2 and Valerii's cuts)
    * Separate options for Missing Mass Cuts (split between 'EDIS' and 'SIDIS' where the 'EDIS' option uses the Exclusive Missing Mass Cuts - 'SIDIS' option uses the original SIDIS Missing Mass Cuts)
* Added ∆P histograms to study the effects of the Momentum Corrections (and develop better momentum smearing functions of the simulated data - future work)
* Missing Mass Histograms (and ∆P Histograms) now plotted with Particle Momentum AND Sector
* Extra_Name = "Bin_Test_Exclusive_Mom_Cor_" output files have been set up but NOT added yet (have not been run yet)
#### Jupyter Code Updates:
* Added new cell to more effiecently study the Momentum Correction/Missing Mass/∆P histograms
* Also added functions to slice and fit the above histograms
* Cleaned up unused/old code that was no longer in use
    

### Update on 8-18-2022:
#### Python Code Updates:
* Added Exclusivity Cuts option
    * Used to check the effects of the momentum corrections (not applied to the MC generated data)
    * Does work with MC reconstructed smearing
* Extra_Name = "Bin_Test_Exclusive_Mom_Cor_" output files have been set up but NOT added yet (have not been run yet)
#### General Updates:
* Updated other files (small updates) 
* Added Notes_and_Ideas.md file for an additional place to write down ideas for future projects/things to look into
    * Was using this file for this purpose but the files are now split to more easily read these updates


### Update on 8-15-2022:
#### Python Code Updates:
* Added Momentum Corrections to the experimental data set
    * Corrections are a option that can be turned on and off before creating the root histogram files
* Removed option to smear any dataset that is not the MC reconstructed files
    * Option was removed with code previously, but this update will (ideally) reduce the overall size of the dataframes by eliminating useless information
* Added 5D kinematic binning to dataframe (some additional histogram options may be possible - have not created them yet)
    * Size of these histograms may limit application prior to unfolding (number of histogram bins exceed 11000)
* "Cleaned-up" other parts of code to simplify overall body of code (i.e., removed repetitive/unnecessary lines of code)
* Extra_Name = "Bin_Test_Mom_Cor_" output files have been set up but NOT added yet (have not been run yet)
    


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
See File_Name_Updates.md for updates by file