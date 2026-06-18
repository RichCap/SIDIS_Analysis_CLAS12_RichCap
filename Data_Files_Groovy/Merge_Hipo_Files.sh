#!/bin/bash

# Function to display help message
function display_help {
    echo
    echo "Usage: $0 <username> <job_id> [-o <dir>] [-s <id>] [-i <input_dir>] [-n <expected_total>] [-c] [--test]"
    echo "       Will merge sets of Monte Carlo HIPO files from a given OSG job into 10 larger files"
    echo
    echo "Arguments:"
    echo "  username            The username for the job (used to find the input files that will be merged)."
    echo "  job_id              The job ID to process    (used to find the input files that will be merged)."
    echo
    echo "Options:"
    echo "  -o  Optional: The directory where the output will be saved."
    echo "                      If not specified, the current working directory is used."
    echo "  -s  Optional: Identifier for input filenames. Defaults to 'inb-clasdis'. Put 'empty' if the files have no name string (will rename the output file to 'nb-clasdis-Q2_1.5')."
    echo "  -i  Optional: FULL path to search for input files. If provided, this REPLACES the default input directory."
    echo "  -n  Optional: Expected file total per group (used for percentage calc). Defaults to 1000."
    echo "  -h, --help          Display this help message and exit."
    echo "  -t, --test          Optional: If specified, the script will only count and print the number of input files instead of merging them."
    echo "  -c, --check         Optional: If specified, the script will scan files and list corrupted files without merging them."
    echo
}

# Function to require an option value
function require_option_value {
    local option_name=$1
    local option_value=$2

    if [[ -z "$option_value" || "$option_value" == -* ]]; then
        echo "Error: $option_name requires a value."
        display_help
        exit 1
    fi
}

# Function to check whether a HIPO file appears corrupted/unusable
function hipo_file_is_corrupted {
    local file_name=$1
    local hipo_info=""
    local hipo_status=0

    if [ ! -s "$file_name" ]; then
        return 0
    fi

    hipo_info=$(hipo-utils -info "$file_name" 2>&1)
    hipo_status=$?

    if [[ "$hipo_status" -ne 0 ]]; then
        hipo_info=$(hipo-utils -dump "$file_name" 2>&1)
        hipo_status=$?
    fi

    if [[ "$hipo_info" == *"does not appear to have an index"* ]]; then
        return 0
    fi

    if echo "$hipo_info" | grep -Eq "number of[[:space:]]+records[[:space:]]*:[[:space:]]*0([^0-9]|$)"; then
        return 0
    fi

    if echo "$hipo_info" | grep -Eq "number of[[:space:]]+events[[:space:]]*:[[:space:]]*0([^0-9]|$)"; then
        return 0
    fi

    if [[ "$hipo_status" -ne 0 ]]; then
        return 0
    fi

    return 1
}

# Check if the first argument is '--help'
if [[ "$1" == "--help" || "$1" == "-h" ]]; then
    display_help
    exit 0
fi

# Check if at least two arguments (username and job_id) are provided
if [ $# -lt 2 ]; then
  echo "Usage: $0 <username> <job_id> [-o <dir>] [-s <id>] [-i <input_dir>] [-n <expected_total>] [-c] [--test]"
  exit 1
fi

# Assign mandatory arguments
username=$1
job_id=$2
shift 2

# Defaults
test_mode=false
check_mode=false
output_directory="$(pwd)"
string_identifier="inb-clasdis"
custom_input_directory=""
expected_total=1000

# Parse optional parameters
while [[ $# -gt 0 ]]; do
    case "$1" in
        -o)
            require_option_value "-o" "$2"
            output_directory="$2"
            shift 2
            ;;
        -s)
            require_option_value "-s" "$2"
            string_identifier="$2"
            shift 2
            ;;
        -i)
            require_option_value "-i" "$2"
            custom_input_directory="$2"
            shift 2
            ;;
        -n)
            require_option_value "-n" "$2"
            if ! [[ "$2" =~ ^[0-9]+$ ]]; then echo "Error: -n expects an integer (e.g., 1000)"; exit 1; fi
            if [[ "$2" -eq 0 ]]; then echo "Error: -n must be greater than 0"; exit 1; fi
            expected_total="$2"
            shift 2
            ;;
        -t|--test)
            test_mode=true
            shift
            ;;
        -c|--check)
            check_mode=true
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

# Set input_directory based on username and job_id, unless custom override given
if [[ -n "$custom_input_directory" ]]; then
    input_directory="$custom_input_directory"
else
    input_directory="/volatile/clas12/osg/$username/job_$job_id/output"
fi

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
total_corrupted_files=0

# Loop to process the files
for i in $(seq 0 9); do
    if [[ "$string_identifier" == "empty" ]]; then
        input_pattern="${input_directory}/${job_id}-*${i}.hipo"
        safe_string_identifier="nb-clasdis-Q2_1.5"
        output_file="${output_directory}/${safe_string_identifier}-${job_id}_${i}.hipo"
    else
        # input_pattern="${input_directory}/${string_identifier}-${job_id}-*${i}.hipo"
        input_pattern="${input_directory}/${string_identifier}-${job_id}*${i}.hipo"
        safe_string_identifier="${string_identifier//\*/}" # Remove '*' from string_identifier only for output_file naming
        output_file="${output_directory}/${safe_string_identifier}-${job_id}_${i}.hipo"
    fi

    input_files=()
    good_files=()
    corrupted_files=()

    while IFS= read -r hipo_file; do
        input_files+=("$hipo_file")
    done < <(compgen -G "$input_pattern" | sort)

    for hipo_file in "${input_files[@]}"; do
        if hipo_file_is_corrupted "$hipo_file"; then
            corrupted_files+=("$hipo_file")
        else
            good_files+=("$hipo_file")
        fi
    done

    num_files=${#input_files[@]}
    num_good_files=${#good_files[@]}
    num_corrupted_files=${#corrupted_files[@]}

    total_corrupted_files=$(($total_corrupted_files + $num_corrupted_files))

    if [ "$test_mode" = true ]; then
        percent_F=$(echo "scale=3; ($num_good_files / $expected_total) * 100" | bc)
        percent_F=$(printf "%.1f" $percent_F)
        total_percent=$(echo "$total_percent + $percent_F" | bc)
        count=$(($count + 1))
    fi

    if [ "$check_mode" = true ]; then
        echo
        echo "Checking files matching pattern: $input_pattern"
        echo "  Total files found:     $num_files"
        echo "  Good files found:      $num_good_files"
        echo "  Corrupted files found: $num_corrupted_files"

        for bad_file in "${corrupted_files[@]}"; do
            echo "    CORRUPTED: $bad_file"
        done

    elif [ "$test_mode" = true ]; then
        echo
        echo "Found $num_files total files matching pattern: $input_pattern"
        echo "Found $num_good_files usable files ($percent_F%)"
        echo "Found $num_corrupted_files corrupted files"
        echo "               Would have merged to form: $output_file"

        for bad_file in "${corrupted_files[@]}"; do
            echo "    WOULD SKIP CORRUPTED: $bad_file"
        done

    else
        echo
        echo "Found $num_files total files matching pattern: $input_pattern"
        echo "Found $num_good_files usable files"
        echo "Found $num_corrupted_files corrupted files"

        for bad_file in "${corrupted_files[@]}"; do
            echo "    SKIPPING CORRUPTED: $bad_file"
        done

        if [ "$num_good_files" -eq 0 ]; then
            echo "Error: No usable files found for this pattern. Skipping merge."
            echo
            continue
        fi

        echo "Merging usable HIPO files only"
        echo "                 To form: $output_file"
        hipo-utils -merge -o "$output_file" "${good_files[@]}"
        echo "Done"
    fi
    echo
done

# Calculate and print the average percentage if test_mode is true
if [ "$test_mode" = true ]; then
    average_percent=$(echo "scale=3; $total_percent / $count" | bc)
    average_percent=$(printf "%.1f" $average_percent)
    echo
    echo "Average percentage of usable files present across all patterns: $average_percent%"
    echo "Total corrupted files found across all patterns: $total_corrupted_files"
    echo
fi

# End of the script
