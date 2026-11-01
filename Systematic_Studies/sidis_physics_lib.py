# Planning, comparison, and artifact helpers for the SIDIS physics-results workflow.
# This module does not unfold, fit histograms, start EvGen, or submit jobs.

import json
import os
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
SPLINE_NOMINAL_NAME = "Sys3D_nominal_only_20261030_AcceptanceWeightVariation_Spline.root"
UNWEIGHTED_NOMINAL_NAME = "Sys3D_nominal_only_20261030_inherited_Unweighted.root"
UNWEIGHTED_5D_NAME = "unfolded_5d_cpp_covariance.root"
RC_FACTOR_ROOT = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/Running_EvGen_richcap/Run_Large_Files_For_Iterative_Corrections/Comparison_With_Unfolding/build_EvGen_PerFile_Hists_Runtime_ifarm_rc/merged_outputs/RC_Factors_ifarm_rc.root"
SPLINE_5D_PATH = os.path.join(ANALYSIS_ROOT, "SIDIS_Campaign", "systematics", "nominal_5d_spline_20261030", "Unfolded_5D_inherited_Spline.root")
ITERATION_MISMATCH_BINS = [1, 5]
ACCSPLINE_VARIATION_NAME = "Sys3D_nominal_only_20261030_inherited_AccSpline.root"
BLOCKED_METHOD_BRANCHES = ["BayesMinus1", "BayesPlus1", "Acc015", "Acc025", "Phi12", "NoRho0"]
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
    for suffix, tag in [("_AccSpline", "AccSpline"), ("_Unweighted", ""), ("_Spline", "Spline")]:
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
        if(branch in BLOCKED_METHOD_BRANCHES):
            blocked_methods.append({
                "file_name": name,
                "path": path,
                "weight_tag": tag,
                "branch": branch,
                "eligible": False,
                "spline_path": None,
                "unweighted_path": None,
                "path_status": "verified",
                "study_state": "blocked",
                "reason": "Unfolded with AccSpline. No Spline or Unweighted file of this branch is available.",
            })
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
        None, "absent_on_disk", "nominals.unweighted", "independent", True,
    ))
    spline_files = {}
    for letter in ["A", "B", "C"]:
        pkl = "%s_Fit_Par_%s.pkl" % (SPLINE_PREFIX, letter)
        spline_files[letter] = {"path": pkl, "path_status": path_state(pkl, False)}
    txt = SPLINE_PREFIX + "_Compute_SplineWeight.txt"
    five_d_spline = os.path.join(ANALYSIS_ROOT, "SIDIS_Campaign", "systematics", "nominal_5d_spline_20261030", "Unfolded_5D_inherited_Spline.root")
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
            "spline": {"path": five_d_spline, "path_status": path_state(five_d_spline, True), "study_state": "blocked"},
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
            if(combine_by_source.get(source) == "not_combined"):
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


def mosaic_command(artifact, spline_overlay, spline_prefix, campaign):
    if(artifact.get("normalization_status") != "applied"):
        raise ValueError("mosaic requires normalization_status applied")
    cmd = [
        MOSAIC_SCRIPT,
        "--json_file", artifact["path"],
        "--formats", "pdf",
        "--y_pars", "Fit_Par_A", "Fit_Par_B", "Fit_Par_C",
        "--err_suffix", "_ERR",
        "--sys_err_suffix", "_SYS",
        "--name", "sidis_mosaic_%s" % campaign,
    ]
    if(spline_overlay):
        cmd.extend(["--spline_prefix", spline_prefix, "--dimension_mode", "4D_xB"])
    for token in cmd:
        if(token in ["--apply_A_corr", "-cs", "-cs_A"]):
            raise ValueError("mosaic must not apply A0 normalization")
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
        "sensitivity_blocked": len(sensitivity_rows()),
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


def patch_manifest(manifest):
    # Update paths in an existing manifest. Do not rebuild the variation list.
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
    spline_dim["study_state"] = "blocked"
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


def write_work_plan(manifest, output_dir, max_concurrent):
    nominal_jobs = []
    variation_jobs = []
    for campaign in ["unweighted", "spline"]:
        for job in fit_jobs(manifest, campaign):
            if(job["kind"] == "nominal"):
                nominal_jobs.append(job)
            else:
                variation_jobs.append(job)
    plan = {
        "max_concurrent": int(max_concurrent),
        "nominal_shards": shard_jobs(nominal_jobs, max_concurrent),
        "variation_shards": shard_jobs(variation_jobs, max_concurrent),
        "deferred_nonblocking": ["radiative_systematic", "bin_centering_method", "bin_centering_iteration", "bin_centering_sensitivity"],
    }
    path = os.path.join(output_dir, "work_plan.json")
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
