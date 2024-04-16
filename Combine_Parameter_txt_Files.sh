#!/bin/bash

# Check if at least one argument was provided
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 base_name_of_files [Smeared|Unsmeared]"
    exit 1
fi

BASE_NAME="$1"
SUFFIX=""
if [ "$#" -eq 2 ]; then
    # Check if the second argument is either "Smeared" or "Unsmeared"
    if [ "$2" == "Smeared" ] || [ "$2" == "Unsmeared" ]; then
        SUFFIX="_$2"
    else
        echo "Invalid suffix. Only 'Smeared' or 'Unsmeared' are accepted."
        exit 1
    fi
fi

output_file="${BASE_NAME}_Combined${SUFFIX}.txt"

# Clear the output file in case it already exists
> "$output_file"

# Placeholder for the line to be removed
line_to_remove="Note to Reader: Print the text in this file as a string in Python for the best formatting..."

# Initialize an array to keep track of the files processed
declare -a files_to_delete

# Append the content of the all file if it exists
if [ -f "${BASE_NAME}_All${SUFFIX}.txt" ]; then
    cat "${BASE_NAME}_All${SUFFIX}.txt" >> "$output_file"
    files_to_delete+=("${BASE_NAME}_All${SUFFIX}.txt") # Add the file to the list for potential deletion
fi

# Loop through the files and append their content minus the unwanted line to the output file
for ii in $(seq 1 17); do
    file="${BASE_NAME}_${ii}${SUFFIX}.txt"
    # Check if the file exists before trying to process it
    if [ -f "$file" ]; then
        grep -vxF "$line_to_remove" "$file" >> "$output_file"
        files_to_delete+=("$file") # Add the file to the list for potential deletion
    else
        echo "Warning: File $file not found and was skipped."
    fi
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
