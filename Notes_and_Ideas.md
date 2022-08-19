# Notes Page
This file contains notes and ideas written down while working on this analysis. Items included here may or may not become relevant later, depending on the usefulness of the idea.
Some items here may also be thought of as a long-term/non-essential, to-do list.


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
- [ ] Add another markdown file for walk-through of code/analysis
    * Add link to analysis note (?)
- [ ] Add option to jupyter notebook to select user range when defining the variable lists (add later)
- [x] In a future update, add the 4D binning to the original kinematic binning from Stephan **(ADDED ON 7-20-2022)**
    * Should be used to show the improvement made by the new binning scheme to the bin migration caused by low Q2
    * Currently, more bin mirgation is occuring such that high generated Q2 is more likely to migrate than low Q2. This is being explained by the low Q2 events that most contribute to bin migration are already being cut by the Q2 > 2 GeV^2 requirement and (more importantly) by the modified bin scheme itself.
    * This addition should be added to verify that the bin migration is being addressed as intended
    