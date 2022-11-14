# Notes Page
This file contains notes and ideas written down while working on this analysis. Items included here may or may not become relevant later, depending on the usefulness of the idea.
Some items here may also be thought of as a long-term/non-essential, to-do list.


## Potential Ideas
These ideas may or may not be implemented later (put here as a reminder to think about later)
- [ ] Create interactive webpage to plot each 1D phi_t plot in each Q2-xB-z-PT bin
    * Purpose: see the distribution in each bin to check if new binning definitions will be required
    * Will need the following:
        - [ ] 8+1 Q2-xB 2D plots to show each Q2-xB bin option (+1 is for all bins - may want to just have the bins highlighted in red instead of cut)
        - [ ] 8+1 z-PT 2D plots to show each z-PT bin option (just like the Q2-xB plots, might not need to draw the 2D plot for each cut bin - would need to show the cut effects of choosing a Q2-xB bin)
        - [ ] 8*(20 to 49)+1 phi_t plots for each Q2-xB-z-PT bin (+1 is for all bins)
            - [ ] Also show the unfolded images from the Collaboration presentation
        - [ ] The webpage code which will:
            - [ ] Reference all images above
            - [ ] Allow for one to select a Q2-xB bin with tabs/buttons
            - [ ] Show new phi_t image by hovering over a z-PT bin
                - [ ] Grid for the z-PT bins must update with choice of Q2-xB bin
        - [ ] Provide link in this repository or on a wikipage
- [ ] Add the interactive python code to the GitHub repository 
    * Purpose: so that others can have the more user-friendly version of the code if they are given access to this repository
        * Would give me a greater reason to share this repository with others
    * Would likely include:
        - [ ] Adding the jupyter notebook file (with edits to run using the files available on GitHub)
        - [ ] Adding additional features to that notebook to keep it concurrent with the available code
            * May want to consider it the "master" version of the code while the existing verision would be the "working" version were new code and ideas are tested
- [ ] Add Multidimensional bins that combine Q2, xB, z, and PT with the phi_h variable
    * Purpose: step-by-step progression to unfolding in each additional dimension
        - [ ] Combine phi_t with Q2 (1D)
            * Maybe all other variables too? --> Create generic code to combine bins
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
    