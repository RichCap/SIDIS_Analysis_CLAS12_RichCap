#!/usr/bin/env python3
# Matched-MC bin-migration (generated Q2 vs y) and matched-PID 1D overlays.
# Usage (from Histo_Files_ROOT/DataFrames):
#     python Chapter3_MC_Bin_Migration_Q2_y.py --data_root work --batch_id 0 --out /path/to/Chapter3_MC_Bin_Migration
from __future__ import print_function

import argparse
import os
import sys

import ROOT

_BOOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if(_BOOT not in sys.path):
    sys.path.insert(0, _BOOT)
from jlab_work_paths import add_data_root_argument, bootstrap_from_file, load_file_batches, print_path_summary
EXEC_ROOT = bootstrap_from_file(__file__)
from MyCommonAnalysisFunction_richcap import Draw_Q2_Y_Bins, Get_Num_of_z_pT_Bins_w_Migrations, skip_condition_z_pT_bins
from helper_functions_for_using_RDataFrames_python import (
    Multi_Bin_Standard_Def_Function, apply_matching_and_redefine_gen, rdf_define_or_redefine, rdf_has_column,
)
from ExtraAnalysisCodeValues import Default_MM_Cut
from Chapter3_DataFrame_Figures import expand, KIN_PLOTS

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

MATCH_RUNS = [("_gen", "gen"), ("Bank", "Bank")]
PID_CATS = [
    ("all",      "1",                                                      ROOT.kBlack,   "All selected"),
    ("both_ok",  "(PID_el == 11) && (PID_pip == 211)",                     ROOT.kGreen+2, "Both correct"),
    ("both_bad", "(PID_el != 0) && (PID_el != 11) && (PID_pip != 0) && (PID_pip != 211)", ROOT.kRed, "Both incorrect"),
    ("ele_bad",  "(PID_el != 0) && (PID_el != 11) && (PID_pip == 211)",    ROOT.kOrange+7, "e wrong, #pi^{+} correct"),
    ("pip_bad",  "(PID_el == 11) && (PID_pip != 0) && (PID_pip != 211)",   ROOT.kBlue,    "e correct, #pi^{+} wrong"),
    ("unmatch",  "(PID_el == 0) || (PID_pip == 0)",                       ROOT.kMagenta, "Unmatched"),
]
# 1D overlays for this study use reconstructed SIDIS kinematics (not KIN_PLOTS).
REC_1D_PLOTS = [
    ("Q2",    "Q2",    0.0, 12.0, 140, "Q^{2};Q^{2} [GeV^{2}];Counts"),
    ("y",     "y",     0.0,  1.0, 100, "y;y;Counts"),
    ("z",     "z",     0.0,  1.0, 100, "z;z;Counts"),
    ("pT",    "pT",    0.0, 1.20, 120, "P_{T};P_{T} [GeV];Counts"),
    ("xB",    "xB",    0.0,  0.8, 100, "x_{B};x_{B};Counts"),
    ("phi_t", "phi_t", 0.0, 360.0, 72, "#phi_{h};#phi_{h} [deg];Counts"),
]
Q2Y_NX, Q2Y_XMIN, Q2Y_XMAX = 100, 0.05, 1.05
Q2Y_NY, Q2Y_YMIN, Q2Y_YMAX = 140, 0.0, 12.0
Q2Y_CANVAS_W, Q2Y_CANVAS_H = 900, 700
MATCHED_NONZERO = "(PID_el != 0) && (PID_pip != 0)"


def ptr(hist):
    if(hasattr(hist, "GetPtr")):
        return hist.GetPtr()
    return hist


def combine_batches(batch_list, number_of_files=-1):
    combined_list = []
    for ii in batch_list:
        for jj in batch_list[ii]:
            combined_list.append(jj)
            if((len(combined_list) >= number_of_files) and (number_of_files > 0)):
                return combined_list
    return combined_list


def is_lund(path):
    name = os.path.basename(str(path)).lower()
    return (("lundrho" in name) or ("lundvpk" in name))


def valid_rec_bin_cut():
    parts = ["(Q2_Y_Bin >= 1)", "(Q2_Y_Bin <= 17)", "(z_pT_Bin_Y_bin >= 1)"]
    for q2y in range(1, 18):
        nmax = Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=q2y)[1]
        for zpt in range(1, int(nmax) + 1):
            if(skip_condition_z_pT_bins(Q2_Y_BIN=q2y, Z_PT_BIN=zpt)):
                parts.append("!((Q2_Y_Bin == %d) && (z_pT_Bin_Y_bin == %d))" % (q2y, zpt))
    return " && ".join(parts)


def ensure_zpt(rdf):
    code = Multi_Bin_Standard_Def_Function(Variable_Type="", Dimension="2D", Use_Dense_Binning=False, args=None)
    return rdf_define_or_redefine(rdf, "z_pT_Bin_Y_bin", code)


def save_pdf(can, out_dir, name):
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, name)
    can.SaveAs(path)
    print("Wrote", path)
    return path


def apply_q2y_pad():
    ROOT.gPad.SetLeftMargin(0.12)
    ROOT.gPad.SetRightMargin(0.14)
    ROOT.gPad.SetBottomMargin(0.12)
    ROOT.gPad.SetTopMargin(0.08)
    ROOT.gPad.SetLogz(1)
    ROOT.gPad.SetGrid(1, 1)


def plot_q2y_gen(rdf, tag, out_dir):
    hist = ptr(rdf.Histo2D(("h_q2y_gen_%s" % tag, "Generated Q^{2} vs y (%s);y_{gen};Q^{2}_{gen} [GeV^{2}]" % tag, Q2Y_NX, Q2Y_XMIN, Q2Y_XMAX, Q2Y_NY, Q2Y_YMIN, Q2Y_YMAX), "y_gen", "Q2_gen"))
    nent = int(hist.GetEntries())
    print("2D generated Q2 vs y (%s) entries: %d" % (tag, nent))
    can = ROOT.TCanvas("c_mig_%s" % tag, "c_mig_%s" % tag, Q2Y_CANVAS_W, Q2Y_CANVAS_H)
    hist.Draw("colz")
    apply_q2y_pad()
    keep = [hist]
    for ibin in range(1, 18):
        for line in Draw_Q2_Y_Bins(Input_Bin=ibin, Use_xB=False):
            line.Draw("same")
            keep.append(line)
    can.keep = keep
    return hist, nent, save_pdf(can, out_dir, "Chapter3_MC_bin_migration_Q2_y_%s.pdf" % tag)


def plot_q2y_compare(h_gen, h_bank, out_dir):
    can = ROOT.TCanvas("c_mig_cmp", "c_mig_cmp", 1600, 700)
    can.Divide(2, 1)
    keep = [h_gen, h_bank]
    for i, (hist, title) in enumerate(((h_gen, "default _gen"), (h_bank, "Bank")), start=1):
        can.cd(i)
        hist.SetTitle("Generated Q^{2} vs y (%s);y_{gen};Q^{2}_{gen} [GeV^{2}]" % title)
        hist.Draw("colz")
        apply_q2y_pad()
        for ibin in range(1, 18):
            for line in Draw_Q2_Y_Bins(Input_Bin=ibin, Use_xB=False):
                line.Draw("same")
                keep.append(line)
    can.keep = keep
    return save_pdf(can, out_dir, "Chapter3_MC_bin_migration_Q2_y_gen_vs_Bank.pdf")


def print_pid_category_counts(rdf, tag, var_name="Q2"):
    print("PID-category counts for %s (%s):" % (var_name, tag))
    counts = {}
    for cat, cut, _col, label in PID_CATS:
        rdf_c = rdf if(cat in ["all"]) else rdf.Filter(cut)
        nent = int(rdf_c.Count().GetValue())
        counts[cat] = nent
        print("  %s (%s): %d" % (cat, label, nent))
    return counts


def plot_pid_1d(rdf, tag, out_dir, also_norm):
    written = []
    for omit_key, var, xmin, xmax, nbins, title in REC_1D_PLOTS:
        can = ROOT.TCanvas("c_pid_%s_%s" % (omit_key, tag), "c_pid_%s_%s" % (omit_key, tag), 800, 600)
        legend = ROOT.TLegend(0.50, 0.55, 0.88, 0.88)
        legend.SetBorderSize(0)
        legend.SetFillStyle(0)
        keep = []
        first = True
        for cat, cut, col, label in PID_CATS:
            rdf_c = rdf if(cat in ["all"]) else rdf.Filter(cut)
            hist = ptr(rdf_c.Histo1D(("h_%s_%s_%s" % (omit_key, tag, cat), "%s (%s);%s;Counts" % (title.split(";")[0], tag, title.split(";")[1] if(";" in title) else ""), nbins, xmin, xmax), var))
            hist.SetLineColor(col)
            hist.SetLineWidth(2)
            hist.SetMarkerColor(col)
            drawopt = "hist" if(first) else "hist same"
            hist.Draw(drawopt)
            first = False
            legend.AddEntry(hist, label, "l")
            keep.append(hist)
        legend.Draw()
        keep.append(legend)
        can.keep = keep
        written.append(save_pdf(can, out_dir, "Chapter3_MC_match_PID_%s_%s.pdf" % (omit_key, tag)))
        if(also_norm):
            can_n = ROOT.TCanvas("c_pidn_%s_%s" % (omit_key, tag), "c_pidn_%s_%s" % (omit_key, tag), 800, 600)
            legend_n = ROOT.TLegend(0.50, 0.55, 0.88, 0.88)
            legend_n.SetBorderSize(0)
            legend_n.SetFillStyle(0)
            keep_n = []
            first = True
            for hist, (_cat, _cut, col, label) in zip(keep[:-1], PID_CATS):
                hn = hist.Clone(hist.GetName() + "_norm")
                if(hn.Integral() != 0):
                    hn.Scale(1.0 / hn.Integral())
                hn.SetLineColor(col)
                hn.Draw("hist" if(first) else "hist same")
                first = False
                legend_n.AddEntry(hn, label, "l")
                keep_n.append(hn)
            legend_n.Draw()
            keep_n.append(legend_n)
            can_n.keep = keep_n
            written.append(save_pdf(can_n, out_dir, "Chapter3_MC_match_PID_%s_%s_norm.pdf" % (omit_key, tag)))
    return written


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_data_root_argument(parser)
    parser.add_argument("-m", "--mc", default=None, help="Optional explicit mdf glob/path. Not rewritten if given.")
    parser.add_argument("-bID", "--batch_id", type=int, default=0, help="File_Batches group (0 = all non-LUND clasdis mdf).")
    parser.add_argument("-numF", "--number_of_files", type=int, default=-1)
    parser.add_argument("-t", "--tree", default="h22")
    parser.add_argument("-o", "--out", default="Chapter3_MC_Bin_Migration")
    parser.add_argument("-n", "--event_limit", type=int, default=-1)
    parser.add_argument("--skip_q2y_migration", action="store_true")
    parser.add_argument("--skip_pid_match_1d", action="store_true")
    parser.add_argument("--norm_pid_1d", action="store_true", help="Also write unit-normalized PID overlay copies.")
    return parser.parse_args()


def load_mdf_files(args):
    if(args.mc not in [None, ""]):
        return expand(args.mc)
    rdf_batch, mdf_batch, gdf_batch, batch_path = load_file_batches(args.data_root, execution_root=EXEC_ROOT)
    print("File_Batches:", batch_path)
    if(args.batch_id > 0):
        files = list(mdf_batch.get(args.batch_id, []))
    else:
        files = combine_batches(mdf_batch, args.number_of_files)
    files = [p for p in files if(not is_lund(p))]
    return files


def open_mdf(files, tree, max_entries):
    chain = ROOT.TChain(tree)
    for path in files:
        chain.Add(path, 0)
    rdf = ROOT.RDataFrame(chain)
    if((max_entries is not None) and (int(max_entries) > 0)):
        rdf = rdf.Range(int(max_entries))
    return rdf


def rec_selected(rdf):
    rdf = rdf.Filter("cut_Complete_SIDIS")
    rdf = ensure_zpt(rdf)
    rdf = rdf.Filter(valid_rec_bin_cut())
    return rdf


def main():
    args = parse_args()
    print_path_summary(EXEC_ROOT, args.data_root)
    files = load_mdf_files(args)
    if(not files):
        raise SystemExit("No non-LUND matched-MC files found")
    print("mdf files:", len(files))
    for path in files:
        print("input file:", os.path.basename(path))
    chain0 = ROOT.TChain(args.tree)
    for path in files:
        chain0.Add(path, 0)
    n_input = int(chain0.GetEntries())
    print("input h22 entries:", n_input)
    rdf0 = rec_selected(open_mdf(files, args.tree, args.event_limit))
    if((not rdf_has_column(rdf0, "MM")) and rdf_has_column(rdf0, "MM2")):
        rdf0 = rdf0.Define("MM", "sqrt(MM2)")
    n_rec = int(rdf0.Count().GetValue())
    print("reconstructed-selected entries (cut_Complete_SIDIS + retained 4D bin):", n_rec)
    os.makedirs(args.out, exist_ok=True)
    hists = {}
    for match_key, tag in MATCH_RUNS:
        try:
            rdf_m, msg = apply_matching_and_redefine_gen(rdf0, match_key)
            print(msg)
        except (ValueError, RuntimeError) as err:
            print("Skipping matching %s: %s" % (tag, err))
            continue
        if((not rdf_has_column(rdf_m, "Q2_gen")) or (not rdf_has_column(rdf_m, "y_gen"))):
            print("Skipping matching %s: missing Q2_gen/y_gen after redefinition" % tag)
            continue
        if(not args.skip_q2y_migration):
            rdf_2d = rdf_m.Filter(MATCHED_NONZERO)
            hist, n_2d, _path = plot_q2y_gen(rdf_2d, tag, args.out)
            hists[tag] = hist
            print("2D nonzero generated-PID count (%s): %d" % (tag, n_2d))
        if(not args.skip_pid_match_1d):
            if((not rdf_has_column(rdf_m, "PID_el")) or (not rdf_has_column(rdf_m, "PID_pip"))):
                print("Skipping PID 1D for %s: missing PID_el/PID_pip" % tag)
            else:
                print_pid_category_counts(rdf_m, tag, var_name="Q2")
                plot_pid_1d(rdf_m, tag, args.out, args.norm_pid_1d)
    if((not args.skip_q2y_migration) and ("gen" in hists) and ("Bank" in hists)):
        plot_q2y_compare(hists["gen"], hists["Bank"], args.out)
    print("Done.")
    return 0


if(__name__ == "__main__"):
    sys.exit(main())
