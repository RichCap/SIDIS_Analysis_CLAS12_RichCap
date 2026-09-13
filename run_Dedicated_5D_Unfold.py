#!/usr/bin/env python3
"""Drop-in launcher for the C++ Dedicated 5D unfolding binary.

Same flags as Dedicated_5D_Unfold.py. Resolves JLab data-root paths in Python,
generates the C++ binning header if needed, compiles the binary if needed, then
execs Cpp_Dedicated_5D_Unfold/Dedicated_5D_Unfold.
"""

import argparse
import os
import shlex
import subprocess
import sys

_BOOT = os.path.abspath(os.path.dirname(__file__))
if(_BOOT not in sys.path):
    sys.path.insert(0, _BOOT)
from jlab_work_paths import add_data_root_argument, apply_input_if_default, apply_output_if_default, bootstrap_from_file
EXEC_ROOT = bootstrap_from_file(__file__)

CPP_DIR = os.path.join(EXEC_ROOT, "Cpp_Dedicated_5D_Unfold")
CPP_BIN = os.path.join(CPP_DIR, "Dedicated_5D_Unfold")
GENERATOR = os.path.join(EXEC_ROOT, "Generate_Dedicated_5D_Unfold_Cpp_Binning.py")
BINNING_HDR = os.path.join(CPP_DIR, "generated", "Dedicated_5D_Binning.h")
BINNING_SOURCES = [
    os.path.join(EXEC_ROOT, "MyCommonAnalysisFunction_richcap.py"),
    os.path.join(EXEC_ROOT, "Convert_MultiDim_Kinematic_Bins.py"),
    GENERATOR,
]


class RawDefaultsHelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
    pass


def parse_args():
    p = argparse.ArgumentParser(description="run_Dedicated_5D_Unfold.py:\n\tLaunch the C++ 5D Bayesian unfolding binary with the same flags as Dedicated_5D_Unfold.py.",
                                formatter_class=RawDefaultsHelpFormatter)
    p.add_argument('-t', '-ns', '--test', '--time', '--no-save',
                   action='store_true',
                   dest='test',
                   help="Run full code but without saving any files.\n")
    p.add_argument('-r', '--root',
                   type=str,
                   default="Unfolded_5D_Histos_From_Dedicated_5D_Unfold.root",
                   help="Name of ROOT output file to be saved.\n")
    p.add_argument('-no-smear', '--no_smear',
                   action='store_true',
                   help="Unfold with unsmeared Monte Carlo only.\n")
    p.add_argument('-sim', '--simulation',
                   action='store_true',
                   dest='sim',
                   help="Use reconstructed MC instead of experimental data.\n")
    p.add_argument('-mod', '--modulation',
                   action='store_true',
                   dest='mod',
                   help="Use modulated MC files to create response matrices.\n")
    p.add_argument('-bi', '-bayes-it', '--bayes_iterations',
                   type=int,
                   default=6,
                   help="Number of Bayesian Iterations performed while Unfolding.\n")
    p.add_argument('-nt', '-ntoys', '--Num_Toys',
                   type=int,
                   default=10,
                   help="Number of Toys used to estimate the unfolding errors.\n")
    p.add_argument('-b', '--bins',
                   nargs="+",
                   type=str,
                   default=['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17'],
                   help="List of Q2-y bin indices to run.\n")
    p.add_argument('-v', '--verbose',
                   action='store_true',
                   help="Prints each Histogram name to be saved.\n")
    p.add_argument('-ac', '-acceptance-cut', '--Min_Allowed_Acceptance_Cut',
                   type=float,
                   default=0.0005,
                   help="Cut made on acceptance before a bin is removed from unfolding.\n")
    p.add_argument('-sfin', '--single_file_input',
                   type=str,
                   default="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_5D_1st_Order_V2_Response_Matrices_Final_Analysis_Iterations_I0_All.root",
                   help="Path to the INPUT ROOT file.\n")
    p.add_argument('-e', '--email',
                   action='store_true',
                   help="Sends an email to user when done running.\n")
    p.add_argument('-em', '--email_message',
                   type=str,
                   default="",
                   help="Extra email message (use with --email).\n")
    p.add_argument('-bgs', '--background_source',
                   type=str,
                   default="lundvpk",
                   choices=["lundrho", "lundvpk", "None"],
                   help="Source of rho0 background subtractions from rdf.\n")
    p.add_argument('-rw', '--require_weighed',
                   action='store_true',
                   help="Require a weight tag on mdf/gdf/slice keys (legacy _(Weighed) or Acc/JSON/Spline tags). Default: reject weighed.\n")
    p.add_argument('-wt', '--weight_tag',
                   type=str,
                   default="",
                   choices=["", "Acc", "JSON", "Spline", "AccJSON", "AccSpline"],
                   help="Select which weighted histogram set to unfold. Empty = unweighted (default). Auto-tags output ROOT name.\n")
    p.add_argument('-i', '--increment',
                   type=int,
                   default=None,
                   help="Optional: force slice increment; crashes if mismatch with auto-detect.\n")
    p.add_argument('-nb', '--num_bins',
                   type=int,
                   default=None,
                   help="Optional: force flattened 5D bin count; crashes if mismatch with auto-detect.\n")
    p.add_argument('-mpdf', '--matrix_pdf',
                   action='store_true',
                   help="Rebuild the 5D response matrix and save a PDF only (no unfolding).\n")
    p.add_argument('-pdf', '--pdf_name',
                   type=str,
                   default="Rebuilt_5D_Response_Matrix.pdf",
                   help="PDF output path for --matrix_pdf mode.\n")
    p.add_argument('-lz', '--logz',
                   action='store_true',
                   help="Use log scale on the PDF Z-axis.\n")
    p.add_argument('-rs', '--recover_slices',
                   action='store_true',
                   help="Skip unfolding; load existing args.root, rename/resave the raw 'unfolded' hist if needed, and only run Multi5D_Slice for Bayesian.\n")
    add_data_root_argument(p)
    p.add_argument('--compile-only',
                   action='store_true',
                   help="Generate binning header, compile the C++ binary, and exit.\n")
    p.add_argument('--generate-binning-only',
                   action='store_true',
                   help="Regenerate Cpp_Dedicated_5D_Unfold/generated/Dedicated_5D_Binning.h and exit.\n")
    p.add_argument('--skip-compile',
                   action='store_true',
                   help="Do not rebuild the C++ binary; require it to already exist.\n")
    p.add_argument('--roounfold-dir',
                   type=str,
                   default=os.environ.get("ROOUNFOLD_DIR", ""),
                   help="RooUnfold source/build directory (sets ROOUNFOLD_DIR for make).\n")
    return p.parse_args()


def newer_than(target, sources):
    if(not os.path.isfile(target)):
        return True
    target_mtime = os.path.getmtime(target)
    for src in sources:
        if(os.path.isfile(src) and (os.path.getmtime(src) > target_mtime)):
            return True
    return False


def run_checked(cmd, cwd=None, env=None):
    print("Running:", " ".join(shlex.quote(str(tok)) for tok in cmd))
    proc = subprocess.run(cmd, cwd=cwd, env=env)
    if(proc.returncode != 0):
        sys.exit(proc.returncode)
    return proc.returncode


def ensure_binning_header(force=False):
    if(force or newer_than(BINNING_HDR, BINNING_SOURCES)):
        run_checked([sys.executable, GENERATOR, "--output", BINNING_HDR])


def find_roounfold_dir(explicit):
    candidates = []
    if(explicit):
        candidates.append(explicit)
    env_dir = os.environ.get("ROOUNFOLD_DIR", "")
    if(env_dir):
        candidates.append(env_dir)
    candidates.extend([
        os.path.join(EXEC_ROOT, "New_RooUnfold", "RooUnfold"),
        "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/New_RooUnfold/RooUnfold",
        "/w/ceph24/hallb/clas12/users/richcap/SIDIS_Analysis_CLAS12_RichCap/New_RooUnfold/RooUnfold",
    ])
    for path in candidates:
        if(path and os.path.isdir(path)):
            return path
    return explicit or env_dir or ""


def ensure_binary(roounfold_dir, skip_compile=False):
    sources = [
        os.path.join(CPP_DIR, "Dedicated_5D_Unfold.cxx"),
        os.path.join(CPP_DIR, "Dedicated_5D_Unfold_Helpers.h"),
        BINNING_HDR,
        os.path.join(CPP_DIR, "Makefile"),
    ]
    if(skip_compile):
        if(not os.path.isfile(CPP_BIN)):
            print(f"ERROR: C++ binary not found: {CPP_BIN}", file=sys.stderr)
            sys.exit(1)
        return
    if(newer_than(CPP_BIN, sources)):
        env = os.environ.copy()
        if(roounfold_dir):
            env["ROOUNFOLD_DIR"] = roounfold_dir
        run_checked(["make", "-C", CPP_DIR], env=env)


def build_cpp_command(args):
    cmd = [CPP_BIN]
    if(args.test):
        cmd.append("--test")
    cmd.extend(["--root", args.root])
    if(args.no_smear):
        cmd.append("--no_smear")
    if(args.sim):
        cmd.append("--simulation")
    if(args.mod):
        cmd.append("--modulation")
    cmd.extend(["--bayes_iterations", str(args.bayes_iterations)])
    cmd.extend(["--Num_Toys", str(args.Num_Toys)])
    cmd.append("--bins")
    cmd.extend([str(b) for b in args.bins])
    if(args.verbose):
        cmd.append("--verbose")
    cmd.extend(["--Min_Allowed_Acceptance_Cut", str(args.Min_Allowed_Acceptance_Cut)])
    cmd.extend(["--single_file_input", args.single_file_input])
    if(args.email):
        cmd.append("--email")
    if(args.email_message not in ["", None]):
        cmd.extend(["--email_message", args.email_message])
    cmd.extend(["--background_source", args.background_source])
    if(args.require_weighed):
        cmd.append("--require_weighed")
    if(args.weight_tag not in ["", None]):
        cmd.extend(["--weight_tag", args.weight_tag])
    if(args.increment is not None):
        cmd.extend(["--increment", str(args.increment)])
    if(args.num_bins is not None):
        cmd.extend(["--num_bins", str(args.num_bins)])
    if(args.matrix_pdf):
        cmd.append("--matrix_pdf")
    cmd.extend(["--pdf_name", args.pdf_name])
    if(args.logz):
        cmd.append("--logz")
    if(args.recover_slices):
        cmd.append("--recover_slices")
    cmd.extend(["--data_root", args.data_root])
    return cmd


def main():
    args = parse_args()
    apply_input_if_default(args, "single_file_input", ["-sfin", "--single_file_input"], args.data_root)
    apply_output_if_default(args, "root", ["-r", "--root"], args.data_root, bare_to_data_root=True)
    apply_output_if_default(args, "pdf_name", ["-pdf", "--pdf_name"], args.data_root, bare_to_data_root=True)

    ensure_binning_header(force=args.generate_binning_only)
    if(args.generate_binning_only):
        return 0

    roounfold_dir = find_roounfold_dir(args.roounfold_dir)
    ensure_binary(roounfold_dir, skip_compile=args.skip_compile)
    if(args.compile_only):
        print(f"Compiled {CPP_BIN}")
        return 0

    cmd = build_cpp_command(args)
    print("Launching C++ unfolding:")
    print(" ", " ".join(shlex.quote(str(tok)) for tok in cmd))
    os.execvp(cmd[0], cmd)


if(__name__ == "__main__"):
    sys.exit(main() or 0)
