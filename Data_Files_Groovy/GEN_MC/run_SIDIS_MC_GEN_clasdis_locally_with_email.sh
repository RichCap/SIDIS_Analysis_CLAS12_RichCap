#!/bin/bash

FILES=(/lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/inb-clasdis-9592*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/inb-clasdis-9626*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/nb-clasdis-Q2_1.5-9648*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/nb-clasdis-Q2_1.5-9649*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/nb-clasdis-Q2_1.5-9652*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/nb-clasdis-Q2_1.5-9656*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/nb-clasdis-Q2_1.5-9662*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/nb-clasdis-Q2_1.5-9667*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/nb-clasdis-Q2_1.5-9678*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/nb-clasdis-Q2_1.5-9688*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/nb-clasdis-Q2_1.5-9689*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/nb-clasdis-Q2_1.5-9690*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/nb-clasdis-Q2_1.5-9691*)

# Path to your Groovy script
SCRIPT_PATH="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/GEN_MC/MC_Gen_TTree_epip_Batch_Pass2_UpToDate.groovy"

PROCESSED_FILES=""

START_TIME="Started Running at: $(date)"

# Run the Groovy script on each file
for FILE in "${FILES[@]}"; do
    echo "Processing file: $FILE"
    run-groovy "$SCRIPT_PATH" "$FILE"
    PROCESSED_FILES+="$FILE (Done at: $(date))"$'\n'
done


JOB_ID="MC_Gen_epip_clasdis_10_2_2025"

# After processing all files, send a completion email
EMAIL="richard.capobianco@uconn.edu"
SUBJECT="Local Job Finished: $JOB_ID"
MESSAGE="The local job ($JOB_ID) processing MC (clasdis) SIDIS files has completed on $(hostname) at:
$(date)

Ran with: $SCRIPT_PATH

$START_TIME

Files processed:
$PROCESSED_FILES
"

# Send the email
echo "$MESSAGE" | mail -s "$SUBJECT" "$EMAIL"

echo "Done"
