#!/usr/bin/env python3
# Unattended SWIF2 recovery. Production does not need -ft.
import json
import os
import shlex
import shutil
import subprocess
import sys
import time

_BOOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if(_BOOT not in sys.path):
    sys.path.insert(0, _BOOT)

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
        "problem": problem, "details": str(job.get("job_attempt_problem_details") or ""),
        "job_id": job.get("job_id"),
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
        acted.append(action)
    return acted


def run_recovery_command(workflow, action):
    if(not action.get("retry")):
        return
    subprocess.check_call(swif_command(workflow, action))


def failure_line(action):
    details = action.get("details") or ""
    wrapper_note = ""
    if("exited with code 13" in details.lower()):
        wrapper_note = "; SWIF2 wrapper/execution-setup failure"
    if(action.get("retry")):
        if(action.get("tool") == "modify-jobs"):
            decision = "will modify and retry (%s)" % " ".join(action.get("args") or [])
        else:
            decision = "will retry unchanged"
    else:
        decision = "no automatic retry"
    job_id = action.get("job_id")
    id_text = "" if(job_id in [None, ""]) else " id %s" % job_id
    return "FAILED %s%s: %s: %s%s; classified as %s; %s" % (
        action.get("name"), id_text, action.get("problem"), details, wrapper_note, action.get("kind"), decision,
    )


def antecedent_names(job):
    # Published data model: antecedents are job-name strings. Pairs or objects are not guessed.
    if("antecedents" not in job):
        return None
    raw = job.get("antecedents")
    if(not isinstance(raw, list)):
        return None
    names = []
    for item in raw:
        if(not isinstance(item, str)):
            return None
        if(item == ""):
            return None
        names.append(item)
    return names


def phase_number(job):
    if("job_phase" not in job):
        return None
    value = job.get("job_phase")
    if(isinstance(value, bool) or (not isinstance(value, int))):
        return None
    return value


def blockage_state(jobs):
    # stalled, open, or unproven. Does not abandon or modify anything.
    if(not isinstance(jobs, list)):
        return "unproven"
    known_names = []
    problem_names = set()
    problem_phases = set()
    waiting = []
    for job in jobs:
        if(not isinstance(job, dict)):
            return "unproven"
        if(("job_status" not in job) or ("job_name" not in job)):
            return "unproven"
        names = antecedent_names(job)
        phase = phase_number(job)
        if((names is None) or (phase is None)):
            return "unproven"
        status = str(job.get("job_status") or "")
        name = str(job.get("job_name"))
        known_names.append(name)
        action = recovery_action(job)
        if((action is not None) and (not action["retry"])):
            problem_names.add(name)
            problem_phases.add(phase)
        if(status in FINISHED_STATES):
            continue
        if(status == "problem"):
            continue
        if(status in ["attempting", "ready", "dispatched", "reaping"]):
            return "open"
        if(status != "pending"):
            return "unproven"
        waiting.append((name, names, phase))
    if(len(problem_names) == 0):
        return "open"
    if(len(waiting) == 0):
        return "stalled"
    for name, names, phase in waiting:
        for parent in names:
            if(parent not in known_names):
                return "unproven"
        held_by_parent = False
        for parent in names:
            if(parent in problem_names):
                held_by_parent = True
        held_by_phase = False
        for lower in problem_phases:
            if(lower < phase):
                held_by_phase = True
        if(not (held_by_parent or held_by_phase)):
            return "open"
    return "stalled"


def farm_queue_busy(payload):
    summary = summary_row(payload)
    if(not isinstance(summary, dict)):
        return None
    for key in ["dispatched", "dispatched_running", "dispatched_pending"]:
        if(key not in summary):
            return None
        try:
            count = int(summary.get(key) or 0)
        except (TypeError, ValueError):
            return None
        if(count > 0):
            return True
    return False


def send_crash_warning(workflow, lines):
    subject = "CRASH REPORT: 'run_sidis_campaign.py' Code Failed"
    body = "\nCRASH WARNING!\n\nThe SWIF2 workflow %s is terminally stalled. No further automatic retry will be submitted.\n\n%s\n" % (
        workflow, "\n".join(lines),
    )
    print(body, file=sys.stderr)
    try:
        subprocess.run(["mail", "-s", subject, "richard.capobianco@uconn.edu"], input=body.encode(), check=False)
    except FileNotFoundError:
        print("WARNING: mail command not found; the crash warning was printed and was not emailed.", file=sys.stderr)
    except Exception as exc:
        print("WARNING: mail failed: %s" % exc, file=sys.stderr)


def workflow_idle(payload):
    summary = summary_row(payload)
    if(summary is None):
        return False
    problems = int(summary.get("problems") or 0)
    undispatched = int(summary.get("undispatched") or 0)
    dispatched = int(summary.get("dispatched") or 0)
    return (problems == 0) and (undispatched == 0) and (dispatched == 0)


def add_job_argv(workflow, spec, swif):
    # -shell is /bin/sh so SWIF2's interpreter does not read ~/.cshrc.
    # The command itself is tcsh -f, which skips `if (! $?prompt) exit` and then sources swif_env.csh.
    wrapper = os.path.join(os.path.dirname(os.path.abspath(__file__)), "swif_job.csh")
    argv = [
        "swif2", "add-job",
        "-workflow", workflow,
        "-name", spec["name"],
        "-phase", str(spec.get("phase", 0)),
        "-ram", spec.get("ram", "4GB"),
        "-time", spec.get("time", "8h"),
        "-disk", spec.get("disk", "10GB"),
        "-cores", "1",
        "-shell", "/bin/sh",
        "-stdout", spec["stdout"],
        "-stderr", spec["stderr"],
        "-account", swif["account"],
        "-partition", swif["partition"],
    ]
    for parent in spec.get("antecedents") or []:
        argv.extend(["-antecedent", parent])
    argv.extend(["/bin/tcsh", "-f", wrapper, spec.get("checkout") or ""])
    argv.extend(shlex.split(spec["command"]))
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
    reported = []
    while True:
        try:
            raw = subprocess.check_output(["swif2", "status", workflow, "-summary", "-problems", "-jobs", "-display", "json"], text=True)
        except subprocess.CalledProcessError as exc:
            print("swif2 status failed (%s). Still polling. No -ft input is required." % exc.returncode)
            time.sleep(60)
            continue
        payload = json.loads(raw)
        actions = apply_status(workflow, payload, registry, seen)
        submitted = False
        for action in actions:
            line = failure_line(action)
            reported.append(line)
            print(line)
            if(action.get("retry")):
                run_recovery_command(workflow, action)
                submitted = True
        if(workflow_idle(payload)):
            print("swif2 workflow %s is idle: no undispatched, dispatched, or problem jobs" % workflow)
            return actions
        if(not submitted):
            busy = farm_queue_busy(payload)
            if(busy is None):
                print("terminal blockage could not be proven: the SWIF2 summary is missing dispatched, dispatched_running, or dispatched_pending. No additional job was abandoned, modified, or retried.")
                raise SystemExit(2)
            if(not busy):
                state = blockage_state(job_rows(payload))
                if(state == "unproven"):
                    print("terminal blockage could not be proven from the SWIF2 jobs JSON (antecedents must be job-name strings and job_phase must be an integer). No additional job was abandoned, modified, or retried. Manual review is required.")
                    raise SystemExit(2)
                if(state == "stalled"):
                    send_crash_warning(workflow, reported)
                    raise SystemExit(1)
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


def _job(name, status, phase, antecedents, problem="", details="", attempts=1, jid=1):
    row = {
        "job_name": name, "job_id": jid, "job_status": status, "job_phase": phase,
        "antecedents": antecedents, "num_attempts": attempts,
        "site_job_ram_bytes": 4 * (1024 ** 3), "site_job_time_secs": 8 * 3600,
    }
    if(problem != ""):
        row["job_attempt_problem"] = problem
        row["job_attempt_problem_details"] = details
    return row


def self_test():
    failed = _job("early_chain_359", "problem", 0, [], "SLURM_FAILED", "Exited with code 13", jid=64259904)
    action = recovery_action(failed)
    if(action["retry"] or (action["kind"] != "application")):
        raise SystemExit("code 13 was classified for retry: %s" % action)
    text = failure_line(action)
    if(("no automatic retry" not in text) or ("wrapper/execution-setup failure" not in text) or ("64259904" not in text)):
        raise SystemExit("failure line missing required fields: %s" % text)
    oom = recovery_action(_job("oom_job", "problem", 0, [], "SLURM_OUT_OF_MEMORY", "out of memory"))
    if((not oom["retry"]) or (oom["tool"] != "modify-jobs") or (oom["args"] != ["-ram", "add", "1gb"])):
        raise SystemExit("oom action changed: %s" % oom)
    if("retry-jobs" in " ".join(swif_command("ifarm_ready", oom))):
        raise SystemExit("oom also called retry-jobs")
    if(not farm_queue_busy({"summary": {"dispatched": 0, "dispatched_running": 0, "dispatched_pending": 1}})):
        raise SystemExit("slurm pending was treated as idle")
    parent = _job("early_chain_0", "problem", 0, [], "SLURM_FAILED", "Exited with code 13")
    sibling = _job("early_chain_1", "pending", 0, [])
    if(blockage_state([parent, sibling]) != "open"):
        raise SystemExit("same-phase pending job was treated as blocked")
    child = _job("early_chain_360", "pending", 1, [])
    if(blockage_state([parent, child]) != "stalled"):
        raise SystemExit("higher phase was not held by the lower-phase failure")
    named = _job("early_chain_360", "pending", 0, ["early_chain_0"])
    if(blockage_state([parent, named]) != "stalled"):
        raise SystemExit("failed antecedent name did not block the child")
    missing = dict(child)
    del missing["job_phase"]
    if(blockage_state([parent, missing]) != "unproven"):
        raise SystemExit("missing job_phase was guessed")
    paired = dict(child)
    paired["antecedents"] = [["done", 1]]
    if(blockage_state([parent, paired]) != "unproven"):
        raise SystemExit("status/id antecedent was accepted")
    print("swif_watch self_test ok")


if(__name__ == "__main__"):
    self_test()
