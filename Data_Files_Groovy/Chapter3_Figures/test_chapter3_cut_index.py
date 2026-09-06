#!/usr/bin/env python3
# Lightweight checks of the Chapter 3 cut-index helper (no HIPO input).
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
    check_equal(plot.cut_filter(0, "ele"), "1", "index 0 is no optional cut")
    check_equal(plot.electron_tree_name(0), "ele", "index 0 uses ele")
    check_equal(plot.electron_tree_name(4), "ele", "index 4 (el DC) uses ele")
    check_equal(plot.electron_tree_name(8), "elepip", "index 8 (pion DC) uses elepip")
    check_equal(plot.electron_tree_name(12), "elepip", "index 12 uses elepip")
    check_equal(plot.electron_tree_name(63), "elepip", "index 63 uses elepip")

    f4 = plot.cut_filter(4, "ele")
    if("e_edge1 > 5.0" not in f4):
        raise SystemExit("FAIL index 4 missing electron DC: %s" % f4)
    if("p_edge" in f4):
        raise SystemExit("FAIL index 4 should not include pion DC: %s" % f4)
    print("OK index 4 electron DC only")

    f8 = plot.cut_filter(8, "elepip")
    if("p_edge1 > 2.5" not in f8):
        raise SystemExit("FAIL index 8 missing pion DC: %s" % f8)
    if("e_edge1" in f8):
        raise SystemExit("FAIL index 8 should not include electron DC: %s" % f8)
    print("OK index 8 pion DC only")

    f12 = plot.cut_filter(12, "elepip")
    if(("e_edge1 > 5.0" not in f12) or ("p_edge1 > 2.5" not in f12)):
        raise SystemExit("FAIL index 12 missing a DC clause: %s" % f12)
    print("OK index 12 both DC")

    f63 = plot.cut_filter(63, "elepip")
    for piece in ["pip_status >= 2000", "abs(pip_chi2pid) < 3", "e_edge1 > 5.0", "p_edge1 > 2.5", "vz > -8.0", "pcal_energy > 0.06"]:
        if(piece not in f63):
            raise SystemExit("FAIL index 63 missing %s in %s" % (piece, f63))
    print("OK index 63 all six bits")

    fhad = plot.cut_filter(11, "had")
    if("had_status" not in fhad):
        raise SystemExit("FAIL had tree should use had_status: %s" % fhad)
    if("h_edge1" not in fhad):
        raise SystemExit("FAIL had tree should use h_edge*: %s" % fhad)
    if("pip_status" in fhad):
        raise SystemExit("FAIL had tree should not use pip_status: %s" % fhad)
    print("OK had-tree branch names")

    check_equal(plot.parse_cut_indices(None), [0], "default parse")
    check_equal(plot.parse_cut_indices(["0,4", "8"]), [0, 4, 8], "comma and repeat parse")

    # Tiny TTrees: index 0 fills all rows; index 4 keeps only the electron-DC-pass row.
    import ROOT
    from array import array
    ROOT.gROOT.SetBatch(True)
    tmp = os.path.join(HERE, "_test_cut_index_tmp.root")
    outf = ROOT.TFile(tmp, "RECREATE")
    tree = ROOT.TTree("ele", "ele")
    e1, e2, e3, nph = array("f", [0.0]), array("f", [0.0]), array("f", [0.0]), array("f", [0.0])
    tree.Branch("e_edge1", e1, "e_edge1/F")
    tree.Branch("e_edge2", e2, "e_edge2/F")
    tree.Branch("e_edge3", e3, "e_edge3/F")
    tree.Branch("nphe",    nph, "nphe/F")
    rows = [(6.0, 6.0, 11.0, 10.0), (1.0, 1.0, 1.0, 20.0)]
    for a, b, c, n in rows:
        e1[0], e2[0], e3[0], nph[0] = a, b, c, n
        tree.Fill()
    tree.Write()
    outf.Close()

    rdf0 = ROOT.RDataFrame("ele", tmp).Filter(plot.cut_filter(0, "ele"))
    rdf4 = ROOT.RDataFrame("ele", tmp).Filter(plot.cut_filter(4, "ele"))
    n0 = int(rdf0.Count().GetValue())
    n4 = int(rdf4.Count().GetValue())
    check_equal(n0, 2, "index 0 keeps both fake ele rows")
    check_equal(n4, 1, "index 4 keeps only the passing DC row")
    os.remove(tmp)
    print("OK fake TTree projection")
    print("All cut-index checks passed.")
    return 0


if(__name__ == "__main__"):
    sys.exit(main())
