#!/usr/bin/env python3
import argparse

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
    if("Q2_y_Bin_" in str(args.log_file)):
        q2y_bin = str(args.log_file).split("Q2_y_Bin_")
        q2y_bin = str(q2y_bin[-1])
        for replace in [".out", ".log"]:
            q2y_bin = q2y_bin.replace(replace, "")
        print(f"\nRun for Q2-y Bin {q2y_bin}\n")

    if(args.verbose):
        print(f"Iterations{print_separator}𝜒2 of change")
    # else:
    #     print("𝜒2 of change")
    current_iteration = None
    with open(args.log_file, 'r', encoding='utf-8') as file:
        for line in file:
            stripped = line.strip()
            if("Iteration :" in stripped):
                try:
                    iter_part = stripped.split(":", 1)[1].strip()
                    current_iteration = int(iter_part)
                except (IndexError, ValueError):
                    current_iteration = None
            elif(("Chi^2 of change" in stripped) and (current_iteration is not None)):
                try:
                    chi_part = stripped.split()[-1]
                    chi_value = float(chi_part)
                    if(args.verbose):
                        print(f"{current_iteration:>10.0f}{print_separator}{chi_value}")
                    else:
                        print(f"{chi_value}")
                    current_iteration = None
                except (IndexError, ValueError):
                    pass

if(__name__ == "__main__"):
    args = parse_args()
    main(args)
    if(args.verbose):
        print("\nDone\n")
    else:
        print("")
    