#!/bin/bash

FILES=(/lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/nb-clasdis-Q2_1.5-9767*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/nb-clasdis-Q2_1.5-9772*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/nb-clasdis-Q2_1.5-9777*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/nb-clasdis-Q2_1.5-9778*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/nb-clasdis-Q2_1.5-9788*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/nb-clasdis-Q2_1.5-9793*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/nb-clasdis-Q2_1.5-9809*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/nb-clasdis-Q2_1.5-9776*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/nb-clasdis-Q2_1.5-9779*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/nb-clasdis-Q2_1.5-9789*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/nb-clasdis-Q2_1.5-9795*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/clasdis_1.5_Cut_Files_Not_Added_To_cache_yet/nb-clasdis-Q2_1.5-9884*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/clasdis_1.5_Cut_Files_Not_Added_To_cache_yet/nb-clasdis-Q2_1.5-9930*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/clasdis_1.5_Cut_Files_Not_Added_To_cache_yet/nb-clasdis-Q2_1.5-9972*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/clasdis_1.5_Cut_Files_Not_Added_To_cache_yet/nb-clasdis-Q2_1.5-9885*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/clasdis_1.5_Cut_Files_Not_Added_To_cache_yet/nb-clasdis-Q2_1.5-9886*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/clasdis_1.5_Cut_Files_Not_Added_To_cache_yet/nb-clasdis-Q2_1.5-9964*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/clasdis_1.5_Cut_Files_Not_Added_To_cache_yet/nb-clasdis-Q2_1.5-9973*)

# Path to your Groovy script
SCRIPT_PATH="/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/MC_Matched_TTree_epip_Batch.groovy"

PROCESSED_FILES=""

START_TIME="Started Running at: $(date)"

# Run the Groovy script on each file
for FILE in "${FILES[@]}"; do
    echo "Processing file: $FILE"
    echo "(Done at: $(date))"
    run-groovy "$SCRIPT_PATH" "$FILE"
    PROCESSED_FILES+="$FILE (Done at: $(date))"$'\n'
done


JOB_ID="MC_REC_epip_clasdis_12_9_2025"

# After processing all files, send a completion email
EMAIL="richard.capobianco@uconn.edu"
SUBJECT="Local Job Finished: $JOB_ID"
MESSAGE="The local job ($JOB_ID) processing MC REC (clasdis) SIDIS files has completed on $(hostname) at:
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
