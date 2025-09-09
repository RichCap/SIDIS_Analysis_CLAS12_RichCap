#!/usr/bin/env python3
# Find_RC_Fit_Params.py
#
# One-shot RC vs φ_h fitter with optional ROOT cache.
# Returns [A, A_err, B, B_err, C, C_err] for a single (Q2_y_bin, z_pT_bin).
# IMPORTANT: This version DOES NOT build graphs. It ONLY reads an existing
#            TGraph/TGraphErrors from --root-in by the canonical key name:
#            f"{plot}_vs_phi_h_Q2_y_Bin_{Q2_y_bin}_z_pT_Bin_{z_pT_bin}"
#            where plot is "RC_factor" (primary). If not found, it errors.
#
# Verbose progress prints by default; pass --quiet to suppress.

import sys
import os
import argparse
import ROOT

script_dir = '/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis'
sys.path.append(script_dir)
from MyCommonAnalysisFunction_richcap import color, RuntimeTimer
sys.path.remove(script_dir)
del script_dir

ROOT.gROOT.SetBatch(1)
ROOT.ROOT.EnableImplicitMT()

# -------------------------
# Logging helper
# -------------------------

def _log(msg, quiet=False, pref=color.CYAN, suff=color.END):
    if(not quiet):
        print(f"{pref}{msg}{suff}")
        sys.stdout.flush()

# -------------------------
# Cache helpers (ROOT I/O)
# -------------------------

def _safe_delete_all_versions(dir_or_file, name):
    obj = dir_or_file.GetListOfKeys().FindObject(name)
    if(obj):
        dir_or_file.Delete(f"{name};*")

def _ensure_dir(tfile, dname):
    d = tfile.Get(dname)
    if(not d):
        d = tfile.mkdir(dname)
    return d

def _read_cache_vector(cache_path, key, quiet):
    if(not os.path.exists(cache_path)):
        _log(f"[cache-in] File not found: {cache_path}", quiet, color.YELLOW, color.END)
        return None
    _log(f"[cache-in] Opening cache: {cache_path}", quiet, color.BBLUE, color.END)
    f = ROOT.TFile.Open(cache_path, "READ")
    if((not f) or f.IsZombie()):
        _log("[cache-in] Failed to open cache (zombie).", quiet, color.Error, color.END)
        return None
    try:
        d = f.Get("fit_params")
        if(not d):
            _log("[cache-in] Missing directory 'fit_params'.", quiet, color.YELLOW, color.END)
            return None
        v = d.Get(key)
        if(not v):
            _log(f"[cache-in] Key miss: {key}", quiet, color.YELLOW, color.END)
            return None
        if(isinstance(v, ROOT.TVectorD)):
            if(int(v.GetNoElements()) != 6):
                _log("[cache-in] TVectorD has wrong length.", quiet, color.Error, color.END)
                return None
            out = [float(v[i]) for i in range(6)]
            _log(f"[cache-in] HIT {key} -> {out}", quiet, color.BGREEN, color.END)
            return out
        if(isinstance(v, ROOT.TNamed)):
            import json
            data = json.loads(v.GetTitle())
            if(isinstance(data, list) and (len(data) == 6)):
                out = [float(x) for x in data]
                _log(f"[cache-in] HIT (JSON) {key} -> {out}", quiet, color.BGREEN, color.END)
                return out
            _log("[cache-in] Malformed JSON entry.", quiet, color.Error, color.END)
            return None
        _log("[cache-in] Unsupported object type.", quiet, color.Error, color.END)
        return None
    finally:
        f.Close()

def _write_cache_vector(cache_path, key, params, quiet):
    if(len(params) != 6):
        raise ValueError("Internal error: params must have length 6.")
    _log(f"[cache-out] Writing key {key} to {cache_path}", quiet, color.BBLUE, color.END)
    f = ROOT.TFile(cache_path, "UPDATE")
    if((not f) or f.IsZombie()):
        raise RuntimeError(f"{color.Error}Unable to open cache file for update: {color.END_B}{cache_path}{color.END}")
    try:
        d = _ensure_dir(f, "fit_params")
        d.cd()
        _safe_delete_all_versions(d, key)
        vec = ROOT.TVectorD(6)
        for i, val in enumerate(params):
            vec[i] = float(val)
        vec.SetName(key)
        vec.Write()
        f.Write("", ROOT.TObject.kOverwrite)
        _log(f"[cache-out] Wrote {key} <- {params}", quiet, color.BGREEN, color.END)
    finally:
        f.Close()

# -------------------------
# Graph lookup (NO BUILDING)
# -------------------------

def _build_key_name(plot_choice, q2y_bin, zpt_bin):
    # Exact string you asked for from the original script
    return f"{plot_choice}_vs_phi_h_Q2_y_Bin_{q2y_bin if(q2y_bin is not None) else 'All'}_z_pT_Bin_{zpt_bin if(zpt_bin is not None) else 'All'}"

def _get_graph_from_file(root_path, plot_choice, q2y_bin, zpt_bin, quiet):
    if(not os.path.exists(root_path)):
        raise FileNotFoundError(f"ROOT file not found: {root_path}")

    key_name = _build_key_name(plot_choice, q2y_bin, zpt_bin)
    _log(f"[lookup] Opening ROOT file: {root_path}", quiet, color.CYAN, color.END)
    _log(f"[lookup] Looking for key: {key_name}", quiet, color.CYAN, color.END)

    f = ROOT.TFile.Open(root_path, "READ")
    if((not f) or f.IsZombie()):
        raise RuntimeError(f"Failed to open ROOT file (zombie): {root_path}")

    try:
        # Exact key match required
        obj = f.Get(key_name)
        if(not obj):
            # Helpful diagnostics: show close candidates
            _log("[lookup] Key not found. Listing candidates starting with 'RC_..._vs_phi_h_Q2_y_Bin_':", quiet, color.YELLOW, color.END)
            keys = f.GetListOfKeys()
            shown = 0
            for i in range(keys.GetEntries()):
                k = keys.At(i)
                nm = k.GetName()
                if("vs_phi_h_Q2_y_Bin_" in nm and nm.startswith("RC_")):
                    _log(f"  - {nm}", quiet, color.YELLOW, color.END)
                    shown += 1
                    if(shown > 24):  # don't spam
                        _log("  ... (truncated)", quiet, color.YELLOW, color.END)
                        break
            raise KeyError(f"Key not found in ROOT file: {key_name}")

        # Accept TGraphErrors or TGraph; convert TGraph -> TGraphErrors for uniform fit
        if(isinstance(obj, ROOT.TGraphErrors)):
            graph = obj
        elif(isinstance(obj, ROOT.TGraph)):
            _log("[lookup] Found TGraph (no errors). Converting to TGraphErrors for fit.", quiet, color.BBLUE, color.END)
            n     = obj.GetN()
            graph = ROOT.TGraphErrors(n)
            graph.SetName(obj.GetName())
            for i in range(n):
                x = obj.GetPointX(i)
                y = obj.GetPointY(i)
                graph.SetPoint(i, x, y)
                graph.SetPointError(i, 0.0, 0.0)
        else:
            raise TypeError(f"Object under key is not a TGraph/TGraphErrors: {type(obj)}")

        # Light style (not used for drawing, just to match your fit cosmetics)
        graph.SetMarkerStyle(8)
        graph.SetMarkerSize(1.0)
        graph.SetLineWidth(2)
        graph.SetLineColor(ROOT.kBlue + 1)
        graph.SetMarkerColor(ROOT.kBlue + 1)
        return graph
    finally:
        # Keep file open until after we copy? Graphs are memory-resident; safe to close.
        f.Close()

# -------------------------
# Fit (same behavior as before)
# -------------------------

def _fit_phi_h_graph(graph, quiet):
    xmin = graph.GetXaxis().GetXmin()
    xmax = graph.GetXaxis().GetXmax()

    ys   = [graph.GetPointY(i) for i in range(graph.GetN())]
    ymin = min(ys)
    ymax = max(ys)

    func = ROOT.TF1(
        f"phi_h_fit_of_graph_{graph.GetName()}",
        "[0]*(1 + [1]*cos(x * TMath::DegToRad()) + [2]*cos(2 * x * TMath::DegToRad()))",
        xmin, xmax
    )

    ave_A = 0.5 * (ymin + ymax)
    func.SetParameter(0, ave_A)
    func.SetParLimits(0, min([0.8*ymin, 1.2*ymin]), max([0.8*ymax, 1.2*ymax]))
    func.SetParameter(1, 0.0)
    func.SetParLimits(1, -1.0, 1.0)
    func.SetParameter(2, 0.0)
    func.SetParLimits(2, -1.0, 1.0)
    func.SetLineColorAlpha(graph.GetLineColor(), 0.85)
    func.SetLineStyle(2)

    _log(f"[fit] Start: N={graph.GetN()} points, x∈[{xmin:.2f},{xmax:.2f}], seed A={ave_A:.6f}", quiet, color.PINK, color.END)
    status = int(graph.Fit(func, "QR"))
    _log(f"[fit] ROOT status = {status}", quiet, color.PINK, color.END)
    if(status != 0):
        raise RuntimeError("Fit failed (ROOT returned non-zero status).")

    A_val = float(func.GetParameter(0));  A_err = float(func.GetParError(0))
    B_val = float(func.GetParameter(1));  B_err = float(func.GetParError(1))
    C_val = float(func.GetParameter(2));  C_err = float(func.GetParError(2))

    _log(f"[fit] A={A_val:.6f} ± {A_err:.6e}", quiet, color.BGREEN, color.END)
    _log(f"[fit] B={B_val:.6e} ± {B_err:.6e}", quiet, color.BGREEN, color.END)
    _log(f"[fit] C={C_val:.6e} ± {C_err:.6e}", quiet, color.BGREEN, color.END)

    return [A_val, A_err, B_val, B_err, C_val, C_err]

# -------------------------
# Public API
# -------------------------

def Find_RC_Fit_Params(Q2_y_bin, z_pT_bin, root_in=None, cache_in=None, cache_out=None, quiet=True):
    if((cache_in is not None) and (cache_out is not None)):
        raise ValueError("Use either 'cache_in' (read-only) or 'cache_out' (write-only), not both.")

    plot_choice = "RC_factor"   # only RC vs φ_h is in-scope; key uses this
    key         = f"RC_{Q2_y_bin}_{z_pT_bin}"
    _log(f"[start] key={key}, plot={plot_choice}", quiet, color.CYAN, color.END)

    # READ-ONLY cache mode
    if(cache_in is not None):
        _log("[mode] READ-ONLY cache", quiet, color.BBLUE, color.END)
        cached = _read_cache_vector(cache_in, key, quiet)
        if(cached is not None):
            return cached
        if(root_in is None):
            raise FileNotFoundError("Cache miss and no 'root_in' provided to read the graph.")
        _log("[fallback] Cache miss -> reading graph from ROOT (no write).", quiet, color.YELLOW, color.END)
        graph  = _get_graph_from_file(root_in, plot_choice, Q2_y_bin, z_pT_bin, quiet)
        params = _fit_phi_h_graph(graph, quiet)
        return params

    # WRITE-ONLY cache mode
    if(cache_out is not None):
        if(root_in is None):
            raise ValueError("'root_in' is required in write-only mode (cache_out).")
        _log("[mode] WRITE-ONLY cache", quiet, color.BBLUE, color.END)
        graph  = _get_graph_from_file(root_in, plot_choice, Q2_y_bin, z_pT_bin, quiet)
        params = _fit_phi_h_graph(graph, quiet)
        _write_cache_vector(cache_out, key, params, quiet)
        return params

    # NO-CACHE mode
    if(root_in is None):
        raise ValueError("'root_in' is required (must contain the TGraph to fit).")
    _log("[mode] NO-CACHE (read graph, fit, return)", quiet, color.BBLUE, color.END)
    graph  = _get_graph_from_file(root_in, plot_choice, Q2_y_bin, z_pT_bin, quiet)
    params = _fit_phi_h_graph(graph, quiet)
    return params


import math

# Reweights each bin and propagates errors from:
# - the original bin error, and
# - parameter uncertainties (diagonal by default, optional full 3×3 covariance).
def Apply_RC_Factor_Corrections(hist, Par_A, Par_B, Par_C, use_param_errors=False, Par_A_err=0.0, Par_B_err=0.0, Par_C_err=0.0, param_cov=None):
    nbins = hist.GetNbinsX()
    if(nbins != 24):
        print(f"\n{color.Error}[Apply_RC_Factor_Corrections] Warning:{color.END} nbins={nbins}; proceeding with actual nbins.\n")
    xmin = hist.GetXaxis().GetXmin()
    xmax = hist.GetXaxis().GetXmax()

    get_center  = hist.GetBinCenter
    get_content = hist.GetBinContent
    get_error   = hist.GetBinError
    set_content = hist.SetBinContent
    set_error   = hist.SetBinError

    # Choose covariance: if(param_cov) use it; else build diagonal from per-parameter errors
    cov = None
    if(use_param_errors):
        if((param_cov is not None) and (len(param_cov) == 3) and (len(param_cov[0]) == 3) and (len(param_cov[1]) == 3) and (len(param_cov[2]) == 3)):
            cov = param_cov
        else:
            cov = ((Par_A_err * Par_A_err, 0.0,                  0.0),
                   (0.0,                  Par_B_err * Par_B_err, 0.0),
                   (0.0,                  0.0,                  Par_C_err * Par_C_err),
            )
    # Underflow(0) .. overflow(nbins+1), inclusive
    for bin_idx in range(0, (nbins + 1) + 1):
        if((1 <= bin_idx) and (bin_idx <= nbins)):
            x_deg = get_center(bin_idx)
        else:
            x_deg = (xmin if(bin_idx == 0) else xmax)

        cos1    = math.cos(math.radians(x_deg))
        cos2    = math.cos(math.radians(2.0 * x_deg))
        weight  = Par_A * (1.0 + (Par_B * cos1) + (Par_C * cos2))

        content = get_content(bin_idx)
        sigma_c = get_error(bin_idx)

        new_content = (content * weight)
        set_content(bin_idx, new_content)

        # Base variance from original bin error: (|w| * σ_c)^2
        var_y = ((abs(weight) * sigma_c) ** 2)

        # Add parameter-propagation variance if requested
        if(use_param_errors):
            # Gradient wrt parameters at this bin:
            # y = c * w, w = A*(1 + B cosφ + C cos2φ)
            # ∂y/∂A = c*(1 + B cosφ + C cos2φ)
            # ∂y/∂B = c*A*cosφ
            # ∂y/∂C = c*A*cos2φ
            gA = (content * (1.0 + (Par_B * cos1) + (Par_C * cos2)))
            gB = (content * Par_A * cos1)
            gC = (content * Par_A * cos2)

            if(param_cov is None):
                # Diagonal-only: g^T diag σ^2 g
                var_params = ((gA * gA) * (Par_A_err * Par_A_err)) + ((gB * gB) * (Par_B_err * Par_B_err)) + ((gC * gC) * (Par_C_err * Par_C_err))
            else:
                # Full 3×3: g^T Cov g (manual to avoid numpy)
                h0 = (cov[0][0] * gA) + (cov[0][1] * gB) + (cov[0][2] * gC)
                h1 = (cov[1][0] * gA) + (cov[1][1] * gB) + (cov[1][2] * gC)
                h2 = (cov[2][0] * gA) + (cov[2][1] * gB) + (cov[2][2] * gC)
                var_params = (gA * h0) + (gB * h1) + (gC * h2)

            if(var_params > 0.0):
                var_y += var_params

        new_error = (math.sqrt(var_y) if(var_y > 0.0) else 0.0)
        set_error(bin_idx, new_error)

    return hist

# -------------------------
# CLI
# -------------------------

def parse_cli():
    p = argparse.ArgumentParser(description="Read pre-made RC vs φ_h TGraph from ROOT by key and fit A*(1+B cosφ + C cos2φ). Returns [A, A_err, B, B_err, C, C_err].")
    p.add_argument("-q2_y", "-Q2_y", "--Q2_y_bin",                       type=int, required=True,
                   help="Q2-y bin index (int).")
    p.add_argument("-z_pt", "-z_pT", "--z_pT_bin",                       type=int, required=True,
                   help="z-pT bin index (int).")
    p.add_argument("-r",             "--root-in",     dest="root_in",    type=str, default="/w/hallb-scshelf2102/clas12/richcap/Radiative_MC/SIDIS_RC_EvGen_richcap/Running_EvGen_richcap/Testing_V2_MM_Cut_Copy.root", 
                   help="Input ROOT file with the pre-made plots (default: 'Testing_V2_MM_Cut_Copy.root' in the EvGen directory - is currently the most Up-To-Date version of the EvGen RC plot file).")
    g = p.add_mutually_exclusive_group()
    g.add_argument("-in",            "--cache-in",    dest="cache_in",   type=str,
                   help="Read-only ROOT cache path.")
    g.add_argument("-out",           "--cache-out",   dest="cache_out",  type=str,
                   help="Write-only ROOT cache path.")
    p.add_argument("-q",             "--quiet",                                    action="store_true",
                   help="Minimize printouts.")
    return p.parse_args()

def cli_main():
    timer = RuntimeTimer()
    timer.start()
    args = parse_cli()
    _log(f"[cli] Args: Q2_y_bin={args.Q2_y_bin}, z_pT_bin={args.z_pT_bin}, root_in={args.root_in}, cache_in={args.cache_in}, cache_out={args.cache_out}, quiet={args.quiet}", args.quiet, color.CYAN, color.END)
    try:
        params = Find_RC_Fit_Params(Q2_y_bin=args.Q2_y_bin, z_pT_bin=args.z_pT_bin, root_in=args.root_in, cache_in=args.cache_in, cache_out=args.cache_out, quiet=args.quiet)
        print(f"[A, Ae, B, Be, C, Ce] -> [{params[0]}, {params[1]}, {params[2]}, {params[3]}, {params[4]}, {params[5]}]\n")
        timer.stop()
        return 0
    except Exception as e:
        sys.stderr.write(f"{color.Error}ERROR: {color.END_R}{e}{color.END}\n")
        timer.stop()
        return 1

if(__name__ == "__main__"):
    print(f"\n{color.BBLUE}Started Running 'Find_RC_Fit_Params.py'{color.END}\n")
    sys.exit(cli_main())


