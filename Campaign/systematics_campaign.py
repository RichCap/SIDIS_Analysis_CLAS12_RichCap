# Planning helpers for the two-phase 3D systematic campaign.
# This module builds commands and the manifest. It does not submit jobs.
import json
import os
import time

try:
    import fcntl
except ImportError:
    fcntl = None

from jlab_work_paths import REL_HADD, REL_HPP_OUT, pipeline_output_path

DEFAULT_CUT = "cut_Complete_SIDIS"
NAME_IN_LABEL = "Final_Thesis_Files"
LINEAGE_COUNT = 41
Q2Y_BINS = list(range(1, 18))
EMAIL_TO = "richard.capobianco@uconn.edu"
SLURM_MEM = "15000"
SLURM_TIME = "1:40:00"
LOCAL_DELAY_S = 60

# CHI2PID_CUT_strict_pip uses coefficient 0.88 and electron momentum el.
# ExtraAnalysisCodeValues.py lines 2744-2751. The campaign uses the stored column as written.


def cut_name(suffix):
    if(suffix in [None, ""]):
        return DEFAULT_CUT
    return "cut_Complete_SIDIS_%s" % suffix


def phase1_row(config_id, suffix, unsmeared=False):
    return {
        "id": config_id,
        "cut": cut_name(suffix),
        "unsmeared": bool(unsmeared),
        "nominal": config_id == "nominal",
    }


def phase1_configs():
    rows = [phase1_row("nominal", "")]
    rows.append(phase1_row("chi2_strict_pip", "chi2_strict_pip"))
    pairs = [
        "dcfid_loose_el", "dcfid_tight_el",
        "dcfid_loose_pip", "dcfid_tight_pip",
        "dcv_loose_el", "dcv_tight_el",
        "dvz_loose_pip", "dvz_tight_pip",
        "pcalvol_loose", "pcalvol_tight",
        "ecband_loose_el", "ecband_tight_el",
        "ecthr_loose_el", "ecthr_tight_el",
        "dcfidref_loose_el", "dcfidref_tight_el",
    ]
    for suffix in pairs:
        rows.append(phase1_row(suffix, suffix))
    for sector in range(1, 7):
        rows.append(phase1_row("eS%do" % sector, "eS%do" % sector))
        rows.append(phase1_row("pipS%do" % sector, "pipS%do" % sector))
    for suffix in ["no_pip_testdc", "no_sector_pcal", "no_valerii_knockout"]:
        rows.append(phase1_row(suffix, suffix))
    rows.append(phase1_row("noSmear", "noSmear", unsmeared=True))
    return rows


def phase2_branches():
    return [
        "BayesMinus1", "BayesPlus1", "Acc015", "Acc025",
        "Phi12", "NoRho0", "AcceptanceWeightVariation",
    ]


def nominal_iterations(q2y):
    if(int(q2y) in [1, 5]):
        return 6
    return 5


def worker_cap(requested):
    if(requested in [None, ""]):
        return LINEAGE_COUNT
    value = int(requested)
    if(value < 1):
        raise ValueError("local worker cap must be at least 1")
    if(value > LINEAGE_COUNT):
        raise ValueError("local worker cap %s is above the %s lineage ceiling" % (value, LINEAGE_COUNT))
    return value


def hpp_pair(data_root, tag):
    folder = pipeline_output_path(REL_HPP_OUT, data_root)
    pure = os.path.join(folder, "generated_acceptance_weights_%s_noSpline.hpp" % tag)
    comb = os.path.join(folder, "generated_acceptance_weights_%s_withSpline.hpp" % tag)
    return pure, comb


def regen_spline_path(data_root, tag, campaign, stamp):
    folder = pipeline_output_path(REL_HPP_OUT, data_root)
    name = "generated_acceptance_weights_%s_withSpline_sysregen_%s_%s.hpp" % (tag, campaign, stamp)
    return os.path.join(folder, name)


def response_basename(config_id, cut):
    shared = "Sys3D_%s_Bank" % config_id
    if(cut != DEFAULT_CUT):
        shared = "%s_%s" % (shared, cut)
    product = "Only_3D_%s_Response_Matrices" % shared
    return "SIDIS_epip_Response_Matrices_from_RDataFrames_%s_%s_All.root" % (product, NAME_IN_LABEL)


def response_path(data_root, config_id, cut):
    return os.path.join(pipeline_output_path(REL_HADD, data_root), response_basename(config_id, cut))


def phase1_command(python, submit_script, data_root, campaign, cap, config, hpp_pure, hpp_spline):
    cmd = [
        python, submit_script,
        "-droot", data_root,
        "-m", "hybrid",
        "-mac", "Bank",
        "-cn", config["cut"],
        "-n", "Sys3D_%s" % config["id"],
        "-sa",
        "-hpf", hpp_pure,
        "-hps", hpp_spline,
        "-j", "1",
        "-j3D", "1",
        "-j2D", "0",
        "-j5D", "0",
        "-jBin", "0",
        "-jch4", "0",
        "-jdph", "0",
        "-j1D", "0",
        "-jdiag", "0",
        "-cwc", str(cap),
        "-cwn", campaign,
        "-e", "none",
    ]
    if(config["unsmeared"]):
        cmd.append("-us")
    return cmd


def expand_batch_spec(text, num_batches=171):
    # Same inclusive ranges as the pipeline parser. The recovery list is not rediscovered.
    if(text in [None, ""]):
        raise ValueError("batch list is empty")
    chosen = []
    for part in str(text).split(","):
        part = part.strip()
        if(part == ""):
            continue
        if("-" in part):
            left, right = part.split("-", 1)
            start = int(left)
            stop = int(right)
            for index in range(start, stop + 1):
                chosen.append(index)
        else:
            chosen.append(int(part))
    unique = []
    for index in chosen:
        if((index < 1) or (index > int(num_batches))):
            raise ValueError("batch id %s is outside 1-%s" % (index, num_batches))
        if(index not in unique):
            unique.append(index)
    if(len(unique) == 0):
        raise ValueError("batch list is empty")
    return unique


def load_recovery_batches(path):
    handle = open(path)
    try:
        payload = json.load(handle)
    finally:
        handle.close()
    if(not isinstance(payload, dict)):
        raise ValueError("recovery file must be an object")
    configs = payload.get("configs")
    if((not isinstance(configs, list)) or (len(configs) == 0)):
        raise ValueError("recovery file has no configs")
    payload["path"] = path
    return payload


def recovery_phase1_command(python, submit_script, data_root, campaign, config, hpp_pure, hpp_spline, batch_ids, hybrid_date, slurm_time, only3d_mem):
    # Slurm only. Hybrid's local walker can cancel and rewrite batches that are not listed.
    cmd = [
        python, submit_script,
        "-droot", data_root,
        "-m", "slurm",
        "-y",
        "-mac", "Bank",
        "-cn", config["cut"],
        "-n", "Sys3D_%s" % config["id"],
        "-sa",
        "-hpf", hpp_pure,
        "-hps", hpp_spline,
        "-j", "1",
        "-j3D", "1",
        "-j2D", "0",
        "-j5D", "0",
        "-jBin", "0",
        "-jch4", "0",
        "-jdph", "0",
        "-j1D", "0",
        "-jdiag", "0",
        "-e", "none",
        "-cwn", campaign,
        "-bids", str(batch_ids),
        "-hdate", str(hybrid_date),
        "-st", str(slurm_time),
        "-o3m", str(only3d_mem),
        "-rlb",
    ]
    if(config["unsmeared"]):
        cmd.append("-us")
    return cmd


def recovery_configs(payload):
    catalog = {}
    for row in phase1_configs():
        catalog[row["id"]] = row
    chosen = []
    seen = []
    for item in payload["configs"]:
        if(not isinstance(item, dict)):
            raise ValueError("recovery config entry must be an object")
        config_id = str(item.get("id", ""))
        if(config_id in seen):
            raise ValueError("duplicate recovery config %s" % config_id)
        seen.append(config_id)
        if(config_id == "nominal"):
            raise ValueError("recovery cannot include nominal")
        if(config_id not in catalog):
            raise ValueError("unknown recovery config %s" % config_id)
        spec = str(item.get("batches", ""))
        expand_batch_spec(spec)
        chosen.append({
            "config": catalog[config_id],
            "batches": spec,
            "original_job": str(item.get("original_job", "")),
        })
    return chosen


def regen_command(python, submit_script, data_root, spline_out):
    return [
        python, submit_script,
        "-droot", data_root,
        "-m", "sequential",
        "-mac", "Bank",
        "-cn", DEFAULT_CUT,
        "-n", "Sys3D_nominal",
        "-hso",
        "-hsp", spline_out,
        "-e", "none",
    ]


def weight_label(weight_tag):
    if(weight_tag in [None, ""]):
        return "Unweighted"
    return str(weight_tag)


def branch_settings(branch, q2y, weight_tag):
    settings = {
        "acceptance": 0.020,
        "background": "rho0_new",
        "phi_bins": 24,
        "iterations": None,
        "weight_tag": weight_tag,
    }
    if(branch == "BayesMinus1"):
        settings["iterations"] = nominal_iterations(q2y) - 1
    elif(branch == "BayesPlus1"):
        settings["iterations"] = nominal_iterations(q2y) + 1
    elif(branch == "Acc015"):
        settings["acceptance"] = 0.015
    elif(branch == "Acc025"):
        settings["acceptance"] = 0.025
    elif(branch == "Phi12"):
        settings["phi_bins"] = 12
    elif(branch == "NoRho0"):
        settings["background"] = "None"
    elif(branch == "AcceptanceWeightVariation"):
        settings["weight_tag"] = "Spline"
    elif(branch != "inherited"):
        raise ValueError("unknown Phase 2 branch %s" % branch)
    return settings


def phase2_jobs(config, weight_mode):
    jobs = []
    if(config["nominal"]):
        jobs.append({"config_id": config["id"], "branch": "inherited", "weight_tag": "AccSpline", "local_order": 0, "lineage": config["id"]})
        for branch in phase2_branches():
            tag = "Spline" if(branch == "AcceptanceWeightVariation") else "AccSpline"
            jobs.append({
                "config_id": config["id"],
                "branch": branch,
                "weight_tag": tag,
                "local_order": 0,
                "lineage": "nominal__%s" % branch,
            })
        return jobs
    if(weight_mode == "unweighted"):
        modes = [("Unweighted", "", 0)]
    elif(weight_mode == "weighted"):
        modes = [("Spline", "Spline", 0)]
    elif(weight_mode == "both"):
        modes = [("Spline", "Spline", 0), ("Unweighted", "", 1)]
    else:
        raise ValueError("unknown weight mode %s" % weight_mode)
    for label, tag, order in modes:
        jobs.append({
            "config_id": config["id"],
            "branch": "inherited",
            "weight_tag": tag,
            "weight_label": label,
            "local_order": order,
            "lineage": config["id"],
        })
    return jobs


def job_key(job):
    return "%s__%s__%s" % (job["config_id"], job["branch"], weight_label(job["weight_tag"]))


def job_stem(job):
    return "Sys3D_%s_%s_%s" % (job["config_id"], job["branch"], weight_label(job["weight_tag"]))


def bin_root(parts_dir, job, q2y):
    return os.path.join(parts_dir, "%s_q2y%02d.root" % (job_stem(job), int(q2y)))


def final_root(unfold_dir, job):
    return os.path.join(unfold_dir, "%s.root" % job_stem(job))


def unfold_command(python, script, data_root, response, root_out, q2y, settings):
    cmd = [
        python, script,
        "-droot", data_root,
        "-u3D",
        "-err", "covariance",
        "-ac", ("%s" % settings["acceptance"]),
        "-bgs", settings["background"],
        "-ph", str(settings["phi_bins"]),
        "-b", str(int(q2y)),
        "-sfin", response,
        "-r", root_out,
        "--skip_compile",
    ]
    if(settings["iterations"] is not None):
        cmd.extend(["-bi", str(settings["iterations"])])
    if(settings["weight_tag"] not in [None, ""]):
        cmd.extend(["-wt", settings["weight_tag"]])
    return cmd


def shell_quote(token):
    return "'" + str(token).replace("'", "'\"'\"'") + "'"


def iteration_shell(branch):
    # Bins 1 and 5 use a different nominal count than the other Q2-y bins.
    if(branch == "BayesMinus1"):
        return ["case \"$BIN\" in", "  1|5) BI=5 ;;", "  *) BI=4 ;;", "esac"], " -bi \"$BI\""
    if(branch == "BayesPlus1"):
        return ["case \"$BIN\" in", "  1|5) BI=7 ;;", "  *) BI=6 ;;", "esac"], " -bi \"$BI\""
    return [], ""


def sbatch_script(job_name, log_dir, python, script, data_root, response, parts_dir, stem, branch, weight_tag):
    settings = branch_settings(branch, 1, weight_tag)
    settings["iterations"] = None
    sample = unfold_command(python, script, data_root, response, "ROOT_OUT", 1, settings)
    quoted = []
    for token in sample:
        if(token == "ROOT_OUT"):
            quoted.append('"$ROOT"')
        elif((token == "1") and (len(quoted) > 0) and (quoted[-1] == shell_quote("-b"))):
            quoted.append('"$BIN"')
        else:
            quoted.append(shell_quote(token))
    case_lines, bi_suffix = iteration_shell(branch)
    lines = [
        "#!/bin/bash",
        "#SBATCH --ntasks=1",
        "#SBATCH --cpus-per-task=1",
        "#SBATCH --job-name=%s" % job_name,
        "#SBATCH --output=%s" % os.path.join(log_dir, job_name + "-%A_%a.out"),
        "#SBATCH --error=%s" % os.path.join(log_dir, job_name + "-%A_%a.err"),
        "#SBATCH --partition=production",
        "#SBATCH --account=clas12",
        "#SBATCH --mem-per-cpu=%s" % SLURM_MEM,
        "#SBATCH --time=%s" % SLURM_TIME,
        "#SBATCH --array=1-17",
        "set -euo pipefail",
        'BIN="${SLURM_ARRAY_TASK_ID}"',
        'PAD=$(printf "%02d" "$BIN")',
        'ROOT="%s"' % os.path.join(parts_dir, stem + "_q2y${PAD}.root"),
    ]
    lines.extend(case_lines)
    lines.append(" ".join(quoted) + bi_suffix)
    lines.append("")
    return "\n".join(lines)


def output_counts(weight_mode):
    if(weight_mode == "both"):
        arrays = 74
    elif(weight_mode in ["unweighted", "weighted"]):
        arrays = 41
    else:
        raise ValueError("unknown weight mode %s" % weight_mode)
    return arrays, arrays * 17, arrays


def campaign_directory(data_root, campaign):
    base = None
    try:
        from jlab_work_paths import data_root_path
        root = data_root_path(data_root)
        if(os.path.isdir(root)):
            base = os.path.join(root, "SIDIS_Campaign", "systematics", str(campaign))
    except Exception:
        base = None
    if(base is None):
        base = os.path.join("/tmp", "SIDIS_systematics_campaign", str(data_root), str(campaign))
    os.makedirs(base, exist_ok=True)
    return base


def assign_hpp(configs, data_root, tag, campaign, stamp, regenerate):
    pure, comb = hpp_pair(data_root, tag)
    nominal_comb = comb
    if(regenerate):
        nominal_comb = regen_spline_path(data_root, tag, campaign, stamp)
    assigned = {}
    for config in configs:
        assigned[config["id"]] = {
            "hpp_nospline": pure,
            "hpp_spline": nominal_comb if(config["nominal"]) else comb,
        }
    return assigned


def keep_recorded_hpp(previous, assigned):
    # Resume must pass the paths stored at launch, not a newly resolved tag.
    if(not isinstance(previous, dict)):
        return assigned
    merged = {}
    for config_id, fresh in assigned.items():
        old = previous.get(config_id) or {}
        merged[config_id] = {
            "hpp_nospline": old.get("hpp_nospline") or fresh["hpp_nospline"],
            "hpp_spline": old.get("hpp_spline") or fresh["hpp_spline"],
        }
    return merged


def build_manifest(data_root, campaign, weight_mode, cap, tag, regenerate, stamp, previous=None, recovery=None):
    batch_by_id = None
    job_by_id = None
    if(recovery is None):
        configs = phase1_configs()
    else:
        # The JSON is the execution set. Nominal and unlisted configs are not added.
        regenerate = False
        picked = recovery_configs(recovery)
        configs = []
        batch_by_id = {}
        job_by_id = {}
        for item in picked:
            config = item["config"]
            configs.append(config)
            batch_by_id[config["id"]] = item["batches"]
            job_by_id[config["id"]] = item["original_job"]
    assigned = assign_hpp(configs, data_root, tag, campaign, stamp, regenerate)
    if(previous is not None):
        old_phase1 = {}
        for row in previous.get("phase1", []):
            old_phase1[row["id"]] = row
        assigned = keep_recorded_hpp(old_phase1, assigned)
    camp = campaign_directory(data_root, campaign)
    parts = os.path.join(camp, "unfold_parts")
    unfold = os.path.join(camp, "unfolded")
    phase1 = []
    phase2 = []
    old_phase1 = {}
    old_phase2 = {}
    if(isinstance(previous, dict)):
        for row in previous.get("phase1", []):
            old_phase1[row["id"]] = row
        for row in previous.get("phase2", []):
            old_phase2[row["key"]] = row
    for config in configs:
        paths = assigned[config["id"]]
        response = response_path(data_root, config["id"], config["cut"])
        if(batch_by_id is None):
            cmd = phase1_command("PYTHON", "SUBMIT", data_root, campaign, cap, config, paths["hpp_nospline"], paths["hpp_spline"])
        else:
            cmd = recovery_phase1_command(
                "PYTHON", "SUBMIT", data_root, campaign, config, paths["hpp_nospline"], paths["hpp_spline"],
                batch_by_id[config["id"]], recovery.get("hybrid_date") or "10_27_2026",
                recovery.get("slurm_time") or "24:00:00", recovery.get("only3d_slurm_mem") or "4500M",
            )
        row = {
            "id": config["id"],
            "cut": config["cut"],
            "nominal": config["nominal"],
            "unsmeared": config["unsmeared"],
            "hpp_nospline": paths["hpp_nospline"],
            "hpp_spline": paths["hpp_spline"],
            "response": response,
            "command": cmd,
            "status": "planned",
            "pid": None,
            "reason": "",
        }
        if(batch_by_id is not None):
            row["batch_ids"] = batch_by_id[config["id"]]
            row["original_job"] = job_by_id[config["id"]]
        old = old_phase1.get(config["id"])
        if(isinstance(old, dict) and (old.get("status") in ["success", "failed", "running"])):
            row["status"] = old.get("status")
            row["pid"] = old.get("pid")
            row["reason"] = old.get("reason") or ""
            row["hpp_nospline"] = old.get("hpp_nospline") or row["hpp_nospline"]
            row["hpp_spline"] = old.get("hpp_spline") or row["hpp_spline"]
            if(batch_by_id is None):
                row["command"] = phase1_command("PYTHON", "SUBMIT", data_root, campaign, cap, config, row["hpp_nospline"], row["hpp_spline"])
            else:
                row["command"] = recovery_phase1_command(
                    "PYTHON", "SUBMIT", data_root, campaign, config, row["hpp_nospline"], row["hpp_spline"],
                    row["batch_ids"], recovery.get("hybrid_date") or "10_27_2026",
                    recovery.get("slurm_time") or "24:00:00", recovery.get("only3d_slurm_mem") or "4500M",
                )
        phase1.append(row)
        for job in phase2_jobs(config, weight_mode):
            key = job_key(job)
            bins = {}
            for q2y in Q2Y_BINS:
                bins[str(q2y)] = {
                    "status": "pending",
                    "root": bin_root(parts, job, q2y),
                    "slurm_state": "",
                    "where": "",
                }
            prow = {
                "key": key,
                "config_id": job["config_id"],
                "branch": job["branch"],
                "weight_tag": job["weight_tag"],
                "weight_label": weight_label(job["weight_tag"]),
                "lineage": job["lineage"],
                "local_order": job["local_order"],
                "response": response,
                "final": final_root(unfold, job),
                "array_id": "",
                "submit_time": None,
                "status": "waiting_phase1",
                "bins": bins,
                "reason": "",
            }
            old = old_phase2.get(key)
            if(isinstance(old, dict)):
                prow["status"] = old.get("status") or prow["status"]
                prow["array_id"] = old.get("array_id") or ""
                prow["submit_time"] = old.get("submit_time")
                prow["reason"] = old.get("reason") or ""
                old_bins = old.get("bins") or {}
                for q2y in Q2Y_BINS:
                    if(str(q2y) in old_bins):
                        prow["bins"][str(q2y)]["status"] = old_bins[str(q2y)].get("status") or "pending"
                        prow["bins"][str(q2y)]["where"] = old_bins[str(q2y)].get("where") or ""
                        prow["bins"][str(q2y)]["slurm_state"] = old_bins[str(q2y)].get("slurm_state") or ""
            phase2.append(prow)
    payload = {
        "campaign": campaign,
        "data_root": data_root,
        "weight_mode": weight_mode,
        "max_local_workers": cap,
        "hpp_tag": tag,
        "regenerate_nominal_spline_hpp": bool(regenerate),
        "phase1": phase1,
        "phase2": phase2,
    }
    if(recovery is not None):
        task_count = 0
        for row in phase1:
            task_count += len(expand_batch_spec(row["batch_ids"]))
        payload["recovery"] = True
        payload["recovery_file"] = recovery.get("path") or ""
        payload["hybrid_date"] = recovery.get("hybrid_date") or "10_27_2026"
        payload["slurm_time"] = recovery.get("slurm_time") or "24:00:00"
        payload["only3d_slurm_mem"] = recovery.get("only3d_slurm_mem") or "4500M"
        payload["recovery_task_count"] = task_count
    return payload


def manifest_path(camp_dir):
    return os.path.join(camp_dir, "manifest.json")


def log_path(camp_dir):
    return os.path.join(camp_dir, "campaign.log")


def write_manifest(camp_dir, payload):
    path = manifest_path(camp_dir)
    tmp = path + ".tmp"
    handle = open(tmp, "w")
    json.dump(payload, handle, indent=2)
    handle.write("\n")
    handle.close()
    os.replace(tmp, path)
    return path


def read_manifest(camp_dir):
    path = manifest_path(camp_dir)
    if(not os.path.isfile(path)):
        return None
    handle = open(path)
    payload = json.load(handle)
    handle.close()
    return payload


def append_log(camp_dir, phase, config_id, branch, weight, q2y, where, slurm_id, status, reason, output):
    path = log_path(camp_dir)
    os.makedirs(camp_dir, exist_ok=True)
    fields = [
        time.strftime("%Y-%m-%dT%H:%M:%S"),
        str(phase), str(config_id), str(branch), str(weight),
        "" if(q2y in [None, ""]) else str(q2y),
        str(where), str(slurm_id), str(status),
        str(reason).replace("\t", " ").replace("\n", " "),
        str(output),
    ]
    line = "\t".join(fields) + "\n"
    handle = open(path, "a")
    try:
        if(fcntl is not None):
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        handle.write(line)
        handle.flush()
    finally:
        if(fcntl is not None):
            try:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
            except Exception:
                pass
        handle.close()


def key_has_q2y(name, q2y):
    token = "Q2_y_Bin_%d" % int(q2y)
    start = 0
    text = str(name)
    while(True):
        pos = text.find(token, start)
        if(pos < 0):
            return False
        end = pos + len(token)
        if((end >= len(text)) or (not text[end].isdigit())):
            return True
        start = pos + 1
    return False


def missing_q2y_bins(names, bins):
    missing = []
    for q2y in bins:
        found = False
        for name in names:
            if(key_has_q2y(name, q2y)):
                found = True
                break
        if(not found):
            missing.append(int(q2y))
    return missing


def file_nonempty(path):
    return os.path.isfile(path) and (os.path.getsize(path) > 0)


def root_key_names(path):
    import ROOT
    ROOT.gErrorIgnoreLevel = ROOT.kError
    handle = ROOT.TFile.Open(path, "READ")
    if((handle is None) or handle.IsZombie()):
        return None
    names = []
    keys = handle.GetListOfKeys()
    if(keys is not None):
        for key in keys:
            names.append(key.GetName())
    handle.Close()
    return names


def unfold_bin_ok(path, q2y):
    if(not file_nonempty(path)):
        return False
    try:
        names = root_key_names(path)
    except Exception:
        return False
    if(names is None):
        return False
    return key_has_q2y_any(names, q2y)


def key_has_q2y_any(names, q2y):
    for name in names:
        if(key_has_q2y(name, q2y)):
            return True
    return False


def unfold_final_ok(path, bins=None):
    if(bins is None):
        bins = Q2Y_BINS
    if(not file_nonempty(path)):
        return False
    try:
        names = root_key_names(path)
    except Exception:
        return False
    if(names is None):
        return False
    return len(missing_q2y_bins(names, bins)) == 0


def command_text(cmd):
    return " ".join(str(token) for token in cmd)


def submission_history_path(camp_dir):
    return os.path.join(camp_dir, "submission_history.jsonl")


def append_submission_history(camp_dir, record):
    # Append one JSON line. Earlier lines stay as they were written.
    path = submission_history_path(camp_dir)
    os.makedirs(camp_dir, exist_ok=True)
    handle = open(path, "a+")
    try:
        if(fcntl is not None):
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        handle.seek(0)
        existing = handle.read().splitlines()
        attempt = 1
        for line in existing:
            if(line.strip() == ""):
                continue
            try:
                old = json.loads(line)
            except Exception:
                continue
            same = (old.get("campaign") == record.get("campaign")) and (old.get("configuration") == record.get("configuration")) and (old.get("phase") == record.get("phase")) and (old.get("job_name") == record.get("job_name")) and (old.get("index_spec") == record.get("index_spec"))
            if(same):
                attempt += 1
        payload = dict(record)
        if(payload.get("attempt") in [None, ""]):
            payload["attempt"] = attempt
        if(payload.get("time") in [None, ""]):
            payload["time"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        handle.seek(0, os.SEEK_END)
        handle.write(json.dumps(payload, sort_keys=True) + "\n")
        handle.flush()
    finally:
        if(fcntl is not None):
            try:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
            except Exception:
                pass
        handle.close()
    return path


def submission_ids_for_config(camp_dir, configuration):
    path = submission_history_path(camp_dir)
    found = []
    if(not os.path.isfile(path)):
        return found
    handle = open(path)
    try:
        for line in handle:
            if(line.strip() == ""):
                continue
            try:
                row = json.loads(line)
            except Exception:
                continue
            if(str(row.get("configuration")) != str(configuration)):
                continue
            slurm_id = str(row.get("slurm_id") or "")
            if((slurm_id not in ["", "None"]) and (slurm_id not in found)):
                found.append(slurm_id)
    finally:
        handle.close()
    return found


def recovery_failure_text(campaign, configuration, batch_ids, slurm_ids, reason):
    if(len(slurm_ids) > 0):
        id_text = ", ".join(str(item) for item in slurm_ids)
    else:
        id_text = "none"
    return "campaign %s\nconfiguration %s\nslurm_ids %s\nrecovery_batches %s\n%s\n" % (
        campaign, configuration, id_text, batch_ids, reason)


def phase2_history_record(manifest, row, array_id):
    return {
        "campaign": manifest["campaign"],
        "configuration": row["config_id"],
        "phase": "phase2",
        "job_name": job_stem(row),
        "slurm_id": str(array_id),
        "index_spec": "1-17",
        "memory": SLURM_MEM,
        "wall": SLURM_TIME,
        "cpus": "1",
    }


def self_test():
    rows = phase1_configs()
    if(len(rows) != 34):
        raise SystemExit("Phase 1 count is %s" % len(rows))
    ids = [row["id"] for row in rows]
    if(len(set(ids)) != 34):
        raise SystemExit("Phase 1 ids are not unique")
    cuts = [row["cut"] for row in rows]
    if(DEFAULT_CUT not in cuts):
        raise SystemExit("nominal cut missing")
    if("cut_Complete_SIDIS_chi2_strict_pip" not in cuts):
        raise SystemExit("strict chi2 cut missing")
    if(any(("pass1" in cut) or ("MM_" in cut) for cut in cuts)):
        raise SystemExit("excluded cut was scheduled")
    if(any("removed" in row["id"] for row in rows)):
        raise SystemExit("chi2-removed config is present")
    smear = [row for row in rows if(row["id"] == "noSmear")]
    if((len(smear) != 1) or (not smear[0]["unsmeared"]) or (smear[0]["cut"] != "cut_Complete_SIDIS_noSmear")):
        raise SystemExit("noSmear is not paired with unsmeared")
    if(len(phase2_branches()) != 7):
        raise SystemExit("Phase 2 branch count is not 7")
    if("Phi6" in phase2_branches()):
        raise SystemExit("Phi6 was enabled")
    if(nominal_iterations(1) != 6) or (nominal_iterations(5) != 6) or (nominal_iterations(2) != 5):
        raise SystemExit("nominal iteration map is wrong")
    if(branch_settings("BayesMinus1", 1, "AccSpline")["iterations"] != 5):
        raise SystemExit("BayesMinus1 bin 1")
    if(branch_settings("BayesPlus1", 4, "AccSpline")["iterations"] != 6):
        raise SystemExit("BayesPlus1 other bin")
    if(branch_settings("Acc015", 3, "AccSpline")["acceptance"] != 0.015):
        raise SystemExit("Acc015")
    if(branch_settings("Acc025", 3, "AccSpline")["acceptance"] != 0.025):
        raise SystemExit("Acc025")
    if(branch_settings("Phi12", 3, "AccSpline")["phi_bins"] != 12):
        raise SystemExit("Phi12")
    if(branch_settings("NoRho0", 3, "AccSpline")["background"] != "None"):
        raise SystemExit("NoRho0")
    if(branch_settings("AcceptanceWeightVariation", 3, "AccSpline")["weight_tag"] != "Spline"):
        raise SystemExit("acceptance-weight tag")
    if(worker_cap(None) != 41):
        raise SystemExit("default cap")
    try:
        worker_cap(42)
        raise SystemExit("cap 42 was accepted")
    except ValueError:
        pass
    if(worker_cap(10) != 10):
        raise SystemExit("lower cap")
    nominal = rows[0]
    other = [row for row in rows if(row["id"] == "dcfid_loose_el")][0]
    nom_jobs = phase2_jobs(nominal, "both")
    if(len(nom_jobs) != 8):
        raise SystemExit("nominal Phase 2 job count %s" % len(nom_jobs))
    if(any(job["branch"] != "inherited" and job["lineage"] == "nominal" for job in nom_jobs)):
        raise SystemExit("a nominal branch reused the nominal lineage")
    if(phase2_jobs(other, "unweighted")[0]["weight_tag"] not in ["", None]):
        raise SystemExit("unweighted tag was set")
    both = phase2_jobs(other, "both")
    if([job["weight_tag"] for job in both] != ["Spline", ""]):
        raise SystemExit("both-mode order is not weighted then unweighted")
    if(len(set(job["lineage"] for job in both)) != 1):
        raise SystemExit("both mode split the lineage")
    if(output_counts("unweighted") != (41, 697, 41)):
        raise SystemExit("unweighted counts")
    if(output_counts("weighted") != (41, 697, 41)):
        raise SystemExit("weighted counts")
    if(output_counts("both") != (74, 1258, 74)):
        raise SystemExit("both counts")
    cmd = phase1_command("python", "Submit_Full_Histogram_Creation_Pipeline.py", "work_b", "demo", 41, other, "/hpp/a_noSpline.hpp", "/hpp/a_withSpline.hpp")
    text = command_text(cmd)
    for token in ["-mac Bank", "-m hybrid", "-j3D 1", "-j2D 0", "-j5D 0", "-j1D 0", "-jdiag 0", "-sa", "-hpf /hpp/a_noSpline.hpp", "-hps /hpp/a_withSpline.hpp", "-cwc 41", "cut_Complete_SIDIS_dcfid_loose_el"]:
        if(token not in text):
            raise SystemExit("Phase 1 command missing %s" % token)
    if(("-us" in cmd) or ("pass1" in text) or ("P12T6" in text)):
        raise SystemExit("Phase 1 command has an excluded flag")
    smear_cmd = phase1_command("python", "submit.py", "work_b", "demo", 41, smear[0], "/a", "/b")
    if("-us" not in smear_cmd):
        raise SystemExit("noSmear command is not unsmeared")
    settings = branch_settings("inherited", 2, "AccSpline")
    unfold = unfold_command("python", "run_Simple_Unfold.py", "work_b", "/in.root", "/out.root", 2, settings)
    utext = command_text(unfold)
    for token in ["-err covariance", "-ac 0.02", "-bgs rho0_new", "-ph 24", "-wt AccSpline", "-u3D", "--skip_compile"]:
        if(token not in utext):
            raise SystemExit("unfold command missing %s" % token)
    if("--iteration_study" in utext) or ("-bi" in unfold):
        raise SystemExit("nominal unfold overrides iterations or starts a study")
    minus = unfold_command("python", "run.py", "work_b", "/in.root", "/out.root", 1, branch_settings("BayesMinus1", 1, "AccSpline"))
    if("-bi 5" not in command_text(minus)):
        raise SystemExit("BayesMinus1 command")
    phi = unfold_command("python", "run.py", "work_b", "/in.root", "/out.root", 1, branch_settings("Phi12", 1, "AccSpline"))
    if("-ph 12" not in command_text(phi)):
        raise SystemExit("Phi12 command")
    if(not key_has_q2y("Histo_Q2_y_Bin_1z_pT_Bin_2", 1)):
        raise SystemExit("bin 1 token")
    if(key_has_q2y("Histo_Q2_y_Bin_10z_pT_Bin_2", 1)):
        raise SystemExit("bin 1 matched bin 10")
    if(missing_q2y_bins(["Q2_y_Bin_1z", "Q2_y_Bin_2z"], [1, 2, 3]) != [3]):
        raise SystemExit("missing bin scan")
    pure, comb = hpp_pair("work_b", "Final_Thesis")
    if((not pure.endswith("generated_acceptance_weights_Final_Thesis_noSpline.hpp")) or (not comb.endswith("generated_acceptance_weights_Final_Thesis_withSpline.hpp"))):
        raise SystemExit("HPP names")
    regen = regen_spline_path("work_b", "Final_Thesis", "demo", "20261027_010203")
    if("sysregen_demo_20261027_010203" not in regen):
        raise SystemExit("regen name")
    if(os.path.basename(regen) == os.path.basename(comb)):
        raise SystemExit("regen path overwrites the existing file")
    manifest = build_manifest("work_b", "demo", "unweighted", 41, "Final_Thesis", True, "20261027_010203")
    nominal_row = [row for row in manifest["phase1"] if(row["id"] == "nominal")][0]
    other_row = [row for row in manifest["phase1"] if(row["id"] == "dcfid_loose_el")][0]
    if(nominal_row["hpp_spline"] == other_row["hpp_spline"]):
        raise SystemExit("nominal regen path was shared")
    if(nominal_row["hpp_nospline"] != other_row["hpp_nospline"]):
        raise SystemExit("noSpline path diverged")
    resumed = build_manifest("work_b", "demo", "unweighted", 41, "OtherTag", True, "19990101_000000", previous=manifest)
    resumed_nom = [row for row in resumed["phase1"] if(row["id"] == "nominal")][0]
    if(resumed_nom["hpp_spline"] != nominal_row["hpp_spline"]):
        raise SystemExit("resume replaced the recorded HPP path")
    if(len(manifest["phase2"]) != 41):
        raise SystemExit("unweighted Phase 2 rows %s" % len(manifest["phase2"]))
    both_manifest = build_manifest("work_b", "demo", "both", 41, "Final_Thesis", False, "stamp")
    if(len(both_manifest["phase2"]) != 74):
        raise SystemExit("both Phase 2 rows %s" % len(both_manifest["phase2"]))
    script = sbatch_script("SysUnfold_nominal", "/logs", "python3", "run_Simple_Unfold.py", "work_b", "/in.root", "/parts", "Sys3D_nominal_inherited_AccSpline", "inherited", "AccSpline")
    bayes_script = sbatch_script("SysUnfold_bayes", "/logs", "python3", "run_Simple_Unfold.py", "work_b", "/in.root", "/parts", "Sys3D_nominal_BayesMinus1_AccSpline", "BayesMinus1", "AccSpline")
    if("1|5) BI=5" not in bayes_script) or ("BI=4" not in bayes_script):
        raise SystemExit("BayesMinus1 sbatch does not vary iterations by bin")
    for token in ["--mem-per-cpu=15000", "--time=1:40:00", "--array=1-17", "--partition=production", "--account=clas12", "-err", "covariance"]:
        if(token not in script):
            raise SystemExit("sbatch missing %s" % token)
    if("--mail-type" in script):
        raise SystemExit("sbatch requests per-task mail")
    if(not script.splitlines()[0].startswith("#!/bin/bash")):
        raise SystemExit("sbatch header")
