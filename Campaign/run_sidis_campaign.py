#!/usr/bin/env python3
# Declare a SIDIS campaign stage and write the command that runs it.
# Physics production is not launched on a machine that does not have the farm inputs.
import argparse
import json
import os
import shlex
import sys

_BOOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if(_BOOT not in sys.path):
    sys.path.insert(0, _BOOT)

from Campaign.backends import local_command
from Campaign.binning_version import BINNING_VERSION
from Campaign.early_chain import checkout_script, early_chain_commands, later_commands, plan_retry, response_commands
from Campaign.registry import Registry
from jlab_work_paths import WORK_ROOTS, data_root_path
from merge_bayesian_iteration_lookup import canonical_cut, lookup_record

LOOKUP = os.path.join(_BOOT, "Unfold_Iteration_Config", "bayesian_iteration_lookup.json")
K_GROUPS_2PCT = {
    5: [2, 3, 5, 6, 8, 14, 17],
    6: [1, 7, 9, 10, 11, 13, 16],
    7: [12, 15],
    10: [4],
}


def load_json(path):
    handle = open(path)
    payload = json.load(handle)
    handle.close()
    return payload


def repo_python():
    return sys.executable


def evgen_dir():
    farm = "/w/hallb-scshelf2102/clas12/richcap/Radiative_MC/SIDIS_RC_EvGen_richcap/Running_EvGen_richcap"
    local = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/Running_EvGen_richcap"
    if(os.path.isdir(farm)):
        return farm
    return local


def command_kind(command):
    if("run_groovy_scripts_with_emails.py" in command):
        if("-src clasdis" in command):
            return "groovy_clasdis"
        return "groovy_rho"
    if("run_dataframe_makeROOT_helper.py" in command):
        if("55na" in command):
            return "df_clasdis"
        return "df_rho"
    if("make_batches" in command):
        return "batches"
    if("Get_rho_Normalization_values.py" in command):
        return "rho_fit"
    if("-rho" in shlex.split(command)):
        return "rho_hist"
    return "other"


def phase_for(kind):
    if(kind in ["groovy_rho", "groovy_clasdis"]):
        return 0
    if(kind in ["df_rho", "df_clasdis"]):
        return 1
    if(kind == "batches"):
        return 2
    if(kind in ["rho_hist", "rho_fit"]):
        return 3
    return 4


def swif_shell_command(command):
    # -m slurm would submit a nested array that swif2 status cannot retry. Sequential keeps the failure on this job.
    text = command.replace(" -m slurm ", " -m sequential ")
    return "cd %s && %s" % (shlex.quote(_BOOT), text)


def specs_from_lines(stage, lines, log_dir):
    specs = []
    for line in lines:
        if((not line) or line.startswith("#")):
            continue
        kind = command_kind(line)
        name = "%s_%d" % (stage.replace(",", "_"), len(specs))
        specs.append({
            "name": name,
            "kind": kind,
            "phase": phase_for(kind),
            "command": swif_shell_command(line),
            "antecedents": [],
            "stdout": os.path.join(log_dir, name + ".out"),
            "stderr": os.path.join(log_dir, name + ".err"),
            "ram": "4GB",
            "time": "8h",
        })
    names = {}
    for spec in specs:
        names.setdefault(spec["kind"], []).append(spec["name"])
    for spec in specs:
        if(spec["kind"] == "df_rho"):
            spec["antecedents"] = list(names.get("groovy_rho", []))
        elif(spec["kind"] == "df_clasdis"):
            spec["antecedents"] = list(names.get("groovy_clasdis", []))
        elif(spec["kind"] == "batches"):
            spec["antecedents"] = list(names.get("df_rho", [])) + list(names.get("df_clasdis", []))
        elif(spec["kind"] == "rho_hist"):
            spec["antecedents"] = list(names.get("batches", []))
        elif(spec["kind"] == "rho_fit"):
            spec["antecedents"] = list(names.get("rho_hist", []))
    return specs


def iteration_record(dimension, cut, q2y):
    cut_text = canonical_cut(cut)
    if(dimension == "5D"):
        return lookup_record(LOOKUP, "5D", cut_text)
    return lookup_record(LOOKUP, "3D", cut_text, int(q2y))


def k_for(dimension, cut, q2y, provenance):
    record = iteration_record(dimension, cut, q2y)
    if(record.get("k_selected") in [None, ""]):
        raise SystemExit("no k_selected for %s %s q2y=%s" % (dimension, cut, q2y))
    if(record.get("data_status") == "unresolved"):
        raise SystemExit("iteration unresolved for %s %s" % (dimension, cut))
    return int(record["k_selected"]), provenance


def unfold_3d_commands(cut, phi_bins, background, bins, provenance, data_root):
    cut_text = canonical_cut(cut)
    grouped = {}
    for q2y in bins:
        k_value, _prov = k_for("3D", cut_text, q2y, provenance)
        grouped.setdefault(k_value, []).append(q2y)
    commands = []
    script = checkout_script(os.path.join(_BOOT, "run_Simple_Unfold.py"))
    for k_value, q2y_list in sorted(grouped.items()):
        bin_text = ",".join([str(q2y) for q2y in q2y_list])
        parts = [
            script, "-droot", data_root,
            "--bayes_iterations", str(k_value),
            "--Min_Allowed_Acceptance_Cut", cut_text,
            "--bins", bin_text,
            "--background_source", background,
            "--phi_bins", str(phi_bins),
        ]
        commands.append((k_value, q2y_list, local_command(" ".join(parts))))
    return commands


def iteration_study_command(dimension, cut, bins, k_max, data_root):
    cut_text = canonical_cut(cut)
    if(dimension == "5D"):
        script = checkout_script(os.path.join(_BOOT, "run_Dedicated_5D_Unfold.py"))
        parts = [
            script, "-droot", data_root,
            "--iteration_study",
            "--parm_min", "1",
            "--parm_max", str(k_max),
            "--parm_step", "1",
            "--Min_Allowed_Acceptance_Cut", cut_text,
            "--background_source", "lundvpk",
        ]
    else:
        script = checkout_script(os.path.join(_BOOT, "run_Simple_Unfold.py"))
        bin_text = ",".join([str(q2y) for q2y in bins])
        parts = [
            script, "-droot", data_root,
            "--iteration_study",
            "--parm_min", "1",
            "--parm_max", str(k_max),
            "--parm_step", "1",
            "--Min_Allowed_Acceptance_Cut", cut_text,
            "--bins", bin_text,
        ]
    return local_command(" ".join(parts))


def hybrid_command(unfolded, evgen, output):
    script = os.path.join(evgen_dir(), "Run_Large_Files_For_Iterative_Corrections", "Comparison_With_Unfolding", "create_Hybrid_SIDIS_Single_File.py")
    # The live hybrid writer lives under the EvGen checkout. It has no campaign data-root flag.
    return local_command("%s -ui %s -ei %s -o %s" % (script, unfolded, evgen, output))


def bc_command(counts):
    script = checkout_script(os.path.join(_BOOT, "BC_Corrections", "BC_Corrections_Script.py"))
    return local_command("%s -nb 3 -nbphi 2 -nbq %d -nby %d -nbz %d -nbpt %d -nbh %d" % (
        script, counts["q2"], counts["y"], counts["z"], counts["pt"], counts["phi"],
    ))


def write_command_file(folder, name, lines):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, name)
    handle = open(path, "w")
    for line in lines:
        if("conda" in line):
            raise SystemExit("refusing a command that activates conda")
        handle.write(local_command(line))
        handle.write("\n")
    handle.close()
    return path


def selected_stages(graph, requested):
    stages = graph["stages"]
    if(requested in [None, "", "all_stages"]):
        return [stage for stage in stages if(not stage.get("optional"))]
    wanted = set(requested.split(","))
    return [stage for stage in stages if(stage["stage_id"] in wanted)]


def main():
    parser = argparse.ArgumentParser(description="SIDIS campaign driver. Writes commands and registry records. It does not launch farm physics from a dry run.")
    parser.add_argument("-c", "--campaign", default="post_binning", help="Campaign name.")
    parser.add_argument("-s", "--stage", default="unfold_3d", help="Stage id, comma-separated ids, or all_stages.")
    parser.add_argument("-g", "--graph", default=os.path.join(os.path.dirname(__file__), "sidis_graph.json"))
    parser.add_argument("-b", "--backend", default="external", help="external, local_seq, swif2, hybrid, slurm_array, local_parallel, or validate.")
    parser.add_argument("-sys", "--systematics", default="nominal", help="nominal, all, or one source name.")
    parser.add_argument("-v", "--variation", default=None)
    parser.add_argument("-dim", "--dimension", default="3D", choices=["1D", "3D", "5D"])
    parser.add_argument("-ac", "--acceptance_cut", default="0.020")
    parser.add_argument("-q", "--q2y_bins", default="1-17")
    parser.add_argument("-rc", "--rc_mode", default="reuse", choices=["reuse", "regenerate"])
    parser.add_argument("-k", "--iteration_action", default="use_lookup", choices=["use_lookup", "refresh"])
    parser.add_argument("-ph", "--phi_bins", default=24, type=int, choices=[12, 24])
    parser.add_argument("-bg", "--background_source", default="lundvpk")
    parser.add_argument("-droot", "--data_root", default="work_b", help="Analysis data root. This campaign defaults to work_b.")
    parser.add_argument("-n", "--dry_run", action="store_true")
    parser.add_argument("-prov", "--k_provenance", default="pre_binning_bootstrap", choices=["pre_binning_bootstrap", "current_binning"])
    parser.add_argument("-ft", "--failure_text", default="", help="Debug hook only. Production recovery polls swif2 status and does not need this.")
    parser.add_argument("-ram", "--ram_gb", default=4, type=int)
    parser.add_argument("-hr", "--hours", default=8, type=int)
    parser.add_argument("-rn", "--retry_number", default=0, type=int)
    args = parser.parse_args()
    graph = load_json(args.graph)
    data_root_key = args.data_root
    registry_root = data_root_path(data_root_key) if(data_root_key in WORK_ROOTS) else data_root_key
    if((data_root_key in WORK_ROOTS) and (not os.path.isdir(registry_root))):
        registry_root = os.path.join("/tmp", "SIDIS_Campaign_preview", data_root_key)
        print("data root %s is not mounted here; command file preview is %s" % (data_root_key, registry_root))
    registry = Registry(registry_root, args.campaign)
    if(args.failure_text):
        record = plan_retry(args.failure_text, args.stage, args.ram_gb, args.hours, args.retry_number)
        record["stage"] = args.stage
        record["status"] = "retryable" if(record["retry"]) else "failed"
        record["campaign"] = args.campaign
        record["validation"] = "retry_plan"
        registry.append(record)
        print(record["status"])
        print(record)
        return
    bins = expand_bins(args.q2y_bins)
    lines = []
    cut_text = canonical_cut(args.acceptance_cut)
    if((args.stage in ["iteration_refresh_3d", "iteration_5d"]) or (args.iteration_action == "refresh")):
        k_max = 10 if(args.dimension == "5D") else 25
        lines.append(iteration_study_command(args.dimension, cut_text, bins, k_max, args.data_root))
    elif(args.stage == "unfold_3d"):
        if(args.iteration_action != "use_lookup"):
            raise SystemExit("unfold does not start an iteration study")
        for k_value, q2y_list, command in unfold_3d_commands(cut_text, args.phi_bins, args.background_source, bins, args.k_provenance, args.data_root):
            if("--iteration_study" in command):
                raise SystemExit("lookup unfold must not scan")
            lines.append(command)
            registry.append({
                "campaign": args.campaign,
                "stage": "unfold_3d",
                "status": "awaiting_jlab_validation" if(args.backend == "external") else "pending",
                "validation": "command_only",
                "dimension": "3D",
                "acceptance_cut": cut_text,
                "phi_mode": args.phi_bins,
                "background_source": args.background_source,
                "k_selected": k_value,
                "k_provenance": args.k_provenance,
                "q2y_bin": ",".join([str(q2y) for q2y in q2y_list]),
                "binning_version": BINNING_VERSION,
                "command": command,
                "backend": args.backend,
            })
    elif(args.stage == "aggregate"):
        lines.append(local_command("%s -t" % checkout_script(os.path.join(os.path.dirname(__file__), "aggregate_systematics.py"))))
    elif(args.stage == "bc_sensitivity"):
        spec = load_json(os.path.join(os.path.dirname(__file__), "systematics.json"))["bc_sensitivity"]
        for variable, values in spec.items():
            for value in values:
                counts = {"q2": 1, "y": 1, "z": 1, "pt": 1, "phi": 1}
                counts[variable] = value
                lines.append(bc_command(counts))
    elif(args.stage in ["early_chain", "groovy_rho", "groovy_55na", "dataframe", "make_batches", "rho_norm"]):
        built = early_chain_commands(os.path.join(registry.root, "commands"), args.data_root)
        if(built["status"] == "blocked"):
            registry.set_status(args.stage, "blocked")
            raise SystemExit(built["reason"])
        lines.extend(built["commands"])
        registry.append({
            "campaign": args.campaign, "stage": "rho_norm", "status": "checkpoint",
            "validation": "awaiting_factor_confirmation", "reason": built["reason"],
            "binning_version": BINNING_VERSION,
        })
    elif(args.stage in ["response", "response_priority", "response_5d", "response_3d", "response_1d", "response_2d", "diagnostic_dphi"]):
        products = response_commands(args.data_root)
        order = ["response_5d", "response_3d", "diagnostic_dphi", "response_1d", "response_2d"]
        if(args.stage in order):
            order = [args.stage]
        for stage_id in order:
            command = products[stage_id]
            if(not command):
                registry.set_status(stage_id, "blocked")
                lines.append("# %s blocked: Submit_Full has no Only_1D product; it is not replaced with 3D or 5D" % stage_id)
                continue
            lines.append(command)
    elif(args.stage in ["iteration_5d", "hybrid_attach", "bc", "rc_regenerate"]):
        command = later_commands(args.rc_mode, args.data_root).get(args.stage, "")
        if(not command):
            registry.set_status(args.stage, "blocked")
            raise SystemExit("%s has no command in rc_mode=%s" % (args.stage, args.rc_mode))
        lines.append(command)
    else:
        lines.append("# stage %s backend %s binning %s rc %s" % (args.stage, args.backend, BINNING_VERSION, args.rc_mode))
    folder = os.path.join(registry.root, "commands")
    path = write_command_file(folder, "%s.tcsh" % args.stage.replace(",", "_"), lines)
    print(path)
    for line in lines:
        print(line)
    from Campaign.swif_watch import launch_swif_workflow, start_unattended_recovery
    if(args.stage == "watch_swif2"):
        start_unattended_recovery(args.campaign, registry, dry_run=args.dry_run)
        return
    specs = specs_from_lines(args.stage, lines, os.path.join(registry.root, "logs"))
    launch_swif_workflow(args.campaign, graph["swif2"], specs, registry, dry_run=args.dry_run)


def expand_bins(text):
    if(text in ["all", "1-17"]):
        return list(range(1, 18))
    bins = []
    for piece in str(text).split(","):
        if("-" in piece):
            start, stop = piece.split("-")
            bins.extend(range(int(start), int(stop) + 1))
        else:
            bins.append(int(piece))
    return bins


if(__name__ == "__main__"):
    main()
