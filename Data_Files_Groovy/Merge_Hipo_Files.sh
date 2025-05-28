#!/bin/bash

# Function to display help message
function display_help {
    echo
    echo "Usage: $0 <username> <job_id> [-o <dir>] [-s <id>] [--test]"
    echo "       Will merge sets of Monte Carlo HIPO files from a given OSG job into 10 larger files"
    echo
    echo "Arguments:"
    echo "  username            The username for the job (used to find the input files that will be merged)."
    echo "  job_id              The job ID to process    (used to find the input files that will be merged)."
    echo
    echo "Options:"
    echo "  -o  Optional: The directory where the output will be saved."
    echo "                      If not specified, the current working directory is used."
    echo "  -s Optional: Identifier for input filenames. Defaults to 'inb-clasdis'."
    echo "  -h, --help          Display this help message and exit."
    echo "  -t, --test          Optional: If specified, the script will only count and print the number of input files instead of merging them."
    echo
}

# Check if the first argument is '--help'
if [[ "$1" == "--help" || "$1" == "-h" ]]; then
    display_help
    exit 0
fi

# Check if at least two arguments (username and job_id) are provided
if [ $# -lt 2 ]; then
  echo "Usage: $0 <username> <job_id> [-o <dir>] [-s <id>] [--test]"
  exit 1
fi

# Assign mandatory arguments
username=$1
job_id=$2
shift 2

test_mode=false
output_directory="$(pwd)"
string_identifier="inb-clasdis"

# Parse optional parameters
while [[ $# -gt 0 ]]; do
    case "$1" in
        -o)
            output_directory="$2"
            shift 2
            ;;
        -s)
            string_identifier="$2"
            shift 2
            ;;
        -t|--test)
            test_mode=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            display_help
            exit 1
            ;;
    esac
done

# Set input_directory based on username and job_id
input_directory="/volatile/clas12/osg/$username/job_$job_id/output"

# Check if input_directory exists
if [ ! -d "$input_directory" ]; then
    echo "Error: Input directory '$input_directory' does not exist."
    exit 1
fi

# Check if output_directory exists
if [ ! -d "$output_directory" ]; then
    echo "Error: Output directory '$output_directory' does not exist."
    exit 1
fi

# Initialize variables for summing percentages and counting iterations
total_percent=0
count=0

# Loop to process the files
for i in $(seq 0 9); do
    input_files="${input_directory}/${string_identifier}-${job_id}-*${i}.hipo"
    output_file="${output_directory}/${string_identifier}-${job_id}_${i}.hipo"
    
    if [ "$test_mode" = true ]; then
        # Count the number of input files
        num_files=$(ls $input_files 2>/dev/null | wc -l)
        percent_F=$(echo "scale=3; ($num_files / 2000) * 100" | bc)
        # percent_F=$(echo $percent_F | awk '{printf "%g", $0}')
        percent_F=$(printf "%.1f" $percent_F)
        # Add the current percent_F to the total_percent
        total_percent=$(echo "$total_percent + $percent_F" | bc)
        # Increment the count
        count=$(($count + 1))
        echo
        echo "Found $num_files files ($percent_F%) matching pattern: $input_files"
        echo "               Would have merged to form: $output_file"
    else
        echo
        echo "Merging these HIPO files: $input_files"
        echo "                 To form: $output_file"
        hipo-utils -merge -o $output_file $input_files
        echo "Done"
    fi
    echo
done

# Calculate and print the average percentage if test_mode is true
if [ "$test_mode" = true ]; then
    average_percent=$(echo "scale=3; $total_percent / $count" | bc)
    average_percent=$(printf "%.1f" $average_percent)
    echo
    echo "Average percentage of files present across all patterns: $average_percent%"
    echo
fi

# End of the script
