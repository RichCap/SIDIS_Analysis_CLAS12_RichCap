#!/usr/bin/env python3
# Reporting tables for the existing systematic budget. Does not refit or rewrite budget.json.

import json
import math
import os
import re

CAMP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "physics_campaign")
BUDGET_PATH = os.path.join(CAMP, "budgets", "rerun_20261106_sector_12_23", "budget.json")
EXCLUSIONS_PATH = os.path.join(CAMP, "budgets", "sector_fit_exclusions_20261106.json")
BORDER_PATH = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Actual_Thesis_LaTeX_Projects/LaTeX_GitHub/Richard_Capobianco_PhD_Thesis/Appendix_Sections/Bin_Borders_Q2_y_z_pT_Bins.tex"
TEX_PATH = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Actual_Thesis_LaTeX_Projects/LaTeX_GitHub/Richard_Capobianco_PhD_Thesis/Appendix_Sections/Systematic_Comparison_Tables.tex"
REVIEW_DIR = os.path.join(CAMP, "review_comparisons")
LETTERS = ("A", "B", "C")
LETTER_NAME = {"A": "A_0", "B": "cosphi", "C": "cos2phi"}


def load_json(path):
    with open(path) as handle:
        return json.load(handle)


def load_fit(rel, key):
    path = os.path.join(CAMP, rel)
    payload = load_json(path)
    if(key not in payload):
        raise SystemExit("%s has no %s" % (rel, key))
    return path, payload[key]


def load_sector_exclusions():
    payload = load_json(EXCLUSIONS_PATH)
    exclusions = {}
    for var_id, bins in payload["exclusions"].items():
        exclusions[var_id] = set(bins)
    return exclusions


def usable_sector(cell):
    if(not isinstance(cell, dict)):
        return False
    ndf = cell.get("NDF")
    if((ndf is None) or (float(ndf) < 1.0)):
        return False
    for letter in LETTERS:
        value = cell.get("Fit_Par_%s" % letter)
        if((not isinstance(value, (int, float))) or (not math.isfinite(float(value)))):
            return False
    if((abs(float(cell["Fit_Par_B"])) > 10.0) or (abs(float(cell["Fit_Par_C"])) > 10.0) or (abs(float(cell["Fit_Par_A"])) < 1.0)):
        return False
    return True


def rms(values):
    count = len(values)
    if(count == 0):
        return None
    total = 0.0
    for value in values:
        total += float(value) * float(value)
    return math.sqrt(total / float(count))


def bin_key(q2y_bin, zpt_bin):
    return "(Q2_y_Bin_%d)-(z_pT_Bin_%d)" % (int(q2y_bin), int(zpt_bin))


def parse_bin_key(key):
    match = re.fullmatch(r"\(Q2_y_Bin_(\d+)\)-\(z_pT_Bin_(\d+)\)", key)
    return int(match.group(1)), int(match.group(2))


def read_border_rows(path):
    rows = []
    skipped = []
    pattern = re.compile(r"^\s*(\d+)\s*--\s*(\d+)\s*&")
    with open(path) as handle:
        for line in handle:
            match = pattern.match(line)
            if(match is None):
                continue
            q2y_bin = int(match.group(1))
            zpt_bin = int(match.group(2))
            if("Skipped" in line):
                skipped.append(bin_key(q2y_bin, zpt_bin))
            else:
                rows.append(bin_key(q2y_bin, zpt_bin))
    return rows, skipped


def converted(cell, letter, scale, coeff):
    value = float(cell["Fit_Par_%s" % letter])
    error = float(cell["Fit_Par_%s_ERR" % letter])
    if(letter == "A"):
        return coeff * scale * value, abs(coeff * scale * error)
    return value, abs(error)


def one_comparison(base_cell, var_cell, letter, scale, base_coeff, var_coeff):
    if((base_cell is None) or (var_cell is None)):
        return None
    if(("Fit_Par_%s" % letter) not in base_cell or ("Fit_Par_%s" % letter) not in var_cell):
        return None
    if(("Fit_Par_%s_ERR" % letter) not in base_cell or ("Fit_Par_%s_ERR" % letter) not in var_cell):
        return None
    baseline, base_err = converted(base_cell, letter, scale, base_coeff)
    varied, var_err = converted(var_cell, letter, scale, var_coeff)
    if((not math.isfinite(baseline)) or (not math.isfinite(varied)) or (not math.isfinite(base_err)) or (not math.isfinite(var_err))):
        return None
    delta = varied - baseline
    sigma = math.sqrt((var_err * var_err) + (base_err * base_err))
    percent = None
    if(baseline != 0.0):
        percent = 100.0 * delta / abs(baseline)
    return {"delta": delta, "sigma": sigma, "percent": percent, "baseline": baseline, "varied": varied}


def histo_name(kind, q2y_bin, zpt_bin, smear):
    if(kind == "5D"):
        return "(MultiDim_5D_Histo)_(Bayesian)_(SMEAR=%s)_(Q2_y_Bin_%d)_(z_pT_Bin_%d)_(MultiDim_Q2_y_z_pT_phi_h)" % (smear, q2y_bin, zpt_bin)
    tag = {"Bayesian": "Bayesian", "Bin": "Bin", "RC": "RC_Bayesian", "BC": "BC_RC_Bayesian"}[kind]
    return "(MultiDim_3D_Histo)_(%s)_(SMEAR=%s)_(Q2_y_Bin_%d)_(z_pT_Bin_%d)_(MultiDim_z_pT_Bin_Y_bin_phi_t)" % (tag, smear, q2y_bin, zpt_bin)


def assign_ranks(pairs):
    # pairs are (index, value). Equal values share the better rank and the next number is skipped.
    ordered = sorted(pairs, key=lambda row: (-row[1], row[0]))
    ranks = {}
    cursor = 0
    while(cursor < len(ordered)):
        end = cursor + 1
        while((end < len(ordered)) and (ordered[end][1] == ordered[cursor][1])):
            end += 1
        rank_number = cursor + 1
        for slot in range(cursor, end):
            ranks[ordered[slot][0]] = rank_number
        cursor = end
    return ranks


def fmt_e(value, decimals):
    absolute = abs(value)
    exponent = int(math.floor(math.log10(absolute)))
    mantissa = value / (10.0 ** exponent)
    text = "%.*f" % (decimals, mantissa)
    if(abs(float(text)) >= 10.0):
        exponent += 1
        mantissa = value / (10.0 ** exponent)
        text = "%.*f" % (decimals, mantissa)
    return "%se%d" % (text, exponent)


def fmt_plain(value, fixed_decimals, e_decimals, zero_text):
    if(value is None):
        return "N/A"
    if(not math.isfinite(value)):
        return "N/A"
    if(value == 0.0):
        return zero_text
    absolute = abs(value)
    if((absolute < 0.01) or (absolute >= 100.0)):
        return fmt_e(value, e_decimals)
    return "%.*f" % (fixed_decimals, value)


def fmt_num(value):
    return fmt_plain(value, 3, 2, "0.000")


def fmt_sigma(value):
    return fmt_plain(value, 2, 1, "0.00")


def fmt_pct(value):
    if(value is None):
        return "N/A"
    if(not math.isfinite(value)):
        return "N/A"
    if(value == 0.0):
        return "0.00\\%"
    absolute = abs(value)
    if((absolute < 0.01) or (absolute >= 100.0)):
        return "%s\\%%" % fmt_e(value, 2)
    if(absolute >= 10.0):
        decimals = 1
    elif(absolute >= 1.0):
        decimals = 2
    elif(absolute >= 0.1):
        decimals = 3
    else:
        decimals = 4
    return "%.*f\\%%" % (decimals, value)


def variation_cell(records):
    if(len(records) == 0):
        return "N/A"
    if(all(record is None for record in records)):
        return "N/A"
    lines = []
    for record in records:
        if(record is None):
            lines.append("N/A")
            lines.append("N/A")
        else:
            lines.append("%s $\\pm$ %s" % (fmt_num(record["delta"]), fmt_sigma(record["sigma"])))
            lines.append(fmt_pct(record["percent"]))
    return "\\makecell{%s}" % " \\\\ ".join(lines)


def build_sources():
    path_bc, nominal_bc = load_fit("corrected/spline/bc/fit.json", "Fit_Pars_from_3D_BC_RC_Bayesian")
    archive = load_json(os.path.join(CAMP, "corrected/spline/normalized_bc_before_bc_families_20261103.json"))["Fit_Pars_from_3D_BC_RC_Bayesian"]
    unw_norm = load_json(os.path.join(CAMP, "corrected/unweighted/normalized_bc.json"))["Fit_Pars_from_3D_BC_RC_Bayesian"]
    path_unw_bc, unw_bc = load_fit("corrected/unweighted/bc/fit.json", "Fit_Pars_from_3D_BC_RC_Bayesian")
    path_bayes, bayes = load_fit("fits/spline/nominal/nominal/fit.json", "Fit_Pars_from_3D_Bayesian")
    path_unw, unw_bayes = load_fit("fits/unweighted/nominal/nominal/fit.json", "Fit_Pars_from_3D_Bayesian")
    scale = {}
    for key, cell in nominal_bc.items():
        scale[key] = float(archive[key]["Fit_Par_A"]) / float(cell["Fit_Par_A"])
    scale_unw = {}
    for key, cell in unw_bc.items():
        scale_unw[key] = float(unw_norm[key]["Fit_Par_A"]) / float(cell["Fit_Par_A"])

    def standard_variation(name, rel, root_name, kind, smear, key_name, baseline_cells, baseline_path, baseline_root, baseline_kind, baseline_key, scale_map, var_coeff_a=1.0):
        path, cells = load_fit(rel, key_name)
        return {
            "name": name,
            "rel": rel,
            "path": path,
            "cells": cells,
            "root": os.path.join(os.path.dirname(path), root_name),
            "kind": kind,
            "smear": smear,
            "key": key_name,
            "baseline_cells": baseline_cells,
            "baseline_path": baseline_path,
            "baseline_root": baseline_root,
            "baseline_kind": baseline_kind,
            "baseline_key": baseline_key,
            "scale_map": scale_map,
            "var_coeff_a": var_coeff_a,
            "sector_filter": False,
        }

    bayes_root = os.path.join(CAMP, "fits/spline/nominal/nominal/fit_copy.root")
    bc_root = os.path.join(CAMP, "corrected/spline/bc/corrected.root")
    sources = []

    def add_pair_source(source_id, title, label, variations):
        sources.append({"id": source_id, "title": title, "label": label, "variations": variations})

    cut_pairs = [
        ("sampling_fraction", "Sampling fraction", "sys-sf-band", "fits/spline/ecband_el/loose/fit.json", "Loose", "fits/spline/ecband_el/tight/fit.json", "Tight"),
        ("pcal_ep", "PCAL $E/p$", "sys-pcal-ep", "fits/spline/ecthr_el/loose/fit.json", "Loose", "fits/spline/ecthr_el/tight/fit.json", "Tight"),
        ("electron_vz", "Electron $v_z$", "sys-vz-el", "fits/spline/dcv_el/loose/fit.json", "Loose", "fits/spline/dcv_el/tight/fit.json", "Tight"),
        ("pcal_volume", "PCAL volume", "sys-pcal-vol", "fits/spline/pcalvol/loose/fit.json", "Loose", "fits/spline/pcalvol/tight/fit.json", "Tight"),
        ("vertex_separation", "$|\\Delta v_z|$", "sys-dvz", "fits/spline/dvz_pip/loose/fit.json", "Loose", "fits/spline/dvz_pip/tight/fit.json", "Tight"),
        ("electron_dc_edges", "Electron DC edges", "sys-dcfid-el", "fits/spline/dcfid_el/loose/fit.json", "Loose", "fits/spline/dcfid_el/tight/fit.json", "Tight"),
        ("pion_dc_edges", "$\\pi^{+}$ DC edges", "sys-dcfid-pip", "fits/spline/dcfid_pip/loose/fit.json", "Loose", "fits/spline/dcfid_pip/tight/fit.json", "Tight"),
        ("electron_dc_refinement", "Electron DC refinement", "sys-dcfid-ref-el", "fits/spline/dcfidref_el/loose/fit.json", "Loose", "fits/spline/dcfidref_el/tight/fit.json", "Tight"),
        ("acceptance_threshold", "Acceptance threshold", "sys-acc-threshold", "fits/spline/acceptance_threshold/Acc015/fit.json", "0.015", "fits/spline/acceptance_threshold/Acc025/fit.json", "0.025"),
        ("bayes_iterations", "Bayesian iterations", "sys-bayes-iter", "fits/spline/bayes_iteration/BayesMinus1/fit.json", "$k-1$", "fits/spline/bayes_iteration/BayesPlus1/fit.json", "$k+1$"),
    ]
    singles_before_sector = [
        ("chi2_pid", "Pion $\\chi^{2}_{\\mathrm{PID}}$", "sys-chi2pid", "fits/spline/chi2_strict_pip/chi2_strict_pip/fit.json", "Stricter bound"),
        ("pcal_dead", "PCAL dead channels", "sys-pcal-knockout", "fits/spline/no_valerii_knockout/no_valerii_knockout/fit.json", "Strips removed"),
        ("sector_pcal", "Sector PCAL fiducial", "sys-sector-pcal", "fits/spline/no_sector_pcal/no_sector_pcal/fit.json", "Vetoes removed"),
        ("pion_dc_extra", "Additional $\\pi^{+}$ DC fiducial", "sys-pip-testdc", "fits/spline/no_pip_testdc/no_pip_testdc/fit.json", "Boundaries removed"),
    ]
    # Table 6.1 order is not the same as the script's acceptance block. Rebuild in table order.
    table_order_prefix = [
        "sampling_fraction", "pcal_ep", "electron_vz", "pcal_volume", "chi2_pid", "vertex_separation",
        "electron_dc_edges", "pion_dc_edges", "pcal_dead", "sector_pcal", "electron_dc_refinement", "pion_dc_extra",
    ]
    made = {}
    for source_id, title, label, loose_rel, loose_name, tight_rel, tight_name in cut_pairs:
        made[source_id] = (title, label, [
            standard_variation(loose_name, loose_rel, "fit_copy.root", "Bayesian", "Smear", "Fit_Pars_from_3D_Bayesian", bayes, path_bayes, bayes_root, "Bayesian", "Fit_Pars_from_3D_Bayesian", scale),
            standard_variation(tight_name, tight_rel, "fit_copy.root", "Bayesian", "Smear", "Fit_Pars_from_3D_Bayesian", bayes, path_bayes, bayes_root, "Bayesian", "Fit_Pars_from_3D_Bayesian", scale),
        ])
    for source_id, title, label, rel, var_name in singles_before_sector:
        made[source_id] = (title, label, [
            standard_variation(var_name, rel, "fit_copy.root", "Bayesian", "Smear", "Fit_Pars_from_3D_Bayesian", bayes, path_bayes, bayes_root, "Bayesian", "Fit_Pars_from_3D_Bayesian", scale),
        ])
    for source_id in table_order_prefix:
        title, label, variations = made[source_id]
        add_pair_source(source_id, title, label, variations)

    sector_vars = []
    for index in range(1, 7):
        for kind, folder, short in (("eS", "electron_sector", "E"), ("pipS", "pion_sector", "P")):
            rel = "fits/spline/%s/%s%do/fit.json" % (folder, kind, index)
            variation = standard_variation("%s%d" % (short, index), rel, "fit_copy.root", "Bayesian", "Smear", "Fit_Pars_from_3D_Bayesian", bayes, path_bayes, bayes_root, "Bayesian", "Fit_Pars_from_3D_Bayesian", scale)
            variation["sector_filter"] = True
            variation["sector_id"] = "%s%do" % (kind, index)
            sector_vars.append(variation)
    add_pair_source("sector", "Sector dependence", "sys-sector", sector_vars)

    phi = standard_variation("12 bins", "fits/spline/phi_bins/Phi12/fit.json", "fit_copy.root", "Bayesian", "Smear", "Fit_Pars_from_3D_Bayesian", bayes, path_bayes, bayes_root, "Bayesian", "Fit_Pars_from_3D_Bayesian", scale, var_coeff_a=0.5)
    add_pair_source("phi_binning", "$\\phi_h$ binning", "sys-phih-bins", [phi])
    add_pair_source("momentum_smearing", "MC momentum smearing", "sys-smear", [
        standard_variation("Smearing removed", "fits/spline/noSmear/noSmear/fit.json", "fit_copy.root", "Bayesian", "Smear", "Fit_Pars_from_3D_Bayesian", bayes, path_bayes, bayes_root, "Bayesian", "Fit_Pars_from_3D_Bayesian", scale),
    ])
    add_pair_source("exclusive_rho0", "Exclusive $\\rho^{0}$", "sys-rho0", [
        standard_variation("Subtraction omitted", "fits/spline/rho0_subtraction/NoRho0/fit.json", "fit_copy.root", "Bayesian", "Smear", "Fit_Pars_from_3D_Bayesian", bayes, path_bayes, bayes_root, "Bayesian", "Fit_Pars_from_3D_Bayesian", scale),
    ])

    path_bin, bin_cells = load_fit("fits/spline/correction_method/BinByBin/fit.json", "Fit_Pars_from_3D_Bin")
    path_5d, five_cells = load_fit("fits/unweighted/dimension/5D/fit.json", "Fit_Pars_from_5D_Bayesian")
    bin_var = standard_variation("Bin-by-bin", "fits/spline/correction_method/BinByBin/fit.json", "fit_copy.root", "Bin", "Smear", "Fit_Pars_from_3D_Bin", bayes, path_bayes, bayes_root, "Bayesian", "Fit_Pars_from_3D_Bayesian", scale)
    bin_var["cells"] = bin_cells
    bin_var["path"] = path_bin
    five_var = standard_variation("Unweighted 5D", "fits/unweighted/dimension/5D/fit.json", "fit_copy.root", "5D", "Smear", "Fit_Pars_from_5D_Bayesian", unw_bayes, path_unw, os.path.join(CAMP, "fits/unweighted/nominal/nominal/fit_copy.root"), "Bayesian", "Fit_Pars_from_3D_Bayesian", scale_unw)
    five_var["cells"] = five_cells
    five_var["path"] = path_5d
    add_pair_source("acceptance_method", "Acceptance method", "sys-acc-method", [bin_var, five_var])
    add_pair_source("acceptance_threshold", made["acceptance_threshold"][0], made["acceptance_threshold"][1], made["acceptance_threshold"][2])
    add_pair_source("bayes_iterations", made["bayes_iterations"][0], made["bayes_iterations"][1], made["bayes_iterations"][2])

    path_rc_base, rc_base = load_fit("corrected/spline/rc/fit_before_guide.json", "Fit_Pars_from_3D_RC_Bayesian")
    rc_root = os.path.join(CAMP, "corrected/spline/rc/corrected.root")
    rc_vars = []
    for rel, var_name in (("alternatives/spline/rc_sf0/fit.json", "rc\\_sf0"), ("alternatives/spline/rc_sf2/fit.json", "rc\\_sf2")):
        variation = standard_variation(var_name, rel, "histograms.root", "RC", "Smear", "Fit_Pars_from_3D_RC_Bayesian", rc_base, path_rc_base, rc_root, "RC", "Fit_Pars_from_3D_RC_Bayesian", scale)
        rc_vars.append(variation)
    add_pair_source("rc_model", "RC model", "sys-rc-model", rc_vars)

    bc_names = []
    for stem, counts in (("sub_phi", (5, 7, 9)), ("sub_pt", (3, 5, 7)), ("sub_q2", (3, 5, 7)), ("sub_y", (3, 5, 7)), ("sub_z", (3, 5, 7))):
        for count in counts:
            bc_names.append("%s_%d" % (stem, count))
    bc_vars = []
    for name in bc_names:
        rel = "alternatives/spline/%s/fit.json" % name
        bc_vars.append(standard_variation(name.replace("_", "\\_"), rel, "histograms.root", "BC", "Smear", "Fit_Pars_from_3D_BC_RC_Bayesian", nominal_bc, path_bc, bc_root, "BC", "Fit_Pars_from_3D_BC_RC_Bayesian", scale))
    add_pair_source("bc_sampling", "BC kinematics", "sys-bc-kin", bc_vars)
    add_pair_source("spline_bc", "Spline BC", "sys-bc-iter", [
        standard_variation("Initial injection spline", "alternatives/spline/bcs_spline/fit.json", "histograms.root", "BC", "Smear", "Fit_Pars_from_3D_BC_RC_Bayesian", nominal_bc, path_bc, bc_root, "BC", "Fit_Pars_from_3D_BC_RC_Bayesian", scale),
    ])

    # Injection A is already A0. B and C stay on the raw BC files. Scale 1 selects the stored numbers.
    injection_a_var = {
        "name": "Zeroth-order unweighted",
        "rel": "corrected/unweighted/normalized_bc.json",
        "path": os.path.join(CAMP, "corrected/unweighted/normalized_bc.json"),
        "cells": unw_norm,
        "root": os.path.join(CAMP, "corrected/unweighted/bc/corrected.root"),
        "kind": "BC",
        "smear": "Smear",
        "key": "Fit_Pars_from_3D_BC_RC_Bayesian",
        "baseline_cells": archive,
        "baseline_path": os.path.join(CAMP, "corrected/spline/normalized_bc_before_bc_families_20261103.json"),
        "baseline_root": bc_root,
        "baseline_kind": "BC",
        "baseline_key": "Fit_Pars_from_3D_BC_RC_Bayesian",
        "scale_map": {key: 1.0 for key in nominal_bc},
        "var_coeff_a": 1.0,
        "sector_filter": False,
        "bc_cells": unw_bc,
        "baseline_bc_cells": nominal_bc,
        "injection": True,
    }
    add_pair_source("physics_injection", "Physics injection", "sys-mod-spline", [injection_a_var])
    add_pair_source("acceptance_reweighting", "Acceptance reweighting", "sys-acc-reweight", [
        standard_variation("Acceptance weights", "fits/spline/acceptance_reweighting/AccSpline/fit.json", "fit_copy.root", "Bayesian", "Smear", "Fit_Pars_from_3D_Bayesian", bayes, path_bayes, bayes_root, "Bayesian", "Fit_Pars_from_3D_Bayesian", scale),
    ])
    return sources, nominal_bc, scale, path_unw_bc


def evaluate(sources, retained):
    sector_exclusions = load_sector_exclusions()
    per_source = []
    for source in sources:
        by_bin = {}
        for key in retained:
            by_bin[key] = {letter: [] for letter in LETTERS}
            for variation in source["variations"]:
                scale = variation["scale_map"].get(key)
                base_cell = variation["baseline_cells"].get(key)
                var_cell = variation["cells"].get(key)
                if(variation.get("injection")):
                    # A from the normalized files. B and C from the raw BC files.
                    for letter in LETTERS:
                        if(letter == "A"):
                            record = one_comparison(base_cell, var_cell, letter, 1.0, 1.0, 1.0)
                        else:
                            record = one_comparison(variation["baseline_bc_cells"].get(key), variation["bc_cells"].get(key), letter, 1.0, 1.0, 1.0)
                        by_bin[key][letter].append(record)
                    continue
                if(scale is None):
                    for letter in LETTERS:
                        by_bin[key][letter].append(None)
                    continue
                if(variation["sector_filter"]):
                    sector_id = variation.get("sector_id")
                    if((sector_id in sector_exclusions) and (key in sector_exclusions[sector_id])):
                        var_cell = None
                    elif(not usable_sector(var_cell)):
                        var_cell = None
                for letter in LETTERS:
                    coeff = variation["var_coeff_a"] if(letter == "A") else 1.0
                    by_bin[key][letter].append(one_comparison(base_cell, var_cell, letter, scale, 1.0, coeff))
        source_rms = {}
        for key in retained:
            source_rms[key] = {}
            for letter in LETTERS:
                present = [record["delta"] for record in by_bin[key][letter] if(record is not None)]
                source_rms[key][letter] = rms(present)
        per_source.append({"source": source, "records": by_bin, "rms": source_rms})
    return per_source


def reconcile(per_source, retained, budget):
    mismatches = []
    stored_sources = budget["sources"]
    for block in per_source:
        source_id = block["source"]["id"]
        stored = stored_sources[source_id]
        for letter in LETTERS:
            values = [block["rms"][key][letter] for key in retained if(block["rms"][key][letter] is not None)]
            got = rms(values)
            expected = float(stored[letter]["rms"])
            if((got is None) or (abs(got - expected) > 1.0e-9)):
                mismatches.append("%s %s across-bin got %s stored %s" % (source_id, letter, got, expected))
            if(len(values) != int(stored[letter]["bins"])):
                mismatches.append("%s %s bins got %d stored %d" % (source_id, letter, len(values), int(stored[letter]["bins"])))
    combined = {}
    for key in retained:
        combined[key] = {}
        for letter in LETTERS:
            pieces = []
            for block in per_source:
                value = block["rms"][key][letter]
                if(value is not None):
                    pieces.append(value)
            combined[key][letter] = math.sqrt(sum(value * value for value in pieces))
            stored_value = float(budget["per_bin_sys"][key][letter])
            if(abs(combined[key][letter] - stored_value) > 1.0e-9):
                mismatches.append("combined %s %s got %.12g stored %.12g" % (key, letter, combined[key][letter], stored_value))
    for letter in LETTERS:
        got = rms([combined[key][letter] for key in retained])
        expected = float(budget["combined_rms"][letter])
        if(abs(got - expected) > 1.0e-9):
            mismatches.append("combined RMS %s got %.12g stored %.12g" % (letter, got, expected))
    return mismatches, combined


def label_rc(per_source):
    for block in per_source:
        if(block["source"]["id"] != "rc_model"):
            continue
        ranges = []
        for index, variation in enumerate(block["source"]["variations"]):
            deltas = []
            for key, row in block["records"].items():
                record = row["A"][index]
                if(record is not None):
                    deltas.append(record["delta"])
            ranges.append((min(deltas), max(deltas), index))
            print("rc variation", index, "A0", min(deltas), max(deltas))
        # Thesis: initial-model -0.01729 to +0.009539; first-iteration -0.007068 to +0.02255.
        targets = [(-0.01729, 0.009539, "Initial-model bin center"), (-0.007068, 0.02255, "First-iteration bin center")]
        for low, high, index in ranges:
            best_name = None
            best_distance = None
            for target_low, target_high, name in targets:
                distance = abs(low - target_low) + abs(high - target_high)
                if((best_distance is None) or (distance < best_distance)):
                    best_distance = distance
                    best_name = name
            block["source"]["variations"][index]["name"] = best_name
            print("rc label", index, best_name, "distance", best_distance)


def ranks_for(per_source, retained):
    per_bin_ranks = {key: {letter: {} for letter in LETTERS} for key in retained}
    for letter in LETTERS:
        for key in retained:
            pairs = []
            for index, block in enumerate(per_source):
                value = block["rms"][key][letter]
                if(value is not None):
                    pairs.append((index, value))
            ranking = assign_ranks(pairs)
            per_bin_ranks[key][letter] = ranking
    overall = {}
    overall_values = {}
    for letter in LETTERS:
        pairs = []
        overall_values[letter] = []
        for index, block in enumerate(per_source):
            values = [block["rms"][key][letter] for key in retained if(block["rms"][key][letter] is not None)]
            value = rms(values)
            overall_values[letter].append(value)
            if(value is not None):
                pairs.append((index, value))
        overall[letter] = assign_ranks(pairs)
    return per_bin_ranks, overall, overall_values


def summary_variation(records_for_variation):
    deltas = []
    sigmas = []
    baselines = []
    for record in records_for_variation:
        if(record is None):
            continue
        deltas.append(record["delta"])
        sigmas.append(record["sigma"])
        baselines.append(record["baseline"])
    if(len(deltas) == 0):
        return None
    mean_delta = sum(deltas) / float(len(deltas))
    mean_sigma = math.sqrt(sum(value * value for value in sigmas)) / float(len(sigmas))
    mean_base = sum(baselines) / float(len(baselines))
    percent = None
    if(mean_base != 0.0):
        percent = 100.0 * mean_delta / abs(mean_base)
    return {"delta": mean_delta, "sigma": mean_sigma, "percent": percent, "baseline": mean_base}


def table_header_rows(title):
    return [
        "    \\hline",
        "    \\multicolumn{10}{|c|}{\\textbf{%s}} \\\\ \\hline" % title,
        "    \\multirow{2}{*}{\\makecell{$Q^2$-$y$--$z$-$P_T$ \\\\ Bin Index}} &",
        "    \\multicolumn{3}{c|}{Variations} &",
        "    \\multicolumn{3}{c|}{$\\Delta_{\\mathrm{RMS}}$} & \\multicolumn{3}{c|}{Contribution Rank}\\\\",
        "    \\cline{2-10} & $\\Delta A_0$ & $\\Delta A_{UU}^{\\cos\\phi}$ & $\\Delta A_{UU}^{\\cos 2\\phi}$ &",
        "    $A_0$ & $A_{UU}^{\\cos\\phi}$ & $A_{UU}^{\\cos 2\\phi}$ &",
        "    $A_0$ & $A_{UU}^{\\cos\\phi}$ & $A_{UU}^{\\cos 2\\phi}$ \\\\ \\hline",
    ]


def section_intro():
    lines = [
        "\\section{Systematic Comparison Tables}",
        "\\label{app:SystematicComparisons}",
        "Each table compares one systematic source with its paired baseline.",
        "The difference is $\\Delta=\\mathrm{variation}-\\mathrm{baseline}$, and the two statistical fit uncertainties are treated as independent, so $\\sigma_{\\Delta}=\\sqrt{\\sigma_{v}^{2}+\\sigma_{b}^{2}}$.",
        "Columns 2--4 list every variation in the order given in that table's caption.",
        "Each variation uses two lines: $\\Delta\\pm\\sigma_{\\Delta}$, then the signed percent difference $100\\Delta/|\\mathrm{baseline}|$.",
        "A percentage is N/A when the baseline is zero or the comparison is unavailable.",
        "An unavailable variation stays in that order as N/A and is not entered as zero.",
        "Columns 5--7 are the source RMS, $\\Delta_{\\mathrm{RMS}}$, over the comparisons included by the existing rules.",
        "The propagated fit uncertainty $\\sigma_{\\Delta}$ is not used in that RMS.",
        "Columns 8--10 rank the source against the other sources in \\Cref{tab:SystematicUncertainties}.",
        "Rank 1 is the largest unrounded contribution.",
        "Equal values share that rank and the next rank number is skipped.",
        "The worst rank in a bin is the number of sources with a finite contribution there, out of 24 catalogued sources.",
        "Rank N/A means the source has no available contribution.",
        "The last row is an across-bin summary, not a kinematic bin.",
        "Its variation entries are the unweighted mean of the signed differences, with uncertainty $\\sqrt{\\sum\\sigma_{\\Delta}^{2}}/N$, and the percent difference of that mean relative to the mean baseline.",
        "Its $\\Delta_{\\mathrm{RMS}}$ entries are the RMS of the per-bin source contributions, and its ranks are the rank of that across-bin RMS.",
        "Bins marked Skipped in \\Cref{tab:BinBorders} are omitted.",
        "Amplitudes compared here are the cross-section-normalized $A_{0}$.",
        "The scale is the one already used for the systematic budget: archived $A_{0}$ divided by the nominal raw amplitude, which equals $1/(\\Delta Q^{2}\\,\\Delta y\\,\\Delta z\\,\\Delta P_{T}^{2}\\,\\Delta\\phi_{h}\\times\\mathcal{L}\\times\\Gamma)$.",
        "The unweighted 5D comparison uses the corresponding unweighted normalization.",
        "Already-normalized injection amplitudes are not scaled again.",
        "$B$ and $C$ are not rescaled.",
        "For the $\\phi_{h}$ binning variation, the 12-bin amplitude is multiplied by one half before the cross-section scale is applied.",
        "",
    ]
    return lines


def write_tables(per_source, retained, per_bin_ranks, overall, overall_values):
    chunks = ["\n".join(section_intro())]
    for source_index, block in enumerate(per_source):
        source = block["source"]
        order = ", ".join(variation["name"].replace("\\_", "_") for variation in source["variations"])
        order_tex = "; ".join(variation["name"] for variation in source["variations"])
        camel = "".join(part.capitalize() for part in source["id"].split("_"))
        lines = []
        lines.append("\\subsection{%s}" % source["title"])
        lines.append("\\label{app:SysCmp%s}" % camel)
        lines.append("\\begingroup")
        lines.append("\\footnotesize")
        lines.append("\\renewcommand{\\arraystretch}{1.15}")
        lines.append("\\setlength{\\tabcolsep}{2.4pt}")
        lines.append("\\setlength{\\LTleft}{0pt}")
        lines.append("\\setlength{\\LTright}{0pt}")
        lines.append("\\begin{longtable}{|*{10}{c|}}")
        lines.append("    \\caption{Signed differences for the \\textbf{%s} comparisons (see \\Cref{%s})." % (source["title"], source["label"]))
        lines.append("    Variations, from top to bottom, are %s." % order_tex)
        if(source["id"] == "physics_injection"):
            lines.append("    The nominal baseline is the spline-weighted result and the variation is the unweighted result, so $\\Delta$ is unweighted minus spline-weighted.")
        lines.append("    Column definitions, the uncertainty convention, ranks, and the across-bin summary are given in \\Cref{app:SystematicComparisons}.}")
        lines.append("    \\label{tab:SysCmp%s}\\\\" % camel)
        lines.extend(table_header_rows(source["title"]))
        lines.append("    \\endfirsthead")
        lines.append("    \\multicolumn{10}{c}{{\\tablename\\ \\thetable} --- continued from previous page}\\\\")
        lines.extend(table_header_rows(source["title"]))
        lines.append("    \\endhead")
        lines.append("    \\endfoot")
        lines.append("    \\endlastfoot")
        for key in retained:
            q2y_bin, zpt_bin = parse_bin_key(key)
            cells = []
            all_missing = True
            for letter in LETTERS:
                records = block["records"][key][letter]
                if(any(record is not None for record in records)):
                    all_missing = False
                cells.append(variation_cell(records))
            if(all_missing):
                rms_cells = ["N/A", "N/A", "N/A"]
                rank_cells = ["N/A", "N/A", "N/A"]
            else:
                rms_cells = [fmt_num(block["rms"][key][letter]) for letter in LETTERS]
                rank_cells = []
                for letter in LETTERS:
                    rank_number = per_bin_ranks[key][letter].get(source_index)
                    rank_cells.append("N/A" if(rank_number is None) else str(rank_number))
            lines.append("    %d -- %d &" % (q2y_bin, zpt_bin))
            lines.append("    %s &" % cells[0])
            lines.append("    %s &" % cells[1])
            lines.append("    %s &" % cells[2])
            lines.append("    %s &" % rms_cells[0])
            lines.append("    %s &" % rms_cells[1])
            lines.append("    %s &" % rms_cells[2])
            lines.append("    %s &" % rank_cells[0])
            lines.append("    %s &" % rank_cells[1])
            lines.append("    %s" % rank_cells[2])
            lines.append("    \\\\ \\hline")
        summary_cells = []
        for letter in LETTERS:
            column = []
            for index in range(len(source["variations"])):
                series = [block["records"][key][letter][index] for key in retained]
                column.append(summary_variation(series))
            summary_cells.append(variation_cell(column))
        summary_rms = [fmt_num(overall_values[letter][source_index]) for letter in LETTERS]
        summary_rank = []
        for letter in LETTERS:
            rank_number = overall[letter].get(source_index)
            summary_rank.append("N/A" if(rank_number is None) else str(rank_number))
        lines.append("    \\makecell{Across-bin \\\\ summary} &")
        lines.append("    %s &" % summary_cells[0])
        lines.append("    %s &" % summary_cells[1])
        lines.append("    %s &" % summary_cells[2])
        lines.append("    %s &" % summary_rms[0])
        lines.append("    %s &" % summary_rms[1])
        lines.append("    %s &" % summary_rms[2])
        lines.append("    %s &" % summary_rank[0])
        lines.append("    %s &" % summary_rank[1])
        lines.append("    %s" % summary_rank[2])
        lines.append("    \\\\ \\hline")
        lines.append("\\end{longtable}")
        lines.append("\\endgroup")
        lines.append("")
        chunks.append("\n".join(lines))
        print("table", source["id"], "order", order)
    with open(TEX_PATH, "w") as handle:
        handle.write("\n".join(chunks))
        handle.write("\n")
    print("wrote", TEX_PATH)


def side_scale(norm_cell, raw_cell):
    if((not isinstance(norm_cell, dict)) or (not isinstance(raw_cell, dict))):
        return None
    if(("Fit_Par_A" not in norm_cell) or ("Fit_Par_A" not in raw_cell)):
        return None
    raw = float(raw_cell["Fit_Par_A"])
    if(raw == 0.0):
        return None
    return float(norm_cell["Fit_Par_A"]) / raw


def amplitude_scales(variation):
    scales = {}
    if(variation.get("injection")):
        keys = set(variation["baseline_cells"].keys())
        keys.update(variation["cells"].keys())
        for key in keys:
            scales[key] = {
                "baseline": side_scale(variation["baseline_cells"].get(key), variation["baseline_bc_cells"].get(key)),
                "variation": side_scale(variation["cells"].get(key), variation["bc_cells"].get(key)),
            }
        return scales
    for key, factor in variation["scale_map"].items():
        if(factor is None):
            scales[key] = None
        else:
            scales[key] = {"baseline": float(factor), "variation": float(factor) * float(variation["var_coeff_a"])}
    return scales


def check_injection_sign(per_source):
    for block in per_source:
        if(block["source"]["id"] != "physics_injection"):
            continue
        variation = block["source"]["variations"][0]
        for key, row in block["records"].items():
            record = row["A"][0]
            if(record is None):
                continue
            expected = float(variation["cells"][key]["Fit_Par_A"]) - float(variation["baseline_cells"][key]["Fit_Par_A"])
            if(abs(record["delta"] - expected) > 1.0e-9):
                raise SystemExit("injection sign mismatch at %s" % key)
            print("injection sign", key, "unweighted-spline", record["delta"])
            return
    raise SystemExit("injection comparison was not checked")


def write_jobs(per_source):
    os.makedirs(REVIEW_DIR, exist_ok=True)
    jobs = []
    for block in per_source:
        source = block["source"]
        for index, variation in enumerate(source["variations"]):
            histogram_baseline = variation["baseline_path"]
            histogram_variation = variation["path"]
            if(variation.get("injection")):
                histogram_baseline = os.path.join(CAMP, "corrected/spline/bc/fit.json")
                histogram_variation = os.path.join(CAMP, "corrected/unweighted/bc/fit.json")
            jobs.append({
                "a_scale": amplitude_scales(variation),
                "source_id": source["id"],
                "source_title": source["title"],
                "variation_index": index,
                "variation_name": variation["name"],
                "baseline_root": variation["baseline_root"],
                "variation_root": variation["root"],
                "baseline_json": histogram_baseline,
                "variation_json": histogram_variation,
                "baseline_fit_key": variation["baseline_key"] if(not variation.get("injection")) else "Fit_Pars_from_3D_BC_RC_Bayesian",
                "variation_fit_key": variation["key"] if(not variation.get("injection")) else "Fit_Pars_from_3D_BC_RC_Bayesian",
                "baseline_kind": variation["baseline_kind"],
                "variation_kind": variation["kind"],
                "baseline_smear": variation["smear"],
                "variation_smear": variation["smear"],
                "var_coeff_a": variation["var_coeff_a"],
                "output_dir": os.path.join(REVIEW_DIR, source["id"], "variation_%02d" % index),
            })
    path = os.path.join(REVIEW_DIR, "jobs.json")
    with open(path, "w") as handle:
        json.dump(jobs, handle)
        handle.write("\n")
    print("jobs", len(jobs), path)
    return jobs


def write_highlights(per_source, retained, per_bin_ranks, combined):
    selected = {}
    for letter in LETTERS:
        scored = sorted(retained, key=lambda key: (-combined[key][letter], key))
        for key in scored[:10]:
            selected.setdefault(key, set()).add(letter)
    lines = []
    lines.append("<!DOCTYPE html>")
    lines.append("<html><head><meta charset=\"utf-8\"><title>Largest systematic bins</title></head><body>")
    lines.append("<h1>Largest combined systematic uncertainties</h1>")
    lines.append("<p>For each observable, these are the 10 retained bins with the largest combined systematic uncertainty in the existing budget. A bin that qualifies for more than one observable is listed once. Ranks use the unrounded per-bin source contributions. The link opens the variation with the largest absolute difference in that bin.</p>")
    lines.append("<table border=\"1\" cellpadding=\"4\">")
    lines.append("<tr><th>Bin</th><th>Observable</th><th>Combined systematic</th><th>Sources in rank order</th></tr>")
    for key in sorted(selected, key=lambda item: parse_bin_key(item)):
        q2y_bin, zpt_bin = parse_bin_key(key)
        observable_lines = []
        combined_lines = []
        source_lines = []
        for letter in LETTERS:
            if(letter not in selected[key]):
                continue
            ranked = []
            for index, block in enumerate(per_source):
                rank_number = per_bin_ranks[key][letter].get(index)
                value = block["rms"][key][letter]
                if((rank_number is None) or (value is None)):
                    continue
                best = None
                best_abs = None
                for var_index, record in enumerate(block["records"][key][letter]):
                    if(record is None):
                        continue
                    absolute = abs(record["delta"])
                    if((best_abs is None) or (absolute > best_abs)):
                        best_abs = absolute
                        best = var_index
                href = "%s/variation_%02d/Q2y_%02d.png" % (block["source"]["id"], best, q2y_bin)
                ranked.append((rank_number, index, "%d. %s RMS %s, largest |Δ| variation <a href=\"%s\">%s</a>" % (
                    rank_number, block["source"]["id"], "%.6g" % value, href, block["source"]["variations"][best]["name"])))
            ranked.sort()
            observable_lines.append(LETTER_NAME[letter])
            combined_lines.append("%.6g" % combined[key][letter])
            source_lines.append("<b>%s</b><br>%s" % (LETTER_NAME[letter], "<br>".join(text for _rank, _index, text in ranked)))
        lines.append("<tr><td>%d -- %d</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
            q2y_bin, zpt_bin, "<br><br>".join(observable_lines), "<br><br>".join(combined_lines), "<br><br>".join(source_lines)))
    lines.append("</table></body></html>")
    path = os.path.join(REVIEW_DIR, "highlights.html")
    with open(path, "w") as handle:
        handle.write("\n".join(lines))
        handle.write("\n")
    print("highlights", path, "bins", len(selected))


def main():
    retained, skipped = read_border_rows(BORDER_PATH)
    sources, nominal_bc, _scale, _path_unw_bc = build_sources()
    retained_set = set(retained)
    nominal_set = set(nominal_bc)
    if(retained_set != nominal_set):
        print("BORDER/NOMINAL MISMATCH")
        print("only border", sorted(retained_set - nominal_set)[:20], "count", len(retained_set - nominal_set))
        print("only nominal", sorted(nominal_set - retained_set)[:20], "count", len(nominal_set - retained_set))
        raise SystemExit(2)
    print("retained", len(retained), "skipped", len(skipped), "sources", len(sources))
    budget = load_json(BUDGET_PATH)
    per_source = evaluate(sources, retained)
    label_rc(per_source)
    mismatches, combined = reconcile(per_source, retained, budget)
    print("mismatches", len(mismatches))
    for line in mismatches[:30]:
        print(line)
    if(len(mismatches)):
        raise SystemExit(3)
    per_bin_ranks, overall, overall_values = ranks_for(per_source, retained)
    check_injection_sign(per_source)
    write_tables(per_source, retained, per_bin_ranks, overall, overall_values)
    write_jobs(per_source)
    write_highlights(per_source, retained, per_bin_ranks, combined)
    # Compact numeric sidecar for the overlay parameter boxes.
    box_path = os.path.join(REVIEW_DIR, "fit_boxes.json")
    payload = {"sources": []}
    for block in per_source:
        source = block["source"]
        variations = []
        for variation in source["variations"]:
            variations.append({
                "name": variation["name"],
                "kind": variation["kind"],
                "smear": variation["smear"],
                "root": variation["root"],
                "baseline_kind": variation["baseline_kind"],
                "baseline_root": variation["baseline_root"],
                "var_coeff_a": variation["var_coeff_a"],
                "injection": bool(variation.get("injection")),
            })
        payload["sources"].append({"id": source["id"], "variations": variations})
    with open(box_path, "w") as handle:
        json.dump(payload, handle)
    print("reconciled")


if(__name__ == "__main__"):
    main()
