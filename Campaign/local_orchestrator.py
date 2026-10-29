# Run the existing hybrid scripts in order. The next stage starts only when this process sees exit 0.
import glob
import hashlib
import json
import os
import shlex
import shutil
import subprocess
import sys
import threading
import time

_BOOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if(_BOOT not in sys.path):
    sys.path.insert(0, _BOOT)

from Campaign.early_chain import evgen_dir
from Campaign.ifarm_inputs import classify_rho_name, load_ifarm_inputs, rho_source_token
from Campaign.rc_pairs import pair_rad_nrad, report_pairs
from jlab_work_paths import REL_FILE_BATCHES, REL_HADD, data_root_path, dataframe_output_dir

EMAIL_TO = "richard.capobianco@uconn.edu"
BINNED_EVGEN = "/lustre24/expphy/volatile/clas12/richcap/Radiative_MC_EvGen_Files/Binned_Files_Made_through_sbatch"
RC_RUNTIME = "/lustre24/expphy/volatile/clas12/richcap/Radiative_MC_EvGen_Files/build_EvGen_PerFile_Hists_Runtime_ifarm_rc"
GEN_DIR = "/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/Pass2"
REC_DIR = "/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/With_BeamCharge/Pass2/More_Cut_Info"
# BC_NO_RAD = "/lustre24/expphy/volatile/clas12/richcap/Radiative_MC_EvGen_Files/Binned_Files_Made_through_sbatch/LUND_EvGen_Iterative_richcap_SBATCH_richcap_Old_MM_Cut_Groups_*No_Rad*.root"
# Final_Groups supplements Old_MM in the same directory. A name contains only one of the two prefixes.
BC_NO_RAD_PATTERNS = [
    BINNED_EVGEN + "/LUND_EvGen_Iterative_richcap_SBATCH_richcap_Old_MM_Cut_Groups_*No_Rad*.root",
    BINNED_EVGEN + "/LUND_EvGen_Iterative_richcap_SBATCH_richcap_Final_Groups_*No_Rad*.root",
]
BC_NO_RAD_BRACE = BINNED_EVGEN + "/LUND_EvGen_Iterative_richcap_SBATCH_richcap_{Old_MM_Cut_Groups,Final_Groups}_*No_Rad*.root"


def mail_note(subject, body):
    print(body)
    try:
        subprocess.run(["mail", "-s", subject, EMAIL_TO], input=body.encode(), check=False)
    except FileNotFoundError:
        print("WARNING: mail command not found; the message was printed and was not emailed.")


def mail_stop(stage, detail):
    mail_note("SIDIS phase %s failed" % stage, "phase: %s\ncause: %s\nThe next phase was not started.\n" % (stage, detail))


def phase_message(args, phase):
    if(getattr(args, "email_message", None)):
        return args.email_message
    return "phase %s" % phase


def record_phase(folder, phase, status):
    path = os.path.join(folder, "phase_status.json")
    phases = {}
    if(os.path.isfile(path)):
        handle = open(path)
        payload = json.load(handle)
        handle.close()
        phases = dict(payload.get("phases", {}))
    phases[phase] = status
    handle = open(path, "w")
    json.dump({"phases": phases}, handle, indent=2)
    handle.write("\n")
    handle.close()


def show_command(argv):
    print(shlex.join([str(part) for part in argv]))


def run_reserved(stage, argv, cwd, dry_run, mode, data_root, next_phase="", mail_success=False):
    print("")
    print("phase %s" % stage)
    show_command(argv)
    if(dry_run):
        return 0
    from Campaign.local_resource_gate import acquire_blocking, bind_worker, release
    token = acquire_blocking(data_root, mode)
    try:
        try:
            proc = subprocess.Popen([str(part) for part in argv], cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        except FileNotFoundError:
            mail_stop(stage, "command not found: %s" % argv[0])
            return 1
        bind_worker(data_root, token, proc.pid)
        tail = []
        for line in proc.stdout:
            print(line, end="")
            tail.append(line)
            if(len(tail) > 80):
                tail.pop(0)
        code = proc.wait()
        excerpt = "".join(tail)
        if(code != 0):
            mail_stop(stage, "exit %s\n\n%s" % (code, excerpt))
            return code
        if(mail_success):
            mail_note("SIDIS phase %s finished" % stage, "phase %s finished.\nnext phase: %s\n" % (stage, next_phase if(next_phase) else "none"))
        return 0
    finally:
        release(data_root, token)


def run_command(stage, argv, cwd, dry_run, next_phase="", mail_success=True):
    print("")
    print("phase %s" % stage)
    show_command(argv)
    if(dry_run):
        return 0
    try:
        proc = subprocess.Popen([str(part) for part in argv], cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    except FileNotFoundError:
        mail_stop(stage, "command not found: %s" % argv[0])
        return 1
    tail = []
    for line in proc.stdout:
        print(line, end="")
        tail.append(line)
        if(len(tail) > 80):
            tail.pop(0)
    code = proc.wait()
    excerpt = "".join(tail)
    if(code != 0):
        mail_stop(stage, "exit %s\n\n%s" % (code, excerpt))
        return code
    if(mail_success):
        mail_note("SIDIS phase %s finished" % stage, "phase %s finished.\nnext phase: %s\n" % (stage, next_phase if(next_phase) else "none"))
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


def hipo_file_num(name):
    # Same token as Check_Converted_Files.py: the last '-' piece, or the piece after nSidis_00.
    text = os.path.basename(name)
    if("nSidis_00" in text):
        parts = text.split("nSidis_00")
    else:
        parts = text.split("-")
    if(len(parts) < 2):
        return ""
    return parts[-1].split(".hipo")[0]


def root_module_ready():
    try:
        import ROOT
        return True
    except Exception:
        return False


def root_is_usable(path, need_h22=True):
    # Header check only. Do not read histograms or event counts.
    # Groovy and DataFrame files carry an h22 tree. BC and RC histogram files do not.
    if((path in [None, ""]) or (not os.path.isfile(path))):
        return False
    try:
        if(os.path.getsize(path) <= 0):
            return False
    except OSError:
        return False
    try:
        import ROOT
    except Exception:
        return False
    root_file = None
    try:
        root_file = ROOT.TFile.Open(str(path), "READ")
        if(root_file is None):
            return False
        if(root_file.IsZombie()):
            return False
        if(hasattr(ROOT.TFile, "kRecovered") and root_file.TestBit(ROOT.TFile.kRecovered)):
            return False
        if(not need_h22):
            return True
        tree_now = root_file.Get("h22")
        if(tree_now is None):
            return False
        if(not tree_now.InheritsFrom("TTree")):
            return False
        return True
    except Exception:
        return False
    finally:
        if(root_file is not None):
            try:
                root_file.Close()
            except Exception:
                pass


def text_is_present(path):
    if(not os.path.isfile(path)):
        return False
    try:
        return os.path.getsize(path) > 0
    except OSError:
        return False


def matching_groovy_roots(hipo_path, source, mc_type):
    # Check_Converted_Files.py searches *qa.new10.*<file_num>*.root rather than one exact name.
    file_num = hipo_file_num(hipo_path)
    if(file_num == ""):
        return []
    folder = GEN_DIR if(mc_type == "gdf") else REC_DIR
    # Rho0 names are inb.qa.rho0.new10.<hipo basename>. Clasdis names are inb.qa.new10.<hipo basename>.
    if(source == "rho0"):
        pattern = os.path.join(folder, "*qa.rho0.new10.*%s*.root" % file_num)
    else:
        pattern = os.path.join(folder, "*qa.new10.*%s*.root" % file_num)
    found = []
    for path in sorted(glob.glob(pattern)):
        base = os.path.basename(path)
        if((source == "rho0") and (".rho0." not in base)):
            continue
        if((source != "rho0") and (".rho0." in base)):
            continue
        if(root_is_usable(path)):
            found.append(path)
    return found


def split_groovy_outputs(paths, source, mc_type):
    done = []
    missing = []
    for hipo in paths:
        roots = matching_groovy_roots(hipo, source, mc_type)
        if(len(roots) > 0):
            done.append(roots[0])
        else:
            missing.append(hipo)
    return done, missing


def dataframes_are_ready(data_root, rho_paths, clasdis_paths):
    groups = [("rho0", "gdf", rho_paths), ("rho0", "mdf", rho_paths), ("clasdis", "gdf", clasdis_paths), ("clasdis", "mdf", clasdis_paths)]
    for source, mc_type, hipos in groups:
        done_roots, missing_hipos = split_groovy_outputs(hipos, source, mc_type)
        if((len(hipos) == 0) or (len(missing_hipos) > 0)):
            return False
        for groovy_path in done_roots:
            frame = dataframe_output_path(groovy_path, mc_type, data_root)
            if((frame == "") or (not root_is_usable(frame))):
                return False
    return True


def dataframe_output_path(groovy_path, data_type, data_root):
    text = os.path.basename(groovy_path).split(".hipo")[0]
    if(".new10." not in text):
        return ""
    label = classify_rho_name(text) or "SIDIS"
    tail = text.split(".new10.")[-1].replace("nSidis_00", "")
    mc = "EvGen_" if("EvGen" in tail) else ""
    background = "55nA_" if("55na" in tail.lower()) else ""
    tail = background + tail.split("10604MeV-")[-1]
    tail = mc + tail.split("-")[-1]
    common = "Pass_2_Final_Analysis_Iterations_I0_"
    if(label not in ["SIDIS", ""]):
        common = common + label + "_"
    if(data_type == "gdf"):
        name = "DataFrame_SIDIS_epip_MC_GEN_%s%s.root" % (common, tail)
    else:
        name = "DataFrame_SIDIS_epip_MC_Matched_%s%s.root" % (common, tail)
    return os.path.join(dataframe_output_dir(data_root, data_type), name.replace("__", "_"))


def write_path_list(folder, name, paths):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, name)
    handle = open(path, "w")
    for item in paths:
        handle.write(item + "\n")
    handle.close()
    return path


def bc_output_name(input_path):
    name = os.path.basename(input_path).split("new6.")[-1].replace(".hipo.root", "").replace(".root", "")
    return "Sub_Bin_Contents_for_BC_Correction_%s.root" % name


def bc_root_dir():
    return os.path.join(_BOOT, "BC_Corrections", "ROOT_Files_Output")


def bc_run_tag(label, explicit=None):
    # Run_BC's default tag is BC_New_Bins_from_BC_Cuts plus the date. A sensitivity does not share that directory.
    if(explicit not in [None, ""]):
        base = str(explicit)
    else:
        base = "BC_New_Bins_from_BC_Cuts_%s" % time.strftime("%m_%d_%Y")
    if(label not in [None, ""]):
        return "%s_%s" % (base, label)
    return base


def bc_run_directory(tag):
    return os.path.join(bc_root_dir(), "Path_to_Volatile", tag)


def bc_output_candidates(input_path, label, tag):
    # Per-file campaign outputs live only in this run directory, not in the flat ROOT_Files_Output parent.
    out_name = bc_output_name(input_path)
    path = os.path.join(bc_run_directory(tag), out_name)
    if(os.path.isfile(path)):
        return [path]
    return []


def bc_expected_bins():
    # Same kept bins as Create_Histograms_for_BC. Do not copy its skip list.
    from MyCommonAnalysisFunction_richcap import skip_condition_z_pT_bins
    bins = []
    for q2_bin in range(1, 18):
        for zpt_bin in range(1, 37):
            if(skip_condition_z_pT_bins(Q2_Y_BIN=q2_bin, Z_PT_BIN=zpt_bin, BINNING_METHOD="Y_bin")):
                continue
            bins.append((q2_bin, zpt_bin))
    return bins


# Current skip_condition drops these three. October 18 files still contain them.
BC_EXTRA_BINS = [(3, 6), (11, 5), (14, 6)]


def bc_hist_name(q2_bin, zpt_bin):
    # Every direct command passes -nb 3 -nbphi 2. Per-axis overrides are not in this name.
    return "Histogram Bin (%d-%d)-(Num SubBins=3)-(Extra phi_h SubBins=2)" % (q2_bin, zpt_bin)


def bc_extra_names():
    names = []
    for q2_bin, zpt_bin in BC_EXTRA_BINS:
        names.append(bc_hist_name(q2_bin, zpt_bin))
    return names


def bc_nsub(counts):
    return counts["q2"] * counts["y"] * counts["z"] * counts["pt"] * counts["phi"]


BC_STATUS_CACHE = {}


def bc_histogram_status(path, counts):
    # Integrity only. Histogram count, names, and axis sizes are not judged.
    # "unread" means the file was not judged, so the caller must not delete it.
    if((path in [None, ""]) or (not os.path.isfile(path))):
        return "missing"
    try:
        stamp = (os.path.getsize(path), os.path.getmtime(path))
    except OSError:
        return "unread"
    cache_key = (os.path.abspath(path), counts["q2"], counts["y"], counts["z"], counts["pt"], counts["phi"], stamp)
    if(cache_key in BC_STATUS_CACHE):
        return BC_STATUS_CACHE[cache_key]
    if(stamp[0] <= 0):
        BC_STATUS_CACHE[cache_key] = "incomplete"
        return "incomplete"
    try:
        import ROOT
    except Exception:
        return "unread"
    # expected = []
    # for q2_bin, zpt_bin in bc_expected_bins():
    #     expected.append(bc_hist_name(q2_bin, zpt_bin))
    # nx_need = bc_nsub(counts) + 2
    root_file = None
    status = "unread"
    reason = ""
    try:
        root_file = ROOT.TFile.Open(str(path), "READ")
        if(root_file is None):
            status = "incomplete"
            reason = "unreadable %s" % path
        elif(root_file.IsZombie()):
            status = "incomplete"
            reason = "unreadable %s" % path
        elif(hasattr(ROOT.TFile, "kRecovered") and root_file.TestBit(ROOT.TFile.kRecovered)):
            status = "incomplete"
            reason = "recovered %s" % path
        else:
            # Histogram count, names, and axis sizes are not acceptance rules.
            # classes = {}
            # for key in root_file.GetListOfKeys():
            #     classes[str(key.GetName())] = str(key.GetClassName())
            # allowed_extra = bc_extra_names()
            # for name, klass in classes.items():
            #     if(name.startswith("Histogram Bin (") and (name not in expected) and (name not in allowed_extra)):
            #         status = "incomplete"
            #         reason = "unexpected histogram %s in %s" % (name, path)
            #         break
            # for name in expected:
            #     hist = root_file.Get(name)
            #     if((hist is None) or (hist.GetNbinsX() != nx_need) or (hist.GetNbinsY() != 24)):
            #         status = "incomplete"
            #         reason = "axis %s is not the expected size in %s" % (name, path)
            #         break
            status = "complete"
    except Exception:
        status = "unread"
    finally:
        if(root_file is not None):
            try:
                root_file.Close()
            except Exception:
                pass
    if(status != "unread"):
        BC_STATUS_CACHE[cache_key] = status
    if((status not in ["complete", "unread"]) and (reason != "")):
        print(reason)
    return status


def bc_histograms_match(path, counts):
    return bc_histogram_status(path, counts) == "complete"


def bc_filtered_copy(path, dest):
    # The merge receives the 452 current bins. The three older histograms stay in the original file.
    try:
        import ROOT
    except Exception:
        return False
    src = None
    out = None
    try:
        src = ROOT.TFile.Open(str(path), "READ")
        if((src is None) or src.IsZombie()):
            return False
        out = ROOT.TFile(str(dest), "RECREATE")
        if((out is None) or out.IsZombie()):
            return False
        for q2_bin, zpt_bin in bc_expected_bins():
            name = bc_hist_name(q2_bin, zpt_bin)
            hist = src.Get(name)
            if(hist is None):
                return False
            hist.Write()
        return True
    except Exception:
        return False
    finally:
        if(out is not None):
            try:
                out.Close()
            except Exception:
                pass
        if(src is not None):
            try:
                src.Close()
            except Exception:
                pass


def bc_output_path(input_path, label, counts, tag):
    saw_unread = False
    for path in bc_output_candidates(input_path, label, tag):
        status = bc_histogram_status(path, counts)
        if(status == "complete"):
            return path
        if(status == "unread"):
            saw_unread = True
    if(saw_unread):
        return None
    return ""


def bc_complete_outputs(inputs, label, counts, tag):
    found = []
    seen = set()
    for bc_input in inputs:
        path = bc_output_path(bc_input, label, counts, tag)
        if(path is None):
            return None
        if((path == "") or (path in seen)):
            continue
        seen.add(path)
        found.append(path)
    return found


def remove_incomplete_bc_outputs(input_path, label, counts, dry_run, tag):
    # A rejected file stays where it is. The next worker must not be pointed at it until a replacement is ready.
    del dry_run
    for path in bc_output_candidates(input_path, label, tag):
        status = bc_histogram_status(path, counts)
        if(status == "complete"):
            continue
        print("BC output was not removed: %s (%s)" % (path, status))
    return True


def bc_merged_path(tag):
    return os.path.join(bc_run_directory(tag), "Sub_Bin_Contents_for_BC_Correction_with_Binned_sbatch.root")


def bc_json_path(tag):
    return os.path.join(bc_run_directory(tag), "Sub_Bin_Contents_for_BC_Correction_with_Binned_sbatch.json")


def bc_json_complete(path, counts):
    if(not text_is_present(path)):
        return False
    try:
        handle = open(path)
        payload = json.load(handle)
        handle.close()
    except Exception:
        return False
    meta = payload.get("meta", {})
    expected_meta = {
        "num_sub_bins": 3,
        "extra_num_phi_sub_bins": 2,
        "num_sub_bins_q2": counts["q2"],
        "num_sub_bins_y": counts["y"],
        "num_sub_bins_z": counts["z"],
        "num_sub_bins_pt": counts["pt"],
        "num_sub_bins_phi": counts["phi"],
    }
    for key, value in expected_meta.items():
        if(key not in meta):
            return False
        if(int(meta[key]) != value):
            return False
    results = payload.get("results", {})
    for q2_bin, zpt_bin in bc_expected_bins():
        for phi_bin in range(1, 25):
            if(("Bin (%d-%d-%d)" % (q2_bin, zpt_bin, phi_bin)) not in results):
                return False
    return True


def bc_worker_command(label, counts):
    # --root_file_out is left unset so Run_BC writes the absolute Path_to_Volatile/<tag> path.
    # out_rel = "ROOT_Files_Output/Sub_Bin_Contents_for_BC_Correction.root"
    if(label == ""):
        return "./BC_Corrections_Script.py -nb 3 -nbphi 2 -hi -ufn"
    return "./BC_Corrections_Script.py -nb 3 -nbphi 2 -nbq %d -nby %d -nbz %d -nbpt %d -nbh %d -hi -ufn" % (
        counts["q2"], counts["y"], counts["z"], counts["pt"], counts["phi"])


def bc_factor_argv(factor, json_path, dest, counts, message, nominal):
    argv = [factor, "-jf", json_path, "-nb", "3", "-nbphi", "2"]
    if(not nominal):
        argv.extend(["-nbq", str(counts["q2"]), "-nby", str(counts["y"]), "-nbz", str(counts["z"]), "-nbpt", str(counts["pt"]), "-nbh", str(counts["phi"])])
    argv.extend(["-bc", "--root_file_out", dest, "-e", "-em", message])
    return argv


def bc_phase_names(label):
    if(label == ""):
        return "bc_hist", "bc_hadd", "bc_factors"
    return "bc_hist_%s" % label, "bc_hadd_%s" % label, "bc_factors_%s" % label


def bc_configurations(systematics):
    nominal = {"label": "", "counts": {"q2": 3, "y": 3, "z": 3, "pt": 3, "phi": 5}}
    configs = [nominal]
    if(systematics not in ["all", "bc_subdivision"]):
        return configs
    handle = open(os.path.join(os.path.dirname(__file__), "systematics.json"))
    table = json.load(handle)["bc_sensitivity"]
    handle.close()
    for variable in ["q2", "y", "z", "pt", "phi"]:
        for value in table[variable]:
            counts = {"q2": 1, "y": 1, "z": 1, "pt": 1, "phi": 1}
            counts[variable] = int(value)
            configs.append({"label": "sens_%s_%s" % (variable, value), "counts": counts})
    return configs


def hadd_executable():
    # hadd_richcap is an alias for $ROOTSYS/bin/hadd. Python does not expand aliases.
    rootsys = os.environ.get("ROOTSYS", "")
    if(rootsys == ""):
        return ""
    path = os.path.join(rootsys, "bin", "hadd")
    if(not os.path.isfile(path)):
        return ""
    return path


def bc_hadd_argv(dest, inputs):
    hadd = hadd_executable()
    if(hadd == ""):
        return []
    return [hadd, dest] + list(inputs)


def rc_factor_names():
    # Same bins Create_RC_Factors writes for --Q2_y_Bin -1 and --Normalize_Weight.
    from MyCommonAnalysisFunction_richcap import Get_Num_of_z_pT_Bins_w_Migrations, skip_condition_z_pT_bins
    names = []
    for q2_bin in range(0, 18):
        q2_tag = "All" if(q2_bin == 0) else str(q2_bin)
        z_max = 0 if(q2_bin == 0) else Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=q2_bin)[1]
        for zpt_bin in range(0, z_max + 1):
            if((zpt_bin != 0) and skip_condition_z_pT_bins(Q2_Y_BIN=q2_bin, Z_PT_BIN=zpt_bin)):
                continue
            z_tag = "All" if(zpt_bin == 0) else str(zpt_bin)
            names.append("(RC_Factor)_(gdf)_(SMEAR='')_(Q2_y_Bin_%s)_(z_pT_Bin_%s)_(phi_t)_(Normalized_Weight)" % (q2_tag, z_tag))
    return names


RC_LOCAL_START_MARKER = "local-start rule: missing queue entry with an invalid output is started locally"
RC_GATE_MARKER = "campaign local resource gate"
RC_BUILD_RELATIVE = "Run_Large_Files_For_Iterative_Corrections/Comparison_With_Unfolding/Build_EvGen_PerFile_Hists.py"
SHELF_RC_BUILD = "/w/hallb-scshelf2102/clas12/richcap/Radiative_MC/SIDIS_RC_EvGen_richcap/Running_EvGen_richcap/" + RC_BUILD_RELATIVE


def rc_build_script():
    return os.path.join(evgen_dir(), RC_BUILD_RELATIVE)


def rc_fix_is_deployed():
    path = rc_build_script()
    text = ""
    if(os.path.isfile(path)):
        handle = open(path)
        text = handle.read()
        handle.close()
    if((RC_LOCAL_START_MARKER not in text) or (RC_GATE_MARKER not in text)):
        print("RC was not started. The local-start fix and the resource gate are not both in %s" % path)
        print("Updating the ceph analysis checkout does not update the shelf EvGen file.")
        print("Copy the edited Build_EvGen_PerFile_Hists.py to %s" % SHELF_RC_BUILD)
        return False
    return True


def rc_evgen_names():
    names = []
    for factor_name in rc_factor_names():
        names.append(factor_name.replace("(RC_Factor)", "(EvGen_Rad)", 1))
        names.append(factor_name.replace("(RC_Factor)", "(EvGenNRad)", 1))
    return names


def root_has_th1_names(path, names):
    if(not root_is_usable(path, need_h22=False)):
        return False
    try:
        import ROOT
    except Exception:
        return False
    root_file = None
    try:
        root_file = ROOT.TFile.Open(str(path), "READ")
        if((root_file is None) or root_file.IsZombie()):
            return False
        classes = {}
        for key in root_file.GetListOfKeys():
            classes[str(key.GetName())] = str(key.GetClassName())
        for name in names:
            if(not classes.get(name, "").startswith("TH1")):
                return False
        return True
    except Exception:
        return False
    finally:
        if(root_file is not None):
            try:
                root_file.Close()
            except Exception:
                pass


def rc_evgen_merged_complete(path):
    return root_has_th1_names(path, rc_evgen_names())


def rc_factors_complete(path):
    if(not root_is_usable(path, need_h22=False)):
        return False
    try:
        import ROOT
    except Exception:
        return False
    root_file = None
    try:
        root_file = ROOT.TFile.Open(str(path), "READ")
        if(root_file is None):
            return False
        if(root_file.IsZombie()):
            return False
        classes = {}
        for key in root_file.GetListOfKeys():
            classes[str(key.GetName())] = str(key.GetClassName())
        for name in rc_factor_names():
            if(not classes.get(name, "").startswith("TH1")):
                return False
        return True
    except Exception:
        return False
    finally:
        if(root_file is not None):
            try:
                root_file.Close()
            except Exception:
                pass


def rc_compare_argv(compare, rc_out):
    # -r is the unfolding file. -usf reads histograms already stored in the factor working file.
    return [compare, "-usf", "-sfn", rc_out, "-ssf", "-rc", "-Nw", "-evgen"]


def rho_fit_argv(fit, data_root, token, merged):
    # Get_rho_Normalization_values.py accepts neither -e nor -em.
    return [fit, "-droot", data_root, "-st", token, "-usf", "-f1", merged]


def finish_phase(args, phase, next_phase):
    if(args.dry_run):
        return
    record_phase(input_folder(args.data_root, False), phase, "success")
    mail_note("SIDIS phase %s finished" % phase, "phase %s finished.\nnext phase: %s\n" % (phase, next_phase if(next_phase) else "none"))


def rc_build_outputs_ready(task_list, merged):
    if(not os.path.isfile(task_list)):
        return False
    if(not root_is_usable(merged, need_h22=False)):
        return False
    saw_worker = False
    handle = open(task_list)
    for line in handle:
        line = line.strip()
        if((line == "") or line.startswith("#")):
            continue
        parts = line.split("\t")
        saw_worker = True
        if((len(parts) < 4) or (not root_is_usable(parts[3], need_h22=False))):
            handle.close()
            return False
    handle.close()
    return saw_worker


def expand_patterns(patterns):
    found = []
    seen = set()
    for pattern in patterns:
        for path in sorted(glob.glob(pattern)):
            full = os.path.abspath(path)
            if(full not in seen):
                seen.add(full)
                found.append(full)
    return found


def inputs_sha256(paths):
    return hashlib.sha256("\n".join(paths).encode("utf-8")).hexdigest()


def read_manifest_patterns(path):
    patterns = []
    handle = open(path)
    for line in handle:
        stripped = line.strip()
        if((stripped == "") or stripped.startswith("#")):
            continue
        patterns.append(stripped)
    handle.close()
    return patterns


def parse_groovy_sbatch(path):
    # Groovy's sbatch script is the submission record: job name, array, and manifest.
    job_name = ""
    array_spec = ""
    manifest = ""
    handle = open(path)
    for line in handle:
        if(line.startswith("#SBATCH --job-name=")):
            job_name = line.split("=", 1)[1].strip()
        elif(line.startswith("#SBATCH --array=")):
            array_spec = line.split("=", 1)[1].strip()
        elif(line.startswith('MANIFEST="')):
            manifest = line.split('"', 2)[1]
    handle.close()
    return job_name, array_spec, manifest


def receipt_path(folder):
    return os.path.join(folder, "groovy_workload_records.json")


def load_receipts(folder):
    path = receipt_path(folder)
    if(not os.path.isfile(path)):
        return []
    handle = open(path)
    payload = json.load(handle)
    handle.close()
    return list(payload.get("records", []))


def save_receipt(folder, record):
    records = []
    for old in load_receipts(folder):
        same = (old.get("inputs_sha256") == record["inputs_sha256"]) and (old.get("source") == record["source"]) and (old.get("mc") == record["mc"])
        if(not same):
            records.append(old)
    records.append(record)
    handle = open(receipt_path(folder), "w")
    json.dump({"records": records}, handle, indent=2)
    handle.write("\n")
    handle.close()


def sacct_tasks(job_name="", job_id=""):
    # None means sacct could not be read. An empty dict means it answered and found nothing.
    cmd = ["sacct", "-n", "--parsable2", "--format=JobID,State,ExitCode"]
    if(job_id not in ["", None]):
        cmd.extend(["-j", str(job_id)])
    elif(job_name not in ["", None]):
        cmd.extend(["--name", str(job_name)])
    else:
        return None
    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except FileNotFoundError:
        return None
    if(proc.returncode != 0):
        print("sacct failed: %s" % proc.stderr.strip())
        return None
    arrays = {}
    for line in proc.stdout.splitlines():
        parts = line.split("|")
        if(len(parts) < 3):
            continue
        job = parts[0].strip()
        if(("." in job) or ("_" not in job)):
            continue
        array_id, index_text = job.split("_", 1)
        if(not index_text.isdigit()):
            continue
        state = parts[1].strip().split()[0]
        exit_code = parts[2].strip()
        arrays.setdefault(array_id, {})[int(index_text)] = (state, exit_code)
    return arrays


def array_outcome(tasks, nfiles):
    if(nfiles < 1):
        return "incomplete"
    active = set(["PENDING", "RUNNING", "CONFIGURING", "COMPLETING", "SUSPENDED", "REQUEUED", "RESIZING"])
    saw_active = False
    for index in range(nfiles):
        if(index not in tasks):
            return "active" if(saw_active) else "incomplete"
        state, exit_code = tasks[index]
        if(state in active):
            saw_active = True
            continue
        if((state != "COMPLETED") or (not str(exit_code).startswith("0:"))):
            return "incomplete"
    if(saw_active):
        return "active"
    return "complete"


def matching_arrays(job_name, job_id, nfiles):
    if(job_id not in ["", None]):
        arrays = sacct_tasks(job_id=job_id)
    else:
        arrays = sacct_tasks(job_name=job_name)
    if(arrays is None):
        return None
    found = []
    for array_id, tasks in arrays.items():
        if((job_id not in ["", None]) and (str(array_id) != str(job_id))):
            continue
        found.append((array_id, array_outcome(tasks, nfiles)))
    return found


def groovy_sbatch_path(groovy_dir, source, mc_type):
    return os.path.join(groovy_dir, "GroovyArray_%s_%s_epipX.sh" % (source, mc_type))


def completed_groovy_job(groovy_dir, folder, source, mc_type, paths, dry_run):
    # Finished means the recorded manifest is this input set and every sacct task exited 0.
    digest = inputs_sha256(paths)
    nfiles = len(paths)
    if(nfiles < 1):
        print("groovy %s %s: input set is empty; completion cannot be established" % (source, mc_type))
        return "submit", "", ""
    candidates = []
    script = groovy_sbatch_path(groovy_dir, source, mc_type)
    if(os.path.isfile(script)):
        job_name, array_spec, manifest = parse_groovy_sbatch(script)
        expected_spec = "0-%d" % (nfiles - 1)
        manifest_paths = expand_patterns(read_manifest_patterns(manifest)) if((manifest != "") and os.path.isfile(manifest)) else []
        if((job_name != "") and (array_spec == expected_spec) and (manifest_paths == paths)):
            candidates.append((job_name, ""))
        else:
            print("groovy %s %s: on-disk %s does not match the current input set" % (source, mc_type, os.path.basename(script)))
    for record in load_receipts(folder):
        if((record.get("source") == source) and (record.get("mc") == mc_type) and (record.get("inputs_sha256") == digest)):
            candidates.append((record.get("job_name", ""), record.get("job_id", "")))
    if(len(candidates) == 0):
        print("groovy %s %s: no submission record matches this input set; submit" % (source, mc_type))
        return "submit", "", ""
    unknown = False
    active_id = ""
    active_name = ""
    for job_name, job_id in candidates:
        found = matching_arrays(job_name, job_id, nfiles)
        if(found is None):
            unknown = True
            continue
        for array_id, outcome in found:
            if(outcome == "complete"):
                if(not dry_run):
                    save_receipt(folder, {"source": source, "mc": mc_type, "event": "epipX", "inputs_sha256": digest, "nfiles": nfiles, "job_id": array_id, "job_name": job_name})
                print("groovy %s %s: reuse array %s (%d tasks COMPLETED, exit 0, inputs match)" % (source, mc_type, array_id, nfiles))
                return "reuse", array_id, job_name
            if((outcome == "active") and (active_id == "")):
                active_id = array_id
                active_name = job_name
    if(active_id != ""):
        print("groovy %s %s: array %s is still running for this input set; watch, do not submit again" % (source, mc_type, active_id))
        return "watch", active_id, active_name
    if(unknown):
        print("groovy %s %s: completion cannot be established because sacct could not be read; submit" % (source, mc_type))
    else:
        print("groovy %s %s: no successful array matches this input set; submit" % (source, mc_type))
    return "submit", "", ""


def watch_groovy_array(source, mc_type, array_id, nfiles, folder, digest, job_name, dry_run):
    print("groovy %s %s: watching array %s" % (source, mc_type, array_id))
    if(dry_run):
        return 0
    while(True):
        found = matching_arrays("", array_id, nfiles)
        if(found is None):
            mail_stop("groovy_%s_%s" % (source, mc_type), "sacct could not be read while watching %s" % array_id)
            return 1
        outcome = "incomplete"
        for found_id, found_outcome in found:
            if(found_id == str(array_id)):
                outcome = found_outcome
        if(outcome == "complete"):
            save_receipt(folder, {"source": source, "mc": mc_type, "event": "epipX", "inputs_sha256": digest, "nfiles": nfiles, "job_id": str(array_id), "job_name": job_name})
            return 0
        if(outcome == "active"):
            time.sleep(60)
            continue
        mail_stop("groovy_%s_%s" % (source, mc_type), "array %s did not finish successfully" % array_id)
        return 1


def run_groovy_processes(pending, folder, identities):
    # Start every outstanding Groovy workload, then wait. One failure does not cancel the others.
    running = []
    for stage, argv, cwd in pending:
        print("")
        print("stage %s" % stage)
        show_command(argv)
        proc = subprocess.Popen([str(part) for part in argv], cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        running.append({"stage": stage, "proc": proc, "lines": []})

    def read_output(item):
        for line in item["proc"].stdout:
            print("[%s] %s" % (item["stage"], line), end="")
            item["lines"].append(line)

    threads = []
    for item in running:
        thread = threading.Thread(target=read_output, args=(item,))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    failed = 0
    for item in running:
        code = item["proc"].wait()
        print("stage %s exit %s" % (item["stage"], code))
        if(code != 0):
            failed = code
            mail_stop(item["stage"], "exit %s" % code)
            continue
        job_id = ""
        for line in item["lines"]:
            if("Submitted SLURM array job id:" in line):
                job_id = line.split(":")[-1].strip()
        identity = identities.get(item["stage"])
        if((identity is not None) and (job_id != "")):
            save_receipt(folder, {"source": identity["source"], "mc": identity["mc"], "event": "epipX", "inputs_sha256": identity["digest"], "nfiles": identity["nfiles"], "job_id": job_id, "job_name": identity.get("job_name", "")})
    return failed


def run_early(args):
    config = load_ifarm_inputs()
    token = rho_source_token(config) or "rho0_new"
    rho_glob = config.get("rho_hipo_glob", "")
    clasdis_glob = config.get("clasdis_55na_hipo_glob", "")
    rho_count = len(glob.glob(rho_glob)) if(rho_glob) else 0
    clasdis_count = len(glob.glob(clasdis_glob)) if(clasdis_glob) else 0
    print("phase groovy: rho0 matches %d" % rho_count)
    print("phase groovy: 55nA clasdis matches %d" % clasdis_count)
    if((not args.dry_run) and ((rho_count < 1) or (clasdis_count < 1))):
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
    merged = response_merged_path(args.data_root, "rho0", token, getattr(args, "matching_criteria", "Bank"))
    rho_paths = expand_patterns([rho_glob])
    clasdis_paths = expand_patterns([clasdis_glob])
    groovy_jobs = [
        ("groovy_rho_gdf", "rho0", "gdf", rho_list, rho_paths, phase_message(args, "groovy rho0 generated")),
        ("groovy_rho_mdf", "rho0", "mdf", rho_list, rho_paths, phase_message(args, "groovy rho0 reconstructed")),
        ("groovy_55na_gdf", "clasdis", "gdf", clasdis_list, clasdis_paths, phase_message(args, "groovy 55 nA clasdis generated")),
        ("groovy_55na_mdf", "clasdis", "mdf", clasdis_list, clasdis_paths, phase_message(args, "groovy 55 nA clasdis reconstructed")),
    ]
    pending = []
    identities = {}
    watches = []
    for stage, source, mc_type, paths_txt, paths, message in groovy_jobs:
        done_roots, missing_hipos = split_groovy_outputs(paths, source, mc_type)
        print("phase groovy %s %s: usable %d missing %d" % (source, mc_type, len(done_roots), len(missing_hipos)))
        if(len(missing_hipos) == 0):
            print("phase groovy %s %s done" % (source, mc_type))
            continue
        action, array_id, job_name = completed_groovy_job(groovy_dir, folder, source, mc_type, missing_hipos, args.dry_run)
        if(action == "watch"):
            watches.append((source, mc_type, array_id, len(missing_hipos), inputs_sha256(missing_hipos), job_name, paths))
            continue
        listed = write_path_list(folder, "groovy_missing_%s_%s.txt" % (source, mc_type), missing_hipos)
        argv = groovy_command(groovy, source, mc_type, listed, message)
        identities[stage] = {"source": source, "mc": mc_type, "digest": inputs_sha256(missing_hipos), "nfiles": len(missing_hipos), "job_name": job_name}
        if(args.dry_run):
            print("")
            print("phase %s submit %d" % (stage, len(missing_hipos)))
            show_command(argv)
        else:
            pending.append((stage, argv, groovy_dir))
    if(len(pending) > 0):
        code = run_groovy_processes(pending, folder, identities)
        if(code != 0):
            return code
    for source, mc_type, array_id, nfiles, digest, job_name, all_paths in watches:
        code = watch_groovy_array(source, mc_type, array_id, nfiles, folder, digest, job_name, args.dry_run)
        if(code != 0):
            return code
        done_roots, missing_hipos = split_groovy_outputs(all_paths, source, mc_type)
        if(len(missing_hipos) == 0):
            continue
        listed = write_path_list(folder, "groovy_missing_%s_%s.txt" % (source, mc_type), missing_hipos)
        message = phase_message(args, "groovy %s %s" % (source, mc_type))
        argv = groovy_command(groovy, source, mc_type, listed, message)
        if(args.dry_run):
            print("phase groovy %s %s still missing %d" % (source, mc_type, len(missing_hipos)))
            show_command(argv)
        else:
            code = run_command("groovy_%s_%s" % (source, mc_type), argv, groovy_dir, False, "dataframe")
            if(code != 0):
                return code
    if(not args.dry_run):
        record_phase(folder, "groovy", "success")
        mail_note("SIDIS phase groovy finished", "phase groovy finished.\nnext phase: dataframe\n")
    note = phase_message(args, "dataframe")
    dataframe_steps = []
    frames_ready = dataframes_are_ready(args.data_root, rho_paths, clasdis_paths)
    for group, source, mc_type, hipos in [("rho_gdf", "rho0", "gdf", rho_paths), ("rho_mdf", "rho0", "mdf", rho_paths), ("55na_gdf", "clasdis", "gdf", clasdis_paths), ("55na_mdf", "clasdis", "mdf", clasdis_paths)]:
        done_roots, missing_hipos = split_groovy_outputs(hipos, source, mc_type)
        if((len(missing_hipos) > 0) and (not args.dry_run)):
            mail_stop("dataframe", "groovy %s %s still missing %d outputs" % (source, mc_type, len(missing_hipos)))
            return 1
        need = []
        for groovy_path in done_roots:
            frame = dataframe_output_path(groovy_path, mc_type, args.data_root)
            if((frame == "") or (not root_is_usable(frame))):
                need.append(groovy_path)
        print("phase dataframe %s: missing %d of %d" % (group, len(need), len(done_roots)))
        if(len(need) == 0):
            print("phase dataframe %s done" % group)
            continue
        listed = write_path_list(folder, "dataframe_missing_%s.txt" % group, need)
        dataframe_steps.append(("dataframe_%s" % group, [helper, "-droot", args.data_root, "-o", "work", "-il", listed, "-dtype", mc_type, "-m", "hybrid", "-j", "10", "-y", "-e", "-em", note], frames))
    batch_file = os.path.join(data_root_path(args.data_root), REL_FILE_BATCHES)
    review_file = os.path.join(frames, "exclusive_rho_review_%s.txt" % token)
    if(frames_ready and text_is_present(batch_file)):
        print("phase make_batches done")
        batch_steps = []
    else:
        batch_steps = [
            ("make_batches", [batches, "-droot", args.data_root, "-m", "make_batches", "-rst", token, "-e", "-em", phase_message(args, "make_batches")], frames),
        ]
    phases = [
        ("dataframe", dataframe_steps, "make_batches"),
        ("make_batches", batch_steps, "rho_hist"),
        ("rho_hist", [] if(root_is_usable(merged)) else [
            ("rho_hist", [submit, "-droot", args.data_root, "-m", "hybrid", "-rho", "-jrho0", "10", "-n", token, "-mac", campaign_matching_value(getattr(args, "matching_criteria", None)), "-e", "-em", phase_message(args, "rho_hist")], frames),
        ], "rho_fit"),
        ("rho_fit", [] if(text_is_present(review_file)) else [
            # ("rho_fit", [fit, "-droot", args.data_root, "-st", token, "-usf", "-f1", merged, "-e", "-em", phase_message(args, "rho_fit")], frames),
            ("rho_fit", rho_fit_argv(fit, args.data_root, token, merged), frames),
        ], ""),
    ]
    if(root_is_usable(merged)):
        print("phase rho_hist done")
    if(text_is_present(review_file)):
        print("phase rho_fit done")
    for phase, steps, next_phase in phases:
        for stage, argv, cwd in steps:
            code = run_command(stage, argv, cwd, args.dry_run, next_phase, mail_success=False)
            if(code != 0):
                return code
        if(phase == "dataframe"):
            ready = dataframes_are_ready(args.data_root, rho_paths, clasdis_paths)
            detail = "dataframe outputs are still missing"
        elif(phase == "make_batches"):
            ready = text_is_present(batch_file)
            detail = "File_Batches.py is missing"
        elif(phase == "rho_hist"):
            ready = root_is_usable(merged)
            detail = "merged rho histogram is missing"
        elif(phase == "rho_fit"):
            ready = text_is_present(review_file)
            detail = "exclusive_rho_review_%s.txt is missing" % token
        else:
            ready = True
            detail = ""
        if((not args.dry_run) and (not ready)):
            mail_stop(phase, detail)
            return 1
        finish_phase(args, phase, next_phase)
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
    if((not args.dry_run) and (not root_module_ready())):
        mail_stop("rc_compare", "ROOT is not importable; RC outputs were not changed")
        return 1
    compare_dir = os.path.join(evgen_dir(), "Run_Large_Files_For_Iterative_Corrections", "Comparison_With_Unfolding")
    build = os.path.join(compare_dir, "Build_EvGen_PerFile_Hists.py")
    compare = os.path.join(compare_dir, "Comparison_Between_GEN_and_Unfold.py")
    merged = os.path.join(RC_RUNTIME, "merged_outputs", "Merged_EvGen_PerFile_Hists.root")
    rc_out = os.path.join(RC_RUNTIME, "merged_outputs", "RC_Factors_ifarm_rc.root")
    paired = matched_evgen(args.dry_run)
    task_list = os.path.join(RC_RUNTIME, "evgen_perfile_task_list.txt")
    if(not rc_fix_is_deployed()):
        return 1
    if(rc_evgen_merged_complete(merged) or rc_build_outputs_ready(task_list, merged)):
        print("phase rc_build done")
        finish_phase(args, "rc_build", "rc_compare")
    else:
        argv = [build, "-m", "hybrid", "-y", "-p", "-mpj", "10", "-e", "-em", phase_message(args, "rc_build"), "-rdir", RC_RUNTIME]
        if(paired is not None):
            argv.extend(["-rrad"] + list(paired["rad"]))
            argv.extend(["-rnrad"] + list(paired["nrad"]))
        else:
            print("RC file list is added when the binned directory is visible")
        code = run_command("rc_build", argv, compare_dir, args.dry_run, "rc_compare", mail_success=False)
        if(code != 0):
            return code
        if(args.dry_run):
            print("phase rc_compare waits until rc_build outputs are complete")
            print("")
            print("phase rc_compare")
            show_command(rc_compare_argv(compare, rc_out))
            return 0
        if(not rc_build_outputs_ready(task_list, merged)):
            mail_stop("rc_build", "build exited 0 but workers or the merged file are incomplete")
            return 1
        finish_phase(args, "rc_build", "rc_compare")
    if(rc_factors_complete(rc_out)):
        print("phase rc_compare done")
        finish_phase(args, "rc_compare", "")
        return 0
    if(root_is_usable(merged, need_h22=False)):
        if(root_is_usable(rc_out, need_h22=False)):
            print("RC factor file opens but the weighted factor set is incomplete; leaving the working copy")
        else:
            print("copying merged EvGen histograms to the RC factor working file: %s" % rc_out)
            if(not args.dry_run):
                os.makedirs(os.path.dirname(rc_out), exist_ok=True)
                shutil.copy2(merged, rc_out)
    elif(args.dry_run):
        print("merged EvGen file is not visible; the compare command is still printed")
    else:
        mail_stop("rc_compare", "merged EvGen file is not usable")
        return 1
    code = run_command("rc_compare", rc_compare_argv(compare, rc_out), compare_dir, args.dry_run, "", mail_success=False)
    if(code != 0):
        return code
    if(args.dry_run):
        return 0
    if(not rc_factors_complete(rc_out)):
        mail_stop("rc_compare", "comparison exited 0 but the weighted RC factor set is incomplete")
        return 1
    finish_phase(args, "rc_compare", "")
    return 0


def run_bc_config(args, label, counts):
    hist_phase, hadd_phase, factor_phase = bc_phase_names(label)
    bc_dir = os.path.join(_BOOT, "BC_Corrections")
    runner = os.path.join(bc_dir, "Run_BC_Scripts_Locally.py")
    factor = os.path.join(bc_dir, "BC_Corrections_Script.py")
    tag = bc_run_tag(label, getattr(args, "run_tag", None))
    per_file = bc_worker_command(label, counts)
    bc_inputs = expand_patterns(BC_NO_RAD_PATTERNS)
    if(args.dry_run):
        print("BC inventory %s directory %s" % (hist_phase, bc_run_directory(tag)))
        for bc_input in bc_inputs:
            expected = os.path.join(bc_run_directory(tag), bc_output_name(bc_input))
            found = bc_output_path(bc_input, label, counts, tag)
            if(found is None):
                print("unread %s" % expected)
            elif(found == ""):
                print("missing %s" % expected)
            else:
                print("complete %s" % found)
        return 0
    done_inputs = []
    missing_inputs = []
    for bc_input in bc_inputs:
        found = bc_output_path(bc_input, label, counts, tag)
        if(found is None):
            mail_stop(hist_phase, "could not inspect an existing BC output; nothing was removed")
            return 1
        if(found != ""):
            done_inputs.append(bc_input)
        else:
            missing_inputs.append(bc_input)
    print("phase %s: usable %d missing %d" % (hist_phase, len(done_inputs), len(missing_inputs)))
    if(len(bc_inputs) == 0):
        if(args.dry_run):
            print("No_Rad input glob matched nothing")
            return 0
        mail_stop(hist_phase, "No_Rad input glob matched nothing")
        return 1
    if(len(missing_inputs) > 0):
        for bc_input in missing_inputs:
            if(not remove_incomplete_bc_outputs(bc_input, label, counts, args.dry_run, tag)):
                mail_stop(hist_phase, "could not inspect an existing BC output; it was left in place")
                return 1
        argv = [runner, "-d", BC_NO_RAD_BRACE, "-rm", "hybrid", "-j", "10", "-y", "-e", "-rcl", phase_message(args, hist_phase), "-rt", tag, "-c", per_file]
        if(len(done_inputs) > 0):
            argv.extend(["-ex", ",".join([os.path.basename(path) for path in done_inputs])])
        code = run_command(hist_phase, argv, bc_dir, args.dry_run, hadd_phase, mail_success=False)
        if(code != 0):
            return code
        if(args.dry_run):
            print("phase %s waits until %d of %d per-file outputs are complete" % (hadd_phase, len(done_inputs), len(bc_inputs)))
            return 0
        done_inputs = []
        missing_inputs = []
        for bc_input in bc_inputs:
            found = bc_output_path(bc_input, label, counts, tag)
            if(found is None):
                mail_stop(hadd_phase, "could not inspect a BC output after the helper exited")
                return 1
            if(found != ""):
                done_inputs.append(bc_input)
            else:
                missing_inputs.append(bc_input)
        if(len(missing_inputs) > 0):
            mail_stop(hadd_phase, "per-file outputs %d of %d; hadd was not run" % (len(done_inputs), len(bc_inputs)))
            return 1
    else:
        print("phase %s done" % hist_phase)
    finish_phase(args, hist_phase, hadd_phase)
    outputs = bc_complete_outputs(bc_inputs, label, counts, tag)
    if(outputs is None):
        mail_stop(hadd_phase, "could not inspect a BC output; hadd was not run")
        return 1
    if(len(outputs) != len(bc_inputs)):
        mail_stop(hadd_phase, "per-file outputs %d of %d; hadd was not run" % (len(outputs), len(bc_inputs)))
        return 1
    dest = bc_merged_path(tag)
    json_path = bc_json_path(tag)
    merged_status = bc_histogram_status(dest, counts)
    if(merged_status == "unread"):
        mail_stop(hadd_phase, "could not inspect the merged BC file; it was left in place")
        return 1
    if(merged_status == "complete"):
        print("phase %s done" % hadd_phase)
    else:
        if(merged_status == "incomplete"):
            print("removing incomplete BC merge so it is recreated: %s" % dest)
            if(not args.dry_run):
                os.remove(dest)
        # filtered = []
        # for path in outputs:
        #     filtered.append(path + ".hadd_input.root")
        # bc_filtered_copy kept only bc_expected_bins and dropped every other histogram.
        hadd_argv = bc_hadd_argv(dest, list(outputs))
        if(len(hadd_argv) == 0):
            mail_stop(hadd_phase, "ROOTSYS is unset or $ROOTSYS/bin/hadd is not a file")
            return 1
        code = run_command(hadd_phase, hadd_argv, bc_dir, args.dry_run, factor_phase, mail_success=False)
        if(code != 0):
            return code
        if(args.dry_run):
            print("phase %s waits until the merged file is complete" % factor_phase)
            return 0
        if(not bc_histograms_match(dest, counts)):
            mail_stop(hadd_phase, "hadd exited 0 but the merged histogram set is incomplete")
            return 1
    finish_phase(args, hadd_phase, factor_phase)
    if(bc_json_complete(json_path, counts)):
        print("phase %s done" % factor_phase)
        finish_phase(args, factor_phase, "")
        return 0
    argv = bc_factor_argv(factor, json_path, dest, counts, phase_message(args, factor_phase), label == "")
    code = run_command(factor_phase, argv, bc_dir, args.dry_run, "", mail_success=False)
    if(code != 0):
        return code
    if(args.dry_run):
        return 0
    if(not bc_json_complete(json_path, counts)):
        mail_stop(factor_phase, "factor script exited 0 but the JSON does not match this configuration")
        return 1
    finish_phase(args, factor_phase, "")
    return 0


def run_bc(args):
    if((not args.dry_run) and (not root_module_ready())):
        mail_stop("bc_hist", "ROOT is not importable; BC outputs were not changed")
        return 1
    choice = getattr(args, "systematics", "nominal")
    for config in bc_configurations(choice):
        code = run_bc_config(args, config["label"], config["counts"])
        if(code != 0):
            return code
    return 0


def review_n_rho(path):
    if(not text_is_present(path)):
        return None
    handle = open(path)
    value = None
    for line in handle:
        text = line.strip()
        if(text.startswith("n_rho_ave")):
            continue
        if(text.startswith("n_rho ")):
            try:
                value = float(text.split()[1])
            except (IndexError, ValueError):
                value = None
            break
    handle.close()
    return value


def rho_weight_status(data_root):
    # rho0_new histograms load Campaign/rho_factors.json. A review file is a fit record and is not required.
    # The factor lives in the checkout. data_root stays in the signature for the existing caller.
    json_path = os.path.join(_BOOT, "Campaign", "rho_factors.json")
    from Campaign.ifarm_inputs import registered_rho0_new_norm
    try:
        stored = registered_rho0_new_norm(json_path)
    except SystemExit as exc:
        print(exc)
        print("weighted products are blocked. Campaign/rho_factors.json was not changed.")
        return "blocked"
    print("rho0_new n_rho %s from %s" % (stored, json_path))
    return "match"


def local_jobs_per_mode(max_local, n_modes):
    # Kept so older callers still import. Histogram launches use histogram_ceilings instead of an even split.
    if(max_local in [None, 0]):
        return 10
    share = max(1, int(max_local) // int(n_modes))
    return min(10, share)


# Same suffixes as Submit_Full MATCHING_OUTPUT_TAG. Historical _gen adds nothing.
MATCH_OUTPUT_TAG = {
    "": "", "_gen": "", "gen": "", "P10T6": "",
    "Bank": "Bank", "_gen_Bank": "Bank",
    "P12T6": "P12T6", "_gen_P12T6": "P12T6",
    "P8T6": "P8T6", "_gen_P8T6": "P8T6",
    "P10T8": "P10T8", "_gen_P10T8": "P10T8",
    "P10T4": "P10T4", "_gen_P10T4": "P10T4",
}
# Same name_fmt strings as Submit_Full PRODUCTS / RHO0_PRODUCT. Default cut adds no suffix.
PRODUCT_STEM = {
    "2D_Presentation": "2D_Presentation_%s_Q2_Y_Bins",
    "Only_3D": "Only_3D_%s_Response_Matrices",
    "Only_5D": "Only_5D_%s_Response_Matrices",
    "Only_1D": "Only_1D_%s_Kinematics",
    "Diagnostic_1D": "Diagnostic_1D_%s",
    "rho0": "Only_2D_rho0_Normalization_Creation_%s",
}
NOMINAL_HPP_TAG = "Final_Thesis"
WORKFLOW_NAME = "SIDIS_Workflow"


def campaign_matching_value(matching):
    if(matching in [None]):
        return "Bank"
    if(matching == ""):
        return "_gen"
    return str(matching)


def campaign_hpp_tag(hpp_tag):
    if(hpp_tag in [None, ""]):
        return NOMINAL_HPP_TAG
    return str(hpp_tag)


def match_output_tag(matching):
    key = campaign_matching_value(matching)
    if(key not in MATCH_OUTPUT_TAG):
        raise ValueError("Unknown matching_criteria=%r" % (matching,))
    return MATCH_OUTPUT_TAG[key]


def response_merged_path(data_root, product_key, workflow_name, matching):
    # Pipeline merge name: SIDIS_epip_Response_Matrices_from_RDataFrames_{-n}_{name_in_label}_All.root
    # name_in_label of the first Submit_Full glob *Final_Thesis_Files*.root is Final_Thesis_Files.
    tag = match_output_tag(matching)
    shared = str(workflow_name) if(tag in ["", None]) else "%s_%s" % (workflow_name, tag)
    stem = PRODUCT_STEM[product_key] % shared
    name = "SIDIS_epip_Response_Matrices_from_RDataFrames_%s_Final_Thesis_Files_All.root" % stem
    return os.path.join(data_root_path(data_root), REL_HADD, name)


def histogram_response_path(args, product_key):
    matching = getattr(args, "matching_criteria", None)
    return response_merged_path(args.data_root, product_key, WORKFLOW_NAME, matching)


def response_file_ready(path, required_piece):
    if(not root_is_usable(path, need_h22=False)):
        return False
    try:
        import ROOT
    except Exception:
        return False
    root_file = None
    try:
        root_file = ROOT.TFile.Open(str(path), "READ")
        if((root_file is None) or root_file.IsZombie()):
            return False
        for key in root_file.GetListOfKeys():
            if(required_piece in str(key.GetName())):
                return True
        return False
    except Exception:
        return False
    finally:
        if(root_file is not None):
            try:
                root_file.Close()
            except Exception:
                pass


def hpp_has_marker(path, marker):
    if((not os.path.isfile(path)) or (os.path.getsize(path) <= 0)):
        return False
    handle = open(path, errors="ignore")
    chunk = handle.read(400000)
    handle.close()
    return marker in chunk


def hpp_pair_for_tag(data_root, tag):
    # Same names as Submit_Full hpp_paths_from_tag. .root twins are not inputs.
    from jlab_work_paths import pipeline_output_path, REL_HPP_OUT, resolve_pipeline_input
    folder = pipeline_output_path(REL_HPP_OUT, data_root)
    pure = os.path.join(folder, "generated_acceptance_weights_%s_noSpline.hpp" % tag)
    spline = os.path.join(folder, "generated_acceptance_weights_%s_withSpline.hpp" % tag)
    pure = resolve_pipeline_input(pure, data_root)
    spline = resolve_pipeline_input(spline, data_root)
    return pure, spline


def hpp_pair_ready(data_root, tag):
    pure, spline = hpp_pair_for_tag(data_root, tag)
    problems = []
    if(not hpp_has_marker(pure, "accw_")):
        problems.append("no-spline HPP missing or without accw_: %s" % pure)
    if(not hpp_has_marker(spline, "accw_sw_")):
        problems.append("with-spline HPP missing or without accw_sw_: %s" % spline)
    if(len(problems) > 0):
        print("acceptance reuse -sa -hon %s data_root %s" % (tag, data_root))
        for line in problems:
            print(line)
        return False
    print("acceptance reuse -sa -hon %s" % tag)
    print("no-spline %s" % pure)
    print("with-spline %s" % spline)
    return True


def regenerated_hpp_paths(data_root):
    from jlab_work_paths import pipeline_output_path, REL_HPP_OUT
    folder = pipeline_output_path(REL_HPP_OUT, data_root)
    pure = os.path.join(folder, "generated_acceptance_weights_SIDIS_Workflow_noSpline.hpp")
    spline = os.path.join(folder, "generated_acceptance_weights_SIDIS_Workflow_withSpline.hpp")
    return pure, spline


def hpp_was_rewritten(path, previous_mtime, started):
    if(not hpp_has_marker(path, "accw_")):
        return False
    try:
        current = os.path.getmtime(path)
    except OSError:
        return False
    if(previous_mtime is None):
        return current + 1.0 >= started
    return (current > previous_mtime) and (current + 1.0 >= started)


def acceptance_commands(data_root, matching=None):
    script = os.path.join(_BOOT, "Histo_Files_ROOT", "DataFrames", "Acceptance_Weights_Creations_using_RDataFrames.py")
    pure, spline = regenerated_hpp_paths(data_root)
    # spline_file = "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Prepare_Next_Iteration/rho0_Subtracted_5D_V2_4D_xB_Fit_Pars_from_5D_BC_RC_Bayesian_Compute_SplineWeight.txt"  # 2026-10-26 previous nominal 5D MC weight; raw-A 3D is the event-weight default
    spline_file = "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Prepare_Next_Iteration/acc020_3D_BC_RC_rawA_4D_xB_Fit_Pars_from_3D_BC_RC_Bayesian_Compute_SplineWeight.txt"
    # shared = [script, "--data_root", data_root, "--make_2D_weight", "--name", "SIDIS_Workflow", "-cnR", "cut_Complete_SIDIS", "-cnM", "cut_Complete_SIDIS", "--run_rho_weight", "--rho0_source", "lundvpk", "--matching_criteria", "_gen"]
    # shared = [script, "--data_root", data_root, "--make_2D_weight", "--name", "SIDIS_Workflow", "-cnR", "cut_Complete_SIDIS", "-cnM", "cut_Complete_SIDIS", "--run_rho_weight", "--rho0_source", "lundvpk", "--matching_criteria", campaign_matching_value(matching)]  # Changed rho0_source to rho0_new on 10/28/2026
    shared = [script, "--data_root", data_root, "--make_2D_weight", "--name", "SIDIS_Workflow", "-cnR", "cut_Complete_SIDIS", "-cnM", "cut_Complete_SIDIS", "--run_rho_weight", "--rho0_source", "rho0_new", "--matching_criteria", campaign_matching_value(matching)]
    pure_cmd = shared + ["--hpp_output_file", pure]
    spline_cmd = shared + ["--hpp_output_file", spline, "--spline_weights", "--spline_file", spline_file]
    return pure_cmd, spline_cmd, pure, spline


def response_override_pairs(args):
    # Temporary 2D/3D/5D overrides. Absent values stay off the command so the pipeline defaults remain.
    pairs = []
    if(getattr(args, "slurm_time", None) not in [None, ""]):
        pairs.append(("-st", str(args.slurm_time)))
    if(getattr(args, "batch_ids", None) not in [None, ""]):
        pairs.append(("-bids", str(args.batch_ids)))
    if(getattr(args, "hybrid_date", None) not in [None, ""]):
        pairs.append(("-hdate", str(args.hybrid_date)))
    return pairs


def response_workflow_name(only_key):
    # histogram_1d, response_1d, and diagnostic_1d write SIDIS_Workflow_V2. histogram_unfold keeps SIDIS_Workflow.
    if(only_key in ["1D", "diag", "both1d"]):
        return "SIDIS_Workflow_V2"
    return WORKFLOW_NAME


def response_argv_has_jobs(argv):
    for flag in ["-j2D", "-j3D", "-j5D", "-j1D", "-jdiag"]:
        if((flag in argv) and (int(argv[argv.index(flag) + 1]) > 0)):
            return True
    return False


def response_submit_argv(args, only_key, slots=None, pass_overrides=False):
    from Campaign.local_resource_gate import clamp_histogram_cap, histogram_ceilings
    ceilings = histogram_ceilings()
    submit = os.path.join(_BOOT, "Histo_Files_ROOT", "DataFrames", "Submit_Full_Histogram_Creation_Pipeline.py")
    workflow = response_workflow_name(only_key)
    argv = [submit, "-droot", args.data_root, "-m", "hybrid", "-y", "-sa", "-n", workflow, "-mac", campaign_matching_value(getattr(args, "matching_criteria", None)), "-j", "0", "-jBin", "0", "-jch4", "0", "-jdph", "0", "-jrho0", "0"]
    hpp_name = campaign_hpp_tag(getattr(args, "hpp_old_name", None))
    argv.extend(["-hon", str(hpp_name)])
    counts = {"2D": 0, "3D": 0, "5D": 0, "1D": 0, "diag": 0}
    allowed = None if(slots is None) else list(slots)
    if((only_key in ["", "2D"]) and ((allowed is None) or ("2D" in allowed))):
        counts["2D"] = ceilings["Only_2D"]
    if((only_key in ["", "3D"]) and ((allowed is None) or ("3D" in allowed))):
        counts["3D"] = ceilings["Only_3D"]
    if((only_key in ["", "5D"]) and ((allowed is None) or ("5D" in allowed))):
        counts["5D"] = ceilings["Only_5D"]
    if((only_key in ["", "1D", "both1d"]) and ((allowed is None) or ("1D" in allowed))):
        counts["1D"] = ceilings["Only_1D"]
    if((only_key in ["", "diag", "both1d"]) and ((allowed is None) or ("diag" in allowed))):
        counts["diag"] = ceilings["Diagnostic_1D"]
    reuse = [("2D", "2D_Presentation", "Q2"), ("3D", "Only_3D", "MultiDim"), ("5D", "Only_5D", "MultiDim"), ("1D", "Only_1D", "phi_response_4d")]
    # Diagnostic reuse looks at the V2 merge only. The unversioned Diagnostic job count is unchanged.
    if(workflow == "SIDIS_Workflow_V2"):
        reuse.append(("diag", "Diagnostic_1D", "match_category"))
    for slot, product_key, piece in reuse:
        if(counts[slot] == 0):
            continue
        merged = response_merged_path(args.data_root, product_key, workflow, getattr(args, "matching_criteria", None))
        if(response_file_ready(merged, piece)):
            print("reusing merged %s" % merged)
            counts[slot] = 0
    argv.extend(["-j2D", str(counts["2D"]), "-j3D", str(counts["3D"]), "-j5D", str(counts["5D"]), "-j1D", str(counts["1D"]), "-jdiag", str(counts["diag"])])
    cap = clamp_histogram_cap(getattr(args, "max_local_jobs", None))
    if(cap not in [None, ""]):
        argv.extend(["-hlc", str(cap)])
    if(pass_overrides):
        for flag, value in response_override_pairs(args):
            argv.extend([flag, value])
    return argv


def response_plan_argvs(args, only_key):
    # One Submit_Full applies one batch list and one output date to every selected product.
    # Recovery overrides stay on 2D, 3D, and 5D. histogram_1d, Diagnostic_1D, and Only_1D do not receive them.
    if(len(response_override_pairs(args)) == 0):
        return [response_submit_argv(args, only_key)]
    if(only_key in ["1D", "diag", "both1d"]):
        return [response_submit_argv(args, only_key)]
    if(only_key in ["2D", "3D", "5D"]):
        argv = response_submit_argv(args, only_key, pass_overrides=True)
        if(response_argv_has_jobs(argv)):
            return [argv]
        return []
    plans = []
    recovery = response_submit_argv(args, "", slots=["2D", "3D", "5D"], pass_overrides=True)
    if(response_argv_has_jobs(recovery)):
        plans.append(recovery)
    rest = response_submit_argv(args, "", slots=["1D", "diag"], pass_overrides=False)
    if(response_argv_has_jobs(rest)):
        plans.append(rest)
    return plans


def run_response(args, only_key):
    if(rho_weight_status(args.data_root) == "blocked"):
        return 1
    hpp_name = campaign_hpp_tag(getattr(args, "hpp_old_name", None))
    if(not hpp_pair_ready(args.data_root, hpp_name)):
        mail_stop("response", "acceptance weights for -hon %s are not usable, so histogram jobs were not started" % hpp_name)
        return 1
    # argv = response_submit_argv(args, only_key)
    # code = run_command("response", argv, os.path.dirname(argv[0]), args.dry_run, "", mail_success=False)
    plans = response_plan_argvs(args, only_key)
    if(len(plans) == 0):
        print("response histograms already usable")
    for argv in plans:
        code = run_command("response", argv, os.path.dirname(argv[0]), args.dry_run, "", mail_success=False)
        if(code != 0):
            return code
    if(args.dry_run):
        return 0
    needed = [("Only_3D", "MultiDim"), ("Only_5D", "MultiDim")]
    if(only_key == "1D"):
        needed = [("Only_1D", "phi_response_4d")]
    elif(only_key == "diag"):
        needed = [("Diagnostic_1D", "match_category")]
    elif(only_key == "both1d"):
        needed = [("Only_1D", "phi_response_4d"), ("Diagnostic_1D", "match_category")]
    elif(only_key == "3D"):
        needed = [("Only_3D", "MultiDim")]
    elif(only_key == "5D"):
        needed = [("Only_5D", "MultiDim")]
    elif(only_key == "2D"):
        needed = [("2D_Presentation", "Q2")]
    workflow = response_workflow_name(only_key)
    for product_key, piece in needed:
        path = response_merged_path(args.data_root, product_key, workflow, getattr(args, "matching_criteria", None))
        if(not response_file_ready(path, piece)):
            mail_stop("response", "aggregated file is missing its histograms: %s" % path)
            return 1
    finish_phase(args, "response", "")
    return 0


def iteration_output_path(data_root, dimension):
    return os.path.join(data_root_path(data_root), "Unfold_Iteration_Config", "iteration_%s_study.root" % dimension.lower())


def unfold_output_path(data_root, dimension):
    return os.path.join(data_root_path(data_root), "Unfold_Iteration_Config", "unfold_%s.root" % dimension.lower())


def root_key_count(path, piece):
    if(not root_is_usable(path, need_h22=False)):
        return 0
    try:
        import ROOT
    except Exception:
        return 0
    root_file = None
    count = 0
    try:
        root_file = ROOT.TFile.Open(str(path), "READ")
        if((root_file is None) or root_file.IsZombie()):
            return 0
        for key in root_file.GetListOfKeys():
            if(piece in str(key.GetName())):
                count += 1
        return count
    except Exception:
        return 0
    finally:
        if(root_file is not None):
            try:
                root_file.Close()
            except Exception:
                pass


def iteration_lookup_ready(dimension, cut, bins):
    from Campaign.run_sidis_campaign import k_for
    try:
        if(dimension == "5D"):
            k_for("5D", cut, None, "current_binning")
            return True
        for q2y in bins:
            k_for("3D", cut, q2y, "current_binning")
        return True
    except SystemExit as exc:
        print(exc)
        return False


def iteration_histograms_ready(path, dimension):
    if(dimension == "5D"):
        return all(root_key_count(path, name) > 0 for name in ["hch2", "herr", "hres", "hrms"])
    pieces = ["Iteration_Study_Chi2", "Iteration_Study_RMSError", "Iteration_Study_MeanResiduals", "Iteration_Study_RMSResiduals"]
    return all(root_key_count(path, piece) > 0 for piece in pieces)


def run_iteration(args, dimension):
    bins = list(range(1, 18))
    out_path = iteration_output_path(args.data_root, dimension)
    if(iteration_histograms_ready(out_path, dimension) and iteration_lookup_ready(dimension, args.acceptance_cut, bins)):
        print("phase iteration_%s done" % dimension.lower())
        return 0
    script = "run_Simple_Unfold.py" if(dimension == "3D") else "run_Dedicated_5D_Unfold.py"
    script = os.path.join(_BOOT, script)
    out_path = iteration_output_path(args.data_root, dimension)
    response = histogram_response_path(args, "Only_3D" if(dimension == "3D") else "Only_5D")
    if((not args.dry_run) and (not response_file_ready(response, "MultiDim"))):
        mail_stop("iteration_%s" % dimension.lower(), "response aggregate is not ready: %s" % response)
        return 1
    argv = [script, "-droot", args.data_root, "--iteration_study", "--parm_min", "1", "--parm_max", "10", "--parm_step", "1", "--Min_Allowed_Acceptance_Cut", str(args.acceptance_cut), "-r", out_path, "-sfin", response]
    if(dimension == "5D"):
        # argv.extend(["--background_source", "lundvpk"])  # 10/25/2026
        # argv.extend(["--background_source", "rho0_new"])  # 10/28/2026: follow campaign -bg
        argv.extend(["--background_source", args.background_source])
    code = run_reserved("iteration_%s" % dimension.lower(), argv, _BOOT, args.dry_run, "iteration_%s" % dimension.lower(), args.data_root)
    if(code != 0):
        return code
    if(args.dry_run):
        return 0
    if(not iteration_histograms_ready(out_path, dimension)):
        mail_stop("iteration_%s" % dimension.lower(), "iteration histograms are incomplete: %s" % out_path)
        return 1
    bins = list(range(1, 18))
    if(not iteration_lookup_ready(dimension, args.acceptance_cut, bins)):
        print("iteration histograms are present, but bayesian_iteration_lookup.json has no resolved k_selected. The full unfold was not started.")
        return 1
    finish_phase(args, "iteration_%s" % dimension.lower(), "")
    return 0


def unfold_histograms_ready(path, n_bins):
    return root_key_count(path, "Bayesian") >= n_bins


def run_unfold(args, dimension):
    bins = list(range(1, 18))
    out_path = unfold_output_path(args.data_root, dimension)
    n_need = 1 if(dimension == "5D") else len(bins)
    if(unfold_histograms_ready(out_path, n_need)):
        print("phase unfold_%s done" % dimension.lower())
        return 0
    if(not iteration_lookup_ready(dimension, args.acceptance_cut, bins)):
        mail_stop("unfold_%s" % dimension.lower(), "iteration lookup is not resolved")
        return 1
    response = histogram_response_path(args, "Only_3D" if(dimension == "3D") else "Only_5D")
    if(dimension == "5D"):
        from Campaign.run_sidis_campaign import k_for
        k_value, _provenance = k_for("5D", args.acceptance_cut, None, args.k_provenance)
        script = os.path.join(_BOOT, "run_Dedicated_5D_Unfold.py")
        argv = [script, "-droot", args.data_root, "--bayes_iterations", str(k_value), "--Min_Allowed_Acceptance_Cut", str(args.acceptance_cut), "--background_source", args.background_source, "-r", out_path, "-sfin", response]
        code = run_reserved("unfold_5d", argv, _BOOT, args.dry_run, "unfold_5d", args.data_root)
        n_need = 1
    else:
        from Campaign.run_sidis_campaign import unfold_3d_commands
        commands = unfold_3d_commands(args.acceptance_cut, args.phi_bins, args.background_source, bins, args.k_provenance, args.data_root)
        code = 0
        for _k_value, _q2y_list, command in commands:
            argv = shlex.split(command) + ["-r", out_path, "-sfin", response]
            code = run_reserved("unfold_3d", argv, _BOOT, args.dry_run, "unfold_3d", args.data_root)
            if(code != 0):
                return code
        n_need = len(bins)
    if(code != 0):
        return code
    if(args.dry_run):
        return 0
    if(not unfold_histograms_ready(out_path, n_need)):
        mail_stop("unfold_%s" % dimension.lower(), "unfolded Bayesian histograms are incomplete: %s" % out_path)
        return 1
    finish_phase(args, "unfold_%s" % dimension.lower(), "")
    return 0


def spawn_stage(args, stage, extra):
    driver = os.path.join(os.path.dirname(__file__), "run_sidis_campaign.py")
    argv = [sys.executable, driver, "-s", stage, "-orch", "direct", "-droot", args.data_root] + extra
    if(args.dry_run):
        argv.append("-n")
    if(getattr(args, "max_local_jobs", None) not in [None, ""]):
        argv.extend(["-mlj", str(args.max_local_jobs)])
    if(getattr(args, "systematics", None)):
        argv.extend(["-sys", args.systematics])
    if(getattr(args, "matching_criteria", None) not in [None]):
        argv.extend(["-mac", campaign_matching_value(args.matching_criteria)])
    if(("-hon" not in extra) and (getattr(args, "hpp_old_name", None) not in [None, ""])):
        argv.extend(["-hon", str(args.hpp_old_name)])
    for flag, value in response_override_pairs(args):
        argv.extend([flag, value])
    print("starting %s" % stage)
    show_command(argv)
    if(args.dry_run):
        return None
    return subprocess.Popen(argv)


def run_acceptance_regen(args):
    pure_cmd, spline_cmd, pure, spline = acceptance_commands(args.data_root, getattr(args, "matching_criteria", None))
    previous = {}
    for path in [pure, spline]:
        previous[path] = os.path.getmtime(path) if(os.path.isfile(path)) else None
    started = time.time()
    code = run_reserved("acceptance_pure", pure_cmd, os.path.dirname(pure_cmd[0]), args.dry_run, "acceptance", args.data_root)
    if(code != 0):
        return code
    code = run_reserved("acceptance_spline", spline_cmd, os.path.dirname(spline_cmd[0]), args.dry_run, "acceptance", args.data_root)
    if(code != 0):
        return code
    if(args.dry_run):
        return 0
    if((not hpp_was_rewritten(pure, previous[pure], started)) or (not hpp_was_rewritten(spline, previous[spline], started))):
        mail_stop("acceptance", "acceptance regeneration did not rewrite both HPP outputs")
        return 1
    return 0


def run_histogram_unfold(args):
    # Does not start RC or BC. Normal execution passes -sa and does not generate acceptance weights.
    if(getattr(args, "regenerate_acceptance", False)):
        code = run_acceptance_regen(args)
        if(code != 0):
            return code
        extra = ["-hon", "SIDIS_Workflow"]
    else:
        tag = campaign_hpp_tag(getattr(args, "hpp_old_name", None))
        if(not hpp_pair_ready(args.data_root, tag)):
            mail_stop("histogram_unfold", "acceptance weights for -hon %s are not usable, so histogram jobs were not started" % tag)
            return 1
        extra = ["-hon", tag]
    children = []
    proc = spawn_stage(args, "response_all", extra)
    if(proc is not None):
        children.append(("response_all", proc))
    return watch_histogram_chain(args, children)


def run_campaign(args):
    # RC and BC do not hold the histogram or unfolding stages.
    children = []
    for stage, extra in [("rc_regenerate", ["-rc", "regenerate"]), ("bc", []), ("response_all", [])]:
        proc = spawn_stage(args, stage, extra)
        if(proc is not None):
            children.append((stage, proc))
    return watch_histogram_chain(args, children)


def watch_histogram_chain(args, children):
    iteration_started = {"3D": False, "5D": False}
    iteration_done = {"3D": False, "5D": False}
    unfold_started = {"3D": False, "5D": False}
    if(args.dry_run):
        print("iteration studies start when the 3D and 5D aggregates exist")
        print("each full unfold starts when its iteration lookup is resolved")
        return 0
    while(True):
        for dimension, product_key in [("3D", "Only_3D"), ("5D", "Only_5D")]:
            ready = response_file_ready(histogram_response_path(args, product_key), "MultiDim")
            if(ready and (not iteration_started[dimension])):
                proc = spawn_stage(args, "iteration_%s" % dimension.lower(), [])
                if(proc is not None):
                    children.append(("iteration_%s" % dimension.lower(), proc))
                iteration_started[dimension] = True
            if(iteration_done[dimension] and iteration_lookup_ready(dimension, args.acceptance_cut, list(range(1, 18))) and (not unfold_started[dimension])):
                proc = spawn_stage(args, "unfold_%s" % dimension.lower(), [])
                if(proc is not None):
                    children.append(("unfold_%s" % dimension.lower(), proc))
                unfold_started[dimension] = True
        still = []
        for stage, proc in children:
            code = proc.poll()
            if(code is None):
                still.append((stage, proc))
            else:
                if(stage == "iteration_3d"):
                    iteration_done["3D"] = code == 0
                if(stage == "iteration_5d"):
                    iteration_done["5D"] = code == 0
                if(code != 0):
                    print("stage %s exited %s" % (stage, code))
                    if(stage in ["iteration_3d", "iteration_5d", "unfold_3d", "unfold_5d"]):
                        return code
        children = still
        if((len(children) == 0) and iteration_started["3D"] and iteration_started["5D"] and unfold_started["3D"] and unfold_started["5D"]):
            return 0
        if((len(children) == 0) and (not response_file_ready(histogram_response_path(args, "Only_3D"), "MultiDim"))):
            return 1
        if((len(children) == 0) and iteration_done["3D"] and (not unfold_started["3D"])):
            return 1
        if((len(children) == 0) and iteration_done["5D"] and (not unfold_started["5D"])):
            return 1
        time.sleep(5)


def five_d_only_response(data_root):
    return response_merged_path(data_root, "Only_5D", "SIDIS_Workflow", "Bank")


def five_d_only_root(data_root):
    return os.path.join(data_root_path(data_root), "Unfold_5D_Only")


def five_d_study_argv(data_root, response, root_out, background="rho0_new"):
    # Previous argv used "--background_source", "lundvpk".  # 10/25/2026
    script = os.path.join(_BOOT, "run_Dedicated_5D_Unfold.py")
    return [sys.executable, script, "-droot", str(data_root), "-sfin", response, "-r", root_out, "--iteration_study", "--study_only", "--error_mode", "errors", "--parm_min", "1", "--parm_max", "10", "--parm_step", "1", "--background_source", background, "--Min_Allowed_Acceptance_Cut", "0.020", "--phi_bins", "24", "--email"]


def five_d_nominal_argv(data_root, response, root_out, k_value, background="rho0_new"):
    # Previous argv used "--background_source", "lundvpk".  # 10/25/2026
    script = os.path.join(_BOOT, "run_Dedicated_5D_Unfold.py")
    return [sys.executable, script, "-droot", str(data_root), "-sfin", response, "-r", root_out, "--error_mode", "covariance", "--bayes_iterations", str(int(k_value)), "--background_source", background, "--Min_Allowed_Acceptance_Cut", "0.020", "--phi_bins", "24"]


def five_d_log_line(handle, text, echo=True):
    line = "[%s] %s\n" % (time.strftime("%Y-%m-%d %H:%M:%S"), str(text).rstrip("\n"))
    if(handle is not None):
        handle.write(line)
        handle.flush()
    if(echo):
        print(line, end="")
        sys.stdout.flush()


def five_d_tee(stage, argv, log_path, orchestrator):
    started = time.time()
    five_d_log_line(orchestrator, "stage %s start" % stage)
    five_d_log_line(orchestrator, " ".join(argv))
    handle = open(log_path, "a", buffering=1)
    five_d_log_line(handle, "stage %s start" % stage)
    proc = subprocess.Popen([str(part) for part in argv], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    for line in proc.stdout:
        five_d_log_line(handle, line)
        five_d_log_line(orchestrator, line, echo=False)
    code = proc.wait()
    elapsed = time.time() - started
    five_d_log_line(handle, "stage %s exit %s elapsed %.1f" % (stage, code, elapsed))
    five_d_log_line(orchestrator, "stage %s exit %s elapsed %.1f" % (stage, code, elapsed))
    handle.close()
    return code


def five_d_list_lines(path, list_name):
    import ROOT
    root_file = ROOT.TFile.Open(str(path), "READ")
    if((root_file is None) or root_file.IsZombie()):
        if(root_file is not None):
            root_file.Close()
        return None
    listed = root_file.Get(list_name)
    lines = []
    try:
        if((listed is not None) and listed.InheritsFrom("TList")):
            for index in range(int(listed.GetSize())):
                lines.append(str(listed.At(index).GetString()))
    except Exception:
        lines = []
    root_file.Close()
    return lines


def five_d_config_map(path):
    lines = five_d_list_lines(path, "Detected_5D_Config")
    if(lines is None):
        return None
    mapped = {}
    for line in lines:
        if("=" in line):
            key, value = line.split("=", 1)
            mapped[key] = value
    return mapped


def five_d_acceptance_matches(mapped):
    try:
        return abs(float(mapped.get("Min_Allowed_Acceptance_Cut", "nan")) - 0.020) < 1e-4
    except ValueError:
        return False


def five_d_series_from(path, hist_name):
    import ROOT
    from plot_iteration_study import extract_iteration_series
    root_file = ROOT.TFile.Open(str(path), "READ")
    if((root_file is None) or root_file.IsZombie()):
        if(root_file is not None):
            root_file.Close()
        return None
    hist = root_file.Get(hist_name)
    if(hist is None):
        root_file.Close()
        return None
    series = extract_iteration_series(hist, 10)
    root_file.Close()
    return series


def five_d_study_is_valid(path, response):
    if(not os.path.isfile(path)):
        return False
    names = five_d_list_lines(path, "Latest_List_of_File_Names")
    mapped = five_d_config_map(path)
    if((names is None) or (response not in names) or (mapped is None)):
        return False
    if(mapped.get("error_mode") != "errors"):
        return False
    if(mapped.get("study_only") != "1"):
        return False
    if(mapped.get("old_binning") != "0"):
        return False
    if(not five_d_acceptance_matches(mapped)):
        return False
    for hist_name in ["Iteration_Study_Chi2", "Iteration_Study_MeanResiduals", "Iteration_Study_RMSError"]:
        series = five_d_series_from(path, hist_name)
        if((series is None) or (any(k not in series for k in range(1, 11)))):
            return False
    return True


def five_d_nominal_is_valid(path, response, k_value):
    if(not os.path.isfile(path)):
        return False
    names = five_d_list_lines(path, "Latest_List_of_File_Names")
    mapped = five_d_config_map(path)
    if((names is None) or (response not in names) or (mapped is None)):
        return False
    if(mapped.get("error_mode") != "covariance"):
        return False
    if(mapped.get("old_binning") != "0"):
        return False
    if(not five_d_acceptance_matches(mapped)):
        return False
    if(str(mapped.get("bayes_iterations")) != str(int(k_value))):
        return False
    import ROOT
    root_file = ROOT.TFile.Open(str(path), "READ")
    if((root_file is None) or root_file.IsZombie()):
        if(root_file is not None):
            root_file.Close()
        return False
    found = False
    for key in root_file.GetListOfKeys():
        if("Bayesian" in str(key.GetName())):
            found = True
            break
    root_file.Close()
    return found


def five_d_sibling(path):
    base, ext = os.path.splitext(path)
    return "%s_%s%s" % (base, time.strftime("%Y%m%dT%H%M%SZ", time.gmtime()), ext)


def five_d_selector_args():
    class Clip(object):
        pass
    args = Clip()
    args.clip_min = 1
    args.clip_max = 10
    args.epsilon = 1e-12
    args.tau_trend = 0.03
    args.tau_flat = 0.03
    args.tau_confirm = 0.03
    args.flag_spread = 4
    return args


def five_d_write_selection(out_dir, result):
    from plot_iteration_study import draw_group
    plot_dir = os.path.join(out_dir, "plots")
    os.makedirs(plot_dir, exist_ok=True)
    classes = result["classes"]
    lines = [
        "status %s" % result["status"],
        "median %s" % ("" if(result["median"] is None) else str(result["median"])),
        "spread %s" % ("" if(result["spread"] is None) else str(result["spread"])),
        "spread_flag %s" % result["spread_flag"],
        "chi2 k=%s %s" % (classes["chi2"]["k"], classes["chi2"]["reason"]),
        "mean_abs k=%s %s" % (classes["mean_abs"]["k"], classes["mean_abs"]["reason"]),
        "rms_error k=%s %s" % (classes["rms_error"]["k"], classes["rms_error"]["reason"]),
    ]
    for name, holes in result["holes"].items():
        if(len(holes) > 0):
            lines.append("missing %s %s" % (name, ",".join([str(k) for k in holes])))
    text_path = os.path.join(plot_dir, "iteration_recommendations.txt")
    handle = open(text_path, "w")
    handle.write("\n".join(lines) + "\n")
    handle.close()
    try:
        draw_group("all", result, plot_dir, five_d_selector_args())
    except Exception as exc:
        lines.append("plot failed: %s" % exc)
        handle = open(text_path, "a")
        handle.write("plot failed: %s\n" % exc)
        handle.close()
    return text_path, lines


def run_unfold_5d_only(args):
    response = five_d_only_response(args.data_root)
    out_dir = five_d_only_root(args.data_root)
    log_dir = os.path.join(out_dir, "logs")
    study_root = os.path.join(out_dir, "iteration_study_errors.root")
    nominal_root = os.path.join(out_dir, "nominal_covariance.root")
    log_paths = {
        "orchestrator": os.path.join(log_dir, "orchestrator.log"),
        "study": os.path.join(log_dir, "iteration_study.log"),
        "selection": os.path.join(log_dir, "selection.log"),
        "nominal": os.path.join(log_dir, "nominal_unfold.log"),
    }
    print("5D-only input %s" % response)
    for name in ["orchestrator", "study", "selection", "nominal"]:
        print("5D-only log %s %s" % (name, log_paths[name]))
    study_cmd = five_d_study_argv(args.data_root, response, study_root, args.background_source)
    print("5D-only study")
    print(" ".join(study_cmd))
    print("5D-only nominal uses --error_mode covariance and the selected --bayes_iterations")
    print(" ".join(five_d_nominal_argv(args.data_root, response, nominal_root, 5, args.background_source)))
    if(args.dry_run):
        return 0
    if(not os.path.isfile(response)):
        mail_stop("unfold_5d_only", "thesis 5D response file is missing: %s" % response)
        return 1
    os.makedirs(log_dir, exist_ok=True)
    orchestrator = open(log_paths["orchestrator"], "a", buffering=1)
    five_d_log_line(orchestrator, "input %s" % response)
    summary_lines = ["input %s" % response]
    try:
        if(five_d_study_is_valid(study_root, response)):
            five_d_log_line(orchestrator, "reusing study %s" % study_root)
            mail_note("SIDIS 5D iteration study already valid", "phase: unfold_5d_only\nstudy: %s\nThe existing study was accepted. Nominal unfolding follows selection.\n" % study_root)
            summary_lines.append("study reused %s" % study_root)
        else:
            if(os.path.isfile(study_root)):
                study_root = five_d_sibling(study_root)
                study_cmd = five_d_study_argv(args.data_root, response, study_root, args.background_source)
                five_d_log_line(orchestrator, "existing study was not reused. New study file %s" % study_root)
            code = five_d_tee("iteration_study", study_cmd, log_paths["study"], orchestrator)
            if(code != 0):
                mail_stop("unfold_5d_only", "iteration study exited %s" % code)
                summary_lines.append("study failed exit %s" % code)
                return 1
            if(not five_d_study_is_valid(study_root, response)):
                mail_stop("unfold_5d_only", "iteration study exited 0 but the diagnostics or config do not match: %s" % study_root)
                summary_lines.append("study invalid %s" % study_root)
                return 1
            summary_lines.append("study wrote %s" % study_root)
        # select_5d_iteration was the older median rule. Nominal 5D k is 5. 10/28/2026
        k_value = 5
        selection_lines = ["nominal 5D k %d" % k_value]
        selection_log = open(log_paths["selection"], "a", buffering=1)
        for line in selection_lines:
            five_d_log_line(selection_log, line)
            five_d_log_line(orchestrator, line)
        selection_log.close()
        summary_lines.extend(selection_lines)
        if(five_d_nominal_is_valid(nominal_root, response, k_value)):
            five_d_log_line(orchestrator, "reusing nominal %s" % nominal_root)
            summary_lines.append("nominal reused %s" % nominal_root)
        else:
            if(os.path.isfile(nominal_root)):
                nominal_root = five_d_sibling(nominal_root)
                five_d_log_line(orchestrator, "existing nominal was not reused. New nominal file %s" % nominal_root)
            code = five_d_tee("nominal_unfold", five_d_nominal_argv(args.data_root, response, nominal_root, k_value, args.background_source), log_paths["nominal"], orchestrator)
            if(code != 0):
                mail_stop("unfold_5d_only", "nominal unfold exited %s" % code)
                summary_lines.append("nominal failed exit %s" % code)
                return 1
            if(not five_d_nominal_is_valid(nominal_root, response, k_value)):
                mail_stop("unfold_5d_only", "nominal unfold exited 0 but the config does not match k=%s: %s" % (k_value, nominal_root))
                summary_lines.append("nominal invalid %s" % nominal_root)
                return 1
            summary_lines.append("nominal wrote %s" % nominal_root)
        summary_lines.append("selected k %s" % k_value)
        summary_lines.append("error_mode study=errors nominal=covariance")
        mail_note("SIDIS 5D-only workflow finished", "phase: unfold_5d_only\nselected k: %s\nstudy: %s\nnominal: %s\n" % (k_value, study_root, nominal_root))
        return 0
    finally:
        summary_path = os.path.join(out_dir, "summary.txt")
        try:
            os.makedirs(out_dir, exist_ok=True)
            handle = open(summary_path, "w")
            handle.write("\n".join(summary_lines) + "\n")
            handle.close()
            five_d_log_line(orchestrator, "summary %s" % summary_path)
        except Exception:
            pass
        orchestrator.close()


def run_direct(args):
    os.environ["SIDIS_ANALYSIS_ROOT"] = _BOOT
    os.environ["SIDIS_DATA_ROOT"] = str(args.data_root)
    if(args.stage == "early_chain"):
        code = run_early(args)
    elif(args.stage == "rc_regenerate"):
        code = run_rc(args)
    elif(args.stage == "bc"):
        code = run_bc(args)
    elif(args.stage == "response_all"):
        code = run_response(args, "")
    elif(args.stage == "response_1d"):
        code = run_response(args, "1D")
    elif(args.stage == "diagnostic_1d"):
        code = run_response(args, "diag")
    elif(args.stage == "histogram_1d"):
        code = run_response(args, "both1d")
    elif(args.stage == "iteration_3d"):
        code = run_iteration(args, "3D")
    elif(args.stage == "iteration_5d"):
        code = run_iteration(args, "5D")
    elif(args.stage == "unfold_3d"):
        code = run_unfold(args, "3D")
    elif(args.stage == "unfold_5d"):
        code = run_unfold(args, "5D")
    elif(args.stage == "campaign"):
        code = run_campaign(args)
    elif(args.stage == "histogram_unfold"):
        code = run_histogram_unfold(args)
    elif(args.stage == "unfold_5d_only"):
        code = run_unfold_5d_only(args)
    else:
        print("direct orchestration does not run stage %s" % args.stage)
        code = 1
    if(code != 0):
        sys.exit(code)
