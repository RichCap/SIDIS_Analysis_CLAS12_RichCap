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
    report["subdivisions"] = phys.discover_bc_subdivisions()
    write_report(args.output, report)


def action_mosaic(args):
    handle = open(args.artifact)
    artifact = json.load(handle)
    handle.close()
    artifact["path"] = args.artifact
    if((args.x_mode not in [None, ""]) and (args.uncertainty not in [None, ""])):
        commands = [phys.mosaic_command(artifact, args.spline_overlay, args.spline_prefix, args.campaign, args.x_mode, args.uncertainty)]
    else:
        commands = phys.mosaic_command_set(artifact, args.spline_overlay, args.spline_prefix, args.campaign)
    if(args.test):
        cmd = commands[0] + ["--test"]
        py = "/Users/richardcapobianco/opt/miniforge3/envs/updated_python/bin/python"
        proc = subprocess.run([py] + cmd, cwd=phys.ANALYSIS_ROOT)
        if(proc.returncode != 0):
            raise SystemExit(proc.returncode)
        print("mosaic test ok")
        return
    for cmd in commands:
        print(" ".join(cmd))
        print("")


def action_record_agent(args):
    path = phys.write_agent_report(args.output_dir, args.run_id, args.stage, args.campaign, args.source_or_shard, args.label, args.body)
    print(path)


def action_record_refinement(args):
    handle = open(args.note)
    note = json.load(handle)
    handle.close()
    plan_handle = open(args.work_plan)
    plan = json.load(plan_handle)
    plan_handle.close()
    fit_payload = json.load(open(args.fit_json))
    init_text = ""
    if(os.path.isfile(args.refine_init)):
        init_text = open(args.refine_init).read()
    classified = phys.classify_refinement_dir(note, fit_payload, init_text, 0)
    output_dir = os.path.dirname(os.path.abspath(args.work_plan))
    registry = phys.PhysicsRegistry(output_dir)
    label = classified["classification"]
    if(label == "verified"):
        status, validation, refinement_status = "completed", "ok", "refined"
    elif(label == "unverifiable"):
        status, validation, refinement_status = "completed_partial", "unverifiable", "unverifiable"
    else:
        status, validation, refinement_status = "failed", "incomplete", "incomplete"
    record = {
        "stage": "refine",
        "producer": "record_refinement",
        "campaign": args.campaign,
        "source": args.source,
        "variation": str(args.variation),
        "match": "%s|%s|%s" % (args.campaign, args.source, args.variation),
        "config_fingerprint": "refined",
        "status": status,
        "validation": validation,
        "refinement_status": refinement_status,
        "run_id": plan.get("run_id", ""),
        "audit_reason": classified["reason"],
    }
    registry.append(record)
    print(label)
    if(label == "incomplete"):
        raise SystemExit("refinement evidence is incomplete: %s" % classified["reason"])
    if(label == "unverifiable"):
        print("not fully validated: %s" % classified["minimum_check"])


def action_audit_refinements(args):
    import sidis_physics_extensions as ext
    summary = ext.write_audit(args.output_dir, args.manifest)
    print(json.dumps(summary, sort_keys=True))


def action_world_comparisons(args):
    import sidis_physics_extensions as ext
    report = ext.world_comparison_report(args.output_dir)
    path = os.path.join(args.output_dir, "reports", "world_comparisons.md")
    print(ext.write_stage_report(path, report["markdown"]))
    print(report["status"])
    if(report["blocker"] != ""):
        print(report["blocker"])


def action_theory_comparisons(args):
    import sidis_physics_extensions as ext
    report = ext.theory_comparison_report(args.output_dir)
    path = os.path.join(args.output_dir, "reports", "theory_comparisons.md")
    print(ext.write_stage_report(path, report["markdown"]))
    print(report["status"])


def action_fixed_point_run(args):
    if(args.enable != "yes"):
        raise SystemExit("fixed_point_run refuses to start unless --enable yes is passed")
    import sidis_physics_extensions as ext
    limit = resolve_worker_count_from_args(args)
    jobs = fixed_point_jobs_from_args(args)
    summary = ext.run_fixed_point_pool(
        jobs,
        args.cache_dir,
        args.log_dir,
        limit["workers"],
        phys.skill_input_fingerprint(),
        ext.correct_py_command,
        retry_failed=args.retry_failed,
        timeout_s=args.timeout_s,
    )
    summary["clamped"] = limit["clamped"]
    print(json.dumps(summary, sort_keys=True))
    if((summary["failed"] > 0) or (summary["left_failed"] > 0) or (summary.get("stopped", 0) > 0)):
        raise SystemExit("fixed-point grid is incomplete")


def resolve_worker_count_from_args(args):
    return phys.resolve_worker_count(args.mode, args.sf, args.workers, allow_untested=args.allow_untested)


def fixed_point_jobs_from_args(args):
    bins = phys.nominal_analysis_bins()
    if(args.limit is not None):
        bins = bins[:int(args.limit)]
    jobs = []
    for q2y_bin, zpt_bin in bins:
        for phi_bin in range(1, 25):
            jobs.append({"mode": args.mode, "sf": args.sf, "q2y": q2y_bin, "zpt": zpt_bin, "phi": phi_bin})
    return jobs


def action_radiative_grids(args):
    if(args.enable != "yes"):
        raise SystemExit("radiative_grids refuses to start unless --enable yes is passed")
    import sidis_physics_extensions as ext
    jobs_sf0 = []
    jobs_sf2 = []
    bins = phys.nominal_analysis_bins()
    if(args.limit is not None):
        bins = bins[:int(args.limit)]
    for q2y_bin, zpt_bin in bins:
        for phi_bin in range(1, 25):
            jobs_sf0.append({"mode": "RC", "sf": 0, "q2y": q2y_bin, "zpt": zpt_bin, "phi": phi_bin})
            jobs_sf2.append({"mode": "RC", "sf": 2, "q2y": q2y_bin, "zpt": zpt_bin, "phi": phi_bin})
    lock_path = args.lock_path if(args.lock_path not in [None, ""]) else os.path.join(args.cache_dir, "rc_grid.lock")
    status = ext.run_radiative_grids(
        jobs_sf0,
        jobs_sf2,
        args.cache_dir,
        args.log_dir,
        args.workers,
        phys.skill_input_fingerprint(),
        ext.correct_py_command,
        lock_path,
        wait_for_lock=(not args.no_wait_for_lock),
        retry_failed=args.retry_failed,
        timeout_s=args.timeout_s,
    )
    print(json.dumps({"complete": status["complete"], "reason": status["reason"], "sf2_workers": status["sf2_workers"]}, sort_keys=True))
    if(not status["complete"]):
        raise SystemExit("radiative grids incomplete: %s" % status["reason"])


def action_sf2_benchmark(args):
    if(args.confirm_benchmark != "yes"):
        raise SystemExit("sf2_benchmark refuses to start unless --confirm_benchmark yes is passed")
    import sidis_physics_extensions as ext
    report = ext.run_sf2_concurrency_benchmark(args.cache_dir, [1, 2, 3, 4, 5])
    phys.write_json(args.report, report)
    print(json.dumps({"recommended_workers": report["recommended_workers"], "report": args.report}, sort_keys=True))


def action_thesis_plan(args):
    import sidis_physics_extensions as ext
    thesis_root = args.thesis_root if(args.thesis_root not in [None, ""]) else ext.THESIS_ROOT
    text = ext.thesis_plan_markdown(args.output_dir, thesis_root)
    path = os.path.join(args.output_dir, "reports", "SIDIS_Thesis_Integration_Plan.md")
    print(ext.write_stage_report(path, text))


def action_report_markdown(args):
    import sidis_physics_reports as reports
    print(reports.write_markdown(args.output_dir, args.run_id))


def action_report_pptx(args):
    import sidis_physics_reports as reports
    print(reports.write_pptx(args.output_dir, args.run_id))


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
        fitted_bins = []
        if((proc.returncode == 0) and os.path.isfile(json_out)):
            payload = json.load(open(json_out))
            fitted_bins = list(payload.get(fit_key, {}).keys())
            n_cells = len(fitted_bins)
        coverage = None
        if(proc.returncode == 0):
            expected_rows = phys.scan_fit_family(copy_root, fit_key)
            coverage = phys.classify_fit_coverage(expected_rows, fitted_bins)
            phys.write_json(os.path.join(os.path.dirname(json_out), "fit_coverage.json"), coverage)
        record = dict(wanted)
        if(proc.returncode != 0):
            record["status"] = "failed"
            record["validation"] = "failed"
        elif(coverage is None):
            record["status"] = "failed"
            record["validation"] = "empty_fit"
        else:
            record["status"] = coverage["status"]
            record["validation"] = "ok" if(coverage["status"] in ["completed", "completed_partial"]) else "empty_fit"
        record["returncode"] = proc.returncode
        record["n_cells"] = n_cells
        record["na"] = None if(coverage is None) else coverage["na"]
        record["other_failure"] = None if(coverage is None) else coverage["other_failure"]
        record["fit_key"] = fit_key
        record["refinement_status"] = "initial_fit"
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
    mosaic.add_argument("-x", "--x_mode", default="")
    mosaic.add_argument("-u", "--uncertainty", default="")
    mosaic.add_argument("-t", "--test", action="store_true")
    mosaic.set_defaults(func=action_mosaic)
    record_agent = sub.add_parser("record_agent")
    record_agent.add_argument("-o", "--output_dir", required=True)
    record_agent.add_argument("-r", "--run_id", required=True)
    record_agent.add_argument("-st", "--stage", required=True)
    record_agent.add_argument("-c", "--campaign", required=True)
    record_agent.add_argument("-ss", "--source_or_shard", required=True)
    record_agent.add_argument("-l", "--label", required=True)
    record_agent.add_argument("-b", "--body", required=True)
    record_agent.set_defaults(func=action_record_agent)
    record_refinement = sub.add_parser("record_refinement")
    record_refinement.add_argument("-w", "--work_plan", required=True)
    record_refinement.add_argument("-c", "--campaign", required=True)
    record_refinement.add_argument("-s", "--source", required=True)
    record_refinement.add_argument("-v", "--variation", required=True)
    record_refinement.add_argument("-n", "--note", required=True)
    record_refinement.add_argument("-fj", "--fit_json", required=True)
    record_refinement.add_argument("-ri", "--refine_init", required=True)
    record_refinement.set_defaults(func=action_record_refinement)
    audit = sub.add_parser("audit_refinements")
    audit.add_argument("-o", "--output_dir", required=True)
    audit.add_argument("-m", "--manifest", required=True)
    audit.set_defaults(func=action_audit_refinements)
    world = sub.add_parser("world_comparisons")
    world.add_argument("-o", "--output_dir", required=True)
    world.set_defaults(func=action_world_comparisons)
    theory = sub.add_parser("theory_comparisons")
    theory.add_argument("-o", "--output_dir", required=True)
    theory.set_defaults(func=action_theory_comparisons)
    thesis = sub.add_parser("thesis_integration_plan")
    thesis.add_argument("-o", "--output_dir", required=True)
    thesis.add_argument("-t", "--thesis_root", default="")
    thesis.set_defaults(func=action_thesis_plan)
    fixed = sub.add_parser("fixed_point_run")
    fixed.add_argument("-en", "--enable", default="no")
    fixed.add_argument("-m", "--mode", required=True, choices=["RC", "BC"])
    fixed.add_argument("-s", "--sf", type=int, default=0)
    fixed.add_argument("-w", "--workers", type=int, default=None)
    fixed.add_argument("-cd", "--cache_dir", required=True)
    fixed.add_argument("-ld", "--log_dir", required=True)
    fixed.add_argument("-n", "--limit", type=int, default=None)
    fixed.add_argument("-rf", "--retry_failed", action="store_true")
    fixed.add_argument("-au", "--allow_untested", action="store_true")
    fixed.add_argument("-to", "--timeout_s", type=int, default=120)
    fixed.set_defaults(func=action_fixed_point_run)
    grids = sub.add_parser("radiative_grids")
    grids.add_argument("-en", "--enable", default="no")
    grids.add_argument("-w", "--workers", type=int, default=None)
    grids.add_argument("-cd", "--cache_dir", required=True)
    grids.add_argument("-ld", "--log_dir", required=True)
    grids.add_argument("-lk", "--lock_path", default="")
    grids.add_argument("-nw", "--no_wait_for_lock", action="store_true")
    grids.add_argument("-n", "--limit", type=int, default=None)
    grids.add_argument("-rf", "--retry_failed", action="store_true")
    grids.add_argument("-to", "--timeout_s", type=int, default=120)
    grids.set_defaults(func=action_radiative_grids)
    bench = sub.add_parser("sf2_benchmark")
    bench.add_argument("-cb", "--confirm_benchmark", default="no")
    bench.add_argument("-cd", "--cache_dir", required=True)
    bench.add_argument("-r", "--report", required=True)
    bench.set_defaults(func=action_sf2_benchmark)
    report_md = sub.add_parser("report_markdown")
    report_md.add_argument("-o", "--output_dir", required=True)
    report_md.add_argument("-r", "--run_id", required=True)
    report_md.set_defaults(func=action_report_markdown)
    report_pptx = sub.add_parser("report_pptx")
    report_pptx.add_argument("-o", "--output_dir", required=True)
    report_pptx.add_argument("-r", "--run_id", required=True)
    report_pptx.set_defaults(func=action_report_pptx)
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
