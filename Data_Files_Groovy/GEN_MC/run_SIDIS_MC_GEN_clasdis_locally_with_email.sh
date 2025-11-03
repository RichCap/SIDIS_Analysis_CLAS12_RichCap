#!/bin/bash

FILES=(/lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/clasdis_1.5_Cut_Files_Not_Added_To_cache_yet/nb-clasdis-Q2_1.5-9682*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/clasdis_1.5_Cut_Files_Not_Added_To_cache_yet/nb-clasdis-Q2_1.5-9704*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/clasdis_1.5_Cut_Files_Not_Added_To_cache_yet/nb-clasdis-Q2_1.5-9707*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/clasdis_1.5_Cut_Files_Not_Added_To_cache_yet/nb-clasdis-Q2_1.5-9708*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/clasdis_1.5_Cut_Files_Not_Added_To_cache_yet/nb-clasdis-Q2_1.5-9711*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/clasdis_1.5_Cut_Files_Not_Added_To_cache_yet/nb-clasdis-Q2_1.5-9714*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/clasdis_1.5_Cut_Files_Not_Added_To_cache_yet/nb-clasdis-Q2_1.5-9719*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/clasdis_1.5_Cut_Files_Not_Added_To_cache_yet/nb-clasdis-Q2_1.5-9739*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/clasdis_1.5_Cut_Files_Not_Added_To_cache_yet/nb-clasdis-Q2_1.5-9740*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/clasdis_1.5_Cut_Files_Not_Added_To_cache_yet/nb-clasdis-Q2_1.5-9742*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/clasdis_1.5_Cut_Files_Not_Added_To_cache_yet/nb-clasdis-Q2_1.5-9747*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/clasdis_1.5_Cut_Files_Not_Added_To_cache_yet/nb-clasdis-Q2_1.5-9752*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/clasdis_1.5_Cut_Files_Not_Added_To_cache_yet/nb-clasdis-Q2_1.5-9753*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/clasdis_1.5_Cut_Files_Not_Added_To_cache_yet/nb-clasdis-Q2_1.5-9754*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/clasdis_1.5_Cut_Files_Not_Added_To_cache_yet/nb-clasdis-Q2_1.5-9755*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/clasdis_1.5_Cut_Files_Not_Added_To_cache_yet/nb-clasdis-Q2_1.5-9756*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/clasdis_1.5_Cut_Files_Not_Added_To_cache_yet/nb-clasdis-Q2_1.5-9757*)

# Path to your Groovy script
SCRIPT_PATH="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/GEN_MC/MC_Gen_TTree_epip_Batch_Pass2_UpToDate.groovy"

PROCESSED_FILES=""

START_TIME="Started Running at: $(date)"

# Run the Groovy script on each file
for FILE in "${FILES[@]}"; do
    echo "Processing file: $FILE"
    echo "(Done at: $(date))"
    run-groovy "$SCRIPT_PATH" "$FILE"
    PROCESSED_FILES+="$FILE (Done at: $(date))"$'\n'
done


JOB_ID="MC_Gen_epip_clasdis_10_21_2025"

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

echo "$START_TIME"

echo "Done"
