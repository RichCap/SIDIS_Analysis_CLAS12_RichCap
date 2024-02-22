#!/bin/bash

# Check if an argument is given
if [ $# -eq 0 ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

# The directory to tar is the first argument
DIR_TO_TAR=$1

# Check if the directory exists
if [ -d "$DIR_TO_TAR" ]; then
    # Create the tar.gz archive
    tar -czvf "${DIR_TO_TAR}.tar.gz" "$DIR_TO_TAR"
    echo "Directory $DIR_TO_TAR is tarred successfully."
else
    # Error message if the directory does not exist
    echo "Error: Directory $DIR_TO_TAR does not exist."
    exit 2
fi

echo "Done"
