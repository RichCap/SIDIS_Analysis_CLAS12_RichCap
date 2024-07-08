# Update Notes by File
The notes in this file contain information about individual file updates made with the python code called "makeROOT_epip_SIDIS_histos_new.py".
These notes are made inside the python code whenever a new set of histograms are made (see where the 'Extra_Name' string is defined to see the most recent notes).
This file will break down individual git updates into the different files that were made between commits, since mutliple files may sometimes be made before they are all Committed.
See the README.md file for more general updates (especially those which pertain to things outside of the updates to the python code)


# (SIDIS) Notes Committed on 7-8-2024:
The following notes were all related to the SIDIS Analysis files but exclude those made to test/develop the momentum smearing functions (see below)

# Extra_Name = "New_Binning_Schemes_V6_"
* Switched to the new Q2-y binning but switched the names so that the Q2-y binning scheme used in the last version of this code is now referred to by "Y_bin" while the new binning scheme uses 'y_bin' (will make updating the other files easier)
* Removed the MM and W to the 1D histogram options (no longer running)
* Smearing is still turned off (not needed at this time)
* Fixed the issue with the 'Multi_Dim' variables' code (was not using the generated information propperly)


# Extra_Name = "New_Binning_Schemes_V7_"
* Added the z-pT bins for the new y-binning scheme
* Smearing is still turned off (not needed at this time)
* Fixed issues with the 'Multi_Dim' binning function (should work correctly now)
* Added new 2D plots for W vs Q2/y and xB vs y (three new plots)
    * Added later (ran a second time without renaming on 6-12-2023) 


# Extra_Name = "New_Binning_Schemes_V8_"
* Added a 5D response matrix by defining a new 4D Bin variable based on the Q2-xB-z-pT bins
    * The 4D variable has a total of 566 bins while the 5D Response Matrix only uses 12 bins for the phi_t variable to limit the memory consumption of creating a histogram with more than 12000 bins (with only 12 phi_t bins, the 5D response matrix should have about 6792 bins)
    * Needed to be fixed after starting to run - the 'Multi_Dim' response matrices no longer use 3D histograms to slice with the z-pT bins
* Smearing is still turned off (not needed at this time)


# Extra_Name = "Gen_Cuts_V1_"
* Added new Missing Mass Cut to the generated events (to both 'gdf' and 'gen' - i.e., all matched/unmatched generated events are cut)
    * First test of the generated missing mass cut
    * The Missing Mass Cut starts at 1.5 GeV (just like the normal cut to the reconstructed events)
* Smearing function was modified with a new smearing factor (and slightly modified function)
* Modified the 5D histogram to use 24 phi_t bins again instead of 12
* Removed the 2D plots for W vs Q2/y and xB vs y (three of the 2D plots)


# Extra_Name = "Gen_Cuts_V2_"
  * Turned off Generated Missing Mass Cut
  * Otherwise is the same as "Gen_Cuts_V1_"


# Extra_Name = "Gen_Cuts_V3_"
  * Generated Cut is not turned on
  * Added the Missing Mass unfolding histogram
  * Modified the number of bins used to plot the 2D z vs pT histograms (did not change the binning scheme itself yet)


# Extra_Name = "Gen_Cuts_V3_Mom_Cor_"
  * Same as 'Gen_Cuts_V3_' but running the momentum correction histograms instead
      * Starting to add the new z-pT bins but not fully updated yet
  * Using smear_factor = 0.8
  * Still using the same MC Momentum Corrections from Unsmeared distribution


# Extra_Name = "Gen_Cuts_V3_Mom_Cor_V2_"
  * Same as 'Gen_Cuts_V3_' but running the momentum correction histograms instead
      * Added the new z-pT bins but not fully tested yet
  * Using smear_factor = 0.75


# Extra_Name = "Gen_Cuts_V3_Mom_Cor_V3_"
  * Same as 'Gen_Cuts_V3_' but running the momentum correction histograms instead
  * Using smear_factor = 0.5


# Extra_Name = "Gen_Cuts_V3_Mom_Cor_V4_"
  * Same as 'Gen_Cuts_V3_' but running the momentum correction histograms instead
  * Using smear_factor = 1.0


# Extra_Name = "Gen_Cuts_V3_Mom_Cor_FX_"
  * Same as 'Gen_Cuts_V3_' but running the momentum correction histograms instead
      * Using FX's smearing function


# Extra_Name = "Gen_Cuts_V4_"
  * Running with new z-pT bins for the Q2-y-z-pT scheme
      * Using fewer bins in some, but not all, cases
      * Data distribution in each bin should be improved (i.e., more evenly distributed)
  * Using fewer phi_h bins for the 5D Response Matrix
      * Current number of bins are as follows:
          * 512 Q2-y-z-pT bins
          * 10 phi_h bins per Q2-y-z-pT bin (36 degrees per bin)
          * TOTAL: 5120 bins
  * Using smear_factor = 0.75
  * No Generated Missing Mass Cuts at this time
  * Turned off MC Momentum Corrections


# Extra_Name = "Gen_Cuts_V5_"
  * Same as 'Gen_Cuts_V4_' except the MC Momentum Corrections are turn back on and a few errors in the Kinematic binning definitions
      * The momentum corrections, upon review, did not need to be turned off/updated (turning the corrections off was done because I forgot that I previously updated them from an inferior version)
      * One binning error was caused by a single missing bin that would throw off the binning scheme used to define the 4D bin variable (it only went up to 512 bins when it should have been 513)
      * Another binning error was with the Q2-y bin number 11 which had a few mistakenly defined z-pT bins (the number of bins was off and some improvements to how they were distributed were possible)
      * NEW number of Q2-y-z-pT bins is 506 (due to the correction of Q2-y bin 11)
          * Using fewer phi_h bins for the 5D Response Matrix
              * Current number of bins are as follows:
                  * 506 Q2-y-z-pT bins
                  * 10 phi_h bins per Q2-y-z-pT bin (36 degrees per bin)
                  * TOTAL: 5060 bins
  * Using smear_factor = 0.75


# Extra_Name = "Gen_Cuts_V5_No_Cor_"
  * Same as 'Gen_Cuts_V5_' except the MC Momentum Corrections are turn back off due to issues recognized in their development
      * Plotting Dp vs p_corrected causes issues in creating the iterative corrections which exists in this code while not existing in the prior Momentum Correction Development code that this procedure is based on
  * Using smear_factor = 0.75
      * The particle's angles are NOT being smeared
  * MC Momentum Corrections are OFF


# Extra_Name = "Gen_Cuts_V6_"
  * The MC Momentum Corrections are turn back ON after testing their new versions
      * Only 1 iteration of the correction per particle
  * Using smear_factor = 0.75
      * The particle's angles are NOT being smeared
  * Not making the 5D-Unfolding Histograms
      * Instead, making new 3D-Unfolding Histograms which unfold z+pT+phi_h together for each Q2-y Bin
  * Made some other minor changes (not present in "Gen_Cuts_V6_Mom_Cor_V*" - but should not affect the results)


# Extra_Name = "Gen_Cuts_V7_"
  * Was the same as "Gen_Cuts_V6_" when started running "SF_Testing_Mom_Cor_V1_" but updated later with new simulated phi_t modulations and MM_gen cuts
  * Added the Missing_Mass_Cut_Gen variable which has a value of -1 if the generated missing mass is below 1.5 GeV. Otherwise, it has a value of 1
      * This does not effect the experimental data histograms
      * These cuts are not available on the mdf 1D phi_h unfolding response matrices as they lack the extra available dimension to make use of the variable
          * Use the multidimensional unfolding plots instead
  * Added Modulations to the Monte Carlo phi_h distributions (effects generated and reconstructed distributions when turned on)
      * This closure test can be turned from the commandline by including "_mod" in the datatype input
      * Modulations are made by weighing the events based on calculations done with the generated phi_h value (using the same function phi_h will be ultimately fitted with)
          * Modulation parameters for this run are:
              * Par_B = -0.050
              * Par_C =  0.025
      * Modulations are applied to all response matrix plots and the 2D histograms
      * Modulations are not allowed as options when running code with the experimental data or for the momentum correction plots (no indication will be given in these cases, but for the other relevant cases, the code will print whether the closure test is being used)
  * Using smear_factor = 0.75


# Extra_Name = "Gen_Cuts_V8_"
  * Increased the modulations to the Monte Carlo phi_h distributions (increased Par_B by a factor of 10)
      * See 'Gen_Cuts_V7_' for first update
          * Modulation parameters for this run are:
              * Par_B = -0.500
              * Par_C =  0.025
      * Modulations are applied to all response matrix plots and the 2D histograms
      * Modulations are NOT allowed as options when running code with the experimental data or for the momentum correction plots
  * Tried to fix the 'Missing_Mass_Cut_Gen' variable (see See 'Gen_Cuts_V7_' for first update)
      * Now split the 'Gen_MM_Cut' into separate histograms from improved usage
          * A potential error occurred with a difference in the number of events in the 1D simulated unfolding closure tests and the 3D simulated unfolding closure tests
              * Possible cause may have been the lack of the 'Missing_Mass_Cut_Gen' variable in the 1D response matrices
          * The histograms which included 'Missing_Mass_Cut_Gen' in 'Gen_Cuts_V7_' are now split into two separate sets of histograms - one having the 'Missing_Mass_Cut_Gen' variable on an extra axis to be projected later and one that is the same as prior versions of the histogram (i.e., does not include 'Gen_MM_Cut')
          * The 1D Response matrices which did not include 'Missing_Mass_Cut_Gen' in the last update are now split into 3 histograms:
              * The 1st one is the same as before (i.e., no reference to 'Missing_Mass_Cut_Gen')
              * The 2nd one includes just the events that would be EXCLUDED by the Generated Missing Mass Cut (i.e., Missing_Mass_Cut_Gen < 0)
                  * Histogram name includes "Gen_Cut_MM" to pick it out from the other histograms
              * The 3rd one applies the Generated Missing Mass Cut as to only keep the events which survive the cut (i.e., Missing_Mass_Cut_Gen > 0)
                  * Histogram name includes "Gen_MM_Cut" to pick it out from the other histograms
                  * This name is identical to the part of the names of the other histograms which include 'Missing_Mass_Cut_Gen' as a plotted variable
  * Removed the Missing Mass 1D histograms and the 2D MM vs W histograms to reduce the number of histograms being created
      * These histograms were not in regular use at this time
  * Added new Multi_Dim histograms for the purpose of checking the phi_t distribution's dependence on the particles' lab angles
      * Wanted to study possible correlations between these angles and the additional modulations noticed in the phi_t distributions
      * Added elth, pipth, elPhi, and pipPhi
  * Attempted to fix parts of the histogram titles
      * Note: Do not use functions like SetTitle() in this code as they cause it to run much slower (not optimal for testing - likely would require the same amount of time to test as it would take to fully run the code to produce the root files)
  * Slightly modified how the response matrix histograms are saved to be slightly more compact (given that the additional histograms would make it even more difficult to save each one properly)
  * Using smear_factor = 0.75
  * Momentum Corrections are applied
  * Extending the 2D z vs pT plot ranges (not changing bin size)
      * Should be a visual change only - though the even number of bins should help slightly when rebinning during the kinematic comparisons (will avoid error messages)
  * Had to run twice due to a typo that deleted some important histograms


# Extra_Name = "New_Bin_Tests_V1_"
  * Ran on 9/27/2023
  * This file serves only to test new Q2-y Bins (and eventually new z-pT bins as well)
      * The response matrices needed for unfolding are not being run
      * Momentum smearing has also been turned off
  * Running new 3D histograms to plot each particle's kinematics versus the phi_h angle
      * The 3 3D histograms being run are grouped such that a single kinematic variable (i.e., p, theta, phi) for both the electron and pion is plotted vs eachother and phi_h
  * Made new 2D histogram dimensions for the Q2 vs y and z vs pT plots
      * The plots will include extended ranges for better coverage of the generated distributions and more refined binning
          * The y, z, and pT bins all have a width now of 0.01/bin while Q2 now has a bin width of 0.05/bin
  * Added new cut for inverting the MM cut (to see where events removed by this cut are comming from)


# Extra_Name = "New_Bin_Tests_V2_"
  * Ran on 10/3/2023
  * This file uses the original Q2-y binning scheme ('y_bin')
      * Testing of the newer scheme still ongoing
      * Still not smearing
  * No response matrices will be run
  * Only making 2D Histograms
      * Including new histograms for the lab phi angles vs phi_t
      * Not making any 3D or 1D histograms
  * New Cuts have been introduced (just cutting on generated missing mass)
      * Adding '_Gen' to the cut name makes the normal SIDIS missing mass cut on the generated events
      * Adding '_Exgen' to the cut name inverts the normal SIDIS missing mass cut on the generated events (i.e., sqrt(MM2_gen) < 1.5)


# Extra_Name = "New_Bin_Tests_V3_"
  * Ran on 10/4/2023
  * This file is mostly the same as "New_Bin_Tests_V2_" but returned to using the new Q2-y bins (for testing 'Y_bins')
      * Still not smearing
      * Added the generated missing mass cuts on MM_gen < 1.5
          * Is in addition to the inverted versions of these cuts that were run in "New_Bin_Tests_V2_"
  * Fixed minor issue with Q2_y_Bin = -3 (migration only)
      * Cut was not applied propperly


# Extra_Name = "New_Bin_Tests_V4_"
  * Ran on 10/11/2023
  * This file uses the original Q2-y binning scheme ('y_bin')
      * Still not smearing
  * This file is mainly used to study the additional phi_t modulations
      * More 2D Histograms of variables vs phi_t have been made including:
          * Electron/Pi+ Sectors (esec/pipsec)
          * Polar angles Theta of both particles
          * Momentum of both particles


# Extra_Name = "MultiDim_Bin_Test_V1_"
  * Ran on 11/1/2023-11/2/2023
  * This file uses the original Q2-y binning scheme ('y_bin')
      * Still not smearing
  * This file is mainly used to study the Multi-Dimensional phi_t histograms to ensure the 1st z-pT bin is constructed correctly for 3D unfolding
      * Turned Response Matrices back on
      * Turned off options from Extra_Name = "New_Bin_Tests_V4_"
      * Added cut on the generated events in z-pT bin 1 (applied to all Q2-y bins)
          * Cut is (basically) rdf = rdf.Filter("z_pT_bin_gen != 1")
              * See line 5991 (as of this note)
              * Cut may be inverted in a later test (ignore this note if this test idea proves to be unnecessary)
              * This cut should remove a single column from the flattened 3D response matrix
      * Removed all extra (generated missing mass) cuts used in prior tests (don't need them for this test)
      * Turned off all 2D histograms


# Extra_Name = "Sec_Cut_Test_V2_"
  * Ran on 11/21/2023
  * This file uses the original Q2-y binning scheme ('y_bin')
      * Still not smearing
      * Running with momentum corrections
  * Added a new alert to notify the user of the complete set of Response Matricies that are to be made when the code is run
      * Also added an optimizations condition which turns off the Response Matrix code automatically if List_of_Quantities_1D = [] (i.e., if the 1D histogram option is turned off)
      * See 'Alert_of_Response_Matricies'
  * This file is mainly used to study the additional phi_t modulations
      * Made as an extention of Extra_Name = "New_Bin_Tests_V4_"
          * Removed the cut added in Extra_Name = "MultiDim_Bin_Test_V1_" (was on line 5991 in the last note)
              * This cut is now on line 6025 as of this note, and can be found by searching for the following line of code:
                  * DF_Out = DF_Out.Filter("".join([str(str(z_pT_Bin_Filter_str).replace("_smeared", "")).replace("_gen", ""), "_gen != 1"]))
      * Added new set of cuts which cut on the electron sectors (to test the relationship between different sectors)
          * Investigation aims to see if the behavior of the modulations with respect to the pion sector changes when restricting the electron to specific sectors
          * Cuts on the electron sector are applied to both the generated AND reconstructed tracks simultaneously
          * Two versions of this cut are run alongside the typical analysis cuts used in this code:
              * 1) Cut 'eS1a' excludes events where the electron was detected in sector 1 of the detector (keeps all other events where the electron was detected in any other sector)
              * 2) Cut 'eS1o' requires all electrons to have been detected in sector 1 (opposite cut as 'eS1a')
              * These cuts can be added to any existing cut to be applied in addition to them
                  * Started to remove some other outdated code that was meant to perform this same type of cut
              * Cut Naming convension is: 
                  * 1st letter corresponds to the particle being cut (i.e.,'e' -> electron)
                  * 2nd letter is 'S' to signify that it is a Sector cut
                  * 3rd character/1st number corresponse to which sector is to be cut (i.e., '1' -> cut on sector 1)
                  * Last letter is either 'a' for 'all sectors' (just excludes the sector given in the cut's name) or 'o' for 'only' (removes all sectors not given in the cut's name)
                  * # Naming convension is not (currently) modular, so adding additional cuts of this nature will require them to be manually added
      * Set of 2D Histograms of variables vs phi_t in this file include:
          * Electron/Pi+ Sectors (esec/pipsec)
          * Lab Azimuthal angles (Phi) of both particles
          * Polar angles (Theta) of both particles
          * Momentum of both particles
      * Not running any 1D or 3D histogram options
   * ERROR NOTED ON 12/5/2023: Definitions of 'eS1a' and 'eS1o' were switched (cuts do not match their definitions above - corrected after the code was run)


# Extra_Name = "Sec_Cut_Test_V2_"
  * Ran on (Not Recorded)
  * This file uses the original Q2-y binning scheme ('y_bin')
      * Smearing option is still turned off (reset after running Extra_Name = "New_Smearing_V1_" - see below)
      * Running with momentum corrections
      * Reduced the bin options to just run the plots for all Q2-y bins and for Q2-y bin 3 (done to reduce the number of plots to be made due to the greater number of cuts being applied)
  * Added ability to weigh events based on the (generated) Q^4 value (for testing the extra modulations) - See below for when it is used
  * Still making the set of histograms used in "Sec_Cut_Test_V1_" to test the dependence of other variables with the extra modulations in phi_t
      * Error in how sectors are handled has caused these histograms to be skipped when plotting the sector vs the SMEARED phi_t angle (error only affects the smeared plots)
  * Added the ability to make other electron sector cuts like those that where introduced in "Sec_Cut_Test_V1_" (i.e., 'eS2o'-'eS6o' and 'eS2a'-'eS6a')
      * Running with all 'eS1o'-'eS6o' cuts (restricting to a specific electron sector)
  * Added new 3D histogram which shows the hit positions Hx and Hy as functions of the electron phi angle
      * These values are used in Valerii's cuts
      * The purpose of this plot is to help describe the fiducial cuts needed to help account for the edge effects in the electron detector sectors
  * Set of 2D Histograms of variables vs phi_t in this file have been reduced to only include:
      * Electron/Pi+ Sectors (esec/pipsec)
      * Lab Azimuthal angles (Phi) of both particles
  * Not running any Response Matrix histogram options


# Extra_Name = "New_Bin_Tests_V5_"
  * Ran on 1/26/2024
  * This file uses the new Q2-y/z-pT binning scheme ('Y_bin')
      * Initial tests of the new binning scheme with 3D unfolding
          * Future tests will try to rework the Multidimensional binning (new code contains the definitions of the 3D/5D kinematic bins that can be used with unfolding)
          * Current version calculates the multidimensional bin number in a more simplistic way (does not account for migration bins)
      * New binning scheme includes more migration bins (i.e., bins which are not meant to be analyzed but will provide details about events migrating into the main kinematic bins from outside the meaningful kinematic ranges)
  * Removed all non-standard options for histograms/cuts that are not required by the unfolding code


# Extra_Name = "New_Bin_Tests_V6_"
  * Ran on 2/14/2024
  * Running with the same binning scheme used in "New_Bin_Tests_V5_"
  * Added new background histogram which (currently) removes all matched generated events with a (generated) Missing Mass < 1.5
      * Also added cut on gdf file for MM > 1.5 (requirement --> is made by default to be included in the "no_cut" option)
  * Added the 3D Unfolding Bin variable to the 1D histogram list for initial test run
  * Running with the smearing function created with Extra_Name = "New_Smearing_V7_"


# Extra_Name = "CrossCheck_V1_"
  * Ran on 2/18/2024
  * Ran with original binning scheme ('y_bin')
  * Preforming cross-check with Timothy's plots (checking for Pass 1 and Pass 2)
  * Using same updates as mentioned in Extra_Name = "New_Bin_Tests_V6_"


# Extra_Name = "CrossCheck_V2_"
  * Ran on 2/19/2024
  * Made a mistake on the last version that prevented me from running any other Q2-y bin aside from bin 0 and 3
      * Fixed it to rerun with this version
  * Did not change anything else


# Extra_Name = "CrossCheck_V3_"
  * Ran on 2/21/2024
  * Fixed other mistakes that prevented the Background Subtraction plots to be made
  * Changed a few other unnecessary run options
  * Should be switching over to the new binning options soon (not in this update)


# Extra_Name = "New_Q2_Y_Bins_V1_"
  * Ran on 2/22/2024
  * Running with new Q2-y Bins (bin option = "Y_bins")
      * First complete run with the refined binning


# Extra_Name = "New_Q2_Y_Bins_V2_"
  * Ran on 2/25/2024
  * Running with new Q2-y Bins (bin option = "Y_bins")
  * Trying to improve memory consumption
      * Running without smearing
      * Running without GEN_MM_CUT plots
      * Running without 'MultiDim_z_pT_Bin_Y_bin_phi_t' (single def of 3D unfolding bins)
      * Removed z-pT overflow bins


# Extra_Name = "New_Q2_Y_Bins_V3_"
  * Ran on 3/5/2024
  * Running with new Q2-y Bins (bin option = "Y_bins")
  * Plots/Options added/removed:
      * (Still) running WITHOUT smearing
      * Running with Sector Cuts ('no_cut_eS1o'/'cut_Complete_SIDIS_eS1o')
      * Running with Electron/Pi+ Sectors (esec/pipsec) vs phi_t Plots
      * Removed 2D plots of pT vs phi_t
      * Not running the 1D MultiDim_z_pT_Bin_Y_bin_phi_t Plots (using regular 3D unfolding methods only)


# For 'mdf' only:
---
## Extra_Name = "New_Q2_Y_Bins_V3_Smeared_"
* Ran on 3/7/2024
* Same as Extra_Name = "New_Q2_Y_Bins_V3_" but the Monte Carlo is always smeared
    * For unsmeared plots, see the above version
    * Smearing is done with the simple smearing factor (used before ∆P/P)
    * Running same info for Pass 1 and Pass 2
## Extra_Name = "New_Q2_Y_Bins_V3_Smeared_V2_"
* Ran on 3/9/2024
* Same as Extra_Name = "New_Q2_Y_Bins_V3_Smeared_" but using a smearing factor of 1.75 instead of 0.75
---


# Extra_Name = "New_Q2_Y_Bins_V4_"
  * Ran on 3/26/2024 and 4/2/2024
  * Running with new Q2-y Bins (bin option = "Y_bins")
  * Plots/Options added/removed:
      * Running WITH smearing (Same as developed with Extra_Name = "Smear_Test_V10_")
          * Originally ran with smearing function developed with Extra_Name = "Smear_Test_V2_", but reran later with the updated version
      * Running with Sector Cuts ('no_cut_eS1o'/'cut_Complete_SIDIS_eS1o')
      * Running with Electron/Pi+ Sectors (esec/pipsec) vs phi_t Plots
      * Not running the 1D MultiDim_z_pT_Bin_Y_bin_phi_t Plots (using regular 3D unfolding methods only)
      * Doubled the binning for the electron/pion kinematic plots (i.e., lab p, theta, and phi plots)
      * Added optional Momentum Corrections from the input commands (default is to still run with the momentum corrections, but now they will not need to be manually turned on/off to run with appropriate data sets)
          * Pass 2 (Data) Momentum Corrections are now available
  * Had to rerun at a later date due to memory issues
      * It seems like the issue may have involved the fact that too many plots were being made all at once
      * Attempted Solution: Will run the smeared momentum separately from the unsmeared plots 
          * Only effects the reconstructed monte carlo options, but those were the only files that truly failed
          * MC generated plots had issues, but seemed to be able to successfully finish running
          * Will also try increasing the requested memory slightly


<hr style="border:2px solid gray">

# (Smearing) Notes Committed on 7-8-2024:
The following notes were all related to files created to test/develop the momentum smearing functions

# Extra_Name = "New_Smearing_V1_"
* Ran on 12/12/2023
* Updated with Extra_Name = "Sec_Cut_Test_V2_" (all the same notes therefore apply)
    * Turned off any cut not related to the Momentum Correction/Smearing code
* Added new form of the smearing plots to begin developing the smearing corrections as described in Valerii's procedure
* Added plots to see the impact of the smearing correction within each kinematic bin (hard-coded to use the current Q2-y binning scheme 'y_bin')

# Extra_Name = "New_Smearing_V2_"
* Ran on 2/5/2024
* Updated after Extra_Name = "New_Bin_Tests_V5_" (some of the same notes therefore apply, though see Extra_Name = "New_Smearing_V1_" for more significant details - newest update should not have a major effect on this version of the code)
    * Turned off any cut not related to the Momentum Correction/Smearing code
* Updated the ∆P/P plots to improve the binning ranges/sizes
* Changed the smearing function based on the new method (initially created with Extra_Name = "New_Smearing_V1_" - modified the original to include more bins, but overwrote it by accident)
    * To replicate the version used to create the new smearing function, run the code as it was on 12/12/2023 with the ∆P/P bins going from the same range as this version but with only 1000 bins
* NOTE MADE ON 2/6/2024: Bin resizing was not implemented correctly, still used a range of ∆P/P of -5 to 5 with only 500 bins
    
# Extra_Name = "New_Smearing_V3_"
* Ran on 2/6/2024
* Updated after Extra_Name = "New_Smearing_V2_" (all the same notes therefore apply)
    * Turned off any cut not related to the Momentum Correction/Smearing code
* Updated the ∆P/P plots to improve the binning ranges/sizes
    * Actually implementing the new bin ranges for the ∆P/P plots as was intended in the last version of this code
    * Using the same number of bins as I was originally (i.e., 500), but the new ranges are from -0.8 to 0.2 (instead of -5 to 5 with the same number of bins)
* The smearing function in use is the same one developed with the Extra_Name = "New_Smearing_V2_" version of the code (is replicable with the available version of Extra_Name = "New_Smearing_V2_")
* NOTE MADE ON 2/6/2024: Bin resizing was not implemented correctly: used a range of ∆P/P of -0.8 to 0.2 with 4000 bins

# Extra_Name = "New_Smearing_V4_"
* Ran on 2/6/2024
* Same update as Extra_Name = "New_Smearing_V3_" however the binning was corrected (see 'NOTE MADE ON 2/6/2024')

# Extra_Name = "New_Smearing_V5_"
* Ran on 2/12/2024
* New Smearing Function Test (also needed to convert from radians to degrees for the equations)
* Working on some other background/binning code with the other run option (i.e., not "mom")
    * Should not effect this version of the code
    
# Extra_Name = "New_Smearing_V6_"
* Ran on 2/13/2024
* New Smearing Function Test
    * Added an 'iterative' smearing function to the pion 
    * This is a test of whether iterative smearing is possible
    
# Extra_Name = "New_Smearing_V7_"
* Ran on 2/14/2024
* New Smearing Function Test
    * Added an 'iterative' smearing function to the electron (on top of the iterative smearing function tested in 'New_Smearing_V6_') 
    * Still trying to test if this is a viable method of smearing (last results were not conclusive)

# Extra_Name = "New_Smearing_V8_"
* Ran on 2/25/2024
* New Smearing Function Test
    * Added another iterative smearing function to the pion (on top of the iterative smearing function tested in 'New_Smearing_V7_') 
    * Modified prior functions to ensure that the smear_factor is always applied as 0.75 since that is what they were developed with (newer iterations can use different values of smear_factor without issue)
    * Final test before it might be better to use ∆P = P_gen - P_rec instead of P_calc - P_rec for the MC ∆P (still using the calculated version)

# Extra_Name = "".join(["New_Smearing_", str(smear_factor).replace(".", ""), "_V8_"])
## For smear_factor != "0.75"
* Same as "New_Smearing_V8_" but with any value of smear_factor not being equal to the default value of 0.75

# Extra_Name = "Smearing_Limit_V1_"
* Ran on 2/26/2024
* Running New Smearing Functions which put a limit of 'Smear_SF_Theta'
    * If Smear_SF_Theta < 0, then that means that the MC is OVERSMEARED (resolution of data is finer than MC)
* Cannot fix this issue with the current smearing function
    * The new limit sets Smear_SF_Theta = 0 if it shows signs of being oversmeared
* Added New Pass 2 smearing (without momentum correction)

# Extra_Name = "".join(["Smearing_Limit_", str(smear_factor).replace(".", ""), "_V1_"])
## For smear_factor != "0.75"
* Same as "Smearing_Limit_V1_" but with any value of smear_factor not being equal to the default value of 0.75
* This default may be changed soon (smear_factor > 1 may work better with the new form of the smearing functions)

# Extra_Name = "Smearing_Limit_V2_"
* Ran on 2/27/2024
* Same smearing function as Extra_Name = "Smearing_Limit_V1_" but now ∆P(MC) = P_Gen - P_Rec instead of ∆P = P_Calc - P_Rec
    * Last update somehow made the oversmearing problem worse? - Don't know why at the time of taking this note

# Extra_Name = "".join(["Smearing_Limit_", str(smear_factor).replace(".", ""), "_V2_"])
## For smear_factor != "0.75"
* Same as "Smearing_Limit_V2_" but with any value of smear_factor not being equal to the default value of 0.75
* This default may be changed soon (smear_factor > 1 may work better with the new form of the smearing functions)

# Extra_Name = "Smearing_Limit_V3_"
* Ran on 2/28/2024
* New smearing function based on using ∆P(MC) = P_Gen - P_Rec instead of ∆P = P_Calc - P_Rec
    * Using this to get the resolution of the MC lends itself more to easier smearing corrections which should not have to be iterative
* i.e., these corrections should be easier to get working and will keep each particle's correction independent of the other particle's kinematics

# Extra_Name = "".join(["Smearing_Limit_", str(smear_factor).replace(".", ""), "_V3_"])
## For smear_factor != "0.75"
* Same as "Smearing_Limit_V3_" but with any value of smear_factor not being equal to the default value of 0.75
* This default may be changed soon (smear_factor > 1 may work better with the new form of the smearing functions)

# Extra_Name = "Smear_Test_V1_"
* Ran on 3/8/2024
* Testing simple smearing factor SF (instead of smearing functions based on ∆P/P vs Theta)
    * Testing with Pass 2
    * Goes with the Extra_Name = "New_Q2_Y_Bins_V3_Smeared_" for the SIDIS plots and the Extra_Name = "New_Smearing_V4_" files for Pass 1 and the Extra_Name = "New_Smearing_V7_" files for Pass 2
    
# Extra_Name = "Smear_Test_V2_"
* Ran on 3/19/2024
* Testing smearing function where the SF is treated as error propagation (is based on ∆P/P vs Theta plots)
    * Testing with Pass 1 and Pass 2
    * Goes with the Extra_Name = "New_Q2_Y_Bins_V3_Smeared_" for the SIDIS plots and the Extra_Name = "New_Smearing_V4_" files for Pass 1 and the Extra_Name = "New_Smearing_V7_" files for Pass 2
    * Otherwise is the same as "Smear_Test_V1_"
    
# Extra_Name = "Smear_Test_V3_"
* Ran on 3/22/2024
* Same smearing function as Extra_Name = "Smear_Test_V2_" but using ∆P = P_Calc - P_Rec again instead of ∆P(MC) = P_Gen - P_Rec
* Also new plots to show the particle angles vs momentum per sector (4 new plots in total)
    * Reran for the Experimental data plots as well
    
# Extra_Name = "Smear_Test_V4_"
* Ran on 3/26/2024
* Same smearing function as Extra_Name = "Smear_Test_V3_" and still using ∆P = P_Calc - P_Rec again instead of ∆P(MC) = P_Gen - P_Rec
* Added new type of cut which restricts the events into a defined kinematic bin (applied on top of the other standard/existing cuts)
    * Changed the standard binning option to the new "Y_bin" option instead of the old "y_bin" bins
* Option has been added to run with the Pass 2 (Data) Momentum Corrections

# Extra_Name = "Smear_Test_V5_"
* Ran on 3/29/2024
* New smearing function for the Electron based on ∆P = P_Calc - P_Rec instead of ∆P(MC) = P_Gen - P_Rec
    * No Pion Smearing (yet)
* Removed all cuts except the Exclusive cuts (for faster run time)

# Extra_Name = "Smear_Test_V6_"
* Ran on 3/29/2024
* New smearing function for the Pion based on ∆P = P_Calc - P_Rec instead of ∆P(MC) = P_Gen - P_Rec
    * No Electron Smearing (yet)
    * Need to smear the pion first or else the electron smearing function will over-smear it
* Removed Smearing function used in Extra_Name = "Smear_Test_V5_"

# Extra_Name = "Smear_Test_V7_"
* Ran on 4/1/2024
* New smearing function for the Electron based on ∆P = P_Calc - P_Rec instead of ∆P(MC) = P_Gen - P_Rec
    * Got the new smearing function after smearing the pion (from Extra_Name = "Smear_Test_V6_")
* Needed to smear the pion first or else the electron smearing function would over-smear it

# Extra_Name = "Smear_Test_V8_"
* Ran on 4/1/2024
* Returning to the smearing function for the Pion from Extra_Name = "Smear_Test_V6_" and turned off the electron smearing
    * Only using the pion smearing for the same reasons previously mentioned
    * Major change: Smearing function now does P_smear = P_rec + Gaus(0, SF(Theta)) instead of P_smear = P_rec + SF(Theta)*Gaus(0, 1)
* SF(Theta) in this note represents a few different parameters contributing to the width
* SF(Theta) will still be 0 instead of being a negative number

# Extra_Name = "Smear_Test_V9_"
* Ran on 4/2/2024
* Created new smearing function for the Electron based on ∆P = P_Calc - P_Rec
    * Got the new smearing function after smearing the pion (from Extra_Name = "Smear_Test_V8_")
* Returned to using addtitional cuts beyond just the exclusivity cuts

# Extra_Name = "Smear_Test_V10_"
* Ran on 4/2/2024
* Reduced electron smearing by 50%
    * The electron smearing function from Extra_Name = "Smear_Test_V9_" caused the pion to be over smeared (reduced it to try and counter this effect)
    
# Extra_Name = "Smear_Test_V11_"
* Ran on 4/2/2024 and 4/4/2024
* Reduced electron smearing by 75% (from Extra_Name = "Smear_Test_V9_")
    * The electron smearing function from Extra_Name = "Smear_Test_10_" was reduced by too great of a factor (basically became negligible)
* Added the Pion Energy Loss Correction to the Pass 2 Experimental Data plots on 4/4/2024

# Extra_Name = "New_Smear_V1_"
* Ran on 4/12/2024
* Reworking the Pion Smearing with a slightly updated fitting procedure (same type of smearing with improved fitting methods to obtain the ∆sigma factor)
    * Smearing should take from the ∆P/P plots but the quality of the smearing is better left to checking the Missing Mass Plots and/or the normal ∆P plots, as the ∆P/P smeared plots seem to exaggerate over-smearing effects
* The ∆P/P plots do not seem to be ideally oriented towards making repeated iterative smearing corrections, but are able to obtain good smearing functions when the criteria is given by matching just ∆P or MM (likely do to the compound effects smearing ∆P and P when trying to plot ∆P/P)
* Removed SIDIS Cuts (Not needed for testing)
* All Pion Energy Loss and Momentum Corrections are included the Pass 2 Experimental Data plots (as of 4/4/2024)
    * Use with Extra_Name = "Smear_Test_V11_" (for Experimental Data)
    
# Extra_Name = "New_Smear_V2_"
* Ran on 4/12/2024
* New Electron Smearing (Based on Extra_Name = "New_Smear_V1_")
    * Not reducing the smear factor of the electron relative to the pion smearing as was done with previous versions (may cause the appearence of oversmearing in the ∆P/P plots as noted above)
* Still not including the SIDIS Cuts (Not needed for testing)
* All Pion Energy Loss and Momentum Corrections are included the Pass 2 Experimental Data plots (as of 4/4/2024)
    * Use with Extra_Name = "Smear_Test_V11_" (for Experimental Data)
    
# Extra_Name = "New_Smear_V3_"
* Ran on 4/12/2024
* New Electron Smearing (Based on Extra_Name = "New_Smear_V2_")
    * Reduced Electron Smearing by 25% (did not see the desired improvements, so reverted attempting to fix with less extreme electron smearing)
* Still not including the SIDIS Cuts (Not needed for testing)
* All Pion Energy Loss and Momentum Corrections are included the Pass 2 Experimental Data plots (as of 4/4/2024)
    * Use with Extra_Name = "Smear_Test_V11_" (for Experimental Data)
    
# Extra_Name = "New_Smear_V4_"
* Ran on 4/12/2024
* New Electron Smearing (Based on Extra_Name = "New_Smear_V2_")
    * Same as Extra_Name = "New_Smear_V3_" but testing other reducing factors (Currently reducing electron smearing by 35%)
    
# Extra_Name = "New_Smear_V5_"
* Ran on 4/12/2024
* Refined the Pion Smearing (Based on Extra_Name = "New_Smear_V4_")
    * Added extra layer of pion smearing on top of the existing smearing functions
    * Electron Smearing is still the same as Extra_Name = "New_Smear_V4_" (i.e., currently reducing electron smearing by 35%)
* Ran again on 4/17/2024 for the rdf datatype as there was a potential issue with the application of the Energy Loss Corrections
    * May create a need to rerun the smearing correction derivation
    
# Extra_Name = "New_Smear_V6_"
* Ran on 4/29/2024
* Added an extra criteria for the electron smearing function aimed at limiting the over-smearing seen in the ∆P/P plots for the pion
    * The criteria prevents the electron from being smeared if the pion polar angle is less than 15 degrees
    * The pion refinement added in "New_Smear_V5_" is also turned off in this region (since it was developed with the electron smearing in mind)
    
# Extra_Name = "New_Smear_V7_"
* Ran on 5/2/2024
* Changed extra criteria for the electron smearing function from "New_Smear_V6_"
    * The criteria prevents the electron from being smeared if the pion polar angle is less than 12.5 degrees or if the pion momentum is greater than 4.5 GeV
    * Increased the electron smearing by reducing the electron smearing factor by 5% instead of by 35% (functions remain the same)
    * The pion refinement added in "New_Smear_V5_" is also turned completely off
    
# Extra_Name = "New_Smear_V8_"
* Ran on 5/2/2024
* Changed extra criteria for the electron smearing function from "New_Smear_V7_"
    * Criteria now does not completely turn off the electron smearing in the specified region
* Now smearing is simply reduced by an additional 95% on top of the 5% reduction applied by default
    * Added additional condition for a less severe reduction in the electron smearing (pipth < 20)
* Reduction is 35% smaller than what Smear_SF_Theta would be otherwise
    * Goal is to better balance the electron and pion smearing and to improve the missing mass distribution comparisons
    * Otherwise is the same as "New_Smear_V7_"



<hr style="border:2px solid gray">
    
# Notes Committed on 9-6-2023:

# Extra_Name = "Gen_Cuts_V3_"
* Generated Cut is not turned on
* Added the Missing Mass unfolding histogram
* Modified the number of bins used to plot the 2D z vs pT histograms (did not change the binning scheme itself yet)

# Extra_Name = "Gen_Cuts_V3_Mom_Cor_"
* Same as 'Gen_Cuts_V3_' but running the momentum correction histograms instead
    * Starting to add the new z-pT bins but not fully updated yet
* Using smear_factor = 0.8
* Still using the same MC Momentum Corrections from Unsmeared distribution

# Extra_Name = "Gen_Cuts_V3_Mom_Cor_V2_"
* Same as 'Gen_Cuts_V3_' but running the momentum correction histograms instead
    * Added the new z-pT bins but not fully tested yet
* Using smear_factor = 0.75


# Extra_Name = "Gen_Cuts_V3_Mom_Cor_V3_"
* Same as 'Gen_Cuts_V3_' but running the momentum correction histograms instead
* Using smear_factor = 0.5


# Extra_Name = "Gen_Cuts_V3_Mom_Cor_V4_"
* Same as 'Gen_Cuts_V3_' but running the momentum correction histograms instead
* Using smear_factor = 1.0

# Extra_Name = "Gen_Cuts_V3_Mom_Cor_FX_"
* Same as 'Gen_Cuts_V3_' but running the momentum correction histograms instead
    * Using FX's smearing function


# Extra_Name = "Gen_Cuts_V4_"
* Running with new z-pT bins for the Q2-y-z-pT scheme
    * Using fewer bins in some, but not all, cases
    * Data distribution in each bin should be improved (i.e., more evenly distributed)
* Using fewer phi_h bins for the 5D Response Matrix
    * Current number of bins are as follows:
        * 512 Q2-y-z-pT bins
        * 10 phi_h bins per Q2-y-z-pT bin (36 degrees per bin)
        * TOTAL: 5120 bins
* Using smear_factor = 0.75
* No Generated Missing Mass Cuts at this time
* Turned off MC Momentum Corrections


# Extra_Name = "Gen_Cuts_V4_Mom_Cor_V1_"
* Same as 'Gen_Cuts_V4_' but running the momentum correction histograms instead
* Using smear_factor = 0.75
* No Generated Missing Mass Cuts at this time
* Turned off MC Momentum Corrections

# Extra_Name = "Gen_Cuts_V4_Mom_Cor_V2_"
* Same as 'Gen_Cuts_V4_Mom_Cor_V1_' but with a new smear_factor
* Using smear_factor = 0.5

# Extra_Name = "Gen_Cuts_V4_Mom_Cor_V3_"
* Same as 'Gen_Cuts_V4_Mom_Cor_V2_' but with a new smear_factor
* Using smear_factor = 1.0

# Extra_Name = "Gen_Cuts_V4_Mom_Cor_FX_"
* Same as 'Gen_Cuts_V4_Mom_Cor_V3_' but with FX's smearing function



# Extra_Name = "Gen_Cuts_V5_"
* Same as 'Gen_Cuts_V4_' except the MC Momentum Corrections are turn back on and a few errors in the Kinematic binning definitions
    * The momentum corrections, upon review, did not need to be turned off/updated (turning the corrections off was done because I forgot that I previously updated them from an inferior version)
    * One binning error was caused by a single missing bin that would throw off the binning scheme used to define the 4D bin variable (it only went up to 512 bins when it should have been 513)
    * Another binning error was with the Q2-y bin number 11 which had a few mistakenly defined z-pT bins (the number of bins was off and some improvements to how they were distributed were possible)
    * NEW number of Q2-y-z-pT bins is 506 (due to the correction of Q2-y bin 11)
        * Using fewer phi_h bins for the 5D Response Matrix
            * Current number of bins are as follows:
                * 506 Q2-y-z-pT bins
                * 10 phi_h bins per Q2-y-z-pT bin (36 degrees per bin)
                * TOTAL: 5060 bins
* Using smear_factor = 0.75


# Extra_Name = "Gen_Cuts_V5_Mom_Cor_V1_"
* Same as 'Gen_Cuts_V5_' but running the momentum correction histograms instead and ONLY SMEARING THE PARTICLE'S MOMENTUMS
    * The particle's angles are not being smeared
* Using smear_factor = 0.75
* No Generated Missing Mass Cuts at this time
* MC Momentum Corrections are ON

# Extra_Name = "Gen_Cuts_V5_Mom_Cor_V2_"
* Same as 'Gen_Cuts_V5_Mom_Cor_V1_' but with a new smear_factor
* Using smear_factor = 0.5

# Extra_Name = "Gen_Cuts_V5_Mom_Cor_V3_"
* Same as 'Gen_Cuts_V5_Mom_Cor_V1_' but with a new smear_factor
* Using smear_factor = 1.0


# Extra_Name = "Gen_Cuts_V5_No_Cor_"
* Same as 'Gen_Cuts_V5_' except the MC Momentum Corrections are turn back off due to issues recognized in their development
    * Plotting Dp vs p_corrected causes issues in creating the iterative corrections which exists in this code while not existing in the prior Momentum Correction Development code that this procedure is based on
* Using smear_factor = 0.75
    * The particle's angles are NOT being smeared
* MC Momentum Corrections are OFF



# Extra_Name = "Gen_Cuts_V5_No_Cor_Mom_Cor_V1_"
* Same as 'Gen_Cuts_V5_No_Cor_' but running the momentum correction histograms instead
    * The Particle Kinematics that are plotted in these histograms will be smeared along with the Missing Mass and ∆P/∆Theta variables
* Using smear_factor = 0.75
    * The particle's angles are NOT being smeared
* MC Momentum Corrections are OFF

# Extra_Name = "Gen_Cuts_V5_No_Cor_Mom_Cor_V2_"
* Same as 'Gen_Cuts_V5_No_Cor_Mom_Cor_V1_' but with a new smear_factor
* Using smear_factor = 0.5

# Extra_Name = "Gen_Cuts_V5_No_Cor_Mom_Cor_V3_"
* Same as 'Gen_Cuts_V5_No_Cor_Mom_Cor_V1_' but with a new smear_factor
* Using smear_factor = 1.0

# Extra_Name = "Gen_Cuts_V5_No_Cor_Mom_Cor_FX_"
* Same as 'Gen_Cuts_V5_No_Cor_Mom_Cor_V1_' but with FX's smearing function


# Extra_Name = "Gen_Cuts_V5_No_Cor_Mom_Cor_V4_"
* Same as 'Gen_Cuts_V5_No_Cor_Mom_Cor_V1_' but with a new smear_factor
* Using smear_factor = 0.7

# Extra_Name = "Gen_Cuts_V5_No_Cor_Mom_Cor_V5_"
* Same as 'Gen_Cuts_V5_No_Cor_Mom_Cor_V1_' but with a new smear_factor
* Using smear_factor = 1.5


# Extra_Name = "Gen_Cuts_V6_"
* The MC Momentum Corrections are turn back ON after testing their new versions
    * Only 1 iteration of the correction per particle
* Using smear_factor = 0.75
    * The particle's angles are NOT being smeared
* Not making the 5D-Unfolding Histograms
    * Instead, making new 3D-Unfolding Histograms which unfold z+pT+phi_h together for each Q2-y Bin
* Made some other minor changes (not present in "Gen_Cuts_V6_Mom_Cor_V*" - but should not affect the results)


# Extra_Name = "Gen_Cuts_V6_Mom_Cor_V1_"
* Same as 'Gen_Cuts_V6_' but running the momentum correction histograms instead
    * The Particle Kinematics that are plotted in these histograms will be smeared along with the Missing Mass and ∆P/∆Theta variables
* Using smear_factor = 0.75
    * The particle's angles are NOT being smeared
* MC Momentum Corrections are ON

# Extra_Name = "Gen_Cuts_V6_Mom_Cor_V2_"
* Same as 'Gen_Cuts_V6_Mom_Cor_V1_' but with a new smear_factor
* Using smear_factor = 0.5

# Extra_Name = "Gen_Cuts_V6_Mom_Cor_V3_"
* Same as 'Gen_Cuts_V6_Mom_Cor_V1_' but with a new smear_factor
* Using smear_factor = 1.0

# Extra_Name = "Gen_Cuts_V6_Mom_Cor_FX_"
* Same as 'Gen_Cuts_V6_Mom_Cor_V1_' but with FX's smearing function


# Extra_Name = "Gen_Cuts_V6_Mom_Cor_V4_"
* Same as 'Gen_Cuts_V6_Mom_Cor_V1_' but with a new smear_factor
* Using smear_factor = 0.7

# Extra_Name = "Gen_Cuts_V6_Mom_Cor_V5_"
* Same as 'Gen_Cuts_V6_Mom_Cor_V1_' but with a new smear_factor
* Using smear_factor = 1.5

# Extra_Name = "Gen_Cuts_V6_Mom_Cor_V6_"
* Same as 'Gen_Cuts_V6_Mom_Cor_V1_' but with a new smear_factor
* Using smear_factor = 0.9

# Extra_Name = "Gen_Cuts_V6_Mom_Cor_V7_"
* Same as 'Gen_Cuts_V6_Mom_Cor_V1_' but with a new smear_factor
* Using smear_factor = 0.8



# Extra_Name = "Gen_Cuts_V7_"
* Was the same as "Gen_Cuts_V6_" when started running "SF_Testing_Mom_Cor_V1_" but updated later with new simulated phi_t modulations and MM_gen cuts
* Added the Missing_Mass_Cut_Gen variable which has a value of -1 if the generated missing mass is below 1.5 GeV. Otherwise, it has a value of 1
    * This does not effect the experimental data histograms
    * These cuts are not available on the mdf 1D phi_h unfolding response matrices as they lack the extra available dimension to make use of the variable
        * Use the multidimensional unfolding plots instead
* Added Modulations to the Monte Carlo phi_h distributions (effects generated and reconstructed distributions when turned on)
    * This closure test can be turned from the commandline by including "_mod" in the datatype input
    * Modulations are made by weighing the events based on calculations done with the generated phi_h value (using the same function phi_h will be ultimately fitted with)
        * Modulation parameters for this run are:
            * Par_B = -0.050
            * Par_C =  0.025
    * Modulations are applied to all response matrix plots and the 2D histograms
    * Modulations are not allowed as options when running code with the experimental data or for the momentum correction plots (no indication will be given in these cases, but for the other relevant cases, the code will print whether the closure test is being used)
* Using smear_factor = 0.75



# Extra_Name = "SF_Testing_Mom_Cor_V1_"
* Same as 'Gen_Cuts_V7_'/'Gen_Cuts_V6_' but running the momentum correction histograms instead
    * The Particle Kinematics that are plotted in these histograms will be smeared along with the Missing Mass and ∆P/∆Theta variables
* Using smear_factor = 0.75
    * The particle's angles are NOT being smeared
* MC Momentum Corrections are ON
* Added MM and Dp vs local phi plots

# Extra_Name = "SF_Testing_Mom_Cor_V2_"
* Same as 'SF_Testing_Mom_Cor_V1_' but with a new smear_factor
* Using smear_factor = 0.5

# Extra_Name = "SF_Testing_Mom_Cor_V3_"
* Same as 'SF_Testing_Mom_Cor_V1_' but with a new smear_factor
* Using smear_factor = 1.0

# Extra_Name = "SF_Testing_Mom_Cor_FX_"
* Same as 'SF_Testing_Mom_Cor_V1_' but with FX's smearing function

# Extra_Name = "SF_Testing_Mom_Cor_V4_"
* Same as 'SF_Testing_Mom_Cor_V1_' but with a new smear_factor
* Using smear_factor = 0.7

# Extra_Name = "SF_Testing_Mom_Cor_V5_"
* Same as 'SF_Testing_Mom_Cor_V1_' but with a new smear_factor
* Using smear_factor = 1.5

# Extra_Name = "SF_Testing_Mom_Cor_V6_"
* Same as 'SF_Testing_Mom_Cor_V1_' but with a new smear_factor
* Using smear_factor = 0.9

# Extra_Name = "SF_Testing_Mom_Cor_V7_"
* Same as 'SF_Testing_Mom_Cor_V1_' but with a new smear_factor
* Using smear_factor = 0.8

# Extra_Name = "SF_Testing_Mom_Cor_V8_"
* Same as 'SF_Testing_Mom_Cor_V1_' but with a new smear_factor
* Using smear_factor = 1.2

# Extra_Name = "SF_Testing_Mom_Cor_V9_"
* Same as 'SF_Testing_Mom_Cor_V1_' but with a new smear_factor
* Using smear_factor = 2.0


# Extra_Name = "Gen_Cuts_V8_"
* Increased the modulations to the Monte Carlo phi_h distributions (increased Par_B by a factor of 10)
    * See 'Gen_Cuts_V7_' for first update
        * Modulation parameters for this run are:
            * Par_B = -0.500
            * Par_C =  0.025
    * Modulations are applied to all response matrix plots and the 2D histograms
    * Modulations are NOT allowed as options when running code with the experimental data or for the momentum correction plots
* Tried to fix the 'Missing_Mass_Cut_Gen' variable (see See 'Gen_Cuts_V7_' for first update)
    * Now split the 'Gen_MM_Cut' into separate histograms from improved usage
        * A potential error occurred with a difference in the number of events in the 1D simulated unfolding closure tests and the 3D simulated unfolding closure tests
            * Possible cause may have been the lack of the 'Missing_Mass_Cut_Gen' variable in the 1D response matrices
        * The histograms which included 'Missing_Mass_Cut_Gen' in 'Gen_Cuts_V7_' are now split into two separate sets of histograms - one having the 'Missing_Mass_Cut_Gen' variable on an extra axis to be projected later and one that is the same as prior versions of the histogram (i.e., does not include 'Gen_MM_Cut')
        * The 1D Response matrices which did not include 'Missing_Mass_Cut_Gen' in the last update are now split into 3 histograms:
            * The 1st one is the same as before (i.e., no reference to 'Missing_Mass_Cut_Gen')
            * The 2nd one includes just the events that would be EXCLUDED by the Generated Missing Mass Cut (i.e., Missing_Mass_Cut_Gen < 0)
                * Histogram name includes "Gen_Cut_MM" to pick it out from the other histograms
            * The 3rd one applies the Generated Missing Mass Cut as to only keep the events which survive the cut (i.e., Missing_Mass_Cut_Gen > 0)
                * Histogram name includes "Gen_MM_Cut" to pick it out from the other histograms
                * This name is identical to the part of the names of the other histograms which include 'Missing_Mass_Cut_Gen' as a plotted variable
* Removed the Missing Mass 1D histograms and the 2D MM vs W histograms to reduce the number of histograms being created
    * These histograms were not in regular use at this time
* Added new Multi_Dim histograms for the purpose of checking the phi_t distribution's dependence on the particles' lab angles
    * Wanted to study possible correlations between these angles and the additional modulations noticed in the phi_t distributions
    * Added elth, pipth, elPhi, and pipPhi
* Attempted to fix parts of the histogram titles
    * Note: Do not use functions like SetTitle() in this code as they cause it to run much slower (not optimal for testing - likely would require the same amount of time to test as it would take to fully run the code to produce the root files)
* Slightly modified how the response matrix histograms are saved to be slightly more compact (given that the additional histograms would make it even more difficult to save each one properly)
* Using smear_factor = 0.75
* Momentum Corrections are applied


<hr style="border:2px solid gray">

# Notes Committed on 6-20-2023:

## Extra_Name = "Gen_Cuts_V1_"
 * Added new Missing Mass Cut to the generated events (to both 'gdf' and 'gen' - i.e., all matched/unmatched generated events are cut)
     * First test of the generated missing mass cut
     * The Missing Mass Cut starts at 1.5 GeV (just like the normal cut to the reconstructed events)
 * Smearing function was modified with a new smearing factor (and slightly modified function)
 * Modified the 5D histogram to use 24 phi_t bins again instead of 12
 * Removed the 2D plots for W vs Q2/y and xB vs y (three of the 2D plots)
    
    
## Extra_Name = "Gen_Cuts_V2_"
* Turned off Generated Missing Mass Cut
* Otherwise is the same as "Gen_Cuts_V1_"


<hr style="border:2px solid gray">

# Notes Committed on 6-15-2023:

## Extra_Name = "New_Binning_Schemes_V1_"
* Added option to make 3D histograms with 3 unique variables (instead of just using the z-pT binning as the 3rd variable always)
* Made a new binning scheme option of "Off" which allows you to run this code without the kinematic bin calculations (all Q2-xB and z-pT bins are automatically assigned to have the value of 1)
    * Still need to work on aspects of the default code which are causing it to run very slowly -> believed to be related to the new method for calculating the kinematic bins
* 'mdf' no longer runs the 'gen' option for histograms
* Minor improvements to how the binning schemes' names are referenced within the code (mainly made notes to be more accepting of the alternative bin names - should not effect how the code runs)
    * Did include more lines to skip the Q2-xB bins outside of the binning scheme in use (safety measure to help prevent possibly unnecessary histogram creation)
        
## Extra_Name = "New_Binning_Schemes_V2_"
* Added new binning type (Q2-y bins)
    * Only ran this scheme
* New Q2 1D binning scheme (new number of bins and range)
    
## Extra_Name = "New_Binning_Schemes_V3_"
* Only making the normal 2D histograms (removed the 3D histos)
    * Also plotting W and Mx
        
## Extra_Name = "New_Binning_Schemes_V4_"
* Added the z-pT binning for y_bin option
* Added one additional Q2-y bin to the scheme (high Q2 but likely has very low event counts - may not be usable)
* Removed all 1D histogram options other than phi_t
* Added the 2D plot for W vs MM
    
## Extra_Name = "New_Binning_Schemes_V5_"
* Fixed issues with the z-pT binning for y_bin option
* Modified the default W and MM binning for better use in the response matrix histograms
* Added MM and W to the 1D histogram options being run
* Turned off smearing (not needed at this time)
* Added the new Y_bin binning option but did not run yet
    * This option is a variation of the y_bin option added in the prior versions of the code
    * Contains more bins with the bin borders of each bin being shared as much as possible (result is that this binning scheme can easily be split into very distinct Q2 and y groups - 5 Q2 groups and 4 y groups)
    
## Extra_Name = "New_Binning_Schemes_V6_"
* Switched to the new Q2-y binning but switched the names so that the Q2-y binning scheme used in the last version of this code is now referred to by "Y_bin" while the new binning scheme uses 'y_bin' (will make updating the other files easier)
* Removed the MM and W to the 1D histogram options (no longer running)
* Smearing is still turned off (not needed at this time)
* Fixed the issue with the 'Multi_Dim' variables' code (was not using the generated information propperly)
    

## Extra_Name = "New_Binning_Schemes_V7_"
* Added the z-pT bins for the new y-binning scheme
* Smearing is still turned off (not needed at this time)
* Fixed issues with the 'Multi_Dim' binning function (should work correctly now)
* Added new 2D plots for W vs Q2/y and xB vs y (three new plots)
    * Added later (ran a second time without renaming on 6-12-2023)
        
        
## Extra_Name = "New_Binning_Schemes_V8_"
* Added a 5D response matrix by defining a new 4D Bin variable based on the Q2-xB-z-pT bins
    * The 4D variable has a total of 566 bins while the 5D Response Matrix only uses 12 bins for the phi_t variable to limit the memory consumption of creating a histogram with more than 12000 bins (with only 12 phi_t bins, the 5D response matrix should have about 6792 bins)
    * Needed to be fixed after starting to run - the 'Multi_Dim' response matrices no longer use 3D histograms to slice with the z-pT bins
* Smearing is still turned off (not needed at this time)
    
    
## Extra_Name = "Gen_Cuts_V1_"
* Added new Missing Mass Cut to the generated events (to both 'gdf' and 'gen' - i.e., all matched/unmatched generated events are cut)
    * First test of the generated missing mass cut
    * The Missing Mass Cut starts at 1.5 GeV (just like the normal cut to the reconstructed events)
* Smearing function was modified with a new smearing factor (and slightly modified function)
* Modified the 5D histogram to use 24 phi_t bins again instead of 12
* Removed the 2D plots for W vs Q2/y and xB vs y (three of the 2D plots)


<hr style="border:2px solid gray">

# Notes Committed on 6-2-2023:

## Extra_Name = "Analysis_Note_Update_VF_APS_"
* Final version of histograms as used in the analysis note for the April APS meetings (released 2/22/2023)
    
    
## Extra_Name = "Multi_Dimension_Unfold_V1_"
* ∆P now uses the generated kinematics for comparison instead of the calculated ones for the matched monte carlo files
* Made a general update to some lines of code to 'clean up' their appearance (does not affect how code is run)
* Testing first multidmimensional binning using just Q2 and phi_h
    
    
## Extra_Name = "Multi_Dimension_Unfold_V2_"
* Turned off ∆P plots for now (use the version above)
* Testing second multidmimensional binning using Q2_xB_Bins with phi_h
    * Use the prior version for all other plots
    * These plots will be cut as to ignore bin migration in the z-pT bins
    
    
## Extra_Name = "Multi_Dimension_Unfold_V3_"
* ∆P plots are still off
* Fixed the multidmimensional binning (had overlapping bins and missed the last bin that was not phi)
    * Running both the Q2_phi and Q2_xB_phi plots
* Added cut to Q2-xB bin 0 in Multidimensional unfolding
    
    
## Extra_Name = "Multi_Dimension_Unfold_V4_"
* Fixed the cuts where Valerii's Fiducial cuts were not being applied
* ∆P plots are turned on
* Made a new momentum correction for the simulated data
    * Correcting both particles as a quadratic function of momentum
    * Corrections are based on ∆P = P_GEN - P_REC instead of P_calc and P_meas (i.e., not calculating the correct kinematics - just taking from the event generator)
        * Means that the corrections of each particle can be obtained completely independently from the other particle
* Made new function for defining the Q2-xB binning schemes
    * Much more condensed, works for normal, gen, and smeared bins
        * New z-pT bin function was created to condense the code for the normal, gen, and smeared bins as well, but this code is otherwise the same as how it was written before
    * Will make future iterations of new bins much easier
    * Should make my modified binning the default with update - Stefan's binning needs to be added to Q2_xB_Bin_Standard_Def_Function() (Double check to make sure it is correct - not tested fully but shouldn't matter)
    * Testing the function with the binning scheme of 'Test' - which is identical to the standard binning scheme used which is called '2'
* Added new binning scheme for Q2-xB bins
    * Still in testing - will need more work
    * Currently called binning scheme '3' with the title of "(Square)" - will likely change later
    * Consists of 12 rectangular bins
    * z-pT bins are not uniquely defined yet (using whatever the default is from the new bin fuctions)
* Removed the 'EDIS' cuts when not using the 'Mom_Cor_Code' option
* 'Mom_Cor_Code' option now runs completely separately from the other histogram options (other than the simple 2D histograms - See 'Multi_Dimension_Unfold_V4_Mom_Cor_')
* Removed the unfolding histograms of all kinematic variables that were not 'phi_t' (done for memory constraints)
* Added 'Quality-of-Life' improvements to print out all run options (including binning, cut, variable selection, etc.)
    
    
## Extra_Name = "Multi_Dimension_Unfold_V4_Mom_Cor_"
* Ran at the same time as 'Multi_Dimension_Unfold_V4_' but only used 'Mom_Cor_Code' option
        
        
## Extra_Name = "Multi_Dimension_Unfold_V4_Norm_"
* Will just use the '2' binning option
    
## Extra_Name = "Multi_Dimension_Unfold_V4_Test_"
* Will just use the 'Test' binning option

## Extra_Name = "Multi_Dimension_Unfold_V4_New_"
* Will just use the '3' binning option

## Extra_Name = "Multi_Dimension_Unfold_V5_"
* Just ran the SIDIS Histograms (no momentum correction histograms)
* Updated the kinematic binning with the following updates:
    * 1) Now using the condensed code (with TH2Poly) for all binning schemes (most of the old code has been removed or otherwise commented out)
    * 2) New 'Square' bins (i.e. Binning option '3') now has 14 Q2-xB bins total (extra bins were added to this scheme since the last committed version used in 'Multi_Dimension_Unfold_V4_')
        * (Still no z-pT bins for these yet)
    * 3) Will be running with both bin option '2' and '3'
* New Multidimensional binning function was written to combine variables (running the same options but the code should be an improvement - still in testing)
    * All overflow bin events are given the value of -1
* Removed a lot of unnecessary code from this script (general clean up) including pre-defined Multidimensional bins (like Bin_4D)
* Reduced the number of bins in some 2D histograms such as the particle momentums and Q2-xB distributions (should have little effect on the plots outside of some minor visual changes)
    * Done to avoid memory overload as the code was crashing even when I wasn't trying to create the root files.
* Updated the Pi+ momentum smearing function as a funtion of theta (may be quite large)
    * MC momentum corrections have already been applied (same as 'Multi_Dimension_Unfold_V4_')
* The kinematic bins are now only defined if they are considered necessary 
* Removed the angular definitions for sectors amoung other unused variables (were not necessary)
* Made several changes in the hopes of improving memory consumption of the code
    
    
## Extra_Name = "Multi_Dimension_Unfold_V5_Mom_Cor_"
* Same as 'Multi_Dimension_Unfold_V5_' but running the momentum correction histograms instead of the SIDIS ones
    
    
## Extra_Name = "Multi_Dimension_Unfold_V5_FX_Mom_Cor_"
* Same as 'Multi_Dimension_Unfold_V5_Mom_Cor_' but using FX's smearing function


## Extra_Name = "New_Smearing_Factor_V1_Mom_Cor_"
* Same as 'Multi_Dimension_Unfold_V5_Mom_Cor_' but using a new method for smearing which relies on a single smearing factor (no other element of the code has changed -> still resolving issues in "Multi_Dimension_Unfold_V" files)
    * smear_factor = 1.5
* May need to change ∆P histograms to always use ∆P = P_calc - P_meas instead of ∆P = P_gen - P_rec (still using the later for the MC files at this time)
   
   
## Extra_Name = "New_Smearing_Factor_V2_Mom_Cor_"
* Modified the smearing function to apply the simple smearing factor 'f' to the particles' angles (in addition to the momentum)
    * smear_factor = 1.5 (did not change)
* Changed ∆P histograms to always use ∆P = P_calc - P_meas instead of ∆P = P_gen - P_rec (should not effect the Missing Mass Histograms)
* Minor changes to the SIDIS kinematic bins (does not affect the code of this current version for what is being run)
    
    
## Extra_Name = "New_Smearing_Factor_V2_FX_Mom_Cor_"
* Same as 'New_Smearing_Factor_V2_Mom_Cor_' but using FX's smearing function
    
    
## Extra_Name = "New_Smearing_Factor_V3_Mom_Cor_"
* Same as 'New_Smearing_Factor_V2_Mom_Cor_' but turned off momentum corrections
    
    
## Extra_Name = "New_Smearing_Factor_V3_FX_Mom_Cor_"
* Same as 'New_Smearing_Factor_V3_Mom_Cor_' but using FX's smearing function
    
    
## Extra_Name = "New_Smearing_Factor_V3_Pip_Mom_Cor_"
* Same as 'New_Smearing_Factor_V2_Mom_Cor_' but new pi+ momentum corrections for MC (electron not yet corrected)
    
    
## Extra_Name = "New_Smearing_Factor_V4_Mom_Cor_"
* New momentum corrections for MC (pi+ and electron are both corrected)
    
    
## Extra_Name = "New_Smearing_Factor_V5_Mom_Cor_"
* Updated the MC pi+ momentum corrections


## Extra_Name = "New_Smearing_Factor_V5_"
* Same as "New_Smearing_Factor_V5_Mom_Cor_" but running the SIDIS code (testing old bins only)
    * Rewrote the kinematic binning code to (hopefully) use less memory
* Needed to fix binning definitions (typo caused some bins to be defined incorrectly)
    
    
## Extra_Name = "New_Binning_Schemes_V1_"
* Added option to make 3D histograms with 3 unique variables (instead of just using the z-pT binning as the 3rd variable always)
* Made a new binning scheme option of "Off" which allows you to run this code without the kinematic bin calculations (all Q2-xB and z-pT bins are automatically assigned to have the value of 1)
    * Still need to work on aspects of the default code which are causing it to run very slowly -> believed to be related to the new method for calculating the kinematic bins
* 'mdf' no longer runs the 'gen' option for histograms
* Minor improvements to how the binning schemes' names are referenced within the code (mainly made notes to be more accepting of the alternative bin names - should not effect how the code runs)
    * Did include more lines to skip the Q2-xB bins outside of the binning scheme in use (safety measure to help prevent possibly unnecessary histogram creation)
        
        
## Extra_Name = "New_Binning_Schemes_V2_"
* Added new binning type (Q2-y bins)
    * Only ran this scheme
* New Q2 1D binning scheme (new number of bins and range)
    
    
## Extra_Name = "New_Binning_Schemes_V3_"
* Only making the normal 2D histograms (removed the 3D histos)
    * Also plotting W and Mx
        
        
## Extra_Name = "New_Binning_Schemes_V4_"
* Added the z-pT binning for y_bin option
* Added one additional Q2-y bin to the scheme (high Q2 but likely has very low event counts - may not be usable)
* Removed all 1D histogram options other than phi_t
* Added the 2D plot for W vs MM
    
    
## Extra_Name = "New_Binning_Schemes_V5_"
* Fixed issues with the z-pT binning for y_bin option
* Modified the default W and MM binning for better use in the response matrix histograms
* Added MM and W to the 1D histogram options being run
* Turned off smearing (not needed at this time)
* Added the new Y_bin binning option but did not run yet
    * This option is a variation of the y_bin option added in the prior versions of the code
    * Contains more bins with the bin borders of each bin being shared as much as possible (result is that this binning scheme can easily be split into very distinct Q2 and y groups - 5 Q2 groups and 4 y groups)
    
## Extra_Name = "New_Binning_Schemes_V6_"
* Switched to the new Q2-y binning but switched the names so that the Q2-y binning scheme used in the last version of this code is now referred to by "Y_bin" while the new binning scheme uses 'y_bin' (will make updating the other files easier)
* Removed the MM and W to the 1D histogram options (no longer running)
* Smearing is still turned off (not needed at this time)
* Fixed the issue with the 'Multi_Dim' variables' code (was not using the generated information propperly)



<hr style="border:2px solid gray">

# Notes Committed on 4-21-2023:

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


<hr style="border:2px solid gray">

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



<hr style="border:2px solid gray">

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

