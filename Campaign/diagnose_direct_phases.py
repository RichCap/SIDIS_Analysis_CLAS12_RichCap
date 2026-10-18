#!/usr/bin/env python3
# Read-only status of the direct phases. It does not submit, cancel, or open ROOT files.
import glob
import json
import os
import sys

_BOOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if(_BOOT not in sys.path):
    sys.path.insert(0, _BOOT)

from Campaign.local_orchestrator import groovy_sbatch_path, input_folder, parse_groovy_sbatch, sacct_tasks


def load_phases(folder):
    path = os.path.join(folder, "phase_status.json")
    if(not os.path.isfile(path)):
        return {}
    handle = open(path)
    payload = json.load(handle)
    handle.close()
    return dict(payload.get("phases", {}))


def owner_lines(log_dir, prefix):
    found = {}
    if(not os.path.isdir(log_dir)):
        return found
    for path in glob.glob(os.path.join(log_dir, "%s*.log" % prefix)):
        handle = open(path)
        text = handle.read()
        handle.close()
        for line in text.splitlines():
            if(not line.startswith("# owner=")):
                continue
            fields = {}
            for part in line[2:].split():
                if("=" in part):
                    key, value = part.split("=", 1)
                    fields[key] = value
            if("owner" in fields):
                found[os.path.basename(path)] = fields
    return found


def count_sacct(arrays):
    counts = {"COMPLETED": 0, "other": 0}
    if(arrays is None):
        return None
    for tasks in arrays.values():
        for state, exit_code in tasks.values():
            if((state == "COMPLETED") and str(exit_code).startswith("0:")):
                counts["COMPLETED"] += 1
            else:
                counts["other"] += 1
    return counts


def report_groovy(folder):
    groovy_dir = os.path.join(_BOOT, "Data_Files_Groovy")
    log_dir = "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/parallel_logs"
    workloads = [("rho0", "gdf", "job_gen_"), ("rho0", "mdf", "job_"), ("clasdis", "gdf", "job_gen_"), ("clasdis", "mdf", "job_")]
    for source, mc_type, prefix in workloads:
        print("workload groovy %s %s" % (source, mc_type))
        script = groovy_sbatch_path(groovy_dir, source, mc_type)
        if(not os.path.isfile(script)):
            print("  sbatch script missing")
            print("  outcome unresolved: no submission record")
            continue
        job_name, array_spec, manifest = parse_groovy_sbatch(script)
        print("  sbatch %s" % os.path.basename(script))
        print("  job_name %s" % job_name)
        print("  array %s" % array_spec)
        print("  manifest %s" % manifest)
        arrays = sacct_tasks(job_name=job_name)
        if(arrays is None):
            print("  sacct not read")
        else:
            counts = count_sacct(arrays)
            print("  sacct arrays %s" % ",".join(sorted(arrays.keys())))
            print("  sacct COMPLETED_exit0 %d" % counts["COMPLETED"])
            print("  sacct other %d" % counts["other"])
        owners = owner_lines(log_dir, prefix)
        success = 0
        failed = 0
        for fields in owners.values():
            if(fields.get("owner") != "local"):
                continue
            if(fields.get("outcome") == "success"):
                success += 1
            elif(fields.get("outcome") == "failed"):
                failed += 1
        print("  local owner lines success %d failed %d" % (success, failed))
        if((success == 0) and (failed == 0)):
            print("  outcome unresolved: ownership was not recorded; sacct is shown and is not the verdict")
        else:
            print("  outcome from owning local records: success %d failed %d" % (success, failed))


def report_phases(phases, names):
    for name in names:
        status = phases.get(name)
        if(status):
            print("phase %s: %s" % (name, status))
        else:
            print("phase %s: no completion record" % name)


def main():
    data_root = "work_b"
    if(("-droot" in sys.argv) or ("--data_root" in sys.argv)):
        flag = "-droot" if("-droot" in sys.argv) else "--data_root"
        data_root = sys.argv[sys.argv.index(flag) + 1]
    folder = input_folder(data_root, True)
    phases = load_phases(folder)
    print("phase records %s" % os.path.join(folder, "phase_status.json"))
    report_groovy(folder)
    report_phases(phases, ["groovy", "dataframe", "make_batches", "rho_hist", "rho_fit", "rc_build", "rc_compare", "bc_hist", "bc_hadd", "bc_factors"])
    print("RC and BC input verdicts need owner lines in their logs. Without those lines the outcome stays unresolved.")
    print("This command did not submit, cancel, or open a ROOT file.")


if(__name__ == "__main__"):
    main()
