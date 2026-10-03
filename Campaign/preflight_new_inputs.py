#!/usr/bin/env python3
# Expand the new HIPO globs and refuse to submit if the selection is wrong.
import glob
import os
import sys

_BOOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if(_BOOT not in sys.path):
    sys.path.insert(0, _BOOT)

from Campaign.early_chain import groovy_command, groovy_file_command
from Campaign.ifarm_inputs import classify_rho_name, load_ifarm_inputs

EXPECTED_RHO = 10
EXPECTED_CLASDIS = 170


def expand_glob(pattern):
    matches = sorted(glob.glob(pattern))
    return matches


def classify_list(paths, expected_kind):
    bad = []
    for path in paths:
        label = classify_rho_name(os.path.basename(path))
        if(expected_kind == "rho0_new"):
            if(label != "rho0_new"):
                bad.append((path, label or "unclassified"))
        elif(label not in ["", None]):
            bad.append((path, label))
    return bad


def run_preflight(command_dir=None, data_root="work_b"):
    config = load_ifarm_inputs()
    rho_paths = expand_glob(config.get("rho_hipo_glob", ""))
    clasdis_paths = expand_glob(config.get("clasdis_55na_hipo_glob", ""))
    print("data_root %s" % data_root)
    print("rho0 matches %d (current expectation %d)" % (len(rho_paths), EXPECTED_RHO))
    for path in rho_paths:
        print("  rho0 %s" % path)
    print("55nA clasdis matches %d (current expectation %d)" % (len(clasdis_paths), EXPECTED_CLASDIS))
    for path in clasdis_paths:
        print("  clasdis %s" % path)
    if(len(rho_paths) != EXPECTED_RHO):
        print("expectation_mismatch rho0 %d != %d" % (len(rho_paths), EXPECTED_RHO))
    if(len(clasdis_paths) != EXPECTED_CLASDIS):
        print("expectation_mismatch clasdis %d != %d" % (len(clasdis_paths), EXPECTED_CLASDIS))
    rho_txt = "new_rho0_hipo.txt" if(not command_dir) else os.path.join(command_dir, "new_rho0_hipo.txt")
    na_txt = "new_55na_hipo.txt" if(not command_dir) else os.path.join(command_dir, "new_55na_hipo.txt")
    print("list_command %s" % groovy_command("rho0", "gdf", rho_txt, data_root))
    print("list_command %s" % groovy_command("rho0", "mdf", rho_txt, data_root))
    print("list_command %s" % groovy_command("clasdis", "gdf", na_txt, data_root))
    print("list_command %s" % groovy_command("clasdis", "mdf", na_txt, data_root))
    if((len(rho_paths) == 0) or (len(clasdis_paths) == 0)):
        print("preflight_failed glob did not resolve on this filesystem; no jobs submitted")
        return 2
    rho_bad = classify_list(rho_paths, "rho0_new")
    clasdis_bad = classify_list(clasdis_paths, "clasdis")
    if((len(rho_bad) > 0) or (len(clasdis_bad) > 0)):
        print("preflight_failed classification")
        for path, label in rho_bad + clasdis_bad:
            print("  %s -> %s" % (path, label))
        print("preflight_failed no jobs submitted")
        return 2
    if(command_dir):
        os.makedirs(command_dir, exist_ok=True)
        rho_list = os.path.join(command_dir, "new_rho0_hipo.txt")
        clasdis_list = os.path.join(command_dir, "new_55na_hipo.txt")
        handle = open(rho_list, "w")
        handle.write("\n".join(rho_paths) + "\n")
        handle.close()
        handle = open(clasdis_list, "w")
        handle.write("\n".join(clasdis_paths) + "\n")
        handle.close()
    for path in rho_paths:
        print(groovy_file_command("rho0", "gdf", path, data_root))
        print(groovy_file_command("rho0", "mdf", path, data_root))
    for path in clasdis_paths:
        print(groovy_file_command("clasdis", "gdf", path, data_root))
        print(groovy_file_command("clasdis", "mdf", path, data_root))
    print("preflight_ok")
    return 0


def main():
    folder = sys.argv[1] if(len(sys.argv) > 1) else None
    data_root = sys.argv[2] if(len(sys.argv) > 2) else "work_b"
    raise SystemExit(run_preflight(folder, data_root))


if(__name__ == "__main__"):
    main()
