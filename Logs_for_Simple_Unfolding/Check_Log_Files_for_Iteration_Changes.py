#!/usr/bin/env python3
import argparse
import os
import sys

_SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
if(_SCRIPT_DIR not in sys.path):
    sys.path.insert(0, _SCRIPT_DIR)
from Plot_Bayes_Iteration_Chi2 import extract_q2y_bin_from_filename, parse_unfold_log

class RawDefaultsHelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
    pass
def parse_args():
    parser = argparse.ArgumentParser(description="Extract Iteration and Chi^2 of change values from log for direct Excel paste.", formatter_class=RawDefaultsHelpFormatter)
    parser.add_argument('-f', '--log_file',
                        type=str,
                        required=True,
                        help="Path to the `.out` log file to process.\n")
    parser.add_argument('-v', '--verbose',
                       action='store_true',
                        help="Return the output as human-readable versus excel readable (excel needs commas between columns while passing `--verbose` will print the outputs with tabs).\n")
    return parser.parse_args()
    
def main(args):
    print_separator = "\t"# if(args.verbose) else ","
    q2y_bin = extract_q2y_bin_from_filename(args.log_file)
    if(q2y_bin is not None):
        print(f"\nRun for Q2-y Bin {q2y_bin}\n")

    if(args.verbose):
        print(f"Iterations{print_separator}𝜒2 of change")
    series_list = parse_unfold_log(args.log_file, block="first")
    if(not series_list):
        return
    series = series_list[0]
    for iteration, chi_value in series.chi2.items():
        if(args.verbose):
            print(f"{iteration:>10.0f}{print_separator}{chi_value}")
        else:
            print(f"{chi_value}")
    if(series.n_bins is not None):
        if(args.verbose and (q2y_bin is not None)):
            print(f"\nNumber of Bins Used in Q2-y Bin {q2y_bin} = {series.n_bins}\n")
        else:
            print(f"\nNumber of Bins Used = {series.n_bins}\n")

if(__name__ == "__main__"):
    args = parse_args()
    main(args)
    if(args.verbose):
        print("\nDone\n")
    else:
        print("")
     