#!/usr/bin/env python3
# Unattended SWIF2 recovery. Production does not need -ft.
import json
import os
import shlex
import shutil
import subprocess
import time

from Campaign.registry import Registry

RAM_CEILING_BYTES = 32 * (1024 ** 3)
TIME_CEILING_SECS = 24 * 3600
MAX_ATTEMPTS = 3
OOM_PROBLEMS = set(["SLURM_OUT_OF_MEMORY"])
TIME_PROBLEMS = set(["SLURM_TIMEOUT"])
TRANSIENT_PROBLEMS = set(["SWIF_SYSTEM_ERROR", "SLURM_NODE_FAIL", "SITE_PREP_FAIL", "SITE_LAUNCH_FAIL"])
ACTIVE_STATES = set(["pending", "attempting", "ready", "dispatched", "reaping"])
FINISHED_STATES = set(["succeeded", "done", "abandoned"])


def problem_kind(problem, details):
    name = str(problem or "")
    text = (name + " " + str(details or "")).lower()
    if((name in OOM_PROBLEMS) or ("out of memory" in text) or ("oom" in text)):
        return "oom"
    if((name in TIME_PROBLEMS) or ("time limit" in text) or ("timeout" in text) or ("walltime" in text)):
        return "walltime"
    if((name in TRANSIENT_PROBLEMS) or ("node_fail" in text) or ("node fail" in text)):
        return "transient"
    return "application"


def recovery_action(job):
    # None means this job is not a current problem. modify requeues; do not also retry-jobs.
    status = str(job.get("job_status") or "")
    if(status in FINISHED_STATES):
        return None
    if(status in ACTIVE_STATES):
        return None
    problem = job.get("job_attempt_problem")
    if(not problem):
        return None
    if((status not in ["", "problem"]) and (status not in ACTIVE_STATES)):
        return None
    attempts = int(job.get("num_attempts") or 1)
    kind = problem_kind(problem, job.get("job_attempt_problem_details"))
    ram = int(job.get("site_job_ram_bytes") or 0)
    secs = int(job.get("site_job_time_secs") or 0)
    name = str(job.get("job_name") or job.get("job_id"))
    action = {
        "tool": None, "kind": kind, "name": name, "args": [], "retry": False,
        "reason": "", "prior_ram_bytes": ram, "prior_time_secs": secs,
        "revised_ram_bytes": ram, "revised_time_secs": secs, "retry_number": attempts,
        "problem": problem,
    }
    if(attempts >= MAX_ATTEMPTS):
        action["reason"] = "retry ceiling"
        return action
    if(kind == "oom"):
        revised = ram + (1024 ** 3)
        if((ram > 0) and (revised > RAM_CEILING_BYTES)):
            action["reason"] = "ram ceiling"
            return action
        action.update({"tool": "modify-jobs", "args": ["-ram", "add", "1gb"], "revised_ram_bytes": revised, "retry": True, "reason": "oom"})
        return action
    if(kind == "walltime"):
        revised = secs + 3600
        if((secs > 0) and (revised > TIME_CEILING_SECS)):
            action["reason"] = "time ceiling"
            return action
        action.update({"tool": "modify-jobs", "args": ["-time", "add", "1h"], "revised_time_secs": revised, "retry": True, "reason": "walltime"})
        return action
    if(kind == "transient"):
        action.update({"tool": "retry-jobs", "retry": True, "reason": "transient"})
        return action
    action["reason"] = "application"
    return action


def swif_command(workflow, action):
    # Field changes come before -names. modify-jobs already requeues a problem job.
    if(action["tool"] == "retry-jobs"):
        return ["swif2", "retry-jobs", workflow, "-names", action["name"]]
    command = ["swif2", "modify-jobs", workflow]
    command.extend(action["args"])
    command.extend(["-names", action["name"]])
    return command


def summary_row(payload):
    summary = payload.get("summary")
    if((summary is None) and isinstance(payload.get("status"), dict)):
        summary = payload["status"].get("summary")
    if(isinstance(summary, list)):
        if(len(summary) == 0):
            return None
        summary = summary[0]
    if(isinstance(summary, dict)):
        return summary
    return None


def job_rows(payload):
    jobs = payload.get("jobs")
    if(isinstance(jobs, dict)):
        jobs = jobs.get("jobs") or []
    if(not isinstance(jobs, list)):
        jobs = []
    if(len(jobs) > 0):
        return jobs
    problems = payload.get("problems") or []
    if(isinstance(problems, dict)):
        problems = problems.get("problems") or []
    if(isinstance(problems, list)):
        return problems
    return []


def apply_status(workflow, payload, registry, seen=None):
    if(seen is None):
        seen = set()
    acted = []
    for job in job_rows(payload):
        action = recovery_action(job)
        if(action is None):
            continue
        key = (action["name"], action["retry_number"], action["kind"], action["retry"])
        if(key in seen):
            continue
        seen.add(key)
        registry.append({
            "campaign": workflow, "stage": "swif2_recovery",
            "status": "retryable" if(action["retry"]) else "failed",
            "job_name": action["name"], "failure_class": action["kind"],
            "problem": action["problem"], "reason": action["reason"],
            "tool": action["tool"], "prior_ram_bytes": action["prior_ram_bytes"],
            "prior_time_secs": action["prior_time_secs"],
            "revised_ram_bytes": action["revised_ram_bytes"],
            "revised_time_secs": action["revised_time_secs"],
            "retry_number": action["retry_number"], "retry": action["retry"],
            "command": "" if(not action["retry"]) else " ".join(swif_command(workflow, action)),
        })
        if(action["retry"]):
            acted.append(action)
    return acted


def run_recovery_command(workflow, action):
    subprocess.check_call(swif_command(workflow, action))


def workflow_idle(payload):
    summary = summary_row(payload)
    if(summary is None):
        return False
    problems = int(summary.get("problems") or 0)
    undispatched = int(summary.get("undispatched") or 0)
    dispatched = int(summary.get("dispatched") or 0)
    return (problems == 0) and (undispatched == 0) and (dispatched == 0)


def add_job_argv(workflow, spec, swif):
    argv = [
        "swif2", "add-job",
        "-workflow", workflow,
        "-name", spec["name"],
        "-phase", str(spec.get("phase", 0)),
        "-ram", spec.get("ram", "4GB"),
        "-time", spec.get("time", "8h"),
        "-cores", "1",
        "-shell", "/bin/tcsh",
        "-stdout", spec["stdout"],
        "-stderr", spec["stderr"],
        "-account", swif["account"],
        "-partition", swif["partition"],
    ]
    for parent in spec.get("antecedents") or []:
        argv.extend(["-antecedent", parent])
    argv.extend(["/bin/tcsh", "-c", spec["command"]])
    return argv


def start_unattended_recovery(workflow, registry, dry_run=False, status_json=None, run_commands=None):
    if(dry_run):
        print("dry-run: SWIF2 recovery is armed and starts on a real launch")
        return []
    if(status_json is not None):
        payload = json.loads(status_json) if(isinstance(status_json, str)) else status_json
        actions = apply_status(workflow, payload, registry)
        if(run_commands):
            for action in actions:
                run_recovery_command(workflow, action)
        return actions
    if(shutil.which("swif2") is None):
        registry.set_status("swif2_recovery", "awaiting_jlab_validation")
        print("swif2 is not on this host. Jobs were not submitted. On ifarm this same process creates the workflow, calls swif2 run, and polls.")
        return []
    seen = set()
    while True:
        try:
            raw = subprocess.check_output(["swif2", "status", workflow, "-summary", "-problems", "-jobs", "-display", "json"], text=True)
        except subprocess.CalledProcessError as exc:
            print("swif2 status failed (%s). Still polling. No -ft input is required." % exc.returncode)
            time.sleep(60)
            continue
        payload = json.loads(raw)
        actions = apply_status(workflow, payload, registry, seen)
        for action in actions:
            run_recovery_command(workflow, action)
        if(workflow_idle(payload)):
            print("swif2 workflow %s is idle: no undispatched, dispatched, or problem jobs" % workflow)
            return actions
        time.sleep(60)


def launch_swif_workflow(workflow, swif, specs, registry, dry_run=False):
    # Create, add-job, swif2 run, then poll. A new workflow stays suspended until swif2 run.
    if(len(specs) == 0):
        print("no SWIF2 jobs to add")
        return []
    if(dry_run):
        print("dry-run: no SWIF2 jobs submitted. A real launch runs these add-job commands, then swif2 run, then polls in this process.")
        for spec in specs:
            print(shlex.join(add_job_argv(workflow, spec, swif)))
        print("swif2 run %s" % workflow)
        return []
    if(shutil.which("swif2") is None):
        registry.set_status("swif2_recovery", "awaiting_jlab_validation")
        print("swif2 is not on this host. No jobs were submitted and recovery was not pretended.")
        return []
    os.makedirs(os.path.dirname(specs[0]["stdout"]), exist_ok=True)
    created = subprocess.run(["swif2", "create", "-workflow", workflow, "-maxconcurrent", str(swif["max_concurrent"])])
    if(created.returncode != 0):
        probed = subprocess.run(["swif2", "status", workflow, "-summary", "-display", "json"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if(probed.returncode != 0):
            registry.set_status("swif2_recovery", "failed")
            print("swif2 create failed and the workflow is not queryable. No jobs were added.")
            return []
        print("workflow %s already exists. Jobs were not added again. Recovery continues in this process." % workflow)
        return start_unattended_recovery(workflow, registry, dry_run=False)
    for spec in specs:
        subprocess.check_call(add_job_argv(workflow, spec, swif))
    subprocess.check_call(["swif2", "run", workflow])
    print("swif2 run %s ; recovery is polling in this process" % workflow)
    return start_unattended_recovery(workflow, registry, dry_run=False)
