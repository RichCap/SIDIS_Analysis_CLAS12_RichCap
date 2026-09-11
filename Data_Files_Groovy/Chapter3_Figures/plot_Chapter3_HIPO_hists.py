#!/usr/bin/env python3
# Render Chapter 3 PID/fiducial figures from the combined HIPO TTree ROOT file.
# Usage (from Chapter3_Figures, after hadd):
#     python plot_Chapter3_HIPO_hists.py \
#         -r Chapter3_HIPO_hists_combined.root \
#         -o Plot_Images
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

# Optional cuts applied at plot time from the h22 TTree.
# Pion/hadron branch names depend on row kind (1 = e-pi+ pair, 2 = positive hadron).
CUT_CLAUSES = {
    "pip_fd":       {"pair": "(pip_status >= 2000) && (pip_status < 4000)",
                     "had":  "(had_status >= 2000) && (had_status < 4000)"},
    "chi2pid":      {"pair": "abs(pip_chi2pid) < 3",
                     "had":  "abs(had_chi2pid) < 3"},
    "el_dc":        {"pair": "(e_edge1 > 5.0) && (e_edge2 > 5.0) && (e_edge3 > 10.0)",
                     "had":  "(e_edge1 > 5.0) && (e_edge2 > 5.0) && (e_edge3 > 10.0)"},
    "pip_dc":       {"pair": "(p_edge1 > 2.5) && (p_edge2 > 2.5) && (p_edge3 > 9.0)",
                     "had":  "(h_edge1 > 2.5) && (h_edge2 > 2.5) && (h_edge3 > 9.0)"},
    "el_vz":        {"pair": "(vz > -8.0) && (vz < 2.0)",
                     "had":  "(vz > -8.0) && (vz < 2.0)"},
    "pcal_emin":    {"pair": "pcal_energy > 0.06",
                     "had":  "pcal_energy > 0.06"},
    "all_electron": {"pair": "all_electron == 1",
                     "had":  "all_electron == 1"},
}
PION_CUTS = ["pip_fd", "chi2pid", "pip_dc"]
NAMED_CONFIGS = [
    ("none",            []),
    ("el_dc",           ["el_dc"]),
    ("pip_dc",          ["pip_dc"]),
    ("el_pip_dc",       ["el_dc", "pip_dc"]),
    ("pip_fd",          ["pip_fd"]),
    ("chi2pid",         ["chi2pid"]),
    ("el_vz",           ["el_vz"]),
    ("pcal_emin",       ["pcal_emin"]),
    ("all_cuts",        ["pip_fd", "chi2pid", "el_dc", "pip_dc", "el_vz", "pcal_emin"]),
    ("all_electron",    ["all_electron"]),
    ("all_electron_FD", ["all_electron", "pip_fd"]),
]
PLOT_CONFIGS = NAMED_CONFIGS
NAMED_CONFIG_MAP = dict(NAMED_CONFIGS)
DEFAULT_CONFIGS = ["none", "all_electron"]
CHI2PID_C = 0.88
DVZ_MID = 20.0


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


def uses_pion_cut(cut_names):
    for name in cut_names:
        if(name in PION_CUTS):
            return True
    return False


def cut_filter(cut_names, row_kind):
    if(row_kind in [2]):
        which = "had"
    else:
        which = "pair"
    clauses = ["(kind == %d)" % row_kind]
    for name in cut_names:
        if(name not in CUT_CLAUSES):
            raise ValueError("Unknown cut name: %s" % name)
        clauses.append("(%s)" % CUT_CLAUSES[name][which])
    return " && ".join(clauses)


def rdf_has(rdf, col):
    try:
        return bool(rdf.HasColumn(col))
    except Exception:
        return False


def fill_histograms(root_path, cut_names):
    if(uses_pion_cut(cut_names)):
        ele_kind = 1
    else:
        ele_kind = 0
    ele_cut = cut_filter(cut_names, ele_kind)
    had_cut = cut_filter(cut_names, 2)
    pip_cut = cut_filter(cut_names, 1)
    print("electron kind %d filter [%s]" % (ele_kind, ele_cut))
    print("hadron filter [%s]" % had_cut)

    rdf_ele = ROOT.RDataFrame("h22", root_path).Filter(ele_cut)
    rdf_had = ROOT.RDataFrame("h22", root_path).Filter(had_cut)
    rdf_pip = ROOT.RDataFrame("h22", root_path).Filter(pip_cut)

    h_htcc = ptr(rdf_ele.Histo1D(("h_htcc_nphe",   "Electron HTCC N_{phe};N_{phe};Counts",           150, 0.0, 75.0), "nphe"))
    h_pcal = ptr(rdf_ele.Histo1D(("h_pcal_energy", "Electron PCAL energy;E_{PCAL} [GeV];Counts",     120, 0.0,  1.2), "pcal_energy"))
    h_beta = ptr(rdf_had.Histo2D(("h_beta_poshad", "Positive hadrons;p [GeV];#beta", 120, 0.0, 8.0, 120, 0.4, 1.2), "had_p", "had_beta"))
    h_vz   = ptr(rdf_ele.Histo1D(("h_ele_vz", "Electron v_{z};v_{z} [cm];Counts", 120, -20.0, 10.0), "vz"))
    h_e_edge = [
        ptr(rdf_ele.Histo1D(("h_e_edge1", "Electron DC edge R1;edge [cm];Counts", 120, -5.0, 40.0), "e_edge1")),
        ptr(rdf_ele.Histo1D(("h_e_edge2", "Electron DC edge R2;edge [cm];Counts", 120, -5.0, 40.0), "e_edge2")),
        ptr(rdf_ele.Histo1D(("h_e_edge3", "Electron DC edge R3;edge [cm];Counts", 120, -5.0, 40.0), "e_edge3")),
    ]
    h_p_edge = [
        ptr(rdf_pip.Histo1D(("h_p_edge1", "Pion DC edge R1;edge [cm];Counts", 120, -5.0, 40.0), "p_edge1")),
        ptr(rdf_pip.Histo1D(("h_p_edge2", "Pion DC edge R2;edge [cm];Counts", 120, -5.0, 40.0), "p_edge2")),
        ptr(rdf_pip.Histo1D(("h_p_edge3", "Pion DC edge R3;edge [cm];Counts", 120, -5.0, 40.0), "p_edge3")),
    ]
    h_pip_chi2 = None
    if(rdf_has(rdf_pip, "pip_p")):
        h_pip_chi2 = ptr(rdf_pip.Histo2D(("h_pip_chi2pid", "Pion #chi^{2}_{PID};p_{#pi^{+}} [GeV];#chi^{2}_{PID}", 120, 0.0, 8.0, 120, -8.0, 8.0), "pip_p", "pip_chi2pid"))
    h_dvz = None
    if(rdf_has(rdf_pip, "dvz")):
        h_dvz = ptr(rdf_pip.Histo1D(("h_dvz", "Electron-pion #Delta v_{z};#Delta v_{z} [cm];Counts", 120, -40.0, 40.0), "dvz"))
    h_hxhy = None
    if(rdf_has(rdf_ele, "Hx") and rdf_has(rdf_ele, "Hy")):
        h_hxhy = ptr(rdf_ele.Histo2D(("h_pcal_hxhy", "PCAL occupancy;H_{x} [cm];H_{y} [cm]", 120, -400, 400, 120, -400, 400), "Hx", "Hy"))
    h_vw = None
    if(rdf_has(rdf_ele, "V_PCal") and rdf_has(rdf_ele, "W_PCal")):
        h_vw = ptr(rdf_ele.Histo2D(("h_pcal_vw", "PCAL V-W;V [cm];W [cm]", 120, 0, 450, 120, 0, 450), "V_PCal", "W_PCal"))

    h_sftot = {}
    h_dc    = {}
    dc_weight = "el_chi2pid" if(rdf_has(rdf_ele, "el_chi2pid")) else None
    for sec in range(1, 7):
        rdf_sec = rdf_ele.Filter("esec == %d" % sec)
        h_sftot[sec] = ptr(rdf_sec.Histo2D(
            ("h_sftot_sec%d" % sec, "Sector %d;p_{e} [GeV];SF_{tot}" % sec, 450, 1.0, 10.0, 500, 0.0, 0.50),
            "el_p", "sftot"
        ))
        dc_args_1 = (("h_ele_dc_r1_s%d" % sec, "R1 S%d;x_{rot} [cm];y_{rot} [cm]" % sec, 80, -160, 20, 80, -90, 90), "xrot1", "yrot1")
        dc_args_2 = (("h_ele_dc_r2_s%d" % sec, "R2 S%d;x_{rot} [cm];y_{rot} [cm]" % sec, 80, -220, 20, 80, -120, 120), "xrot2", "yrot2")
        dc_args_3 = (("h_ele_dc_r3_s%d" % sec, "R3 S%d;x_{rot} [cm];y_{rot} [cm]" % sec, 80, -280, 20, 80, -160, 160), "xrot3", "yrot3")
        if(dc_weight is not None):
            h_dc[(1, sec)] = ptr(rdf_sec.Histo2D(dc_args_1[0], dc_args_1[1], dc_args_1[2], dc_weight))
            h_dc[(2, sec)] = ptr(rdf_sec.Histo2D(dc_args_2[0], dc_args_2[1], dc_args_2[2], dc_weight))
            h_dc[(3, sec)] = ptr(rdf_sec.Histo2D(dc_args_3[0], dc_args_3[1], dc_args_3[2], dc_weight))
        else:
            h_dc[(1, sec)] = ptr(rdf_sec.Histo2D(dc_args_1[0], dc_args_1[1], dc_args_1[2]))
            h_dc[(2, sec)] = ptr(rdf_sec.Histo2D(dc_args_2[0], dc_args_2[1], dc_args_2[2]))
            h_dc[(3, sec)] = ptr(rdf_sec.Histo2D(dc_args_3[0], dc_args_3[1], dc_args_3[2]))
    return {
        "htcc": h_htcc, "pcal": h_pcal, "sftot": h_sftot, "beta": h_beta, "dc": h_dc,
        "vz": h_vz, "e_edge": h_e_edge, "p_edge": h_p_edge, "pip_chi2": h_pip_chi2,
        "dvz": h_dvz, "hxhy": h_hxhy, "vw": h_vw,
    }


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
    legend = ROOT.TLegend(0.62, 0.18, 0.88, 0.38)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    labels = {M_PI: "#pi^{+}", M_K: "Kaon", M_P: "Proton"}
    for mass, col in ((M_PI, ROOT.kRed), (M_K, ROOT.kGreen + 2), (M_P, ROOT.kMagenta)):
        gr = ROOT.TGraph(n)
        for i in range(n):
            p = 0.2 + (7.5 - 0.2) * i / (n - 1)
            gr.SetPoint(i, p, beta_mass(p, mass))
        gr.SetLineColor(col)
        gr.SetLineWidth(2)
        gr.Draw("L same")
        legend.AddEntry(gr, labels[mass], "l")
        keep.append(gr)
    legend.Draw()
    keep.append(legend)
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


def plot_1d_cut(hist, outdir, name, title, lines):
    if(not hist):
        print("SKIP", name)
        return None
    can = ROOT.TCanvas("c_" + name, "c_" + name, 700, 500)
    hist.SetTitle(title)
    hist.Draw("hist")
    apply_grid()
    ymax = hist.GetMaximum() * 1.05
    if(ymax <= 0):
        ymax = 1.0
    keep = [hist]
    for xcut in lines:
        line = ROOT.TLine(xcut, 0.0, xcut, ymax)
        line.SetLineColor(ROOT.kRed)
        line.SetLineWidth(2)
        line.Draw("same")
        keep.append(line)
    can.keep = keep
    return save(can, outdir, name)


def plot_edge_row(hists, outdir, name, titles, cuts):
    if(not hists or any(h is None for h in hists)):
        print("SKIP", name)
        return None
    can = ROOT.TCanvas("c_" + name, "c_" + name, 1400, 450)
    can.Divide(3, 1)
    keep = []
    for i, (hist, title, cut) in enumerate(zip(hists, titles, cuts), start=1):
        pad = can.cd(i)
        hist.SetTitle(title)
        hist.Draw("hist")
        apply_grid(pad)
        ymax = hist.GetMaximum() * 1.05
        if(ymax <= 0):
            ymax = 1.0
        line = ROOT.TLine(cut, 0.0, cut, ymax)
        line.SetLineColor(ROOT.kRed)
        line.SetLineWidth(2)
        line.Draw("same")
        keep.extend([hist, line])
    can.keep = keep
    return save(can, outdir, name)


def pip_chi2_high(p):
    if(p < 2.44):
        return 3.0 * CHI2PID_C
    return CHI2PID_C * (0.00869 + 14.98587 * math.exp(-p / 1.18236) + 1.81751 * math.exp(-p / 4.86394))


def plot_pip_chi2(hist, outdir):
    if(not hist):
        print("SKIP pip_chi2pid.pdf")
        return None
    can = ROOT.TCanvas("c_pipchi2", "c_pipchi2", 800, 650)
    hist.SetTitle("Pion #chi^{2}_{PID} vs p;p_{#pi^{+}} [GeV];#chi^{2}_{PID}")
    apply_grid()
    ROOT.gPad.SetLogz(1)
    hist.Draw("colz")
    keep = [hist]
    n = 80
    g_lo = ROOT.TGraph(n)
    g_hi = ROOT.TGraph(n)
    for i in range(n):
        p = 0.2 + (7.5 - 0.2) * i / (n - 1)
        g_lo.SetPoint(i, p, -3.0 * CHI2PID_C)
        g_hi.SetPoint(i, p, pip_chi2_high(p))
    for g in (g_lo, g_hi):
        g.SetLineColor(ROOT.kRed)
        g.SetLineWidth(2)
        g.Draw("L same")
        keep.append(g)
    can.keep = keep
    return save(can, outdir, "pip_chi2pid.pdf")


def plot_colz(hist, outdir, name, title, overlays=None):
    if(not hist):
        print("SKIP", name)
        return None
    can = ROOT.TCanvas("c_" + name, "c_" + name, 800, 700)
    hist.SetTitle(title)
    apply_grid()
    ROOT.gPad.SetLogz(1)
    hist.Draw("colz")
    keep = [hist]
    if(overlays):
        for item in overlays:
            item.SetLineColor(ROOT.kRed)
            item.SetLineWidth(2)
            item.Draw("L same")
            keep.append(item)
    can.keep = keep
    return save(can, outdir, name)


def plot_one_config(root_path, outdir, cut_names):
    h = fill_histograms(root_path, cut_names)
    written = []
    for path in (
        plot_htcc(h["htcc"], outdir),
        plot_pcal(h["pcal"], outdir),
        plot_sftot(h["sftot"], outdir),
        plot_beta(h["beta"], outdir),
        plot_electron_dc(h["dc"], outdir),
        plot_1d_cut(h["vz"], outdir, "electron_vz.pdf", "Electron v_{z};v_{z} [cm];Counts", [-8.0, 2.0]),
        plot_edge_row(h["e_edge"], outdir, "electron_DC_edge.pdf",
                      ["R1;edge [cm];Counts", "R2;edge [cm];Counts", "R3;edge [cm];Counts"], [5.0, 5.0, 10.0]),
        plot_pip_chi2(h["pip_chi2"], outdir),
        plot_1d_cut(h["dvz"], outdir, "delta_vz.pdf", "Electron-pion #Delta v_{z};#Delta v_{z} [cm];Counts", [-DVZ_MID, DVZ_MID]),
        plot_edge_row(h["p_edge"], outdir, "pion_DC_edge.pdf",
                      ["R1;edge [cm];Counts", "R2;edge [cm];Counts", "R3;edge [cm];Counts"], [2.5, 2.5, 9.0]),
        plot_colz(h["hxhy"], outdir, "PCAL_inefficient.pdf", "PCAL occupancy;H_{x} [cm];H_{y} [cm]"),
        plot_colz(h["vw"], outdir, "PCAL_VW.pdf", "PCAL V-W fiducial;V [cm];W [cm]",
                  [ROOT.TLine(14.0, 0.0, 14.0, 450.0), ROOT.TLine(0.0, 14.0, 450.0, 14.0)]),
    ):
        if(path):
            written.append(path)
    return written


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-r", "--root",
                        dest="root",
                        default="Chapter3_HIPO_hists_combined.root",
                        help="Input ROOT file with the Chapter 3 h22 TTree.")
    parser.add_argument("-o", "--out",
                        dest="out",
                        default="Plot_Images",
                        help="Output directory where the plots will be saved.")
    parser.add_argument("-c", "--config",
                        dest="config",
                        nargs="+",
                        default=["none", "all_electron"],
                        choices=["none", "el_dc", "pip_dc", "el_pip_dc", "pip_fd", "chi2pid", "el_vz", "pcal_emin", "all_cuts", "all_electron", "all_electron_FD", "all"],
                        help="Named plot-time cut configurations (one or more). Default: none all_electron. 'all' runs every named config except the meta-option itself. The old combined set is now 'all_cuts'.")
    args = parser.parse_args()
    if(not os.path.isfile(args.root)):
        raise SystemExit("Missing combined ROOT file: %s" % args.root)
    if("all" in args.config):
        selected = [name for name, _cuts in NAMED_CONFIGS]
    else:
        selected = list(args.config)
    written = []
    ROOT.gROOT.SetMustClean(False)
    for name in selected:
        cuts = NAMED_CONFIG_MAP[name]
        outdir = os.path.join(args.out, name)
        print("=== %s -> %s" % (name, outdir))
        written.extend(plot_one_config(args.root, outdir, cuts))
    print("Done. %d PDFs" % len(written))
    return 0


if(__name__ == "__main__"):
    sys.exit(main())
