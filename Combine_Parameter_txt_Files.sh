#!/bin/bash

# Check if at least one argument was provided
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 base_name_of_files [SUFFIX1 SUFFIX2 ...]"
    echo "Suffix options: Smeared, Unsmeared, TagProton_Unsmeared, TagProton_Smeared, ProtonCut_Unsmeared, ProtonCut_Smeared"
    exit 1
fi

BASE_NAME="$1"
shift # Shift to process suffixes as arguments

# Determine if a single suffix was provided
if [ "$#" -eq 1 ]; then
    SINGLE_SUFFIX="$1"
else
    SINGLE_SUFFIX=""
fi

# Initialize the output file name
if [ -n "$SINGLE_SUFFIX" ]; then
    output_file="${BASE_NAME}_Combined_${SINGLE_SUFFIX}.txt"
else
    output_file="${BASE_NAME}_Combined.txt"
fi

# Clear the output file in case it already exists
> "$output_file"

# Placeholder for the line to be removed
line_to_remove="Note to Reader: Print the text in this file as a string in Python for the best formatting..."

# Initialize an array to keep track of the files processed
declare -a files_to_delete

# Iterate over each suffix provided in the arguments
for SUFFIX in "$@"; do
    if [[ "$SUFFIX" != "Smeared" && "$SUFFIX" != "Unsmeared" && "$SUFFIX" != "TagProton_Unsmeared" && "$SUFFIX" != "TagProton_Smeared" && "$SUFFIX" != "ProtonCut_Unsmeared" && "$SUFFIX" != "ProtonCut_Smeared" ]]; then
        echo "Invalid suffix: $SUFFIX. Skipping."
        continue
    fi

    SUFFIX="_$SUFFIX"

    # Append the content of the 'All' file if it exists
    if [ -f "${BASE_NAME}_All${SUFFIX}.txt" ]; then
        cat "${BASE_NAME}_All${SUFFIX}.txt" >> "$output_file"
        files_to_delete+=("${BASE_NAME}_All${SUFFIX}.txt") # Add the file to the list for potential deletion
    fi

    # Loop through numbered files and append content minus unwanted line
    for ii in $(seq 1 17); do
        file="${BASE_NAME}_${ii}${SUFFIX}.txt"
        if [ -f "$file" ]; then
            grep -vxF "$line_to_remove" "$file" >> "$output_file"
            files_to_delete+=("$file") # Add file to the list for potential deletion
        else
            echo "Warning: File $file not found and was skipped."
        fi
    done
done

echo "All available files have been combined into $output_file"

# Ask the user if they want to delete the input files
echo "Do you want to delete the input files? This cannot be undone."
echo "Files to be deleted: "
for file in "${files_to_delete[@]}"; do
    ls -lh "$file"
done
read -p "Type 'yes' to delete or anything else to keep: " confirm_delete

if [ "$confirm_delete" = "yes" ]; then
    for file in "${files_to_delete[@]}"; do
        rm -v "$file"
    done
    echo "Input files have been deleted."
else
    echo "Input files have been kept."
fi