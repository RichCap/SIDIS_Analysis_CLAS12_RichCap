#!/usr/bin/env python3
# Command line for the SIDIS physics-results skills. Does not launch fits or farm jobs.

import argparse
import json
import os
import subprocess
import sys

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, THIS_DIR)
import sidis_physics_lib as phys


def write_report(path, payload):
    phys.write_json(path, payload)
    print(path)


def action_resolve(args):
    if(os.path.isfile(args.manifest)):
        handle = open(args.manifest)
        manifest = json.load(handle)
        handle.close()
        manifest = phys.patch_manifest(manifest)
    else:
        manifest = phys.build_manifest(args.unfolded_dir)
        manifest = phys.patch_manifest(manifest)
    if(args.output_dir not in [None, ""]):
        manifest["run"]["output_dir"] = os.path.abspath(args.output_dir)
    if(args.max_concurrent is not None):
        manifest["run"]["max_concurrent"] = int(args.max_concurrent)
    if(args.campaigns not in [None, ""]):
        manifest["run"]["campaigns"] = args.campaigns
    phys.write_json(args.manifest, manifest)
    output_dir = manifest["run"]["output_dir"]
    os.makedirs(output_dir, exist_ok=True)
    work_plan = phys.write_work_plan(manifest, output_dir, manifest["run"]["max_concurrent"])
    jobs = []
    campaigns = ["unweighted", "spline"] if(manifest["run"]["campaigns"] == "both") else [manifest["run"]["campaigns"]]
    for campaign in campaigns:
        jobs.extend(phys.fit_jobs(manifest, campaign))
    shards = phys.shard_jobs(jobs, manifest["run"]["max_concurrent"])
    summary = {
        "manifest": os.path.abspath(args.manifest),
        "spline_nominal": os.path.basename(manifest["nominals"]["spline"]["path"] or ""),
        "unweighted_nominal": os.path.basename(manifest["nominals"]["unweighted"]["path"] or ""),
        "fit_jobs": len(jobs),
        "shards": len(shards),
        "blocked_methods": len(manifest["method_branches_blocked"]),
        "acc_status": [row["path_status"] for row in manifest["variations"] if(row["variation"] == "Acc")][0],
        "radiative": manifest["radiative"]["study_state"],
        "work_plan": work_plan,
        "unweighted_5d": manifest["dimension"]["unweighted"]["path_status"],
        "spline_5d": manifest["dimension"]["spline"]["path_status"],
        "event_ratio": manifest["radiative"]["event_ratio_root"]["path_status"],
    }
    print(json.dumps(summary, sort_keys=True))


def action_radiative(args):
    report = phys.radiative_report(event_ratio_path=args.event_ratio)
    report["study_state"] = "pending"
    report["systematic"] = None
    write_report(args.output, report)


def action_bin_centering(args):
    meta = None
    if((args.event_json not in [None, ""]) and os.path.isfile(args.event_json)):
        handle = open(args.event_json)
        payload = json.load(handle)
        handle.close()
        meta = payload.get("meta", {})
    report = phys.bin_centering_report(meta, args.initial_spline, args.later_spline)
    write_report(args.output, report)


def action_mosaic(args):
    handle = open(args.artifact)
    artifact = json.load(handle)
    handle.close()
    artifact["path"] = args.artifact
    cmd = phys.mosaic_command(artifact, args.spline_overlay, args.spline_prefix, args.campaign)
    print("\n".join(cmd))


def action_run_shard(args):
    # Execute one shard from work_plan.json. Does not unfold or submit farm jobs.
    handle = open(args.work_plan)
    plan = json.load(handle)
    handle.close()
    key = "nominal_shards" if(args.phase == "nominal") else "variation_shards"
    shards = plan[key]
    shard = shards[int(args.shard)]
    output_dir = os.path.dirname(os.path.abspath(args.work_plan))
    registry = phys.PhysicsRegistry(output_dir)
    log_dir = os.path.join(output_dir, "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "%s_shard_%s.log" % (args.phase, args.shard))
    py = "/Users/richardcapobianco/opt/miniforge3/envs/updated_python/bin/python"
    root_build = os.path.join(phys.ANALYSIS_ROOT, "New_RooUnfold", "RooUnfold", "build-arm64")
    env = os.environ.copy()
    env["PYTHONPATH"] = root_build + (os.pathsep + env["PYTHONPATH"] if(env.get("PYTHONPATH")) else "")
    env["LD_LIBRARY_PATH"] = root_build + (os.pathsep + env["LD_LIBRARY_PATH"] if(env.get("LD_LIBRARY_PATH")) else "")
    env["DYLD_LIBRARY_PATH"] = root_build + (os.pathsep + env["DYLD_LIBRARY_PATH"] if(env.get("DYLD_LIBRARY_PATH")) else "")
    log = open(log_path, "a")
    for job in shard:
        fingerprint = phys.file_fingerprint(job["input_path"])
        wanted = {
            "stage": "fit",
            "producer": "run_shard",
            "campaign": job["campaign"],
            "source": job["source"],
            "variation": job["variation"],
            "method": job["method"],
            "acceptance_weight": job["weight_tag"],
            "input_size": fingerprint["size"],
            "input_mtime": fingerprint["mtime"],
            "config_fingerprint": phys.fit_config_fingerprint(job),
            "match": "%s|%s|%s" % (job["campaign"], job["source"], job["variation"]),
        }
        if((not args.force) and (registry.find_reusable(wanted, False) is not None)):
            log.write("reuse %s %s\n" % (job["campaign"], job["variation"]))
            log.flush()
            continue
        copy_root = phys.copy_input_for_fit(job, output_dir)
        json_out = os.path.join(os.path.dirname(copy_root), "fit.json")
        init_file = None
        if(job["kind"] == "variation"):
            nominal_json = os.path.join(output_dir, "fits", job["campaign"], "nominal", "nominal", "fit.json")
            if(not os.path.isfile(nominal_json)):
                log.write("blocked %s waiting for nominal json\n" % job["variation"])
                log.flush()
                registry.append({"status": "blocked", "stage": "fit", "campaign": job["campaign"], "source": job["source"], "variation": str(job["variation"]), "validation": "missing_nominal"})
                continue
            init_file = os.path.join(os.path.dirname(copy_root), "nominal_init.py")
            phys.init_module_from_nominal_json(nominal_json, init_file)
        cmd = phys.plan_fit_command(job, copy_root, json_out, init_file)
        cmd = [py] + cmd
        log.write("start %s\n" % " ".join(cmd))
        log.flush()
        proc = subprocess.run(cmd, cwd=phys.ANALYSIS_ROOT, env=env, stdout=log, stderr=log)
        n_cells = 0
        fit_key = phys.expected_fit_key(job)
        if((proc.returncode == 0) and os.path.isfile(json_out)):
            payload = json.load(open(json_out))
            n_cells = len(payload.get(fit_key, {}))
        record = dict(wanted)
        record["status"] = "completed" if((proc.returncode == 0) and (n_cells > 0)) else "failed"
        record["validation"] = "ok" if(record["status"] == "completed") else ("empty_fit" if(proc.returncode == 0) else "failed")
        record["returncode"] = proc.returncode
        record["n_cells"] = n_cells
        record["fit_key"] = fit_key
        record["output"] = json_out
        record["iteration_mismatch_bins"] = job.get("iteration_mismatch_bins", [])
        registry.append(record)
        log.write("done %s rc=%s\n" % (job["variation"], proc.returncode))
        log.flush()
    log.close()
    print(log_path)


def action_fit_plan(args):
    job = {
        "kind": args.kind,
        "campaign": args.campaign,
        "source": args.source,
        "variation": args.variation,
        "weight_tag": "" if(args.weight_tag == "unweighted") else args.weight_tag,
        "nominal_tag": "" if(args.nominal_tag == "unweighted") else args.nominal_tag,
        "method": args.method,
        "input_path": os.path.abspath(args.input),
    }
    if(not phys.weight_pair_allowed(job["source"] if(job["kind"] == "variation") else "nominal", job["nominal_tag"], job["weight_tag"])):
        raise SystemExit("Rejected weight pair %s -> %s for source %s." % (job["nominal_tag"], job["weight_tag"], job["source"]))
    copy_root = phys.fit_output_root(args.output_dir, job)
    json_out = os.path.join(os.path.dirname(copy_root), "fit.json")
    cmd = phys.plan_fit_command(job, copy_root, json_out, args.fit_init_file)
    print("\n".join(cmd))


def main():
    parser = argparse.ArgumentParser(description="SIDIS physics-results helpers. Does not run the fitting campaign.")
    sub = parser.add_subparsers(dest="action", required=True)
    resolve = sub.add_parser("resolve")
    resolve.add_argument("-m", "--manifest", required=True)
    resolve.add_argument("-u", "--unfolded_dir", default=None)
    resolve.add_argument("-o", "--output_dir", default=None)
    resolve.add_argument("-mc", "--max_concurrent", type=int, default=None)
    resolve.add_argument("-c", "--campaigns", default=None)
    resolve.set_defaults(func=action_resolve)
    radiative = sub.add_parser("radiative")
    radiative.add_argument("-o", "--output", required=True)
    radiative.add_argument("-er", "--event_ratio", default=None)
    radiative.set_defaults(func=action_radiative)
    centering = sub.add_parser("bin_centering")
    centering.add_argument("-o", "--output", required=True)
    centering.add_argument("-ej", "--event_json", default=phys.BC_EVENT_JSON)
    centering.add_argument("-is", "--initial_spline", default=None)
    centering.add_argument("-ls", "--later_spline", default=None)
    centering.set_defaults(func=action_bin_centering)
    mosaic = sub.add_parser("mosaic")
    mosaic.add_argument("-a", "--artifact", required=True)
    mosaic.add_argument("-c", "--campaign", required=True)
    mosaic.add_argument("-so", "--spline_overlay", action="store_true")
    mosaic.add_argument("-sp", "--spline_prefix", default=phys.SPLINE_PREFIX)
    mosaic.set_defaults(func=action_mosaic)
    fit_plan = sub.add_parser("fit_plan")
    fit_plan.add_argument("-k", "--kind", required=True, choices=["nominal", "variation"])
    fit_plan.add_argument("-c", "--campaign", required=True)
    fit_plan.add_argument("-s", "--source", required=True)
    fit_plan.add_argument("-v", "--variation", required=True)
    fit_plan.add_argument("-wt", "--weight_tag", required=True)
    fit_plan.add_argument("-nt", "--nominal_tag", required=True)
    fit_plan.add_argument("-md", "--method", required=True, choices=["Bayesian", "Bin"])
    fit_plan.add_argument("-i", "--input", required=True)
    fit_plan.add_argument("-o", "--output_dir", required=True)
    fit_plan.add_argument("-fi", "--fit_init_file", default=None)
    fit_plan.set_defaults(func=action_fit_plan)
    run_shard = sub.add_parser("run_shard")
    run_shard.add_argument("-w", "--work_plan", required=True)
    run_shard.add_argument("-p", "--phase", required=True, choices=["nominal", "variation"])
    run_shard.add_argument("-s", "--shard", required=True, type=int)
    run_shard.add_argument("-f", "--force", action="store_true")
    run_shard.set_defaults(func=action_run_shard)
    args = parser.parse_args()
    args.func(args)


if(__name__ == "__main__"):
    main()
