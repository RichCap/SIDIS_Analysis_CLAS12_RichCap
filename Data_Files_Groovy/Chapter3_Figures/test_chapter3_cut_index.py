#!/usr/bin/env python3
# Lightweight checks of named Chapter 3 plot-time cuts (no HIPO input).
from __future__ import print_function

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import plot_Chapter3_HIPO_hists as plot


def check_equal(got, want, msg):
    if(got != want):
        raise SystemExit("FAIL %s\n  got : %s\n  want: %s" % (msg, got, want))
    print("OK", msg)


def main():
    check_equal(plot.uses_pion_cut([]), False, "none has no pion cut")
    check_equal(plot.uses_pion_cut(["el_dc"]), False, "el_dc has no pion cut")
    check_equal(plot.uses_pion_cut(["pip_dc"]), True, "pip_dc is a pion cut")
    check_equal(plot.uses_pion_cut(["el_dc", "pip_dc"]), True, "el_pip_dc uses a pion cut")

    none_ele = plot.cut_filter([], 0)
    if("kind == 0" not in none_ele):
        raise SystemExit("FAIL none electron filter: %s" % none_ele)
    check_equal(none_ele, "(kind == 0)", "none electron is kind==0 only")

    el_dc = plot.cut_filter(["el_dc"], 0)
    if("e_edge1 > 5.0" not in el_dc):
        raise SystemExit("FAIL el_dc missing electron DC: %s" % el_dc)
    if("p_edge" in el_dc):
        raise SystemExit("FAIL el_dc should not include pion DC: %s" % el_dc)
    print("OK el_dc electron DC only")

    pip_dc = plot.cut_filter(["pip_dc"], 1)
    if("p_edge1 > 2.5" not in pip_dc):
        raise SystemExit("FAIL pip_dc missing pion DC: %s" % pip_dc)
    if("kind == 1" not in pip_dc):
        raise SystemExit("FAIL pip_dc should use pair rows: %s" % pip_dc)
    print("OK pip_dc pair rows")

    both = plot.cut_filter(["el_dc", "pip_dc"], 1)
    if(("e_edge1 > 5.0" not in both) or ("p_edge1 > 2.5" not in both)):
        raise SystemExit("FAIL el_pip_dc missing a DC clause: %s" % both)
    print("OK el_pip_dc both DC")

    had_all = plot.cut_filter(["pip_fd", "chi2pid", "el_dc", "pip_dc", "el_vz", "pcal_emin"], 2)
    for piece in ["kind == 2", "had_status >= 2000", "abs(had_chi2pid) < 3", "e_edge1 > 5.0", "h_edge1 > 2.5", "vz > -8.0", "pcal_energy > 0.06"]:
        if(piece not in had_all):
            raise SystemExit("FAIL all-had missing %s in %s" % (piece, had_all))
    print("OK all-hadron filter")

    names = [name for name, _cuts in plot.PLOT_CONFIGS]
    check_equal(names, ["none", "el_dc", "pip_dc", "el_pip_dc", "pip_fd", "chi2pid", "el_vz", "pcal_emin", "all"], "default config names")
    print("All named-cut checks passed.")
    return 0


if(__name__ == "__main__"):
    sys.exit(main())
