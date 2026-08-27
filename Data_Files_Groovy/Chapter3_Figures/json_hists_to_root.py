#!/usr/bin/env python3
"""Convert a Chapter 3 histogram JSON dump into a ROOT file of TH1/TH2 objects.

The Groovy histogram job writes one JSON per HIPO file. This converter builds
like-named ROOT histograms so that ROOT ``hadd`` can sum them after all jobs
finish.

Usage:
    python json_hists_to_root.py input.json output.root
"""
from __future__ import print_function

import json
import os
import sys

import ROOT

ROOT.gROOT.SetBatch(True)


def make_th1(spec):
    hist = ROOT.TH1D(str(spec["name"]), str(spec.get("title", spec["name"])), int(spec["nbins"]), float(spec["xmin"]), float(spec["xmax"]))
    hist.Sumw2()
    contents = spec.get("contents", [])
    errors = spec.get("errors", [])
    for ibin, value in enumerate(contents):
        hist.SetBinContent(ibin, float(value))
        if ibin < len(errors):
            hist.SetBinError(ibin, float(errors[ibin]))
    hist.SetEntries(float(spec.get("entries", 0.0)))
    return hist


def make_th2(spec):
    hist = ROOT.TH2D(
        str(spec["name"]),
        str(spec.get("title", spec["name"])),
        int(spec["nbinsx"]),
        float(spec["xmin"]),
        float(spec["xmax"]),
        int(spec["nbinsy"]),
        float(spec["ymin"]),
        float(spec["ymax"]),
    )
    hist.Sumw2()
    nx = int(spec["nbinsx"])
    ny = int(spec["nbinsy"])
    contents = spec.get("contents", [])
    errors = spec.get("errors", [])
    # contents are stored including overflow bins: (ny+2) * (nx+2), ix fastest
    for iy in range(ny + 2):
        for ix in range(nx + 2):
            idx = iy * (nx + 2) + ix
            if idx >= len(contents):
                continue
            hist.SetBinContent(ix, iy, float(contents[idx]))
            if idx < len(errors):
                hist.SetBinError(ix, iy, float(errors[idx]))
    hist.SetEntries(float(spec.get("entries", 0.0)))
    return hist


def convert(json_path, root_path):
    with open(json_path, "r") as handle:
        payload = json.load(handle)
    hist_list = payload.get("histograms", [])
    if not hist_list:
        raise SystemExit("No histograms in %s" % json_path)

    out = ROOT.TFile.Open(root_path, "RECREATE")
    if not out or out.IsZombie():
        raise SystemExit("Cannot create %s" % root_path)
    written = []
    for spec in hist_list:
        kind = str(spec.get("type", "th1")).lower()
        if kind in ("th2", "h2", "2d"):
            hist = make_th2(spec)
        else:
            hist = make_th1(spec)
        hist.SetDirectory(out)
        hist.Write()
        written.append(hist.GetName())
    out.Close()
    print("Wrote %d histograms to %s" % (len(written), root_path))
    return 0


def main(argv):
    if len(argv) != 3:
        print(__doc__)
        return 2
    json_path, root_path = argv[1], argv[2]
    if not os.path.isfile(json_path):
        raise SystemExit("Missing JSON: %s" % json_path)
    parent = os.path.dirname(os.path.abspath(root_path))
    if parent and not os.path.isdir(parent):
        os.makedirs(parent)
    return convert(json_path, root_path)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
