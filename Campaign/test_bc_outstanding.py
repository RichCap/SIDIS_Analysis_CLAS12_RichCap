# Local checks for the nine BC sensitivity configurations. No SLURM submission.
import os
import sys
import tempfile

_BOOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if(_BOOT not in sys.path):
    sys.path.insert(0, _BOOT)
sys.path.insert(0, os.path.join(_BOOT, "BC_Corrections"))

from Campaign.local_orchestrator import (
    BC_OUTSTANDING_TAG, bc_hist_argv, bc_is_outstanding, bc_outstanding_configurations,
    bc_outstanding_launch_commands, bc_required_histograms_ok, bc_run_tag,
    remove_incomplete_bc_outputs,
)
from Run_BC_Scripts_Locally import hybrid_local_action


def test_inventory():
    configs = bc_outstanding_configurations()
    labels = [config["label"] for config in configs]
    if(labels != ["sens_z_3", "sens_z_5", "sens_z_7", "sens_pt_3", "sens_pt_5", "sens_pt_7", "sens_phi_5", "sens_phi_7", "sens_phi_9"]):
        raise SystemExit("inventory %s" % labels)
    for config in configs:
        counts = config["counts"]
        varied = config["label"].split("_")[1]
        if(counts[varied] == 1):
            raise SystemExit("varied axis stayed at 1 for %s" % config["label"])
        for axis in ["q2", "y", "z", "pt", "phi"]:
            if((axis != varied) and (counts[axis] != 1)):
                raise SystemExit("extra axis changed for %s" % config["label"])
    if(any(("q2" in label) or (label in ["", "nominal"]) for label in labels)):
        raise SystemExit("nominal or q2 was included")
    if(bc_is_outstanding("sens_y_7") or bc_is_outstanding("")):
        raise SystemExit("completed configuration was treated as outstanding")


def test_commands():
    runner = "Run_BC_Scripts_Locally.py"
    z3 = [config for config in bc_outstanding_configurations() if(config["label"] == "sens_z_3")][0]
    tag = bc_run_tag(z3["label"], BC_OUTSTANDING_TAG)
    argv = bc_hist_argv(runner, z3["label"], z3["counts"], tag, "msg", ["done_a.root"])
    text = " ".join(argv)
    for needed in ["-j 5", "-st 03:00:00", "-jn BC_sens_z_3", "-rt %s" % tag, "-nbq 1 -nby 1 -nbz 3 -nbpt 1 -nbh 1", "-ex done_a.root"]:
        if(needed not in text):
            raise SystemExit("missing %s in %s" % (needed, text))
    if("-j 10" in text):
        raise SystemExit("outstanding command used 10 workers")
    nominal = bc_hist_argv(runner, "", {"q2": 3, "y": 3, "z": 3, "pt": 3, "phi": 5}, "nominal_tag", "msg", [])
    nominal_text = " ".join(nominal)
    if("-j 10" not in nominal_text):
        raise SystemExit("nominal lost its worker setting")
    if("-st" in nominal_text):
        raise SystemExit("nominal command changed the SLURM time")
    commands = bc_outstanding_launch_commands("python3", "Campaign/run_sidis_campaign.py", "work_b", None, True)
    if(len(commands) != 9):
        raise SystemExit("launch count %s" % len(commands))
    started = []

    def run_one(command):
        started.append(command[command.index("-v") + 1])
        if(started[-1] == "sens_z_5"):
            return 1
        return 0

    results = [run_one(command) for command in commands]
    if((len(started) != 9) or (1 not in results) or ("sens_q2_3" in started)):
        raise SystemExit("failure isolation %s %s" % (started, results))


def test_ownership():
    if(hybrid_local_action("", None, False) != "start"):
        raise SystemExit("missing array did not allow local work")
    if(hybrid_local_action("13647621", "PD", True) != "start"):
        raise SystemExit("pending canceled task was not local")
    if(hybrid_local_action("13647621", "PD", False) != "defer"):
        raise SystemExit("uncanceled pending task started locally")
    if(hybrid_local_action("13647621", None, False) != "defer"):
        raise SystemExit("absent queue row started locally")
    if(hybrid_local_action("13647621", "RETRY", False) != "retry"):
        raise SystemExit("unknown queue state started locally")
    if(hybrid_local_action("13647621", "R", True) != "defer"):
        raise SystemExit("running task started locally")


def test_root_recovery():
    import Campaign.local_orchestrator as orchestrator
    import ROOT
    counts = {"q2": 1, "y": 1, "z": 3, "pt": 1, "phi": 1}
    folder = tempfile.mkdtemp(prefix="bc_outstanding_")
    good_path = os.path.join(folder, "good.root")
    bad_path = os.path.join(folder, "bad.root")
    good = ROOT.TFile(good_path, "RECREATE")
    hist = ROOT.TH2D("Histogram Bin (1-1)-(Num SubBins=3)-(Extra phi_h SubBins=2)", "good", 5, -0.5, 4.5, 24, 0.5, 24.5)
    extra = ROOT.TH2D("Histogram Bin (3-6)-(Num SubBins=3)-(Extra phi_h SubBins=2)", "extra", 5, -0.5, 4.5, 24, 0.5, 24.5)
    hist.Write()
    extra.Write()
    good.Close()
    bad = ROOT.TFile(bad_path, "RECREATE")
    wrong = ROOT.TH2D("Histogram Bin (1-1)-(Num SubBins=3)-(Extra phi_h SubBins=2)", "bad", 3, -0.5, 2.5, 24, 0.5, 24.5)
    wrong.Write()
    bad.Close()
    good_file = ROOT.TFile.Open(good_path)
    bad_file = ROOT.TFile.Open(bad_path)
    if(not bc_required_histograms_ok(good_file, counts, [(1, 1)])):
        raise SystemExit("valid histogram was rejected")
    if(bc_required_histograms_ok(bad_file, counts, [(1, 1)])):
        raise SystemExit("wrong axis was accepted")
    good_file.Close()
    bad_file.Close()
    saved_candidates = orchestrator.bc_output_candidates
    saved_status = orchestrator.bc_histogram_status

    def candidates(input_path, label, tag):
        if(os.path.basename(input_path) == "keep.root"):
            return [good_path]
        return [bad_path]

    def status(path, counts_in):
        if(path == good_path):
            return "complete"
        return "incomplete"

    orchestrator.bc_output_candidates = candidates
    orchestrator.bc_histogram_status = status
    try:
        remove_incomplete_bc_outputs("keep.root", "sens_z_3", counts, False, "tag")
        remove_incomplete_bc_outputs("redo.root", "sens_z_3", counts, False, "tag")
    finally:
        orchestrator.bc_output_candidates = saved_candidates
        orchestrator.bc_histogram_status = saved_status
    if(not os.path.isfile(good_path)):
        raise SystemExit("validated output was removed")
    if(os.path.isfile(bad_path)):
        raise SystemExit("incomplete output was left for UPDATE")
    os.remove(good_path)
    os.rmdir(folder)


def main():
    test_inventory()
    test_commands()
    test_ownership()
    test_root_recovery()
    print("bc outstanding self-test ok")


if(__name__ == "__main__"):
    main()
