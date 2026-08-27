#!/usr/bin/env python3
"""Pion DC polygon occupancy and data/MC comparison plots.

Uses the live vertices in Pion_Test_Fiducial_Cuts_Defs.polygon_pip_secs
(layers 6/18/36, sectors 1-6). Requires experimental and reconstructed-MC
DataFrame files with pip_x_DC_{6,18,36} and pip_y_DC_*.

Do not run this on a machine that does not contain the reconstructed-MC
DataFrames.

Example (from Histo_Files_ROOT/DataFrames on the farm):

    python Chapter3_Pion_DC_Polygon_Plots.py \\
      --data '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/REAL_Data/DataFrame_SIDIS_epip_Data_REC_Pass_2_Final_Analysis_Iterations_I0_*.root' \\
      --mc   '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/Matching_REC_MC/DataFrame_SIDIS_epip_Matching_REC_Pass_2_Final_Analysis_Iterations_I0_*.root' \\
      --out  /path/to/thesis/Experiment/Data_Collection_Images/Analysis_Cut_Images
"""
from __future__ import print_function

import argparse
import glob
import os
import sys

import ROOT

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

LAYERS = [6, 18, 36]
XYRANGE = {6: (-200, 200), 18: (-280, 280), 36: (-360, 360)}


def expand(spec):
    out = []
    for piece in spec.split(","):
        piece = piece.strip()
        if not piece:
            continue
        matched = sorted(glob.glob(piece))
        if matched:
            out.extend(matched)
        elif os.path.isfile(piece):
            out.append(piece)
    seen, uniq = set(), []
    for path in out:
        if path not in seen:
            seen.add(path)
            uniq.append(path)
    return uniq


def load_polygons(analysis_root):
    sys.path.insert(0, analysis_root)
    import Pion_Test_Fiducial_Cuts_Defs as pdefs
    return pdefs.polygon_pip_secs


def open_rdf(files, tree_name, max_entries):
    chain = ROOT.TChain(tree_name)
    for path in files:
        chain.Add(path, 0)
    rdf = ROOT.RDataFrame(chain)
    if max_entries is not None and int(max_entries) > 0:
        rdf = rdf.Range(int(max_entries))
    return rdf, set(str(c) for c in rdf.GetColumnNames())


def graph_xy(points):
    gr = ROOT.TGraph(len(points))
    for i, (x, y) in enumerate(points):
        gr.SetPoint(i, float(x), float(y))
    gr.SetLineColor(ROOT.kRed)
    gr.SetLineWidth(2)
    return gr


def overlay_polygons(polygons, layer, keep):
    for sec in range(1, 7):
        xy = polygons["Sector_%d" % sec]["Layer_%d" % layer]
        gr = graph_xy(xy)
        gr.Draw("L same")
        keep.append(gr)


def fill_occupancy(rdf, layer, name, title):
    xmin, xmax = XYRANGE[layer]
    return rdf.Histo2D(
        (name, title, 120, xmin, xmax, 120, xmin, xmax),
        "pip_x_DC_%d" % layer,
        "pip_y_DC_%d" % layer,
    )


def percent_diff(hdata, hmc, name):
    hist = hdata.Clone(name)
    hist.Reset()
    nx, ny = hist.GetNbinsX(), hist.GetNbinsY()
    for ix in range(1, nx + 1):
        for iy in range(1, ny + 1):
            d = hdata.GetBinContent(ix, iy)
            m = hmc.GetBinContent(ix, iy)
            if d <= 0:
                continue
            diff = 100.0 * abs(d - m) / d
            if diff < 5.0:
                diff = 0.0
            hist.SetBinContent(ix, iy, diff)
    hist.SetTitle(hdata.GetTitle())
    return hist


def draw_layer_row(can, start_pad, hist_by_layer, polygons, keep, ztitle=None):
    for col, layer in enumerate(LAYERS):
        pad = can.cd(start_pad + col)
        pad.SetRightMargin(0.14)
        hist = hist_by_layer[layer]
        hist.Draw("colz")
        if ztitle:
            hist.GetZaxis().SetTitle(ztitle)
        overlay_polygons(polygons, layer, keep)
        keep.append(hist)


def save(can, outdir, name):
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, name)
    can.SaveAs(path)
    print("Wrote", path)
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--data", required=True)
    parser.add_argument("--mc", required=True)
    parser.add_argument("--tree", default="h22")
    parser.add_argument("--out", default=".")
    parser.add_argument("--max-entries", type=int, default=-1)
    parser.add_argument(
        "--analysis-root",
        default=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")),
    )
    args = parser.parse_args()

    data_files = expand(args.data)
    mc_files = expand(args.mc)
    if not data_files:
        raise SystemExit("No --data files matched")
    if not mc_files:
        raise SystemExit("No --mc files matched")

    polygons = load_polygons(args.analysis_root)
    rdf, cols = open_rdf(data_files, args.tree, args.max_entries)
    mdf, mcols = open_rdf(mc_files, args.tree, args.max_entries)
    needed = []
    for layer in LAYERS:
        needed.extend(["pip_x_DC_%d" % layer, "pip_y_DC_%d" % layer])
    missing = [c for c in needed if c not in cols or c not in mcols]
    if missing:
        raise SystemExit("Missing columns: %s" % missing)

    h_data, h_mc, h_diff = {}, {}, {}
    for layer in LAYERS:
        h_data[layer] = fill_occupancy(rdf, layer, "hdata%d" % layer, "Data, DC layer %d;x [cm];y [cm]" % layer)
        h_mc[layer] = fill_occupancy(mdf, layer, "hmc%d" % layer, "REC MC, DC layer %d;x [cm];y [cm]" % layer)

    # Normalize each occupancy to unit integral before the percent-difference map.
    for layer in LAYERS:
        hd = h_data[layer].GetPtr() if hasattr(h_data[layer], "GetPtr") else h_data[layer]
        hm = h_mc[layer].GetPtr() if hasattr(h_mc[layer], "GetPtr") else h_mc[layer]
        if hd.Integral() > 0:
            hd.Scale(1.0 / hd.Integral())
        if hm.Integral() > 0:
            hm.Scale(1.0 / hm.Integral())
        h_data[layer] = hd
        h_mc[layer] = hm
        h_diff[layer] = percent_diff(hd, hm, "hdiff%d" % layer)
        h_diff[layer].SetTitle("Data/MC percent difference, DC layer %d;x [cm];y [cm]" % layer)

    keep = []
    can_data = ROOT.TCanvas("c_pip_data", "c_pip_data", 1500, 500)
    can_data.Divide(3, 1)
    draw_layer_row(can_data, 1, h_data, polygons, keep)
    save(can_data, args.out, "pip_DC_polygons_data.pdf")

    can_mc = ROOT.TCanvas("c_pip_mc", "c_pip_mc", 1500, 500)
    can_mc.Divide(3, 1)
    draw_layer_row(can_mc, 1, h_mc, polygons, keep)
    save(can_mc, args.out, "pip_DC_polygons_mc.pdf")

    can_diff = ROOT.TCanvas("c_pip_diff", "c_pip_diff", 1500, 500)
    can_diff.Divide(3, 1)
    draw_layer_row(can_diff, 1, h_diff, polygons, keep, ztitle="|data-MC|/data [%]")
    save(can_diff, args.out, "pip_DC_polygons.pdf")

    print("Polygon plots written to", args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
