#!/usr/bin/env python3
# Read-only inventory plus recovery lists. A usable output is the verdict. It does not submit or cancel.
import glob
import os
import sys

_BOOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if(_BOOT not in sys.path):
    sys.path.insert(0, _BOOT)

from Campaign.ifarm_inputs import classify_rho_name, load_ifarm_inputs, rho_source_token
from Campaign.local_orchestrator import (
    GEN_DIR, RC_RUNTIME, REC_DIR, expand_patterns, groovy_sbatch_path,
    input_folder, matching_groovy_roots, parse_groovy_sbatch, read_manifest_patterns, sacct_tasks,
)
from jlab_work_paths import REL_FILE_BATCHES, REL_HADD, data_root_path, dataframe_output_dir, resolve_pipeline_input

BC_DIR = os.path.join(_BOOT, "BC_Corrections")
BC_FLAT = os.path.join(BC_DIR, "ROOT_Files_Output")
BC_VOLATILE = os.path.join(BC_FLAT, "Path_to_Volatile")
BC_NO_RAD = "/lustre24/expphy/volatile/clas12/richcap/Radiative_MC_EvGen_Files/Binned_Files_Made_through_sbatch/LUND_EvGen_Iterative_richcap_SBATCH_richcap_Old_MM_Cut_Groups_*No_Rad*.root"
GROOVY = os.path.join(_BOOT, "Data_Files_Groovy", "run_groovy_scripts_with_emails.py")
HELPER = os.path.join(_BOOT, "Histo_Files_ROOT", "DataFrames", "run_dataframe_makeROOT_helper.py")
BATCHES = os.path.join(_BOOT, "Histo_Files_ROOT", "DataFrames", "run_sidis_DataFrame_pipeline.py")
SUBMIT = os.path.join(_BOOT, "Histo_Files_ROOT", "DataFrames", "Submit_Full_Histogram_Creation_Pipeline.py")
FIT = os.path.join(_BOOT, "Histo_Files_ROOT", "DataFrames", "Get_rho_Normalization_values.py")
FRAMES = os.path.join(_BOOT, "Histo_Files_ROOT", "DataFrames")
BUILD = None
ACTIONS = []


def checkout_evgen_build():
    from Campaign.early_chain import evgen_dir
    return os.path.join(evgen_dir(), "Run_Large_Files_For_Iterative_Corrections", "Comparison_With_Unfolding", "Build_EvGen_PerFile_Hists.py")


def compare_script():
    return os.path.join(os.path.dirname(checkout_evgen_build()), "Comparison_Between_GEN_and_Unfold.py")


def root_verdict(path):
    # completed, missing, or uncertain. Histograms are not read.
    if(path in [None, ""]):
        return "uncertain"
    if(not os.path.isfile(path)):
        return "missing"
    try:
        if(os.path.getsize(path) <= 0):
            return "missing"
    except OSError:
        return "uncertain"
    try:
        import ROOT
    except Exception:
        return "uncertain"
    root_file = None
    try:
        root_file = ROOT.TFile.Open(str(path), "READ")
        if(root_file is None):
            return "missing"
        if(root_file.IsZombie()):
            return "missing"
        recovered = False
        if(hasattr(root_file, "IsRecovered")):
            recovered = bool(root_file.IsRecovered())
        elif(hasattr(ROOT.TFile, "kRecovered")):
            recovered = bool(root_file.TestBit(ROOT.TFile.kRecovered))
        if(recovered):
            return "missing"
        return "completed"
    except Exception:
        return "uncertain"
    finally:
        if(root_file is not None):
            try:
                root_file.Close()
            except Exception:
                pass


def text_verdict(path):
    if(not os.path.isfile(path)):
        return "missing"
    try:
        if(os.path.getsize(path) <= 0):
            return "missing"
    except OSError:
        return "uncertain"
    return "completed"


def groovy_output(hipo_path, source, mc_type):
    base = os.path.basename(hipo_path)
    low = base.lower()
    suff = "inb.qa" if(("inb" in low) and ("gemc" not in low)) else "gemc"
    if(mc_type == "gdf"):
        folder = GEN_DIR
        stem = "MC_Gen_sidis_epip_richcap.%s" % suff
    else:
        folder = REC_DIR
        stem = "MC_Matching_sidis_epip_richcap.%s" % suff
    if(source == "rho0"):
        stem = stem + ".rho0"
    return os.path.join(folder, "%s.new10.%s.root" % (stem, base))


def file_num_from_groovy(groovy_path):
    text = os.path.basename(groovy_path).split(".hipo")[0]
    if(".new10." not in text):
        return None, "SIDIS"
    label = classify_rho_name(text) or "SIDIS"
    tail = text.split(".new10.")[-1]
    tail = tail.replace("nSidis_00", "")
    mc = "EvGen_" if("EvGen" in tail) else ""
    background = "55nA_" if("55na" in tail.lower()) else ""
    tail = background + tail.split("10604MeV-")[-1]
    tail = mc + tail.split("-")[-1]
    return tail, label


def dataframe_output(groovy_path, data_type, data_root):
    tail, label = file_num_from_groovy(groovy_path)
    if(tail is None):
        return None
    common = "Pass_2_Final_Analysis_Iterations_I0_"
    if(label not in ["SIDIS", ""]):
        common = common + label + "_"
    if(data_type == "gdf"):
        name = "DataFrame_SIDIS_epip_MC_GEN_%s%s.root" % (common, tail)
    else:
        name = "DataFrame_SIDIS_epip_MC_Matched_%s%s.root" % (common, tail)
    name = name.replace("__", "_")
    return os.path.join(dataframe_output_dir(data_root, data_type), name)


def write_lines(folder, name, lines):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, name)
    handle = open(path, "w")
    for line in lines:
        handle.write(line + "\n")
    handle.close()
    return path


def sacct_note(job_name):
    arrays = sacct_tasks(job_name=job_name)
    if(arrays is None):
        print("  note: sacct was not read")
        return
    completed = 0
    other = 0
    for tasks in arrays.values():
        for state, exit_code in tasks.values():
            if((state == "COMPLETED") and str(exit_code).startswith("0:")):
                completed += 1
            else:
                other += 1
    print("  note: sacct arrays %s COMPLETED_exit0 %d other %d (not a verdict)" % (",".join(sorted(arrays.keys())), completed, other))


def add_action(kind, text):
    ACTIONS.append((kind, text))
    print(kind + ": " + text)


def groovy_and_frames(data_root, recovery):
    config = load_ifarm_inputs()
    token = rho_source_token(config) or "rho0_new"
    groovy_dir = os.path.dirname(GROOVY)
    groups = [
        ("rho_gdf", "rho0", "gdf"),
        ("rho_mdf", "rho0", "mdf"),
        ("55na_gdf", "clasdis", "gdf"),
        ("55na_mdf", "clasdis", "mdf"),
    ]
    frame_ready = True
    for group, source, mc_type in groups:
        print("workload groovy %s %s" % (source, mc_type))
        script = groovy_sbatch_path(groovy_dir, source, mc_type)
        if(not os.path.isfile(script)):
            print("  uncertain: sbatch script missing")
            frame_ready = False
            add_action("blocked", "groovy %s %s has no sbatch script" % (source, mc_type))
            continue
        job_name, array_spec, manifest = parse_groovy_sbatch(script)
        print("  sbatch %s job %s array %s" % (os.path.basename(script), job_name, array_spec))
        sacct_note(job_name)
        if(not os.path.isfile(manifest)):
            print("  uncertain: manifest missing")
            frame_ready = False
            add_action("blocked", "groovy %s %s manifest is missing" % (source, mc_type))
            continue
        hipos = expand_patterns(read_manifest_patterns(manifest))
        missing_hipo = []
        completed_groovy = []
        uncertain = 0
        for hipo in hipos:
            roots = matching_groovy_roots(hipo, source, mc_type)
            if(len(roots) > 0):
                completed_groovy.append(hipo)
            else:
                missing_hipo.append(hipo)
        print("  groovy outputs completed %d missing %d uncertain %d of %d" % (len(completed_groovy), len(missing_hipo), uncertain, len(hipos)))
        if(uncertain > 0):
            frame_ready = False
            add_action("blocked", "groovy %s %s has uncertain outputs" % (source, mc_type))
        elif(len(missing_hipo) == 0):
            add_action("done", "groovy %s %s" % (source, mc_type))
        else:
            listed = write_lines(recovery, "groovy_%s_%s.txt" % (source, mc_type), missing_hipo)
            add_action("rerun", "%s -m hybrid -pj 10 -na -e -src %s -mc %s -ptxt %s" % (GROOVY, source, mc_type, listed))
            frame_ready = False
        missing_frames = []
        frame_uncertain = 0
        frame_done = 0
        for hipo in completed_groovy:
            roots = matching_groovy_roots(hipo, source, mc_type)
            groovy_file = roots[0] if(len(roots) > 0) else ""
            frame = dataframe_output(groovy_file, mc_type, data_root)
            status = root_verdict(frame)
            if(status == "completed"):
                frame_done += 1
            elif(status == "missing"):
                missing_frames.append(groovy_file)
            else:
                frame_uncertain += 1
        print("  dataframe outputs completed %d missing %d uncertain %d" % (frame_done, len(missing_frames), frame_uncertain))
        if((frame_uncertain > 0) or (len(missing_hipo) > 0) or (uncertain > 0) or (len(missing_frames) > 0)):
            frame_ready = False
            if(frame_uncertain > 0):
                add_action("blocked", "dataframe %s has uncertain outputs" % group)
        if((frame_uncertain == 0) and (len(missing_hipo) == 0) and (uncertain == 0) and (len(missing_frames) == 0)):
            add_action("done", "dataframe %s" % group)
        elif((frame_uncertain == 0) and (uncertain == 0) and (len(missing_frames) > 0)):
            listed = write_lines(recovery, "dataframe_%s.txt" % group, missing_frames)
            add_action("rerun", "%s -droot %s -o work -il %s -dtype %s -m hybrid -j 10 -y" % (HELPER, data_root, listed, mc_type))
    return frame_ready, token


def later_early(data_root, token, frame_ready):
    batch_file = resolve_pipeline_input(REL_FILE_BATCHES, data_root)
    batch_status = text_verdict(batch_file)
    merged = os.path.join(data_root_path(data_root), REL_HADD, "SIDIS_epip_Response_Matrices_from_RDataFrames_Only_2D_rho0_Normalization_Creation_%s_Final_Thesis_Files_All.root" % token)
    merged_status = root_verdict(merged)
    review = os.path.join(FRAMES, "exclusive_rho_review_%s.txt" % token)
    review_status = text_verdict(review)
    print("phase make_batches file %s %s" % (batch_status, batch_file))
    print("phase rho_hist file %s %s" % (merged_status, merged))
    print("phase rho_fit file %s %s" % (review_status, review))
    if(not frame_ready):
        add_action("blocked", "make_batches waits until every DataFrame output is completed")
        return
    if(batch_status == "completed"):
        add_action("done", "make_batches")
    elif(batch_status == "missing"):
        add_action("rerun", "%s -droot %s -m make_batches -rst %s" % (BATCHES, data_root, token))
    else:
        add_action("blocked", "make_batches output is uncertain")
        return
    if(batch_status != "completed"):
        add_action("blocked", "rho_hist waits until File_Batches.py is completed")
        return
    if(merged_status == "completed"):
        add_action("done", "rho_hist")
    elif(merged_status == "missing"):
        add_action("rerun", "%s -droot %s -m hybrid -rho -jrho0 10 -n %s" % (SUBMIT, data_root, token))
        add_action("blocked", "rho_fit waits until the merged histogram is completed")
        return
    else:
        add_action("blocked", "rho_hist output is uncertain")
        return
    if(review_status == "completed"):
        add_action("done", "rho_fit")
    elif(review_status == "missing"):
        add_action("rerun", "%s -droot %s -st %s -usf -f1 %s" % (FIT, data_root, token, merged))
    else:
        add_action("blocked", "rho_fit review file is uncertain")


def report_rc(data_root):
    print("workflow rc_regenerate")
    task_list = os.path.join(RC_RUNTIME, "evgen_perfile_task_list.txt")
    merged = os.path.join(RC_RUNTIME, "merged_outputs", "Merged_EvGen_PerFile_Hists.root")
    factors = os.path.join(RC_RUNTIME, "merged_outputs", "RC_Factors_ifarm_rc.root")
    if(not os.path.isfile(task_list)):
        print("  per-file inventory uncertain: task list missing")
        add_action("blocked", "rc_build has no evgen_perfile_task_list.txt")
        return
    missing = 0
    completed = 0
    uncertain = 0
    handle = open(task_list)
    for line in handle:
        line = line.strip()
        if((line == "") or line.startswith("#")):
            continue
        parts = line.split("\t")
        if(len(parts) < 4):
            uncertain += 1
            continue
        status = root_verdict(parts[3])
        if(status == "completed"):
            completed += 1
        elif(status == "missing"):
            missing += 1
        else:
            uncertain += 1
    handle.close()
    print("  workers completed %d missing %d uncertain %d" % (completed, missing, uncertain))
    merged_status = root_verdict(merged)
    factor_status = root_verdict(factors)
    print("  merged %s" % merged_status)
    print("  factors %s" % factor_status)
    build = checkout_evgen_build()
    if(uncertain > 0):
        add_action("blocked", "rc_build worker inventory is uncertain")
        return
    if(merged_status == "completed"):
        add_action("done", "rc_build")
    elif((missing > 0) or (merged_status == "missing")):
        add_action("rerun", "%s -m hybrid -y -p -mpj 10 -rdir %s" % (build, RC_RUNTIME))
        add_action("blocked", "rc_compare waits until the merged EvGen file is completed")
        return
    else:
        add_action("blocked", "rc merged file is uncertain")
        return
    compare = compare_script()
    if(factor_status == "completed"):
        add_action("done", "rc_compare")
    elif(factor_status == "missing"):
        add_action("rerun", "%s -r %s -ssf -sfn %s -rc -Nw -evgen" % (compare, merged, factors))
    else:
        add_action("blocked", "rc factor file is uncertain")


def bc_output(input_path):
    name = os.path.basename(input_path)
    name = name.split("new6.")[-1].replace(".hipo.root", "").replace(".root", "")
    out_name = "Sub_Bin_Contents_for_BC_Correction_%s.root" % name
    flat = os.path.join(BC_FLAT, out_name)
    if(os.path.isfile(flat)):
        return flat
    matches = glob.glob(os.path.join(BC_VOLATILE, "*", out_name))
    if(len(matches) == 1):
        return matches[0]
    if(len(matches) > 1):
        return None
    return flat


def report_bc(recovery):
    print("workflow bc")
    inputs = expand_patterns([BC_NO_RAD])
    if(len(inputs) == 0):
        print("  uncertain: No_Rad glob matched nothing")
        add_action("blocked", "bc inputs were not found")
        return
    missing_indexes = []
    completed_paths = []
    uncertain = 0
    for index, path in enumerate(inputs):
        out_path = bc_output(path)
        if(out_path is None):
            uncertain += 1
            continue
        status = root_verdict(out_path)
        if(status == "completed"):
            completed_paths.append(out_path)
        elif(status == "missing"):
            missing_indexes.append(index)
        else:
            uncertain += 1
    print("  per-file completed %d missing %d uncertain %d of %d" % (len(completed_paths), len(missing_indexes), uncertain, len(inputs)))
    runner = os.path.join(BC_DIR, "Run_BC_Scripts_Locally.py")
    factor = os.path.join(BC_DIR, "BC_Corrections_Script.py")
    last = len(inputs) - 1
    if(uncertain > 0):
        add_action("blocked", "bc per-file inventory is uncertain")
    elif(len(missing_indexes) == 0):
        add_action("done", "bc_hist")
    elif(last not in missing_indexes):
        add_action("blocked", "bc_hist would UPDATE the completed last input because -ix does not stop that automatic file")
    else:
        spec = compress_indexes(missing_indexes)
        listed = write_lines(recovery, "bc_indices.txt", [spec])
        add_action("rerun", "%s -rm hybrid -j 10 -y -ix %s -c \"./BC_Corrections_Script.py -nb 3 -nbphi 2 -hi -ufn --root_file_out ROOT_Files_Output/Sub_Bin_Contents_for_BC_Correction.root\"" % (runner, spec))
        print("  wrote %s" % listed)
    combined = os.path.join(BC_FLAT, "Sub_Bin_Contents_for_BC_Correction_with_Binned_sbatch.root")
    combined_status = root_verdict(combined)
    json_path = os.path.join(BC_DIR, "Sub_Bin_Contents_for_BC_Correction_with_Binned_sbatch.json")
    json_status = text_verdict(json_path)
    print("  combined %s" % combined_status)
    print("  json %s" % json_status)
    if((len(missing_indexes) == 0) and (uncertain == 0) and (combined_status == "missing")):
        listed = write_lines(recovery, "bc_per_file.txt", completed_paths)
        add_action("rerun", "hadd_richcap %s $(cat %s)" % (combined, listed))
    elif(combined_status == "completed"):
        add_action("done", "bc_hadd")
    elif(len(missing_indexes) > 0):
        add_action("blocked", "bc_hadd waits until every per-file output is completed")
    if(combined_status != "completed"):
        add_action("blocked", "bc_factors waits until the combined ROOT file is completed")
        return
    if(json_status == "completed"):
        add_action("done", "bc_factors")
    elif(json_status == "missing"):
        add_action("rerun", "%s -jf %s -nb 3 -nbphi 2 -bc --root_file_out %s" % (factor, json_path, combined))
    else:
        add_action("blocked", "bc json is uncertain")


def compress_indexes(indexes):
    if(len(indexes) == 0):
        return ""
    parts = []
    start = indexes[0]
    prev = indexes[0]
    for index in indexes[1:]:
        if(index == prev + 1):
            prev = index
            continue
        if(start == prev):
            parts.append(str(start))
        else:
            parts.append("%d-%d" % (start, prev))
        start = index
        prev = index
    if(start == prev):
        parts.append(str(start))
    else:
        parts.append("%d-%d" % (start, prev))
    return ",".join(parts)


def main():
    data_root = "work_b"
    if(("-droot" in sys.argv) or ("--data_root" in sys.argv)):
        flag = "-droot" if("-droot" in sys.argv) else "--data_root"
        data_root = sys.argv[sys.argv.index(flag) + 1]
    folder = input_folder(data_root, True)
    recovery = os.path.join(folder, "recovery")
    print("recovery files %s" % recovery)
    print("workflow early_chain")
    frame_ready, token = groovy_and_frames(data_root, recovery)
    later_early(data_root, token, frame_ready)
    report_rc(data_root)
    report_bc(recovery)
    print("summary")
    for kind, text in ACTIONS:
        print("%s: %s" % (kind, text))
    print("Usable outputs were not marked failed because of another path. This command did not submit or cancel.")


if(__name__ == "__main__"):
    main()
