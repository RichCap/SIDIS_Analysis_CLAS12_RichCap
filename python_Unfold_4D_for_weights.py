#!/usr/bin/env python3

import ROOT, numpy, re
import traceback
import sys
import os
import argparse
import math
import array
import copy
import subprocess

# ----------------------------------------------------------------------
# Imports from your analysis environment
# ----------------------------------------------------------------------
class RawDefaultsHelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
    pass
script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis'
sys.path.append(script_dir)
from MyCommonAnalysisFunction_richcap import *  # safe_write, color, etc.
from ExtraAnalysisCodeValues import *
sys.path.remove(script_dir)
del script_dir


# ----------------------------------------------------------------------
# ANSI → HTML + email helper (as given)
# ----------------------------------------------------------------------
def ansi_to_html(text):
    # Converts ANSI escape sequences (from the `color` class) into HTML span tags with inline CSS (Unsupported codes are removed)
    # Map ANSI codes to HTML spans
    ansi_html_map = {  # Styles
                      '\033[1m': "", '\033[2m': "", '\033[3m': "", '\033[4m': "", '\033[5m': "",
                      # Colors
                      '\033[91m': "", '\033[92m': "", '\033[93m': "", '\033[94m': "", '\033[95m': "", '\033[96m': "", '\033[36m': "", '\033[35m': "",
                      # Reset (closes span)
                      '\033[0m': "",
                     }
    sorted_codes = sorted(ansi_html_map.keys(), key=len, reverse=True)
    for code in sorted_codes:
        text = text.replace(code, ansi_html_map[code])
    # Remove any stray/unsupported ANSI codes that might remain
    text = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', text)
    return text


def send_email(subject, body, recipient):
    # Send an email via the system mail command.
    html_body = ansi_to_html(body)
    subprocess.run(["mail", "-s", subject, recipient], input=html_body.encode(), check=False)


# ----------------------------------------------------------------------
# 4D → (Q2_y_Bin, z_pT_Bin) decoder
# This is the inverse of your Q2_y_z_pT_4D_Bins encoding.
# ----------------------------------------------------------------------
def decode_Q2_y_and_z_pT(Q2_y_z_pT_4D_Bins):
    # Inverse mapping: from 4D bin index back to (Q2_y_Bin, z_pT_Bin)
    # Returns (0, 0) for invalid / underflow codes.
    if(Q2_y_z_pT_4D_Bins <= 0):
        return 0, 0

    max_Q2_y_Bin = 17  # Adjust if your analysis uses a different maximum

    for Q2_y_Bin in range(max_Q2_y_Bin, 0, -1):
        offset = 0

        if(Q2_y_Bin >  1):
            offset += 35
        if(Q2_y_Bin >  2):
            offset += 36
        if(Q2_y_Bin >  3):
            offset += 30
        if(Q2_y_Bin >  4):
            offset += 36
        if(Q2_y_Bin >  5):
            offset += 36
        if(Q2_y_Bin >  6):
            offset += 30
        if(Q2_y_Bin >  7):
            offset += 36
        if(Q2_y_Bin >  8):
            offset += 35
        if(Q2_y_Bin >  9):
            offset += 35
        if(Q2_y_Bin > 10):
            offset += 36
        if(Q2_y_Bin > 11):
            offset += 25
        if(Q2_y_Bin > 12):
            offset += 25
        if(Q2_y_Bin > 13):
            offset += 30
        if(Q2_y_Bin > 14):
            offset += 36
        if(Q2_y_Bin > 15):
            offset += 25
        if(Q2_y_Bin > 16):
            offset += 30

        if(Q2_y_z_pT_4D_Bins > offset):
            z_pT_Bin = Q2_y_z_pT_4D_Bins - offset
            return Q2_y_Bin, z_pT_Bin

    return 0, 0


# ----------------------------------------------------------------------
# Placeholder: decode 2D bin indices into kinematic values
# You will replace the body of this with your real mapping.
# ----------------------------------------------------------------------
def decode_kinematics_from_bins(Q2_y_Bin_Find_In, z_pT_Bin_Find_In):
    Q2_y_bins, z_pT_bins = Find_Q2_y_z_pT_Bin_Stats(Q2_y_Bin_Find=Q2_y_Bin_Find_In, z_pT_Bin_Find=z_pT_Bin_Find_In, List_Of_Histos_For_Stats_Search="Use_Center", Smearing_Q="''", DataType="bbb", Binning_Method_Input=Binning_Method)
    Q2_bins, y_bins = Q2_y_bins
    z_bins, pT_bins = z_pT_bins
    Q2_val, y_val, z_val, pT_val = Q2_bins[1], y_bins[1], z_bins[1], pT_bins[1]
    return Q2_val, y_val, z_val, pT_val


# ----------------------------------------------------------------------
# Build or fetch the ratio histogram: h_ratio = h_num / h_den
# ----------------------------------------------------------------------
def build_ratio_histogram(root_file, num_name, den_name, ratio_name, force_ratio):
    if((root_file is None) or root_file.IsZombie()):
        raise RuntimeError("Input ROOT file is not open or is a zombie.")

    existing_ratio = root_file.Get(ratio_name)
    if((existing_ratio is not None) and (not force_ratio)):
        print(f"{color.BBLUE}Ratio histogram '{ratio_name}' already exists and force recreation is disabled. Reusing existing histogram.{color.END}")
        return existing_ratio

    num_hist = root_file.Get(num_name)
    den_hist = root_file.Get(den_name)

    if(num_hist is None):
        raise RuntimeError(f"Numerator histogram '{num_name}' not found in file.")
    if(den_hist is None):
        raise RuntimeError(f"Denominator histogram '{den_name}' not found in file.")

    # Clone numerator to get same binning and axis labels
    ratio_hist = num_hist.Clone(ratio_name)
    ratio_hist.SetDirectory(0)  # Detach from file until we explicitly write it
    ratio_hist.Sumw2()          # Make sure errors are stored

    # Perform bin-by-bin division
    ratio_hist.Divide(num_hist, den_hist)

    # Placeholder: you will likely want a more structured title convention here
    ratio_hist.SetTitle(f"{ratio_name}")

    # Write to file using your safe_write helper
    root_file.cd()
    safe_write(ratio_hist, root_file)

    print(f"{color.BGREEN}Created ratio histogram '{ratio_name}' and wrote it to file.{color.END}")
    return ratio_hist


# ----------------------------------------------------------------------
# Convert TH1D ratio histogram → RDataFrame with 7 columns:
#   Q2_y_Bin, Q2_val, y_val, z_val, pT_val, bin_content, bin_error
# ----------------------------------------------------------------------
def build_dataframe_from_hist(ratio_hist):
    if(ratio_hist is None):
        raise RuntimeError("build_dataframe_from_hist: ratio_hist is None.")

    n_bins = ratio_hist.GetNbinsX()

    Q2_y_Bin_list  = []
    Q2_val_list    = []
    y_val_list     = []
    z_val_list     = []
    pT_val_list    = []
    content_list   = []
    error_list     = []

    for ibin in range(1, n_bins + 1):
        Q2_y_z_pT_4D_Bins = ibin

        Q2_y_Bin, z_pT_Bin = decode_Q2_y_and_z_pT(Q2_y_z_pT_4D_Bins)

        if((Q2_y_Bin <= 0) or (z_pT_Bin <= 0)):
            # Skip invalid/underflow mappings
            continue

        bin_content = ratio_hist.GetBinContent(ibin)
        bin_error   = ratio_hist.GetBinError(ibin)

        # User-supplied mapping from bin indices to actual kinematics
        Q2_val, y_val, z_val, pT_val = decode_kinematics_from_bins(Q2_y_Bin, z_pT_Bin)

        Q2_y_Bin_list.append(Q2_y_Bin)
        Q2_val_list.append(Q2_val)
        y_val_list.append(y_val)
        z_val_list.append(z_val)
        pT_val_list.append(pT_val)
        content_list.append(bin_content)
        error_list.append(bin_error)

    if(len(Q2_y_Bin_list) == 0):
        print(f"{color.YELLOW}Warning: No valid bins were converted into dataframe entries.{color.END}")

    data_dict = {
        "Q2_y_Bin":    numpy.array(Q2_y_Bin_list, dtype="int32"),
        "Q2_val":      numpy.array(Q2_val_list,   dtype="float64"),
        "y_val":       numpy.array(y_val_list,    dtype="float64"),
        "z_val":       numpy.array(z_val_list,    dtype="float64"),
        "pT_val":      numpy.array(pT_val_list,   dtype="float64"),
        "bin_content": numpy.array(content_list,  dtype="float64"),
        "bin_error":   numpy.array(error_list,    dtype="float64"),
    }

    rdf = ROOT.RDF.MakeNumpyDataFrame(data_dict)
    return rdf


# ----------------------------------------------------------------------
# Argument parsing
# ----------------------------------------------------------------------
def parse_arguments():
    parser = argparse.ArgumentParser(description="Build ratio histograms and export their 4D-bin contents into an RDataFrame ROOT file.",
                                formatter_class=RawDefaultsHelpFormatter)

    parser.add_argument("-r", "-inR", "--input_root",
                        help="Input ROOT file containing the numerator and denominator TH1D histograms.")
    parser.add_argument("-nh", "--num_hist",
                        help="Name of the numerator TH1D histogram in the input file.")
    parser.add_argument("-dh", "--den_hist",
                        help="Name of the denominator TH1D histogram in the input file.")
    parser.add_argument("-rh", "--ratio_hist", default=None,
                        help="Name to use (or look for) for the ratio TH1D histogram in the input file. Overwrites the default naming.")
    parser.add_argument("-rf", "--rdf_file",
                        help="Output ROOT file to store the RDataFrame with bin-by-bin values.\n\tIf this file already exists and `--force_rdf` is not set, all processing is skipped.")
    # parser.add_argument("--rdf-tree-name", default="h22",
    #                     help="Name of the output TTree created by Snapshot (default: 'ratio_points').")
    # Above will always be h22 for code compatiblity

    parser.add_argument("-fr", "--force_ratio", action="store_true",
                        help="Force recreation of the ratio histogram even if it already exists in the input file.")
    parser.add_argument("-frdf", "--force_rdf", action="store_true",
                        help="Force recreation of the RDataFrame file even if it already exists.")
    parser.add_argument("-e", "--email", action="store_true",
                        help="Optional email sent at the end of the script.")
    parser.add_argument("-ee", "--email_message", default=None, type=str,
                        help="Additional message to be attached to the email.")

    args = parser.parse_args()
    return args


# ----------------------------------------------------------------------
# Main control flow
# ----------------------------------------------------------------------
def main():
    args = parse_arguments()

    try:
        # If the RDataFrame output file already exists and user does not want to overwrite, skip everything
        if(os.path.exists(args.rdf_file) and (not args.force_rdf)):
            print(f"{color.BBLUE}RDataFrame file '{args.rdf_file}' already exists and --force-rdf was not set. Skipping all processing.{color.END}")
            return

        if(not os.path.exists(args.input_root)):
            raise RuntimeError(f"Input ROOT file '{args.input_root}' does not exist.")

        # Open ROOT file in UPDATE mode so we can read and also write the ratio histogram
        root_file = ROOT.TFile.Open(args.input_root, "UPDATE")
        if((root_file is None) or root_file.IsZombie()):
            raise RuntimeError(f"Failed to open input ROOT file '{args.input_root}' in UPDATE mode.")

        # 1–3) Build or reuse ratio histogram, write it safely to the ROOT file
        ratio_hist = build_ratio_histogram(root_file, args.num_hist, args.den_hist, args.ratio_hist, args.force_ratio)

        # Make sure the file is updated on disk
        root_file.Write("", ROOT.TObject.kOverwrite)
        root_file.Close()
        root_file = None

        # 4–5) Convert ratio histogram to RDataFrame and Snapshot to a new ROOT file
        rdf = build_dataframe_from_hist(ratio_hist)

        # Create / overwrite the RDataFrame output file
        print(f"{color.BBLUE}Writing RDataFrame to file '{args.rdf_file}' as tree 'h22'.{color.END}")
        rdf.Snapshot("h22", args.rdf_file)
        print(f"{color.BGREEN}Done. RDataFrame with 7 columns written to '{args.rdf_file}'.{color.END}")

    except Exception as e:
        err_msg = "".join([
            color.Error,
            "\nERROR in ratio → RDataFrame script:\n",
            color.END,
            str(e),
            "\n\nTraceback:\n",
            traceback.format_exc(),
            "\n"
        ]) # Replace the `join` command with one-line f-strings later
        print(err_msg)

        # if(args.email_recipient is not None):
        #     send_email("Ratio → RDataFrame script error", err_msg, args.email_recipient)
        # need to fix the emails to also send one when the script is successful (more important than when it fails)

        # Non-zero exit code to signal failure in batch environments
        sys.exit(1)


if(__name__ == "__main__"):
    main()
