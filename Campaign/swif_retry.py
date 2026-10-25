# Classify one SWIF2/SLURM failure and decide the next automatic attempt.
RAM_STEP_GB     = 1
TIME_STEP_H     = 1
RAM_CEILING_GB  = 32
TIME_CEILING_H  = 24
MAX_RETRIES     = 2


def classify_failure(text):
    low = str(text).lower()
    if(any(token in low for token in ["oom", "out of memory", "memory limit", "exceeded memory", "cgroup"])):
        return "oom"
    if(any(token in low for token in ["walltime", "wall time", "time limit", "timeout", "due to time"])):
        return "walltime"
    if(any(token in low for token in ["node_fail", "node fail", "boot_fail", "preempt", "requeue", "unavailable", "connection reset"])):
        return "transient"
    return "application"


def next_resources(kind, ram_gb, hours, retry_number, max_retries=MAX_RETRIES, ram_ceiling=RAM_CEILING_GB, time_ceiling=TIME_CEILING_H):
    # None means do not retry. Application failures are never retried.
    if(kind == "application"):
        return None
    if(int(retry_number) >= int(max_retries)):
        return None
    ram_gb = int(ram_gb)
    hours = int(hours)
    if(kind == "oom"):
        revised = ram_gb + RAM_STEP_GB
        if(revised > int(ram_ceiling)):
            return None
        return {"ram_gb": revised, "hours": hours}
    if(kind == "walltime"):
        revised = hours + TIME_STEP_H
        if(revised > int(time_ceiling)):
            return None
        return {"ram_gb": ram_gb, "hours": revised}
    if(kind == "transient"):
        return {"ram_gb": ram_gb, "hours": hours}
    return None


def attempt_record(command, kind, ram_gb, hours, revised, retry_number):
    return {
        "command": command,
        "failure_class": kind,
        "prior_ram_gb": int(ram_gb),
        "prior_hours": int(hours),
        "revised_ram_gb": None if(revised is None) else int(revised["ram_gb"]),
        "revised_hours": None if(revised is None) else int(revised["hours"]),
        "retry_number": int(retry_number),
        "retry": revised is not None,
    }
