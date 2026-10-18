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
BC_NO_RAD = "/lustre24/expphy/volatile/clas12/richcap/Radiative_MC_EvGen_Files/Binned_Files_Made_through_sbatch/LUND_EvGen_Iterative_richcap_SBATCH_richcap_Old_MM_Cut_Groups_*No_Rad*.root"


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


def bc_output_candidates(input_path, label):
    # Nominal files stay in the flat ceph directory or its Path_to_Volatile runs.
    # Sensitivity files stay in sens_<var>_<value> and are not mixed into that search.
    out_name = bc_output_name(input_path)
    found = []
    if(label == ""):
        flat = os.path.join(bc_root_dir(), out_name)
        if(os.path.isfile(flat)):
            found.append(flat)
        matches = glob.glob(os.path.join(bc_root_dir(), "Path_to_Volatile", "*", out_name))
        for match in sorted(matches):
            if(match not in found):
                found.append(match)
        return found
    flat = os.path.join(bc_root_dir(), label, out_name)
    if(os.path.isfile(flat)):
        found.append(flat)
    return found


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


def bc_hist_name(q2_bin, zpt_bin):
    # Every direct command passes -nb 3 -nbphi 2. Per-axis overrides are not in this name.
    return "Histogram Bin (%d-%d)-(Num SubBins=3)-(Extra phi_h SubBins=2)" % (q2_bin, zpt_bin)


def bc_nsub(counts):
    return counts["q2"] * counts["y"] * counts["z"] * counts["pt"] * counts["phi"]


BC_STATUS_CACHE = {}


def bc_histogram_status(path, counts):
    # Names, classes, and axis sizes only. Bin contents are not read.
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
    expected = []
    for q2_bin, zpt_bin in bc_expected_bins():
        expected.append(bc_hist_name(q2_bin, zpt_bin))
    nx_need = bc_nsub(counts) + 2
    root_file = None
    status = "unread"
    try:
        root_file = ROOT.TFile.Open(str(path), "READ")
        if(root_file is None):
            status = "incomplete"
        elif(root_file.IsZombie()):
            status = "incomplete"
        elif(hasattr(ROOT.TFile, "kRecovered") and root_file.TestBit(ROOT.TFile.kRecovered)):
            status = "incomplete"
        else:
            classes = {}
            for key in root_file.GetListOfKeys():
                classes[str(key.GetName())] = str(key.GetClassName())
            status = "complete"
            for name, klass in classes.items():
                if(name.startswith("Histogram Bin (") and (name not in expected)):
                    status = "incomplete"
            if(status == "complete"):
                for name in expected:
                    if("TH2" not in classes.get(name, "")):
                        status = "incomplete"
                        break
                    hist = root_file.Get(name)
                    if(hist is None):
                        status = "incomplete"
                        break
                    if((hist.GetNbinsX() != nx_need) or (hist.GetNbinsY() != 24)):
                        status = "incomplete"
                        break
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
    return status


def bc_histograms_match(path, counts):
    return bc_histogram_status(path, counts) == "complete"


def bc_output_path(input_path, label, counts):
    saw_unread = False
    for path in bc_output_candidates(input_path, label):
        status = bc_histogram_status(path, counts)
        if(status == "complete"):
            return path
        if(status == "unread"):
            saw_unread = True
    if(saw_unread):
        return None
    return ""


def bc_complete_outputs(inputs, label, counts):
    found = []
    seen = set()
    for bc_input in inputs:
        path = bc_output_path(bc_input, label, counts)
        if(path is None):
            return None
        if((path == "") or (path in seen)):
            continue
        seen.add(path)
        found.append(path)
    return found


def remove_incomplete_bc_outputs(input_path, label, counts, dry_run):
    # BC opens an existing file in UPDATE. A partial file has to be removed or its old histograms stay.
    for path in bc_output_candidates(input_path, label):
        status = bc_histogram_status(path, counts)
        if(status == "complete"):
            continue
        if(status == "unread"):
            print("could not inspect BC output; it was left in place: %s" % path)
            return False
        print("removing incomplete BC output so it is recreated: %s" % path)
        if(not dry_run):
            os.remove(path)
    return True


def bc_merged_path(label):
    folder = bc_root_dir() if(label == "") else os.path.join(bc_root_dir(), label)
    return os.path.join(folder, "Sub_Bin_Contents_for_BC_Correction_with_Binned_sbatch.root")


def bc_json_path(label):
    if(label == ""):
        return os.path.join(_BOOT, "BC_Corrections", "Sub_Bin_Contents_for_BC_Correction_with_Binned_sbatch.json")
    return os.path.join(bc_root_dir(), label, "Sub_Bin_Contents_for_BC_Correction_with_Binned_sbatch.json")


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
    if(label == ""):
        out_rel = "ROOT_Files_Output/Sub_Bin_Contents_for_BC_Correction.root"
        return "./BC_Corrections_Script.py -nb 3 -nbphi 2 -hi -ufn --root_file_out %s" % out_rel
    out_rel = "ROOT_Files_Output/%s/Sub_Bin_Contents_for_BC_Correction.root" % label
    return "./BC_Corrections_Script.py -nb 3 -nbphi 2 -nbq %d -nby %d -nbz %d -nbpt %d -nbh %d -hi -ufn --root_file_out %s" % (
        counts["q2"], counts["y"], counts["z"], counts["pt"], counts["phi"], out_rel)


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
    merged = os.path.join(data_root_path(args.data_root), REL_HADD, "SIDIS_epip_Response_Matrices_from_RDataFrames_Only_2D_rho0_Normalization_Creation_%s_Final_Thesis_Files_All.root" % token)
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
            ("rho_hist", [submit, "-droot", args.data_root, "-m", "hybrid", "-rho", "-jrho0", "10", "-n", token, "-e", "-em", phase_message(args, "rho_hist")], frames),
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
    if(rc_build_outputs_ready(task_list, merged)):
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
    per_file = bc_worker_command(label, counts)
    bc_inputs = expand_patterns([BC_NO_RAD])
    done_inputs = []
    missing_inputs = []
    for bc_input in bc_inputs:
        found = bc_output_path(bc_input, label, counts)
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
            if(not remove_incomplete_bc_outputs(bc_input, label, counts, args.dry_run)):
                mail_stop(hist_phase, "could not inspect an existing BC output; it was left in place")
                return 1
        argv = [runner, "-rm", "hybrid", "-j", "10", "-y", "-e", "-rcl", phase_message(args, hist_phase), "-c", per_file]
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
            found = bc_output_path(bc_input, label, counts)
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
    outputs = bc_complete_outputs(bc_inputs, label, counts)
    if(outputs is None):
        mail_stop(hadd_phase, "could not inspect a BC output; hadd was not run")
        return 1
    if(len(outputs) != len(bc_inputs)):
        mail_stop(hadd_phase, "per-file outputs %d of %d; hadd was not run" % (len(outputs), len(bc_inputs)))
        return 1
    dest = bc_merged_path(label)
    json_path = bc_json_path(label)
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
        hadd_argv = bc_hadd_argv(dest, outputs)
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
