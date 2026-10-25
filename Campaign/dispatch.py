# Refill free slots by product priority. Independent lower-priority work still runs.
RESPONSE_PRIORITY = ["response_5d", "response_3d", "response_1d", "response_2d"]


def priority_key(stage):
    if(stage in RESPONSE_PRIORITY):
        return RESPONSE_PRIORITY.index(stage)
    return len(RESPONSE_PRIORITY)


def refill(ready, free_slots):
    ordered = sorted(list(ready), key=lambda job: (priority_key(job.get("stage", "")), str(job.get("name", ""))))
    return ordered[:max(0, int(free_slots))]
