#!/usr/bin/env python3
# Regenerate the thesis bin-border listing from the live Y_bin rectangles.
import argparse
import os
import sys

_BOOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if(_BOOT not in sys.path):
    sys.path.insert(0, _BOOT)

from Binning_Dictionaries import Full_Bin_Definition_Array
from MyCommonAnalysisFunction_richcap import (
    Get_Num_of_z_pT_Bins_w_Migrations,
    Get_z_pT_Bin_Corners,
    skip_condition_z_pT_bins,
)

_THESIS = os.path.join(_BOOT, "Actual_Thesis_LaTeX_Projects")
DEFAULT_OUTPUTS = [
    os.path.join(_THESIS, "LaTeX_GitHub", "Richard_Capobianco_PhD_Thesis", "Appendix_Sections", "Bin_Borders_Q2_y_z_pT_Bins.tex"),
    os.path.join(_THESIS, "Richard_Capobianco_PhD_Thesis", "Appendix_Sections", "Bin_Borders_Q2_y_z_pT_Bins.tex"),
    os.path.join(_THESIS, "LaTeX_GitHub", "DNP_2026_Release_Note", "Appendix_Sections", "Bin_Borders_Q2_y_z_pT_Bins.tex"),
    os.path.join(_THESIS, "DNP_2026_Release_Note", "Appendix_Sections", "Bin_Borders_Q2_y_z_pT_Bins.tex"),
]


def format_edge(value):
    return "%7.2f" % float(value)


def render_listing():
    lines = []
    lines.append("The following information describes the borders for the kinematic bins used in this analysis.")
    lines.append("")
    lines.append("====================================================================")
    lines.append("| Q2-y Bin (#) Borders:     [Q2_max, Q2_min, y_max, y_min]         |")
    lines.append("====================================================================")
    lines.append("|'Q2-y=#, z-pT=#':      |  z_max  |   z_min  |  pT_max  |  pT_min  |")
    lines.append("====================================================================")
    lines.append("")
    for q2y in range(1, 18):
        q2_key    = "Q2-y=%d, Q2-y" % q2y
        q2_border = Full_Bin_Definition_Array[q2_key]
        q2_text   = ", ".join([format_edge(value).strip() for value in q2_border])
        total     = int(Get_Num_of_z_pT_Bins_w_Migrations(Q2_y_Bin_Num_In=q2y)[0])
        lines.append("====================================================================")
        lines.append("| Q2-y Bin (%d) Borders:     [%s] |" % (q2y, q2_text))
        lines.append("====================================================================")
        for zpt in range(1, total + 1):
            corners = Get_z_pT_Bin_Corners(z_pT_Bin_Num=zpt, Q2_y_Bin_Num=q2y)
            z_max, z_min, pt_max, pt_min = corners[0], corners[1], corners[2], corners[3]
            label   = "Q2-y=%d, z-pT=%d" % (q2y, zpt)
            cells   = " | ".join([format_edge(z_max), format_edge(z_min), format_edge(pt_max), format_edge(pt_min)])
            status  = " Skipped" if(skip_condition_z_pT_bins(q2y, zpt)) else ""
            lines.append("|%-22s |%s |%s" % (("'%s':" % label), cells, status))
            lines.append("--------------------------------------------------------------------")
        lines.append("")
    return "\n".join(lines) + "\n"


def check_listing(text):
    if("OVERFLOW" in text):
        raise SystemExit("listing still contains OVERFLOW")
    required = [
        "Q2-y=4, z-pT=4",
        "0.50",
        "0.65",
        "Q2-y=4, z-pT=24",
        "Q2-y=4, z-pT=30",
        "Q2-y=12, z-pT=20",
        "Skipped",
    ]
    for token in required:
        if(token not in text):
            raise SystemExit("listing missing %s" % token)
    # Column checks are on the rendered rows, not on every 0.50 in the file.
    rows = {}
    for line in text.splitlines():
        if(("Q2-y=4, z-pT=" in line) or ("Q2-y=12, z-pT=" in line)):
            rows[line.split("'")[1]] = line
    expect_edges = {
        "Q2-y=4, z-pT=4":   ("0.50", "0.38"),
        "Q2-y=4, z-pT=10":  ("0.50", "0.38"),
        "Q2-y=4, z-pT=5":   ("0.65", "0.50"),
        "Q2-y=4, z-pT=17":  ("0.65", "0.50"),
        "Q2-y=4, z-pT=6":   ("0.70", "0.65"),
        "Q2-y=4, z-pT=24":  ("0.70", "0.65"),
        "Q2-y=4, z-pT=30":  ("0.70", "0.65"),
        "Q2-y=12, z-pT=14": ("0.50", "0.36"),
        "Q2-y=12, z-pT=5":  ("0.60", "0.50"),
        "Q2-y=12, z-pT=20": ("0.60", "0.50"),
    }
    for key, (pt_max, pt_min) in expect_edges.items():
        line = rows[key]
        if((pt_max not in line) or (pt_min not in line)):
            raise SystemExit("bad edges for %s: %s" % (key, line))
    for key in ["Q2-y=4, z-pT=6", "Q2-y=4, z-pT=24", "Q2-y=4, z-pT=30", "Q2-y=12, z-pT=5", "Q2-y=12, z-pT=20"]:
        if("Skipped" not in rows[key]):
            raise SystemExit("expected Skipped on %s" % key)
    for key in ["Q2-y=4, z-pT=10", "Q2-y=4, z-pT=17", "Q2-y=12, z-pT=14"]:
        if("Skipped" in rows[key]):
            raise SystemExit("did not expect Skipped on %s" % key)


def main():
    parser = argparse.ArgumentParser(description="Write the live z-pT bin-border listing.")
    parser.add_argument("-o", "--output", action="append", default=None, help="Output path. Repeatable. Default is the thesis and note copies.")
    parser.add_argument("-c", "--check_only", action="store_true", help="Render and check without writing.")
    args = parser.parse_args()
    text = render_listing()
    check_listing(text)
    outputs = args.output if(args.output) else DEFAULT_OUTPUTS
    if(args.check_only):
        print("bin-border listing checks passed (%d lines)" % len(text.splitlines()))
        return
    for path in outputs:
        folder = os.path.dirname(path)
        if(not os.path.isdir(folder)):
            raise SystemExit("missing directory %s" % folder)
        handle = open(path, "w")
        handle.write(text)
        handle.close()
        print(path)
    print("wrote %d listings" % len(outputs))


if(__name__ == "__main__"):
    main()
