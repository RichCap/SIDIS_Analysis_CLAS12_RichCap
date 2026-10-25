# Read the untagged 5D iteration profiles. There is no q2y_bin.
# rms_aligned is the bin error of Iteration_Study_MeanResiduals, not RMSResiduals.
import os
import sys

_BOOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if(_BOOT not in sys.path):
    sys.path.insert(0, _BOOT)

from merge_bayesian_iteration_lookup import canonical_cut
from score_3d_iteration_closure import bin_value


def rows_from_values(cut, by_k):
    # by_k[k] = chi2, mean_signed, mean_error, rms_aligned
    cut_text = canonical_cut(cut)
    rows = []
    for k in sorted(by_k):
        chi2, mean_signed, mean_error, rms_aligned = by_k[k]
        if((chi2 is None) or (mean_signed is None) or (mean_error is None) or (rms_aligned is None)):
            continue
        rows.append({
            "sample": "data",
            "cut": cut_text,
            "k": int(k),
            "chi2": float(chi2),
            "mean_residual": float(mean_signed),
            "mean_abs": abs(float(mean_signed)),
            "rms_aligned": float(rms_aligned),
            "mean_error": float(mean_error),
        })
    return rows


def load_5d_rows(path, cut, k_max=10):
    import ROOT
    ROOT.gROOT.SetBatch(True)
    tfile = ROOT.TFile.Open(path, "READ")
    if((tfile is None) or tfile.IsZombie()):
        raise RuntimeError("Could not open %s" % path)
    chi2_h = tfile.Get("Iteration_Study_Chi2")
    mean_h = tfile.Get("Iteration_Study_MeanResiduals")
    err_h  = tfile.Get("Iteration_Study_RMSError")
    if((not chi2_h) or (not mean_h) or (not err_h)):
        tfile.Close()
        raise RuntimeError("5D iteration file is missing an untagged diagnostic histogram")
    by_k = {}
    for k in range(1, int(k_max) + 1):
        chi2 = bin_value(chi2_h, k, False)
        mean_signed = bin_value(mean_h, k, False)
        mean_error = bin_value(err_h, k, False)
        rms_aligned = bin_value(mean_h, k, True)
        if((chi2 is None) and (k == 1)):
            tfile.Close()
            raise RuntimeError("5D profile axis does not place k=1 on a bin low edge in %s" % path)
        by_k[k] = (chi2, mean_signed, mean_error, rms_aligned)
    tfile.Close()
    rows = rows_from_values(cut, by_k)
    if(("q2y" in rows[0]) if(rows) else False):
        raise RuntimeError("5D rows must not carry q2y")
    return rows


def self_test():
    rows = rows_from_values("0.0005", {1: (1.0, 0.2, 0.1, 0.05), 2: (None, 0.2, 0.1, 0.05)})
    if(rows[0]["cut"] != "0.0005"):
        raise SystemExit("0.0005 was reformatted")
    if(len(rows) != 1):
        raise SystemExit("missing chi2 was kept")
    if("q2y" in rows[0]):
        raise SystemExit("5D row has q2y")
    print("load_5d self_test ok")


if(__name__ == "__main__"):
    self_test()
