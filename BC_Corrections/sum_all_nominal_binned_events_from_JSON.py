#!/usr/bin/env python3
import json
import argparse
import sys
from pathlib import Path

class RawDefaultsHelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
    pass
def main():
    parser = argparse.ArgumentParser(description="Sum all nominal bin contents from a BC Corrections JSON file.", formatter_class=RawDefaultsHelpFormatter)
    parser.add_argument("-jf", "--json_file",
                        type=str,
                        default="Sub_Bin_Contents_for_BC_Correction_with_Binned_sbatch.json",
                        help="Path to the JSON file containing the BC correction results.\n")
    parser.add_argument("-v", "--verbose",
                        action="store_true",
                        help="Print more details, including number of bins processed and any skipped entries.\n")
    
    args = parser.parse_args()
    json_path = Path(args.json_file)
    
    if(not json_path.exists()):
        print(f"Error: File not found: {json_path}")
        sys.exit(1)
    if(not json_path.is_file()):
        print(f"Error: Path is not a file: {json_path}")
        sys.exit(1)

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in {json_path}")
        print(e)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file {json_path}: {e}")
        sys.exit(1)

    if(("results" not in data) or (not isinstance(data["results"], dict))):
        print("Error: JSON is missing the required 'results' dictionary.")
        sys.exit(1)

    results = data["results"]
    total = 0.0
    counted = 0
    skipped = 0

    for key, entry in results.items():
        if(not isinstance(entry, dict)):
            skipped += 1
            continue
        nom = entry.get("Nominal Bin")
        if((not isinstance(nom, dict)) or ("Content" not in nom)):
            skipped += 1
            continue
        if(args.verbose):
            print(f"Adding: '{key}'...")
        try:
            val = float(nom["Content"])
            if(val >= 0):  # safety check
                total += val
                counted += 1
            else:
                skipped += 1
        except (ValueError, TypeError):
            skipped += 1
            continue

    print(f"\nGrand total events across all nominal bins: {total:,.0f}")
    print(f"Found and summed {counted} valid nominal bins.\n")

    # if(args.verbose):
    print(f"Skipped {skipped} entries (missing Nominal Bin or Content field).")
    print(f"Total entries scanned in 'results': {len(results)}")

if(__name__ == "__main__"):
    main()