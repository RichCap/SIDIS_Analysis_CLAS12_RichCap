# Branch plan on top of sidis_graph.json. One launch can run independent branches together.
import json
import os

_BOOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

BRANCH_OF = {
    "groovy_rho": "acceptance", "groovy_55na": "acceptance", "dataframe": "acceptance",
    "make_batches": "acceptance", "rho_norm": "acceptance", "response_5d": "acceptance",
    "response_3d": "acceptance", "response_1d": "acceptance", "response_2d": "acceptance",
    "response": "acceptance", "diagnostic_dphi": "acceptance", "unfold_3d": "acceptance",
    "iteration_refresh_3d": "acceptance", "iteration_5d": "acceptance",
    "rc_regenerate": "rc",
    "hybrid_attach": "correction", "bc": "correction", "bc_sensitivity": "correction",
    "fit": "correction", "aggregate": "correction",
}
CHECKPOINTS = {"rho_norm": "rho_factors", "iteration_5d": "iteration_choice", "bc": "bc_choice"}
STARTS = {
    "groovy": ["groovy_rho", "groovy_55na"],
    "dataframe": ["dataframe"],
    "batches": ["make_batches"],
    "response": ["response_5d", "response_3d", "diagnostic_dphi", "response_2d"],
    "unfold": ["unfold_3d"],
    "rc": ["rc_regenerate"],
    "bc": ["bc"],
    "hybrid": ["hybrid_attach"],
}


def load_graph(path=None):
    if(path is None):
        path = os.path.join(os.path.dirname(__file__), "sidis_graph.json")
    handle = open(path)
    graph = json.load(handle)
    handle.close()
    return graph


def parse_artifacts(text):
    modes = {}
    if(text in [None, ""]):
        return modes
    for piece in str(text).split(","):
        name, mode = piece.split("=")
        if(mode not in ["regenerate", "reuse", "disabled"]):
            raise ValueError("unknown artifact mode %s" % mode)
        modes[name.strip()] = mode
    return modes


def stage_branch(stage_id):
    return BRANCH_OF.get(stage_id, "other")


def ancestors(stage_map, roots):
    found = set()
    stack = list(roots)
    while(len(stack) > 0):
        node = stack.pop()
        for parent in stage_map[node].get("depends_on") or []:
            if((parent in stage_map) and (parent not in found)):
                found.add(parent)
                stack.append(parent)
    return found


def descendants(stage_map, roots):
    wanted = set(roots)
    changed = True
    while changed:
        changed = False
        for stage_id, stage in stage_map.items():
            if(stage_id in wanted):
                continue
            parents = stage.get("depends_on") or []
            if(any(parent in wanted for parent in parents)):
                wanted.add(stage_id)
                changed = True
    return wanted


def effective_parents(stage, artifacts):
    parents = []
    for parent in stage.get("depends_on") or []:
        if(artifacts.get(stage_branch(parent)) == "disabled"):
            continue
        parents.append(parent)
    return parents


def plan_launch(graph, start, artifacts, satisfied):
    stage_map = {}
    for stage in graph["stages"]:
        stage_map[stage["stage_id"]] = stage
    if(start not in STARTS):
        raise ValueError("unknown start %s" % start)
    for branch_name, mode in artifacts.items():
        if(mode not in ["regenerate", "reuse", "disabled"]):
            raise ValueError("unknown artifact mode %s" % mode)
    roots = STARTS[start]
    earlier = ancestors(stage_map, roots)
    scope = descendants(stage_map, roots)
    start_branches = set([stage_branch(stage_id) for stage_id in roots])
    for stage_id, branch_name in BRANCH_OF.items():
        mode = artifacts.get(branch_name, "regenerate")
        if((mode == "disabled") or (branch_name in start_branches) or (stage_id in earlier)):
            continue
        scope.add(stage_id)
    rows = []
    for stage_id in scope:
        branch_name = stage_branch(stage_id)
        mode = artifacts.get(branch_name, "regenerate")
        if(mode == "disabled"):
            rows.append({"stage_id": stage_id, "branch": branch_name, "state": "disabled", "phase": None})
            continue
        if(mode == "reuse"):
            # if(stage_id not in satisfied):
            if((stage_id not in satisfied) and (branch_name not in satisfied)):
                raise ValueError("reuse requested but %s is not a validated artifact" % stage_id)
            rows.append({"stage_id": stage_id, "branch": branch_name, "state": "reuse", "phase": None})
            continue
        rows.append({"stage_id": stage_id, "branch": branch_name, "state": "regenerate", "phase": 0})
    by_id = {}
    for row in rows:
        by_id[row["stage_id"]] = row
        row["release"] = "no"
        row["antecedents"] = []
    ready = set()
    for _pass in range(len(rows) + 1):
        changed = False
        for row in rows:
            if(row["state"] != "regenerate"):
                continue
            stage = stage_map[row["stage_id"]]
            parents = effective_parents(stage, artifacts)
            blocked = False
            waiting = False
            antecedents = []
            for parent in parents:
                parent_row = by_id.get(parent)
                if((parent in CHECKPOINTS) and (parent not in satisfied)):
                    blocked = True
                    continue
                if(parent_row is None):
                    continue
                if(parent_row["state"] == "disabled"):
                    continue
                if(parent_row["state"] == "reuse"):
                    continue
                if(parent not in ready):
                    waiting = True
                    continue
                antecedents.append(parent)
            if(blocked):
                new_release = "checkpoint"
            elif(waiting):
                new_release = "waiting"
            else:
                new_release = "now"
            if(row["release"] != new_release):
                row["release"] = new_release
                changed = True
            if(new_release == "now"):
                ready.add(row["stage_id"])
                row["antecedents"] = antecedents
        if(not changed):
            break
    return rows


def format_plan(rows):
    lines = []
    for row in rows:
        lines.append("%s %s %s %s" % (row["branch"], row["stage_id"], row["state"], row.get("release", "no")))
    return lines


# Checks concurrent acceptance and RC, reuse of either branch, a start after Groovy, a merge that waits on both, and RC staying runnable while rho approval is open.
def self_test():
    graph = load_graph()
    both = plan_launch(graph, "groovy", {"acceptance": "regenerate", "rc": "regenerate", "correction": "regenerate"}, set())
    now = [row["stage_id"] for row in both if(row.get("release") == "now")]
    if(("groovy_rho" not in now) or ("rc_regenerate" not in now)):
        raise SystemExit("acceptance and RC were not both ready: %s" % now)
    if(any((row["stage_id"] == "hybrid_attach") and (row.get("release") == "now") for row in both)):
        raise SystemExit("merge ran before both parents")
    # rc_only = plan_launch(graph, "groovy", {"acceptance": "reuse", "rc": "regenerate", "correction": "disabled"}, set(["groovy_rho", "groovy_55na", "dataframe", "make_batches", "rho_norm", "response", "unfold_3d"]))
    rc_only = plan_launch(graph, "groovy", {"acceptance": "reuse", "rc": "regenerate", "correction": "disabled"}, set(["acceptance"]))
    if(any((row["branch"] == "acceptance") and (row["state"] != "reuse") for row in rc_only)):
        raise SystemExit("reused acceptance was regenerated")
    if(not any((row["stage_id"] == "rc_regenerate") and (row.get("release") == "now") for row in rc_only)):
        raise SystemExit("RC did not run while acceptance was reused")
    # acc_only = plan_launch(graph, "groovy", {"acceptance": "regenerate", "rc": "reuse", "correction": "regenerate"}, set(["rc_regenerate"]))
    acc_only = plan_launch(graph, "groovy", {"acceptance": "regenerate", "rc": "reuse", "correction": "regenerate"}, set(["rc"]))
    if(any((row["stage_id"] == "rc_regenerate") and (row["state"] != "reuse") for row in acc_only)):
        raise SystemExit("reused RC was regenerated")
    later = plan_launch(graph, "response", {"acceptance": "regenerate", "rc": "disabled", "correction": "disabled"}, set(["rho_norm"]))
    if(any(row["stage_id"] in ["groovy_rho", "groovy_55na"] for row in later)):
        raise SystemExit("a later start reran Groovy")
    paused = [row for row in both if((row["stage_id"] == "response_5d") and (row.get("release") == "checkpoint"))]
    rc_now = [row for row in both if((row["stage_id"] == "rc_regenerate") and (row.get("release") == "now"))]
    if((len(paused) != 1) or (len(rc_now) != 1)):
        raise SystemExit("rho checkpoint blocked RC or failed to block response")
    print("branches self_test ok")


if(__name__ == "__main__"):
    self_test()
