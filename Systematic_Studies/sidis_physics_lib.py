# Planning, comparison, and artifact helpers for the SIDIS physics-results workflow.
# This module does not unfold, fit histograms, start EvGen, or submit jobs.

import datetime
import json
import math
import os
import re
import shutil
import sys

ANALYSIS_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if(ANALYSIS_ROOT not in sys.path):
    sys.path.insert(0, ANALYSIS_ROOT)

from Campaign.aggregate_systematics import combine_sources, reduce_source, variation_record
from Campaign.registry import Registry

UNFOLDED_DIR = os.path.join(
    ANALYSIS_ROOT,
    "SIDIS_Campaign",
    "systematics",
    "systematics_3d_complete_20261029",
    "unfolded",
)
SPLINE_NOMINAL_NAME = "Sys3D_nominal_only_20261030_inherited_Spline.root"
UNWEIGHTED_NOMINAL_NAME = "Sys3D_nominal_only_20261030_inherited_Unweighted.root"
UNWEIGHTED_5D_NAME = "unfolded_5d_cpp_covariance.root"
RC_FACTOR_ROOT = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/Running_EvGen_richcap/Run_Large_Files_For_Iterative_Corrections/Comparison_With_Unfolding/build_EvGen_PerFile_Hists_Runtime_ifarm_rc/merged_outputs/RC_Factors_ifarm_rc.root"
SPLINE_5D_PATH = os.path.join(ANALYSIS_ROOT, "SIDIS_Campaign", "systematics", "nominal_5d_spline_20261030", "unfolded", "Unfolded_5D_inherited_Spline_WSpline.root")
ITERATION_MISMATCH_BINS = [1, 5]
ACCSPLINE_VARIATION_NAME = "Sys3D_nominal_only_20261030_inherited_AccSpline.root"
ACC_VARIATION_NAME = "Sys3D_nominal_only_20261030_inherited_Acc.root"
METHOD_BRANCH_SOURCES = {
    "BayesMinus1": ("bayes_iteration", "BayesMinus1", "independent"),
    "BayesPlus1": ("bayes_iteration", "BayesPlus1", "independent"),
    "Acc015": ("acceptance_threshold", "Acc015", "independent"),
    "Acc025": ("acceptance_threshold", "Acc025", "independent"),
    "Phi12": ("phi_bins", "Phi12", "independent"),
    "NoRho0": ("rho0_subtraction", "NoRho0", "independent"),
}
BRANCH_SUFFIXES = [
    "AcceptanceWeightVariation",
    "BayesMinus1",
    "BayesPlus1",
    "Acc015",
    "Acc025",
    "Phi12",
    "NoRho0",
    "BinByBin",
    "inherited",
]
PAIR_SOURCES = {
    "dcfid_loose_el": ("dcfid_el", "loose"),
    "dcfid_tight_el": ("dcfid_el", "tight"),
    "dcfid_loose_pip": ("dcfid_pip", "loose"),
    "dcfid_tight_pip": ("dcfid_pip", "tight"),
    "dcv_loose_el": ("dcv_el", "loose"),
    "dcv_tight_el": ("dcv_el", "tight"),
    "dvz_loose_pip": ("dvz_pip", "loose"),
    "dvz_tight_pip": ("dvz_pip", "tight"),
    "pcalvol_loose": ("pcalvol", "loose"),
    "pcalvol_tight": ("pcalvol", "tight"),
    "ecband_loose_el": ("ecband_el", "loose"),
    "ecband_tight_el": ("ecband_el", "tight"),
    "ecthr_loose_el": ("ecthr_el", "loose"),
    "ecthr_tight_el": ("ecthr_el", "tight"),
    "dcfidref_loose_el": ("dcfidref_el", "loose"),
    "dcfidref_tight_el": ("dcfidref_el", "tight"),
    "pip_testdc_loose": ("pion_dc_extra", "loose"),
    "pip_testdc_tight": ("pion_dc_extra", "tight"),
}
SINGLE_SOURCES = [
    "chi2_strict_pip",
    "no_pip_testdc",
    "no_sector_pcal",
    "no_valerii_knockout",
    "noSmear",
]
PARAMETERS = ["A", "B", "C"]
FIT_FIELDS = {"A": "Fit_Par_A", "B": "Fit_Par_B", "C": "Fit_Par_C"}
BC_NOMINAL_COUNTS = {"q2": 3, "y": 3, "z": 3, "pt": 3, "phi": 5}
BC_SENSITIVITY = {
    "q2": [3, 5, 7],
    "y": [3, 5, 7],
    "z": [3, 5, 7],
    "pt": [3, 5, 7],
    "phi": [5, 7, 9],
}
LOCAL_CROSS_SECTION = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/Running_EvGen_richcap/sidis/build/example/cross_section"
LOCAL_RC_SCAN = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/Running_EvGen_richcap/RC_Cross_Section_Scan_Outputs_Final.root"
BC_DIR = os.path.join(ANALYSIS_ROOT, "BC_Corrections")
BC_EVENT_JSON = os.path.join(BC_DIR, "Sub_Bin_Contents_for_BC_Correction_with_Binned_sbatch_from_10_26_2026.json")
BC_EVENT_ROOT = os.path.join(BC_DIR, "Sub_Bin_Contents_for_BC_Correction_with_Binned_sbatch_from_10_26_2026.root")
SPLINE_PREFIX = os.path.join(ANALYSIS_ROOT, "Prepare_Next_Iteration", "acc020_3D_BC_RC_rawA_4D_xB_Fit_Pars_from_3D_BC_RC_Bayesian")
FIT_SCRIPT = os.path.join(ANALYSIS_ROOT, "Simple_RooUnfold_SelfContained.py")
MOSAIC_SCRIPT = os.path.join(ANALYSIS_ROOT, "Full_Moment_Plots_Creation_From_JSON.py")
PHI_SCRIPT = os.path.join(ANALYSIS_ROOT, "plot_consolidated_phi_h_figures.py")
INJECTION_SPLINE_TXT = SPLINE_PREFIX + "_Compute_SplineWeight.txt"


def file_fingerprint(path):
    if((path is None) or (not os.path.isfile(path))):
        return {"size": None, "mtime": None}
    stat = os.stat(path)
    return {"size": int(stat.st_size), "mtime": int(stat.st_mtime)}


def path_state(path, searched):
    if(path in [None, ""]):
        if(searched):
            return "absent_on_disk"
        return "needs_configuration"
    if(os.path.isfile(path)):
        return "verified"
    return "absent_on_disk"


class PhysicsRegistry(Registry):
    # Same append-only records as Campaign.registry.Registry, rooted at the workflow output.
    def __init__(self, output_dir):
        self.root       = os.path.abspath(output_dir)
        self.reg_dir    = os.path.join(self.root, "registry")
        self.jsonl      = os.path.join(self.reg_dir, "artifacts.jsonl")
        self.state_path = os.path.join(self.reg_dir, "state.json")
        os.makedirs(self.reg_dir, exist_ok=True)
        if(not os.path.isfile(self.state_path)):
            self.write_state({})

    def find_completed(self, wanted):
        found = None
        for record in self.records():
            if(record.get("status") not in ["completed", "completed_partial"]):
                continue
            if(record.get("validation") not in ["ok", "passed", True]):
                continue
            if(self.identity_matches(record, wanted)):
                found = record
        return found

    def find_reusable(self, wanted, force):
        if(force):
            return None
        found = self.find_completed(wanted)
        if(found is None):
            return None
        for field in ["input_size", "input_mtime", "config_fingerprint"]:
            if(field not in wanted):
                continue
            if(str(found.get(field)) != str(wanted.get(field))):
                return None
        return found


def weight_pair_allowed(source, nominal_tag, variation_tag):
    nominal_tag   = "" if(nominal_tag in [None]) else str(nominal_tag)
    variation_tag = "" if(variation_tag in [None]) else str(variation_tag)
    if(source == "acceptance_reweighting"):
        return (nominal_tag, variation_tag) in [("", "Acc"), ("Spline", "AccSpline")]
    return nominal_tag == variation_tag


def split_unfolded_name(name):
    if(not str(name).endswith(".root")):
        return None
    stem = str(name)[:-5]
    if(not stem.startswith("Sys3D_")):
        return None
    body = stem[len("Sys3D_"):]
    weight_tag = None
    for suffix, tag in [("_AccSpline", "AccSpline"), ("_Unweighted", ""), ("_Acc", "Acc"), ("_Spline", "Spline")]:
        if(body.endswith(suffix)):
            weight_tag = tag
            head = body[:-len(suffix)]
            break
    if(weight_tag is None):
        return None
    branch = None
    config_id = None
    for candidate in BRANCH_SUFFIXES:
        token = "_" + candidate
        if(head.endswith(token)):
            branch = candidate
            config_id = head[:-len(token)]
            break
    if(branch is None):
        return None
    return {"config_id": config_id, "branch": branch, "weight_tag": weight_tag, "file_name": name}


def source_for_config(config_id):
    if(config_id in PAIR_SOURCES):
        source, variation = PAIR_SOURCES[config_id]
        return source, variation, "independent"
    if(config_id in SINGLE_SOURCES):
        return config_id, config_id, "independent"
    if(config_id.startswith("eS") and config_id.endswith("o")):
        return "electron_sector", config_id, "not_combined"
    if(config_id.startswith("pipS") and config_id.endswith("o")):
        return "pion_sector", config_id, "not_combined"
    return None, None, None


def entry(role, campaign, source, variation, weight_tag, method, path, path_status, nominal_id, combine, enabled):
    return {
        "role": role,
        "campaign": campaign,
        "source": source,
        "variation": variation,
        "weight_tag": weight_tag,
        "method": method,
        "dimension": "3D",
        "path": path,
        "path_status": path_status,
        "nominal_id": nominal_id,
        "combine": combine,
        "enabled": enabled,
        "fingerprint": file_fingerprint(path),
    }


def build_manifest(unfolded_dir=None):
    folder = UNFOLDED_DIR if(unfolded_dir in [None, ""]) else unfolded_dir
    names = []
    if(os.path.isdir(folder)):
        names = sorted(os.listdir(folder))
    by_name = {}
    for name in names:
        parsed = split_unfolded_name(name)
        if(parsed is None):
            continue
        parsed["path"] = os.path.join(folder, name)
        by_name[name] = parsed

    def take(name):
        parsed = by_name.get(name)
        if(parsed is None):
            return None, "absent_on_disk"
        return parsed["path"], "verified"

    unweighted_path, unweighted_state = take(UNWEIGHTED_NOMINAL_NAME)
    spline_path, spline_state = take(SPLINE_NOMINAL_NAME)
    accspline_path, accspline_state = take(ACCSPLINE_VARIATION_NAME)
    acc_path, acc_state = take(ACC_VARIATION_NAME)
    nominals = {
        "unweighted": entry("nominal", "unweighted", "nominal", "nominal", "", "Bayesian", unweighted_path, unweighted_state, None, "not_combined", True),
        "spline": entry("nominal", "spline", "nominal", "nominal", "Spline", "Bayesian", spline_path, spline_state, None, "not_combined", True),
    }
    variations = []
    blocked_methods = []
    for name, parsed in by_name.items():
        path = parsed["path"]
        tag = parsed["weight_tag"]
        branch = parsed["branch"]
        config_id = parsed["config_id"]
        if(name in [SPLINE_NOMINAL_NAME, UNWEIGHTED_NOMINAL_NAME, ACCSPLINE_VARIATION_NAME]):
            continue
        if(branch in METHOD_BRANCH_SOURCES):
            source_name, variation_name, combine = METHOD_BRANCH_SOURCES[branch]
            if(tag == "Spline"):
                campaign = "spline"
            elif(tag == ""):
                campaign = "unweighted"
            else:
                blocked_methods.append({
                    "file_name": name,
                    "path": path,
                    "weight_tag": tag,
                    "branch": branch,
                    "eligible": False,
                    "path_status": "verified",
                    "study_state": "blocked",
                    "reason": "This weight is not the Unweighted or Spline nominal for the branch.",
                })
                continue
            variations.append(entry("method", campaign, source_name, variation_name, tag, "Bayesian", path, "verified", "nominals.%s" % campaign, combine, True))
            continue
        if(branch == "BinByBin"):
            campaign = "spline" if(tag == "Spline") else "unweighted" if(tag == "") else None
            if(campaign is None):
                continue
            nominal_id = "nominals.%s" % campaign
            variations.append(entry("method", campaign, "correction_method", "BinByBin", tag, "Bin", path, "verified", nominal_id, "independent", True))
            continue
        if(branch != "inherited"):
            continue
        if(config_id == "nominal_only_20261030"):
            continue
        source, variation, combine = source_for_config(config_id)
        if(source is None):
            continue
        if(tag == "Spline"):
            campaign = "spline"
        elif(tag == ""):
            campaign = "unweighted"
        else:
            continue
        variations.append(entry("cut", campaign, source, variation, tag, "Bayesian", path, "verified", "nominals.%s" % campaign, combine, True))
    variations.append(entry(
        "acceptance_reweighting", "spline", "acceptance_reweighting", "AccSpline", "AccSpline", "Bayesian",
        accspline_path, accspline_state, "nominals.spline", "independent", accspline_state == "verified",
    ))
    variations.append(entry(
        "acceptance_reweighting", "unweighted", "acceptance_reweighting", "Acc", "Acc", "Bayesian",
        acc_path, acc_state, "nominals.unweighted", "independent", acc_state == "verified",
    ))
    spline_files = {}
    for letter in ["A", "B", "C"]:
        pkl = "%s_Fit_Par_%s.pkl" % (SPLINE_PREFIX, letter)
        spline_files[letter] = {"path": pkl, "path_status": path_state(pkl, False)}
    txt = SPLINE_PREFIX + "_Compute_SplineWeight.txt"
    five_d_spline = SPLINE_5D_PATH
    manifest = {
        "schema_version": 1,
        "nominals": nominals,
        "variations": variations,
        "method_branches_blocked": blocked_methods,
        "comparisons": {
            "unweighted_versus_spline": {
                "role": "weight_scheme",
                "combine": "not_combined",
                "nominal_ids": ["nominals.unweighted", "nominals.spline"],
            },
        },
        "dimension": {
            "spline": {"path": five_d_spline, "path_status": path_state(five_d_spline, True), "study_state": "ready" if(os.path.isfile(five_d_spline)) else "blocked", "weight_tag": "Spline"},
            "unweighted": {"path": None, "path_status": "absent_on_disk", "study_state": "blocked", "reason": "No unweighted 5D job was scheduled."},
            "bayesian_1d": {"path": None, "path_status": "needs_configuration", "enabled": False, "study_state": "disabled"},
        },
        "radiative": {
            "study_state": "pending",
            "enabled": True,
            "execute": "inspect",
            "scan_root": {"path": LOCAL_RC_SCAN, "path_status": path_state(LOCAL_RC_SCAN, True)},
            "cross_section": {"path": LOCAL_CROSS_SECTION, "path_status": path_state(LOCAL_CROSS_SECTION, True)},
            "event_ratio_root": {"path": None, "path_status": "needs_configuration"},
        },
        "bin_centering": {
            "event_nominal": {"path": BC_EVENT_JSON, "path_status": path_state(BC_EVENT_JSON, True), "counts": BC_NOMINAL_COUNTS, "role": "event_unweighted_reference"},
            "initial_spline": {"path": None, "path_status": "needs_configuration"},
            "later_spline": {"path": None, "path_status": "needs_configuration"},
            "sensitivity": sensitivity_rows(),
            "transfer": {"prescription": "user_decision"},
            "iteration_combine": "not_combined",
        },
        "splines": {"pkl": spline_files, "compute_txt": {"path": txt, "path_status": path_state(txt, False)}},
        "run": {
            "output_dir": os.path.join(ANALYSIS_ROOT, "Systematic_Studies", "physics_campaign"),
            "campaigns": "both",
            "stages": ["resolve"],
            "max_concurrent": 2,
            "force": False,
            "spline_overlay": False,
            "tolerance": 1.0e-9,
            "uncertainty_campaign": None,
        },
    }
    return manifest


def sensitivity_rows():
    rows = []
    for variable in ["q2", "y", "z", "pt", "phi"]:
        for value in BC_SENSITIVITY[variable]:
            rows.append({
                "label": "sens_%s_%s" % (variable, value),
                "variable": variable,
                "value": value,
                "other_variables": 1,
                "path": None,
                "path_status": "absent_on_disk",
                "study_state": "blocked",
                "combine": "not_combined",
            })
    return rows


def nominal_id_for(manifest, campaign):
    nominal = manifest["nominals"][campaign]
    if(nominal["weight_tag"] == "AccSpline"):
        raise ValueError("AccSpline cannot be a nominal")
    if(nominal["path_status"] != "verified"):
        return None
    return "nominals.%s" % campaign


def fit_jobs(manifest, campaign):
    jobs = []
    nominal = manifest["nominals"][campaign]
    if(nominal["path_status"] != "verified"):
        return jobs
    if(not weight_pair_allowed("nominal", nominal["weight_tag"], nominal["weight_tag"])):
        raise ValueError("nominal weight tag is not allowed")
    jobs.append({
        "kind": "nominal",
        "campaign": campaign,
        "source": "nominal",
        "variation": "nominal",
        "weight_tag": nominal["weight_tag"],
        "nominal_tag": nominal["weight_tag"],
        "method": "Bayesian",
        "dimension": nominal.get("dimension", "3D"),
        "input_path": nominal["path"],
        "enabled": True,
        "iteration_mismatch_bins": [],
    })
    dimension_row = manifest.get("dimension", {}).get(campaign, {})
    same_weight = str(dimension_row.get("weight_tag", "")) == str(nominal["weight_tag"])
    if(dimension_row.get("study_state") == "ready" and dimension_row.get("path_status") == "verified" and same_weight):
        jobs.append({
            "kind": "variation",
            "campaign": campaign,
            "source": "dimension",
            "variation": "5D",
            "weight_tag": nominal["weight_tag"],
            "nominal_tag": nominal["weight_tag"],
            "method": "Bayesian",
            "dimension": "5D",
            "input_path": dimension_row["path"],
            "enabled": True,
            "iteration_mismatch_bins": list(dimension_row.get("iteration_mismatch_bins", [])),
        })
    for row in manifest["variations"]:
        if(row["campaign"] != campaign):
            continue
        if(row["path_status"] != "verified"):
            continue
        if(not row["enabled"]):
            continue
        if(not weight_pair_allowed(row["source"], nominal["weight_tag"], row["weight_tag"])):
            continue
        jobs.append({
            "kind": "variation",
            "campaign": campaign,
            "source": row["source"],
            "variation": row["variation"],
            "weight_tag": row["weight_tag"],
            "nominal_tag": nominal["weight_tag"],
            "method": row["method"],
            "dimension": row.get("dimension", "3D"),
            "input_path": row["path"],
            "enabled": True,
            "iteration_mismatch_bins": [],
        })
    return jobs


def shard_jobs(jobs, max_concurrent):
    count = len(jobs)
    if(count == 0):
        return []
    width = int(max_concurrent)
    if(width < 1):
        raise ValueError("max_concurrent must be at least 1")
    width = count if(count < width) else width
    shards = [[] for _index in range(width)]
    for index, job in enumerate(jobs):
        shards[index % width].append(job)
    return shards


def fit_output_root(output_dir, job):
    folder = os.path.join(output_dir, "fits", job["campaign"], job["source"], str(job["variation"]))
    return os.path.join(folder, "fit_copy.root")


def fit_config_fingerprint(job):
    if(job.get("method") == "Bin"):
        return "3D|Bin|MultiDim_3D_Histo"
    return job.get("dimension", "3D")


def expected_fit_key(job):
    if(job.get("dimension") == "5D"):
        return "Fit_Pars_from_5D_Bayesian"
    if(job.get("method") == "Bin"):
        return "Fit_Pars_from_3D_Bin"
    return "Fit_Pars_from_3D_Bayesian"


def plan_fit_command(job, copy_root, json_out, init_file):
    if(os.path.abspath(copy_root) == os.path.abspath(job["input_path"])):
        raise ValueError("fit output must be a copy, not the input ROOT file")
    if(not weight_pair_allowed(job["source"] if(job["kind"] == "variation") else "nominal", job["nominal_tag"], job["weight_tag"])):
        raise ValueError("weight tags are not an allowed pair")
    cmd = [
        FIT_SCRIPT,
        "--root", copy_root,
        "--Use_TTree", "--fit", "--remake_fit", "--smear", "--save_json",
        "--json_name", json_out,
        "--fit_error_source", "histogram",
    ]
    dimension = job.get("dimension", "3D")
    if(job["method"] == "Bayesian" and dimension == "5D"):
        cmd.extend(["--unfolding_5D", "--fit_corrections", "Bayesian"])
    elif(job["method"] == "Bayesian"):
        cmd.extend(["--unfolding_3D", "--fit_corrections", "Bayesian"])
    elif(job["method"] == "Bin"):
        cmd.extend(["--unfolding_3D", "--Unfold_Methods", "(Bin)"])
    else:
        raise ValueError("unknown fit method %s" % job["method"])
    if(init_file not in [None, ""]):
        cmd.extend(["--fit_init_file", init_file])
    for token in cmd:
        if(token in ["--Apply_RC", "--Apply_BC", "-rc", "-bc"]):
            raise ValueError("correction flags are not part of the fit command")
    return cmd


def copy_input_for_fit(job, output_dir):
    dest = fit_output_root(output_dir, job)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    temporary = dest + ".partial"
    shutil.copyfile(job["input_path"], temporary)
    os.replace(temporary, dest)
    return dest


def bin_key(q2y_bin, zpt_bin):
    return "(Q2_y_Bin_%s)-(z_pT_Bin_%s)" % (q2y_bin, zpt_bin)


def write_init_module(nominal_cells, limits_by_key, out_path):
    # nominal_cells: bin key -> {Fit_Par_B, Fit_Par_C}. limits_by_key keeps the existing windows.
    mapping = {}
    skipped = []
    for key, cell in nominal_cells.items():
        if(("Fit_Par_B" not in cell) or ("Fit_Par_C" not in cell)):
            skipped.append(key)
            continue
        q2y, zpt = parse_bin_key(key)
        limits = limits_by_key.get((q2y, zpt), {})
        mapping[(q2y, zpt)] = {
            "B_initial": cell["Fit_Par_B"],
            "C_initial": cell["Fit_Par_C"],
            "B_limits": limits.get("B_limits"),
            "C_limits": limits.get("C_limits"),
        }
    lines = ["special_fit_parameters_set = {"]
    for key in sorted(mapping):
        lines.append("    %r: %r," % (key, mapping[key]))
    lines.append("}")
    lines.append("")
    folder = os.path.dirname(out_path)
    if(folder):
        os.makedirs(folder, exist_ok=True)
    handle = open(out_path, "w")
    handle.write("\n".join(lines))
    handle.close()
    return {"path": out_path, "bins": len(mapping), "skipped": skipped}


def parse_bin_key(key):
    # "(Q2_y_Bin_5)-(z_pT_Bin_16)" -> ("5", "16")
    left, right = str(key).split(")-(")
    q2y = left.split("Q2_y_Bin_")[1]
    zpt = right.split("z_pT_Bin_")[1].rstrip(")")
    return q2y, zpt


def dominance_flag(systematic, statistical, tolerance):
    if(systematic is None):
        return None, "systematic_missing"
    if(statistical is None):
        return None, "fit_uncertainty_missing"
    if(statistical != statistical):
        return None, "fit_uncertainty_invalid"
    if(float(statistical) == 0.0):
        return None, "fit_uncertainty_zero"
    ratio = float(systematic) / float(statistical)
    if(abs(ratio - 1.0) <= float(tolerance)):
        return ratio, "equal_within_tolerance"
    if(ratio > 1.0):
        return ratio, "systematic_larger"
    return ratio, "fit_larger"


def scan_fit_family(root_path, fit_key):
    import ROOT
    ROOT.gROOT.SetBatch(True)
    needles = {
        "Fit_Pars_from_5D_Bayesian": "(MultiDim_5D_Histo)_(Bayesian)_",
        "Fit_Pars_from_3D_Bin": "(MultiDim_3D_Histo)_(Bin)_",
        "Fit_Pars_from_3D_RC_Bayesian": "(MultiDim_3D_Histo)_(RC_Bayesian)_",
        "Fit_Pars_from_3D_BC_RC_Bayesian": "(MultiDim_3D_Histo)_(BC_RC_Bayesian)_",
        "Fit_Pars_from_3D_Bayesian": "(MultiDim_3D_Histo)_(Bayesian)_",
    }
    needle = needles.get(fit_key, "(MultiDim_3D_Histo)_(Bayesian)_")
    handle = ROOT.TFile.Open(root_path, "READ")
    rows = []
    if((handle is None) or handle.IsZombie()):
        return rows
    for key in handle.GetListOfKeys():
        name = key.GetName()
        if(needle not in name):
            continue
        if(("Bin_All" in name) or ("z_pT_Bin_All" in name) or ("Q2_y_Bin_All" in name)):
            continue
        if(("Q2_y_Bin_" not in name) or ("z_pT_Bin_" not in name)):
            continue
        q2y = name.split("Q2_y_Bin_")[1].split(")")[0]
        zpt = name.split("z_pT_Bin_")[1].split(")")[0]
        if((not q2y.isdigit()) or (not zpt.isdigit())):
            continue
        hist = key.ReadObj()
        rows.append({
            "bin": "(Q2_y_Bin_%s)-(z_pT_Bin_%s)" % (q2y, zpt),
            "q2y": int(q2y),
            "zpt": int(zpt),
            "integral": float(hist.Integral()),
        })
    handle.Close()
    return rows


def classify_fit_coverage(expected_rows, fitted_bins):
    # expected_rows: bin, integral, q2y, zpt. Empty integrals are N/A and are not zeroes in an RMS.
    fitted_set = set(fitted_bins)
    na_rows = []
    other_rows = []
    fitted = []
    for row in expected_rows:
        record = {
            "bin": row["bin"],
            "q2y": row.get("q2y"),
            "zpt": row.get("zpt"),
            "integral": row.get("integral"),
        }
        if(float(row.get("integral", 0.0)) == 0.0):
            record["reason"] = "empty_histogram"
            record["status"] = "N/A"
            na_rows.append(record)
        elif(row["bin"] in fitted_set):
            fitted.append(row["bin"])
        else:
            record["reason"] = "missing_from_json"
            record["status"] = "other_failure"
            other_rows.append(record)
    n_fitted = len(fitted)
    n_expected = len(expected_rows)
    if(n_fitted == 0):
        status = "failed"
    elif((len(na_rows) + len(other_rows)) == 0):
        status = "completed"
    else:
        status = "completed_partial"
    return {
        "status": status,
        "expected": n_expected,
        "fitted": n_fitted,
        "na": len(na_rows),
        "other_failure": len(other_rows),
        "na_bins": na_rows,
        "other_bins": other_rows,
        "na_fraction": (float(len(na_rows)) / float(n_expected)) if(n_expected > 0) else None,
    }


def shifts_for_rms(values_by_bin, excluded_bins):
    # Drop N/A and other missing bins. Do not replace them with zero.
    shifts = []
    excluded = set(excluded_bins)
    for bin_name, value in values_by_bin.items():
        if(bin_name in excluded):
            continue
        if(value is None):
            continue
        shifts.append(float(value))
    return shifts


def nominal_stage_products(output_dir, campaign):
    return {
        "acceptance": {
            "family": "unfolded_ac",
            "fit_key": "Fit_Pars_from_3D_Bayesian",
            "root": None,
            "fit": os.path.join(output_dir, "fits", campaign, "nominal", "nominal", "fit.json"),
        },
        "rc": {
            "family": "unfolded_rc",
            "fit_key": "Fit_Pars_from_3D_RC_Bayesian",
            "root": os.path.join(output_dir, "corrected", campaign, "rc", "corrected.root"),
            "fit": os.path.join(output_dir, "corrected", campaign, "rc", "fit.json"),
        },
        "bc": {
            "family": "unfolded_bc",
            "fit_key": "Fit_Pars_from_3D_BC_RC_Bayesian",
            "root": os.path.join(output_dir, "corrected", campaign, "bc", "corrected.root"),
            "fit": os.path.join(output_dir, "corrected", campaign, "bc", "fit.json"),
        },
    }


def correction_fingerprint(stage, paths):
    parts = [str(stage)]
    for path in paths:
        fingerprint = file_fingerprint(path)
        parts.append("%s:%s" % (fingerprint["size"], fingerprint["mtime"]))
    return "|".join(parts)


def nominal_rc_ready(event_ratio_status, radiative_study_state):
    # A pending alternative radiative study does not block the nominal RC file.
    if(radiative_study_state == "pending"):
        return event_ratio_status == "verified"
    return event_ratio_status == "verified"


def collect_bin_shifts(nominal_cells, variation_cells):
    # Returns per-bin parameter records. A bin missing on either side is reported and omitted from RMS.
    rows = []
    missing = []
    keys = sorted(set(list(nominal_cells) + list(variation_cells)))
    for key in keys:
        if((key not in nominal_cells) or (key not in variation_cells)):
            missing.append(key)
            continue
        observables = {}
        for parameter in PARAMETERS:
            field = FIT_FIELDS[parameter]
            err_field = field + "_ERR"
            if((field not in nominal_cells[key]) or (field not in variation_cells[key])):
                missing.append(key)
                observables = None
                break
            observables[parameter] = {
                "nominal": nominal_cells[key][field],
                "variation": variation_cells[key][field],
                "stat_nominal": nominal_cells[key].get(err_field),
            }
        if(observables is None):
            continue
        rows.append({"bin": key, "observables": observables})
    return rows, missing


def rms_for_source(records_for_source):
    # records_for_source: list of variation_record() outputs for one source.
    return reduce_source(records_for_source, "rms")


def stat_from_group(group, parameter):
    for record in group:
        values = record["observables"].get(parameter)
        if((values is None) or (values.get("stat_nominal") is None)):
            continue
        return values.get("stat_nominal")
    return None


def aggregate_campaign(groups_by_source, combine_by_source, tolerance):
    # groups_by_source[source][bin] is a list of variation_record objects.
    # Quadrature uses only sources marked independent. not_combined stays in the source table.
    source_tables = {}
    groups_by_bin = {}
    for source, by_bin in groups_by_source.items():
        for bin_name, group in by_bin.items():
            reduced = rms_for_source(group)
            for parameter in PARAMETERS:
                if(parameter in reduced):
                    reduced[parameter]["stat_nominal"] = stat_from_group(group, parameter)
            source_tables.setdefault(source, {})[bin_name] = reduced
            groups_by_bin.setdefault(bin_name, {})[source] = reduced
    totals = {}
    diagnostics = []
    for bin_name, sources in groups_by_bin.items():
        independent = {}
        for source, reduced in sources.items():
            if(not source_enters_quadrature(source, combine_by_source)):
                continue
            independent[source] = {name: values for name, values in reduced.items() if(name != "_method")}
        if(len(independent) == 0):
            totals[bin_name] = {parameter: {"up": None, "down": None} for parameter in PARAMETERS}
        else:
            totals[bin_name] = combine_sources(independent, "quadrature")
        stat_by_parameter = {}
        for parameter in PARAMETERS:
            for reduced in sources.values():
                piece = reduced.get(parameter)
                if((piece is not None) and (piece.get("stat_nominal") is not None)):
                    stat_by_parameter[parameter] = piece.get("stat_nominal")
                    break
        for parameter in PARAMETERS:
            stat = stat_by_parameter.get(parameter)
            total_value = totals[bin_name].get(parameter, {}).get("up")
            ratio, flag = dominance_flag(total_value, stat, tolerance)
            diagnostics.append({
                "bin": bin_name,
                "parameter": parameter,
                "R_total": ratio,
                "flag": flag,
                "systematic": total_value,
                "statistical": stat,
            })
            for source, reduced in sources.items():
                piece = reduced.get(parameter)
                if(piece is None):
                    continue
                source_ratio, source_flag = dominance_flag(piece.get("up"), stat, tolerance)
                diagnostics.append({
                    "bin": bin_name,
                    "parameter": parameter,
                    "source": source,
                    "R_source": source_ratio,
                    "flag": source_flag,
                    "systematic": piece.get("up"),
                    "statistical": stat,
                })
    return {"sources": source_tables, "totals": totals, "diagnostics": diagnostics}


def variation_bin_record(source, variation, bin_name, observables):
    record = variation_record(source, variation, observables)
    record["bin"] = bin_name
    # Keep the statistical error beside the RMS result. reduce_source does not copy it.
    for parameter, values in record["observables"].items():
        values["stat_nominal"] = observables[parameter].get("stat_nominal")
    return record


def attach_stat_to_reduced(reduced, stat_by_parameter):
    for parameter, stat in stat_by_parameter.items():
        if(parameter in reduced):
            reduced[parameter]["stat_nominal"] = stat
    return reduced


def scale_isolated(value, error, scale):
    scale = float(scale)
    if(scale == 0.0):
        raise ValueError("zero normalization scale")
    return float(value) / scale, float(error) / scale


def normalize_campaign_copy(cells, error_mode, scale_by_bin):
    # error_mode is "statistical" or "systematic". Central values are copied unchanged before the scale.
    # The scale is the existing Cross_Section_Normalization product. It is not given its own uncertainty.
    output = {"normalization_status": "applied", "error_mode": error_mode, "cells": {}, "unassigned_factor_uncertainty": True}
    for key, cell in cells.items():
        scale = scale_by_bin[key]
        updated = {}
        for parameter, field in FIT_FIELDS.items():
            err_field = field + "_ERR"
            sys_field = field + "_SYS"
            central = cell[field]
            if(error_mode == "statistical"):
                error = cell[err_field]
            elif(error_mode == "systematic"):
                if(sys_field not in cell):
                    raise ValueError("missing %s" % sys_field)
                error = cell[sys_field]
            else:
                raise ValueError("unknown error mode")
            if(parameter == "A"):
                scaled_central, scaled_error = scale_isolated(central, error, scale)
            else:
                scaled_central, scaled_error = float(central), float(error)
            updated[field] = scaled_central
            if(error_mode == "statistical"):
                updated[err_field] = scaled_error
            else:
                updated[sys_field] = scaled_error
        if(error_mode == "statistical"):
            for parameter, field in FIT_FIELDS.items():
                sys_field = field + "_SYS"
                if(sys_field in cell):
                    updated[sys_field] = cell[sys_field]
        else:
            for parameter, field in FIT_FIELDS.items():
                err_field = field + "_ERR"
                updated[err_field] = cell[err_field]
        output["cells"][key] = updated
    return output


def merge_normalized(stat_copy, sys_copy):
    if(stat_copy["normalization_status"] != "applied"):
        raise ValueError("statistical copy is not normalized")
    if(sys_copy["normalization_status"] != "applied"):
        raise ValueError("systematic copy is not normalized")
    merged = {"normalization_status": "applied", "cells": {}, "unassigned_factor_uncertainty": True}
    for key, stat_cell in stat_copy["cells"].items():
        sys_cell = sys_copy["cells"][key]
        if(stat_cell["Fit_Par_A"] != sys_cell["Fit_Par_A"]):
            raise ValueError("normalization changed the A central value across channels")
        cell = {}
        for parameter, field in FIT_FIELDS.items():
            cell[field] = stat_cell[field]
            cell[field + "_ERR"] = stat_cell[field + "_ERR"]
            cell[field + "_SYS"] = sys_cell[field + "_SYS"]
        merged["cells"][key] = cell
    return merged


def missing_uncertainty_fields(artifact, suffix):
    cells = artifact.get("cells")
    if((cells is None) and os.path.isfile(str(artifact.get("path", "")))):
        handle = open(artifact["path"])
        payload = json.load(handle)
        handle.close()
        for key, value in payload.items():
            if(isinstance(value, dict) and str(key).startswith("Fit_")):
                cells = value
                break
    if(not isinstance(cells, dict)):
        return ["unreadable"]
    missing = []
    for bin_name, cell in cells.items():
        if(not isinstance(cell, dict)):
            missing.append(bin_name)
            continue
        for field in FIT_FIELDS.values():
            if((field + suffix) not in cell):
                missing.append(bin_name)
                break
    return missing


def mosaic_command(artifact, spline_overlay, spline_prefix, campaign, x_mode="z", uncertainty="statistical"):
    if(artifact.get("normalization_status") != "applied"):
        raise ValueError("mosaic requires normalization_status applied")
    reject_stale_normalized_artifact(artifact)
    if(uncertainty not in ["statistical", "systematic"]):
        raise ValueError("unknown uncertainty channel")
    if(x_mode not in ["z", "pt", "pt2"]):
        raise ValueError("unknown x mode")
    if(uncertainty == "systematic"):
        missing = missing_uncertainty_fields(artifact, "_SYS")
        if(len(missing) > 0):
            raise ValueError("systematic mosaic is missing _SYS entries")
    err_suffix = "_ERR" if(uncertainty == "statistical") else "_SYS"
    cmd = [
        MOSAIC_SCRIPT,
        "--json_file", artifact["path"],
        "--formats", "pdf",
        "--y_pars", "Fit_Par_A", "Fit_Par_B", "Fit_Par_C",
        "--err_suffix", err_suffix,
        "--draw_with_log_A",
        "--pad_label_mode", "bin_Q2y",
        "--draw_legends",
        "--title_text", "%s uncertainties" % uncertainty,
        "--name", "sidis_mosaic_%s_%s_%s" % (campaign, x_mode, uncertainty),
    ]
    if(x_mode == "pt2"):
        cmd.extend(["--x_mode", "pt", "--pT2"])
    else:
        cmd.extend(["--x_mode", x_mode])
    if(spline_overlay):
        cmd.extend(["--spline_prefix", spline_prefix, "--dimension_mode", "4D_xB"])
    for token in cmd:
        if(token in ["--apply_A_corr", "-cs", "-cs_A", "--sys_err_suffix"]):
            raise ValueError("mosaic must not apply A0 normalization or mix error channels")
    return cmd


def mosaic_command_set(artifact, spline_overlay, spline_prefix, campaign):
    commands = []
    for x_mode in ["z", "pt", "pt2"]:
        for uncertainty in ["statistical", "systematic"]:
            commands.append(mosaic_command(artifact, spline_overlay, spline_prefix, campaign, x_mode, uncertainty))
    return commands


def phi_figure_command(family, output_dir, root_path, fit_json, dry_run):
    if(family not in ["unfolded_ac", "unfolded_rc", "unfolded_bc"]):
        raise ValueError("family is outside the physics-results phi_h set")
    cmd = [PHI_SCRIPT, "-f", family, "-o", output_dir]
    if(family == "unfolded_ac"):
        cmd.extend(["-u3d", root_path, "-fit", fit_json])
    elif(family == "unfolded_rc"):
        cmd.extend(["--root_unfolded_rc", root_path, "--fit_unfolded_rc", fit_json])
    else:
        cmd.extend(["--root_unfolded_bc", root_path, "--fit_unfolded_bc", fit_json])
    if(dry_run):
        cmd.append("-n")
    return cmd


def radiative_report(scan_path=None, cross_section_path=None, event_ratio_path=None):
    scan_path = LOCAL_RC_SCAN if(scan_path is None) else scan_path
    cross_section_path = LOCAL_CROSS_SECTION if(cross_section_path is None) else cross_section_path
    return {
        "study_state": "pending",
        "systematic": None,
        "scan_root": {"path": scan_path, "path_status": path_state(scan_path, True)},
        "cross_section": {"path": cross_section_path, "path_status": path_state(cross_section_path, True)},
        "event_ratio_root": {
            "path": event_ratio_path,
            "path_status": "needs_configuration" if(event_ratio_path in [None, ""]) else path_state(event_ratio_path, True),
        },
        "note": "No radiative systematic value is calculated. The nominal correction remains the event-ratio division.",
    }


def bin_centering_report(event_meta, initial_path, later_path):
    counts_ok = True
    if(event_meta is None):
        counts_ok = False
    else:
        for key, value in BC_NOMINAL_COUNTS.items():
            meta_key = "num_sub_bins_%s" % ("pt" if(key == "pt") else key)
            if(key == "pt"):
                meta_key = "num_sub_bins_pt"
            if(int(event_meta.get(meta_key, -1)) != value):
                counts_ok = False
    method = {
        "kind": "estimated_transfer",
        "reference": "event_unweighted",
        "alternative": "initial_spline",
        "transfer_prescription": "user_decision",
        "combine": "not_combined",
        "study_state": "blocked" if(initial_path in [None, ""]) else "ready",
        "systematic": None,
    }
    iteration = {
        "combine": "not_combined",
        "study_state": "blocked" if((initial_path in [None, ""]) or (later_path in [None, ""])) else "ready",
        "systematic": None,
    }
    return {
        "event_counts_match": counts_ok,
        "method": method,
        "iteration": iteration,
        "subdivision": {
            "campaign": "unweighted",
            "combine": "independent",
            "variables": 5,
            "variations_each": 3,
            "pooled": "rms_of_all_15",
            "study_state": "awaiting_observable_shifts",
            "systematic": None,
            "spline_transfer": "user_decision",
        },
        "injection_spline": injection_spline_record(),
        "updated_spline": {
            "path": None,
            "path_status": "needs_configuration",
            "study_state": "blocked",
            "reason": "No configuration names a spline file written after the weighted unfold and its refit.",
        },
        "evgen_bin_centering": {"implemented": False, "study_state": "deferred"},
        "sensitivity_blocked": 0,
    }


def weighted_line_fit(points):
    # points: list of {x, y, err}. Ordinary weighted least squares, used only to show that errors can change the slope.
    weight_sum = 0.0
    wx = 0.0
    wy = 0.0
    wxx = 0.0
    wxy = 0.0
    for point in points:
        err = float(point["err"])
        if(err == 0.0):
            raise ValueError("zero error")
        weight = 1.0 / (err * err)
        x_value = float(point["x"])
        y_value = float(point["y"])
        weight_sum += weight
        wx += weight * x_value
        wy += weight * y_value
        wxx += weight * x_value * x_value
        wxy += weight * x_value * y_value
    denom = (weight_sum * wxx) - (wx * wx)
    if(denom == 0.0):
        raise ValueError("degenerate fit")
    slope = ((weight_sum * wxy) - (wx * wy)) / denom
    intercept = ((wy * wxx) - (wx * wxy)) / denom
    return {"slope": slope, "intercept": intercept}


def sync_corrected_unfold_inputs(manifest):
    # Pick up corrected same-weight files without replacing a nominal by AccSpline.
    folder = UNFOLDED_DIR
    spline_path = os.path.join(folder, SPLINE_NOMINAL_NAME)
    if(os.path.isfile(spline_path)):
        nominal = manifest["nominals"]["spline"]
        nominal["path"] = spline_path
        nominal["path_status"] = "verified"
        nominal["weight_tag"] = "Spline"
        nominal["fingerprint"] = file_fingerprint(spline_path)
    acc_path = os.path.join(folder, ACC_VARIATION_NAME)
    for row in manifest["variations"]:
        if(row["campaign"] == "unweighted" and row["source"] == "acceptance_reweighting" and row["variation"] == "Acc"):
            row["path"] = acc_path if(os.path.isfile(acc_path)) else None
            row["path_status"] = path_state(acc_path, True)
            row["weight_tag"] = "Acc"
            row["enabled"] = os.path.isfile(acc_path)
            row["fingerprint"] = file_fingerprint(row["path"])
    present = set()
    for row in manifest["variations"]:
        present.add((row["campaign"], row["source"], str(row["variation"])))
    if(os.path.isdir(folder)):
        for name in sorted(os.listdir(folder)):
            parsed = split_unfolded_name(name)
            if(parsed is None):
                continue
            if(parsed["branch"] not in METHOD_BRANCH_SOURCES):
                continue
            tag = parsed["weight_tag"]
            if(tag == "Spline"):
                campaign = "spline"
            elif(tag == ""):
                campaign = "unweighted"
            else:
                continue
            source_name, variation_name, combine = METHOD_BRANCH_SOURCES[parsed["branch"]]
            key = (campaign, source_name, variation_name)
            if(key in present):
                continue
            path = os.path.join(folder, name)
            manifest["variations"].append(entry("method", campaign, source_name, variation_name, tag, "Bayesian", path, "verified", "nominals.%s" % campaign, combine, True))
            present.add(key)
    return manifest


def patch_manifest(manifest):
    # Update paths in an existing manifest. Do not rebuild the cut-variation list.
    sync_corrected_unfold_inputs(manifest)
    five_path = os.path.join(UNFOLDED_DIR, UNWEIGHTED_5D_NAME)
    manifest["dimension"]["unweighted"] = {
        "path": five_path,
        "path_status": path_state(five_path, True),
        "weight_tag": "",
        "method": "Bayesian",
        "dimension": "5D",
        "study_state": "ready" if(os.path.isfile(five_path)) else "blocked",
        "bayes_iterations": 5,
        "nominal_iterations_bins_1_and_5": 6,
        "iteration_mismatch_bins": list(ITERATION_MISMATCH_BINS),
        "nominal_id": "nominals.unweighted",
        "input_response": "SIDIS_epip_Response_Matrices_from_RDataFrames_Only_5D_SIDIS_Workflow_Bank_Response_Matrices_Final_Thesis_Files_All.root",
    }
    if(not os.path.isfile(five_path)):
        manifest["dimension"]["unweighted"]["study_state"] = "blocked"
    spline_dim = manifest["dimension"].get("spline", {})
    spline_dim["path"] = SPLINE_5D_PATH
    spline_dim["path_status"] = path_state(SPLINE_5D_PATH, True)
    spline_dim["study_state"] = "ready" if(os.path.isfile(SPLINE_5D_PATH)) else "blocked"
    spline_dim["weight_tag"] = "Spline"
    manifest["dimension"]["spline"] = spline_dim
    manifest["radiative"]["event_ratio_root"] = {
        "path": RC_FACTOR_ROOT,
        "path_status": path_state(RC_FACTOR_ROOT, True),
        "role": "nominal_correction",
    }
    manifest["radiative"]["study_state"] = "pending"
    manifest["radiative"]["blocks_aggregation"] = False
    manifest["bin_centering"]["event_root"] = {
        "path": BC_EVENT_ROOT,
        "path_status": path_state(BC_EVENT_ROOT, True),
        "role": "supporting_subbin_distributions",
    }
    manifest["bin_centering"]["blocks_aggregation"] = False
    manifest["run"]["max_concurrent"] = 2
    for row in manifest.get("method_branches_blocked", []):
        row["path_status"] = path_state(row.get("path"), True)
        row["eligible"] = False
        row["study_state"] = "blocked"
    return manifest


def rc_factor_name(q2y_bin, zpt_bin):
    return "(RC_Factor)_(gdf)_(SMEAR='')_(Q2_y_Bin_%s)_(z_pT_Bin_%s)_(phi_t)_(Normalized_Weight)" % (q2y_bin, zpt_bin)


def bc_factor_key(q2y_bin, zpt_bin, phi_bin):
    return "Bin (%s-%s-%s)" % (q2y_bin, zpt_bin, phi_bin)


def count_5d_bayesian(path):
    # Read-only. Returns how many (MultiDim_5D_Histo)_(Bayesian)_ keys are present.
    import ROOT
    ROOT.gROOT.SetBatch(True)
    handle = ROOT.TFile.Open(path, "READ")
    if((handle is None) or handle.IsZombie()):
        raise ValueError("unreadable 5D file")
    count = 0
    for key in handle.GetListOfKeys():
        if("(MultiDim_5D_Histo)_(Bayesian)_" in key.GetName()):
            count += 1
    handle.Close()
    return count


def correction_coverage(rc_path, bc_json_path, bins):
    # bins is a list of (q2y, zpt). Missing factors are reported and not invented.
    import ROOT
    ROOT.gROOT.SetBatch(True)
    rc_file = ROOT.TFile.Open(rc_path, "READ")
    if((rc_file is None) or rc_file.IsZombie()):
        raise ValueError("unreadable RC file")
    rc_names = set(key.GetName() for key in rc_file.GetListOfKeys())
    rc_bad = []
    for q2y_bin, zpt_bin in bins:
        name = rc_factor_name(q2y_bin, zpt_bin)
        if(name not in rc_names):
            rc_bad.append({"bin": [q2y_bin, zpt_bin], "reason": "missing"})
            continue
        hist = rc_file.Get(name)
        xmin = hist.GetXaxis().GetXmin()
        xmax = hist.GetXaxis().GetXmax()
        if((hist.GetNbinsX() != 24) or (xmin != 0.0) or (xmax != 360.0)):
            rc_bad.append({"bin": [q2y_bin, zpt_bin], "reason": "incompatible_axis"})
    rc_file.Close()
    handle = open(bc_json_path)
    payload = json.load(handle)
    handle.close()
    results = payload.get("results", {})
    bc_bad = []
    for q2y_bin, zpt_bin in bins:
        for phi_bin in range(1, 25):
            key = bc_factor_key(q2y_bin, zpt_bin, phi_bin)
            entry = results.get(key)
            factor = None if(not isinstance(entry, dict)) else entry.get("BC_Factor")
            if(factor is None):
                bc_bad.append({"key": key, "reason": "missing"})
                continue
            try:
                value = float(factor)
            except (TypeError, ValueError):
                bc_bad.append({"key": key, "reason": "invalid"})
                continue
            if(value != value):
                bc_bad.append({"key": key, "reason": "invalid"})
    return {"rc_bad": rc_bad, "bc_bad": bc_bad, "bins_checked": len(bins)}


def nominal_analysis_bins():
    # Analysis cells used by the 3D fit: Q2-y 1-17 and the z-pT slots that are not skipped.
    from MyCommonAnalysisFunction_richcap import skip_condition_z_pT_bins
    bins = []
    for q2y_bin in range(1, 18):
        for zpt_bin in range(1, 37):
            if(skip_condition_z_pT_bins(Q2_Y_BIN=q2y_bin, Z_PT_BIN=zpt_bin)):
                continue
            bins.append((q2y_bin, zpt_bin))
    return bins


def limits_table():
    import importlib.util
    path = os.path.join(ANALYSIS_ROOT, "Phi_h_Fit_Parameters_Initialize.py")
    spec = importlib.util.spec_from_file_location("phi_h_fit_parameters_initialize", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    table = {}
    for key, value in module.special_fit_parameters_set.items():
        if((not isinstance(key, tuple)) or (len(key) < 2)):
            continue
        table[(str(key[0]), str(key[1]))] = value
    return table


def init_module_from_nominal_json(nominal_json, out_path):
    handle = open(nominal_json)
    payload = json.load(handle)
    handle.close()
    cells = {}
    for name, value in payload.items():
        if(not isinstance(value, dict)):
            continue
        for bin_name, cell in value.items():
            if((not isinstance(cell, dict)) or ("Fit_Par_B" not in cell) or ("Fit_Par_C" not in cell)):
                continue
            cells[bin_name] = cell
    return write_init_module(cells, limits_table(), out_path)


def rms_of_shifts(shifts):
    count = len(shifts)
    if(count == 0):
        return None
    total = 0.0
    for value in shifts:
        number = float(value)
        total += number * number
    return math.sqrt(total / float(count))


def pooled_subdivision_rms(shifts_by_variable):
    # One RMS over every variation. Equivalent to sqrt(mean of the five variable variances).
    if(sorted(shifts_by_variable.keys()) != sorted(BC_SENSITIVITY.keys())):
        return None
    all_shifts = []
    variable_rms = {}
    for variable in BC_SENSITIVITY.keys():
        shifts = list(shifts_by_variable[variable])
        if(len(shifts) != 3):
            return None
        variable_rms[variable] = rms_of_shifts(shifts)
        all_shifts.extend(shifts)
    pooled = rms_of_shifts(all_shifts)
    variance_mean = 0.0
    for value in variable_rms.values():
        variance_mean += float(value) * float(value)
    from_variables = math.sqrt(variance_mean / float(len(variable_rms)))
    if(abs(pooled - from_variables) > 1.0e-12):
        raise ValueError("pooled subdivision RMS disagrees with the five-variable mean")
    quadrature = math.sqrt(variance_mean)
    return {"variable_rms": variable_rms, "pooled": pooled, "quadrature_of_five": quadrature, "count": len(all_shifts)}


def event_style_bc_factor(sub_values, center_value):
    # Same orientation as the nominal JSON: unweighted sub-bin mean divided by the center value.
    if(len(sub_values) == 0):
        return None
    if(float(center_value) == 0.0):
        return None
    total = 0.0
    for value in sub_values:
        total += float(value)
    return (total / float(len(sub_values))) / float(center_value)


def modulation_value(parameter_a, parameter_b, parameter_c, phi_deg):
    radians = float(phi_deg) * math.pi / 180.0
    return float(parameter_a) * (1.0 + (float(parameter_b) * math.cos(radians)) + (float(parameter_c) * math.cos(2.0 * radians)))


def injection_spline_record():
    return {
        "role": "original_injection",
        "path": INJECTION_SPLINE_TXT,
        "path_status": path_state(INJECTION_SPLINE_TXT, True),
        "provenance": "jlab_work_paths.REL_SPLINE_DEFAULT and Campaign/local_orchestrator.py --spline_file",
        "study_state": "verified" if(os.path.isfile(INJECTION_SPLINE_TXT)) else "blocked",
    }


def json_meta(path):
    handle = open(path)
    payload = json.load(handle)
    handle.close()
    meta = payload.get("meta", {})
    return meta if(isinstance(meta, dict)) else {}


def discover_bc_subdivisions(folder=None):
    folder = BC_DIR if(folder in [None, ""]) else folder
    groups = {}
    for variable, counts in BC_SENSITIVITY.items():
        rows = []
        for count in counts:
            name = "Sub_Bin_Contents_for_BC_Correction_with_Binned_sbatch_from_10_26_2026_sens_%s_%s.json" % (variable, count)
            path = os.path.join(folder, name)
            row = {
                "variable": variable,
                "count": int(count),
                "path": path,
                "path_status": path_state(path, True),
                "others_at_one": False,
                "studied_count_matches": False,
                "study_state": "absent_on_disk",
            }
            if(os.path.isfile(path)):
                meta = json_meta(path)
                studied_key = "num_sub_bins_%s" % variable
                studied_ok = int(meta.get(studied_key, -1)) == int(count)
                others_ok = True
                for other in BC_NOMINAL_COUNTS.keys():
                    if(other == variable):
                        continue
                    if(int(meta.get("num_sub_bins_%s" % other, -1)) != 1):
                        others_ok = False
                row["path_status"] = "verified"
                row["studied_count_matches"] = studied_ok
                row["others_at_one"] = others_ok
                row["study_state"] = "verified" if(studied_ok and others_ok) else "invalid"
                row["comparison_basis"] = "The named variable changes. Every other subdivision count is 1, which is not the nominal 3,3,3,3,5 grid."
            rows.append(row)
        groups[variable] = rows
    return groups


def safe_report_token(value):
    text = "nominal" if(value in [None, ""]) else str(value)
    cleaned = []
    for character in text:
        if(character.isalnum() or character in ["_", "-", "."]):
            cleaned.append(character)
        else:
            cleaned.append("_")
    token = "".join(cleaned).strip("_")
    return "nominal" if(token == "") else token


def agent_report_path(output_dir, run_id, stage, campaign, source_or_shard, label):
    return os.path.join(
        output_dir, "reports", "agents",
        safe_report_token(run_id), safe_report_token(stage), safe_report_token(campaign),
        safe_report_token(source_or_shard), safe_report_token(label) + ".md",
    )


def agent_report_text(run_id, stage, campaign, source_or_shard, label, body):
    header = [
        "# Agent record",
        "- run_id: %s" % run_id,
        "- stage: %s" % stage,
        "- campaign: %s" % campaign,
        "- source_or_shard: %s" % source_or_shard,
        "- label: %s" % label,
        "",
        str(body).rstrip(),
        "",
    ]
    return "\n".join(header)


def write_agent_report(output_dir, run_id, stage, campaign, source_or_shard, label, body):
    path = agent_report_path(output_dir, run_id, stage, campaign, source_or_shard, label)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    text = agent_report_text(run_id, stage, campaign, source_or_shard, label, body)
    if(os.path.isfile(path)):
        existing = open(path).read()
        if(("run_id: %s" % run_id) not in existing):
            raise ValueError("agent report path belongs to a different run")
    temporary = path + ".partial"
    handle = open(temporary, "w")
    handle.write(text)
    handle.close()
    os.replace(temporary, path)
    return path


def parse_agent_report(path):
    handle = open(path)
    lines = handle.read().splitlines()
    handle.close()
    record = {"path": path, "mtime": os.path.getmtime(path)}
    for line in lines:
        if(not line.startswith("- ")):
            continue
        if(": " not in line):
            continue
        key, value = line[2:].split(": ", 1)
        if(key in ["run_id", "stage", "campaign", "source_or_shard", "label"]):
            record[key] = value
    record["body"] = "\n".join(lines)
    return record


def load_agent_reports(output_dir, run_id):
    root = os.path.join(output_dir, "reports", "agents", safe_report_token(run_id))
    if(not os.path.isdir(root)):
        return {"records": [], "collisions": [], "missing_tree": root}
    found = {}
    collisions = []
    for dirpath, _dirnames, filenames in os.walk(root):
        for name in filenames:
            if(not name.endswith(".md")):
                continue
            record = parse_agent_report(os.path.join(dirpath, name))
            identity = (
                record.get("run_id"), record.get("stage"), record.get("campaign"),
                record.get("source_or_shard"), record.get("label"),
            )
            if(None in identity):
                collisions.append({"path": record["path"], "reason": "missing identity"})
                continue
            previous = found.get(identity)
            if(previous is None):
                found[identity] = record
            elif(record["mtime"] >= previous["mtime"]):
                collisions.append({"path": previous["path"], "kept": record["path"]})
                found[identity] = record
            else:
                collisions.append({"path": record["path"], "kept": previous["path"]})
    records = [found[key] for key in sorted(found.keys())]
    return {"records": records, "collisions": collisions, "missing_tree": None}


def refinement_note_ok(note):
    required = ["scope", "start_mode", "error_source", "changed", "left_bins", "unresolved"]
    if(not isinstance(note, dict)):
        return False
    for key in required:
        if(key not in note):
            return False
        if(str(note[key]).strip() == ""):
            return False
    return True


def new_run_id():
    return datetime.datetime.now().strftime("%Y%m%dT%H%M%S")


def write_work_plan(manifest, output_dir, max_concurrent):
    nominal_jobs = []
    variation_jobs = []
    for campaign in ["unweighted", "spline"]:
        for job in fit_jobs(manifest, campaign):
            if(job["kind"] == "nominal"):
                nominal_jobs.append(job)
            else:
                variation_jobs.append(job)
    path = os.path.join(output_dir, "work_plan.json")
    run_id = new_run_id()
    if(os.path.isfile(path)):
        handle = open(path)
        previous = json.load(handle)
        handle.close()
        if(previous.get("run_id") not in [None, ""]):
            run_id = previous["run_id"]
    plan = {
        "run_id": run_id,
        "max_concurrent": int(max_concurrent),
        "nominal_shards": shard_jobs(nominal_jobs, max_concurrent),
        "variation_shards": shard_jobs(variation_jobs, max_concurrent),
        "deferred_nonblocking": [
            "radiative_systematic",
            "bin_centering_method",
            "bin_centering_iteration",
            "bin_centering_subdivision_until_observable_shifts",
        ],
    }
    write_json(path, plan)
    return path


def write_json(path, payload):
    folder = os.path.dirname(path)
    if(folder):
        os.makedirs(folder, exist_ok=True)
    temporary = path + ".partial"
    handle = open(temporary, "w")
    json.dump(payload, handle, indent=2, sort_keys=True)
    handle.write("\n")
    handle.close()
    os.replace(temporary, path)
    return path


KNOWN_STAGES = [
    "resolve",
    "nominal",
    "variations",
    "radiative",
    "bin_centering",
    "aggregate",
    "correct",
    "nominal_rc",
    "nominal_bc",
    "mosaic",
    "kt2",
    "phi_figures",
    "report_markdown",
    "report_pptx",
    "world_comparisons",
    "theory_comparisons",
    "thesis_integration_plan",
]
FORCED_NOT_COMBINED = [
    "electron_sector",
    "pion_sector",
    "unweighted_versus_spline",
    "radiative_sf0",
    "radiative_sf2",
    "radiative_sf0_versus_sf2",
    "bc_spline_alternative",
]
PHI_BIN_COUNT = 24
RC_SF2_WORKERS_DEFAULT = 4
RC_SF2_WORKERS_TESTED_MAX = 5
LOCAL_PYTHON = "/Users/richardcapobianco/opt/miniforge3/envs/updated_python/bin/python"
SKILL_CORRECT = os.path.expanduser("~/.grok/skills/sidis-bin-corrections/scripts/correct.py")
SKILL_NORM_NOTE = os.path.expanduser("~/.grok/skills/sidis-bin-corrections/references/electroproduction-normalization.md")
FORK_CROSS_SECTION = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/EvGen_sidis_fork/sidis/build/example/cross_section"
CONTINUOUS_BENCHMARK = {
    0: {
        "sigma_B": 3.2640895232967875e-05,
        "sigma_tot": 2.9883114578853511e-05,
        "rc": 0.9155114884432165,
    },
    2: {
        "sigma_B": 5.1022637054989254e-04,
        "sigma_tot": 4.6766432619644064e-04,
        "rc": 0.91658203728752596,
    },
}
INDEXED_BIN_1_1_FACTORS = {
    "delta_q2": 0.4,
    "delta_y": 0.1,
    "delta_z": 0.31,
    "delta_pt": 0.17,
    "delta_phi_deg": 15.0,
    "area": 0.03162,
    "lumi": 4.5818041672663315e10,
    "gamma": 6.715367807307382e-4,
}
PROVENANCE_FIELDS = [
    "normalization_reference",
    "physics_configuration",
    "normalization_convention",
    "normalization_gamma",
]
AFTER_QUALITY = re.compile(r"\((\d+)\s*,\s*(\d+)\)\s+([0-9]+(?:\.[0-9]+)?)\s+(?:to|→|->)\s+([0-9]+(?:\.[0-9]+)?)")
AFTER_QUALITY_AT = re.compile(r"([0-9]+(?:\.[0-9]+)?)\s+(?:to|→|->)\s+([0-9]+(?:\.[0-9]+)?)\s+at Q2-y\s+(\d+),\s*z-pT\s+(\d+)")
FITTED_COUNT = re.compile(r"(\d+)\s+fitted cells")
JSON_STILL = re.compile(r"JSON still(?: has)?\s+(\d+)")
INIT_KEY = re.compile(r"\(\s*'(\d+)'\s*,\s*'(\d+)'")
IMPROVED_LIST = re.compile(r"improved,\s+to\s+([0-9.,\s]+and\s+[0-9]+(?:\.[0-9]+)?)")


def source_enters_quadrature(source, combine_by_source):
    if(source in FORCED_NOT_COMBINED):
        return False
    return combine_by_source.get(source) == "independent"


def stage_request_plan(stage_names, rc_fixed_point="no", bc_spline_alternative="no"):
    unknown = []
    for name in stage_names:
        if(name not in KNOWN_STAGES):
            unknown.append(name)
    if(len(unknown) > 0):
        return {"ok": False, "blocker": "unknown_stage", "unknown": unknown, "falls_back_to_resolve_only": False}
    actions = []
    for name in stage_names:
        if(name == "radiative"):
            if(rc_fixed_point == "yes"):
                actions.append({"stage": name, "action": "run_rc_grid"})
            else:
                actions.append({"stage": name, "action": "record_grid_not_enabled", "flag": "rc_fixed_point"})
        elif(name == "bin_centering"):
            if(bc_spline_alternative == "yes"):
                actions.append({"stage": name, "action": "run_bc_grid"})
            else:
                actions.append({"stage": name, "action": "record_grid_not_enabled", "flag": "bc_spline_alternative"})
        elif(name in ["world_comparisons", "theory_comparisons"]):
            actions.append({"stage": name, "action": "run_or_record_blocker"})
        elif(name == "thesis_integration_plan"):
            actions.append({"stage": name, "action": "write_partial_plan"})
        else:
            actions.append({"stage": name, "action": "run"})
    return {
        "ok": True,
        "stages": list(stage_names),
        "actions": actions,
        "rc_fixed_point": rc_fixed_point,
        "bc_spline_alternative": bc_spline_alternative,
        "falls_back_to_resolve_only": False,
    }


def phi_canvas_decision(drawn, na_count, dry_run):
    thesis_ready = (int(na_count) == 0) and (int(drawn) > 0)
    save = (not dry_run) and ((int(drawn) + int(na_count)) > 0)
    return {"save": save, "thesis_ready": thesis_ready}


def skill_input_fingerprint():
    return {
        "correct_py": file_fingerprint(SKILL_CORRECT),
        "normalization_note": file_fingerprint(SKILL_NORM_NOTE),
    }


def accept_fixed_point_record(payload):
    if(not isinstance(payload, dict)):
        return False, "not_an_object"
    if(payload.get("ok") is not True):
        return False, "not_ok"
    for key in PROVENANCE_FIELDS:
        if(str(payload.get(key, "")).strip() == ""):
            return False, "missing_%s" % key
    mode = payload.get("mode")
    if(mode == "RC"):
        if(payload.get("rc") in [None, ""]):
            return False, "missing_rc"
        meaning = str(payload.get("delta_rc_meaning", ""))
        if("not a statistical" not in meaning):
            return False, "delta_rc_meaning"
        if(payload.get("sf_index") not in [0, 2]):
            return False, "sf_index"
    elif(mode == "BC"):
        if(payload.get("bc") in [None, ""]):
            return False, "missing_bc"
        if(int(payload.get("n_sub", 0)) != 405):
            return False, "n_sub"
        if(int(payload.get("center_subbin", 0)) != 203):
            return False, "center_subbin"
    else:
        return False, "unknown_mode"
    return True, "ok"


def factor_from_fixed_point(payload):
    # A failed or incomplete object contributes no factor. It is not replaced by 0, 1, or a nominal value.
    accepted, reason = accept_fixed_point_record(payload)
    if(not accepted):
        return None, reason
    if(payload["mode"] == "RC"):
        return float(payload["rc"]), "ok"
    return float(payload["bc"]), "ok"


def radiative_stage_gate(rc_fixed_point, stage_names, grid_complete, grid_active, sf2_workers=None):
    # While the RC grids are active, no other stage is concurrent. Downstream stages wait for both grids.
    enabled = (str(rc_fixed_point) == "yes") and ("radiative" in list(stage_names))
    limit = resolve_worker_count("RC", 2, sf2_workers)
    others = [name for name in stage_names if(name != "radiative")]
    if(not enabled):
        return {"grid_enabled": False, "sf0_workers": 1, "sf2_workers": limit["workers"], "concurrent_stages": [], "downstream_stages": others}
    if(grid_active or (not grid_complete)):
        return {"grid_enabled": True, "sf0_workers": 1, "sf2_workers": limit["workers"], "concurrent_stages": [], "downstream_stages": []}
    return {"grid_enabled": True, "sf0_workers": 1, "sf2_workers": limit["workers"], "concurrent_stages": [], "downstream_stages": others}


def resolve_worker_count(mode, sf_index, requested, allow_untested=False):
    # SF 0 and spline BC stay at one process. Only RC SF 2 uses the worker limit.
    count = RC_SF2_WORKERS_DEFAULT if(requested is None) else int(requested)
    if(count < 1):
        raise ValueError("worker count must be at least 1")
    mode_name = str(mode)
    sf_value = None if(sf_index is None) else int(sf_index)
    if((mode_name == "BC") or ((mode_name == "RC") and (sf_value == 0))):
        return {"workers": 1, "clamped": "sf0_and_bc_stay_at_one_process"}
    if((mode_name != "RC") or (sf_value != 2)):
        raise ValueError("unsupported fixed-point configuration")
    if((count > RC_SF2_WORKERS_TESTED_MAX) and (not allow_untested)):
        raise ValueError("SF 2 worker counts above %s were not benchmarked" % RC_SF2_WORKERS_TESTED_MAX)
    return {"workers": count, "clamped": ""}


def fixed_point_cache_state(path, fingerprint):
    if(not os.path.isfile(path)):
        return "missing"
    try:
        handle = open(path)
        payload = json.load(handle)
        handle.close()
    except (OSError, ValueError):
        return "invalid"
    if(not isinstance(payload, dict)):
        return "invalid"
    if(payload.get("skill_fingerprint") != fingerprint):
        return "stale"
    if(payload.get("ok") is True):
        return "ok"
    return "failed"


def fixed_point_cache_name(mode, q2y_bin, zpt_bin, phi_bin, sf_index):
    sf_token = "na" if(sf_index is None) else str(int(sf_index))
    return os.path.join(mode, "q%d" % int(q2y_bin), "z%d" % int(zpt_bin), "p%d_s%s.json" % (int(phi_bin), sf_token))


def fixed_point_coverage(ok_keys, expected_bins):
    holes = []
    for q2y_bin, zpt_bin in expected_bins:
        for phi_bin in range(1, PHI_BIN_COUNT + 1):
            if((int(q2y_bin), int(zpt_bin), phi_bin) not in ok_keys):
                holes.append([int(q2y_bin), int(zpt_bin), phi_bin])
    calls = len(expected_bins) * PHI_BIN_COUNT
    return {"calls": calls, "holes": holes, "ok": len(holes) == 0}


def assemble_phi_factors(values_by_phi, q2y_bin, zpt_bin):
    # values_by_phi maps phi bin -> accepted factor, or omits a failed phi. Missing keys are holes.
    factors = {}
    holes = []
    for phi_bin in range(1, PHI_BIN_COUNT + 1):
        key = bc_factor_key(q2y_bin, zpt_bin, phi_bin)
        if(phi_bin not in values_by_phi):
            holes.append(key)
            continue
        value = values_by_phi[phi_bin]
        if(value is None):
            holes.append(key)
            continue
        factors[key] = float(value)
    return {"factors": factors, "holes": holes, "complete": len(holes) == 0}


def normalized_bc_path(output_dir, campaign):
    return os.path.join(output_dir, "corrected", campaign, "normalized_bc.json")


def stale_normalized_path(output_dir, campaign):
    return os.path.join(output_dir, "corrected", campaign, "normalized.json")


def normalization_provenance(campaign, fit_path, budget_path):
    return {
        "normalization_status": "applied",
        "campaign": campaign,
        "systematic_scope": "provisional_acceptance_level",
        "systematic_scope_text": "Acceptance-level budget attached to the BC central values. Not the complete final systematic.",
        "provisional_systematic": True,
        "unassigned_factor_uncertainty": True,
        "source_fit": os.path.abspath(fit_path),
        "source_fit_fingerprint": file_fingerprint(fit_path),
        "budget_path": os.path.abspath(budget_path),
        "budget_fingerprint": file_fingerprint(budget_path),
        "scales_A_only": True,
        "fit_family": "Fit_Pars_from_3D_BC_RC_Bayesian",
    }


def build_normalized_document(cells, totals, scales, campaign, fit_path, budget_path):
    prepared = {}
    for bin_name, cell in cells.items():
        updated = dict(cell)
        total = totals[bin_name]
        for parameter, field in FIT_FIELDS.items():
            piece = total[parameter]
            sys_value = piece.get("up")
            if(sys_value is None):
                raise ValueError("missing systematic for %s" % bin_name)
            updated[field + "_SYS"] = float(sys_value)
        prepared[bin_name] = updated
    stat_copy = normalize_campaign_copy(prepared, "statistical", scales)
    sys_copy = normalize_campaign_copy(prepared, "systematic", scales)
    merged = merge_normalized(stat_copy, sys_copy)
    document = normalization_provenance(campaign, fit_path, budget_path)
    document["Fit_Pars_from_3D_BC_RC_Bayesian"] = merged["cells"]
    return document


def reject_stale_normalized_artifact(artifact):
    path = str(artifact.get("path", ""))
    if(path == ""):
        return
    folder = os.path.dirname(path)
    fresh = os.path.join(folder, "normalized_bc.json")
    if((os.path.basename(path) == "normalized.json") and os.path.isfile(fresh)):
        raise ValueError("stale normalized.json is refused because normalized_bc.json exists")
    if(os.path.basename(path) != "normalized_bc.json"):
        return
    if(artifact.get("systematic_scope") != "provisional_acceptance_level"):
        raise ValueError("normalized file is missing the provisional acceptance-level label")
    expected = artifact.get("source_fit_fingerprint")
    if(not isinstance(expected, dict)):
        raise ValueError("normalized file is missing source_fit_fingerprint")
    fit_path = os.path.join(folder, "bc", "fit.json")
    current = file_fingerprint(fit_path)
    if((expected.get("size") != current.get("size")) or (expected.get("mtime") != current.get("mtime"))):
        raise ValueError("normalized file does not match the latest BC fit")


def continuous_benchmark_matches(sf_index, sigma_b, sigma_tot, rc_value):
    row = CONTINUOUS_BENCHMARK.get(int(sf_index))
    if(row is None):
        return False
    for got, name in [(sigma_b, "sigma_B"), (sigma_tot, "sigma_tot"), (rc_value, "rc")]:
        reference = row[name]
        scale = max(abs(reference), 1.0e-30)
        if(abs(float(got) - reference) / scale > 1.0e-9):
            return False
    return True


def parse_cross_section_text(text):
    values = {}
    for line in str(text).splitlines():
        if("=" not in line):
            continue
        label, rest = line.split("=", 1)
        label = label.strip()
        token = rest.strip().split()[0]
        try:
            values[label] = float(token)
        except ValueError:
            continue
    return values


def fit_family_cells(payload):
    for key in ["Fit_Pars_from_3D_Bayesian", "Fit_Pars_from_3D_RC_Bayesian", "Fit_Pars_from_3D_BC_RC_Bayesian", "Fit_Pars_from_3D_Bin", "Fit_Pars_from_5D_Bayesian"]:
        block = payload.get(key)
        if(isinstance(block, dict) and (len(block) > 0)):
            return key, block
    return None, {}


def reduced_chi2(cell):
    if(not isinstance(cell, dict)):
        return None
    chi2 = cell.get("Chi2")
    ndf = cell.get("NDF")
    if((chi2 is None) or (ndf in [None, 0, 0.0])):
        return None
    return float(chi2) / float(ndf)


def after_matches(cell, claimed, decimals):
    reduced = reduced_chi2(cell)
    raw = None if(not isinstance(cell, dict)) else cell.get("Chi2")
    tolerance = (0.5 * (10.0 ** (-int(decimals)))) + 0.001
    for value in [reduced, raw]:
        if(value is None):
            continue
        if(abs(float(value) - float(claimed)) <= tolerance):
            return True
    return False


def classify_refinement_dir(note, fit_payload, refine_init_text, overlay_count):
    evidence = []
    if(not refinement_note_ok(note)):
        return {"classification": "incomplete", "reason": "note is missing a required field", "minimum_check": "restore scope, start_mode, error_source, changed, left_bins, and unresolved", "evidence": ["required note fields are empty or absent"]}
    if(not isinstance(fit_payload, dict)):
        return {"classification": "incomplete", "reason": "fit JSON is missing", "minimum_check": "confirm the fit JSON for this directory", "evidence": ["fit JSON missing"]}
    family, cells = fit_family_cells(fit_payload)
    if(family is None):
        return {"classification": "incomplete", "reason": "fit JSON has no populated family", "minimum_check": "confirm the fit family key and cell count", "evidence": ["no populated fit family"]}
    text = " ".join([str(note.get("changed", "")), str(note.get("scope", "")), str(note.get("left_bins", ""))])
    claimed_counts = []
    for match in JSON_STILL.finditer(text):
        claimed_counts.append(int(match.group(1)))
    for match in FITTED_COUNT.finditer(text):
        claimed_counts.append(int(match.group(1)))
    if(len(set(claimed_counts)) > 1):
        return {
            "classification": "incomplete",
            "reason": "the note states more than one cell count",
            "minimum_check": "keep one cell count and compare it with %s" % family,
            "evidence": ["note counts %s" % claimed_counts],
        }
    if((len(claimed_counts) > 0) and (len(cells) != claimed_counts[0])):
        return {
            "classification": "incomplete",
            "reason": "stated cell count does not match the fit JSON",
            "minimum_check": "compare the note's cell count with %s (%s cells)" % (family, len(cells)),
            "evidence": ["note counts %s; JSON %s has %s" % (claimed_counts, family, len(cells))],
        }
    init_keys = set()
    if(refine_init_text not in [None, ""]):
        for match in INIT_KEY.finditer(refine_init_text):
            init_keys.add((match.group(1), match.group(2)))
    mismatches = []
    checked = []
    pairs = []
    changed = str(note.get("changed", ""))
    for match in AFTER_QUALITY.finditer(changed):
        pairs.append((match.group(1), match.group(2), match.group(3), match.group(4)))
    for match in AFTER_QUALITY_AT.finditer(changed):
        pairs.append((match.group(3), match.group(4), match.group(1), match.group(2)))
    improved = IMPROVED_LIST.search(changed)
    if(improved is not None):
        numbers = re.findall(r"[0-9]+(?:\.[0-9]+)?", improved.group(1))
        head = changed.split("improved, to", 1)[0]
        listed = re.findall(r"\((\d+)\s*,\s*(\d+)\)", head)
        if(len(listed) == len(numbers)):
            for (q2y, zpt), after in zip(listed, numbers):
                pairs.append((q2y, zpt, "", after))
    for q2y, zpt, before, after in pairs:
        bin_name = "(Q2_y_Bin_%s)-(z_pT_Bin_%s)" % (q2y, zpt)
        cell = cells.get(bin_name)
        decimals = len(after.split(".")[1]) if("." in after) else 0
        if(cell is None):
            mismatches.append("%s is absent from the fit JSON" % bin_name)
            continue
        if(not after_matches(cell, after, decimals)):
            mismatches.append("%s after %s does not match Chi2/NDF %s" % (bin_name, after, reduced_chi2(cell)))
            continue
        checked.append({"bin": bin_name, "before": before, "after": after, "stored_reduced_chi2": reduced_chi2(cell)})
        if(("refine_init" in str(note.get("changed", ""))) and ((q2y, zpt) not in init_keys) and (len(init_keys) > 0)):
            mismatches.append("%s is named as edited but is absent from refine_init.py" % bin_name)
    if(len(mismatches) > 0):
        return {"classification": "incomplete", "reason": mismatches[0], "minimum_check": "refit only the bins named in the mismatch list", "evidence": mismatches, "checked": checked}
    claims_guide = "refine_init" in str(note.get("changed", ""))
    if(claims_guide and (refine_init_text in [None, ""])):
        return {"classification": "incomplete", "reason": "the note cites refine_init.py and that file is absent", "minimum_check": "restore or regenerate the guide file, then compare its keys with the note", "evidence": ["refine_init.py absent"]}
    if(len(checked) == 0):
        minimum = "compare each bin named in changed with the stored Chi2/NDF and with refine_init.py"
        if(int(overlay_count) == 0):
            minimum = "open the histogram for one bin named in changed; no overlay file is stored. " + minimum
        return {
            "classification": "unverifiable",
            "reason": "the note has no before/after number that can be compared with the fit JSON",
            "minimum_check": minimum,
            "evidence": ["family %s has %s cells" % (family, len(cells)), "overlays %s" % overlay_count, "guide keys %s" % len(init_keys)],
            "validated": False,
        }
    return {
        "classification": "verified",
        "reason": "each stated after-quality matches the saved fit, and the stated cell count matches",
        "minimum_check": "",
        "evidence": ["checked %s bins" % len(checked), "family %s cells %s" % (family, len(cells)), "overlays %s" % overlay_count],
        "checked": checked,
        "validated": True,
    }
