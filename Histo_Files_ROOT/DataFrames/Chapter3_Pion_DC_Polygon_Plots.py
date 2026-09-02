#!/usr/bin/env python3
"""Pion DC polygon occupancy and data/MC comparison plots for Chapter 3.

Produces three 1x3 pre-cut figures (layers 6, 18, 36 left to right):

  pip_DC_polygons_Data.pdf         experimental occupancy
  pip_DC_polygons_MC.pdf           reconstructed-MC occupancy
  pip_DC_polygons_Percent_Diff.pdf normalized Data/REC-MC percent difference

Both Data and REC-MC are filtered with cut_Complete_SIDIS_no_pip_testdc
before histogram filling. The additional pion polygon/test-DC cut is not
applied. Occupancy histograms are normalized to integral 1 before they
are drawn and before the percent-difference histograms are built.

Polygon overlays use Pion_Test_Fiducial_Cuts_Defs.polygon_pip_secs.
Default axis ranges match Fiducial_Cut_TTree_Tests.py All-sector settings
and do not come from polygon extent.

Do not run this on a machine that does not contain the reconstructed-MC
DataFrames. For a local draft on a laptop with only experimental data,
use cd_SIDIS/Chapter3_Thesis_Cut_Plots.py instead.

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
REGION = {6: "R1", 18: "R2", 36: "R3"}
SIDIS_CUT = "cut_Complete_SIDIS_no_pip_testdc"
NBINS = 170
BOOK_LO, BOOK_HI = -425.0, 425.0
DISP_XMIN, DISP_XMAX = -357.0, 357.0
DISP_YMIN, DISP_YMAX = -425.0, 425.0


def region_label(layer):
    return REGION[layer]


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


def ptr(hist):
    return hist.GetPtr() if hasattr(hist, "GetPtr") else hist


def graph_xy(points):
    gr = ROOT.TGraph(len(points))
    for i, (x, y) in enumerate(points):
        gr.SetPoint(i, float(x), float(y))
    gr.SetLineColor(ROOT.kRed)
    gr.SetLineWidth(1)
    return gr


def overlay_polygons(polygons, layer, keep):
    for sec in range(1, 7):
        xy = polygons["Sector_%d" % sec]["Layer_%d" % layer]
        gr = graph_xy(xy)
        gr.Draw("L same")
        keep.append(gr)


def book_occupancy(rdf, layer, name, title):
    return rdf.Histo2D(
        (name, title, NBINS, BOOK_LO, BOOK_HI, NBINS, BOOK_LO, BOOK_HI),
        "pip_x_DC_%d" % layer,
        "pip_y_DC_%d" % layer,
    )


def normalize_occupancy(hist):
    integral = hist.Integral()
    if integral != 0:
        hist.Scale(1.0 / integral)
    return hist


def ratio_of_2d_histos(hdata, hmc, name):
    # Original TTree Ratio_of_2D_Histos after occupancy normalization.
    # Absolute percent difference; no 20% floor (visualization only).
    out = hdata.Clone(name)
    out.Reset()
    nx, ny = out.GetNbinsX(), out.GetNbinsY()
    for ix in range(0, nx + 2):
        for iy in range(0, ny + 2):
            data_val = hdata.GetBinContent(ix, iy)
            mc_val = hmc.GetBinContent(ix, iy)
            if data_val == 0:
                percent_diff = 10000.0 if mc_val != 0 else 0.0
            else:
                percent_diff = 100.0 * abs(data_val - mc_val) / data_val
            out.SetBinContent(ix, iy, percent_diff)
    return out


def populated_half_range(hist, pad=10.0, default_half=400.0, max_half=500.0):
    xmax_pop = 0.0
    ymax_pop = 0.0
    nx, ny = hist.GetNbinsX(), hist.GetNbinsY()
    for ix in range(1, nx + 1):
        for iy in range(1, ny + 1):
            if hist.GetBinContent(ix, iy) <= 0:
                continue
            xmax_pop = max(xmax_pop, abs(hist.GetXaxis().GetBinCenter(ix)))
            ymax_pop = max(ymax_pop, abs(hist.GetYaxis().GetBinCenter(iy)))
    half = max(xmax_pop, ymax_pop) + pad
    if half <= 0:
        half = default_half
    if half > max_half:
        half = max_half
    return half


def occupancy_zoom_range(layer, hist_data, hist_mc=None):
    if layer == 6:
        return -200.0, 200.0, -200.0, 200.0
    half = populated_half_range(hist_data)
    if hist_mc is not None:
        half = max(half, populated_half_range(hist_mc))
    if half < 400.0:
        half = 400.0
    return -half, half, -half, half


def display_range(layer, hist_data, hist_mc, zoom_dc):
    if zoom_dc:
        return occupancy_zoom_range(layer, hist_data, hist_mc)
    return DISP_XMIN, DISP_XMAX, DISP_YMIN, DISP_YMAX


def save(can, outdir, name):
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, name)
    can.SaveAs(path)
    print("Wrote", path)
    return path


def style_polygon_grid(pad):
    ROOT.gStyle.SetGridColor(18)
    ROOT.gStyle.SetGridStyle(3)
    ROOT.gStyle.SetGridWidth(1)
    pad.SetGrid(1, 1)


def adjust_z_palette(hist, pad):
    pad.Update()
    hist.GetZaxis().SetLabelSize(0.032)
    hist.GetZaxis().SetTitleSize(0.035)
    hist.GetZaxis().SetTitleOffset(1.15)
    palette = hist.GetListOfFunctions().FindObject("palette") if hist.GetListOfFunctions() else None
    if palette is None:
        return
    palette.SetX1NDC(0.81)
    palette.SetX2NDC(0.85)
    palette.SetY1NDC(0.12)
    palette.SetY2NDC(0.88)
    if hasattr(palette, "SetLabelSize"):
        palette.SetLabelSize(0.032)
    axis = palette.GetAxis() if hasattr(palette, "GetAxis") else None
    if axis is not None:
        axis.SetLabelSize(0.032)
        axis.SetTitleSize(0.035)
        axis.SetTitleOffset(1.15)


def draw_row(hmap, polygons, ranges, outdir, filename, logz=False, ztitle=None):
    keep = []
    cname = "c_" + filename.replace(".pdf", "")
    can = ROOT.TCanvas(cname, cname, 1600, 520)
    can.Divide(3, 1, 0.01, 0.01)
    for icol, layer in enumerate(LAYERS, start=1):
        pad = can.cd(icol)
        pad.SetRightMargin(0.20)
        pad.SetLeftMargin(0.12)
        pad.SetTopMargin(0.12)
        pad.SetBottomMargin(0.12)
        style_polygon_grid(pad)
        hist = hmap[layer]
        xmin, xmax, ymin, ymax = ranges[layer]
        hist.GetXaxis().SetRangeUser(xmin, xmax)
        hist.GetYaxis().SetRangeUser(ymin, ymax)
        if ztitle:
            hist.GetZaxis().SetTitle(ztitle)
        if logz:
            pad.SetLogz(1)
        hist.Draw("colz")
        adjust_z_palette(hist, pad)
        overlay_polygons(polygons, layer, keep)
        keep.append(hist)
    _ = keep
    return save(can, outdir, filename)


def apply_sidis_cut(rdf, cols, label):
    if SIDIS_CUT not in cols:
        raise SystemExit("Missing column %s in %s" % (SIDIS_CUT, label))
    print("Applied %s to %s before histogram filling" % (SIDIS_CUT, label))
    return rdf.Filter(SIDIS_CUT)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-d", "--data", dest="data", required=True)
    parser.add_argument("-m", "--mc", dest="mc", required=True)
    parser.add_argument("-t", "--tree", dest="tree", default="h22")
    parser.add_argument("-o", "--out", dest="out", default=".")
    parser.add_argument("-n", "--max_entries", dest="max_entries", type=int, default=-1)
    parser.add_argument(
        "-ar", "--analysis_root",
        dest="analysis_root",
        default=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")),
    )
    parser.add_argument(
        "-zdc", "--zoom_dc",
        dest="zoom_dc",
        action="store_true",
        help="Optional occupancy-based DC axis zoom (default: Fiducial_Cut All-sector ranges).",
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

    rdf = apply_sidis_cut(rdf, cols, "Data")
    mdf = apply_sidis_cut(mdf, mcols, "REC-MC")

    print("Booking pion DC occupancy: %d bins, x,y in [%.0f, %.0f] cm" % (NBINS, BOOK_LO, BOOK_HI))
    data_res, mc_res = {}, {}
    for layer in LAYERS:
        data_res[layer] = book_occupancy(
            rdf, layer, "hdata%d" % layer, "Data, DC %s;x [cm];y [cm]" % region_label(layer)
        )
        mc_res[layer] = book_occupancy(
            mdf, layer, "hmc%d" % layer, "Reconstructed MC, DC %s;x [cm];y [cm]" % region_label(layer)
        )

    h_data, h_mc, h_diff, ranges = {}, {}, {}, {}
    for layer in LAYERS:
        hd = ptr(data_res[layer])
        hm = ptr(mc_res[layer])
        ranges[layer] = display_range(layer, hd, hm, args.zoom_dc)
        print("Layer %d display range: x in [%.0f, %.0f] cm, y in [%.0f, %.0f] cm" % (
            layer, ranges[layer][0], ranges[layer][1], ranges[layer][2], ranges[layer][3]
        ))
        normalize_occupancy(hd)
        normalize_occupancy(hm)
        hdiff = ratio_of_2d_histos(hd, hm, "hdiff%d" % layer)
        hdiff.SetTitle("#splitline{%% Diff, DC %s}{#scale[0.5]{Comparison of Normalized Data/MC Hits}};x [cm];y [cm]" % region_label(layer))
        h_data[layer], h_mc[layer], h_diff[layer] = hd, hm, hdiff

    draw_row(h_data, polygons, ranges, args.out, "pip_DC_polygons_Data.pdf")
    draw_row(h_mc, polygons, ranges, args.out, "pip_DC_polygons_MC.pdf")
    draw_row(h_diff, polygons, ranges, args.out, "pip_DC_polygons_Percent_Diff.pdf", logz=True, ztitle="% Diff")
    print("Polygon 1x3 figures written to", args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
