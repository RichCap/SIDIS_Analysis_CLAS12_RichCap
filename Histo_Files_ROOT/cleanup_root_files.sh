#!/bin/bash

# Check if the correct number of arguments were passed
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <directory> <file_pattern> <option>"
    exit 1
fi

DIRECTORY=$1
FILE_PATTERN=$2
OPTION=$3

# Adjust file pattern for deletion based on OPTION
case $OPTION in
    rdf)
        FILE_PATTERN="${FILE_PATTERN}_5*"
        ;;
    mdf|gdf)
        FILE_PATTERN="${FILE_PATTERN}_3*"
        ;;
    *)
        echo "Invalid option for cleanup: $OPTION"
        exit 2
        ;;
esac

# Prompt the user for confirmation
echo "Do you want to delete the input files matching pattern $FILE_PATTERN? [yes/no]"
read USER_CONFIRMATION

if [ "$USER_CONFIRMATION" = "yes" ]; then
    # Perform the deletion
    rm -v ${DIRECTORY}${FILE_PATTERN}
    echo "Input files have been deleted."
else
    echo "Deletion aborted."
fi
