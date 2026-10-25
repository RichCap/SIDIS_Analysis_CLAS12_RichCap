#!/usr/bin/env python3
# Fit unfolded phi_h slices with Fitting_Phi_Function and compare to the injected moments.
# No radiative correction and no bin-centering correction.

import argparse
import os
import re
import sys

_BOOT = os.path.abspath(os.path.dirname(__file__))
if(_BOOT not in sys.path):
    sys.path.insert(0, _BOOT)

import evaluate_spline_reference as spline_ref


class FitArgs(object):
    def __init__(self):
        self.fit = True
        self.use_spline_init = False
        self.fit_init_file = None
        self.CrossSection_Norm = False
        self.sim = True
        self.smearing_options = "smear"
        self.Common_Int_Bins = False


def parse_args():
    parser = argparse.ArgumentParser(description="fit_pseudo_data_closure.py:\n\tFit unfolded phi distributions and compare them to the injected moments.")
    parser.add_argument("-r", "--root", required=True, help="Unfolded ROOT file.\n")
    parser.add_argument("-s", "--sample", required=True, choices=["nominal", "Acc", "Spline", "AccSpline"],
                        help="Pseudo-data sample. nominal and Acc are flat. Spline and AccSpline use the authoritative spline.\n")
    parser.add_argument("-c", "--cut", required=True, type=float, help="Acceptance cut.\n")
    parser.add_argument("-k", "--iteration", required=True, type=int, help="Bayesian iteration used for this file.\n")
    parser.add_argument("-o", "--out", required=True, help="Output TSV.\n")
    parser.add_argument("-q", "--q2y", type=int, default=0, help="One Q2-y bin. 0 means every bin in the file.\n")
    parser.add_argument("-ns", "--n_sigma", type=float, default=3.0, help="A slice passes when both moments are within this many fit errors.\n")
    parser.add_argument("-ph", "--phi_bins", type=int, default=24, choices=[12, 24], help="24 keeps the 8-bin minimum. 12 uses 4 filled merged bins.\n")
    parser.add_argument("-mf", "--min_filled", type=int, default=None, help="Slices with fewer filled phi bins are reported and not counted. Default is 8 for 24 bins and 4 for 12.\n")
    return parser.parse_args()


def bin_centers(q2y, zpt):
    from BC_Corrections.Creation_of_Parameter_Fits import get_bin_centers
    q2_y = get_bin_centers("Q2_y", q2y)
    z_pt = get_bin_centers("z_pT", q2y, z_pT_num=zpt)
    if((q2_y in [None, [None, None]]) or (z_pt in [None, [None, None]])):
        return None
    q2, y = q2_y
    # get_bin_centers("z_pT") returns [pT, z], not [z, pT].
    pT, z = z_pt
    xB = spline_ref.xb_from_q2_y(q2, y)
    return xB, y, z, pT


def reference_moments(sample, q2y, zpt):
    if(sample in ["nominal", "Acc"]):
        return 0.0, 0.0
    centers = bin_centers(q2y, zpt)
    if(centers is None):
        return None
    xB, y, z, pT = centers
    return spline_ref.moments_at(xB, y, z, pT)


def filled_bins(hist):
    count = 0
    for i in range(1, hist.GetNbinsX() + 1):
        if(hist.GetBinContent(i) != 0.0):
            count += 1
    return count


def _as_fit(b_pair, c_pair, chisq):
    if(not isinstance(b_pair, (list, tuple))):
        return None
    chi2 = float(chisq[0]) if(isinstance(chisq, (list, tuple))) else float("nan")
    ndf = chisq[1] if(isinstance(chisq, (list, tuple))) else ""
    try:
        ndf = float(ndf)
    except (TypeError, ValueError):
        ndf = ""
    return {
        "B": float(b_pair[0]),
        "B_err": float(b_pair[1]),
        "C": float(c_pair[0]),
        "C_err": float(c_pair[1]),
        "chi2": chi2,
        "ndf": ndf,
    }


def _zero_seed_fit(hist):
    # Same modulation as Fitting_Phi_Function. The built-in seed starts at B=C=1 and the
    # second pass locks the limits, which invents a modulation on a gapped but flat slice.
    import ROOT
    func = ROOT.TF1("closure_fit_" + hist.GetName(), "[0]*(1+[1]*cos(x*3.1415926/180)+[2]*cos(2*x*3.1415926/180))", 0, 360)
    mean = 0.0
    n_pos = 0
    lo = 0.0
    hi = 360.0
    for i in range(1, hist.GetNbinsX() + 1):
        if(hist.GetBinContent(i) == 0.0):
            continue
        if(n_pos == 0):
            lo = hist.GetXaxis().GetBinLowEdge(i)
        hi = hist.GetXaxis().GetBinUpEdge(i)
        mean += hist.GetBinContent(i)
        n_pos += 1
    if(n_pos == 0):
        return None
    func.SetRange(lo, hi)
    func.SetParameter(0, mean / n_pos)
    func.SetParameter(1, 0.0)
    func.SetParameter(2, 0.0)
    hist.Fit(func, "QR")
    return _as_fit(
        [func.GetParameter(1), func.GetParError(1)],
        [func.GetParameter(2), func.GetParError(2)],
        [func.GetChisquare(), func.GetNDF()],
    )


def _chi2_ndf(result):
    if((result is None) or (result["ndf"] in ["", 0, 0.0])):
        return 1.0e99
    return result["chi2"] / float(result["ndf"])


def fit_one(hist, q2y, zpt):
    from Simple_RooUnfold_SelfContained import Fitting_Phi_Function
    args = FitArgs()
    out = Fitting_Phi_Function(hist, Method="Bayesian", Fitting="default", Special=[q2y, zpt], args=args, Allow_Normalization=False)
    builtin = None
    if(out not in ["ERROR", None]):
        builtin = _as_fit(out[4], out[5], out[2])
    seeded = _zero_seed_fit(hist)
    # Keep the same functional form. Prefer the fit that actually describes the slice.
    if(_chi2_ndf(seeded) <= _chi2_ndf(builtin)):
        return seeded
    return builtin


def main():
    args = parse_args()
    if(args.min_filled is None):
        args.min_filled = 4 if(args.phi_bins == 12) else 8
    import ROOT
    ROOT.gROOT.SetBatch(True)
    ROOT.gErrorIgnoreLevel = ROOT.kError
    tfile = ROOT.TFile.Open(args.root, "READ")
    if((tfile is None) or tfile.IsZombie()):
        print("Could not open " + args.root, file=sys.stderr)
        return 1
    rows = []
    pattern = re.compile(r"\(MultiDim_3D_Histo\)_\(Bayesian\).*\(Q2_y_Bin_(\d+)\).*\(z_pT_Bin_(\d+)\)")
    for key in tfile.GetListOfKeys():
        name = key.GetName()
        match = pattern.search(name)
        if(match is None):
            continue
        if("z_pT_Bin_All" in name):
            continue
        q2y = int(match.group(1))
        zpt = int(match.group(2))
        if((args.q2y != 0) and (q2y != args.q2y)):
            continue
        hist = tfile.Get(name)
        n_filled = filled_bins(hist)
        ref = reference_moments(args.sample, q2y, zpt)
        row = {
            "cut": f"{args.cut:.3f}",
            "sample": args.sample,
            "k": args.iteration,
            "q2y": q2y,
            "zpt": zpt,
            "n_filled": n_filled,
        }
        if(n_filled < args.min_filled):
            row.update({"status": "too_few_bins", "B": "", "B_err": "", "C": "", "C_err": "", "B_ref": "", "C_ref": "", "chi2": "", "ndf": ""})
            rows.append(row)
            continue
        if(ref is None):
            row.update({"status": "no_reference", "B": "", "B_err": "", "C": "", "C_err": "", "B_ref": "", "C_ref": "", "chi2": "", "ndf": ""})
            rows.append(row)
            continue
        fitted = fit_one(hist, q2y, zpt)
        if(fitted is None):
            row.update({"status": "fit_failed", "B": "", "B_err": "", "C": "", "C_err": "", "B_ref": ref[0], "C_ref": ref[1], "chi2": "", "ndf": ""})
            rows.append(row)
            continue
        b_ref, c_ref = ref
        b_ok = abs(fitted["B"] - b_ref) <= args.n_sigma * max(fitted["B_err"], 1.0e-12)
        c_ok = abs(fitted["C"] - c_ref) <= args.n_sigma * max(fitted["C_err"], 1.0e-12)
        row.update(fitted)
        row["B_ref"] = b_ref
        row["C_ref"] = c_ref
        row["status"] = "pass" if(b_ok and c_ok) else "fail"
        rows.append(row)
    tfile.Close()
    columns = ["cut", "sample", "k", "q2y", "zpt", "n_filled", "status", "B", "B_err", "C", "C_err", "B_ref", "C_ref", "chi2", "ndf"]
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w") as handle:
        handle.write("\t".join(columns) + "\n")
        for row in sorted(rows, key=lambda item: (int(item["q2y"]), int(item["zpt"]))):
            handle.write("\t".join(str(row.get(col, "")) for col in columns) + "\n")
    n_pass = sum(1 for row in rows if(row["status"] == "pass"))
    n_fail = sum(1 for row in rows if(row["status"] == "fail"))
    n_skip = sum(1 for row in rows if(row["status"] not in ["pass", "fail"]))
    print(f"Wrote {args.out} pass={n_pass} fail={n_fail} skipped={n_skip}")
    return 0


if(__name__ == "__main__"):
    sys.exit(main() or 0)
