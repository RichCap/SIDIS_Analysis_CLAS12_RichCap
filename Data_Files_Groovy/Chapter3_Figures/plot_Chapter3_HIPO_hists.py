#!/usr/bin/env python3
"""Render Chapter 3 PID/fiducial figures from the combined HIPO histogram ROOT file.

Usage (from Data_Files_Groovy, after hadd):
    python Chapter3_Figures/plot_Chapter3_HIPO_hists.py \\
        --root Chapter3_Figures/Chapter3_HIPO_hists_combined.root \\
        --out  /path/to/Experiment/Data_Collection_Images/Analysis_Cut_Images
"""
from __future__ import print_function

import argparse
import math
import os
import sys

import ROOT

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetGridColor(ROOT.kGray)
ROOT.gStyle.SetGridStyle(3)
ROOT.gStyle.SetGridWidth(1)

P0MEAN = [0.111767, 0.116619, 0.114606, 0.116586, 0.118251, 0.117391]
P1MEAN = [-0.0281943, 0.0662751, -0.0896597, 0.181465, 0.085993, 0.0186504]
P2MEAN = [0.00711137, 0.00633334, 0.00912098, 0.00652068, 0.00416682, 0.00622289]
P3MEAN = [-0.000878776, -0.000780257, -0.00108891, -0.000645957, -0.000485189, -0.000829729]
P0SIG = [-0.00497609, 0.0259435, 0.0296159, 0.0161445, 0.0239166, 0.0244309]
P1SIG = [0.0275006, -0.000805156, -0.00449379, 0.0099462, 0.00192551, 0.00258059]
P2SIG = [0.00253641, -0.00386759, -0.00469883, -0.00182968, -0.00355973, -0.00398967]
P3SIG = [-0.000173549, 0.00030325, 0.000380195, 0.00012328, 0.000302528, 0.000340911]

M_PI = 0.13957039
M_K = 0.493677
M_P = 0.938272081


def apply_grid(pad=None):
    if pad is None:
        pad = ROOT.gPad
    if pad is not None:
        pad.SetGrid(1, 1)


def sf_mean_sigma(p, isec):
    p2 = p * p
    mean = P0MEAN[isec] * (1.0 + p / math.sqrt(p2 + P1MEAN[isec])) + P2MEAN[isec] * p + P3MEAN[isec] * p2
    sigma = P0SIG[isec] + P1SIG[isec] / math.sqrt(p) + P2SIG[isec] * p + P3SIG[isec] * p2
    return mean, sigma


def beta_mass(p, mass):
    return p / math.sqrt(p * p + mass * mass)


def save(can, outdir, name):
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, name)
    can.SaveAs(path)
    print("Wrote", path)
    return path


def plot_htcc(root_file, outdir):
    hist = root_file.Get("h_htcc_nphe")
    if not hist:
        print("SKIP h_htcc_nphe")
        return None
    can = ROOT.TCanvas("c_htcc", "c_htcc", 700, 500)
    hist.SetTitle(";N_{phe}^{HTCC};Counts")
    hist.Draw("hist")
    apply_grid()
    ymax = hist.GetMaximum() * 1.05
    line = ROOT.TLine(2.0, 0.0, 2.0, ymax)
    line.SetLineColor(ROOT.kRed)
    line.SetLineWidth(2)
    line.Draw("same")
    can.keep = [hist, line]
    return save(can, outdir, "HTCC_Nphe.pdf")


def plot_pcal(root_file, outdir):
    hist = root_file.Get("h_pcal_energy")
    if not hist:
        print("SKIP h_pcal_energy")
        return None
    can = ROOT.TCanvas("c_pcal", "c_pcal", 700, 500)
    hist.SetTitle(";E_{PCAL} [GeV];Counts")
    hist.Draw("hist")
    apply_grid()
    ymax = hist.GetMaximum() * 1.05
    line = ROOT.TLine(0.06, 0.0, 0.06, ymax)
    line.SetLineColor(ROOT.kRed)
    line.SetLineWidth(2)
    line.Draw("same")
    can.keep = [hist, line]
    return save(can, outdir, "PCAL_Emin.pdf")


def plot_sftot(root_file, outdir):
    can = ROOT.TCanvas("c_sftot", "c_sftot", 1400, 900)
    can.Divide(3, 2)
    keep = []
    pmin, pmax, ncurve = 1.0, 10.5, 80
    for sec in range(1, 7):
        pad = can.cd(sec)
        pad.SetRightMargin(0.12)
        hist = root_file.Get("h_sftot_sec%d" % sec)
        if not hist:
            print("SKIP h_sftot_sec%d" % sec)
            continue
        hist.SetTitle("Sector %d;p_{e} [GeV];SF_{tot}" % sec)
        hist.Draw("colz")
        keep.append(hist)
        gx_lo = ROOT.TGraph(ncurve)
        gx_hi = ROOT.TGraph(ncurve)
        gx_mu = ROOT.TGraph(ncurve)
        for i in range(ncurve):
            p = pmin + (pmax - pmin) * i / (ncurve - 1)
            mu, sig = sf_mean_sigma(p, sec - 1)
            gx_mu.SetPoint(i, p, mu)
            gx_lo.SetPoint(i, p, mu - 3.5 * sig)
            gx_hi.SetPoint(i, p, mu + 3.5 * sig)
        for g, col in ((gx_mu, ROOT.kBlack), (gx_lo, ROOT.kRed), (gx_hi, ROOT.kRed)):
            g.SetLineWidth(2)
            g.SetLineColor(col)
            g.Draw("L same")
            keep.append(g)
    can.keep = keep
    return save(can, outdir, "SFtot_band.pdf")


def plot_beta(root_file, outdir):
    hist = root_file.Get("h_beta_poshad")
    if not hist:
        print("SKIP h_beta_poshad")
        return None
    can = ROOT.TCanvas("c_beta", "c_beta", 800, 650)
    hist.SetTitle(";p [GeV];#beta")
    hist.Draw("colz")
    apply_grid()
    keep = [hist]
    n = 80
    for mass, col in ((M_PI, ROOT.kRed), (M_K, ROOT.kGreen + 2), (M_P, ROOT.kBlue)):
        gr = ROOT.TGraph(n)
        for i in range(n):
            p = 0.2 + (7.5 - 0.2) * i / (n - 1)
            gr.SetPoint(i, p, beta_mass(p, mass))
        gr.SetLineColor(col)
        gr.SetLineWidth(2)
        gr.Draw("L same")
        keep.append(gr)
    can.keep = keep
    return save(can, outdir, "Beta_PID.pdf")


def plot_electron_dc(root_file, outdir):
    layers = [(1, 6, 0.50, 72.0, -160, 20, -90, 90), (2, 18, 0.505, 114.0, -220, 20, -120, 120), (3, 36, 0.495, 180.0, -280, 20, -160, 160)]
    can = ROOT.TCanvas("c_eldc", "c_eldc", 1600, 900)
    can.Divide(6, 3)
    keep = []
    for irow, (reg, ly, a, b, xmin, xmax, ymin, ymax) in enumerate(layers):
        for sec in range(1, 7):
            pad = can.cd(irow * 6 + sec)
            pad.SetRightMargin(0.12)
            hist = root_file.Get("h_ele_dc_r%d_s%d" % (reg, sec))
            if not hist:
                print("SKIP h_ele_dc_r%d_s%d" % (reg, sec))
                continue
            hist.SetTitle("R%d S%d;x_{rot} [cm];y_{rot} [cm]" % (reg, sec))
            hist.GetXaxis().SetRangeUser(xmin, xmax)
            hist.GetYaxis().SetRangeUser(ymin, ymax)
            hist.Draw("colz")
            keep.append(hist)
            n = 50
            g1 = ROOT.TGraph(n)
            g2 = ROOT.TGraph(n)
            for j in range(n):
                x = xmin + (xmax - xmin) * j / (n - 1)
                yb = a * (x + b)
                g1.SetPoint(j, x, yb)
                g2.SetPoint(j, x, -yb)
            for g in (g1, g2):
                g.SetLineColor(ROOT.kRed)
                g.SetLineWidth(2)
                g.Draw("L same")
                keep.append(g)
    can.keep = keep
    return save(can, outdir, "electron_DC_rotated.pdf")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", default="Chapter3_Figures/Chapter3_HIPO_hists_combined.root")
    parser.add_argument("--out", default="Chapter3_Figures/plots")
    args = parser.parse_args()
    if not os.path.isfile(args.root):
        raise SystemExit("Missing combined ROOT file: %s" % args.root)
    root_file = ROOT.TFile.Open(args.root, "READ")
    if not root_file or root_file.IsZombie():
        raise SystemExit("Failed to open %s" % args.root)
    written = []
    for fn in (plot_htcc, plot_pcal, plot_sftot, plot_beta, plot_electron_dc):
        path = fn(root_file, args.out)
        if path:
            written.append(path)
    print("Done. %d PDFs in %s" % (len(written), args.out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
