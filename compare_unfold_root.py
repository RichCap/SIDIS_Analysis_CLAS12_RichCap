#!/usr/bin/env python3
"""Compare two unfolding ROOT files for histogram equivalence with float tolerances."""

import argparse
import math
import os
import sys

_BOOT = os.path.abspath(os.path.dirname(__file__))
if(_BOOT not in sys.path):
    sys.path.insert(0, _BOOT)


def parse_args():
    p = argparse.ArgumentParser(description="Compare TH1/TH2/TProfile objects in two ROOT files.")
    p.add_argument('file_a', help="Reference ROOT file (e.g. Python).")
    p.add_argument('file_b', help="Comparison ROOT file (e.g. C++).")
    p.add_argument('-la', '--label-a', default="A", help="Label for file A.")
    p.add_argument('-lb', '--label-b', default="B", help="Label for file B.")
    p.add_argument('-ctol', '--content-rel', type=float, default=1e-6, help="Relative content tolerance.")
    p.add_argument('-cabs', '--content-abs', type=float, default=1e-8, help="Absolute content tolerance.")
    p.add_argument('-etol', '--error-rel', type=float, default=1e-4, help="Relative error tolerance.")
    p.add_argument('-eabs', '--error-abs', type=float, default=1e-8, help="Absolute error tolerance.")
    p.add_argument('-eps', '--epsilon', type=float, default=1e-12, help="Floor for relative denominators.")
    p.add_argument('-eo', '--errors-optional', action='store_true',
                   help="Do not fail the process on error mismatches (still report them).")
    p.add_argument('-p', '--pattern', default="", help="Optional substring filter on object names.")
    return p.parse_args()


def silence_root():
    import ROOT
    ROOT.gROOT.SetBatch(True)
    ROOT.gErrorIgnoreLevel = ROOT.kError


def hist_kind(obj):
    if(obj.InheritsFrom("TProfile")): return "TProfile"
    if(obj.InheritsFrom("TH2")): return "TH2"
    if(obj.InheritsFrom("TH1")): return "TH1"
    return type(obj).__name__


def axis_edges(axis):
    n = axis.GetNbins()
    return [axis.GetBinLowEdge(i) for i in range(1, n + 2)]


def collect_names(tfile, pattern=""):
    names = []
    keys = tfile.GetListOfKeys()
    if(keys is None):
        return names
    for key in keys:
        name = key.GetName()
        if(pattern and (pattern not in name)):
            continue
        names.append(name)
    return names


def compare_hist(a, b, args):
    report = {
        "ok_content": True,
        "ok_errors": True,
        "ok_axes": True,
        "n": 0,
        "max_abs_c": 0.0,
        "max_rel_c": 0.0,
        "max_abs_e": 0.0,
        "max_rel_e": 0.0,
        "rms_rel_c": 0.0,
        "notes": [],
    }
    if(hist_kind(a) != hist_kind(b)):
        report["ok_axes"] = False
        report["notes"].append(f"type mismatch {hist_kind(a)} vs {hist_kind(b)}")
        return report
    if(a.GetDimension() != b.GetDimension()):
        report["ok_axes"] = False
        report["notes"].append(f"dimension mismatch {a.GetDimension()} vs {b.GetDimension()}")
        return report
    axes = [("x", a.GetXaxis(), b.GetXaxis())]
    if(a.GetDimension() >= 2):
        axes.append(("y", a.GetYaxis(), b.GetYaxis()))
    for label, axa, axb in axes:
        if(axa.GetNbins() != axb.GetNbins()):
            report["ok_axes"] = False
            report["notes"].append(f"{label} Nbins {axa.GetNbins()} vs {axb.GetNbins()}")
        ea, eb = axis_edges(axa), axis_edges(axb)
        if(len(ea) == len(eb)):
            max_edge = max((abs(x - y) for x, y in zip(ea, eb)), default=0.0)
            if(max_edge > 1e-9):
                report["ok_axes"] = False
                report["notes"].append(f"{label} edge max-abs {max_edge}")
    ncells = a.GetNcells()
    if(ncells != b.GetNcells()):
        report["ok_axes"] = False
        report["notes"].append(f"Ncells {ncells} vs {b.GetNcells()}")
        return report
    rels = []
    for i in range(ncells):
        ca, cb = a.GetBinContent(i), b.GetBinContent(i)
        ea, eb = a.GetBinError(i), b.GetBinError(i)
        abs_c = abs(ca - cb)
        den_c = max(abs(ca), args.epsilon)
        rel_c = abs_c / den_c
        abs_e = abs(ea - eb)
        den_e = max(abs(ea), args.epsilon)
        rel_e = abs_e / den_e
        report["max_abs_c"] = max(report["max_abs_c"], abs_c)
        report["max_rel_c"] = max(report["max_rel_c"], rel_c)
        report["max_abs_e"] = max(report["max_abs_e"], abs_e)
        report["max_rel_e"] = max(report["max_rel_e"], rel_e)
        if(abs(ca) > args.epsilon):
            rels.append(rel_c * rel_c)
        if((abs_c > args.content_abs) and (rel_c > args.content_rel)):
            report["ok_content"] = False
        if((abs_e > args.error_abs) and (rel_e > args.error_rel)):
            report["ok_errors"] = False
    report["n"] = ncells
    report["rms_rel_c"] = math.sqrt(sum(rels) / len(rels)) if(rels) else 0.0
    return report


def main():
    args = parse_args()
    silence_root()
    import ROOT
    if(not os.path.isfile(args.file_a)):
        print(f"ERROR: missing {args.file_a}", file=sys.stderr)
        return 2
    if(not os.path.isfile(args.file_b)):
        print(f"ERROR: missing {args.file_b}", file=sys.stderr)
        return 2
    fa = ROOT.TFile.Open(args.file_a, "READ")
    fb = ROOT.TFile.Open(args.file_b, "READ")
    names_a = set(collect_names(fa, args.pattern))
    names_b = set(collect_names(fb, args.pattern))
    only_a = sorted(names_a - names_b)
    only_b = sorted(names_b - names_a)
    both = sorted(names_a & names_b)
    print(f"{args.label_a}: {args.file_a} ({len(names_a)} keys)")
    print(f"{args.label_b}: {args.file_b} ({len(names_b)} keys)")
    print(f"shared={len(both)} only_{args.label_a}={len(only_a)} only_{args.label_b}={len(only_b)}")
    for name in only_a[:50]:
        print(f"  missing in {args.label_b}: {name}")
    for name in only_b[:50]:
        print(f"  extra in {args.label_b}: {name}")
    n_fail_c = 0
    n_fail_e = 0
    n_fail_ax = 0
    n_cmp = 0
    for name in both:
        oa = fa.Get(name)
        ob = fb.Get(name)
        if((oa is None) or (ob is None)):
            continue
        if((oa is None) or (ob is None)):
            continue
        if((not hasattr(oa, "InheritsFrom")) or (not hasattr(ob, "InheritsFrom"))):
            continue
        try:
            is_hist = bool(oa.InheritsFrom("TH1") or oa.InheritsFrom("TProfile"))
        except Exception:
            continue
        if(not is_hist):
            continue
        n_cmp += 1
        rep = compare_hist(oa, ob, args)
        status = "OK"
        if(not rep["ok_axes"]):
            status = "AXIS"
            n_fail_ax += 1
        elif(not rep["ok_content"]):
            status = "CONTENT"
            n_fail_c += 1
        elif(not rep["ok_errors"]):
            status = "ERRORS"
            n_fail_e += 1
        if(status != "OK"):
            print(f"{status:8s} {name}")
            print(f"         max|dc|={rep['max_abs_c']:.3e} max|dc|/ref={rep['max_rel_c']:.3e} rms_rel={rep['rms_rel_c']:.3e}")
            print(f"         max|de|={rep['max_abs_e']:.3e} max|de|/ref={rep['max_rel_e']:.3e} ncells={rep['n']}")
            for note in rep["notes"]:
                print(f"         {note}")
    print(f"compared_hists={n_cmp} content_fail={n_fail_c} error_fail={n_fail_e} axis_fail={n_fail_ax}")
    fa.Close()
    fb.Close()
    failed = (n_fail_c > 0) or (n_fail_ax > 0) or (len(only_a) > 0) or (len(only_b) > 0)
    if((n_fail_e > 0) and (not args.errors_optional)):
        failed = True
    return 1 if(failed) else 0


if(__name__ == "__main__"):
    sys.exit(main())
