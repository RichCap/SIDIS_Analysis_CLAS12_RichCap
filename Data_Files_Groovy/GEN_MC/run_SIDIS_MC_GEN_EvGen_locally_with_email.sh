#!/bin/bash

FILES=(/lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/inb-EvGen-LUND_EvGen_richcap_GEMC-0047*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/inb-EvGen-LUND_EvGen_richcap_GEMC-0013*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/inb-EvGen-LUND_EvGen_richcap_GEMC-0020*)

# Path to your Groovy script
SCRIPT_PATH="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/GEN_MC/MC_Gen_TTree_epip_EvGen.groovy"

PROCESSED_FILES=""

START_TIME="Started Running at: $(date)"

# Run the Groovy script on each file
for FILE in "${FILES[@]}"; do
    echo "Processing file: $FILE"
    echo "(Done at: $(date))"
    run-groovy "$SCRIPT_PATH" "$FILE"
    PROCESSED_FILES+="$FILE (Done at: $(date))"$'\n'
done


JOB_ID="MC_Gen_epip_EvGen_10_31_2025"

# After processing all files, send a completion email
EMAIL="richard.capobianco@uconn.edu"
SUBJECT="Local Job Finished: $JOB_ID"
MESSAGE="The local job ($JOB_ID) processing MC (EvGen) SIDIS files has completed on $(hostname) at:
$(date)

Ran with: $SCRIPT_PATH

$START_TIME

Files processed:
$PROCESSED_FILES
"

# Send the email
echo "$MESSAGE" | mail -s "$SUBJECT" "$EMAIL"

echo "$START_TIME"

echo "Done"
