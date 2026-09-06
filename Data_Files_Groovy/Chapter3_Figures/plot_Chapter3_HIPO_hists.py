#!/usr/bin/env python3
# Render Chapter 3 PID/fiducial figures from the combined HIPO TTree ROOT file.
# Usage (from Chapter3_Figures, after hadd):
#     python plot_Chapter3_HIPO_hists.py \
#         -r Chapter3_HIPO_hists_combined.root \
#         -o Plot_Images
#     python plot_Chapter3_HIPO_hists.py -ci 0,4,8,12,63
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
M_K  = 0.493677
M_P  = 0.938272081

# Optional-cut bits (plot-time only). Thresholds live here, not in the HIPO TTrees.
# bit 0 (1):  pion FD status, 2000 <= status < 4000
# bit 1 (2):  abs(chi2pid) < 3   (simple diagnostic; not the nominal momentum-dependent cut)
# bit 2 (4):  electron DC edges, R1/R2 > 5.0 cm and R3 > 10.0 cm
# bit 3 (8):  pion/hadron DC edges, R1/R2 > 2.5 cm and R3 > 9.0 cm
# bit 4 (16): electron -8 < vz < 2 cm
# bit 5 (32): PCAL E > 0.06 GeV
BIT_PIP_FD     = 0
BIT_CHI2PID    = 1
BIT_EL_DC      = 2
BIT_PIP_DC     = 3
BIT_EL_VZ      = 4
BIT_PCAL_EMIN  = 5
PION_BITS      = (1 << BIT_PIP_FD) | (1 << BIT_CHI2PID) | (1 << BIT_PIP_DC)


def apply_grid(pad=None):
    if(pad is None):
        pad = ROOT.gPad
    if(pad is not None):
        pad.SetGrid(1, 1)


def sf_mean_sigma(p, isec):
    p2 = p * p
    mean  = P0MEAN[isec] * (1.0 + p / math.sqrt(p2 + P1MEAN[isec])) + P2MEAN[isec] * p + P3MEAN[isec] * p2
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


def ptr(hist):
    if(hasattr(hist, "GetPtr")):
        return hist.GetPtr()
    return hist


def cut_filter(cut_index, kind):
    # AND of the optional cuts whose bits are set in cut_index.
    # kind is 'ele', 'elepip', or 'had' (selects pion vs hadron branch names).
    idx = int(cut_index)
    if((idx < 0) or (idx > 63)):
        raise ValueError("cut_index must be 0-63, got %s" % cut_index)
    clauses = []
    if(kind in ["had"]):
        status_br = "had_status"
        chi2_br   = "had_chi2pid"
        p_e1, p_e2, p_e3 = "h_edge1", "h_edge2", "h_edge3"
    else:
        status_br = "pip_status"
        chi2_br   = "pip_chi2pid"
        p_e1, p_e2, p_e3 = "p_edge1", "p_edge2", "p_edge3"
    if(idx & (1 << BIT_PIP_FD)):
        clauses.append("(%s >= 2000) && (%s < 4000)" % (status_br, status_br))
    if(idx & (1 << BIT_CHI2PID)):
        clauses.append("abs(%s) < 3" % chi2_br)
    if(idx & (1 << BIT_EL_DC)):
        clauses.append("(e_edge1 > 5.0) && (e_edge2 > 5.0) && (e_edge3 > 10.0)")
    if(idx & (1 << BIT_PIP_DC)):
        clauses.append("(%s > 2.5) && (%s > 2.5) && (%s > 9.0)" % (p_e1, p_e2, p_e3))
    if(idx & (1 << BIT_EL_VZ)):
        clauses.append("(vz > -8.0) && (vz < 2.0)")
    if(idx & (1 << BIT_PCAL_EMIN)):
        clauses.append("pcal_energy > 0.06")
    if(len(clauses) == 0):
        return "1"
    return " && ".join(clauses)


def electron_tree_name(cut_index):
    if(int(cut_index) & PION_BITS):
        return "elepip"
    return "ele"


def parse_cut_indices(values):
    out = []
    if(values is None):
        return [0]
    for item in values:
        for piece in str(item).split(","):
            piece = piece.strip()
            if(piece in [""]):
                continue
            idx = int(piece)
            if((idx < 0) or (idx > 63)):
                raise ValueError("cut_index must be 0-63, got %s" % piece)
            if(idx not in out):
                out.append(idx)
    if(len(out) == 0):
        out = [0]
    return out


def fill_histograms(root_path, cut_index):
    ele_tree = electron_tree_name(cut_index)
    ele_cut  = cut_filter(cut_index, ele_tree)
    had_cut  = cut_filter(cut_index, "had")
    print("cut_index %d: electron tree %s filter [%s]" % (cut_index, ele_tree, ele_cut))
    print("cut_index %d: had tree filter [%s]" % (cut_index, had_cut))

    rdf_ele = ROOT.RDataFrame(ele_tree, root_path).Filter(ele_cut)
    rdf_had = ROOT.RDataFrame("had",    root_path).Filter(had_cut)

    h_htcc = ptr(rdf_ele.Histo1D(("h_htcc_nphe",   "Electron HTCC N_{phe};N_{phe};Counts",           150, 0.0, 75.0), "nphe"))
    h_pcal = ptr(rdf_ele.Histo1D(("h_pcal_energy", "Electron PCAL energy;E_{PCAL} [GeV];Counts",     120, 0.0,  1.2), "pcal_energy"))
    h_beta = ptr(rdf_had.Histo2D(("h_beta_poshad", "Positive hadrons;p [GeV];#beta", 120, 0.0, 8.0, 120, 0.4, 1.2), "had_p", "had_beta"))

    h_sftot = {}
    h_dc    = {}
    for sec in range(1, 7):
        rdf_sec = rdf_ele.Filter("esec == %d" % sec)
        h_sftot[sec] = ptr(rdf_sec.Histo2D(
            ("h_sftot_sec%d" % sec, "Sector %d;p_{e} [GeV];SF_{tot}" % sec, 450, 1.0, 10.0, 500, 0.0, 0.50),
            "el_p", "sftot"
        ))
        h_dc[(1, sec)] = ptr(rdf_sec.Histo2D(
            ("h_ele_dc_r1_s%d" % sec, "R1 S%d;x_{rot} [cm];y_{rot} [cm]" % sec, 80, -160, 20, 80, -90, 90),
            "xrot1", "yrot1"
        ))
        h_dc[(2, sec)] = ptr(rdf_sec.Histo2D(
            ("h_ele_dc_r2_s%d" % sec, "R2 S%d;x_{rot} [cm];y_{rot} [cm]" % sec, 80, -220, 20, 80, -120, 120),
            "xrot2", "yrot2"
        ))
        h_dc[(3, sec)] = ptr(rdf_sec.Histo2D(
            ("h_ele_dc_r3_s%d" % sec, "R3 S%d;x_{rot} [cm];y_{rot} [cm]" % sec, 80, -280, 20, 80, -160, 160),
            "xrot3", "yrot3"
        ))
    return h_htcc, h_pcal, h_sftot, h_beta, h_dc


def plot_htcc(hist, outdir):
    if(not hist):
        print("SKIP h_htcc_nphe")
        return None
    can = ROOT.TCanvas("c_htcc", "c_htcc", 700, 500)
    hist.SetTitle("HTCC photoelectron multiplicity;N_{phe}^{HTCC};Counts")
    hist.Draw("hist")
    apply_grid()
    ymax = hist.GetMaximum() * 1.05
    if(ymax <= 0):
        ymax = 1.0
    line = ROOT.TLine(2.0, 0.0, 2.0, ymax)
    line.SetLineColor(ROOT.kRed)
    line.SetLineWidth(2)
    line.Draw("same")
    can.keep = [hist, line]
    return save(can, outdir, "HTCC_Nphe.pdf")


def plot_pcal(hist, outdir):
    if(not hist):
        print("SKIP h_pcal_energy")
        return None
    can = ROOT.TCanvas("c_pcal", "c_pcal", 700, 500)
    hist.SetTitle(";E_{PCAL} [GeV];Counts")
    hist.Draw("hist")
    apply_grid()
    ymax = hist.GetMaximum() * 1.05
    if(ymax <= 0):
        ymax = 1.0
    line = ROOT.TLine(0.06, 0.0, 0.06, ymax)
    line.SetLineColor(ROOT.kRed)
    line.SetLineWidth(2)
    line.Draw("same")
    can.keep = [hist, line]
    return save(can, outdir, "PCAL_Emin.pdf")


def plot_sftot(h_sftot, outdir):
    can = ROOT.TCanvas("c_sftot", "c_sftot", 1400, 900)
    can.Divide(3, 2)
    keep = []
    pmin, pmax, ncurve = 2.0, 9.0, 140
    for sec in range(1, 7):
        pad = can.cd(sec)
        pad.SetRightMargin(0.12)
        pad.SetLeftMargin(0.12)
        hist = h_sftot.get(sec)
        if(not hist):
            print("SKIP h_sftot_sec%d" % sec)
            continue
        hist.SetTitle("#scale[1.5]{Sector %d};p_{el} [GeV];SF_{tot}" % sec)
        hist.GetXaxis().SetRangeUser(pmin, pmax)
        hist.GetYaxis().SetRangeUser(0, 0.4)
        ROOT.gPad.SetLogz(1)
        apply_grid()
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


def plot_beta(hist, outdir):
    if(not hist):
        print("SKIP h_beta_poshad")
        return None
    can = ROOT.TCanvas("c_beta", "c_beta", 800, 650)
    hist.SetTitle("#scale[1.15]{Positive hadrons #beta vs p};p [GeV];#beta")
    apply_grid()
    ROOT.gPad.SetLogz(1)
    hist.Draw("colz")
    keep = [hist]
    n = 80
    for mass, col in ((M_PI, ROOT.kRed), (M_K, ROOT.kGreen + 2), (M_P, ROOT.kMagenta)):
        gr = ROOT.TGraph(n)
        for i in range(n):
            p = 0.2 + (7.5 - 0.2) * i / (n - 1)
            gr.SetPoint(i, p, beta_mass(p, mass))
        gr.SetLineColor(col)
        gr.SetLineWidth(1)
        gr.Draw("L same")
        keep.append(gr)
    can.keep = keep
    return save(can, outdir, "Beta_PID.pdf")


def plot_electron_dc(h_dc, outdir):
    layers = [(1, 6, 0.50, 72.0, -90, 20, -90, 90), (2, 18, 0.505, 114.0, -130, 20, -120, 120), (3, 36, 0.495, 180.0, -220, 20, -160, 160)]
    can = ROOT.TCanvas("c_eldc", "c_eldc", 1600, 900)
    can.Divide(6, 3)
    keep = []
    for irow, (reg, ly, a, b, xmin, xmax, ymin, ymax) in enumerate(layers):
        for sec in range(1, 7):
            pad = can.cd(irow * 6 + sec)
            pad.SetRightMargin(0.12)
            pad.SetLeftMargin(0.12)
            hist = h_dc.get((reg, sec))
            if(not hist):
                print("SKIP h_ele_dc_r%d_s%d" % (reg, sec))
                continue
            hist.SetTitle("#scale[1.5]{R%d #topbar Sector %d};#scale[1.25]{x_{rot} [cm]};#scale[1.25]{y_{rot} [cm]}" % (reg, sec))
            hist.GetXaxis().SetRangeUser(xmin, xmax)
            hist.GetYaxis().SetRangeUser(ymin, ymax)
            ROOT.gPad.SetLogz(1)
            apply_grid()
            hist.Draw("colz")
            keep.append(hist)
            x_int = -b
            y_hi  = a * (xmax + b)
            y_lo  = -y_hi
            g1 = ROOT.TGraph(2)
            g2 = ROOT.TGraph(2)
            g1.SetPoint(0, x_int, 0.0)
            g1.SetPoint(1, xmax, y_hi)
            g2.SetPoint(0, x_int, 0.0)
            g2.SetPoint(1, xmax, y_lo)
            for g in (g1, g2):
                g.SetLineColor(ROOT.kRed)
                g.SetLineWidth(2)
                g.Draw("L same")
                keep.append(g)
    can.keep = keep
    return save(can, outdir, "electron_DC_rotated.pdf")


def plot_one_index(root_path, outdir, cut_index):
    h_htcc, h_pcal, h_sftot, h_beta, h_dc = fill_histograms(root_path, cut_index)
    written = []
    path = plot_htcc(h_htcc, outdir)
    if(path): written.append(path)
    path = plot_pcal(h_pcal, outdir)
    if(path): written.append(path)
    path = plot_sftot(h_sftot, outdir)
    if(path): written.append(path)
    path = plot_beta(h_beta, outdir)
    if(path): written.append(path)
    path = plot_electron_dc(h_dc, outdir)
    if(path): written.append(path)
    return written


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-r", "--root",
                        dest="root",
                        default="Chapter3_HIPO_hists_combined.root",
                        help="Input ROOT file with Chapter 3 TTrees (ele, elepip, had).")
    parser.add_argument("-o", "--out",
                        dest="out",
                        default="Plot_Images",
                        help="Output directory where the plots will be saved.")
    parser.add_argument("-ci", "--cut_index",
                        dest="cut_index",
                        action="append",
                        default=None,
                        help="Optional-cut index 0-63 (repeat or comma-separate). Default: 0.")
    args = parser.parse_args()
    if(not os.path.isfile(args.root)):
        raise SystemExit("Missing combined ROOT file: %s" % args.root)
    indices = parse_cut_indices(args.cut_index)
    written = []
    ROOT.gROOT.SetMustClean(False)
    for idx in indices:
        outdir = os.path.join(args.out, "cut_index_%02d" % idx)
        print("=== cut_index %d -> %s" % (idx, outdir))
        written.extend(plot_one_index(args.root, outdir, idx))
    print("Done. %d PDFs" % len(written))
    return 0


if(__name__ == "__main__"):
    sys.exit(main())
