#!/usr/bin/env python3
# Plot RooUnfoldParms iteration-study diagnostics and recommend k per Q2-y bin.

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
    p.add_argument('root_file',
                   help="ROOT file containing Iteration_Study_* histograms.")
    p.add_argument('-o', '--out',
                   default="Unfold_Iteration_Study_3D/",
                   help="Output directory for PDFs.")
    p.add_argument('-kmin', '--clip_min',
                   type=int,
                   # default=3, # Changed default to 1 on 9/16/2026 (iteration 2 is valid)
                   default=1,
                   help="Minimum recommended k (1 allows iteration 2).")
    p.add_argument('-kmax', '--clip_max',
                   type=int,
                   default=25,
                   help="Maximum recommended k.")
    p.add_argument('-plat', '--plateau',
                   type=float,
                   default=0.05,
                   help="Retained flag. Plateau selection uses --tau_trend, --tau_flat, and --tau_confirm.")
    p.add_argument('-spread', '--flag_spread',
                   type=int,
                   default=4,
                   help="Report when resolved diagnostic candidates differ by this many iterations or more.")
    p.add_argument('-tt', '--tau_trend',
                   type=float,
                   default=0.03,
                   help="Normalized step that still counts as a meaningful approach to a plateau.")
    p.add_argument('-tf', '--tau_flat',
                   type=float,
                   # default=0.02,  # Changed to 0.03 on 9/22/2026. The 0.025 chi2 curves step from about 0.036 to 0.022, so a 0.02 flat band is not adjacent to a 0.03 trend.
                   default=0.03,
                   help="Normalized step that counts as flat after that approach.")
    p.add_argument('-tc', '--tau_confirm',
                   type=float,
                   # default=0.02,  # Changed to 0.03 on 9/22/2026, same calibration as --tau_flat.
                   default=0.03,
                   help="Following step must also be this flat when it exists. Does not move the chosen iteration.")
    p.add_argument('-eps', '--epsilon',
                   type=float,
                   default=1e-12)
    return p.parse_args()


def silence_root():
    import ROOT
    ROOT.gROOT.SetBatch(True)
    ROOT.gErrorIgnoreLevel = ROOT.kError


def extract_iteration_series(hist, kmax=None):
    # Extract one value per integer iteration from a TProfile or TH1. Print (k, value) pairs.
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


def normalized_steps(by_k, eps):
    # r_k = (y_{k+1} - y_k) / max(|y_k|, |y_{k+1}|, eps) for consecutive iterations.
    steps = {}
    keys = sorted(by_k)
    for i in range(len(keys) - 1):
        k0 = keys[i]
        k1 = keys[i + 1]
        if(k1 != (k0 + 1)):
            continue
        y0 = by_k[k0]
        y1 = by_k[k1]
        den = max(abs(y0), abs(y1), eps)
        steps[k0] = (y1 - y0) / den
    return steps


def strictly_lower(y_k, y_other, eps):
    den = max(abs(y_k), abs(y_other), eps)
    return ((y_other - y_k) / den) > eps


def in_clip(k, args):
    if(k < args.clip_min):
        return False
    if(k > args.clip_max):
        return False
    return True


def earliest_local_minimum(by_k, args):
    keys = sorted(by_k)
    for i in range(1, len(keys) - 1):
        k_prev = keys[i - 1]
        k = keys[i]
        k_next = keys[i + 1]
        if((k != (k_prev + 1)) or (k_next != (k + 1))):
            continue
        if(not in_clip(k, args)):
            continue
        y_prev = by_k[k_prev]
        y_k = by_k[k]
        y_next = by_k[k_next]
        if(strictly_lower(y_k, y_prev, args.epsilon) and strictly_lower(y_k, y_next, args.epsilon)):
            reason = f"y({k})={y_k:.6g} < y({k_prev})={y_prev:.6g} and < y({k_next})={y_next:.6g}"
            return k, reason
    return None, ""


def earliest_plateau(by_k, args):
    steps = normalized_steps(by_k, args.epsilon)
    ks = sorted(k for k in steps if(((k - 1) in steps) and in_clip(k, args)))
    for k in ks:
        r_in = steps[k - 1]
        r_out = steps[k]
        if((abs(r_in) <= args.tau_trend) or (abs(r_out) > args.tau_flat)):
            continue
        if((k + 1) in steps):
            r_conf = steps[k + 1]
            if(abs(r_conf) > args.tau_confirm):
                continue
            reason = f"|r({k - 1})|={abs(r_in):.6g}>tau_trend, |r({k})|={abs(r_out):.6g}<=tau_flat, |r({k + 1})|={abs(r_conf):.6g}<=tau_confirm"
        else:
            reason = f"|r({k - 1})|={abs(r_in):.6g}>tau_trend, |r({k})|={abs(r_out):.6g}<=tau_flat, no further step"
        return k, reason
    return None, ""


def classify_series(by_k, args):
    steps = normalized_steps(by_k, args.epsilon)
    if(not by_k):
        return {"klass": "unresolved", "k": None, "reason": "empty series", "steps": steps}
    k_min, reason_min = earliest_local_minimum(by_k, args)
    if(k_min is not None):
        return {"klass": "min", "k": k_min, "reason": reason_min, "steps": steps}
    k_plat, reason_plat = earliest_plateau(by_k, args)
    if(k_plat is not None):
        return {"klass": "plateau", "k": k_plat, "reason": reason_plat, "steps": steps}
    return {"klass": "unresolved", "k": None, "reason": "no local minimum and no plateau onset", "steps": steps}


def empty_class():
    return {"klass": "unresolved", "k": None, "reason": "histogram missing", "steps": {}}


def candidate_spread(classes):
    vals = [item["k"] for item in classes if(item["k"] is not None)]
    if(len(vals) < 2):
        return None
    return max(vals) - min(vals)


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


def recommend(group, args):
    # Each diagnostic is classified on its own. No combined k is chosen here.
    chi2_h = pick(group, "Iteration_Study_Chi2")
    mean_h = pick(group, "Iteration_Study_MeanResiduals")
    rms_h = pick(group, "Iteration_Study_RMSError")
    rmsr_h = pick(group, "Iteration_Study_RMSResiduals")
    chi2_by_k = extract_iteration_series(chi2_h, args.clip_max)
    mean_signed = extract_iteration_series(mean_h, args.clip_max)
    rms_by_k = extract_iteration_series(rms_h, args.clip_max)
    rmsr_by_k = extract_iteration_series(rmsr_h, args.clip_max) if(rmsr_h is not None) else {}
    mean_abs = {k: abs(v) for k, v in mean_signed.items()}
    classes = {
        "chi2": classify_series(chi2_by_k, args),
        "mean_abs": classify_series(mean_abs, args),
        "rms_error": classify_series(rms_by_k, args),
        "rms_resid": classify_series(rmsr_by_k, args) if(rmsr_by_k) else empty_class(),
    }
    spread = candidate_spread([classes["chi2"], classes["mean_abs"], classes["rms_error"], classes["rms_resid"]])
    spread_flag = "no"
    if((spread is not None) and (spread >= args.flag_spread)):
        spread_flag = "YES"
    return {
        "classes": classes,
        "spread": spread,
        "spread_flag": spread_flag,
        "chi2_by_k": chi2_by_k,
        "chi2_steps": classes["chi2"]["steps"],
        "mean_abs": mean_abs,
        "rms_by_k": rms_by_k,
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
        h.SetStats(0)
        # Absolute mean residual sits on a large offset. A zero-based axis hides the iteration dependence.
        if((ipad == 3) and by_k):
            y_lo = min(by_k.values())
            y_hi = max(by_k.values())
            span = y_hi - y_lo
            if(span <= 0.0):
                span = abs(y_lo) * 0.01 if(y_lo != 0.0) else 1.0
            pad = 0.12 * span
            h.SetMinimum(y_lo - pad)
            h.SetMaximum(y_hi + pad)
        h.Draw("hist")
        if(mark_k is not None):
            line = ROOT.TLine(mark_k, h.GetMinimum(), mark_k, h.GetMaximum())
            line.SetLineColor(ROOT.kRed)
            line.SetLineStyle(2)
            line.Draw()
            h._line = line
        return h
    classes = rec["classes"]
    hists = []
    hists.append(plot_pad(1, rec["chi2_by_k"], "#chi^{2} diagnostic", "#chi^{2} diagnostic", classes["chi2"]["k"]))
    hists.append(plot_pad(2, rec["chi2_steps"], "normalized #chi^{2} step r_{k}", "r_{k}", classes["chi2"]["k"]))
    hists.append(plot_pad(3, rec["mean_abs"], "absolute mean residual", "|mean residual|", classes["mean_abs"]["k"]))
    hists.append(plot_pad(4, rec["rms_by_k"], "mean bin error", "mean bin error", classes["rms_error"]["k"]))
    os.makedirs(out_dir, exist_ok=True)
    pdf = os.path.join(out_dir, f"iteration_study_Q2y_{q2y}.pdf")
    canv.SaveAs(pdf)
    return pdf, hists, canv


def format_class(item):
    k_txt = "" if(item["k"] is None) else str(item["k"])
    return item["klass"], k_txt, item["reason"]


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
    header = "\t".join([
        "Q2y", "spread_flag", "spread",
        "chi2_class", "chi2_k", "chi2_reason",
        "mean_abs_class", "mean_abs_k", "mean_abs_reason",
        "rms_error_class", "rms_error_k", "rms_error_reason",
        "rms_resid_class", "rms_resid_k", "rms_resid_reason",
    ])
    with open(summary_path, "w") as summary:
        summary.write(header + "\n")
        print("Q2-y  spread  chi2  |mean|  mean-error  rms-resid")
        order = ["chi2", "mean_abs", "rms_error", "rms_resid"]
        for q2y in sorted(groups, key=lambda x: (x != "all", int(x) if(str(x).lstrip('-').isdigit()) else 9999)):
            rec = recommend(groups[q2y], args)
            cells = [q2y, rec["spread_flag"], "" if(rec["spread"] is None) else str(rec["spread"])]
            shown = []
            for name in order:
                klass, k_txt, reason = format_class(rec["classes"][name])
                cells.extend([klass, k_txt, reason])
                shown.append(f"{klass}:{k_txt or '-'}")
            print(f"{q2y:>5s}  {rec['spread_flag']:>6s}  " + "  ".join(shown))
            summary.write("\t".join(cells) + "\n")
            pdf, hists, canv = draw_group(q2y, rec, args.out, args)
            pdfs.append(pdf)
            keep.append((hists, canv))
    merged = os.path.join(args.out, "iteration_study_all.pdf")
    if(pdfs):
        cmd = " ".join(["pdfunite"] + [f"'{p}'" for p in pdfs] + [f"'{merged}'"])
        rc = os.system(f"command -v pdfunite >/dev/null && {cmd}")
        if(rc != 0):
            import fitz
            merged_doc = fitz.open()
            for pdf in pdfs:
                src = fitz.open(pdf)
                merged_doc.insert_pdf(src)
                src.close()
            merged_doc.save(merged)
            merged_doc.close()
    print(f"Wrote {summary_path}")
    print(f"PDFs: {len(pdfs)} per-bin files under {args.out}")
    tfile.Close()
    return 0


if(__name__ == "__main__"):
    sys.exit(main())


