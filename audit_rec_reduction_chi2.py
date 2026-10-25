#!/usr/bin/env python3
"""One-bin 3D audit of reduced reconstructed binning vs RooUnfoldBayes first-iteration quantities."""

import math
import os
import sys

_BOOT = os.path.abspath(os.path.dirname(__file__))
if(_BOOT not in sys.path):
    sys.path.insert(0, _BOOT)

import ROOT
from reconstructed_bin_reduction import build_rec_skip_map, compress_th1_rec, compress_th2_rec_axis

ROOT.gROOT.SetBatch(True)
ROOT.TH1.AddDirectory(0)


def strip_smear(name):
    name = name.replace("_smeared", "")
    name = name.replace("smear_", "")
    name = name.replace("smear", "")
    return name


def apply_1d(name):
    return name.replace("'Response_Matrix_Normal'", "'Response_Matrix_Normal_1D'")


def finite_stats(hist):
    nnan = ninf = nfin = 0
    s = 0.0
    for i in range(1, hist.GetNbinsX() + 1):
        c = hist.GetBinContent(i)
        if math.isnan(c):
            nnan += 1
        elif math.isinf(c):
            ninf += 1
        else:
            nfin += 1
            s += c
    return nfin, nnan, ninf, s


def main():
    inf = "Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_3D_Final_Thesis_Response_Matrices_Final_Thesis_Files_All.root"
    f = ROOT.TFile.Open(inf)
    resp_name = "((Histo-Group='Response_Matrix_Normal'), (Data-Type='mdf'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type='smear'), (Binning-Type='Y_bin'-[Q2-y-Bin=1, z-PT-Bin=All]), (Var-D1='MultiDim_z_pT_Bin_Y_bin_phi_t'-[NumBins=698, MinBin=-1.5, MaxBin=696.5]), (Var-D2='z_pT_Bin_Y_bin_smeared'-[NumBins=38, MinBin=-0.5, MaxBin=37.5]))"
    mdf_1d = apply_1d(resp_name)
    rdf_name = apply_1d(strip_smear(resp_name.replace("(Data-Type='mdf')", "(Data-Type='rdf')")))
    gdf_name = apply_1d(strip_smear(resp_name.replace("(Data-Type='mdf')", "(Data-Type='gdf')").replace("cut_Complete_SIDIS", "no_cut")))
    bdf_name = mdf_1d.replace("'Response_Matrix_Normal_1D'", "'Background_Response_Matrix_1D'")
    rho_name = mdf_1d + "_(lundvpk)"
    print("keys exist", {k: bool(f.Get(k)) for k, k in [("resp", resp_name), ("mdf", mdf_1d), ("rdf", rdf_name), ("gdf", gdf_name), ("bdf", bdf_name), ("rho", rho_name)].__iter__() if False})
    for lab, n in [("resp", resp_name), ("mdf", mdf_1d), ("rdf", rdf_name), ("gdf", gdf_name), ("bdf", bdf_name), ("rho", rho_name)]:
        o = f.Get(n)
        print(f"GET {lab}: {o is not None}  {n[:80]}...")

    resp = f.Get(resp_name)
    mdf = f.Get(mdf_1d)
    rdf = f.Get(rdf_name)
    gdf = f.Get(gdf_name)
    bdf = f.Get(bdf_name)
    rho = f.Get(rho_name)
    print("types", type(resp).__name__, type(mdf).__name__, type(rdf).__name__, type(gdf).__name__, type(bdf).__name__, type(rho).__name__)
    rdf = rdf.Clone("rdf_in")
    rdf.SetDirectory(0)
    mdf = mdf.Clone("mdf_in")
    mdf.SetDirectory(0)
    gdf = gdf.Clone("gdf_in")
    gdf.SetDirectory(0)
    bdf = bdf.Clone("bdf_in")
    bdf.SetDirectory(0)
    rho = rho.Clone("rho_in")
    rho.SetDirectory(0)
    rdf_sub = rdf.Clone("rdf_sub")
    rdf_sub.SetDirectory(0)
    rdf_sub.Add(rho, -1.0)
    for i in range(rdf_sub.GetNcells()):
        if rdf_sub.GetBinContent(i) < 0:
            rdf_sub.SetBinContent(i, 0.0)

    # skip_map = build_rec_skip_map(rdf_sub, mdf, gdf, bdf, 0.0005)  # Changed to 0.025 on 9/16/2026
    skip_map = build_rec_skip_map(rdf_sub, mdf, gdf, bdf, 0.025)
    print("\n=== SKIP MAP ===")
    for line in skip_map.report_lines():
        print(line)
    print("first10 skipped", skip_map.skipped[:10])
    print("last10 skipped", skip_map.skipped[-10:])

    rdf_red = compress_th1_rec(rdf_sub, skip_map, "rdf_red")
    mdf_red = compress_th1_rec(mdf, skip_map, "mdf_red")
    bdf_red = compress_th1_rec(bdf, skip_map, "bdf_red")

    maxdiff = 0.0
    for orig in skip_map.kept:
        red = skip_map.orig_to_reduced[orig]
        for h0, h1 in ((rdf_sub, rdf_red), (mdf, mdf_red), (bdf, bdf_red)):
            maxdiff = max(maxdiff, abs(h0.GetBinContent(orig) - h1.GetBinContent(red)))
    print("max |orig kept - reduced| on rdf/mdf/bdf", maxdiff)
    print("gdf nbins", gdf.GetNbinsX(), "xmin", gdf.GetXaxis().GetXmin(), "xmax", gdf.GetXaxis().GetXmax(), "integral", gdf.Integral())
    print("rdf_red", rdf_red.GetNbinsX(), rdf_red.GetXaxis().GetXmin(), rdf_red.GetXaxis().GetXmax())
    print("mdf_red", mdf_red.GetNbinsX(), mdf_red.GetXaxis().GetXmin(), mdf_red.GetXaxis().GetXmax())

    n_orig = resp.GetNbinsX()
    n_rec_orig = resp.GetNbinsY()
    print("\n=== ORIENTATION (stored response) ===")
    print(f"stored TH2 nx={resp.GetNbinsX()} (GEN) ny={resp.GetNbinsY()} (REC)")

    # C++ reduced-mode flip: uses reduced rec axis range but original rec bin count
    n_kept = skip_map.n_kept
    rec_width = rdf_red.GetBinWidth(1)
    rec_min = rdf_red.GetBinCenter(0) + 0.5 * rec_width
    rec_max = rdf_red.GetBinCenter(n_kept) + 0.5 * rec_width
    gen_width = gdf.GetBinWidth(1)
    n_gen = gdf.GetNbinsX()
    gen_min = gdf.GetBinCenter(0) + 0.5 * gen_width
    gen_max = gdf.GetBinCenter(n_gen) + 0.5 * gen_width
    print("C++ flip axis (reduced path): rec_min/max", rec_min, rec_max, "nY_orig", n_rec_orig, "gen", gen_min, gen_max, n_gen)

    flipped_bug = ROOT.TH2D("flipped_bug", "flip reduced-range orig-nbins", n_rec_orig, rec_min, rec_max, n_orig, gen_min, gen_max)
    flipped_bug.SetDirectory(0)
    for gen_bin in range(0, n_gen + 1):
        for rec_bin in range(0, n_rec_orig + 1):
            flipped_bug.SetBinContent(rec_bin, gen_bin, resp.GetBinContent(gen_bin, rec_bin))
            flipped_bug.SetBinError(rec_bin, gen_bin, resp.GetBinError(gen_bin, rec_bin))
    print("flipped_bug nx,ny", flipped_bug.GetNbinsX(), flipped_bug.GetNbinsY(), "xmin,xmax", flipped_bug.GetXaxis().GetXmin(), flipped_bug.GetXaxis().GetXmax())

    flipped_ok = ROOT.TH2D("flipped_ok", "flip orig-range orig-nbins", n_rec_orig, resp.GetYaxis().GetXmin(), resp.GetYaxis().GetXmax(), n_orig, resp.GetXaxis().GetXmin(), resp.GetXaxis().GetXmax())
    flipped_ok.SetDirectory(0)
    for gen_bin in range(0, n_gen + 1):
        for rec_bin in range(0, n_rec_orig + 1):
            flipped_ok.SetBinContent(rec_bin, gen_bin, resp.GetBinContent(gen_bin, rec_bin))

    compressed = compress_th2_rec_axis(flipped_bug, skip_map, True, "resp_red")
    compressed_ok = compress_th2_rec_axis(flipped_ok, skip_map, True, "resp_red_ok")
    print("compressed nx,ny", compressed.GetNbinsX(), compressed.GetNbinsY(), "rec axis", compressed.GetXaxis().GetXmin(), compressed.GetXaxis().GetXmax(), "gen axis", compressed.GetYaxis().GetXmin(), compressed.GetYaxis().GetXmax())

    max_resp_diff = 0.0
    max_bug_vs_ok = 0.0
    probes = skip_map.kept[:3] + skip_map.kept[len(skip_map.kept)//2:len(skip_map.kept)//2+2]
    print("\n=== REC TRACE (orig -> red -> rdf/mdf/resp) ===")
    for orig in probes:
        red = skip_map.orig_to_reduced[orig]
        print(f"orig={orig} red={red} rdf={rdf_sub.GetBinContent(orig):.6g} rdf_red={rdf_red.GetBinContent(red):.6g} mdf={mdf.GetBinContent(orig):.6g} mdf_red={mdf_red.GetBinContent(red):.6g}")
        for gy in (1, 10, 50):
            a = flipped_ok.GetBinContent(orig, gy)
            b = compressed.GetBinContent(red, gy)
            c = compressed_ok.GetBinContent(red, gy)
            max_resp_diff = max(max_resp_diff, abs(a - b))
            max_bug_vs_ok = max(max_bug_vs_ok, abs(b - c))
    print("max |flipped_ok(orig,g) - compressed_bug(red,g)| over probes", max_resp_diff)
    print("max |compressed_bug - compressed_ok| over probes", max_bug_vs_ok)

    # miss accounting
    print("\n=== MISS ACCOUNTING ===")
    def proj_y(th2, gen_i, rec_lo, rec_hi):
        s = 0.0
        for r in range(rec_lo, rec_hi + 1):
            s += th2.GetBinContent(r, gen_i)
        return s
    skipped = set(skip_map.skipped)
    kept = skip_map.kept
    # pick gen bins: first, one with skipped partners, last
    gen_probes = [1, 2, 24, 50, 100, 697, 698]
    n_zero_eff = 0
    n_gpos = 0
    max_balance = 0.0
    sumG = sumKeep = sumSkip = sumU = 0.0
    for gi in range(1, n_gen + 1):
        G = gdf.GetBinContent(gi)
        M_keep = sum(flipped_ok.GetBinContent(r, gi) for r in kept)
        M_skip = sum(flipped_ok.GetBinContent(r, gi) for r in skip_map.skipped)
        M_all = sum(flipped_ok.GetBinContent(r, gi) for r in range(1, n_rec_orig + 1))
        U = G - M_all
        sumG += G
        sumKeep += M_keep
        sumSkip += M_skip
        sumU += U
        bal = abs(G - (M_keep + M_skip + U))
        max_balance = max(max_balance, bal)
        if G > 0:
            n_gpos += 1
            if M_keep == 0:
                n_zero_eff += 1
    print(f"integrals G={sumG:.6g} M_keep={sumKeep:.6g} M_skip={sumSkip:.6g} U={sumU:.6g} max|G-(keep+skip+U)|={max_balance}")
    print(f"gen bins G>0: {n_gpos}; G>0 and M_keep==0 (zero remaining rec matches): {n_zero_eff}")
    print("gen probes:")
    for gi in gen_probes:
        if gi > n_gen:
            continue
        G = gdf.GetBinContent(gi)
        M_keep = sum(flipped_ok.GetBinContent(r, gi) for r in kept)
        M_skip = sum(flipped_ok.GetBinContent(r, gi) for r in skip_map.skipped)
        M_all = sum(flipped_ok.GetBinContent(r, gi) for r in range(1, n_rec_orig + 1))
        print(f"  gen={gi} G={G:.6g} M_keep={M_keep:.6g} M_skip={M_skip:.6g} M_all={M_all:.6g} U={G-M_all:.6g} eff_keep={0 if G==0 else M_keep/G:.6g}")

    # RooUnfoldResponse public objects
    print("\n=== ROOUNFOLDRESPONSE PUBLIC ===")
    ru = ROOT.RooUnfoldResponse(mdf_red, gdf, compressed, "ru", "ru")
    for rec_bin in range(1, bdf_red.GetNbinsX() + 1):
        ru.Fake(bdf_red.GetBinCenter(rec_bin), bdf_red.GetBinContent(rec_bin))
    ht = ru.Htruth()
    hm = ru.Hmeasured()
    hf = ru.Hfakes()
    hr = ru.Hresponse()
    print("Htruth nbins", ht.GetNbinsX(), "xmin", ht.GetXaxis().GetXmin(), "integral", ht.Integral(), "vs gdf", gdf.Integral())
    print("Hmeasured nbins", hm.GetNbinsX(), "xmin", hm.GetXaxis().GetXmin(), "integral", hm.Integral(), "vs mdf_red", mdf_red.Integral())
    print("Hfakes integral", hf.Integral() if hf else None)
    print("Hresponse nx,ny", hr.GetNbinsX(), hr.GetNbinsY())
    max_t = max(abs(ht.GetBinContent(i) - gdf.GetBinContent(i)) for i in range(1, n_gen + 1))
    print("max |Htruth - gdf|", max_t)

    veff = ru.Vefficiency()
    n_eff0_gpos = 0
    n_eff_nan = 0
    for i in range(n_gen):
        e = veff[i]
        g = gdf.GetBinContent(i + 1)
        if math.isnan(e) or math.isinf(e):
            n_eff_nan += 1
        if g > 0 and e == 0:
            n_eff0_gpos += 1
    print("Vefficiency len", veff.GetNrows(), "NaN/Inf", n_eff_nan, "G>0 and eff==0", n_eff0_gpos)

    # Reconstruct first Bayes iteration from public objects (handleFakes=false)
    print("\n=== EXTERNAL FIRST-ITERATION BAYES ===")
    nt = n_gen
    nm = n_kept
    nCi = [ht.GetBinContent(i + 1) for i in range(nt)]
    nEst = [rdf_red.GetBinContent(j + 1) for j in range(nm)]  # measured data, not mdf
    # Nji[j][i] measured j, truth i  == Hresponse(j+1, i+1)
    Nji = [[hr.GetBinContent(j + 1, i + 1) for i in range(nt)] for j in range(nm)]

    def nfinite(xs):
        return sum(1 for x in xs if (not math.isnan(x)) and (not math.isinf(x)))

    N0C = sum(nCi)
    print("N0C (sum truth)", N0C, "finite nCi", nfinite(nCi), "/", nt)
    P0C = [c / N0C if N0C != 0 else math.nan for c in nCi]
    print("P0C finite", nfinite(P0C), "nan", sum(math.isnan(x) for x in P0C), "min", min(P0C), "max", max(P0C))

    eff = [0.0] * nt
    PEjCi = [[0.0] * nt for _ in range(nm)]
    PEjCiEff = [[0.0] * nt for _ in range(nm)]
    n_resp_nan = 0
    for i in range(nt):
        if nCi[i] <= 0:
            continue
        s = 0.0
        for j in range(nm):
            r = Nji[j][i] / nCi[i]
            if math.isnan(r) or math.isinf(r):
                n_resp_nan += 1
            PEjCi[j][i] = r
            s += r
        eff[i] = s
        inv = (1.0 / s) if s > 0 else 0.0
        for j in range(nm):
            PEjCiEff[j][i] = PEjCi[j][i] * inv
    print("response/nCi NaN-or-Inf cells", n_resp_nan)
    print("eff finite", nfinite(eff), "nan", sum(math.isnan(x) for x in eff), "zeros with nCi>0", sum(1 for i in range(nt) if nCi[i] > 0 and eff[i] == 0))

    UjInv = [0.0] * nm
    n_U0 = 0
    n_U_nan = 0
    for j in range(nm):
        Uj = sum(PEjCi[j][i] * P0C[i] for i in range(nt))
        if math.isnan(Uj) or math.isinf(Uj):
            n_U_nan += 1
            UjInv[j] = math.nan
        elif Uj > 0:
            UjInv[j] = 1.0 / Uj
        else:
            UjInv[j] = 0.0
            n_U0 += 1
    print("UjInv: Uj==0", n_U0, "Uj nan/inf", n_U_nan, "finite", nfinite(UjInv))

    nbarC = [0.0] * nt
    nbartrue = 0.0
    first_bad = None
    for i in range(nt):
        nbar = 0.0
        for j in range(nm):
            Mij = UjInv[j] * PEjCiEff[j][i] * P0C[i]
            if first_bad is None and (math.isnan(Mij) or math.isinf(Mij)):
                first_bad = ("Mij", i, j, "UjInv", UjInv[j], "PEjCiEff", PEjCiEff[j][i], "P0C", P0C[i], "nEst", nEst[j])
            nbar += Mij * nEst[j]
        nbarC[i] = nbar
        nbartrue += nbar
        if first_bad is None and (math.isnan(nbar) or math.isinf(nbar)):
            first_bad = ("nbarC", i, nbar, "nCi", nCi[i], "eff", eff[i])
    print("nbartrue", nbartrue, "finite nbarC", nfinite(nbarC), "nan nbarC", sum(math.isnan(x) for x in nbarC))
    print("first_bad", first_bad)

    if nbartrue == 0 or math.isnan(nbartrue) or math.isinf(nbartrue):
        print("PbarCi cannot be formed: nbartrue is", nbartrue)
        Pbar = [math.nan] * nt
    else:
        Pbar = [c / nbartrue for c in nbarC]
    print("Pbar finite", nfinite(Pbar), "nan", sum(math.isnan(x) for x in Pbar), "inf", sum(math.isinf(x) for x in Pbar))

    chi2 = 0.0
    chi2_nan = False
    for i in range(nt):
        psum = (Pbar[i] + P0C[i]) * nbartrue
        pdiff = (Pbar[i] - P0C[i]) * nbartrue
        if math.isnan(psum) or math.isnan(pdiff) or math.isinf(psum) or math.isinf(pdiff):
            chi2_nan = True
            if first_bad is None or first_bad[0] not in ("Mij", "nbarC"):
                first_bad = ("getChi2_term", i, "Pbar", Pbar[i], "P0C", P0C[i], "nbartrue", nbartrue)
            break
        if psum > 1.0:
            chi2 += (pdiff * pdiff) / psum
        else:
            chi2 += (pdiff * pdiff)
    print("reconstructed Chi2 of change", "nan" if chi2_nan else chi2)

    # Also unfold with RooUnfold 2 iter none to compare
    unf = ROOT.RooUnfoldBayes(ru, rdf_red, 2)
    unf.SetVerbose(2)
    h = unf.Hunfold(ROOT.RooUnfold.kNoError)
    fs = finite_stats(h)
    print("Hunfold kNoError 2iter finite/nan/inf/sum", fs)

    f.Close()


if __name__ == "__main__":
    sys.exit(main() or 0)
