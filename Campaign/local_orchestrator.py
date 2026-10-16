# Run the existing hybrid scripts in order. The next stage starts only when this process sees exit 0.
import glob
import os
import shlex
import subprocess
import sys

_BOOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if(_BOOT not in sys.path):
    sys.path.insert(0, _BOOT)

from Campaign.early_chain import evgen_dir
from Campaign.ifarm_inputs import load_ifarm_inputs, rho_source_token
from Campaign.rc_pairs import pair_rad_nrad, report_pairs
from jlab_work_paths import REL_HADD, data_root_path

EMAIL_TO = "richard.capobianco@uconn.edu"
EXPECTED_RHO = 40
EXPECTED_CLASDIS = 170
BINNED_EVGEN = "/lustre24/expphy/volatile/clas12/richcap/Radiative_MC_EvGen_Files/Binned_Files_Made_through_sbatch"
RC_RUNTIME = "/lustre24/expphy/volatile/clas12/richcap/Radiative_MC_EvGen_Files/build_EvGen_PerFile_Hists_Runtime_ifarm_rc"
GEN_DIR = "/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/Pass2"
REC_DIR = "/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/With_BeamCharge/Pass2/More_Cut_Info"


def mail_stop(stage, detail):
    body = "direct orchestration stopped\nstage: %s\n%s\nThe next stage was not started.\n" % (stage, detail)
    print(body)
    try:
        subprocess.run(["mail", "-s", "SIDIS direct orchestration stopped: %s" % stage, EMAIL_TO], input=body.encode(), check=False)
    except FileNotFoundError:
        print("WARNING: mail command not found; the stop message was printed and was not emailed.")


def show_command(argv):
    print(shlex.join([str(part) for part in argv]))


def run_command(stage, argv, cwd, dry_run):
    print("")
    print("stage %s" % stage)
    show_command(argv)
    if(dry_run):
        return 0
    try:
        proc = subprocess.run([str(part) for part in argv], cwd=cwd)
    except FileNotFoundError:
        mail_stop(stage, "command not found: %s" % argv[0])
        return 1
    if(proc.returncode != 0):
        mail_stop(stage, "exit %s" % proc.returncode)
        return proc.returncode
    return 0


def input_folder(data_root, dry_run):
    root = data_root_path(data_root)
    folder = os.path.join(root, "SIDIS_Campaign", "direct_inputs")
    if(os.path.isdir(root)):
        os.makedirs(folder, exist_ok=True)
        return folder
    if(dry_run):
        folder = os.path.join("/tmp", "SIDIS_direct_inputs")
        os.makedirs(folder, exist_ok=True)
        return folder
    print("data root is not mounted: %s" % root)
    sys.exit(1)


def write_glob_file(folder, name, pattern):
    path = os.path.join(folder, name)
    handle = open(path, "w")
    handle.write(pattern.strip() + "\n")
    handle.close()
    return path


def groovy_command(script, source, mc_type, paths_txt, message):
    return [script, "-m", "hybrid", "-pj", "10", "-na", "-e", "-em", message, "-src", source, "-mc", mc_type, "-ptxt", paths_txt]


def run_early(args):
    config = load_ifarm_inputs()
    token = rho_source_token(config) or "rho0_new"
    rho_glob = config.get("rho_hipo_glob", "")
    clasdis_glob = config.get("clasdis_55na_hipo_glob", "")
    rho_count = len(glob.glob(rho_glob)) if(rho_glob) else 0
    clasdis_count = len(glob.glob(clasdis_glob)) if(clasdis_glob) else 0
    print("rho0 matches %d (required %d)" % (rho_count, EXPECTED_RHO))
    print("55nA clasdis matches %d (required %d)" % (clasdis_count, EXPECTED_CLASDIS))
    if((not args.dry_run) and ((rho_count != EXPECTED_RHO) or (clasdis_count != EXPECTED_CLASDIS))):
        mail_stop("groovy", "refusing to submit: rho0 %d, clasdis %d" % (rho_count, clasdis_count))
        return 1
    folder = input_folder(args.data_root, args.dry_run)
    rho_list = write_glob_file(folder, "rho0_new_runs.txt", rho_glob)
    clasdis_list = write_glob_file(folder, "clasdis_55na_new.txt", clasdis_glob)
    groovy = os.path.join(_BOOT, "Data_Files_Groovy", "run_groovy_scripts_with_emails.py")
    groovy_dir = os.path.dirname(groovy)
    frames = os.path.join(_BOOT, "Histo_Files_ROOT", "DataFrames")
    helper = os.path.join(frames, "run_dataframe_makeROOT_helper.py")
    batches = os.path.join(frames, "run_sidis_DataFrame_pipeline.py")
    submit = os.path.join(frames, "Submit_Full_Histogram_Creation_Pipeline.py")
    fit = os.path.join(frames, "Get_rho_Normalization_values.py")
    merged = os.path.join(data_root_path(args.data_root), REL_HADD, "SIDIS_epip_Response_Matrices_from_RDataFrames_Only_2D_rho0_Normalization_Creation_%s_Final_Thesis_Files_All.root" % token)
    steps = [
        ("groovy_rho_gdf", groovy_command(groovy, "rho0", "gdf", rho_list, "Groovy generated rho0, hybrid, 10 local jobs. Ran in tmuxPython."), groovy_dir),
        ("groovy_rho_mdf", groovy_command(groovy, "rho0", "mdf", rho_list, "Groovy reconstructed rho0, hybrid, 10 local jobs. Ran in tmuxPython."), groovy_dir),
        ("groovy_55na_gdf", groovy_command(groovy, "clasdis", "gdf", clasdis_list, "Groovy generated 55 nA clasdis, hybrid, 10 local jobs. Ran in tmuxPython."), groovy_dir),
        ("groovy_55na_mdf", groovy_command(groovy, "clasdis", "mdf", clasdis_list, "Groovy reconstructed 55 nA clasdis, hybrid, 10 local jobs. Ran in tmuxPython."), groovy_dir),
        ("dataframe_rho_gdf", [helper, "-droot", args.data_root, "-o", "work", "-i", os.path.join(GEN_DIR, "*%s*" % config.get("rho_name_discriminator", "output-rho0_10.6gev")), "-dtype", "gdf", "-m", "hybrid", "-j", "10", "-y", "-e", "-em", "RDataFrame generated rho0. Ran in tmuxPython."], frames),
        ("dataframe_rho_mdf", [helper, "-droot", args.data_root, "-o", "work", "-i", os.path.join(REC_DIR, "*%s*" % config.get("rho_name_discriminator", "output-rho0_10.6gev")), "-dtype", "mdf", "-m", "hybrid", "-j", "10", "-y", "-e", "-em", "RDataFrame reconstructed rho0. Ran in tmuxPython."], frames),
        ("dataframe_55na_gdf", [helper, "-droot", args.data_root, "-o", "work", "-i", os.path.join(GEN_DIR, "*inb-clasdis-55na*"), "-dtype", "gdf", "-m", "hybrid", "-j", "10", "-y", "-e", "-em", "RDataFrame generated 55 nA clasdis. Ran in tmuxPython."], frames),
        ("dataframe_55na_mdf", [helper, "-droot", args.data_root, "-o", "work", "-i", os.path.join(REC_DIR, "*inb-clasdis-55na*"), "-dtype", "mdf", "-m", "hybrid", "-j", "10", "-y", "-e", "-em", "RDataFrame reconstructed 55 nA clasdis. Ran in tmuxPython."], frames),
        ("make_batches", [batches, "-droot", args.data_root, "-m", "make_batches", "-rst", token, "-e", "-em", "make_batches with %s appended after lundvpk and lundrho. Ran in tmuxPython." % token], frames),
        ("rho_hist", [submit, "-droot", args.data_root, "-m", "hybrid", "-rho", "-jrho0", "10", "-n", token, "-e", "-em", "Unweighted rho0 normalization histograms, hybrid, 10 local jobs. Ran in tmuxPython."], frames),
        ("rho_fit", [fit, "-droot", args.data_root, "-st", token, "-usf", "-f1", merged, "-e", "-em", "rho0 normalization fit. Ran in tmuxPython."], frames),
    ]
    for stage, argv, cwd in steps:
        code = run_command(stage, argv, cwd, args.dry_run)
        if(code != 0):
            return code
    if(not args.dry_run):
        print("rho fit finished. Read exclusive_rho_review_%s.txt. Campaign/rho_factors.json is still written by hand before weighted response." % token)
    return 0


def matched_evgen(dry_run):
    if(not os.path.isdir(BINNED_EVGEN)):
        print("binned EvGen directory is not mounted: %s" % BINNED_EVGEN)
        if(dry_run):
            return None
        mail_stop("rc_build", "binned EvGen directory is not mounted")
        sys.exit(1)
    rad_files = []
    nrad_files = []
    for path in sorted(glob.glob(os.path.join(BINNED_EVGEN, "*.root"))):
        base = os.path.basename(path)
        if("_No_Rad_" in base):
            nrad_files.append(path)
        elif("_Rad_" in base):
            rad_files.append(path)
    try:
        paired = pair_rad_nrad(rad_files, nrad_files)
    except ValueError as exc:
        print(exc)
        if(dry_run):
            return None
        mail_stop("rc_build", str(exc))
        sys.exit(1)
    report_pairs(paired)
    if(len(paired["matched"]) == 0):
        print("no Rad/No_Rad pairs")
        if(dry_run):
            return None
        mail_stop("rc_build", "no Rad/No_Rad pairs")
        sys.exit(1)
    return paired


def run_rc(args):
    if(args.rc_mode != "regenerate"):
        print("rc_mode %s has no direct command" % args.rc_mode)
        return 1
    compare_dir = os.path.join(evgen_dir(), "Run_Large_Files_For_Iterative_Corrections", "Comparison_With_Unfolding")
    build = os.path.join(compare_dir, "Build_EvGen_PerFile_Hists.py")
    compare = os.path.join(compare_dir, "Comparison_Between_GEN_and_Unfold.py")
    merged = os.path.join(RC_RUNTIME, "merged_outputs", "Merged_EvGen_PerFile_Hists.root")
    rc_out = os.path.join(RC_RUNTIME, "merged_outputs", "RC_Factors_ifarm_rc.root")
    paired = matched_evgen(args.dry_run)
    argv = [build, "-m", "hybrid", "-y", "-p", "-mpj", "10", "-e", "-em", "EvGen per-file RC histograms, hybrid, 10 local jobs. Ran in tmuxRADGEN.", "-rdir", RC_RUNTIME]
    if(paired is not None):
        argv.extend(["-rrad"] + list(paired["rad"]))
        argv.extend(["-rnrad"] + list(paired["nrad"]))
    else:
        print("RC file list is added when the binned directory is visible")
    code = run_command("rc_build", argv, compare_dir, args.dry_run)
    if(code != 0):
        return code
    argv = [compare, "-r", merged, "-ssf", "-sfn", rc_out, "-rc", "-Nw", "-evgen"]
    return run_command("rc_compare", argv, compare_dir, args.dry_run)


def run_bc(args):
    bc_dir = os.path.join(_BOOT, "BC_Corrections")
    runner = os.path.join(bc_dir, "Run_BC_Scripts_Locally.py")
    factor = os.path.join(bc_dir, "BC_Corrections_Script.py")
    per_file = "./BC_Corrections_Script.py -nb 3 -nbphi 2 -hi -ufn --root_file_out ROOT_Files_Output/Sub_Bin_Contents_for_BC_Correction.root"
    code = run_command("bc_hist", [runner, "-rm", "hybrid", "-j", "10", "-y", "-e", "-rcl", "BC per-file histograms. Ran in tmuxBC.", "-c", per_file], bc_dir, args.dry_run)
    if(code != 0):
        return code
    dest = "ROOT_Files_Output/Sub_Bin_Contents_for_BC_Correction_with_Binned_sbatch.root"
    inputs = sorted(glob.glob(os.path.join(bc_dir, "ROOT_Files_Output", "Sub_Bin_Contents_for_BC_Correction_*EvGen*.root")))
    if((len(inputs) == 0) and (not args.dry_run)):
        mail_stop("bc_hadd", "no per-file BC ROOT files matched Sub_Bin_Contents_for_BC_Correction_*EvGen*.root")
        return 1
    relative_inputs = [os.path.relpath(path, bc_dir) for path in inputs]
    if((len(relative_inputs) == 0) and args.dry_run):
        relative_inputs = ["ROOT_Files_Output/Sub_Bin_Contents_for_BC_Correction_*EvGen*.root"]
    code = run_command("bc_hadd", ["hadd_richcap", dest] + relative_inputs, bc_dir, args.dry_run)
    if(code != 0):
        return code
    argv = [factor, "-jf", "Sub_Bin_Contents_for_BC_Correction_with_Binned_sbatch.json", "-nb", "3", "-nbphi", "2", "-bc", "--root_file_out", dest, "-e", "-em", "BC factors from the merged histogram. Ran in tmuxBC."]
    return run_command("bc_factors", argv, bc_dir, args.dry_run)


def run_direct(args):
    if(args.stage == "early_chain"):
        code = run_early(args)
    elif(args.stage == "rc_regenerate"):
        code = run_rc(args)
    elif(args.stage == "bc"):
        code = run_bc(args)
    else:
        print("direct orchestration does not run stage %s" % args.stage)
        code = 1
    if(code != 0):
        sys.exit(code)
