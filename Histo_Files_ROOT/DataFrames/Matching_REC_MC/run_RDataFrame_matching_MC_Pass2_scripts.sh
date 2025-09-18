#!/bin/bash

# -------------------------------------------------------------------
# Sequential runner for dataframe_makeROOT_epip_SIDIS.py
# Creates per‐file stdout/stderr logs named like your job names
# Prints each file’s full log output as it completes
# -------------------------------------------------------------------

# Base job name (change this to suit your naming convention)
JOB_BASE="FC14_mdf_DF_7_28_2025_Run1_Sector_Tests_V2"

# Glob of input files
FILES=(/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/With_BeamCharge/Pass2/More_Cut_Info/MC_Matching_sidis_epip_richcap.inb.qa.new5*.inb-clasdis*)

# Path to your Python script
CMD="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/./dataframe_makeROOT_epip_SIDIS.py"

# Loop over files by index so we can embed the index in the log names
for idx in "${!FILES[@]}"; do
    file="${FILES[$idx]}"
    
    # Define per‐file log names
    LOG_FILE="${JOB_BASE}_${idx}.log"
    ERR_FILE="${JOB_BASE}_${idx}.err"
    
    echo "=== Processing [$idx] $file ==="
    
    # Run the command, overwrite any existing logs for this file
    "$CMD" -s mdf -f "$file" > "$LOG_FILE" 2> "$ERR_FILE"
    
    # Print the entire contents of the logs so you see everything as it happened
    echo "--- stdout ($LOG_FILE) ---"
    cat  "$LOG_FILE"
    # echo "--- stderr ($ERR_FILE) ---"
    # cat  "$ERR_FILE"
    echo ""
done

