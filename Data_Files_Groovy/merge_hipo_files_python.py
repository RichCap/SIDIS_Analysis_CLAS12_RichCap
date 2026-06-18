#!/usr/bin/env python3
Name_of_Script = "merge_hipo_files_python.py"

import argparse
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from pathlib import Path


script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis'
sys.path.append(script_dir)
from MyCommonAnalysisFunction_richcap import color, RuntimeTimer
sys.path.remove(script_dir)
del script_dir

try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False
    def tqdm(iterable):
        return iterable

def parse_args():
    class RawDefaultsHelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
        pass
    parser = argparse.ArgumentParser(description=f"{Name_of_Script} - merges Monte Carlo HIPO files from OSG job into 10 larger files", formatter_class=RawDefaultsHelpFormatter)
    parser.add_argument("username",
                        nargs="?",
                        default=None,
                        help="The username for the job (optional if -i used).\n")
    parser.add_argument("job_id",
                        nargs="?",
                        default=None,
                        help="The job ID to process (optional if -i used).\n")
    parser.add_argument("-o", "--output_dir",
                        default=str(Path.cwd()),
                        help="The directory where the output will be saved.\nIf not specified the current working directory is used.\n")
    parser.add_argument("-s", "--string_id",
                        default="nb-clasdis-Q2_1.5",
                        help="Identifier for input filenames. Put 'empty' if the files have no name string.\n")
    parser.add_argument("-i", "--input_dir",
                        default="",
                        help="FULL path to search for input files. If provided this REPLACES the default input directory.\n")
    parser.add_argument("-n", "--expected_total",
                        default=1000,
                        type=int,
                        help="Expected file total per group (used for percentage calc).\n")
    parser.add_argument("-c", "--check_mode",
                        action="store_true",
                        help="If specified the script will scan files and list corrupted files without merging them.\n")
    parser.add_argument("-t", "--test_mode",
                        action="store_true",
                        help="If specified the script will only count and print the number of input files instead of merging them.\n")
    parser.add_argument("-f", "--fast_mode",
                        action="store_true",
                        help="Fast mode - skips the long corrupted file check and runs the faster old code.\n")
    parser.add_argument("-w", "--workers",
                        default=10,
                        type=int,
                        help="Max parallel workers for file checks.\n")
    args = parser.parse_args()
    return args

def hipo_file_is_corrupted(file_path):
    if((not Path(file_path).exists()) or (Path(file_path).stat().st_size == 0)):
        return True
    try:
        result = subprocess.run(["hipo-utils", "-info", str(file_path)], capture_output=True, text=True, timeout=30)
        hipo_info = result.stdout + result.stderr
        hipo_status = result.returncode
        if(hipo_status != 0):
            result = subprocess.run(["hipo-utils", "-dump", str(file_path)], capture_output=True, text=True, timeout=30)
            hipo_info = result.stdout + result.stderr
            hipo_status = result.returncode
        if("does not appear to have an index" in hipo_info):
            return True
        if(re.search(r"number of\s+records\s*:\s*0(\D|$)", hipo_info) or re.search(r"number of\s+events\s*:\s*0(\D|$)", hipo_info)):
            return True
        if(hipo_status != 0):
            return True
        return False
    except Exception:
        import traceback
        print(traceback.format_exc())
        return True

def process_one_group(group_index, args):
    if(args.string_id == "empty"):
        if(args.job_id is not None):
            input_pattern_name = f"{args.job_id}-*{group_index}.hipo"
            safe_id = "nb-clasdis-Q2_1.5"
            output_file = f"{args.output_dir}/{safe_id}-{args.job_id}_{group_index}.hipo"
        else:
            input_pattern_name = f"*{group_index}.hipo"
            safe_id = "nb-clasdis-Q2_1.5"
            output_file = f"{args.output_dir}/{safe_id}_{group_index}.hipo"
    else:
        if(args.job_id is not None):
            input_pattern_name = f"{args.string_id}-{args.job_id}-*{group_index}.hipo"
            safe_id = args.string_id.replace("*", "")
            output_file = f"{args.output_dir}/{safe_id}-{args.job_id}_{group_index}.hipo"
        else:
            input_pattern_name = f"{args.string_id}-*{group_index}.hipo"
            safe_id = args.string_id.replace("*", "")
            output_file = f"{args.output_dir}/{safe_id}_{group_index}.hipo"
    input_pattern = f"{args.input_dir}/{input_pattern_name}"
    input_files = sorted(Path(args.input_dir).glob(input_pattern_name))
    good_files = []
    corrupted_files = []
    if(args.fast_mode):
        good_files = input_files
    else:
        file_is_corrupted = {}
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            future_to_file = {executor.submit(hipo_file_is_corrupted, hipo_file): hipo_file for hipo_file in input_files}
            future_iterator = as_completed(future_to_file)
            if(HAS_TQDM):
                future_iterator = tqdm(future_iterator, total=len(input_files), desc=f"Group {group_index}")
            for future in future_iterator:
                hipo_file = future_to_file[future]
                file_is_corrupted[hipo_file] = future.result()
        for hipo_file in input_files:
            if(file_is_corrupted[hipo_file]):
                corrupted_files.append(hipo_file)
            else:
                good_files.append(hipo_file)
    num_total = len(input_files)
    num_good  = len(good_files)
    num_corrupted = len(corrupted_files)
    if(args.check_mode):
        print(f"Checking files matching pattern: {input_pattern}")
        print(f"  Total files found:     {num_total}")
        print(f"  Good files found:      {num_good}")
        print(f"  Corrupted files found: {num_corrupted}")
        for bad in corrupted_files:
            print(f"    CORRUPTED: {bad}")
        # args.timer.time_elapsed()
        print("")
    elif(args.test_mode):
        percent = (num_good / args.expected_total * 100) if(args.expected_total > 0) else 0
        print(f"Found {num_total} total files matching pattern: {input_pattern}")
        print(f"Found {num_good} usable files ({percent:.1f}%)")
        print(f"Found {num_corrupted} corrupted files")
        print(f"               Would have merged to form: {output_file}")
        for bad in corrupted_files:
            print(f"    {color.Error}WOULD SKIP CORRUPTED:{color.END_R} {bad}{color.END}")
        # args.timer.time_elapsed()
        print("")
    else:
        print(f"Found {num_total} total files matching pattern: {input_pattern}")
        print(f"Found {num_good} usable files")
        print(f"Found {num_corrupted} corrupted files")
        for bad in corrupted_files:
            print(f"    {color.Error}SKIPPING CORRUPTED:{color.END_R} {bad}{color.END}")
        if(num_good == 0):
            print("Error: No usable files found for this pattern. Skipping merge.")
            return {"group": group_index, "good": 0}
        print(f"Merging usable HIPO files only to form: {output_file}\n")
        # args.timer.time_elapsed()
        print("")
        try:
            cmd = ["hipo-utils", "-merge", "-o", output_file] + [str(f) for f in good_files]
            subprocess.run(cmd, check=True)
            print("Done")
        except Exception:
            import traceback
            print(traceback.format_exc())
    return {"group": group_index, "good": num_good, "corrupted": num_corrupted}


if(__name__ == "__main__"):
    args = parse_args()
    args.timer = RuntimeTimer()
    args.timer.start()
    
    if((args.input_dir != "") and (args.username is not None) and (args.job_id is None)):
        args.job_id = args.username
        args.username = None
    if(args.expected_total <= 0):
        print("Error: expected_total must be greater than 0.")
        sys.exit(1)
    if(args.workers <= 0):
        print("Error: workers must be greater than 0.")
        sys.exit(1)
    if(args.fast_mode and args.check_mode):
        print("Error: --fast_mode cannot be used with --check_mode because check mode requires corruption checks.")
        sys.exit(1)
    if(args.input_dir != ""):
        args.input_dir = args.input_dir
    else:
        if((args.username is None) or (args.job_id is None)):
            print("Error: username and job_id required unless -i is provided")
            sys.exit(1)
        args.input_dir = f"/volatile/clas12/osg/{args.username}/job_{args.job_id}/output"
    input_directory = Path(args.input_dir)
    if(not input_directory.exists()):
        print(f"Error: Input directory '{input_directory}' does not exist.")
        sys.exit(1)
    output_directory = Path(args.output_dir)
    if(not output_directory.exists()):
        print(f"Error: Output directory '{output_directory}' does not exist.")
        sys.exit(1)
    args.test_mode = args.test_mode or args.check_mode
    print(f"Starting processing with {args.workers} workers (fast={args.fast_mode})...")
    results = []
    for group_index in range(10):
        res = process_one_group(group_index, args)
        results.append(res)
    if(args.test_mode):
        total_percent, count, total_good, total_corrupted = 0, 0, 0, 0
        for r in results:
            percent = (r["good"] / args.expected_total * 100) if(args.expected_total > 0) else 0
            total_percent = total_percent + percent
            count = count + 1
            total_corrupted = total_corrupted + r["corrupted"]
            total_good      = total_good      + r["good"]
        average_percent = (total_percent / count) if(count > 0) else 0
        print(f"\nAverage percentage of usable files present across all patterns: {average_percent:.1f}%")
        print(f"{color.RED   }Total corrupted files found across all patterns: {total_corrupted:>5.0f}")
        print(f"{color.Error }Total failed/missing files (includes corrupted): {(args.expected_total*10) - total_good:>5.0f}{color.END} (out of the expected {args.expected_total*10})")
        if(args.test_mode):
            print(f'''\t{color.ERROR}Job List Entry Output = ['{args.username}', "{args.job_id if(args.input_dir in ['', None]) else f"{args.job_id} -i '{args.input_dir}'"}", {(args.expected_total*10) - total_good}]{color.END}\n''')
        print(f"{color.BGREEN}Total usable files found across all patterns:    {total_good:>5.0f}{color.END}")
    # print("\nAll groups processed.")
    args.timer.stop()
    # print("\n\n")
    
    
