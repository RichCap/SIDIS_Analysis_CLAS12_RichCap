#!/bin/bash

# Check if at least two arguments were provided
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <variable_part_of_filename> <rdf/mdf/gdf> [check/run]"
    exit 1
fi

# Assign the command line arguments to variables
VARIABLE_PART="$1"
OPTION="$2"
ACTION="${3:-run}"  # Default to 'run' if no third argument is provided

# Initialize variables for directory and file pattern
DIRECTORY=""
FILE_PATTERN=""

FILE_PATTERN="SIDIS_${OPTION}_${VARIABLE_PART}_"
OUTPUT_FILE="${DIRECTORY}${FILE_PATTERN}_All.root"

echo ""

# Determine the directory and file pattern based on the option
case "$OPTION" in
    rdf)
        DIRECTORY="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/REAL_Data/"
        FILE_PATTERN="SIDIS_epip_Data_REC_${VARIABLE_PART}"
        INPUT_PATTERN="${DIRECTORY}${FILE_PATTERN}_5*root"
        ;;
    mdf)
        DIRECTORY="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/Matching_REC_MC/"
        FILE_PATTERN="SIDIS_epip_MC_Matched_${VARIABLE_PART}"
        INPUT_PATTERN="${DIRECTORY}${FILE_PATTERN}_*root"
        ;;
    gdf)
        DIRECTORY="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/GEN_MC/"
        FILE_PATTERN="SIDIS_epip_MC_GEN_${VARIABLE_PART}"
        INPUT_PATTERN="${DIRECTORY}${FILE_PATTERN}_[0-9]*root"
        ;;
    *)
        echo "Invalid option: $OPTION. Use rdf, mdf, or gdf."
        exit 2
        ;;
esac

# Define the output file name based on the input variable part and option
OUTPUT_FILE="${DIRECTORY}${FILE_PATTERN}_All.root"

# Check for existing output file
if [ -f "$OUTPUT_FILE" ]; then
    if [ "$ACTION" = "check" ]; then
        echo "Output file $OUTPUT_FILE already exists."
        echo "Remove it manually if you want to run the hadd command again for the files:"
        echo "       $INPUT_PATTERN"
        echo ""
    else
        echo "Error: Output file $OUTPUT_FILE already exists. Remove it manually if you want to proceed."
        echo ""
        exit 3
    fi
fi

# Check if input files exist
shopt -s nullglob # Make sure an empty glob matches nothing
file_array=($INPUT_PATTERN)
if [ ${#file_array[@]} -eq 0 ]; then
    echo "Error: No input files found matching pattern $INPUT_PATTERN."
    echo ""
    exit 4
fi
shopt -u nullglob # Revert nullglob back to its default behavior

# Check the action to be performed
if [ "$ACTION" = "check" ]; then
    # List files and count them
    echo "Checking files in directory: ${DIRECTORY}"
    ls -lhSr ${INPUT_PATTERN}
    FILE_COUNT=$(ls -1 ${INPUT_PATTERN} 2>/dev/null | wc -l)
    echo "Number of files to be combined: ${FILE_COUNT}"
    echo ""
else
    # Run the hadd command
    echo "Combining files: ${INPUT_PATTERN} into ${OUTPUT_FILE}"
    echo ""
    $ROOTSYS/bin/hadd ${OUTPUT_FILE} ${INPUT_PATTERN}; ls -lhtr ${DIRECTORY}${FILE_PATTERN}*
    echo ""
    echo "Done running the hadd command."

    # Send notification email
    echo "Finished running hadd_root_files_command.sh to combine these files: ${INPUT_PATTERN}" | mail -s "Finished running hadd_root_files_command.sh for ${OPTION}" richard.capobianco@uconn.edu

    # Call cleanup script only if hadd was successful
    if [ $? -eq 0 ]; then
       ./cleanup_root_files.sh "$DIRECTORY" "${INPUT_PATTERN}" "$OUTPUT_FILE"
    fi
    echo ""
fi
echo "Done"
