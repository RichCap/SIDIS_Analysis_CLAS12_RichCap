#!/bin/bash

FILES=(/lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/EvGen_Files_Not_Added_To_cache_yet/inb-EvGen-LUND_EvGen_richcap_GEMC-0003*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/EvGen_Files_Not_Added_To_cache_yet/inb-EvGen-LUND_EvGen_richcap_GEMC-0009*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/EvGen_Files_Not_Added_To_cache_yet/inb-EvGen-LUND_EvGen_richcap_GEMC-0012*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/EvGen_Files_Not_Added_To_cache_yet/inb-EvGen-LUND_EvGen_richcap_GEMC-0017*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/EvGen_Files_Not_Added_To_cache_yet/inb-EvGen-LUND_EvGen_richcap_GEMC-0065*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/EvGen_Files_Not_Added_To_cache_yet/inb-EvGen-LUND_EvGen_richcap_GEMC-0066*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/EvGen_Files_Not_Added_To_cache_yet/inb-EvGen-LUND_EvGen_richcap_GEMC-9710*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/EvGen_Files_Not_Added_To_cache_yet/inb-EvGen-LUND_EvGen_richcap_GEMC-9728*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/EvGen_Files_Not_Added_To_cache_yet/inb-EvGen-LUND_EvGen_richcap_GEMC-9729*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/EvGen_Files_Not_Added_To_cache_yet/inb-EvGen-LUND_EvGen_richcap_GEMC-9769*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/EvGen_Files_Not_Added_To_cache_yet/inb-EvGen-LUND_EvGen_richcap_GEMC-9770*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/EvGen_Files_Not_Added_To_cache_yet/inb-EvGen-LUND_EvGen_richcap_GEMC-9780*
       /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/EvGen_Files_Not_Added_To_cache_yet/inb-EvGen-LUND_EvGen_richcap_GEMC-9781*)

# Path to your Groovy script
SCRIPT_PATH="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/Matched_REC_MC/MC_Matched_EvGen_epip_Batch.groovy"

PROCESSED_FILES=""

START_TIME="Started Running at: $(date)"

# Run the Groovy script on each file
for FILE in "${FILES[@]}"; do
    echo "Processing file: $FILE"
    run-groovy "$SCRIPT_PATH" "$FILE"
    PROCESSED_FILES+="$FILE (Done at: $(date))"$'\n'
done


JOB_ID="MC_REC_epip_EvGen_10_21_2025"

# After processing all files, send a completion email
EMAIL="richard.capobianco@uconn.edu"
SUBJECT="Local Job Finished: $JOB_ID"
MESSAGE="The local job ($JOB_ID) processing MC (EvGen) SIDIS files has completed on $(hostname) at:
$(date)

$START_TIME

Files processed:
$PROCESSED_FILES
"

# Send the email
echo "$MESSAGE" | mail -s "$SUBJECT" "$EMAIL"

echo "Done"
