#!/usr/bin/env python3
"""Plot RooUnfoldParms iteration-study diagnostics and recommend k per Q2-y bin."""

import argparse
import math
import os
import re
import sys

_BOOT = os.path.abspath(os.path.dirname(__file__))
if(_BOOT not in sys.path):
    sys.path.insert(0, _BOOT)


def parse_args():
    p = argparse.ArgumentParser(description="Plot χ² diagnostic, χ² change, mean residuals, and RMS error vs iteration.")
    p.add_argument('root_file', help="ROOT file containing Iteration_Study_* histograms.")
    p.add_argument('-o', '--out', default="Unfold_Iteration_Study_3D/",
                   help="Output directory for PDFs.")
    # p.add_argument('-kmin', '--clip-min', type=int, default=3, help="Minimum recommended k.")  # Changed default to 1 on 9/16/2026 (iteration 2 is valid)
    p.add_argument('-kmin', '--clip-min', type=int, default=1, help="Minimum recommended k (1 allows iteration 2).")
    p.add_argument('-kmax', '--clip-max', type=int, default=25, help="Maximum recommended k.")
    p.add_argument('-plat', '--plateau', type=float, default=0.05,
                   help="χ²-change plateau threshold.")
    p.add_argument('-spread', '--flag-spread', type=int, default=4,
                   help="Flag if the three k choices differ by this many iterations or more.")
    p.add_argument('-eps', '--epsilon', type=float, default=1e-12)
    return p.parse_args()


def silence_root():
    import ROOT
    ROOT.gROOT.SetBatch(True)
    ROOT.gErrorIgnoreLevel = ROOT.kError


def extract_iteration_series(hist, kmax=None):
    """Extract one value per integer iteration from a TProfile or TH1. Print (k, value) pairs."""
    by_k = {}
    if(hist is None):
        return by_k
    is_prof = False
    try:
        is_prof = bool(hist.InheritsFrom("TProfile"))
    except Exception:
        is_prof = False
    last = hist.GetNbinsX() + (1 if(is_prof) else 0)
    for i in range(1, last + 1):
        if(is_prof):
            try:
                if(hist.GetBinEntries(i) <= 0):
                    continue
            except Exception:
                pass
        xlow = hist.GetBinLowEdge(i)
        x = hist.GetBinCenter(i)
        if(abs(xlow - round(xlow)) <= 1e-6):
            k = int(round(xlow))
        else:
            k = int(round(x))
        if(k < 1):
            continue
        if((kmax is not None) and (k > kmax)):
            continue
        if(k in by_k):
            raise RuntimeError(f"duplicate iteration k={k} in {hist.GetName()}")
        by_k[k] = hist.GetBinContent(i)
    print(f"{hist.GetName()} (k, value):")
    for k in sorted(by_k):
        print(f"  {k:3d}  {by_k[k]:.6g}")
    if(kmax is not None):
        missing = [k for k in range(1, kmax + 1) if(k not in by_k)]
        if(missing):
            print(f"  missing iterations: {missing}")
    return by_k


def chi2_change(chi2_by_k, eps):
    keys = sorted(chi2_by_k)
    ch = {}
    for i, k in enumerate(keys):
        if(i == 0):
            continue
        prev = keys[i - 1]
        den = max(abs(chi2_by_k[prev]), eps)
        ch[k] = abs(chi2_by_k[k] - chi2_by_k[prev]) / den
    return ch


def first_diff(by_k):
    keys = sorted(by_k)
    d1 = {}
    for i in range(1, len(keys)):
        d1[keys[i]] = by_k[keys[i]] - by_k[keys[i - 1]]
    return d1


def second_diff(d1):
    keys = sorted(d1)
    d2 = {}
    for i in range(1, len(keys)):
        d2[keys[i]] = d1[keys[i]] - d1[keys[i - 1]]
    return d2


def first_local_min(by_k, kmin):
    keys = [k for k in sorted(by_k) if(k >= kmin)]
    d1 = first_diff(by_k)
    for i in range(1, len(keys)):
        k_prev, k = keys[i - 1], keys[i]
        if((k not in d1) or (k_prev not in d1 and i == 1)):
            pass
        sl_prev = d1.get(k_prev, by_k[k] - by_k[k_prev] if(k_prev in by_k) else 0)
        sl = d1.get(k)
        if((sl_prev is not None) and (sl is not None) and (sl_prev < 0) and (sl >= 0)):
            return k_prev if(by_k[k_prev] <= by_k[k]) else k
    return None


def local_min_abs_d1(d1, kmin):
    keys = [k for k in sorted(d1) if(k >= kmin)]
    if(not keys):
        return None
    best_k, best = keys[0], abs(d1[keys[0]])
    for k in keys[1:]:
        av = abs(d1[k])
        if(av < best):
            best_k, best = k, av
    return best_k


def flattening_from_slope(d1, d2, kmin, eps=1e-12):
    keys = [k for k in sorted(d1) if(k >= kmin)]
    for i in range(len(keys) - 1):
        k0, k1 = keys[i], keys[i + 1]
        if(k1 != k0 + 1):
            continue
        small0 = abs(d1[k0]) <= max(abs(d1[k0]) * 0 + 0, abs(d1.get(k0, 0)))
        # Slope approaching zero: |d1| local-small and curvature not swinging.
        if((abs(d1[k0]) <= abs(d1.get(keys[max(i - 1, 0)], d1[k0])) + eps) and (abs(d1[k1]) <= abs(d1[k0]) + eps)):
            c0 = abs(d2.get(k0, 0))
            c1 = abs(d2.get(k1, 0))
            if(c1 <= c0 + eps):
                return k0
    return None


def fallback_rel_change(by_k, kmin, thresh, eps):
    keys = [k for k in sorted(by_k) if(k >= kmin)]
    for i in range(1, len(keys) - 1):
        k0, k1 = keys[i], keys[i + 1]
        if(k1 != k0 + 1):
            continue
        prev = keys[i - 1]
        den0 = max(abs(by_k[prev]), eps)
        den1 = max(abs(by_k[k0]), eps)
        r0 = abs(by_k[k0] - by_k[prev]) / den0
        r1 = abs(by_k[k1] - by_k[k0]) / den1
        if((r0 < thresh) and (r1 < thresh)):
            return k0
    return None


def argmin_abs(by_k, kmin):
    best_k, best_v = None, None
    for k, v in by_k.items():
        if(k < kmin):
            continue
        av = abs(v)
        if((best_v is None) or (av < best_v)):
            best_k, best_v = k, av
    return best_k


def argmin_before_rise(by_k, kmin):
    keys = sorted(k for k in by_k if(k >= kmin))
    if(not keys):
        return None
    best_k = keys[0]
    best_v = by_k[best_k]
    for k in keys[1:]:
        if(by_k[k] < best_v):
            best_k, best_v = k, by_k[k]
        elif(by_k[k] > best_v * 1.05):
            break
    return best_k


def median_int(vals):
    s = sorted(v for v in vals if(v is not None))
    if(not s):
        return None
    mid = len(s) // 2
    if(len(s) % 2):
        return s[mid]
    return int(round(0.5 * (s[mid - 1] + s[mid])))


def parse_q2y(name):
    m = re.search(r"Q2y_(-?\d+)", name)
    if(m):
        return m.group(1)
    return "all"


def group_hists(tfile):
    groups = {}
    keys = tfile.GetListOfKeys()
    if(keys is None):
        return groups
    for key in keys:
        name = key.GetName()
        if(not name.startswith("Iteration_Study_")):
            continue
        q2y = parse_q2y(name)
        groups.setdefault(q2y, {})[name] = tfile.Get(name)
    return groups


def pick(group, stem):
    for name, hist in group.items():
        if(name.startswith(stem)):
            return hist
    return None


def pick_smaller_is_better(by_k, kmin):
    k_ext = first_local_min(by_k, kmin)
    if(k_ext is not None):
        return k_ext
    d1 = first_diff(by_k)
    d2 = second_diff(d1)
    k_flat = flattening_from_slope(d1, d2, kmin)
    if(k_flat is not None):
        return k_flat
    k_d1 = local_min_abs_d1(d1, kmin)
    if(k_d1 is not None):
        return k_d1
    return None


def mean_residual_relative_range(mean_by_k):
    abs_vals = [abs(v) for v in mean_by_k.values()]
    if(not abs_vals):
        return 0.0
    mx = max(abs_vals)
    if(mx <= 0):
        return 0.0
    return (mx - min(abs_vals)) / mx


def select_mean_residual_k(mean_by_k, kmin):
    # Primary selector: |mean residual| first local min after the initial transient (k=2 is valid).
    # A <1% swing across the whole scan is not a meaningful minimum (pathological offset).
    abs_mean = {k: abs(v) for k, v in mean_by_k.items()}
    if(not abs_mean):
        return None, True, True
    if(mean_residual_relative_range(mean_by_k) < 0.01):
        return None, True, True
    k_loc = first_local_min(abs_mean, kmin)
    if(k_loc is not None):
        return k_loc, False, False
    k_rise = argmin_before_rise(abs_mean, kmin)
    if(k_rise is not None):
        return k_rise, False, False
    d1 = first_diff(abs_mean)
    d2 = second_diff(d1)
    k_flat = flattening_from_slope(d1, d2, kmin)
    if(k_flat is not None):
        return k_flat, False, False
    k_rel = fallback_rel_change(abs_mean, kmin, 0.05, 1e-12)
    if(k_rel is not None):
        return k_rel, False, False
    return None, True, True


def recommend(group, args):
    # Mean-residual-first selection as of 9/16/2026 (no longer the median of chi2 / |mean| / RMS).
    chi2_h = pick(group, "Iteration_Study_Chi2")
    mean_h = pick(group, "Iteration_Study_MeanResiduals")
    rms_h = pick(group, "Iteration_Study_RMSError")
    rmsr_h = pick(group, "Iteration_Study_RMSResiduals")
    chi2_by_k = extract_iteration_series(chi2_h, args.clip_max)
    mean_by_k = extract_iteration_series(mean_h, args.clip_max)
    rms_by_k = extract_iteration_series(rms_h, args.clip_max)
    if(rmsr_h is not None):
        extract_iteration_series(rmsr_h, args.clip_max)
    change = chi2_change(chi2_by_k, args.epsilon)
    d1_chi2 = first_diff(chi2_by_k)
    k_chi2min = first_local_min(chi2_by_k, args.clip_min)
    k_flat = flattening_from_slope(d1_chi2, second_diff(d1_chi2), args.clip_min)
    k_chi2 = k_chi2min if(k_chi2min is not None) else k_flat
    if(k_chi2 is None):
        k_chi2 = fallback_rel_change(chi2_by_k, args.clip_min, args.plateau, args.epsilon)
    k_mean, need_fallback, pathological = select_mean_residual_k(mean_by_k, args.clip_min)
    k_rms = pick_smaller_is_better(rms_by_k, args.clip_min)
    if(k_rms is None):
        k_rms = argmin_before_rise(rms_by_k, args.clip_min)
    rec = k_mean
    fallback_used = False
    if(need_fallback or (rec is None)):
        fallback_used = True
        rec = k_chi2 if(k_chi2 is not None) else k_rms
    if(rec is not None):
        rec = max(args.clip_min, min(args.clip_max, rec))
    return {
        "k_chi2_change": k_flat,
        "k_chi2_diag": k_chi2min,
        "k_chi2_slot": k_chi2,
        "k_mean": k_mean,
        "k_rms": k_rms,
        "recommend": rec,
        "flagged": pathological or fallback_used,
        "fallback_used": fallback_used,
        "pathological": pathological,
        "chi2_by_k": chi2_by_k,
        "change": change,
        "mean": mean_by_k,
        "rms": rms_by_k,
    }


def draw_group(q2y, rec, out_dir, args):
    import ROOT
    canv = ROOT.TCanvas(f"c_iter_{q2y}", f"Iteration study Q2-y {q2y}", 1200, 900)
    canv.Divide(2, 2)
    def plot_pad(ipad, by_k, title, ytitle, mark_k):
        canv.cd(ipad)
        if(not by_k):
            return None
        ks = sorted(by_k)
        h = ROOT.TH1D(f"h_{q2y}_{ipad}", f"Q^{{2}}-y bin {q2y}: {title};Bayesian iteration;{ytitle}", max(ks) - min(ks) + 1, min(ks) - 0.5, max(ks) + 0.5)
        h.SetDirectory(0)
        for k, v in by_k.items():
            h.SetBinContent(h.FindBin(k), v)
        h.SetLineWidth(2)
        h.Draw("hist")
        if(mark_k is not None):
            line = ROOT.TLine(mark_k, h.GetMinimum(), mark_k, h.GetMaximum())
            line.SetLineColor(ROOT.kRed)
            line.SetLineStyle(2)
            line.Draw()
            h._line = line
        return h
    hists = []
    hists.append(plot_pad(1, rec["chi2_by_k"], "#chi^{2} diagnostic", "#chi^{2} diagnostic", rec["recommend"]))
    hists.append(plot_pad(2, rec["change"], "#Delta#chi^{2}", "#Delta#chi^{2}", rec["recommend"]))
    hists.append(plot_pad(3, rec["mean"], "mean residuals", "mean residuals", rec["recommend"]))
    hists.append(plot_pad(4, rec["rms"], "RMS error", "RMS error", rec["recommend"]))
    os.makedirs(out_dir, exist_ok=True)
    pdf = os.path.join(out_dir, f"iteration_study_Q2y_{q2y}.pdf")
    canv.SaveAs(pdf)
    return pdf, hists, canv


def main():
    args = parse_args()
    silence_root()
    import ROOT
    if(not os.path.isfile(args.root_file)):
        print(f"ERROR: missing {args.root_file}", file=sys.stderr)
        return 2
    tfile = ROOT.TFile.Open(args.root_file, "READ")
    groups = group_hists(tfile)
    if(not groups):
        print("No Iteration_Study_* histograms found.")
        return 1
    os.makedirs(args.out, exist_ok=True)
    summary_path = os.path.join(args.out, "iteration_recommendations.txt")
    pdfs = []
    keep = []
    with open(summary_path, "w") as summary:
        summary.write("Q2y\trecommend\tchi2_change\tchi2_diag\tmean_resid\trms_error\tflagged\tfallback\tpathological\n")
        print("Q2-y  recommend  chi2-flat  chi2-min  |mean resid|  RMS error  flag  fallback  pathol")
        for q2y in sorted(groups, key=lambda x: (x != "all", int(x) if(str(x).lstrip('-').isdigit()) else 9999)):
            rec = recommend(groups[q2y], args)
            flag = "YES" if(rec["flagged"]) else "no"
            fb = "YES" if(rec["fallback_used"]) else "no"
            pathol = "YES" if(rec["pathological"]) else "no"
            print(f"{q2y:>5s}  {str(rec['recommend']):>9s}  {str(rec['k_chi2_change']):>9s}  {str(rec['k_chi2_diag']):>7s}  {str(rec['k_mean']):>12s}  {str(rec['k_rms']):>9s}  {flag:>4s}  {fb:>8s}  {pathol}")
            summary.write(f"{q2y}\t{rec['recommend']}\t{rec['k_chi2_change']}\t{rec['k_chi2_diag']}\t{rec['k_mean']}\t{rec['k_rms']}\t{flag}\t{fb}\t{pathol}\n")
            pdf, hists, canv = draw_group(q2y, rec, args.out, args)
            pdfs.append(pdf)
            keep.append((hists, canv))
    merged = os.path.join(args.out, "iteration_study_all.pdf")
    if(pdfs):
        cmd = " ".join(["pdfunite"] + [f"'{p}'" for p in pdfs] + [f"'{merged}'"])
        rc = os.system(f"command -v pdfunite >/dev/null && {cmd}")
        if(rc != 0):
            merged = pdfs[0]
    print(f"Wrote {summary_path}")
    print(f"PDFs: {len(pdfs)} per-bin files under {args.out}")
    tfile.Close()
    return 0


if(__name__ == "__main__"):
    sys.exit(main())
