#!/usr/bin/env python3
# Static checks for the systematic campaign. No SLURM submission and no ROOT production.
import os
import sys

_BOOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if(_BOOT not in sys.path):
    sys.path.insert(0, _BOOT)

from Campaign.systematics_campaign import hpp_pair, self_test
from Campaign.systematics_worker_ledger import ledger_self_test
from Campaign import run_sidis_systematics_campaign as runner


def squeue_compact_is_pending():
    df = os.path.join(_BOOT, "Histo_Files_ROOT", "DataFrames")
    if(df not in sys.path):
        sys.path.insert(0, df)
    import run_sidis_DataFrame_pipeline as pipeline
    state = pipeline._parse_squeue_task_state("12345", 1, "12345_[1-17] PD")
    if(state != "PD"):
        raise SystemExit("compact pending array was not PD, got %s" % state)
    running = pipeline._parse_squeue_task_state("12345", 4, "12345_4 R")
    if(running == "PD"):
        raise SystemExit("a running task was treated as pending")


def hpp_matches_submit_full():
    df = os.path.join(_BOOT, "Histo_Files_ROOT", "DataFrames")
    if(df not in sys.path):
        sys.path.insert(0, df)
    import Submit_Full_Histogram_Creation_Pipeline as submit_full
    pure, comb = hpp_pair("work_b", "Final_Thesis")
    other_pure, other_comb = submit_full.hpp_paths_from_tag("Final_Thesis", "work_b")
    if((pure != other_pure) or (comb != other_comb)):
        raise SystemExit("HPP paths diverged from Submit_Full")


def dry_run_writes_manifest():
    code = runner.main(["-n", "-c", "systematics_self_test", "-droot", "work_b", "-wm", "both", "-mlw", "41"])
    if(code != 0):
        raise SystemExit("dry-run exit %s" % code)
    camp = runner.campaign_directory("work_b", "systematics_self_test")
    manifest = runner.read_manifest(camp)
    if(manifest is None):
        raise SystemExit("dry-run did not write a manifest")
    if(len(manifest["phase1"]) != 34):
        raise SystemExit("dry-run phase1 count")
    if(len(manifest["phase2"]) != 74):
        raise SystemExit("dry-run both-mode phase2 count")
    nominal = [row for row in manifest["phase1"] if(row["id"] == "nominal")][0]
    other = [row for row in manifest["phase1"] if(row["id"] == "chi2_strict_pip")][0]
    if("cut_Complete_SIDIS_chi2_strict_pip" not in " ".join(other["command"])):
        raise SystemExit("dry-run dropped the strict chi2 cut")
    if("-mac" not in other["command"]):
        raise SystemExit("dry-run dropped Bank matching")
    if(nominal["hpp_nospline"] in [None, ""]):
        raise SystemExit("manifest is missing the noSpline path")
    resumed = runner.main(["-n", "-rs", "-c", "systematics_self_test", "-droot", "work_b", "-wm", "both", "-ht", "NotTheOriginalTag"])
    if(resumed != 0):
        raise SystemExit("resume dry-run exit %s" % resumed)
    again = runner.read_manifest(camp)
    again_nom = [row for row in again["phase1"] if(row["id"] == "nominal")][0]
    if(again_nom["hpp_nospline"] != nominal["hpp_nospline"]):
        raise SystemExit("resume dry-run replaced the recorded HPP path")
    refused = runner.main(["-n", "-c", "systematics_cap_reject", "-droot", "work_b", "-mlw", "42"])
    if(refused == 0):
        raise SystemExit("cap 42 was accepted")


def main():
    self_test()
    ledger_self_test()
    squeue_compact_is_pending()
    hpp_matches_submit_full()
    dry_run_writes_manifest()
    print("systematics campaign self-test ok")
    return 0


if(__name__ == "__main__"):
    sys.exit(main())
