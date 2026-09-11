#!/usr/bin/env python3
# Chapter 3 non-HIPO figures from analysis ROOT DataFrames (rdf / mdf / gdf).
# Usage (from Histo_Files_ROOT/DataFrames):
#     python Chapter3_DataFrame_Figures.py --format pdf --data_root work --out /path/to/Analysis_Cut_Images
#     python Chapter3_DataFrame_Figures.py --format root --data_root work --out Chapter3_DataFrame_hists.root
from __future__ import print_function

import argparse
import glob
import os
import sys

import ROOT

_BOOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if(_BOOT not in sys.path):
    sys.path.insert(0, _BOOT)
from jlab_work_paths import (
    add_data_root_argument, bootstrap_from_file, collect_files_with_fallback,
    dataframe_output_dir, print_path_summary,
)
EXEC_ROOT = bootstrap_from_file(__file__)
from ExtraAnalysisCodeValues import Default_MM_Cut, Define_Cut_Variations_With_Smeared_Kinematics
from MyCommonAnalysisFunction_richcap import Draw_Q2_Y_Bins, Draw_z_pT_Bins_With_Migration
from helper_functions_for_using_RDataFrames_python import Multi_Bin_Standard_Def_Function, rdf_define_or_redefine
from Chapter3_Pion_DC_Polygon_Plots import expand, run_polygon_plots

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

PID_DEFAULT = " && ".join([
    "(CHI2PID_CUT_mid_pip == 1)",
    "(DC_FIDUCIAL_REG1_mid_el == 1) && (DC_FIDUCIAL_REG2_mid_el == 1) && (DC_FIDUCIAL_REG3_mid_el == 1)",
    "(DC_FIDUCIAL_REG1_mid_pip == 1) && (DC_FIDUCIAL_REG2_mid_pip == 1) && (DC_FIDUCIAL_REG3_mid_pip == 1)",
    "(DC_VERTEX_mid_el == 1)",
    "(DELTA_VZ_mid_pip == 1)",
    "(EC_OUTER_VS_INNER_mid_el == 1)",
    "(EC_SAMPLING_BAND_mid_el == 1)",
    "(EC_SAMPLING_THRESHOLD_mid_el == 1)",
    "(EC_SAMPLING_TRIANGLE_mid_el == 1)",
])
NONPID_DEFAULT = " && ".join([
    "(valerii_PCAL_knockout_cut)",
    "(Valerii_PCal_Fiducial_Cuts)",
    "(Sector_PCal_Fiducial_Cuts)",
    "(Valerii_DC_Fiducial_Cuts_ele_DC_6) && (Valerii_DC_Fiducial_Cuts_ele_DC_18) && (Valerii_DC_Fiducial_Cuts_ele_DC_36)",
    "(My_pip_DC_Fiducial_Cuts_Layer_6) && (My_pip_DC_Fiducial_Cuts_Layer_18) && (My_pip_DC_Fiducial_Cuts_Layer_36)",
])
KIN_CLAUSES = [
    ("Q2",    "(Q2 > 2)",                                              ["Q2 > 2"]),
    ("pip",   "(pip > 1.25) && (pip < 5)",                             ["1.25 < pip < 5"]),
    ("pipth", "(5 < pipth) && (pipth < 35)",                           ["5 < pipth < 35"]),
    ("elth",  "(5 < elth) && (elth < 35)",                             ["5 < elth < 35"]),
    ("y",     "(y < 0.75)",                                            ["y < 0.75"]),
    ("xF",    "(xF > 0)",                                              ["xF > 0"]),
    ("MM",    "(MM > %s)" % Default_MM_Cut,                            ["MM > %s" % Default_MM_Cut]),
]
KIN_PLOTS = [
    ("Q2",    "Q2",        0.0, 12.0, 140, [2.0],           "Q^{2};Q^{2} [GeV^{2}];Counts",           "Q2_cut.pdf"),
    ("pip",   "pip",       0.0,  8.0, 120, [1.25, 5.0],     "p_{#pi^{+}};p_{#pi^{+}} [GeV];Counts",   "pip_mom_cut.pdf"),
    ("pipth", "pipth",     0.0, 50.0, 100, [5.0, 35.0],     "#theta_{#pi^{+}};#theta_{#pi^{+}} [deg];Counts", "pip_theta_cut.pdf"),
    ("elth",  "elth",      0.0, 50.0, 100, [5.0, 35.0],     "#theta_{e};#theta_{e} [deg];Counts",     "el_theta_cut.pdf"),
    ("y",     "y",         0.0,  1.0, 100, [0.75],          "y;y;Counts",                             "y_cut.pdf"),
    ("xF",    "xF",       -1.0,  1.0, 100, [0.0],           "x_{F};x_{F};Counts",                     "xF_cut.pdf"),
    ("MM",    "MM",        0.0,  4.0, 120, [Default_MM_Cut], "M_{X};M_{X} [GeV];Counts",              "MM_cut.pdf"),
]


def ptr(hist):
    if(hasattr(hist, "GetPtr")):
        return hist.GetPtr()
    return hist


def rdf_has(df, col):
    try:
        return bool(df.HasColumn(col))
    except Exception:
        return False


def discover_files(data_root_key, data_type, explicit):
    if(explicit not in [None, ""]):
        return expand(explicit)
    found, missing = collect_files_with_fallback(dataframe_output_dir(data_root_key, data_type), ["*Final_Thesis_Files*.root"], data_root_key)
    if(missing):
        print("Missing search dirs for %s: %s" % (data_type, missing))
    return found


def open_chain(files, tree, max_entries):
    if(not files):
        return None
    chain = ROOT.TChain(tree)
    for path in files:
        chain.Add(path, 0)
    rdf = ROOT.RDataFrame(chain)
    if((max_entries is not None) and (int(max_entries) > 0)):
        rdf = rdf.Range(int(max_entries))
    return rdf


def kin_without(omit_key):
    parts = [expr for key, expr, _lab in KIN_CLAUSES if(key != omit_key)]
    return " && ".join(parts)


def can_omit_one(rdf):
    needed = ["DC_FIDUCIAL_REG1_mid_el", "CHI2PID_CUT_mid_pip", "valerii_PCAL_knockout_cut", "Valerii_DC_Fiducial_Cuts_ele_DC_6"]
    return all(rdf_has(rdf, col) for col in needed)


def apply_omit_one(rdf, omit_key):
    cut = " && ".join(["(%s)" % PID_DEFAULT, "(%s)" % NONPID_DEFAULT, "(%s)" % kin_without(omit_key)])
    print("Omit-one %s filter: %s" % (omit_key, cut))
    return rdf.Filter(cut)


def save_canvas(can, out_dir, name, fmt, root_file):
    os.makedirs(out_dir, exist_ok=True)
    if(fmt in ["pdf"]):
        path = os.path.join(out_dir, name)
        can.SaveAs(path)
        print("Wrote", path)
        return path
    key = name.replace(".pdf", "")
    if(root_file is not None):
        can.Write(key)
        print("Wrote canvas", key)
    return key


def plot_1d_cut(rdf, omit_key, var, nbins, xmin, xmax, lines, title, out_name, out_dir, fmt, root_file):
    rdf_cut = apply_omit_one(rdf, omit_key)
    hist = ptr(rdf_cut.Histo1D(("h_%s" % omit_key, title, nbins, xmin, xmax), var))
    if(root_file is not None):
        root_file.cd()
        hist.Write("h_%s" % omit_key)
    can = ROOT.TCanvas("c_%s" % omit_key, "c_%s" % omit_key, 700, 500)
    hist.Draw("hist")
    ROOT.gPad.SetGrid(1, 1)
    ymax = hist.GetMaximum() * 1.05
    if(ymax <= 0):
        ymax = 1.0
    keep = [hist]
    for xcut in lines:
        line = ROOT.TLine(float(xcut), 0.0, float(xcut), ymax)
        line.SetLineColor(ROOT.kRed)
        line.SetLineWidth(2)
        line.Draw("same")
        keep.append(line)
    can.keep = keep
    return save_canvas(can, out_dir, out_name, fmt, root_file)


def ensure_zpt(rdf):
    if(not (rdf_has(rdf, "Q2_Y_Bin") and rdf_has(rdf, "z") and rdf_has(rdf, "pT"))):
        return rdf
    code = Multi_Bin_Standard_Def_Function(Variable_Type="", Dimension="2D", Use_Dense_Binning=False, args=None)
    return rdf_define_or_redefine(rdf, "z_pT_Bin_Y_bin", code)


def plot_q2_y(rdf, out_dir, fmt, root_file, name, title, use_xb=False):
    if(use_xb):
        hist = ptr(rdf.Histo2D(("h_q2xb", title, 100, 0.0, 0.8, 140, 0.0, 12.0), "xB", "Q2"))
    else:
        hist = ptr(rdf.Histo2D(("h_q2y", title, 100, 0.05, 1.05, 140, 0.0, 12.0), "y", "Q2"))
    if(root_file is not None):
        root_file.cd()
        hist.Write(hist.GetName())
    can = ROOT.TCanvas("c_" + name, "c_" + name, 900, 700)
    hist.Draw("colz")
    ROOT.gPad.SetLogz(1)
    ROOT.gPad.SetGrid(1, 1)
    keep = [hist]
    for ibin in range(1, 18):
        for line in Draw_Q2_Y_Bins(Input_Bin=ibin, Use_xB=use_xb):
            line.Draw("same")
            keep.append(line)
    can.keep = keep
    return save_canvas(can, out_dir, name, fmt, root_file)


def plot_zpt_one(rdf, q2y, out_dir, fmt, root_file):
    rdf_bin = rdf.Filter("(Q2_Y_Bin == %d)" % q2y)
    hist = ptr(rdf_bin.Histo2D(("h_zpt_%d" % q2y, "z vs P_{T} (Q^{2}-y bin %d);z;P_{T} [GeV]" % q2y, 100, 0.0, 1.0, 105, 0.0, 1.05), "z", "pT"))
    if(root_file is not None):
        root_file.cd()
        hist.Write(hist.GetName())
    can = ROOT.TCanvas("c_zpt_%d" % q2y, "c_zpt_%d" % q2y, 800, 700)
    hist.Draw("colz")
    ROOT.gPad.SetLogz(1)
    ROOT.gPad.SetGrid(1, 1)
    borders = Draw_z_pT_Bins_With_Migration(Q2_y_Bin_Num_In=q2y, Set_Max_Y=1.05, Set_Max_X=1.0, Plot_Orientation_Input="z_pT")
    can.keep = [hist, borders]
    return save_canvas(can, out_dir, "Normal_2D_Histos_For_Q2_y_Bin_%d.pdf" % q2y, fmt, root_file)


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_data_root_argument(parser)
    parser.add_argument("-d", "--data", default=None, help="Optional explicit rdf glob/path. Not rewritten if given.")
    parser.add_argument("-m", "--mc", default=None, help="Optional explicit mdf glob/path. Not rewritten if given.")
    parser.add_argument("-g", "--gen", default=None, help="Optional explicit gdf glob/path. Not rewritten if given.")
    parser.add_argument("-t", "--tree", default="h22")
    parser.add_argument("-o", "--out", default="Chapter3_DataFrame_Plots")
    parser.add_argument("-f", "--format", dest="fmt", choices=["pdf", "root"], default="pdf")
    parser.add_argument("-n", "--event_limit", type=int, default=-1)
    parser.add_argument("-p", "--plots", nargs="+", default=["all"], choices=["all", "1d", "polygons", "2d"], help="Which figure groups to produce.")
    return parser.parse_args()


def main():
    args = parse_args()
    print_path_summary(EXEC_ROOT, args.data_root)
    data_files = discover_files(args.data_root, "rdf", args.data)
    mc_files = discover_files(args.data_root, "mdf", args.mc)
    gen_files = discover_files(args.data_root, "gdf", args.gen)
    print("rdf files: %d  mdf files: %d  gdf files: %d" % (len(data_files), len(mc_files), len(gen_files)))
    if(not data_files):
        raise SystemExit("No REAL_Data DataFrame files found")
    want = set(args.plots)
    if("all" in want):
        want = set(["1d", "polygons", "2d"])
    out_dir = args.out
    root_file = None
    if(args.fmt in ["root"]):
        if(not str(args.out).endswith(".root")):
            os.makedirs(args.out, exist_ok=True)
            out_path = os.path.join(args.out, "Chapter3_DataFrame_hists.root")
        else:
            out_path = args.out
            out_dir = os.path.dirname(os.path.abspath(out_path)) or "."
        root_file = ROOT.TFile.Open(out_path, "RECREATE")
        print("ROOT output", out_path)
    rdf = open_chain(data_files, args.tree, args.event_limit)
    if((rdf is not None) and (not rdf_has(rdf, "MM")) and rdf_has(rdf, "MM2")):
        rdf = rdf.Define("MM", "sqrt(MM2)")
    if((rdf is not None) and rdf_has(rdf, "DC_FIDUCIAL_REG1_mid_el")):
        rdf, _cuts = Define_Cut_Variations_With_Smeared_Kinematics(rdf, df_type="rdf")
    written = []
    if("1d" in want):
        # 1D omit-one kinematic PDFs: use Chapter3_Kinematic_Cut_Figures.py (Groovy ntuples). Processed DataFrames lack PID/fiducial flag columns.
        if(not can_omit_one(rdf)):
            print("Skipping 1D omit-one kinematic plots: DataFrame is missing the production PID/fiducial flag columns used by PID_Default/NonPID_Default. Use Chapter3_Kinematic_Cut_Figures.py on Groovy-converted ntuples.")
        else:
            for omit_key, var, xmin, xmax, nbins, lines, title, fname in KIN_PLOTS:
                written.append(plot_1d_cut(rdf, omit_key, var, nbins, xmin, xmax, lines, title, fname, out_dir, args.fmt, root_file))
    if("2d" in want):
        rdf_full = rdf.Filter("cut_Complete_SIDIS")
        rdf_full = ensure_zpt(rdf_full)
        written.append(plot_q2_y(rdf_full, out_dir, args.fmt, root_file, "Q2_vs_y.pdf", "Q^{2} vs y;y;Q^{2} [GeV^{2}]", use_xb=False))
        if(rdf_has(rdf_full, "xB")):
            written.append(plot_q2_y(rdf_full, out_dir, args.fmt, root_file, "Q2_vs_xB.pdf", "Q^{2} vs x_{B};x_{B};Q^{2} [GeV^{2}]", use_xb=True))
        for q2y in range(1, 18):
            written.append(plot_zpt_one(rdf_full, q2y, out_dir, args.fmt, root_file))
    if("polygons" in want):
        if(not mc_files):
            print("Skipping pion DC polygons: no matched-MC files")
        else:
            run_polygon_plots(data_files, mc_files, out_dir, tree=args.tree, max_entries=args.event_limit, analysis_root=EXEC_ROOT)
    if(root_file is not None):
        root_file.Close()
    print("Done. %d outputs" % len([w for w in written if(w)]))
    return 0


if(__name__ == "__main__"):
    sys.exit(main())
