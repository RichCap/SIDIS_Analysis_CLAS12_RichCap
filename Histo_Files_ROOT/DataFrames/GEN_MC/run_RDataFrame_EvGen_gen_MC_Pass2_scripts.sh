#!/bin/bash

# -------------------------------------------------------------------
# Sequential runner for dataframe_makeROOT_epip_SIDIS.py
# Creates per‐file stdout/stderr logs named like your job names
# Prints each file’s full log output as it completes
# -------------------------------------------------------------------

# Base job name (change this to suit your naming convention)
JOB_BASE="gdf_EvGen_DF_9_18_2025_Run1_Acceptance_Tests_V3"


EMAIL="richard.capobianco@uconn.edu"
START_TIME="Started Running at: $(date)"
# Track processed files for the email
PROCESSED_FILES=""

# Glob of input files
FILES=(/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/Pass2/MC_Gen_sidis_epip_richcap.inb.qa.new5.45nA.inb-EvGen-LUND_EvGen_richcap_GEMC*)

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
    "$CMD" -s gdf -f "$file" > "$LOG_FILE" 2> "$ERR_FILE"

    # Record the completion for this file
    PROCESSED_FILES+="$file (Done at: $(date))"$'\n'
    
    # Print the entire contents of the logs so you see everything as it happened
    echo "--- stdout ($LOG_FILE) ---"
    cat  "$LOG_FILE"
    # echo "--- stderr ($ERR_FILE) ---"
    # cat  "$ERR_FILE"
    echo ""
done

# Compose and send the email
SUBJECT="Finished running $JOB_BASE"
MESSAGE="The local job ($JOB_BASE) processing RDataframe files has completed at:
$(date)

$START_TIME

Files processed:
$PROCESSED_FILES
"

echo "$MESSAGE" | mail -s "$SUBJECT" "$EMAIL"
