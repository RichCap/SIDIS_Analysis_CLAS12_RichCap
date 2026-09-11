#!/usr/bin/env python3
# Chapter 3 1D kinematic cut-demonstration from Groovy-converted ntuples.
# Isolated from DataFrame Snapshot production. Does not define cut_Complete_SIDIS.
#
# Architecture:
#     converted *.hipo.root ntuple(s) -> histogram ROOT file(s) -> optional hadd -> PDF plotting
#
# Usage (from Histo_Files_ROOT/DataFrames):
#     python Chapter3_Kinematic_Cut_Figures.py --data_root work
#     python Chapter3_Kinematic_Cut_Figures.py --data_root work_b
#     python Chapter3_Kinematic_Cut_Figures.py -f /path/to/one.hipo.root --hists Chapter3_Kinematic_Cut_hists_<id>.root
#     python Chapter3_Kinematic_Cut_Figures.py --plot Chapter3_Kinematic_Cut_hists_all.root --out Chapter3_Kinematic_Cut_Plots
from __future__ import print_function

import argparse
import glob
import os
import sys

import ROOT

_BOOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if(_BOOT not in sys.path):
    sys.path.insert(0, _BOOT)
from jlab_work_paths import add_data_root_argument, bootstrap_from_file, print_path_summary
EXEC_ROOT = bootstrap_from_file(__file__)
from ExtraAnalysisCodeValues import (
    Correction_Code_Full_In, Default_MM_Cut, Pion_Energy_Loss_Cor_Function, Rotation_Matrix,
    Sangbaek_and_Valerii_Fiducial_Cuts, Sector_Fiducial_PCal_Cuts, Valerii_Fiducial_PCal_Volume_Cuts,
    filter_Valerii,
)
from MyCommonAnalysisFunction_richcap import color
from Pion_Test_Fiducial_Cuts_Defs import Apply_Test_Fiducial_Cuts
from Chapter3_DataFrame_Figures import KIN_PLOTS
from Chapter3_Pion_DC_Polygon_Plots import expand

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

DEFAULT_INPUT_GLOB = "/w/hallb-scshelf2102/clas12/richcap/SIDIS/REAL_Data/Pass2/More_Cut_Info/Data_sidis_epip_richcap.inb.qa.new10.nSidis_005*"
DEFAULT_OUT_DIR = os.path.join(EXEC_ROOT, "Histo_Files_ROOT", "DataFrames", "Chapter3_Kinematic_Cut_Plots")
BEAM_ENERGY = 10.6041
DPPC_RDF_PASS2 = "3"

NTUPLE_REQUIRED = [
    "ex", "ey", "ez", "pipx", "pipy", "pipz", "esec", "pipsec",
    "Hx", "Hy", "V_PCal", "W_PCal", "U_PCal",
    "ele_x_DC_6", "ele_y_DC_6", "ele_z_DC_6",
    "ele_x_DC_18", "ele_y_DC_18", "ele_z_DC_18",
    "ele_x_DC_36", "ele_y_DC_36", "ele_z_DC_36",
    "pip_x_DC_6", "pip_y_DC_6", "pip_z_DC_6",
    "pip_x_DC_18", "pip_y_DC_18", "pip_z_DC_18",
    "pip_x_DC_36", "pip_y_DC_36", "pip_z_DC_36",
    "CHI2PID_CUT_mid_pip",
    "DC_FIDUCIAL_REG1_mid_el", "DC_FIDUCIAL_REG2_mid_el", "DC_FIDUCIAL_REG3_mid_el",
    "DC_FIDUCIAL_REG1_mid_pip", "DC_FIDUCIAL_REG2_mid_pip", "DC_FIDUCIAL_REG3_mid_pip",
    "DC_VERTEX_mid_el", "DELTA_VZ_mid_pip",
    "EC_OUTER_VS_INNER_mid_el", "EC_SAMPLING_BAND_mid_el",
    "EC_SAMPLING_THRESHOLD_mid_el", "EC_SAMPLING_TRIANGLE_mid_el",
]

# Local copies of production PID_Default / NonPID_Default from ExtraAnalysisCodeValues.Define_Cut_Variations_With_Smeared_Kinematics.
# Script-only: do not Define cut_Complete_SIDIS.
PID_DEFAULT = " && ".join([
    "(CHI2PID_CUT_mid_pip == 1)",
    "(DC_FIDUCIAL_REG1_mid_el   == 1) && (DC_FIDUCIAL_REG2_mid_el   == 1) && (DC_FIDUCIAL_REG3_mid_el   == 1)",
    "(DC_FIDUCIAL_REG1_mid_pip   == 1) && (DC_FIDUCIAL_REG2_mid_pip   == 1) && (DC_FIDUCIAL_REG3_mid_pip   == 1)",
    "(DC_VERTEX_mid_el   == 1)",
    "(DELTA_VZ_mid_pip   == 1)",
    "(EC_OUTER_VS_INNER_mid_el   == 1)",
    "(EC_SAMPLING_BAND_mid_el   == 1)",
    "(EC_SAMPLING_THRESHOLD_mid_el   == 1)",
    "(EC_SAMPLING_TRIANGLE_mid_el   == 1)",
])
NONPID_DEFAULT = " && ".join([
    "(valerii_PCAL_knockout_cut)",
    "(Valerii_PCal_Fiducial_Cuts)",
    "(Sector_PCal_Fiducial_Cuts)",
    "(Valerii_DC_Fiducial_Cuts_ele_DC_6) && (Valerii_DC_Fiducial_Cuts_ele_DC_18) && (Valerii_DC_Fiducial_Cuts_ele_DC_36)",
    "(My_pip_DC_Fiducial_Cuts_Layer_6) && (My_pip_DC_Fiducial_Cuts_Layer_18) && (My_pip_DC_Fiducial_Cuts_Layer_36)",
])
CUT_COMPLETE_NO_KINEMATICS = "(%s) && (%s)" % (PID_DEFAULT, NONPID_DEFAULT)

# Production KinCuts_Unsm_base plus MM as sqrt(MM2) > Default_MM_Cut.
KIN_CLAUSES = [
    ("W",     "(W > 2)"),
    ("Q2",    "(Q2 > 2)"),
    ("pip",   "(pip > 1.25) && (pip < 5)"),
    ("pipth", "(5 < pipth) && (pipth < 35)"),
    ("elth",  "(5 < elth) && (elth < 35)"),
    ("y",     "(y < 0.75)"),
    ("xF",    "(xF > 0)"),
    ("MM",    "(sqrt(MM2) > %s)" % Default_MM_Cut),
]
INVERT_CLAUSE = {
    "Q2":    "(Q2 <= 2)",
    "pip":   "((pip <= 1.25) || (pip >= 5))",
    "pipth": "((pipth <= 5) || (pipth >= 35))",
    "elth":  "((elth <= 5) || (elth >= 35))",
    "y":     "(y >= 0.75)",
    "xF":    "(xF <= 0)",
    "MM":    "(sqrt(MM2) <= %s)" % Default_MM_Cut,
}


def ptr(hist):
    if(hasattr(hist, "GetPtr")):
        return hist.GetPtr()
    return hist


def rdf_has(df, col):
    try:
        return bool(df.HasColumn(col))
    except Exception:
        return str(col) in [str(name) for name in df.GetColumnNames()]


def declare_cpp(code, label):
    try:
        ROOT.gInterpreter.Declare(code)
        print("Declared %s" % label)
    except Exception as exc:
        print("Declare %s skipped (%s)" % (label, exc))


def missing_columns(df, needed):
    return [name for name in needed if(not rdf_has(df, name))]


def omit_one_filter(omit_key):
    parts = [CUT_COMPLETE_NO_KINEMATICS]
    for key, expr in KIN_CLAUSES:
        if(key == omit_key):
            continue
        parts.append(expr)
    return " && ".join(parts)


def no_kin_filter():
    return CUT_COMPLETE_NO_KINEMATICS


def hist_name(omit_key, no_kin):
    if(no_kin):
        return "h_%s_no_kin" % omit_key
    return "h_%s" % omit_key


def pdf_name(fname, no_kin):
    if(no_kin):
        return fname.replace(".pdf", "_no_kinematics.pdf")
    return fname


def default_hist_path(out_dir, files, explicit):
    if(explicit not in [None, ""]):
        if(os.path.dirname(explicit) in ["", "."]):
            return os.path.join(out_dir, os.path.basename(explicit))
        return explicit
    if(len(files) == 1):
        stem = os.path.basename(files[0])
        for suffix in [".hipo.root", ".root"]:
            if(stem.endswith(suffix)):
                stem = stem[:-len(suffix)]
                break
        return os.path.join(out_dir, "Chapter3_Kinematic_Cut_hists_%s.root" % stem)
    return os.path.join(out_dir, "Chapter3_Kinematic_Cut_hists.root")


def prepare_corrected_rdf(rdf):
    # rdf Pass-2 reconstructed quantities, matching dataframe_makeROOT_epip_SIDIS.py (~447-827).
    declare_cpp(Pion_Energy_Loss_Cor_Function, "Pion_Energy_Loss_Cor_Function")
    declare_cpp(Correction_Code_Full_In, "Correction_Code_Full_In")
    declare_cpp(Rotation_Matrix, "Rotation_Matrix")

    if("pipx" not in [str(name) for name in rdf.GetColumnNames()]):
        rdf = rdf.Define("pipx", "px")
    if("pipy" not in [str(name) for name in rdf.GetColumnNames()]):
        rdf = rdf.Define("pipy", "py")
    if("pipz" not in [str(name) for name in rdf.GetColumnNames()]):
        rdf = rdf.Define("pipz", "pz")

    print("%s\nApplying Pass 2 (Forward Detector) Energy Loss Corrections to the Pi+ Pion\n%s" % (color.BBLUE, color.END))
    rdf = rdf.Define("Energy_Loss_Cor_Factor", """
        double pip_mom                  =       sqrt(pipx*pipx + pipy*pipy + pipz*pipz);
        double pip__th                  = atan2(sqrt(pipx*pipx + pipy*pipy), pipz)*(180/3.1415926);
        auto p_pip_loss                 = eloss_pip_In_Forward(pip_mom, pip__th);
        auto pip_Energy_Loss_Cor_Factor = ((pip_mom + p_pip_loss)/pip_mom);
        return pip_Energy_Loss_Cor_Factor;
    """)
    for pion_mom in ["pipx", "pipy", "pipz"]:
        rdf = rdf.Redefine(str(pion_mom), "Energy_Loss_Cor_Factor*%s" % pion_mom)

    rdf = rdf.Define("el", "".join(["""
        auto fe     = dppC(ex, ey, ez, esec, 0, """, DPPC_RDF_PASS2, """) + 1;
        double el_P = fe*(sqrt(ex*ex + ey*ey + ez*ez));
        return el_P;"""]))
    rdf = rdf.Define("pip", "".join(["""
        auto fpip    = dppC(pipx, pipy, pipz, pipsec, 1, """, DPPC_RDF_PASS2, """) + 1;
        double pip_P = fpip*(sqrt(pipx*pipx + pipy*pipy + pipz*pipz));
        return pip_P;"""]))
    rdf = rdf.Define("elth", "atan2(sqrt(ex*ex + ey*ey), ez)*TMath::RadToDeg()")
    rdf = rdf.Define("pipth", "atan2(sqrt(pipx*pipx + pipy*pipy), pipz)*TMath::RadToDeg()")

    rdf = rdf.Define("vals", "".join(["""
        auto fe      = dppC(ex, ey, ez, esec, 0, """, DPPC_RDF_PASS2, """) + 1;
        auto fpip    = dppC(pipx, pipy, pipz, pipsec, 1, """, DPPC_RDF_PASS2, """) + 1;

        auto beam    = ROOT::Math::PxPyPzMVector(0, 0, """, str(BEAM_ENERGY), """, 0);
        auto targ    = ROOT::Math::PxPyPzMVector(0, 0, 0, 0.938272);

        auto ele     = ROOT::Math::PxPyPzMVector(ex*fe, ey*fe, ez*fe, 0);
        auto pip0    = ROOT::Math::PxPyPzMVector(pipx*fpip, pipy*fpip, pipz*fpip, 0.13957);

        auto epipX   = beam + targ - ele - pip0;
        auto q       = beam - ele;
        auto Q2      = -q.M2();
        auto v       = beam.E() - ele.E();
        auto xB      = Q2/(2*targ.M()*v);
        auto W2      = targ.M2() + 2*targ.M()*v - Q2;
        auto W       = sqrt(W2);
        auto y       = (targ.Dot(q))/(targ.Dot(beam));
        auto z       = ((pip0.E())/(q.E()));
        auto gamma   = 2*targ.M()*(xB/sqrt(Q2));
        auto epsilon = (1 - y - 0.25*(gamma*gamma)*(y*y))/(1 - y + 0.5*(y*y) + 0.25*(gamma*gamma)*(y*y));

        std::vector<double> vals = {epipX.M(), epipX.M2(), Q2, xB, v, W2, W, y, z, epsilon};

        return vals;"""]))
    rdf = rdf.Define("MM", "vals[0]")
    rdf = rdf.Define("MM2", "vals[1]")
    rdf = rdf.Define("Q2", "vals[2]")
    rdf = rdf.Define("xB", "vals[3]")
    rdf = rdf.Define("W", "vals[6]")
    rdf = rdf.Define("y", "vals[7]")
    rdf = rdf.Define("z", "vals[8]")

    rdf = rdf.Define("vals2", "".join(["""
    auto fe     = dppC(ex, ey, ez, esec, 0, """, DPPC_RDF_PASS2, """) + 1;
    auto fpip   = dppC(pipx, pipy, pipz, pipsec, 1, """, DPPC_RDF_PASS2, """) + 1;

    auto beamM  = ROOT::Math::PxPyPzMVector(0, 0, """, str(BEAM_ENERGY), """, 0);
    auto targM  = ROOT::Math::PxPyPzMVector(0, 0, 0,       0.938272);

    auto eleM   = ROOT::Math::PxPyPzMVector(ex*fe,     ey*fe,     ez*fe,     0);
    auto pip0M  = ROOT::Math::PxPyPzMVector(pipx*fpip, pipy*fpip, pipz*fpip, 0.13957);

    auto lv_qMM = beamM - eleM;

    TLorentzVector beam(0, 0, """, str(BEAM_ENERGY), """, beamM.E());
    TLorentzVector targ(0, 0, 0, targM.E());

    TLorentzVector ele(ex*fe,      ey*fe,     ez*fe,     eleM.E());
    TLorentzVector pip0(pipx*fpip, pipy*fpip, pipz*fpip, pip0M.E());

    TLorentzVector lv_q = beam - ele;

    double Theta_q = lv_q.Theta();
    double Phi_el  = ele.Phi();

    auto beam_Clone = Rot_Matrix(beam, -1, Theta_q, Phi_el);
    auto targ_Clone = Rot_Matrix(targ, -1, Theta_q, Phi_el);
    auto ele_Clone  = Rot_Matrix(ele,  -1, Theta_q, Phi_el);
    auto pip0_Clone = Rot_Matrix(pip0, -1, Theta_q, Phi_el);
    auto lv_q_Clone = Rot_Matrix(lv_q, -1, Theta_q, Phi_el);

    double pipx_1 = pip0_Clone.X();
    double pipy_1 = pip0_Clone.Y();

    auto fCM   = lv_q_Clone + targ_Clone;
    auto boost = -(fCM.BoostVector());

    auto qlv_Boost(lv_q_Clone);
    auto pip_Boost(pip0_Clone);

    qlv_Boost.Boost(boost);
    pip_Boost.Boost(boost);

    double xF = 2*(pip_Boost.Vect().Dot(qlv_Boost.Vect()))/(qlv_Boost.Vect().Mag()*W);
    double pT = sqrt(pipx_1*pipx_1 + pipy_1*pipy_1);
    double phi_t = pip0_Clone.Phi()*TMath::RadToDeg();
    if(phi_t < 0){phi_t += 360;}

    std::vector<double> vals2 = {pT, phi_t, xF};
    return vals2;"""]))
    rdf = rdf.Define("pT", "vals2[0]")
    rdf = rdf.Define("phi_t", "vals2[1]")
    rdf = rdf.Define("xF", "vals2[2]")

    print("%sCreating variables for Valerii's (New) Fiducial Cuts%s" % (color.BOLD, color.END))
    rdf = Sangbaek_and_Valerii_Fiducial_Cuts(Data_Frame_Input=rdf, fidlevel="N/A", Particle="ele")
    rdf = Sangbaek_and_Valerii_Fiducial_Cuts(Data_Frame_Input=rdf, fidlevel="N/A", Particle="pip")
    rdf = filter_Valerii(Data_Frame=rdf, Valerii_Cut="Complete", Cut_Flag=True)
    rdf = Valerii_Fiducial_PCal_Volume_Cuts(Data_Frame_Input=rdf, Cut_Flag=True, show_cut_code=False, cut_level="norm")
    rdf = Sector_Fiducial_PCal_Cuts(Data_Frame_Input=rdf, Cut_Flag=True, show_cut_code=False)
    rdf = Sangbaek_and_Valerii_Fiducial_Cuts(Data_Frame_Input=rdf, fidlevel="mid", Particle="ele", Cut_Flag=True, show_cut_code=False)
    rdf = Apply_Test_Fiducial_Cuts(Data_Frame_In=rdf, List_of_Layers=["6", "18", "36"], List_of_Particles=["pip"], Define_Column=True, show_cut_code=False)
    return rdf


def open_ntuple_rdf(files, tree, max_entries):
    if(not files):
        return None
    chain = ROOT.TChain(tree)
    for path in files:
        chain.Add(path, 0)
    rdf = ROOT.RDataFrame(chain)
    if((max_entries is not None) and (int(max_entries) > 0)):
        rdf = rdf.Range(int(max_entries))
    return rdf


def fill_histograms(rdf):
    booked = []
    print("%sLocal base selection cut_Complete_no_kinematics:%s" % (color.BOLD, color.END))
    print("  %s" % CUT_COMPLETE_NO_KINEMATICS)
    for omit_key, var, xmin, xmax, nbins, lines, title, fname in KIN_PLOTS:
        cut_omit = omit_one_filter(omit_key)
        cut_none = no_kin_filter()
        print("%sOmit-one %s filter:%s %s" % (color.BBLUE, omit_key, color.END, cut_omit))
        print("%sNo-kinematics %s filter:%s %s" % (color.BBLUE, omit_key, color.END, cut_none))
        rdf_omit = rdf.Filter(cut_omit)
        rdf_none = rdf.Filter(cut_none)
        h_omit = rdf_omit.Histo1D((hist_name(omit_key, False), title, nbins, xmin, xmax), var)
        h_none = rdf_none.Histo1D((hist_name(omit_key, True), "%s (PID/fiducial only)" % title, nbins, xmin, xmax), var)
        n_out_omit = rdf_omit.Filter(INVERT_CLAUSE[omit_key]).Count()
        n_out_none = rdf_none.Filter(INVERT_CLAUSE[omit_key]).Count()
        booked.append({
            "omit_key": omit_key,
            "var": var,
            "lines": lines,
            "title": title,
            "fname": fname,
            "h_omit": h_omit,
            "h_none": h_none,
            "n_out_omit": n_out_omit,
            "n_out_none": n_out_none,
            "cut_omit": cut_omit,
            "cut_none": cut_none,
        })
    written = []
    for item in booked:
        h_omit = ptr(item["h_omit"])
        h_none = ptr(item["h_none"])
        n_omit = int(item["n_out_omit"].GetValue())
        n_none = int(item["n_out_none"].GetValue())
        print("%s %s: omit-one entries=%.0f outside_illustrated=%d ; no-kin entries=%.0f outside_illustrated=%d%s" % (
            color.BOLD, item["omit_key"], h_omit.GetEntries(), n_omit, h_none.GetEntries(), n_none, color.END,
        ))
        if(n_none < n_omit):
            print("%sWARNING: no-kin outside count < omit-one outside count for %s%s" % (color.Error, item["omit_key"], color.END))
        written.append((hist_name(item["omit_key"], False), h_omit))
        written.append((hist_name(item["omit_key"], True), h_none))
    return written


def write_hist_file(path, hists):
    parent = os.path.dirname(os.path.abspath(path)) or "."
    os.makedirs(parent, exist_ok=True)
    out = ROOT.TFile.Open(path, "RECREATE")
    if((out is None) or (not out.IsOpen())):
        raise SystemExit("Cannot write histogram ROOT file %s" % path)
    out.cd()
    for name, hist in hists:
        hist.SetName(name)
        hist.Write(name)
        print("Wrote histogram", name)
    out.Close()
    print("Wrote", path)
    return path


def draw_cut_hist(hist, lines, pdf_path):
    can = ROOT.TCanvas("c_%s" % os.path.basename(pdf_path).replace(".pdf", ""), "c", 700, 500)
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
    os.makedirs(os.path.dirname(os.path.abspath(pdf_path)) or ".", exist_ok=True)
    can.SaveAs(pdf_path)
    print("Wrote", pdf_path)
    return pdf_path


def plot_from_root(hist_path, out_dir):
    infile = ROOT.TFile.Open(hist_path)
    if((infile is None) or (not infile.IsOpen())):
        raise SystemExit("Cannot open histogram ROOT file %s" % hist_path)
    written = []
    for omit_key, var, xmin, xmax, nbins, lines, title, fname in KIN_PLOTS:
        for no_kin in [False, True]:
            name = hist_name(omit_key, no_kin)
            hist = infile.Get(name)
            if(hist is None):
                print("%sMissing histogram %s in %s%s" % (color.Error, name, hist_path, color.END))
                continue
            hist.SetDirectory(0)
            pdf_path = os.path.join(out_dir, pdf_name(fname, no_kin))
            written.append(draw_cut_hist(hist, lines, pdf_path))
    infile.Close()
    return written


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_data_root_argument(parser)
    parser.add_argument("-f", "--file", default=None, help="Groovy-converted ntuple path/glob (comma-separated). Not rewritten if given. Default is the real_data_pass2 new10 glob.")
    parser.add_argument("--hists", default=None, help="ROOT histogram output path. Default is Chapter3_Kinematic_Cut_hists.root (or per-file basename if -f is one file).")
    parser.add_argument("--plot", default=None, help="Histogram ROOT file for PDF-only rendering. Does not reopen event ntuples.")
    parser.add_argument("-o", "--out", default=None, help="PDF output directory.")
    parser.add_argument("-t", "--tree", default="h22")
    parser.add_argument("-n", "--event_limit", type=int, default=-1)
    return parser.parse_args()


def main():
    args = parse_args()
    print_path_summary(EXEC_ROOT, args.data_root)
    out_dir = args.out if(args.out not in [None, ""]) else DEFAULT_OUT_DIR
    os.makedirs(out_dir, exist_ok=True)
    if(args.plot not in [None, ""]):
        written = plot_from_root(args.plot, out_dir)
        print("Done. %d PDFs from %s" % (len(written), args.plot))
        return 0

    if(args.file not in [None, ""]):
        files = expand(args.file)
    else:
        files = expand(DEFAULT_INPUT_GLOB)
    print("Input ntuples: %d" % len(files))
    for path in files:
        print("  %s" % path)
    if(not files):
        raise SystemExit("No Groovy-converted ntuple files found. Production default glob is %s. Pass -f for an explicit local file; the default is not rewritten for missing farm files." % DEFAULT_INPUT_GLOB)

    rdf = open_ntuple_rdf(files, args.tree, args.event_limit)
    missing = missing_columns(rdf, NTUPLE_REQUIRED)
    if(missing):
        have = [str(name) for name in rdf.GetColumnNames()]
        print("%sMissing required ntuple columns:%s %s" % (color.Error, color.END, missing))
        print("Available columns: %s" % have)
        raise SystemExit("Upstream ntuple is missing columns needed to reproduce production selections.")
    print("%sUpstream ntuple schema contains the required PID/fiducial/momentum columns.%s" % (color.BGREEN, color.END))

    rdf = prepare_corrected_rdf(rdf)
    for col in ["Q2", "y", "xF", "MM", "MM2", "elth", "pipth", "pip", "el", "W"]:
        if(not rdf_has(rdf, col)):
            raise SystemExit("Failed to define reconstructed column %s" % col)
    for col in ["valerii_PCAL_knockout_cut", "Valerii_PCal_Fiducial_Cuts", "Sector_PCal_Fiducial_Cuts", "Valerii_DC_Fiducial_Cuts_ele_DC_6", "My_pip_DC_Fiducial_Cuts_Layer_6"]:
        if(not rdf_has(rdf, col)):
            raise SystemExit("Failed to define selection flag %s" % col)

    hists = fill_histograms(rdf)
    hist_path = default_hist_path(out_dir, files, args.hists)
    write_hist_file(hist_path, hists)
    written = plot_from_root(hist_path, out_dir)
    print("Done. %d histograms -> %s ; %d PDFs -> %s" % (len(hists), hist_path, len(written), out_dir))
    return 0


if(__name__ == "__main__"):
    sys.exit(main())
