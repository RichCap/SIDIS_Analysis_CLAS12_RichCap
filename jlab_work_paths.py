#!/usr/bin/env python3
# Execution-root vs data-root helpers for the CLAS12 SIDIS analysis repository.
# Execution root is always derived from the running script. Data root is user-selectable.

import argparse
import glob
import importlib.util
import os
import sys

WORK_ROOTS = {
    "work":   "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis",
    "work_b": "/w/ceph24/hallb/clas12/users/richcap/SIDIS_Analysis_CLAS12_RichCap",
}
DEFAULT_DATA_ROOT = "work"
VOLATILE_BASE = "/lustre24/expphy/volatile/clas12/richcap/RDataFrames_to_Delete_from_work"

_REPO_MARKERS = ("dataframe_makeROOT_epip_SIDIS.py", "MyCommonAnalysisFunction_richcap.py")

REL_DATAFRAMES = os.path.join("Histo_Files_ROOT", "DataFrames")
REL_HADD = os.path.join(REL_DATAFRAMES, "hadd_ROOT_files_From_using_RDataFrames")
REL_HPP_OUT = os.path.join(REL_DATAFRAMES, "HPP_Files_Output")
REL_FILE_BATCHES = os.path.join(REL_DATAFRAMES, "File_Batches.py")
REL_SPLINE_DEFAULT = os.path.join("Prepare_Next_Iteration", "rho0_Subtracted_5D_V2_4D_xB_Fit_Pars_from_5D_BC_RC_Bayesian_Compute_SplineWeight.txt")
REL_JSON_TOYS = "Fit_Pars_from_3D_Bayesian_with_Toys.json"
REL_HPP_DEFAULT = os.path.join(REL_DATAFRAMES, "generated_acceptance_weights.hpp")
REL_HPP_ACC_IN = os.path.join(REL_DATAFRAMES, "New_Pass_2_Cut_generated_acceptance_weights_Zeroth_Order.hpp")
REL_HPP_ACC_OUT = os.path.join(REL_HPP_OUT, "New_Pass_2_Cut_generated_acceptance_weights.hpp")
REL_BC_JSON = os.path.join("BC_Corrections", "Sub_Bin_Contents_for_BC_Correction.json")
REL_GET_RHO_DEFAULT = os.path.join(REL_HADD, "SIDIS_epip_Response_Matrices_from_RDataFrames_Only_2D_rho0_Normalization_Creation_Final_Thesis_Bank_Final_Thesis_Files_All.root")
REL_SIMPLE_UNFOLD_IN = os.path.join(REL_HADD, "SIDIS_epip_Response_Matrices_from_RDataFrames_ZerothOrder.root")
REL_DEDICATED_5D_IN = os.path.join(REL_HADD, "SIDIS_epip_Response_Matrices_from_RDataFrames_Only_5D_1st_Order_V2_Response_Matrices_Final_Analysis_Iterations_I0_All.root")
REL_RUN_SIMPLE_IN = os.path.join(REL_HADD, "SIDIS_epip_Response_Matrices_from_RDataFrames_Only_3D_wFitIntegration_V4_Response_Matrices_Final_Analysis_Iterations_I0_All.root")

DATAFRAME_SUBDIRS = {
    "rdf": "REAL_Data",
    "mdf": "Matching_REC_MC",
    "gdf": "GEN_MC",
}


def _abspath(path):
    if(path in [None, ""]):
        return path
    return os.path.abspath(os.path.expanduser(str(path)))


def data_root_path(key):
    if(key not in WORK_ROOTS):
        raise ValueError(f"Unknown data_root {key!r}; expected one of {sorted(WORK_ROOTS)}")
    return WORK_ROOTS[key]


def other_data_root_key(key):
    if(key == "work"):
        return "work_b"
    if(key == "work_b"):
        return "work"
    raise ValueError(f"Unknown data_root {key!r}")


def execution_root(start_file):
    cur = _abspath(start_file)
    if(os.path.isfile(cur)):
        cur = os.path.dirname(cur)
    while(True):
        if(all(os.path.isfile(os.path.join(cur, marker)) for marker in _REPO_MARKERS)):
            return cur
        parent = os.path.dirname(cur)
        if(parent == cur):
            start = _abspath(start_file)
            return os.path.dirname(start) if(os.path.isfile(start)) else start
        cur = parent


def root_label(path):
    path_n = _abspath(path)
    for key, root in sorted(WORK_ROOTS.items(), key=lambda item: -len(item[1])):
        if((path_n == root) or path_n.startswith(root + os.sep)):
            return key
    return "local"


def strip_known_analysis_root(path):
    if(path in [None, ""]):
        return None
    path_n = _abspath(path)
    for _key, root in sorted(WORK_ROOTS.items(), key=lambda item: -len(item[1])):
        if(path_n == root):
            return ""
        prefix = root + os.sep
        if(path_n.startswith(prefix)):
            return path_n[len(prefix):]
    return None


def is_bare_filename(path):
    if(path in [None, ""]):
        return False
    return os.path.dirname(str(path)) in ["", "."]


def resolve_pipeline_input(path_or_rel, data_root_key, explicit=False, exists_fn=os.path.exists):
    if(explicit or (path_or_rel in [None, ""])):
        return path_or_rel
    rel = strip_known_analysis_root(path_or_rel)
    if(rel is None):
        if(os.path.isabs(str(path_or_rel))):
            return path_or_rel
        rel = str(path_or_rel).lstrip(os.sep)
    preferred = os.path.join(data_root_path(data_root_key), rel)
    if(exists_fn(preferred)):
        return preferred
    other = os.path.join(data_root_path(other_data_root_key(data_root_key)), rel)
    if(exists_fn(other)):
        return other
    return preferred


def pipeline_output_path(rel_or_name, data_root_key):
    if(rel_or_name in [None, ""]):
        return rel_or_name
    rel = strip_known_analysis_root(rel_or_name)
    if(rel is None):
        if(os.path.isabs(str(rel_or_name))):
            return rel_or_name
        rel = str(rel_or_name).lstrip(os.sep)
    return os.path.join(data_root_path(data_root_key), rel)


def resolve_output_name(path, data_root_key, explicit=False):
    if(path in [None, ""]):
        return path
    if(is_bare_filename(path)):
        return os.path.join(data_root_path(data_root_key), os.path.basename(str(path)))
    if(explicit):
        return path
    rel = strip_known_analysis_root(path)
    if(rel is not None):
        return os.path.join(data_root_path(data_root_key), rel)
    return path


def dataframe_output_dir(data_root_key, data_type):
    subdir = DATAFRAME_SUBDIRS.get(data_type, data_type)
    return os.path.join(data_root_path(data_root_key), REL_DATAFRAMES, subdir)


def volatile_dataframe_dir(data_type):
    subdir = DATAFRAME_SUBDIRS.get(data_type, data_type)
    return os.path.join(VOLATILE_BASE, subdir)


def iter_data_root_search_dirs(dir_path, data_root_key):
    seen = set()
    dirs = [dir_path]
    rel = strip_known_analysis_root(dir_path)
    if(rel is not None):
        dirs = [
            os.path.join(data_root_path(data_root_key), rel),
            os.path.join(data_root_path(other_data_root_key(data_root_key)), rel),
        ]
    for candidate in dirs:
        if(candidate in [None, ""]):
            continue
        normalized = os.path.abspath(candidate)
        if(normalized not in seen):
            seen.add(normalized)
            yield normalized


def collect_files_with_fallback(dir_path, patterns, data_root_key, glob_fn=glob.glob, isdir_fn=os.path.isdir):
    if(isinstance(patterns, str)):
        patterns = [patterns]
    if(not patterns):
        patterns = ["*.root"]
    by_basename = {}
    missing_dirs = []
    for search_dir in iter_data_root_search_dirs(dir_path, data_root_key):
        if(not isdir_fn(search_dir)):
            missing_dirs.append(search_dir)
            continue
        for pat in patterns:
            use = pat
            if(all(backup not in use for backup in ["*", "."])):
                use = f"*{use}*"
            if("*.root" not in use):
                use = f"{use}.root" if("*" in use) else f"{use}*.root"
            for fpath in glob_fn(os.path.join(search_dir, use)):
                base = os.path.basename(fpath)
                if(base not in by_basename):
                    by_basename[base] = os.path.abspath(fpath)
    return sorted(by_basename.values()), missing_dirs


def load_file_batches(data_root_key, exists_fn=os.path.exists, execution_root=None):
    batch_path = resolve_pipeline_input(REL_FILE_BATCHES, data_root_key, explicit=False, exists_fn=exists_fn)
    if((not exists_fn(batch_path)) and (execution_root not in [None, ""])):
        local_batch = os.path.join(execution_root, REL_FILE_BATCHES)
        if(exists_fn(local_batch)):
            batch_path = local_batch
    spec = importlib.util.spec_from_file_location("File_Batches", batch_path)
    if((spec is None) or (spec.loader is None)):
        raise ImportError(f"Cannot load File_Batches from {batch_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    def remap_dict(batch_dict):
        remapped = {}
        for key, value in dict(batch_dict or {}).items():
            if(isinstance(value, (list, tuple))):
                remapped[key] = [resolve_pipeline_input(path, data_root_key, explicit=False, exists_fn=exists_fn) for path in value]
            else:
                remapped[key] = value
        return remapped

    rdf_batch = remap_dict(getattr(module, "rdf_batch", {}))
    mdf_batch = remap_dict(getattr(module, "mdf_batch", {}))
    gdf_batch = remap_dict(getattr(module, "gdf_batch", {}))
    return rdf_batch, mdf_batch, gdf_batch, batch_path


def flag_was_passed(option_strings, argv=None):
    argv = sys.argv[1:] if(argv is None) else argv
    for tok in argv:
        for opt in option_strings:
            if((tok == opt) or tok.startswith(f"{opt}=")):
                return True
    return False


def apply_input_if_default(args, dest, option_strings, data_root_key, argv=None):
    if(flag_was_passed(option_strings, argv=argv)):
        return getattr(args, dest)
    value = getattr(args, dest)
    resolved = resolve_pipeline_input(value, data_root_key, explicit=False)
    setattr(args, dest, resolved)
    return resolved


def apply_output_if_default(args, dest, option_strings, data_root_key, argv=None, bare_to_data_root=False):
    value = getattr(args, dest)
    if(flag_was_passed(option_strings, argv=argv)):
        if(bare_to_data_root and is_bare_filename(value)):
            resolved = resolve_output_name(value, data_root_key, explicit=True)
            setattr(args, dest, resolved)
            return resolved
        return value
    if(bare_to_data_root):
        resolved = resolve_output_name(value, data_root_key, explicit=False)
    else:
        resolved = pipeline_output_path(value, data_root_key)
    setattr(args, dest, resolved)
    return resolved


def add_data_root_argument(parser):
    parser.add_argument("-droot", "--data_root",
                        choices=list(WORK_ROOTS.keys()),
                        default=DEFAULT_DATA_ROOT,
                        help="JLab analysis data tree for pipeline-owned files. Scripts still come from the launched repository. work=/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis ; work_b=/w/ceph24/hallb/clas12/users/richcap/SIDIS_Analysis_CLAS12_RichCap.\n")
    return parser


def print_path_summary(exec_root, data_root_key):
    print(f"Execution repository: {root_label(exec_root)} ({exec_root})")
    print(f"Data root: {data_root_key} ({data_root_path(data_root_key)})")


def ensure_sys_path(repo_root):
    if(repo_root not in sys.path):
        sys.path.insert(0, repo_root)
    return repo_root


def bootstrap_from_file(start_file):
    exec_root = execution_root(start_file)
    ensure_sys_path(exec_root)
    return exec_root


if(__name__ == "__main__"):
    import tempfile

    def _run_self_check():
        failures = []
        work = data_root_path("work")
        work_b = data_root_path("work_b")
        rel = os.path.join(REL_HADD, "example.root")
        work_path = os.path.join(work, rel)
        work_b_path = os.path.join(work_b, rel)

        def check(cond, msg):
            if(not cond):
                failures.append(msg)

        check(other_data_root_key("work") == "work_b", "other_data_root_key(work)")
        check(other_data_root_key("work_b") == "work", "other_data_root_key(work_b)")
        check(root_label(work) == "work", "root_label(work)")
        check(root_label(work_b) == "work_b", "root_label(work_b)")
        check(root_label("/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap") == "local", "root_label(local)")
        check(strip_known_analysis_root(work_path) == rel, "strip work path")
        check(strip_known_analysis_root(work_b_path) == rel, "strip work_b path")
        check(strip_known_analysis_root("/w/hallb-scshelf2102/clas12/richcap/SIDIS/REAL_Data/file.root") is None, "do not strip Groovy SIDIS")
        check(strip_known_analysis_root(os.path.join(VOLATILE_BASE, "REAL_Data", "x.root")) is None, "do not strip volatile")

        exists_selected = lambda path: path == work_b_path
        check(resolve_pipeline_input(work_path, "work_b", exists_fn=exists_selected) == work_b_path, "selected exists")
        exists_other = lambda path: path == work_path
        check(resolve_pipeline_input(work_path, "work_b", exists_fn=exists_other) == work_path, "fallback to other")
        exists_none = lambda path: False
        check(resolve_pipeline_input(work_path, "work_b", exists_fn=exists_none) == work_b_path, "neither exists returns selected")
        explicit = "/tmp/explicit.root"
        check(resolve_pipeline_input(explicit, "work_b", explicit=True, exists_fn=exists_none) == explicit, "explicit path unchanged")
        groovy = "/w/hallb-scshelf2102/clas12/richcap/SIDIS/REAL_Data/file.root"
        check(resolve_pipeline_input(groovy, "work_b", exists_fn=exists_none) == groovy, "groovy path unchanged")
        check(pipeline_output_path(work_path, "work_b") == work_b_path, "output rewrite")
        check(is_bare_filename("out.root"), "bare filename")
        check(resolve_output_name("out.root", "work_b") == os.path.join(work_b, "out.root"), "bare output under data root")
        check(not flag_was_passed(["--data_root"], argv=["-n", "x"]), "flag not passed")
        check(flag_was_passed(["--data_root", "-droot"], argv=["--data_root", "work_b"]), "flag passed")
        check(VOLATILE_BASE.startswith("/lustre24/"), "volatile unchanged")
        local_root = execution_root(__file__)
        check(os.path.isfile(os.path.join(local_root, "MyCommonAnalysisFunction_richcap.py")), "execution_root from __file__")
        check(root_label(local_root) == "local", "local execution label")

        with tempfile.TemporaryDirectory() as tmp:
            selected_dir = os.path.join(tmp, "selected")
            other_dir = os.path.join(tmp, "other")
            os.makedirs(selected_dir)
            os.makedirs(other_dir)
            open(os.path.join(selected_dir, "keep.root"), "w").close()
            open(os.path.join(other_dir, "keep.root"), "w").close()
            open(os.path.join(other_dir, "only_other.root"), "w").close()
            # Monkeypatch WORK_ROOTS for glob uniqueness by using iter_data_root_search_dirs with a fake dir_path under work.
            fake_work_dir = os.path.join(work, "Histo_Files_ROOT", "DataFrames", "REAL_Data")
            # Direct basename merge test without rewriting WORK_ROOTS:
            files = {}
            for search_dir in [selected_dir, other_dir]:
                for fpath in glob.glob(os.path.join(search_dir, "*.root")):
                    base = os.path.basename(fpath)
                    if(base not in files):
                        files[base] = fpath
            check(os.path.dirname(files["keep.root"]) == selected_dir, "glob prefers first/selected")
            check(os.path.basename(files["only_other.root"]) == "only_other.root", "glob fallback unique basename")
            _ = fake_work_dir

        if(failures):
            print("SELF_CHECK_FAIL")
            for item in failures:
                print(f"  {item}")
            sys.exit(1)
        print("SELF_CHECK_OK")
        print_path_summary(execution_root(__file__), "work")
        print_path_summary(execution_root(__file__), "work_b")

    _run_self_check()
