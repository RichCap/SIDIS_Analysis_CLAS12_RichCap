#!/usr/bin/env python3
# Checks ROOT Divide and the Spline-only switch. Does not unfold or open a response file.

import math
import sys

import ROOT

from spline_amplitude_correction import (
    divide_spline_active,
    divide_spline_histogram,
    histograms_match_for_divide,
    output_root_with_weight,
    prepare_spline_histogram,
    unweighted_spline_counterpart,
)

ROOT.TH1.AddDirectory(0)


def near(left, right):
    return abs(float(left) - float(right)) < 1e-6


def require(condition, message):
    if(not condition):
        raise SystemExit(message)


def test_names_and_switch():
    require(unweighted_spline_counterpart("response_(Spline)") == "response", "Spline suffix was not removed")
    require(unweighted_spline_counterpart("response_(AccSpline)") == "", "AccSpline was treated as Spline")
    require(unweighted_spline_counterpart("slice_(Increment='434')_(Spline)") == "slice_(Increment='434')", "slice suffix was not removed")
    require(divide_spline_active("Spline", "auto") is True, "auto Spline was off")
    require(divide_spline_active("AccSpline", "auto") is False, "auto AccSpline was on")
    require(divide_spline_active("Spline", "off") is False, "off still divided")
    try:
        divide_spline_active("AccSpline", "on")
    except ValueError:
        pass
    else:
        raise SystemExit("on accepted AccSpline")
    require(output_root_with_weight("out.root", "Spline", True) == "out_WSpline_DivUnw.root", "divided output name is wrong")
    require(output_root_with_weight("out_WSpline.root", "Spline", True) == "out_WSpline_DivUnw.root", "existing weight suffix was not extended")
    require(output_root_with_weight("out.root", "Spline", False) == "out_WSpline.root", "off output name changed")
    require(output_root_with_weight("out.root", "AccSpline", True) == "out_WAccSpline.root", "AccSpline received _DivUnw")


def test_root_divide():
    weighted = ROOT.TH1D("spline_num", "spline_num", 2, 0, 2)
    unweighted = ROOT.TH1D("spline_den", "spline_den", 2, 0, 2)
    weighted.SetBinContent(0, 4)
    weighted.SetBinError(0, 2)
    unweighted.SetBinContent(0, 2)
    unweighted.SetBinError(0, 1)
    weighted.SetBinContent(1, 9)
    weighted.SetBinError(1, 3)
    unweighted.SetBinContent(1, 3)
    unweighted.SetBinError(1, 1)
    weighted.SetBinContent(2, 5)
    weighted.SetBinError(2, 1)
    unweighted.SetBinContent(2, 0)
    unweighted.SetBinError(2, 0)
    weighted.SetBinContent(3, 0)
    weighted.SetBinError(3, 0)
    unweighted.SetBinContent(3, 0)
    unweighted.SetBinError(3, 0)
    divided = divide_spline_histogram(weighted, unweighted)
    root_two = math.sqrt(2.0)
    require(divided is not None, "matching histograms were rejected")
    require(near(divided.GetBinContent(0), 2.0) and near(divided.GetBinError(0), root_two), "underflow ratio mismatch")
    require(near(divided.GetBinContent(1), 3.0) and near(divided.GetBinError(1), root_two), "bin ratio mismatch")
    require((divided.GetBinContent(2) == 0.0) and (divided.GetBinError(2) == 0.0), "zero denominator was not cleared")
    require((divided.GetBinContent(3) == 0.0) and (divided.GetBinError(3) == 0.0), "empty overflow was not cleared")
    require(near(weighted.GetBinContent(1), 9.0) and near(weighted.GetBinError(1), 3.0), "numerator was modified")
    kept = ROOT.TH1D("kept", "kept", 2, 0, 2)
    kept.SetBinContent(1, 4)
    kept.SetBinError(1, 2)
    wider = ROOT.TH1D("wider", "wider", 3, 0, 3)
    require(histograms_match_for_divide(kept, wider) is False, "different bin counts were accepted")
    direct = ROOT.TH1D("direct", "direct", 2, 0, 2)
    direct.SetBinContent(1, 4)
    direct.SetBinError(1, 2)
    require((direct.Divide(wider) is False) and near(direct.GetBinContent(1), 4.0) and near(direct.GetBinError(1), 2.0), "ROOT Divide changed a mismatched histogram")
    other_edges = ROOT.TH1D("edges", "edges", 2, 0, 4)
    other_edges.SetBinContent(1, 2)
    require(histograms_match_for_divide(kept, other_edges) is False, "different edges were accepted")
    require(divide_spline_histogram(kept, other_edges) is None, "edge mismatch was divided")
    require(near(kept.GetBinContent(1), 4.0) and near(kept.GetBinError(1), 2.0), "rejected division modified the numerator")
    num2 = ROOT.TH2D("num2", "num2", 1, 0, 1, 1, 0, 1)
    den2 = ROOT.TH2D("den2", "den2", 1, 0, 1, 1, 0, 1)
    num2.SetBinContent(1, 1, 8)
    num2.SetBinError(1, 1, 2)
    den2.SetBinContent(1, 1, 2)
    den2.SetBinError(1, 1, 1)
    divided2 = divide_spline_histogram(num2, den2)
    require(divided2 is not None, "TH2 division failed")
    require(near(divided2.GetBinContent(1, 1), 4.0) and near(divided2.GetBinError(1, 1), math.sqrt(5.0)), "TH2 ratio mismatch")
    untouched = ROOT.TH1D("untouched", "untouched", 1, 0, 1)
    untouched.SetBinContent(1, 9)
    untouched.SetBinError(1, 3)
    same = prepare_spline_histogram(untouched, unweighted, False)
    require(same is untouched, "off mode replaced the histogram")
    require(near(same.GetBinContent(1), 9.0) and near(same.GetBinError(1), 3.0), "off mode changed the histogram")


def main():
    test_names_and_switch()
    test_root_divide()
    print("spline amplitude correction test ok")
    return 0


if(__name__ == "__main__"):
    sys.exit(main())
