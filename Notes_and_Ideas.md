# Notes Page
This file contains notes and ideas written down while working on this analysis. Items included here may or may not become relevant later, depending on the usefulness of the idea.
Some items here may also be thought of as a long-term/non-essential, to-do list.


## Potential Ideas
These ideas may or may not be implemented later (put here as a reminder to think about later)
- [x] Rework the Jupyter notebook/python code with the following ideas:
    - [x] Streamline remaining naming convensions
        * Momentum Correction/Smearing histograms already do this - apply to normal histograms and all response matrices
    - [ ] Remove the old 2D binning schemes as the default
    - [x] Rewrite variable calculations so that a simpler method of writing the unsmeared/smeared variables is possible
        * Will reduce repetitiveness in code
    - [x] Will be making these updates in a new python file called "makeROOT_epip_SIDIS_histos_new.py" (must update other files to interact with this version of the code)
- [x] Create interactive webpage to plot each 1D phi_t plot in each Q2-xB-z-PT bin
    * Purpose: see the distribution in each bin to check if new binning definitions will be required
- [x] Add Multidimensional bins that combine Q2, xB, z, and PT with the phi_h variable
    * Purpose: step-by-step progression to unfolding in each additional dimension
        - [x] Combine phi_t with Q2 (1D)
        - [ ] Combine phi_t with Q2-xB (2D) and z-PT (2D)
        - [ ] Create the 5D response matrix (final step)
- [ ] Add Save options based on the cell being run (don't wait for the whole code to run each cell before moving the images into their final location)
    * Would make organizing images easier
    * Could use a custom function to make saving results easier in each cell


## Note to self:
- [ ] Add another markdown file for walk-through of code/analysis
    * Add link to analysis note (?)
- [ ] Add option to jupyter notebook to select user range when defining the variable lists (add later)
- [x] In a future update, add the 4D binning to the original kinematic binning from Stephan **(ADDED ON 7-20-2022)**
    * Should be used to show the improvement made by the new binning scheme to the bin migration caused by low Q2
    * Currently, more bin mirgation is occuring such that high generated Q2 is more likely to migrate than low Q2. This is being explained by the low Q2 events that most contribute to bin migration are already being cut by the Q2 > 2 GeV^2 requirement and (more importantly) by the modified bin scheme itself.
    * This addition should be added to verify that the bin migration is being addressed as intended
    