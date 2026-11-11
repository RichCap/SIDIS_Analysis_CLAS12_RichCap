#!/usr/bin/env python3
# Write the thesis coverage-exclusion tables from the 135 degree records.

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CAMP = os.path.dirname(HERE)
THESIS = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Actual_Thesis_LaTeX_Projects/LaTeX_GitHub/Richard_Capobianco_PhD_Thesis"
OUT = os.path.join(THESIS, "Results/Results_SubSections/Uncertainties_SubSections/Coverage135")
RECORDS = os.path.join(HERE, "coverage_records.json")
NUMBERS = os.path.join(CAMP, "budgets/rerun_refinement_20261108_coverage135/propagate_numbers.json")

GROUPS = [
    ("sampling_fraction", "Coverage_Sampling_Fraction.tex", "tab:CoverageSamplingFraction", "sampling-fraction variations"),
    ("pcal_ep", "Coverage_PCal_Energy_Momentum.tex", "tab:CoveragePCalEP", "PCAL $E/p$ variations"),
    ("electron_vz", "Coverage_Electron_Vertex.tex", "tab:CoverageElectronVertex", "electron-vertex variations"),
    ("pcal_volume", "Coverage_PCal_Volume.tex", "tab:CoveragePCalVolume", "PCAL-volume variations"),
    ("chi2_pid", "Coverage_Chi2_PID.tex", "tab:CoverageChi2PID", "pion $\\chi^{2}_{\\mathrm{PID}}$ variation"),
    ("vertex_separation", "Coverage_Vertex_Separation.tex", "tab:CoverageVertexSeparation", "vertex-separation variations"),
    ("electron_dc_edges", "Coverage_Electron_DC_Edges.tex", "tab:CoverageElectronDCEdges", "electron DC-edge variations"),
    ("pion_dc_edges", "Coverage_Pion_DC_Edges.tex", "tab:CoveragePionDCEdges", "pion DC-edge variations"),
    ("pcal_dead", "Coverage_PCal_Dead.tex", "tab:CoveragePCalDead", "PCAL dead-channel variation"),
    ("sector_pcal", "Coverage_Sector_PCal.tex", "tab:CoverageSectorPCal", "sector-PCAL variation"),
    ("electron_dc_refinement", "Coverage_Electron_DC_Refinement.tex", "tab:CoverageElectronDCRefinement", "electron DC-refinement variations"),
    ("pion_dc_extra", "Coverage_Pion_DC_Extra.tex", "tab:CoveragePionDCExtra", "additional $\\pi^{+}$ DC variation"),
    ("sector", "Coverage_Sector.tex", "tab:CoverageSector", "sector variations"),
    ("phi_binning", "Coverage_Phi_Binning.tex", "tab:CoveragePhiBinning", "$\\phi_h$-binning variation"),
    ("momentum_smearing", "Coverage_Momentum_Smearing.tex", "tab:CoverageMomentumSmearing", "momentum-smearing variation"),
    ("exclusive_rho0", "Coverage_Exclusive_Rho0.tex", "tab:CoverageExclusiveRho0", "exclusive-$\\rho^{0}$ variation"),
    ("acceptance_method", "Coverage_Acceptance_Method.tex", "tab:CoverageAcceptanceMethod", "acceptance-method variations"),
    ("acceptance_threshold", "Coverage_Acceptance_Threshold.tex", "tab:CoverageAcceptanceThreshold", "acceptance-threshold variations"),
    ("bayes_iterations", "Coverage_Bayesian_Iterations.tex", "tab:CoverageBayesianIterations", "Bayesian-iteration variations"),
    ("rc_model", "Coverage_Radiative_Model.tex", "tab:CoverageRadiativeModel", "radiative-correction variations"),
    ("bc_sampling", "Coverage_BC_Sampling.tex", "tab:CoverageBCSampling", "bin-centering sampling variations"),
    ("spline_bc", "Coverage_Spline_BC.tex", "tab:CoverageSplineBC", "spline bin-centering variation"),
    ("physics_injection", "Coverage_Physics_Injection.tex", "tab:CoveragePhysicsInjection", "physics-injection variation"),
    ("acceptance_reweighting", "Coverage_Acceptance_Reweighting.tex", "tab:CoverageAcceptanceReweighting", "acceptance-reweighting variation"),
]


def latex_name(name):
    if(("\\" in name) or ("$" in name)):
        return name
    return name.replace("_", "\\_")


def bin_numbers(key):
    q2y = int(key.split("Q2_y_Bin_")[1].split(")")[0])
    zpt = int(key.split("z_pT_Bin_")[1].split(")")[0])
    return q2y, zpt


def range_text(values):
    if(len(values) == 0):
        return "None"
    values = sorted(values)
    chunks = []
    start = values[0]
    previous = values[0]
    for value in values[1:]:
        if(value == previous + 1):
            previous = value
            continue
        if(start == previous):
            chunks.append("\\mbox{$%d$}" % start)
        else:
            chunks.append("\\mbox{$%d$--$%d$}" % (start, previous))
        start = value
        previous = value
    if(start == previous):
        chunks.append("\\mbox{$%d$}" % start)
    else:
        chunks.append("\\mbox{$%d$--$%d$}" % (start, previous))
    return ", ".join(chunks)


def group_lines(keys):
    by_q2y = {}
    for key in keys:
        q2y, zpt = bin_numbers(key)
        by_q2y.setdefault(q2y, []).append(zpt)
    lines = []
    for q2y in sorted(by_q2y):
        lines.append("\\textbf{%d:} %s" % (q2y, range_text(by_q2y[q2y])))
    return lines


def variation_label(item):
    if(item["sector_id"] != ""):
        sector_id = item["sector_id"]
        if(sector_id.startswith("pipS")):
            number = int(sector_id.replace("pipS", "").replace("o", ""))
            return "Pion Sector %d" % number
        number = int(sector_id.replace("eS", "").replace("o", ""))
        return "Electron Sector %d" % number
    name = latex_name(item["variation_name"])
    if(name == "Zeroth-order unweighted"):
        return "Zeroth-order\\newline unweighted"
    return name


def write_group(handle, items, caption, label):
    handle.write("\\begin{longtable}{p{3.5cm}p{2.2cm}p{8.3cm}}\n")
    handle.write("\\caption{%s The percentage uses the $452$ retained kinematic bins.}\\label{%s}\\\\\n" % (caption, label))
    handle.write("\\toprule\n")
    handle.write("Variation & Excluded & Excluded bins \\\\\n")
    handle.write("\\midrule\n")
    handle.write("\\endfirsthead\n")
    handle.write("\\multicolumn{3}{l}{\\tablename\\ \\thetable\\ continued}\\\\\n")
    handle.write("\\toprule\n")
    handle.write("Variation & Excluded & Excluded bins \\\\\n")
    handle.write("\\midrule\n")
    handle.write("\\endhead\n")
    handle.write("\\bottomrule\n")
    handle.write("\\endfoot\n")
    last_index = len(items) - 1
    for index, item in enumerate(items):
        failed = []
        for key, record in item["records"].items():
            if((record.get("status") != "assessed") or (float(record.get("missing_deg", 0.0)) > 135.0)):
                failed.append(key)
        label_text = variation_label(item)
        if(len(failed) == 0):
            handle.write("%s & 0 (0\\%%) & None \\\\\n" % label_text)
        else:
            excluded = "%d (%.1f\\%%)" % (len(failed), 100.0 * float(len(failed)) / 452.0)
            lines = group_lines(failed)
            final = len(lines) - 1
            for line_index, line in enumerate(lines):
                name = label_text if(line_index == 0) else ""
                count_cell = excluded if(line_index == 0) else ""
                if(line_index == final):
                    handle.write("%s & %s & %s \\\\\n" % (name, count_cell, line))
                else:
                    handle.write("%s & %s & %s \\\\*\n" % (name, count_cell, line))
        if(index != last_index):
            handle.write("\\addlinespace\n")
    handle.write("\\end{longtable}\n")


def write_unavailable(numbers):
    path = os.path.join(OUT, "Sector_Unavailable.tex")
    rows = numbers["sector"]["unavailable_rows"]
    with open(path, "w") as handle:
        handle.write("\\begin{longtable}{ccl}\n")
        handle.write("\\caption{Bins with at least one sector comparison omitted from the RMS. E1--E6 restrict the electron to sectors 1--6, and P1--P6 restrict the $\\pi^{+}$ to sectors 1--6. A label is omitted when that comparison fails the coverage requirement, fails the fit-quality requirement, or is one of the three manual exclusions. A comparison omitted for more than one reason is listed once. A row that lists all twelve labels has no usable comparison. The kinematic ranges are in \\Cref{tab:BinBorders}.}\\label{tab:SectorUnavailable}\\\\\n")
        handle.write("\\toprule\n")
        handle.write("$Q^{2}$--$y$ & $z$--$P_{T}$ & Omitted comparisons \\\\\n")
        handle.write("\\midrule\n")
        handle.write("\\endfirsthead\n")
        handle.write("\\toprule\n")
        handle.write("$Q^{2}$--$y$ & $z$--$P_{T}$ & Omitted comparisons \\\\\n")
        handle.write("\\midrule\n")
        handle.write("\\endhead\n")
        for row in rows:
            handle.write("%d & %d & %s \\\\\n" % (row["q2y"], row["zpt"], ", ".join(row["labels"])))
        handle.write("\\bottomrule\n")
        handle.write("\\end{longtable}\n")
    print("unavailable rows", len(rows))


def main():
    os.makedirs(OUT, exist_ok=True)
    payload = json.load(open(RECORDS))
    numbers = json.load(open(NUMBERS))
    by_source = {}
    for item in payload["inputs"]:
        if(item["role"] != "variation"):
            continue
        by_source.setdefault(item["source_id"], []).append(item)
    for source_id, items in by_source.items():
        items.sort(key=lambda item: item["variation_index"])
    for source_id, filename, label, caption in GROUPS:
        items = by_source[source_id]
        path = os.path.join(OUT, filename)
        with open(path, "w") as handle:
            write_group(handle, items, "Kinematic bins excluded by the $\\phi_h$ coverage requirement for the %s." % caption, label)
        failures = 0
        for item in items:
            for record in item["records"].values():
                if((record.get("status") != "assessed") or (float(record.get("missing_deg", 0.0)) > 135.0)):
                    failures += 1
        print(source_id, "variations", len(items), "coverage exclusions", failures, "file", filename)
    write_unavailable(numbers)


if(__name__ == "__main__"):
    main()
