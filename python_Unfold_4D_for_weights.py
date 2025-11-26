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
from MyCommonAnalysisFunction_richcap import *  # color, etc.
from ExtraAnalysisCodeValues import *
sys.path.remove(script_dir)
del script_dir

# Single email recipient (you can hardcode your real address here)
EMAIL_RECIPIENT = "richard.capobianco@uconn.edu"


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


def send_email(subject, body):
    # Send an email via the system mail command.
    if(EMAIL_RECIPIENT is None):
        return
    html_body = ansi_to_html(body)
    subprocess.run(["mail", "-s", subject, EMAIL_RECIPIENT], input=html_body.encode(), check=False)


def safe_write(obj, tfile):
    existing = tfile.GetListOfKeys().FindObject(obj.GetName())
    if(existing):
        tfile.Delete(f"{obj.GetName()};*")  # delete all versions of the object
    obj.Write()


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
            # print(f"4D Bin ({Q2_y_z_pT_4D_Bins}) --> ({Q2_y_Bin}-{z_pT_Bin})")
            return Q2_y_Bin, z_pT_Bin

    return 0, 0


# ----------------------------------------------------------------------
# Decode 2D bin indices into kinematic values
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

    # The reuse logic is commented out for now due to segfault issues when returning
    # existing histograms. Can revisit this later.
    # if((root_file.GetListOfKeys().Contains(ratio_name)) and (not force_ratio)):
    #     print(f"{color.BBLUE}Ratio histogram '{ratio_name}' already exists and force recreation is disabled. Reusing existing histogram.{color.END}")
    #     existing_histo = root_file.Get(ratio_name)
    #     return existing_histo

    num_hist = root_file.Get(num_name)
    den_hist = root_file.Get(den_name)

    if(num_hist is None):
        raise RuntimeError(f"Numerator histogram '{num_name}' not found in file.")
    if(den_hist is None):
        raise RuntimeError(f"Denominator histogram '{den_name}' not found in file.")

    # Clone numerator to get same binning and axis labels
    ratio_hist = num_hist.Clone(ratio_name)
    ratio_hist.SetDirectory(0)  # Detach from file until we explicitly write it
    # ratio_hist.Sumw2()        # Don't use this (I want to keep the original errors set in the original histogram)

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

    Q2_y_Bin_list = []
    Q2_val_list   = []
    y_val_list    = []
    z_val_list    = []
    pT_val_list   = []
    content_list  = []
    error_list    = []

    for ibin in range(1, n_bins + 1):
        Q2_y_z_pT_4D_Bins = int(ratio_hist.GetBinCenter(ibin))

        Q2_y_Bin, z_pT_Bin = decode_Q2_y_and_z_pT(Q2_y_z_pT_4D_Bins)

        if((Q2_y_Bin <= 0) or (z_pT_Bin <= 0)):
            # Skip invalid/underflow mappings
            continue

        bin_content = ratio_hist.GetBinContent(ibin)
        bin_error   = ratio_hist.GetBinError(ibin)

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

    # Instead of ROOT.RDF.MakeNumpyDataFrame (not available in this ROOT), create a small in-memory TTree and wrap it in an RDataFrame.
    n_entries = len(Q2_y_Bin_list)

    memfile = ROOT.TMemFile("tmp_unfold_4D_mem", "RECREATE")
    tree    = ROOT.TTree("h22_tmp", "h22_tmp")

    b_Q2_y_Bin = array.array("i", [0])
    b_Q2_val   = array.array("d", [0.0])
    b_y_val    = array.array("d", [0.0])
    b_z_val    = array.array("d", [0.0])
    b_pT_val   = array.array("d", [0.0])
    b_content  = array.array("d", [0.0])
    b_error    = array.array("d", [0.0])

    tree.Branch("Q2_y_Bin",    b_Q2_y_Bin, "Q2_y_Bin/I")
    tree.Branch("Q2_val",      b_Q2_val,   "Q2_val/D")
    tree.Branch("y_val",       b_y_val,    "y_val/D")
    tree.Branch("z_val",       b_z_val,    "z_val/D")
    tree.Branch("pT_val",      b_pT_val,   "pT_val/D")
    tree.Branch("bin_content", b_content,  "bin_content/D")
    tree.Branch("bin_error",   b_error,    "bin_error/D")

    for index in range(n_entries):
        b_Q2_y_Bin[0] = Q2_y_Bin_list[index]
        b_Q2_val[0]   = Q2_val_list[index]
        b_y_val[0]    = y_val_list[index]
        b_z_val[0]    = z_val_list[index]
        b_pT_val[0]   = pT_val_list[index]
        b_content[0]  = content_list[index]
        b_error[0]    = error_list[index]
        tree.Fill()

    memfile.Write()

    rdf = ROOT.RDataFrame(tree)
    # Keep backing objects alive by attaching them to the rdf object
    rdf._unfold_memfile = memfile
    rdf._unfold_tree    = tree

    return rdf


# ----------------------------------------------------------------------
# Argument parsing
# ----------------------------------------------------------------------
def parse_arguments():
    parser = argparse.ArgumentParser(description="Build ratio histograms and export their 4D-bin contents into an RDataFrame ROOT file.",
                                     formatter_class=RawDefaultsHelpFormatter)

    parser.add_argument("-r", "-inR", "--input_root", default="Unfold_4D_Bins_Test_with_SF_FirstOrder_Almost_All.root",
                        help="Input ROOT file containing the TH1D histograms.\n")
    parser.add_argument("-nh", "--num_hist", default="(1D)_(Bayesian)_(SMEAR=Smear)_(Q2_y_Bin_All)_(z_pT_Bin_All)_(Q2_y_z_pT_4D_Bins)",
                        help="Name of the numerator TH1D histogram in the input file.\n")
    parser.add_argument("-dh", "--den_hist", default="(1D)_(gdf)_(SMEAR='')_(Q2_y_Bin_All)_(z_pT_Bin_All)_(Q2_y_z_pT_4D_Bins)",
                        help="Name of the denominator TH1D histogram in the input file.\n")
    parser.add_argument("-rh", "--ratio_hist", default=None,
                        help="Name to use (or look for) for the ratio TH1D histogram in the input file. Overwrites the default naming.")
    parser.add_argument("-rf", "--rdf_file", default="Kinematic_4D_Unfolding.root",
                        help="Output ROOT file to store the RDataFrame with bin-by-bin values.\nIf this file already exists and `--force_rdf` is not set, all processing is skipped.")

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

    # Decide on ratio histogram name if not provided
    if(args.ratio_hist is None):
        ratio_name = args.num_hist
        for options in ["(Bin)", "(Bayesian)", "(gdf)"]:
            ratio_name = ratio_name.replace(options, "(ratio)")
            if("(ratio)" in ratio_name):
                break
        if("(ratio)" not in ratio_name):
            print(f"{color.Error}Error in updating ratio_name = {color.END_B}'{ratio_name}'\n\t{color.Error}Appending {color.END_B}'_(ratio)'{color.Error} to the end of the name...{color.END}")
            ratio_name = f"{ratio_name}_(ratio)"
    else:
        ratio_name = args.ratio_hist

    try:
        # If the RDataFrame output file already exists and user does not want to overwrite, skip everything
        if(os.path.exists(args.rdf_file) and (not args.force_rdf)):
            msg = f"{color.BBLUE}RDataFrame file '{args.rdf_file}' already exists and --force_rdf was not set. Skipping all processing.{color.END}"
            print(msg if(args.email_message is None) else f"{msg}\n\nUser message:\n{args.email_message}\n")
            # Not worth sending an email if the run purpose is just skipped
            return

        if(not os.path.exists(args.input_root)):
            raise RuntimeError(f"Input ROOT file '{args.input_root}' does not exist.")

        # Open ROOT file in UPDATE mode so we can read and also write the ratio histogram
        root_file = ROOT.TFile.Open(args.input_root, "UPDATE")
        if((root_file is None) or root_file.IsZombie()):
            raise RuntimeError(f"Failed to open input ROOT file '{args.input_root}' in UPDATE mode.")

        # 1–3) Build or reuse ratio histogram, write it safely to the ROOT file
        ratio_hist = build_ratio_histogram(root_file, args.num_hist, args.den_hist, ratio_name, args.force_ratio)

        # Make sure the file is updated on disk
        root_file.Write("", ROOT.TObject.kOverwrite)
        root_file.Close()
        root_file = None

        # 4–5) Convert ratio histogram to RDataFrame and Snapshot to a new ROOT file
        rdf = build_dataframe_from_hist(ratio_hist)

        print(f"{color.BBLUE}Writing RDataFrame to file '{args.rdf_file}' as tree 'h22'.{color.END}")
        rdf.Snapshot("h22", args.rdf_file)
        email_body = f"{color.BGREEN}Done. RDataFrame with 7 columns written to '{args.rdf_file}'.{color.END}"
        email_body += f"\n\nInput ROOT file: {args.input_root}\n"
        email_body += f"Numerator hist:  {args.num_hist}\n"
        email_body += f"Denominator hist:{args.den_hist}\n"
        email_body += f"Ratio hist:      {ratio_name}\n"
        email_body += f"Output RDF file: {args.rdf_file}\n"
        if(args.email_message is not None):
            email_body += f"\nUser message:\n{args.email_message}\n"
        print(email_body)
        if(args.email):
            send_email("python_Unfold_4D_for_weights.py Script Done", email_body)

    except Exception as e:
        email_body = f"\n{color.Error}ERROR in python_Unfold_4D_for_weights.py script:\n{color.END}{e}\n\n{traceback.format_exc()}\n"
        if(args.email_message is not None):
            email_body += f"\nUser message:\n{args.email_message}\n"
        print(email_body)
        if(args.email):
            send_email("python_Unfold_4D_for_weights.py Script Error", email_body)

        # Non-zero exit code to signal failure in batch environments
        sys.exit(1)


if(__name__ == "__main__"):
    main()
