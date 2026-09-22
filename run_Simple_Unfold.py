#!/usr/bin/env python3
"""Drop-in launcher for the C++ 3D/1D unfolding binary (Simple_RooUnfold_SelfContained.py unfold path).

Does not pin ROOTSYS or conda. make uses ROOTSYS/PATH, or CONDA_PREFIX only if already set.
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

CPP_DIR = os.path.join(EXEC_ROOT, "Cpp_Simple_Unfold")
CPP_BIN = os.path.join(CPP_DIR, "Simple_Unfold")
DEFAULT_INPUT = "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_3D_Final_Thesis_Response_Matrices_Final_Thesis_Files_All.root"


class RawDefaultsHelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
    pass


def parse_args():
    p = argparse.ArgumentParser(description="run_Simple_Unfold.py:\n\tLaunch the C++ 3D/1D Bayesian unfolding binary.",
                                formatter_class=RawDefaultsHelpFormatter)
    p.add_argument('-t', '-ns', '--test', '--time', '--no-save',
                   action='store_true', dest='test',
                   help="Run full code but without saving any files.\n")
    p.add_argument('-r', '--root',
                   type=str, default="Unfolded_Histos_From_Simple_Unfold.root",
                   help="Name of ROOT output file to be saved.\n")
    p.add_argument('-no-smear', '--no_smear', action='store_true',
                   help="Unfold with unsmeared Monte Carlo only.\n")
    p.add_argument('-smear', '--smear', action='store_true',
                   help="Unfold with smeared Monte Carlo (default unless --no_smear).\n")
    p.add_argument('-sim', '--simulation', action='store_true', dest='sim',
                   help="Use reconstructed MC instead of experimental data.\n")
    p.add_argument('-bi', '-bayes-it', '--bayes_iterations',
                   type=int, default=None,
                   help="Number of Bayesian iterations. Default follows the Python 3D/1D table unless set.\n")
    p.add_argument('-nt', '-ntoys', '--Num_Toys',
                   type=int, default=500,
                   help="Number of Toys used to estimate the unfolding errors.\n")
    p.add_argument('-err', '--error_mode',
                   type=str, default="toys",
                   choices=["toys", "covariance", "errors", "none"],
                   help="RooUnfold error treatment: toys=kCovToys (default), covariance=kCovariance, errors=kErrors, none=kNoError.\n")
    p.add_argument('-ist', '--iteration_study', action='store_true',
                   help="Optional RooUnfoldParms iteration/regularisation scan (not the default unfolding path).\n")
    p.add_argument('-pmin', '--parm_min', type=float, default=None,
                   help="Optional RooUnfoldParms minimum iteration/regularisation parameter.\n")
    p.add_argument('-pmax', '--parm_max', type=float, default=None,
                   help="Optional RooUnfoldParms maximum iteration/regularisation parameter.\n")
    p.add_argument('-pstep', '--parm_step', type=float, default=None,
                   help="Optional RooUnfoldParms step size.\n")
    p.add_argument('-u1D', '--unfolding_1D', action='store_true',
                   help="Run 1D unfolding only.\n")
    p.add_argument('-u3D', '--unfolding_3D', action='store_true',
                   help="Run 3D unfolding only.\n")
    p.add_argument('-ob', '--old_binning', action='store_true',
                   help="Keep full reconstructed binning (previous behavior).\n")
    p.add_argument('-npac', '--no_post_unfold_acc_cut', action='store_true',
                   help="Disable the legacy acceptance cut applied after unfolding. Pre-unfold reconstructed-bin reduction is unchanged unless --old_binning is also set.\n")
    p.add_argument('-b', '--bins', nargs="+", type=str,
                   default=['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17'],
                   help="List of Q2-y bin indices to run.\n")
    p.add_argument('-v', '--verbose', action='store_true',
                   help="Prints each Histogram name to be saved.\n")
    p.add_argument('-ac', '-acceptance-cut', '--Min_Allowed_Acceptance_Cut',
                   # type=float, default=0.0005,  # Changed to 0.025 on 9/16/2026
                   type=float, default=0.025,
                   help="Cut made on acceptance before a bin is removed from unfolding.\n")
    p.add_argument('-sfin', '--single_file_input', type=str, default=DEFAULT_INPUT,
                   help="Path to the INPUT ROOT file.\n")
    p.add_argument('-e', '--email', action='store_true',
                   help="Sends an email to user when done running.\n")
    p.add_argument('-em', '--email_message', type=str, default="",
                   help="Extra email message (use with --email).\n")
    p.add_argument('-bgs', '--background_source', type=str, default="lundvpk",
                   choices=["lundrho", "lundvpk", "None"],
                   help="Source of rho0 background subtractions from rdf.\n")
    p.add_argument('-urho', '--unfold_exclusive_rho0', action='store_true',
                   help="Optional 3D acceptance-only exclusive rho0 unfold. Uses Simple_RooUnfold_SelfContained.py. Default launches stay on the C++ binary.\n")
    p.add_argument('-rw', '--require_weighed', action='store_true',
                   help="Require a weight tag on mdf/gdf/slice keys.\n")
    p.add_argument('-wt', '--weight_tag', type=str, default="",
                   choices=["", "Acc", "JSON", "Spline", "AccJSON", "AccSpline"],
                   help="Select which weighted histogram set to unfold.\n")
    add_data_root_argument(p)
    p.add_argument('--compile_only', action='store_true',
                   help="Compile the C++ binary and exit.\n")
    p.add_argument('--skip_compile', action='store_true',
                   help="Do not rebuild the C++ binary; require it to already exist.\n")
    p.add_argument('--roounfold_dir', type=str, default=os.environ.get("ROOUNFOLD_DIR", ""),
                   help="RooUnfold source/build directory (sets ROOUNFOLD_DIR for make).\n")
    p.add_argument('pos_bins', nargs='*', metavar='BIN',
                   help="Optional positional Q2-y bin indices (same as --bins).\n")
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
    helpers = os.path.join(EXEC_ROOT, "Cpp_Dedicated_5D_Unfold", "Dedicated_5D_Unfold_Helpers.h")
    sources = [
        os.path.join(CPP_DIR, "Simple_Unfold.cxx"),
        helpers,
        os.path.join(CPP_DIR, "Makefile"),
        os.path.join(EXEC_ROOT, "Cpp_Dedicated_5D_Unfold", "rootconfig.mk"),
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
    if(args.smear):
        cmd.append("--smear")
    if(args.sim):
        cmd.append("--simulation")
    if(args.bayes_iterations is not None):
        cmd.extend(["--bayes_iterations", str(args.bayes_iterations)])
    cmd.extend(["--Num_Toys", str(args.Num_Toys)])
    cmd.extend(["--error_mode", str(args.error_mode)])
    if(args.iteration_study):
        cmd.append("--iteration_study")
    if(args.parm_min is not None):
        cmd.extend(["--parm_min", str(args.parm_min)])
    if(args.parm_max is not None):
        cmd.extend(["--parm_max", str(args.parm_max)])
    if(args.parm_step is not None):
        cmd.extend(["--parm_step", str(args.parm_step)])
    if(args.old_binning):
        cmd.append("--old_binning")
    if(args.no_post_unfold_acc_cut):
        cmd.append("--no_post_unfold_acc_cut")
    if(args.unfolding_1D):
        cmd.append("--unfolding_1D")
    if(args.unfolding_3D):
        cmd.append("--unfolding_3D")
    bins = args.pos_bins if(args.pos_bins) else args.bins
    cmd.append("--bins")
    cmd.extend([str(b) for b in bins])
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
    cmd.extend(["--data_root", args.data_root])
    return cmd


def ensure_roounfold_python_env():
    build = os.path.join(EXEC_ROOT, "New_RooUnfold", "RooUnfold", "build-arm64")
    if(not os.path.isdir(build)):
        return
    os.environ["PYTHONPATH"] = build + (":" + os.environ["PYTHONPATH"] if(os.environ.get("PYTHONPATH")) else "")
    for var in ("LD_LIBRARY_PATH", "DYLD_LIBRARY_PATH"):
        os.environ[var] = build + (":" + os.environ[var] if(os.environ.get(var)) else "")


def build_python_rho_command(args):
    script = os.path.join(EXEC_ROOT, "Simple_RooUnfold_SelfContained.py")
    cmd = [sys.executable, script, "--unfold_exclusive_rho0", "--unfolding_3D"]
    if(args.test):
        cmd.append("--test")
    cmd.extend(["--root", args.root])
    if(args.no_smear):
        cmd.append("--no_smear")
    if(args.smear):
        cmd.append("--smear")
    if(args.sim):
        cmd.append("--simulation")
    if(args.bayes_iterations is not None):
        cmd.extend(["--bayes_iterations", str(args.bayes_iterations)])
    cmd.extend(["--Num_Toys", str(args.Num_Toys)])
    cmd.extend(["--error_mode", str(args.error_mode)])
    if(args.old_binning):
        cmd.append("--old_binning")
    if(args.no_post_unfold_acc_cut):
        cmd.append("--no_post_unfold_acc_cut")
    if(args.verbose):
        cmd.append("--verbose")
    cmd.extend(["--Min_Allowed_Acceptance_Cut", str(args.Min_Allowed_Acceptance_Cut)])
    cmd.extend(["--single_file_input", args.single_file_input])
    if(args.email):
        cmd.append("--email")
    if(args.email_message not in ["", None]):
        cmd.extend(["--email_message", args.email_message])
    if(args.weight_tag not in ["", None]):
        cmd.extend(["--weight_tag", args.weight_tag])
    cmd.extend(["--data_root", args.data_root])
    bins = args.pos_bins if(args.pos_bins) else args.bins
    cmd.extend([str(b) for b in bins])
    return cmd


def main():
    args = parse_args()
    apply_input_if_default(args, "single_file_input", ["-sfin", "--single_file_input"], args.data_root)
    apply_output_if_default(args, "root", ["-r", "--root"], args.data_root, bare_to_data_root=True)
    if(args.unfold_exclusive_rho0):
        if(args.unfolding_1D):
            print("ERROR: --unfold_exclusive_rho0 is 3D only.", file=sys.stderr)
            sys.exit(1)
        if(args.iteration_study or (args.parm_min is not None) or (args.parm_max is not None) or (args.parm_step is not None)):
            print("Exclusive rho0 mode does not forward the C++ iteration-study flags.")
        ensure_roounfold_python_env()
        cmd = build_python_rho_command(args)
        print("Launching Python exclusive rho0 unfolding:")
        print(" ", " ".join(shlex.quote(str(tok)) for tok in cmd))
        os.execv(cmd[0], cmd)
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
