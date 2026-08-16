#!/usr/bin/env python3

import argparse
import os
import re
import sys


# --------------------------------------------------------------------------------------
# Spline-export helpers (wrap farm SciPy 1.16.2 C++; do not rebuild RBF coefficients)
# --------------------------------------------------------------------------------------

def _script_dir():
    return os.path.dirname(os.path.abspath(__file__))

def _default_spline_dir():
    return os.path.dirname(_script_dir())

def _artifact_stem(args):
    return f"{args.output_prefix}_{args.dimension_mode}_{args.fit_set}"

def _txt_path(args):
    return os.path.join(args.spline_dir, f"{_artifact_stem(args)}_Compute_SplineWeight.txt")

def _npz_path(args, y_par):
    return os.path.join(args.spline_dir, f"{_artifact_stem(args)}_{y_par}.npz")

def _extract_header_field(text, label):
    mm = re.search(rf"^// {re.escape(label)}:?\s*(.+)$", text, flags=re.MULTILINE)
    return (None if(mm is None) else mm.group(1).strip())

def _strip_compute_spline_weight(body):
    start = body.find("\ndouble ComputeSplineWeight(")
    if(start < 0):
        start = body.find("double ComputeSplineWeight(")
    if(start < 0):
        return body.rstrip() + "\n"
    return body[:start].rstrip() + "\n"

def _adapt_exported_cpp(raw_txt):
    # Keep the farm SciPy 1.16.2 evaluator bodies. Drop ROOT-only includes/weight helper.
    lines = raw_txt.splitlines(True)
    kept = []
    skip_includes = True
    for line in lines:
        stripped = line.strip()
        if(skip_includes):
            if(stripped.startswith("#include")):
                continue
            if(stripped == ""):
                skip_includes = False
                continue
            if(stripped.startswith("//")):
                kept.append(line)
                continue
            skip_includes = False
        kept.append(line)
    return _strip_compute_spline_weight("".join(kept))

def _verify_txt_is_4d_xb(raw_txt, txt_path):
    header_mode = _extract_header_field(raw_txt, "Dimension mode")
    dim_modes = re.findall(r'const std::string dim_mode_fit_par_[abc] = "([^"]+)";', raw_txt)
    if((header_mode is not None) and (header_mode != "4D_xB")):
        print(f"ERROR: {txt_path} header Dimension mode is '{header_mode}', expected 4D_xB.", file=sys.stderr)
        sys.exit(1)
    if(not dim_modes):
        print(f"ERROR: {txt_path} has no dim_mode_fit_par_* constants.", file=sys.stderr)
        sys.exit(1)
    if(any(mm != "4D_xB" for mm in dim_modes)):
        print(f"ERROR: {txt_path} dim_mode constants are {dim_modes}, expected all 4D_xB.", file=sys.stderr)
        sys.exit(1)
    for fn in ["ComputeSplineA", "ComputeSplineB", "ComputeSplineC"]:
        if(fn not in raw_txt):
            print(f"ERROR: {txt_path} is missing {fn}.", file=sys.stderr)
            sys.exit(1)

def _verify_npz_metadata(args):
    try:
        import numpy as np
    except ImportError:
        print("WARNING: numpy is not available; skipping .npz metadata checks.", file=sys.stderr)
        return
    first_centers = {}
    for y_par in ["Fit_Par_A", "Fit_Par_B", "Fit_Par_C"]:
        path = _npz_path(args, y_par)
        if(not os.path.isfile(path)):
            print(f"WARNING: Missing {path}; skipping .npz check for {y_par}.", file=sys.stderr)
            continue
        data = np.load(path, allow_pickle=True)
        dim_mode = str(data["dimension_mode"])
        if(dim_mode != "4D_xB"):
            print(f"ERROR: {path} dimension_mode='{dim_mode}', expected 4D_xB.", file=sys.stderr)
            sys.exit(1)
        points = data["points"]
        if((points.ndim != 2) or (points.shape[1] != 4)):
            print(f"ERROR: {path} points shape {points.shape} is not (N, 4) for 4D_xB.", file=sys.stderr)
            sys.exit(1)
        first_centers[y_par] = [float(vv) for vv in points[0]]
        print(f"  npz {y_par}: kernel={data['kernel']} epsilon={data['epsilon']} log_space={data['log_space']} n={data['n_points']} first_center={first_centers[y_par]}")
    names = list(first_centers.keys())
    for name in names[1:]:
        if(any(abs(aa - bb) > 1.0e-12 for aa, bb in zip(first_centers[names[0]], first_centers[name]))):
            print(f"ERROR: first training center differs between {names[0]} and {name}.", file=sys.stderr)
            sys.exit(1)

def _verify_txt_first_center_is_xb(adapted_cpp):
    mm = re.search(r"const double centers_fit_par_a\[\d+\]\[\d+\] = \{\s*\{([^}]+)\}", adapted_cpp)
    if(mm is None):
        print("WARNING: could not parse first Fit_Par_A center from the export.", file=sys.stderr)
        return
    vals = [float(tok) for tok in mm.group(1).split(",")]
    # 4D_xB first coordinate is xB (~0.1-0.6), not Q2 (~2-8).
    if(vals[0] > 1.5):
        print(f"ERROR: first A center starts with {vals[0]:.6g}, which looks like Q2, not xB. 4D_xB packing must be [xB, y, z, pT].", file=sys.stderr)
        sys.exit(1)
    print(f"  txt first A center = {vals}  (4D_xB: xB, y, z, pT)")


# --------------------------------------------------------------------------------------
# Code generation
# --------------------------------------------------------------------------------------

def write_generated_files(args, adapted_cpp, raw_txt):
    out_base_name = args.out_base_name
    os.makedirs(args.out_dir_hpp, exist_ok=True)
    os.makedirs(args.out_dir_cpp, exist_ok=True)

    hpp_path = os.path.join(args.out_dir_hpp, f"{out_base_name}.hpp")
    cpp_path = os.path.join(args.out_dir_cpp, f"{out_base_name}.cpp")

    dim_mode = _extract_header_field(raw_txt, "Dimension mode") or args.dimension_mode
    fit_set = _extract_header_field(raw_txt, "Fit set") or args.fit_set
    gen_on = _extract_header_field(raw_txt, "Generated on") or "unknown"

    with open(hpp_path, "w") as hpp:
        hpp.write(f"""#pragma once

// Auto-generated. DO NOT EDIT BY HAND.
// Generated by Create_cpp_Compatible_Files_for_EvGen.py
// Source: farm SciPy 1.16.2 export (*_Compute_SplineWeight.txt)
// Dimension mode: {dim_mode}
// Fit set: {fit_set}
// Farm export generated on {gen_on}
//
// 4D_xB evaluation order inside ComputeSplineA/B/C is [xB, y, z, pT].
// The Q2 argument is unused in 4D_xB (kept to match the exporter signature).
// Dual coefficients are copied from the farm export; they are not rebuilt here.

#include <cmath>
#include <string>

namespace sidis::sf::set::measured_tables {{

double ComputeSplineA(double Q2, double xB, double y, double z, double pT);
double ComputeSplineB(double Q2, double xB, double y, double z, double pT);
double ComputeSplineC(double Q2, double xB, double y, double z, double pT);

}} // namespace sidis::sf::set::measured_tables
""")

    with open(cpp_path, "w") as cpp:
        cpp.write(f"""// Auto-generated. DO NOT EDIT BY HAND.
// Generated by Create_cpp_Compatible_Files_for_EvGen.py
// Source: farm SciPy 1.16.2 export (*_Compute_SplineWeight.txt)
// Dimension mode: {dim_mode}
// Fit set: {fit_set}
// Farm export generated on {gen_on}

#include "sidis/sf_set/{out_base_name}.hpp"

#include <cmath>
#include <string>

namespace sidis::sf::set::measured_tables {{

""")
        cpp.write(adapted_cpp)
        if(not adapted_cpp.endswith("\n")):
            cpp.write("\n")
        cpp.write("\n} // namespace sidis::sf::set::measured_tables\n")

    return hpp_path, cpp_path


# --------------------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Wrap a farm-exported 4D_xB Compute_SplineWeight.txt into EvGen .hpp/.cpp evaluators for A, B, and C. Does not rebuild RBF coefficients.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-sd", "--spline_dir",
                        default=_default_spline_dir(),
                        type=str,
                        help="Directory containing the farm-exported spline artifacts (.txt and optional .npz).")
    parser.add_argument("-o", "--output_prefix",
                        default="rho0_Subtracted_5D_V2",
                        type=str,
                        help="Prefix used by Create_Continuous_4D_Moments_From_JSON.py when naming spline artifacts.")
    parser.add_argument("-dm", "--dimension_mode",
                        default="4D_xB",
                        type=str,
                        help="Spline dimensionality. Only 4D_xB is supported. 4D and 5D are legacy and abort.")
    parser.add_argument("-f", "--fit_set",
                        default="Fit_Pars_from_5D_BC_RC_Bayesian",
                        type=str,
                        help="Fit-set token used in the spline artifact names.")
    parser.add_argument("-odh", "--out_dir_hpp",
                        default="Symbolic_Path_to_HPP_EvGen_Directory",
                        # default="/w/hallb-scshelf2102/clas12/richcap/Radiative_MC/SIDIS_RC_EvGen_richcap/sidis/include/sidis/sf_set",
                        type=str,
                        help="Directory to write the generated '.hpp' file.")
    parser.add_argument("-odc", "--out_dir_cpp",
                        default="Symbolic_Path_to_CPP_EvGen_Directory",
                        # default="/w/hallb-scshelf2102/clas12/richcap/Radiative_MC/SIDIS_RC_EvGen_richcap/sidis/src/sf_set",
                        type=str,
                        help="Directory to write the generated '.cpp' file.")
    parser.add_argument("-obn", "--out_base_name",
                        default="richcap_measured_sf_tables",
                        help="Base filename (no extension) for generated files.")

    args = parser.parse_args()
    args.spline_dir = os.path.abspath(args.spline_dir)

    if(str(args.dimension_mode).strip() != "4D_xB"):
        print(f"ERROR: dimension_mode='{args.dimension_mode}' is a legacy spline mode. This EvGen generator only supports 4D_xB. 4D and 5D packs are not generated.", file=sys.stderr)
        sys.exit(1)

    txt_path = _txt_path(args)
    if(not os.path.isfile(txt_path)):
        print(f"ERROR: Missing farm SciPy 1.16.2 Compute_SplineWeight.txt: {txt_path}. If you have new .npz files, generate that txt on the farm with Create_Continuous_4D_Moments_From_JSON.py -gcO/--generate_spline_code_only. This script does not rebuild RBF coefficients.", file=sys.stderr)
        sys.exit(1)

    with open(txt_path, "r") as handle:
        raw_txt = handle.read()

    print("Wrapping farm export (no RBF rebuild):")
    print(f"  txt = {txt_path}")
    _verify_txt_is_4d_xb(raw_txt, txt_path)
    _verify_npz_metadata(args)

    adapted_cpp = _adapt_exported_cpp(raw_txt)
    _verify_txt_first_center_is_xb(adapted_cpp)

    if("TMath" in adapted_cpp):
        print("ERROR: adapted C++ still contains TMath; refuse to write EvGen sources.", file=sys.stderr)
        sys.exit(1)
    if("ComputeSplineWeight" in adapted_cpp):
        print("ERROR: adapted C++ still contains ComputeSplineWeight; refuse to write EvGen sources.", file=sys.stderr)
        sys.exit(1)

    hpp_path, cpp_path = write_generated_files(args, adapted_cpp, raw_txt)

    print("Wrote:")
    print(f"\thpp_path = {hpp_path}")
    print(f"\tcpp_path = {cpp_path}")


if(__name__ == "__main__"):
    main()
