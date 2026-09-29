#!/usr/bin/env python3
# B and C from the authoritative Compute_SplineWeight file.
# The RDataFrame filler calls ComputeSplineWeight(Q2, xB, y, z, pT, phi).
# B and C depend on (xB, y, z, pT). xB at a bin center is Q2/(2*M*E*y) with the Pass-2 beam energy.

import math
import re

SPLINE_FILE = "Prepare_Next_Iteration/rho0_Subtracted_5D_V2_4D_xB_Fit_Pars_from_5D_BC_RC_Bayesian_Compute_SplineWeight.txt"
PROTON_MASS = 0.938272
BEAM_ENERGY = 10.6

_CACHE = {}


def _array_block(text, name):
    match = re.search(r"const (?:double|int) " + name + r"\[[^\]]*\](?:\[[^\]]*\])?\s*=\s*\{(.*?)\};", text, re.S)
    if(match is None):
        raise RuntimeError("Missing " + name)
    nums = re.findall(r"[-+]?(?:\d+\.\d*|\d+)(?:[eE][-+]?\d+)?", match.group(1))
    return [float(item) for item in nums]


def _int_const(text, name):
    match = re.search(r"const int " + name + r"\s*=\s*(\d+);", text)
    return int(match.group(1))


def _string_const(text, name):
    match = re.search(r"const std::string " + name + r"\s*=\s*\"([^\"]+)\";", text)
    return match.group(1)


def load_piece(text, tag):
    n = _int_const(text, "n_fit_par_" + tag)
    ndim = _int_const(text, "ndim_fit_par_" + tag)
    npoly = _int_const(text, "n_poly_fit_par_" + tag)
    centers = _array_block(text, "centers_fit_par_" + tag)
    coeffs = _array_block(text, "coeffs_fit_par_" + tag)
    shift = _array_block(text, "shift_fit_par_" + tag)
    scale = _array_block(text, "scale_fit_par_" + tag)
    powers = _array_block(text, "powers_fit_par_" + tag)
    kernel = _string_const(text, "kernel_fit_par_" + tag)
    epsilon = float(re.search(r"const double epsilon_fit_par_" + tag + r"\s*=\s*([0-9eE.+\-]+);", text).group(1))
    if(kernel != "gaussian"):
        raise RuntimeError("Unexpected kernel " + kernel)
    centers = [centers[i * ndim:(i + 1) * ndim] for i in range(n)]
    powers = [powers[i * ndim:(i + 1) * ndim] for i in range(npoly)]
    return {
        "n": n,
        "ndim": ndim,
        "npoly": npoly,
        "centers": centers,
        "coeffs": coeffs,
        "shift": shift,
        "scale": scale,
        "powers": powers,
        "epsilon": epsilon,
    }


def load_spline(path=SPLINE_FILE):
    if(path in _CACHE):
        return _CACHE[path]
    text = open(path).read()
    pieces = {"b": load_piece(text, "b"), "c": load_piece(text, "c")}
    _CACHE[path] = pieces
    return pieces


def evaluate(piece, point):
    total = 0.0
    eps = piece["epsilon"]
    for i, center in enumerate(piece["centers"]):
        r2 = 0.0
        for j in range(piece["ndim"]):
            diff = eps * point[j] - eps * center[j]
            r2 += diff * diff
        total += piece["coeffs"][i] * math.exp(-r2)
    xhat = []
    for j in range(piece["ndim"]):
        xhat.append((point[j] - piece["shift"][j]) / piece["scale"][j])
    for m, power in enumerate(piece["powers"]):
        mono = 1.0
        for j in range(piece["ndim"]):
            mono *= xhat[j] ** int(power[j])
        total += piece["coeffs"][piece["n"] + m] * mono
    return total


def xb_from_q2_y(q2, y):
    return q2 / (2.0 * PROTON_MASS * BEAM_ENERGY * y)


def moments_at(xB, y, z, pT, path=SPLINE_FILE):
    pieces = load_spline(path)
    point = [xB, y, z, pT]
    return evaluate(pieces["b"], point), evaluate(pieces["c"], point)


if(__name__ == "__main__"):
    b_val, c_val = moments_at(0.2, 0.5, 0.4, 0.4)
    print(f"sample B={b_val:.6g} C={c_val:.6g}")
