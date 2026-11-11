#!/usr/bin/env python3
# Put the 135 degree budget numbers into the systematic table and subsection sentences.

import math
import os
import re

import json

CAMP = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign"
THESIS = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Actual_Thesis_LaTeX_Projects/LaTeX_GitHub/Richard_Capobianco_PhD_Thesis"
SUB = os.path.join(THESIS, "Results/Results_SubSections/Uncertainties_SubSections")
TABLE = os.path.join(THESIS, "Results/Results_SubSections/Systematic_Uncertainties.tex")
BUDGET = os.path.join(CAMP, "budgets/rerun_refinement_20261108_coverage135/budget.json")
SHARES = os.path.join(CAMP, "budgets/rerun_refinement_20261108_coverage135/per_bin_source_shares.json")
RANGES = os.path.join(CAMP, "budgets/rerun_refinement_20261108_coverage135/propagate_numbers.json")

LABELS = {
    "sys-sf-band": "sampling_fraction",
    "sys-pcal-ep": "pcal_ep",
    "sys-vz-el": "electron_vz",
    "sys-pcal-vol": "pcal_volume",
    "sys-chi2pid": "chi2_pid",
    "sys-dvz": "vertex_separation",
    "sys-dcfid-el": "electron_dc_edges",
    "sys-dcfid-pip": "pion_dc_edges",
    "sys-pcal-knockout": "pcal_dead",
    "sys-sector-pcal": "sector_pcal",
    "sys-dcfid-ref-el": "electron_dc_refinement",
    "sys-pip-testdc": "pion_dc_extra",
    "sys-sector": "sector",
    "sys-phih-bins": "phi_binning",
    "sys-smear": "momentum_smearing",
    "sys-rho0": "exclusive_rho0",
    "sys-acc-method": "acceptance_method",
    "sys-acc-threshold": "acceptance_threshold",
    "sys-bayes-iter": "bayes_iterations",
    "sys-rc-model": "rc_model",
    "sys-bc-kin": "bc_sampling",
    "sys-bc-iter": "spline_bc",
    "sys-mod-spline": "physics_injection",
    "sys-acc-reweight": "acceptance_reweighting",
}

FILES = {
    "sampling_fraction": "Sys_Sampling_Fraction.tex",
    "pcal_ep": "Sys_PCal_Energy_Momentum.tex",
    "electron_vz": "Sys_Electron_Vertex.tex",
    "pcal_volume": "Sys_PCal_Volume.tex",
    "chi2_pid": "Sys_Chi2_PID_Pion.tex",
    "vertex_separation": "Sys_Vertex_Separation.tex",
    "electron_dc_edges": "Sys_Electron_DC_Fiducial.tex",
    "pion_dc_edges": "Sys_Electron_DC_Fiducial.tex",
    "pcal_dead": "Sys_PCal_Dead_Channels.tex",
    "sector_pcal": "Sys_Sector_PCal.tex",
    "electron_dc_refinement": "Sys_Electron_DC_Refinement.tex",
    "pion_dc_extra": "Sys_Custom_Pion_DC.tex",
    "sector": "Sys_Sector_Dependence.tex",
    "phi_binning": "Sys_Phi_h_Binning.tex",
    "momentum_smearing": "Sys_Momentum_Smearing.tex",
    "exclusive_rho0": "Sys_Exclusive_Rho0.tex",
    "acceptance_method": "Sys_Acceptance_Method.tex",
    "acceptance_threshold": "Sys_Acceptance_Threshold.tex",
    "bayes_iterations": "Sys_Bayesian_Iterations.tex",
    "rc_model": "Sys_Radiative_Model.tex",
    "bc_sampling": "Sys_Iterative_Bin_Centering.tex",
    "spline_bc": "Sys_Iterative_Bin_Centering.tex",
    "physics_injection": "Sys_Modulation_Spline.tex",
    "acceptance_reweighting": "Sys_Acceptance_Reweighting.tex",
}

INPUTS = {
    "Sys_Sampling_Fraction.tex": [("The resulting systematic uncertainties", "Coverage_Sampling_Fraction")],
    "Sys_PCal_Energy_Momentum.tex": [("The resulting systematic uncertainties", "Coverage_PCal_Energy_Momentum")],
    "Sys_Electron_Vertex.tex": [("The resulting systematic uncertainties", "Coverage_Electron_Vertex")],
    "Sys_PCal_Volume.tex": [("The resulting systematic uncertainties", "Coverage_PCal_Volume")],
    "Sys_Chi2_PID_Pion.tex": [("The resulting systematic uncertainties", "Coverage_Chi2_PID")],
    "Sys_Vertex_Separation.tex": [("The resulting systematic uncertainties", "Coverage_Vertex_Separation")],
    "Sys_Electron_DC_Fiducial.tex": [
        ("The electron-edge uncertainties", "Coverage_Electron_DC_Edges"),
        ("The pion-edge uncertainties", "Coverage_Pion_DC_Edges"),
    ],
    "Sys_PCal_Dead_Channels.tex": [("The resulting systematic uncertainties", "Coverage_PCal_Dead")],
    "Sys_Sector_PCal.tex": [("The resulting systematic uncertainties", "Coverage_Sector_PCal")],
    "Sys_Electron_DC_Refinement.tex": [("The resulting systematic uncertainties", "Coverage_Electron_DC_Refinement")],
    "Sys_Custom_Pion_DC.tex": [("The resulting systematic uncertainties", "Coverage_Pion_DC_Extra")],
    "Sys_Sector_Dependence.tex": [("The resulting sector-dependence uncertainties", "Coverage_Sector")],
    "Sys_Phi_h_Binning.tex": [("The resulting systematic uncertainties", "Coverage_Phi_Binning")],
    "Sys_Momentum_Smearing.tex": [("The resulting systematic uncertainties", "Coverage_Momentum_Smearing")],
    "Sys_Exclusive_Rho0.tex": [("The resulting systematic uncertainties", "Coverage_Exclusive_Rho0")],
    "Sys_Acceptance_Method.tex": [("The resulting systematic uncertainties", "Coverage_Acceptance_Method")],
    "Sys_Acceptance_Threshold.tex": [("The resulting systematic uncertainties", "Coverage_Acceptance_Threshold")],
    "Sys_Bayesian_Iterations.tex": [("The resulting systematic uncertainties", "Coverage_Bayesian_Iterations")],
    "Sys_Radiative_Model.tex": [("The resulting systematic uncertainties", "Coverage_Radiative_Model")],
    "Sys_Iterative_Bin_Centering.tex": [
        ("The combined systematic contribution is the RMS of the fifteen", "Coverage_BC_Sampling"),
        ("The resulting RMS shifts across the retained kinematic bins", "Coverage_Spline_BC"),
    ],
    "Sys_Modulation_Spline.tex": [("The resulting systematic uncertainties", "Coverage_Physics_Injection")],
    "Sys_Acceptance_Reweighting.tex": [("The resulting systematic uncertainties", "Coverage_Acceptance_Reweighting")],
}

CELL = re.compile(r"\$([^$]+)\$ \{\\scriptsize\(\$([^$]+)\\%\$\)\}")
NUMBER = re.compile(r"\$(?P<body>[^$]+)\$")


def sig_count(token):
    mantissa = token.split("\\times")[0]
    digits = re.sub(r"[^0-9]", "", mantissa)
    stripped = digits.lstrip("0")
    if(stripped == ""):
        return 1
    return len(stripped)


def format_like(token, value):
    count = sig_count(token)
    number = float(value)
    if(number == 0.0):
        return "0"
    scientific = ("\\times" in token) or (abs(number) < 1.0e-3)
    if(scientific):
        exponent = int(math.floor(math.log10(abs(number))))
        mantissa = number / (10.0 ** exponent)
        text = "%.*g" % (count, mantissa)
        if("." not in text):
            if(count > 1):
                text = text + "." + ("0" * (count - 1))
        return "%s\\times 10^{%d}" % (text, exponent)
    exponent = int(math.floor(math.log10(abs(number))))
    decimals = count - exponent - 1
    if(decimals < 0):
        decimals = 0
    return "%.*f" % (decimals, number)


def format_share(value):
    number = float(value)
    if(number >= 0.01):
        return "%.2f" % number
    return "%.3f" % number


def replace_cells(line, values):
    matches = list(CELL.finditer(line))
    if(len(matches) != 3):
        raise SystemExit("expected three systematic cells, found %d in %s" % (len(matches), line[:80]))
    pieces = []
    cursor = 0
    for index, match in enumerate(matches):
        pieces.append(line[cursor:match.start()])
        rms = format_like(match.group(1), values[index][0])
        share = format_share(values[index][1])
        pieces.append("$%s$ {\\scriptsize($%s\\%%$)}" % (rms, share))
        cursor = match.end()
    pieces.append(line[cursor:])
    return "".join(pieces)


def update_table(budget, shares):
    text = open(TABLE).read()
    lines = text.splitlines(keepends=True)
    updated = []
    seen = set()
    for line in lines:
        label = None
        for key, source_id in LABELS.items():
            if(("hyperref[%s]" % key) in line):
                label = source_id
                break
        if(label is None):
            if(line.startswith("Combined&")):
                combined = budget["combined_rms"]
                numbers = [format_like(token, combined[letter]) for token, letter in (("0.03137", "A"), ("0.1341", "B"), ("0.06021", "C"))]
                line = "Combined& Independent variations& & $%s$ & $%s$ & $%s$ & $>\\,>\\,>$ \\\\\n" % tuple(numbers)
            updated.append(line)
            continue
        values = []
        for letter in ("A", "B", "C"):
            values.append((budget["sources"][label][letter]["rms"], shares["table_shares_percent"][label][letter]))
        updated.append(replace_cells(line, values))
        seen.add(label)
    if(seen != set(LABELS.values())):
        raise SystemExit("table update missed %s" % sorted(set(LABELS.values()) - seen))
    open(TABLE, "w").write("".join(updated))
    print("updated table")


def replace_token(path, old, new_value):
    text = open(path).read()
    formatted = format_like(old, new_value)
    needle = "$%s$" % old
    replacement = "$%s$" % formatted
    if(needle not in text):
        raise SystemExit("missing %s in %s" % (needle, path))
    if(needle == replacement):
        return
    count = text.count(needle)
    text = text.replace(needle, replacement)
    open(path, "w").write(text)
    print("replaced %s -> %s (%d) in %s" % (old, formatted, count, os.path.basename(path)))


def insert_inputs():
    prefix = "\\input{Results/Results_SubSections/Uncertainties_SubSections/Coverage135/"
    for filename, pairs in INPUTS.items():
        path = os.path.join(SUB, filename)
        text = open(path).read()
        for anchor, stem in pairs:
            command = "%s%s}\n\n" % (prefix, stem)
            if(stem in text):
                continue
            if(anchor not in text):
                raise SystemExit("anchor missing in %s: %s" % (filename, anchor))
            text = text.replace(anchor, command + anchor, 1)
        open(path, "w").write(text)
        print("inputs", filename)


def main():
    budget = json.load(open(BUDGET))
    shares = json.load(open(SHARES))
    update_table(budget, shares)
    insert_inputs()
    sentences = [
        ("electron_vz", "0.001855", "A"),
        ("electron_vz", "0.004597", "B"),
        ("electron_vz", "0.003432", "C"),
        ("pcal_volume", "0.007242", "A"),
        ("pcal_volume", "0.005586", "B"),
        ("pcal_volume", "0.004649", "C"),
        ("chi2_pid", "0.01614", "A"),
        ("chi2_pid", "0.02159", "B"),
        ("chi2_pid", "0.01087", "C"),
        ("pion_dc_edges", "0.0005718", "A"),
        ("pion_dc_edges", "0.00525", "B"),
        ("pion_dc_edges", "0.003682", "C"),
        ("electron_dc_refinement", "0.001448", "A"),
        ("electron_dc_refinement", "0.005492", "B"),
        ("electron_dc_refinement", "0.004176", "C"),
        ("phi_binning", "0.001678", "A"),
        ("phi_binning", "0.01119", "B"),
        ("phi_binning", "0.007454", "C"),
        ("acceptance_threshold", "0.0004082", "A"),
        ("acceptance_threshold", "0.005222", "B"),
        ("acceptance_threshold", "0.003914", "C"),
        ("acceptance_reweighting", "0.004974", "A"),
        ("acceptance_reweighting", "0.1101", "B"),
        ("acceptance_reweighting", "0.03161", "C"),
        ("acceptance_method", "0.01244", "A"),
        ("acceptance_method", "0.01347", "B"),
        ("acceptance_method", "0.008717", "C"),
        ("physics_injection", "0.01245", "A"),
        ("physics_injection", "0.02262", "B"),
        ("physics_injection", "0.0132", "C"),
        ("sector", "0.01444", "A"),
        ("sector", "0.05694", "B"),
        ("sector", "0.03845", "C"),
        ("spline_bc", "0.006309", "A"),
        ("spline_bc", "0.01257", "B"),
        ("spline_bc", "0.009539", "C"),
        ("bc_sampling", "0.005931", "A"),
        ("bc_sampling", "0.01327", "B"),
        ("bc_sampling", "0.009063", "C"),
    ]
    for source_id, old, letter in sentences:
        path = os.path.join(SUB, FILES[source_id])
        replace_token(path, old, budget["sources"][source_id][letter]["rms"])
    ranges = json.load(open(RANGES))["ranges"]
    endpoints = [
        ("Sys_Electron_Vertex.tex", "0.059191", ranges["electron_vz"]["B"]["max"]),
        ("Sys_Electron_DC_Fiducial.tex", "0.051615", ranges["pion_dc_edges"]["B"]["max"]),
        ("Sys_Electron_DC_Fiducial.tex", "0.026545", ranges["pion_dc_edges"]["C"]["max"]),
        ("Sys_Electron_DC_Refinement.tex", "0.05662", ranges["electron_dc_refinement"]["B"]["max"]),
        ("Sys_Phi_h_Binning.tex", "0.085235", ranges["phi_binning"]["B"]["max"]),
        ("Sys_Acceptance_Threshold.tex", "0.047093", ranges["acceptance_threshold"]["B"]["max"]),
    ]
    for filename, old, value in endpoints:
        replace_token(os.path.join(SUB, filename), old, value)


if(__name__ == "__main__"):
    main()
