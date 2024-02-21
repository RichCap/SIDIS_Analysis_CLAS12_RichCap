#!/bin/bash

# Check if the correct number of arguments were passed
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <directory> <file_pattern> <output_file>"
    exit 1
fi

DIRECTORY=$1
FILE_PATTERN=$2
OUTPUT_FILE=$3


echo "Do you want to delete the input files in the directory:"
echo "          $DIRECTORY"
echo "Excluding the file $OUTPUT_FILE? [yes/no]"

read USER_CONFIRMATION

if [ "$USER_CONFIRMATION" = "yes" ]; then
    # List input files excluding the output file and prompt for confirmation
    INPUT_FILES=$(ls ${FILE_PATTERN} | grep -v "${OUTPUT_FILE}")
    echo "The following input files will be deleted:"
    echo "${INPUT_FILES}"
    echo "Are you sure (Final Confirmation)? [yes/no]"
    read FINAL_CONFIRMATION
    if [ "$FINAL_CONFIRMATION" = "yes" ]; then
        # Perform the deletion
        echo "Deleting input files..."
        rm -v ${INPUT_FILES}
        # ls -hltr ${INPUT_FILES};ls -1 ${INPUT_FILES} | wc -l
        echo "Input files have been deleted."
    else
        echo "Deletion aborted."
    fi
else
    echo "Deletion aborted."
fi

# # Adjust file pattern for deletion based on OPTION
# case $OPTION in
#     rdf)
#         FILE_PATTERN="${FILE_PATTERN}_5*"
#         ;;
#     mdf|gdf)
#         FILE_PATTERN="${FILE_PATTERN}_3*"
#         ;;
#     *)
#         echo "Invalid option for cleanup: $OPTION"
#         exit 2
#         ;;
# esac
# # Prompt the user for confirmation
# echo "Do you want to delete the input files matching pattern $FILE_PATTERN? [yes/no]"
# read USER_CONFIRMATION
# if [ "$USER_CONFIRMATION" = "yes" ]; then
#     # Perform the deletion
#     rm -v ${DIRECTORY}${FILE_PATTERN}
#     echo "Input files have been deleted."
# else
#     echo "Deletion aborted."
# fi
