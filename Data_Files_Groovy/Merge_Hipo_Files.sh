#!/bin/bash

# Function to display help message
function display_help {
    echo
    echo "Usage: $0 <username> <job_id> [output_directory] [test]"
    echo "       Will merge sets of Monte Carlo HIPO files from a given OSG job into 10 larger files"
    echo
    echo "Arguments:"
    echo "  username          The username for the job (used to find the input files that will be merged)."
    echo "  job_id            The job ID to process    (used to find the input files that will be merged)."
    echo "  output_directory  Optional: The directory where the output will be saved."
    echo "                              If not specified, the current working directory is used."
    echo
    echo "Options:"
    echo "  --help            Display this help message and exit."
    echo "  --test            Optional: If specified, the script will only count and print the number of input files instead of merging them."
    echo
}

# Check if the first argument is '--help'
if [ "$1" == "--help" ]; then
    display_help
    exit 0
fi

# Check if at least two arguments (username and job_id) are provided
if [ $# -lt 2 ]; then
  echo "Usage: $0 <username> <job_id> [output_directory] [test]"
  exit 1
fi

# Can change if input file names change
string_identifier="inb-clasdis"

# Assign variables from the input arguments
username=$1
job_id=$2

# Set input_directory based on the first two arguments
input_directory="/volatile/clas12/osg/$username/job_$job_id/output"
# Set output_directory to the third argument or default to the current working directory
output_directory=${3:-$(pwd)}

# Check if input_directory exists
if [ ! -d "$input_directory" ]; then
    echo "Error: Input directory '$input_directory' does not exist."
    exit 1
fi


# Determine if the 'test' mode is active
test_mode=false
if [ "$4" == "--test" ] || [ "$3" == "--test" ]; then
    test_mode=true
    if [ $# -lt 4 ]; then
        output_directory=$(pwd)
    fi
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
        percent_F=$(echo "scale=3; ($num_files / 1000) * 100" | bc)
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
