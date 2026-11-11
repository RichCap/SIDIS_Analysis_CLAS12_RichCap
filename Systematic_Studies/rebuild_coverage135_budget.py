#!/usr/bin/env python3
# Recalculate the 2026-11-08 systematic budget after the 135 degree coverage cut.
# Pairings match rebuild_refinement_budget_20261108.py. This file does not refit.

import argparse
import hashlib
import json
import math
import os
import shutil
import subprocess

import rebuild_final_systematic_budget as base

CAMP = base.CAMP
REF = os.path.join(CAMP, "refinement_20261108")
PRESERVED_DIR = os.path.join(CAMP, "budgets", "rerun_refinement_20261108_before_coverage135")
PRESERVED_BUDGET = os.path.join(PRESERVED_DIR, "budget.json")
PRESERVED_SHARES = os.path.join(PRESERVED_DIR, "per_bin_source_shares.json")
PRESERVED_NORM = os.path.join(PRESERVED_DIR, "normalized_bc.json")
REPRODUCE_DIR = os.path.join(CAMP, "budgets", "rerun_refinement_20261108_coverage135_reproduce")
OUT = os.path.join(CAMP, "budgets", "rerun_refinement_20261108_coverage135")
COVERAGE_PATH = os.path.join(CAMP, "coverage135_20261109", "coverage_records.json")
EXCLUSIONS_PATH = base.EXCLUSIONS_PATH
KEY_BAYES = base.KEY_BAYES
KEY_BIN = base.KEY_BIN
KEY_5D = base.KEY_5D
KEY_RC = base.KEY_RC
KEY_BC = base.KEY_BC
LETTERS = base.LETTERS
PROTECTED = [
    os.path.join(CAMP, "budgets", "rerun_20261104", "budget.json"),
    os.path.join(CAMP, "budgets", "rerun_20261106_sector_exclusions", "budget.json"),
    os.path.join(CAMP, "budgets", "rerun_20261106_sector_12_23", "budget.json"),
    EXCLUSIONS_PATH,
    os.path.join(CAMP, "corrected", "unweighted", "normalized_bc.json"),
    os.path.join(CAMP, "corrected", "spline", "bc", "fit.json"),
    os.path.join(CAMP, "corrected", "unweighted", "bc", "fit.json"),
]


def sha256(path):
    return base.sha256(path)


def load_key(path, key):
    payload = json.load(open(path))
    if(key not in payload):
        raise SystemExit("%s has no %s" % (path, key))
    return payload[key]


def protected_hashes():
    hashes = {}
    for path in PROTECTED:
        hashes[path] = sha256(path)
    return hashes


def column_minmax(maps, letter):
    lowest = None
    highest = None
    for shifts in maps:
        for row in shifts.values():
            value = float(row[letter])
            if((lowest is None) or (value < lowest)):
                lowest = value
            if((highest is None) or (value > highest)):
                highest = value
    return lowest, highest


def mean_abs(maps, letter):
    total = 0.0
    count = 0
    for shifts in maps:
        for row in shifts.values():
            total += abs(float(row[letter]))
            count += 1
    if(count == 0):
        return None, 0
    return total / float(count), count


def parse_args():
    parser = argparse.ArgumentParser(description="Rebuild the systematic budget with the 135 degree coverage cut.")
    parser.add_argument("-c", "--coverage", default=COVERAGE_PATH)
    parser.add_argument("-p", "--preserved_budget", default=PRESERVED_BUDGET)
    parser.add_argument("-s", "--preserved_shares", default=PRESERVED_SHARES)
    parser.add_argument("-n", "--preserved_norm", default=PRESERVED_NORM)
    parser.add_argument("-r", "--reproduce_dir", default=REPRODUCE_DIR)
    parser.add_argument("-o", "--output", default=OUT)
    parser.add_argument("-x", "--exclude_sources", default="", help="Comma-separated budget keys to leave out. chi2_pid and acceptance_reweighting are the known keys.")
    parser.add_argument("-sr", "--skip_reproduction", action="store_true", help="Do not rebuild or consume the reproduction budget.")
    parser.add_argument("-nl", "--no_write_live", action="store_true", help="Do not write corrected/spline/normalized_bc.json.")
    parser.add_argument("-no", "--normalized_out", default="", help="Write a version normalized JSON here. Does not replace the live file.")
    parser.add_argument("-co", "--comparison_only", action="store_true", help="Rewrite the comparison and provenance baseline from saved budget files. Does not aggregate.")
    parser.add_argument("-cb", "--comparison_baseline_budget", default="", help="Budget JSON used as the comparison baseline.")
    parser.add_argument("-cs", "--comparison_baseline_shares", default="", help="Share JSON used as the comparison baseline.")
    parser.add_argument("-sk", "--sector_kinds", default="electron,pion", help="Sector populations to aggregate. electron,pion is the mixed study. electron keeps only eS1o--eS6o.")
    return parser.parse_args()


def coverage_fails(record):
    if(record.get("status") != "assessed"):
        return True
    return float(record["missing_deg"]) > 135.0


def load_coverage(path):
    payload = json.load(open(path))
    by_fit = {}
    for item in payload["inputs"]:
        by_fit[os.path.abspath(item["fit_json"])] = item
    return payload, by_fit


def drop_map(by_fit):
    drops = {}
    known = set()
    for path, item in by_fit.items():
        if(item["role"] != "variation"):
            continue
        known.add(path)
        failed = set()
        for key, record in item["records"].items():
            if(coverage_fails(record)):
                failed.add(key)
        drops[path] = failed
    return drops, known


def same_number(left, right):
    if((left is None) and (right is None)):
        return True
    if((left is None) or (right is None)):
        return False
    return abs(float(left) - float(right)) <= 1.0e-9


EXCLUDED_FIT = {
    "chi2_pid": ["spline/chi2_strict_pip/chi2_strict_pip/fit.json"],
    "acceptance_reweighting": ["spline/acceptance_reweighting/AccSpline/fit.json"],
}


def selected_sector_kinds(text):
    names = [item.strip() for item in text.split(",") if(item.strip() != "")]
    if(len(names) != len(set(names))):
        raise SystemExit("repeated sector kind in %s" % text)
    got = set(names)
    if(got == set(["electron", "pion"])):
        return ["electron", "pion"]
    if(got == set(["electron"])):
        return ["electron"]
    raise SystemExit("unsupported sector kinds %s" % names)


def aggregate(drop_by_path, out_dir, write_live, preserved_norm, known_fits, status_label, excluded_sources=None, sector_kinds=None):
    before = protected_hashes()
    os.makedirs(out_dir, exist_ok=True)
    kept_by_path = {}
    if(excluded_sources is None):
        excluded_sources = []
    excluded = set(excluded_sources)
    excluded_paths = set()
    for name in excluded:
        if(name not in EXCLUDED_FIT):
            raise SystemExit("unknown excluded source %s" % name)
        for relative in EXCLUDED_FIT[name]:
            excluded_paths.add(os.path.abspath(os.path.join(REF, relative)))

    def omit_coverage(path, shifts):
        absolute = os.path.abspath(path)
        if((known_fits is not None) and (absolute not in known_fits)):
            raise SystemExit("variation fit is not in the coverage scan: %s" % absolute)
        banned = drop_by_path.get(absolute, set())
        if(len(banned) > 0):
            shifts = {key: value for key, value in shifts.items() if(key not in banned)}
        kept_by_path[absolute] = set(shifts.keys())
        return shifts

    def check_scaled_shift(path, base_cells, alt_cells, scale_map, shifts, phi_half):
        if(len(shifts) == 0):
            return
        check_key = sorted(shifts.keys())[0]
        alt_a = float(alt_cells[check_key]["Fit_Par_A"])
        if(phi_half):
            alt_a = 0.5 * alt_a
        expected_a = (alt_a - float(base_cells[check_key]["Fit_Par_A"])) * scale_map[check_key]
        expected_b = float(alt_cells[check_key]["Fit_Par_B"]) - float(base_cells[check_key]["Fit_Par_B"])
        expected_c = float(alt_cells[check_key]["Fit_Par_C"]) - float(base_cells[check_key]["Fit_Par_C"])
        row = shifts[check_key]
        if((abs(expected_a - row["A"]) > 1.0e-8) or (abs(expected_b - row["B"]) > 1.0e-8) or (abs(expected_c - row["C"]) > 1.0e-8)):
            raise SystemExit("shift does not follow the stored scale convention in %s" % path)
    path_bc_old = os.path.join(CAMP, "corrected", "spline", "bc", "fit.json")
    path_bc = os.path.join(REF, "spline", "nominal", "bc", "fit.json")
    path_bayes = os.path.join(REF, "spline", "nominal", "acceptance", "fit.json")
    path_unw = os.path.join(REF, "unweighted", "nominal", "acceptance", "fit.json")
    path_unw_bc_old = os.path.join(CAMP, "corrected", "unweighted", "bc", "fit.json")
    path_unw_bc = os.path.join(REF, "unweighted", "nominal", "bc", "fit.json")
    path_unw_norm = os.path.join(CAMP, "corrected", "unweighted", "normalized_bc.json")
    path_archive = os.path.join(CAMP, "corrected", "spline", "normalized_bc_before_bc_families_20261103.json")
    path_now = os.path.join(CAMP, "corrected", "spline", "normalized_bc.json")
    path_rc = os.path.join(REF, "spline", "nominal", "rc", "fit.json")

    old_bc = load_key(path_bc_old, KEY_BC)
    nominal_bc = load_key(path_bc, KEY_BC)
    bayes = load_key(path_bayes, KEY_BAYES)
    unw_bayes = load_key(path_unw, KEY_BAYES)
    old_unw_bc = load_key(path_unw_bc_old, KEY_BC)
    unw_bc = load_key(path_unw_bc, KEY_BC)
    archive = load_key(path_archive, KEY_BC)
    archive_norm = os.path.join(CAMP, "corrected", "spline", "normalized_bc_before_refinement_20261108.json")
    if(os.path.isfile(archive_norm)):
        current = load_key(archive_norm, KEY_BC)
    else:
        current = load_key(path_now, KEY_BC)
    unw_norm = load_key(path_unw_norm, KEY_BC)
    if(set(nominal_bc) != set(archive)):
        raise SystemExit("refined BC bins and the archived A0 bins differ")
    if(set(current) != set(archive)):
        raise SystemExit("live normalized bins and the archived A0 bins differ")

    scale = {}
    scale_if_new_raw = {}
    for key, cell in old_bc.items():
        raw_a = float(cell["Fit_Par_A"])
        if(raw_a == 0.0):
            raise SystemExit("raw A is 0 in %s" % key)
        scale[key] = float(archive[key]["Fit_Par_A"]) / raw_a
        new_raw = float(nominal_bc[key]["Fit_Par_A"])
        if(new_raw == 0.0):
            raise SystemExit("refined raw A is 0 in %s" % key)
        scale_if_new_raw[key] = float(archive[key]["Fit_Par_A"]) / new_raw
    scale_unw = {}
    for key, cell in old_unw_bc.items():
        raw_a = float(cell["Fit_Par_A"])
        if(raw_a == 0.0):
            raise SystemExit("unweighted raw A is 0 in %s" % key)
        if(key not in unw_norm):
            continue
        scale_unw[key] = float(unw_norm[key]["Fit_Par_A"]) / raw_a
    scale_gap = 0.0
    scale_move = 0.0
    for key in scale:
        if(key in scale_unw):
            scale_gap = max(scale_gap, abs(scale[key] - scale_unw[key]) / abs(scale[key]))
        scale_move = max(scale_move, abs(scale[key] - scale_if_new_raw[key]) / abs(scale[key]))
    print("max relative A0 scale difference, spline versus unweighted: %.3e" % scale_gap)
    print("max relative scale move if the refined raw A were the denominator: %.3e" % scale_move)

    pairs = []
    signed = {}

    def add_acceptance(name, relatives, phi_half=False):
        if(name in excluded):
            return
        maps = []
        used = []
        for rel in relatives:
            path = os.path.join(REF, rel)
            cells = load_key(path, KEY_BAYES)
            shifts = omit_coverage(path, base.pair_shifts(bayes, cells, scale, phi_half=phi_half))
            check_scaled_shift(path, bayes, cells, scale, shifts, phi_half)
            maps.append(shifts)
            used.append(path)
        per_bin, counts = base.family_rms(maps)
        pairs.append((name, per_bin, counts, used))
        signed[name] = maps

    add_acceptance("sampling_fraction", ["spline/ecband_el/loose/fit.json", "spline/ecband_el/tight/fit.json"])
    add_acceptance("pcal_ep", ["spline/ecthr_el/loose/fit.json", "spline/ecthr_el/tight/fit.json"])
    add_acceptance("electron_vz", ["spline/dcv_el/loose/fit.json", "spline/dcv_el/tight/fit.json"])
    add_acceptance("pcal_volume", ["spline/pcalvol/loose/fit.json", "spline/pcalvol/tight/fit.json"])
    add_acceptance("chi2_pid", ["spline/chi2_strict_pip/chi2_strict_pip/fit.json"])
    add_acceptance("vertex_separation", ["spline/dvz_pip/loose/fit.json", "spline/dvz_pip/tight/fit.json"])
    add_acceptance("electron_dc_edges", ["spline/dcfid_el/loose/fit.json", "spline/dcfid_el/tight/fit.json"])
    add_acceptance("pion_dc_edges", ["spline/dcfid_pip/loose/fit.json", "spline/dcfid_pip/tight/fit.json"])
    add_acceptance("pcal_dead", ["spline/no_valerii_knockout/no_valerii_knockout/fit.json"])
    add_acceptance("sector_pcal", ["spline/no_sector_pcal/no_sector_pcal/fit.json"])
    add_acceptance("electron_dc_refinement", ["spline/dcfidref_el/loose/fit.json", "spline/dcfidref_el/tight/fit.json"])
    add_acceptance("pion_dc_extra", ["spline/no_pip_testdc/no_pip_testdc/fit.json"])
    add_acceptance("phi_binning", ["spline/phi_bins/Phi12/fit.json"], phi_half=True)
    add_acceptance("momentum_smearing", ["spline/noSmear/noSmear/fit.json"])
    add_acceptance("exclusive_rho0", ["spline/rho0_subtraction/NoRho0/fit.json"])
    add_acceptance("acceptance_threshold", ["spline/acceptance_threshold/Acc015/fit.json", "spline/acceptance_threshold/Acc025/fit.json"])
    add_acceptance("bayes_iterations", ["spline/bayes_iteration/BayesMinus1/fit.json", "spline/bayes_iteration/BayesPlus1/fit.json"])
    add_acceptance("acceptance_reweighting", ["spline/acceptance_reweighting/AccSpline/fit.json"])

    path_bin = os.path.join(REF, "spline", "correction_method", "BinByBin", "fit.json")
    bin_cells = load_key(path_bin, KEY_BIN)
    bin_shifts = omit_coverage(path_bin, base.pair_shifts(bayes, bin_cells, scale))
    check_scaled_shift(path_bin, bayes, bin_cells, scale, bin_shifts, False)
    path_5d = os.path.join(REF, "unweighted", "dimension", "5D", "fit.json")
    five_cells = load_key(path_5d, KEY_5D)
    five_shifts = omit_coverage(path_5d, base.pair_shifts(unw_bayes, five_cells, scale_unw))
    check_scaled_shift(path_5d, unw_bayes, five_cells, scale_unw, five_shifts, False)
    acceptance, acceptance_counts = base.family_rms([bin_shifts, five_shifts])
    pairs.append(("acceptance_method", acceptance, acceptance_counts, [path_bin, path_5d, path_bayes, path_unw]))
    signed["acceptance_method"] = [bin_shifts, five_shifts]
    signed["acceptance_bin_by_bin"] = [bin_shifts]
    signed["acceptance_5d"] = [five_shifts]

    sector_exclusions = base.load_sector_exclusions()
    sector_maps = []
    sector_kept_by_id = {}
    sector_paths = []
    sector_quality_omitted = []
    sector_missing = []
    sector_present_unusable = []
    sector_user_excluded = []
    sector_requested_already_unavailable = []
    sector_shift_rows = []
    not_in_study_paths = []
    active_sector_ids = []
    if(sector_kinds is None):
        sector_kinds = ["electron", "pion"]
    selected_kinds = set(sector_kinds)
    kind_folders = (
        ("electron", "eS", "electron_sector"),
        ("pion", "pipS", "pion_sector"),
    )
    for index in range(1, 7):
        for kind_name, kind, folder in kind_folders:
            var_id = base.sector_variation_id(kind, index)
            path = os.path.join(REF, "spline", folder, var_id, "fit.json")
            if(kind_name not in selected_kinds):
                not_in_study_paths.append(os.path.abspath(path))
                continue
            active_sector_ids.append(var_id)
            cells = load_key(path, KEY_BAYES)
            sector_paths.append(path)
            kept = {}
            listed = sector_exclusions.get(var_id, set())
            banned = drop_by_path.get(os.path.abspath(path), set())
            if((known_fits is not None) and (os.path.abspath(path) not in known_fits)):
                raise SystemExit("variation fit is not in the coverage scan: %s" % path)
            sector_kept_keys = set()
            for key, nominal_cell in bayes.items():
                cell = cells.get(key)
                if(not base.usable_sector(cell)):
                    sector_quality_omitted.append("%s %s" % (var_id, key))
                    if(cell is None):
                        sector_missing.append("%s %s" % (var_id, key))
                    else:
                        sector_present_unusable.append("%s %s" % (var_id, key))
                    if(key in listed):
                        sector_requested_already_unavailable.append("%s %s" % (var_id, key))
                    continue
                factor = scale[key]
                shift = {
                    "A": (float(cell["Fit_Par_A"]) - float(nominal_cell["Fit_Par_A"])) * factor,
                    "B": float(cell["Fit_Par_B"]) - float(nominal_cell["Fit_Par_B"]),
                    "C": float(cell["Fit_Par_C"]) - float(nominal_cell["Fit_Par_C"]),
                }
                if(key in listed):
                    sector_user_excluded.append("%s %s" % (var_id, key))
                    continue
                if(key in banned):
                    continue
                kept[key] = shift
                sector_kept_keys.add(key)
                sector_shift_rows.append((var_id, key, shift))
            sector_maps.append(kept)
            sector_kept_by_id[var_id] = set(kept.keys())
            kept_by_path[os.path.abspath(path)] = sector_kept_keys
    sector_unmatched = []
    for var_id, listed in sector_exclusions.items():
        for key in listed:
            if(key not in bayes):
                sector_unmatched.append("%s %s" % (var_id, key))
    sector, sector_counts = base.family_rms(sector_maps)
    pairs.append(("sector", sector, sector_counts, sector_paths))
    signed["sector"] = sector_maps
    print("sector missing stored fits: %d" % len(sector_missing))
    print("sector present but unusable: %d" % len(sector_present_unusable))
    print("sector quality omissions: %d" % len(sector_quality_omitted))
    print("sector user exclusions of usable comparisons: %d" % len(sector_user_excluded))
    print("sector requested entries already unavailable: %d" % len(sector_requested_already_unavailable))
    print("sector requested entries with no stored bin: %d" % len(sector_unmatched))
    print("sector comparisons kept: %d" % sum(len(item) for item in sector_maps))
    print("active sector ids: %s" % " ".join(active_sector_ids))
    print("sector variations not in this study: %d" % len(not_in_study_paths))
    if(selected_kinds == set(["electron"])):
        for kept_path in kept_by_path:
            if("/pion_sector/" in kept_path):
                raise SystemExit("pion sector entered the kept set: %s" % kept_path)

    path_sf0 = os.path.join(REF, "spline", "rc_model", "rc_sf0", "fit.json")
    path_sf2 = os.path.join(REF, "spline", "rc_model", "rc_sf2", "fit.json")
    sf0 = load_key(path_sf0, KEY_RC)
    sf2 = load_key(path_sf2, KEY_RC)
    rc_base = load_key(path_rc, KEY_RC)
    rc_maps = [
        omit_coverage(path_sf0, base.pair_shifts(rc_base, sf0, scale)),
        omit_coverage(path_sf2, base.pair_shifts(rc_base, sf2, scale)),
    ]
    check_scaled_shift(path_sf0, rc_base, sf0, scale, rc_maps[0], False)
    check_scaled_shift(path_sf2, rc_base, sf2, scale, rc_maps[1], False)
    rc_piece, rc_counts = base.family_rms(rc_maps)
    pairs.append(("rc_model", rc_piece, rc_counts, [path_sf0, path_sf2, path_rc]))
    signed["rc_model"] = rc_maps

    kin_names = [
        "sub_phi_5", "sub_phi_7", "sub_phi_9",
        "sub_pt_3", "sub_pt_5", "sub_pt_7",
        "sub_q2_3", "sub_q2_5", "sub_q2_7",
        "sub_y_3", "sub_y_5", "sub_y_7",
        "sub_z_3", "sub_z_5", "sub_z_7",
    ]
    kin_maps = []
    kin_paths = []
    kin_by_name = {}
    for name in kin_names:
        path = os.path.join(REF, "spline", "bc_sampling", name, "fit.json")
        cells = load_key(path, KEY_BC)
        shifts = omit_coverage(path, base.pair_shifts(nominal_bc, cells, scale))
        check_scaled_shift(path, nominal_bc, cells, scale, shifts, False)
        kin_maps.append(shifts)
        kin_paths.append(path)
        kin_by_name[name] = shifts
    kin_piece, kin_counts = base.family_rms(kin_maps)
    pairs.append(("bc_sampling", kin_piece, kin_counts, kin_paths))
    signed["bc_sampling"] = kin_maps

    path_spline = os.path.join(REF, "spline", "spline_bc", "bcs_spline", "fit.json")
    spline_cells = load_key(path_spline, KEY_BC)
    spline_map = omit_coverage(path_spline, base.pair_shifts(nominal_bc, spline_cells, scale))
    check_scaled_shift(path_spline, nominal_bc, spline_cells, scale, spline_map, False)
    spline_piece, spline_counts = base.family_rms([spline_map])
    pairs.append(("spline_bc", spline_piece, spline_counts, [path_spline, path_bc]))
    signed["spline_bc"] = [spline_map]

    injection = {}
    injection_file = {}
    injection_archive = {}
    for key in nominal_bc:
        if((key not in unw_bc) or (key not in scale_unw) or (key not in unw_norm)):
            continue
        new_a0 = float(nominal_bc[key]["Fit_Par_A"]) * scale[key]
        unw_a0 = float(unw_bc[key]["Fit_Par_A"]) * scale_unw[key]
        injection[key] = {
            "A": new_a0 - unw_a0,
            "B": float(nominal_bc[key]["Fit_Par_B"]) - float(unw_bc[key]["Fit_Par_B"]),
            "C": float(nominal_bc[key]["Fit_Par_C"]) - float(unw_bc[key]["Fit_Par_C"]),
        }
        injection_file[key] = {"A": new_a0 - float(unw_norm[key]["Fit_Par_A"])}
        injection_archive[key] = {"A": float(archive[key]["Fit_Par_A"]) - float(unw_norm[key]["Fit_Par_A"])}
    unw_bc_absolute = os.path.abspath(path_unw_bc)
    if((known_fits is not None) and (unw_bc_absolute not in known_fits)):
        raise SystemExit("variation fit is not in the coverage scan: %s" % path_unw_bc)
    injection_banned = drop_by_path.get(unw_bc_absolute, set())
    if(len(injection_banned) > 0):
        injection = {key: value for key, value in injection.items() if(key not in injection_banned)}
    kept_by_path[unw_bc_absolute] = set(injection.keys())
    if(len(injection) > 0):
        injection_key = sorted(injection.keys())[0]
        scaled_a = (float(nominal_bc[injection_key]["Fit_Par_A"]) * scale[injection_key]) - (float(unw_bc[injection_key]["Fit_Par_A"]) * scale_unw[injection_key])
        raw_a = float(nominal_bc[injection_key]["Fit_Par_A"]) - float(unw_bc[injection_key]["Fit_Par_A"])
        if(abs(injection[injection_key]["A"] - scaled_a) > 1.0e-8):
            raise SystemExit("physics-injection A is not the normalized difference")
        if((abs(raw_a - scaled_a) > 1.0e-6) and (abs(injection[injection_key]["A"] - raw_a) <= 1.0e-8)):
            raise SystemExit("physics-injection A was copied without the A0 scale")
    injection_piece, injection_counts = base.family_rms([injection])
    pairs.append(("physics_injection", injection_piece, injection_counts, [path_now, path_unw_norm, path_bc, path_unw_bc]))
    signed["physics_injection"] = [injection]
    injection_gap = 0.0
    archive_gap = 0.0
    for key, row in injection.items():
        injection_gap = max(injection_gap, abs(row["A"] - injection_file[key]["A"]))
        archive_gap = max(archive_gap, abs(row["A"] - injection_archive[key]["A"]))
    print("max |refined-BC injection A minus stored-unweighted-file injection A|: %.6g" % injection_gap)
    print("max |refined-BC injection A minus archived-spline injection A|: %.6g" % archive_gap)

    by_name = {}
    for name, per_bin, counts, used in pairs:
        by_name[name] = per_bin
    final_names = [name for name, _per, _counts, _used in pairs]
    summary = {}
    for name, per_bin, counts, used in pairs:
        summary[name] = {"files": used, "sha256": [sha256(path) for path in used]}
        for letter in LETTERS:
            value, count = base.column_rms(per_bin, letter)
            summary[name][letter] = {"rms": value, "bins": count}
        summary[name]["min_variations"] = min(counts.values()) if(len(counts)) else 0
        summary[name]["max_variations"] = max(counts.values()) if(len(counts)) else 0
    bin_only, _bin_counts = base.family_rms([bin_shifts])
    five_only, _five_counts = base.family_rms([five_shifts])
    for label, piece in (("acceptance_bin_by_bin", bin_only), ("acceptance_5d", five_only)):
        summary[label] = {}
        for letter in LETTERS:
            value, count = base.column_rms(piece, letter)
            summary[label][letter] = {"rms": value, "bins": count}

    variable_groups = {
        "Q2": ["sub_q2_3", "sub_q2_5", "sub_q2_7"],
        "y": ["sub_y_3", "sub_y_5", "sub_y_7"],
        "z": ["sub_z_3", "sub_z_5", "sub_z_7"],
        "PT": ["sub_pt_3", "sub_pt_5", "sub_pt_7"],
        "phi": ["sub_phi_5", "sub_phi_7", "sub_phi_9"],
    }
    variable_rms = {}
    for label, names in variable_groups.items():
        piece, _counts = base.family_rms([kin_by_name[name] for name in names])
        variable_rms[label] = {}
        for letter in LETTERS:
            value, count = base.column_rms(piece, letter)
            variable_rms[label][letter] = {"rms": value, "bins": count}

    new_a0 = {}
    changed_central = []
    stat_left = []
    for key, cell in current.items():
        proposed = {
            "A": float(nominal_bc[key]["Fit_Par_A"]) * scale[key],
            "B": float(nominal_bc[key]["Fit_Par_B"]),
            "C": float(nominal_bc[key]["Fit_Par_C"]),
        }
        proposed_err = {
            "A": float(nominal_bc[key]["Fit_Par_A_ERR"]) * scale[key],
            "B": float(nominal_bc[key]["Fit_Par_B_ERR"]),
            "C": float(nominal_bc[key]["Fit_Par_C_ERR"]),
        }
        new_a0[key] = proposed["A"]
        for letter in LETTERS:
            old_value = float(cell["Fit_Par_%s" % letter])
            old_err = float(cell["Fit_Par_%s_ERR" % letter])
            if(abs(proposed[letter] - old_value) > 1.0e-9):
                changed_central.append({
                    "bin": key,
                    "letter": letter,
                    "old": old_value,
                    "new": proposed[letter],
                    "old_err": old_err,
                    "new_err": proposed_err[letter],
                })
            elif(abs(proposed_err[letter] - old_err) > 1.0e-9):
                stat_left.append({
                    "bin": key,
                    "letter": letter,
                    "old_err": old_err,
                    "refined_err": proposed_err[letter],
                })

    holes = []
    new_sys = {}
    for key in nominal_bc:
        new_sys[key] = {}
        for letter in LETTERS:
            pieces = []
            for name in final_names:
                row = by_name[name].get(key)
                if(row is None):
                    holes.append("%s %s %s" % (name, letter, key))
                    continue
                pieces.append(row[letter])
            if(len(pieces) == 0):
                raise SystemExit("no systematic source remains in %s %s; refusing a zero total" % (key, letter))
            new_sys[key][letter] = math.sqrt(sum(value * value for value in pieces))
    combined = {}
    for letter in LETTERS:
        combined[letter] = base.rms([new_sys[key][letter] for key in new_sys])
    print("new combined RMS: %s" % combined)

    share_sums = {letter: 0.0 for letter in LETTERS}
    source_square = {name: {letter: 0.0 for letter in LETTERS} for name in final_names}
    per_bin_share = {}
    for key in sorted(nominal_bc.keys()):
        per_bin_share[key] = {}
        for letter in LETTERS:
            present = []
            for name in final_names:
                row = by_name[name].get(key)
                if(row is None):
                    continue
                present.append((name, float(row[letter])))
            total_square = 0.0
            for name, value in present:
                total_square += value * value
                source_square[name][letter] += value * value
            share_sums[letter] += total_square
            order = sorted(present, key=lambda item: (-abs(item[1]), item[0]))
            ranks = {}
            rank = 0
            seen = 0
            previous = None
            for name, value in order:
                seen += 1
                if((previous is None) or (abs(value) != abs(previous))):
                    rank = seen
                    previous = abs(value)
                ranks[name] = rank
            block = {
                "sources_present": [name for name, _value in present],
                "contributions": {name: value for name, value in present},
                "shares_percent": {},
                "ranks": ranks,
                "sum_squared": total_square,
                "combined_quadrature": new_sys[key][letter],
            }
            for name, value in present:
                if(total_square == 0.0):
                    block["shares_percent"][name] = None
                else:
                    block["shares_percent"][name] = 100.0 * value * value / total_square
            per_bin_share[key][letter] = block
    table_shares = {}
    for name in final_names:
        table_shares[name] = {}
        for letter in LETTERS:
            if(share_sums[letter] == 0.0):
                table_shares[name][letter] = None
            else:
                table_shares[name][letter] = 100.0 * source_square[name][letter] / share_sums[letter]
    share_total = {}
    for letter in LETTERS:
        share_total[letter] = sum(table_shares[name][letter] for name in final_names)
    print("table share sums: %s" % share_total)

    ranges = {}
    for name, maps in signed.items():
        ranges[name] = {"count": sum(len(item) for item in maps)}
        for letter in LETTERS:
            lowest, highest = column_minmax(maps, letter)
            mean_value, count = mean_abs(maps, letter)
            ranges[name][letter] = {"min": lowest, "max": highest, "mean_abs": mean_value, "n": count}

    extrema = {}
    for group in ("electron", "pion"):
        extrema[group] = {}
        for letter in LETTERS:
            extrema[group][letter] = {"min": None, "max": None}
    for var_id, key, shift in sector_shift_rows:
        group = "pion" if(var_id.startswith("pipS")) else "electron"
        for letter in LETTERS:
            value = shift[letter]
            slot = extrema[group][letter]
            record = {"value": value, "variation": var_id, "bin": key}
            if((slot["min"] is None) or (value < slot["min"]["value"])):
                slot["min"] = record
            if((slot["max"] is None) or (value > slot["max"]["value"])):
                slot["max"] = record

    order = list(active_sector_ids)

    def variation_label(var_id):
        if(var_id.startswith("pipS")):
            return "P%d" % int(var_id.replace("pipS", "").replace("o", ""))
        return "E%d" % int(var_id.replace("eS", "").replace("o", ""))

    unavailable_rows = []
    for key in nominal_bc:
        q2y_bin = int(key.split("Q2_y_Bin_")[1].split(")")[0])
        zpt_bin = int(key.split("z_pT_Bin_")[1].split(")")[0])
        labels = []
        for var_id in order:
            if(key not in sector_kept_by_id[var_id]):
                labels.append(variation_label(var_id))
        if(len(labels) > 0):
            unavailable_rows.append({"q2y": q2y_bin, "zpt": zpt_bin, "labels": labels})
    unavailable_rows.sort(key=lambda row: (row["q2y"], row["zpt"]))
    bins_without_sector = sorted([key for key in nominal_bc if(key not in sector)])

    payload = {
        "status": status_label,
        "excluded_sources": sorted(excluded),
        "included_sources": list(final_names),
        "scale_definition": "archived spline A0 / pre-refinement spline BC raw A; unweighted normalized A0 / pre-refinement unweighted BC raw A for the 5D pair only",
        "max_relative_scale_gap": scale_gap,
        "max_relative_scale_move_if_refined_raw": scale_move,
        "injection_A_versus_single_spline_scale_max_abs": injection_gap,
        "injection_A_versus_archived_spline_max_abs": archive_gap,
        "sector_quality_omitted": len(sector_quality_omitted),
        "sector_missing": len(sector_missing),
        "sector_present_unusable": len(sector_present_unusable),
        "sector_user_excluded": len(sector_user_excluded),
        "sector_requested_already_unavailable": len(sector_requested_already_unavailable),
        "sector_unmatched": sector_unmatched,
        "sector_kinds": list(sector_kinds),
        "active_sector_ids": list(active_sector_ids),
        "sector_defined_variations": len(active_sector_ids),
        "sector_not_in_study_paths": list(not_in_study_paths),
        "sector_kept": sum(len(item) for item in sector_maps),
        "bins_without_sector": bins_without_sector,
        "bins_missing_a_source": holes,
        "combined_rms": combined,
        "sources": summary,
        "variable_rms": variable_rms,
        "per_bin_sys": new_sys,
        "changed_central_count": len(changed_central),
        "stat_error_left_when_central_unchanged": len(stat_left),
    }
    budget_path = os.path.join(out_dir, "budget.json")
    with open(budget_path, "w") as handle:
        json.dump(payload, handle)
        handle.write("\n")
    print("wrote %s" % budget_path)

    shares = {
        "definition": "In one bin, a source percentage is 100 times that source RMS squared over the sum of the squared RMS values of the sources present in that bin. A missing comparison is omitted, not entered as zero. The table percentage is 100 times the sum over bins of that source's squared per-bin RMS, over the sum over bins of those per-bin sums. Rank 1 is the largest absolute contribution in that bin. Tied absolute values share the smaller rank and the next rank skips.",
        "sources": final_names,
        "table_shares_percent": table_shares,
        "table_share_sums": share_total,
        "per_bin": per_bin_share,
    }
    share_path = os.path.join(out_dir, "per_bin_source_shares.json")
    with open(share_path, "w") as handle:
        json.dump(shares, handle)
        handle.write("\n")
    print("wrote %s" % share_path)

    numbers = {
        "combined_rms": combined,
        "sources": {name: {letter: summary[name][letter] for letter in LETTERS} for name in list(summary.keys())},
        "table_shares_percent": table_shares,
        "ranges": ranges,
        "variable_rms": variable_rms,
        "sector": {
            "missing": len(sector_missing),
            "present_unusable": len(sector_present_unusable),
            "quality_omitted": len(sector_quality_omitted),
            "user_excluded": len(sector_user_excluded),
            "already_unavailable": len(sector_requested_already_unavailable),
            "unmatched": sector_unmatched,
            "kept": sum(len(item) for item in sector_maps),
            "defined_variations": len(active_sector_ids),
            "active_ids": list(active_sector_ids),
            "bins_without_sector": len(bins_without_sector),
            "unavailable_rows": unavailable_rows,
            "extrema": extrema,
        },
        "changed_central": changed_central,
        "stat_left": stat_left,
        "injection_gap": injection_gap,
        "archive_gap": archive_gap,
        "scale_gap": scale_gap,
        "scale_move": scale_move,
    }
    numbers_path = os.path.join(out_dir, "propagate_numbers.json")
    with open(numbers_path, "w") as handle:
        json.dump(numbers, handle)
        handle.write("\n")
    print("wrote %s" % numbers_path)

    if(not os.path.isfile(preserved_norm)):
        raise SystemExit("preserved normalized file is missing: %s" % preserved_norm)
    preserved = json.load(open(preserved_norm))
    preserved_cells = preserved[KEY_BC]
    if(set(preserved_cells) != set(new_sys)):
        raise SystemExit("preserved normalized bins and the systematic budget differ")
    if(write_live):
        live = json.load(open(preserved_norm))
        live_cells = live[KEY_BC]
        for key, cell in live_cells.items():
            for letter in LETTERS:
                cell["Fit_Par_%s_SYS" % letter] = new_sys[key][letter]
        live["final_systematic_budget"] = status_label
        live["budget_path"] = budget_path
        live["budget_fingerprint"] = {"mtime": os.path.getmtime(budget_path), "size": os.path.getsize(budget_path)}
        with open(path_now, "w") as handle:
            json.dump(live, handle)
            handle.write("\n")
        written = json.load(open(path_now))[KEY_BC]
        for key, cell in written.items():
            original = preserved_cells[key]
            for letter in LETTERS:
                if(cell["Fit_Par_%s" % letter] != original["Fit_Par_%s" % letter]):
                    raise SystemExit("central value changed in %s %s" % (key, letter))
                if(cell["Fit_Par_%s_ERR" % letter] != original["Fit_Par_%s_ERR" % letter]):
                    raise SystemExit("statistical uncertainty changed in %s %s" % (key, letter))
                if(abs(float(cell["Fit_Par_%s_SYS" % letter]) - float(new_sys[key][letter])) > 1.0e-12):
                    raise SystemExit("systematic field was not the normalized budget value in %s %s" % (key, letter))
        print("updated only Fit_Par_*_SYS in %s" % path_now)
    print("central-value differences versus the pre-refinement archive: %d" % len(changed_central))
    print("statistical errors left unchanged despite a refined error: %d" % len(stat_left))

    fit_rms = {}
    updated = preserved_cells
    for letter in LETTERS:
        fit_rms[letter] = base.rms([float(updated[key]["Fit_Par_%s_ERR" % letter]) for key in updated])
    print("fit uncertainty RMS: %s" % fit_rms)
    marks = {}
    for name in final_names:
        marks[name] = ""
        for letter in LETTERS:
            value = summary[name][letter]["rms"]
            if(value > fit_rms[letter]):
                marks[name] += ">"
            elif(value < fit_rms[letter]):
                marks[name] += "<"
            else:
                marks[name] += "="
        print("%s  %.6g  %.6g  %.6g  share %.3f %.3f %.3f  %s" % (
            name,
            summary[name]["A"]["rms"], summary[name]["B"]["rms"], summary[name]["C"]["rms"],
            table_shares[name]["A"], table_shares[name]["B"], table_shares[name]["C"],
            marks[name],
        ))
    combined_marks = ""
    for letter in LETTERS:
        if(combined[letter] > fit_rms[letter]):
            combined_marks += ">"
        elif(combined[letter] < fit_rms[letter]):
            combined_marks += "<"
        else:
            combined_marks += "="
    print("combined %s" % combined_marks)
    with open(os.path.join(out_dir, "versus_fit.json"), "w") as handle:
        json.dump({"fit_rms": fit_rms, "marks": marks, "combined": combined_marks}, handle)
        handle.write("\n")

    after = protected_hashes()
    for path, digest in before.items():
        if(after[path] != digest):
            raise SystemExit("protected file changed: %s" % path)
    print("protected files unchanged")
    return {
        "kept_by_path": kept_by_path,
        "sector_kept_by_id": sector_kept_by_id,
        "combined": combined,
        "summary": summary,
        "table_shares": table_shares,
        "new_sys": new_sys,
        "per_bin_share": per_bin_share,
        "final_names": final_names,
        "sector_unmatched": sector_unmatched,
        "marks": marks,
        "fit_rms": fit_rms,
        "budget_path": budget_path,
        "excluded_sources": sorted(excluded),
        "excluded_paths": sorted(excluded_paths),
        "sector_kinds": list(sector_kinds),
        "active_sector_ids": list(active_sector_ids),
        "sector_defined_variations": len(active_sector_ids),
        "not_in_study_paths": list(not_in_study_paths),
    }


def compare_reproduction(got_budget_path, got_share_path, preserved_budget_path, preserved_share_path):
    got_budget = json.load(open(got_budget_path))
    old_budget = json.load(open(preserved_budget_path))
    got_shares = json.load(open(got_share_path))
    old_shares = json.load(open(preserved_share_path))
    mismatches = []
    for letter in LETTERS:
        if(not same_number(got_budget["combined_rms"][letter], old_budget["combined_rms"][letter])):
            mismatches.append("combined %s" % letter)
    if(int(got_budget["sector_kept"]) != int(old_budget["sector_kept"])):
        mismatches.append("sector_kept %s versus %s" % (got_budget["sector_kept"], old_budget["sector_kept"]))
    for name, old_source in old_budget["sources"].items():
        got_source = got_budget["sources"].get(name)
        if(got_source is None):
            mismatches.append("missing source %s" % name)
            continue
        for letter in LETTERS:
            if(not same_number(got_source[letter]["rms"], old_source[letter]["rms"])):
                mismatches.append("rms %s %s" % (name, letter))
            if(int(got_source[letter]["bins"]) != int(old_source[letter]["bins"])):
                mismatches.append("bins %s %s" % (name, letter))
    for name in got_budget["sources"]:
        if(name not in old_budget["sources"]):
            mismatches.append("extra source %s" % name)
    for name, old_row in old_shares["table_shares_percent"].items():
        got_row = got_shares["table_shares_percent"].get(name)
        if(got_row is None):
            mismatches.append("missing share %s" % name)
            continue
        for letter in LETTERS:
            if(not same_number(got_row[letter], old_row[letter])):
                mismatches.append("share %s %s" % (name, letter))
    old_sys = old_budget["per_bin_sys"]
    got_sys = got_budget["per_bin_sys"]
    if(set(old_sys) != set(got_sys)):
        mismatches.append("per-bin systematic keys differ")
    else:
        for key, old_row in old_sys.items():
            for letter in LETTERS:
                if(not same_number(got_sys[key][letter], old_row[letter])):
                    mismatches.append("per-bin %s %s" % (key, letter))
                    if(len(mismatches) > 30):
                        break
            if(len(mismatches) > 30):
                break
    return mismatches


def change_between(old_value, new_value):
    if((old_value is None) or (new_value is None)):
        return {"status": "unavailable", "absolute": None, "relative": None, "old": old_value, "new": new_value}
    old_number = float(old_value)
    new_number = float(new_value)
    absolute = new_number - old_number
    if(old_number == 0.0):
        return {"status": "absolute", "absolute": absolute, "relative": None, "old": old_number, "new": new_number}
    return {
        "status": "relative",
        "absolute": absolute,
        "relative": absolute / old_number,
        "old": old_number,
        "new": new_number,
    }


def quality_flags(cell):
    flags = {
        "fit_present": isinstance(cell, dict),
        "ndf_below_1": False,
        "nonfinite_coefficient": False,
        "abs_b_above_10": False,
        "abs_c_above_10": False,
        "abs_a_below_1": False,
        "usable_sector": False,
        "ndf": None,
    }
    if(not isinstance(cell, dict)):
        flags["ndf_below_1"] = True
        return flags
    ndf = cell.get("NDF")
    flags["ndf"] = ndf
    if((ndf is None) or (float(ndf) < 1.0)):
        flags["ndf_below_1"] = True
    for letter in LETTERS:
        value = cell.get("Fit_Par_%s" % letter)
        if((not isinstance(value, (int, float))) or (not math.isfinite(float(value)))):
            flags["nonfinite_coefficient"] = True
    if(not flags["nonfinite_coefficient"]):
        if(abs(float(cell["Fit_Par_B"])) > 10.0):
            flags["abs_b_above_10"] = True
        if(abs(float(cell["Fit_Par_C"])) > 10.0):
            flags["abs_c_above_10"] = True
        if(abs(float(cell["Fit_Par_A"])) < 1.0):
            flags["abs_a_below_1"] = True
    flags["usable_sector"] = base.usable_sector(cell)
    return flags


def write_audit(coverage_payload, by_fit, reproduce, covered, out_dir, excluded_paths=None, coverage_path="", not_in_study_paths=None, active_sector_ids=None):
    if(excluded_paths is None):
        excluded_paths = set()
    if(not_in_study_paths is None):
        not_in_study_paths = set()
    else:
        not_in_study_paths = set(not_in_study_paths)
    if(active_sector_ids is None):
        active_sector_ids = []
    jobs = json.load(open(coverage_payload["jobs_path"]))
    exclusions = base.load_sector_exclusions()
    fit_cache = {}
    records = []
    incremental = []
    overlap_manual = []
    overlap_quality = []
    for job in jobs:
        fit_path = os.path.abspath(job["variation_json"])
        item = by_fit[fit_path]
        if(fit_path not in fit_cache):
            payload = json.load(open(fit_path))
            fit_cache[fit_path] = payload.get(job["variation_fit_key"], {})
        cells = fit_cache[fit_path]
        sector_id = item["sector_id"]
        listed = exclusions.get(sector_id, set()) if(sector_id != "") else set()
        old_kept = set()
        if(reproduce is not None):
            old_kept = reproduce["kept_by_path"].get(fit_path, set())
        new_kept = covered["kept_by_path"].get(fit_path, set())
        source_excluded = fit_path in excluded_paths
        not_in_study = fit_path in not_in_study_paths
        for key, measured in item["records"].items():
            cell = cells.get(key)
            flags = quality_flags(cell)
            fails = coverage_fails(measured)
            manual = key in listed
            previously = None
            if(reproduce is not None):
                previously = key in old_kept
            included = (not source_excluded) and (key in new_kept)
            q2y = int(key.split("Q2_y_Bin_")[1].split(")")[0])
            zpt = int(key.split("z_pT_Bin_")[1].split(")")[0])
            if((reproduce is not None) and (previously) and (not included) and (not source_excluded) and (not not_in_study)):
                incremental.append("%s %s %s" % (job["source_id"], job["variation_name"], key))
                if(not fails):
                    raise SystemExit("removed a previously eligible comparison that passes coverage: %s %s" % (job["variation_name"], key))
            if((fails) and (manual)):
                overlap_manual.append("%s %s" % (sector_id, key))
            if((fails) and (job["source_id"] == "sector") and (not flags["usable_sector"])):
                overlap_quality.append("%s %s" % (sector_id, key))
            if((included) and (fails)):
                raise SystemExit("included a coverage failure: %s %s" % (job["variation_name"], key))
            records.append({
                "source_id": job["source_id"],
                "variation_name": job["variation_name"],
                "variation_index": job["variation_index"],
                "q2y": q2y,
                "zpt": zpt,
                "bin": key,
                "histogram": measured.get("name", ""),
                "histogram_root": job["variation_root"],
                "kind": job["variation_kind"],
                "smear": job["variation_smear"],
                "stage": item["stage"],
                "baseline_root": job["baseline_root"],
                "baseline_kind": job["baseline_kind"],
                "baseline_smear": job["baseline_smear"],
                "baseline_json": job["baseline_json"],
                "baseline_fit_key": job["baseline_fit_key"],
                "missing_deg": measured.get("missing_deg"),
                "empty_bins": measured.get("empty_bins"),
                "nbins": measured.get("nbins"),
                "coverage_status": measured.get("status"),
                "coverage_fail": fails,
                "manual_exclusion": manual,
                "quality": flags,
                "quality_rule_applied": job["source_id"] == "sector",
                "previously_included": previously,
                "included": included,
                "exclusion_reason": "source_excluded" if(source_excluded) else ("pion_sector_not_in_study" if(not_in_study) else ""),
            })
    exceptions = [
        ("eS4o", 15, 22),
        ("pipS4o", 15, 21),
        ("pipS5o", 9, 9),
    ]
    exception_rows = []
    for sector_id, q2y, zpt in exceptions:
        matched = [
            row for row in records
            if((row["source_id"] == "sector") and (row["q2y"] == q2y) and (row["zpt"] == zpt) and (sector_id in row["histogram_root"]))
        ]
        if(len(matched) != 1):
            raise SystemExit("manual exception %s (%d, %d) matched %d rows" % (sector_id, q2y, zpt, len(matched)))
        row = matched[0]
        if((row["coverage_fail"]) or (not row["manual_exclusion"]) or (row["included"])):
            raise SystemExit("manual exception %s (%d, %d) is not retained as an exclusion that passes coverage" % (sector_id, q2y, zpt))
        exception_rows.append(row)
    audit = {
        "coverage_records_role": "historical_full_campaign_scan",
        "coverage_records_path": os.path.abspath(coverage_path) if(coverage_path != "") else "",
        "records": records,
        "incremental_removals": incremental,
        "incremental_count": len(incremental),
        "coverage_fail_count": sum(1 for row in records if(row["coverage_fail"])),
        "included_count": sum(1 for row in records if(row["included"])),
        "version_included_count": sum(1 for row in records if(row["included"])),
        "source_excluded_count": sum(1 for row in records if(row["exclusion_reason"] == "source_excluded")),
        "not_in_study_count": sum(1 for row in records if(row["exclusion_reason"] == "pion_sector_not_in_study")),
        "active_sector_ids": list(active_sector_ids),
        "overlap_manual": overlap_manual,
        "overlap_manual_count": len(overlap_manual),
        "overlap_quality": overlap_quality,
        "overlap_quality_count": len(overlap_quality),
        "manual_exceptions": [
            {"sector": row["histogram_root"], "bin": row["bin"], "missing_deg": row["missing_deg"], "included": row["included"]}
            for row in exception_rows
        ],
    }
    audit_path = os.path.join(out_dir, "coverage_audit.json")
    with open(audit_path, "w") as handle:
        json.dump(audit, handle)
        handle.write("\n")
    print("wrote %s" % audit_path)
    print("included %d incremental %d coverage failures %d" % (
        audit["included_count"], audit["incremental_count"], audit["coverage_fail_count"]))
    return audit


def write_comparison(preserved_budget_path, preserved_share_path, covered, out_dir, excluded_sources=None):
    if(excluded_sources is None):
        excluded_sources = set()
    old_budget = json.load(open(preserved_budget_path))
    old_shares = json.load(open(preserved_share_path))
    sources = {}
    for name, old_source in old_budget["sources"].items():
        got_source = covered["summary"].get(name)
        sources[name] = {}
        for letter in LETTERS:
            old_rms = None if(old_source is None) else old_source[letter]["rms"]
            if(name in excluded_sources):
                sources[name][letter] = {"status": "excluded", "absolute": None, "relative": None, "old": old_rms, "new": None}
                continue
            new_rms = None if(got_source is None) else got_source[letter]["rms"]
            sources[name][letter] = change_between(old_rms, new_rms)
    combined = {}
    for letter in LETTERS:
        combined[letter] = change_between(old_budget["combined_rms"][letter], covered["combined"][letter])
    shares = {}
    for name, old_row in old_shares["table_shares_percent"].items():
        got_row = covered["table_shares"].get(name)
        shares[name] = {}
        for letter in LETTERS:
            if(name in excluded_sources):
                shares[name][letter] = {"status": "excluded", "absolute": None, "relative": None, "old": old_row[letter], "new": None}
                continue
            new_value = None if(got_row is None) else got_row[letter]
            shares[name][letter] = change_between(old_row[letter], new_value)
    largest = []
    old_sys = old_budget["per_bin_sys"]
    for key, new_row in covered["new_sys"].items():
        old_row = old_sys.get(key)
        for letter in LETTERS:
            old_value = None if(old_row is None) else old_row[letter]
            change = change_between(old_value, new_row[letter])
            if(change["absolute"] is None):
                continue
            largest.append({"bin": key, "letter": letter, "source": "combined", "change": change})
    largest.sort(key=lambda item: abs(item["change"]["absolute"]), reverse=True)
    source_largest = []
    old_per_bin = old_shares["per_bin"]
    for key, block in covered["per_bin_share"].items():
        for letter in LETTERS:
            old_block = old_per_bin.get(key, {}).get(letter, {})
            old_contributions = old_block.get("contributions", {})
            new_contributions = block[letter]["contributions"]
            names = set(old_contributions) | set(new_contributions)
            for name in names:
                old_value = old_contributions.get(name)
                if(name in excluded_sources):
                    source_largest.append({
                        "bin": key,
                        "letter": letter,
                        "source": name,
                        "change": {
                            "status": "excluded",
                            "absolute": None,
                            "relative": None,
                            "old": old_value,
                            "new": None,
                        },
                    })
                    continue
                new_value = new_contributions.get(name)
                change = change_between(old_value, new_value)
                source_largest.append({"bin": key, "letter": letter, "source": name, "change": change})
    numeric = [item for item in source_largest if(item["change"]["absolute"] is not None)]
    numeric.sort(key=lambda item: abs(item["change"]["absolute"]), reverse=True)
    unavailable = [item for item in source_largest if(item["change"]["status"] == "unavailable")]
    excluded_per_bin = [item for item in source_largest if(item["change"]["status"] == "excluded")]
    excluded_per_bin_counts = {}
    for item in excluded_per_bin:
        if(item["change"]["new"] is not None):
            raise SystemExit("excluded per-bin contribution stored a new value for %s" % item["source"])
        excluded_per_bin_counts[item["source"]] = excluded_per_bin_counts.get(item["source"], 0) + 1
    payload = {
        "baseline_budget": os.path.abspath(preserved_budget_path),
        "baseline_shares": os.path.abspath(preserved_share_path),
        "excluded_sources": sorted(excluded_sources),
        "combined": combined,
        "sources": sources,
        "table_shares_percent": shares,
        "largest_combined": largest[:30],
        "largest_source": numeric[:40],
        "unavailable_source_changes": len(unavailable),
        "excluded_per_bin_count": len(excluded_per_bin),
        "excluded_per_bin_counts": excluded_per_bin_counts,
    }
    path = os.path.join(out_dir, "budget_comparison.json")
    with open(path, "w") as handle:
        json.dump(payload, handle)
        handle.write("\n")
    print("wrote %s" % path)
    return payload


def git_revision():
    analysis = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        revision = subprocess.check_output(["git", "-C", analysis, "rev-parse", "HEAD"], text=True).strip()
    except(subprocess.CalledProcessError, OSError):
        revision = "unavailable"
    return analysis, revision


def version_status(excluded, sector_kinds):
    names = set(excluded)
    if(len(names) == 0):
        label = "rerun_refinement_20261108_coverage135"
    elif(names == set(["chi2_pid"])):
        label = "rerun_refinement_20261108_coverage135_no_chi2_pid"
    elif(names == set(["chi2_pid", "acceptance_reweighting"])):
        label = "rerun_refinement_20261108_coverage135_no_chi2_pid_no_reweight"
    else:
        raise SystemExit("unsupported exclusion set %s" % sorted(names))
    kinds = list(sector_kinds)
    if(kinds == ["electron", "pion"]):
        return label
    if(kinds == ["electron"]):
        return label + "_electron_sector"
    raise SystemExit("unsupported sector kinds %s" % kinds)


def write_version_normalized(live_path, covered, destination, status_label):
    original = json.load(open(live_path))
    live = json.load(open(live_path))
    cells = live[KEY_BC]
    original_cells = original[KEY_BC]
    new_sys = covered["new_sys"]
    if(set(cells) != set(new_sys)):
        raise SystemExit("normalized bins and the version budget differ")
    for key, cell in cells.items():
        for letter in LETTERS:
            cell["Fit_Par_%s_SYS" % letter] = new_sys[key][letter]
    budget_path = covered["budget_path"]
    live["final_systematic_budget"] = status_label
    live["budget_path"] = os.path.abspath(budget_path)
    live["budget_fingerprint"] = {"mtime": os.path.getmtime(budget_path), "size": os.path.getsize(budget_path)}
    live["excluded_sources"] = covered["excluded_sources"]
    live["included_sources"] = covered["final_names"]
    with open(destination, "w") as handle:
        json.dump(live, handle)
        handle.write("\n")
    written = json.load(open(destination))[KEY_BC]
    for key, cell in written.items():
        source = original_cells[key]
        for letter in LETTERS:
            if(cell["Fit_Par_%s" % letter] != source["Fit_Par_%s" % letter]):
                raise SystemExit("central value changed in %s %s" % (key, letter))
            if(cell["Fit_Par_%s_ERR" % letter] != source["Fit_Par_%s_ERR" % letter]):
                raise SystemExit("statistical uncertainty changed in %s %s" % (key, letter))
            if(abs(float(cell["Fit_Par_%s_SYS" % letter]) - float(new_sys[key][letter])) > 1.0e-12):
                raise SystemExit("systematic field was not the version budget value in %s %s" % (key, letter))
    print("wrote %s" % destination)


def covered_from_saved(budget_path, share_path):
    budget = json.load(open(budget_path))
    shares = json.load(open(share_path))
    summary = {}
    for name, source in budget["sources"].items():
        summary[name] = {}
        for letter in LETTERS:
            summary[name][letter] = {"rms": source[letter]["rms"]}
    return {
        "summary": summary,
        "combined": budget["combined_rms"],
        "table_shares": shares["table_shares_percent"],
        "new_sys": budget["per_bin_sys"],
        "per_bin_share": shares["per_bin"],
        "excluded_sources": list(budget.get("excluded_sources", [])),
    }


def rewrite_saved_comparison(args):
    if((args.comparison_baseline_budget == "") or (args.comparison_baseline_shares == "")):
        raise SystemExit("comparison_only requires comparison_baseline_budget and comparison_baseline_shares")
    budget_path = os.path.join(args.output, "budget.json")
    share_path = os.path.join(args.output, "per_bin_source_shares.json")
    covered = covered_from_saved(budget_path, share_path)
    excluded = set(covered["excluded_sources"])
    comparison = write_comparison(
        args.comparison_baseline_budget,
        args.comparison_baseline_shares,
        covered,
        args.output,
        excluded,
    )
    for filename in ("provenance.json", "reproduction.json"):
        path = os.path.join(args.output, filename)
        payload = json.load(open(path))
        payload["comparison_baseline"] = os.path.abspath(args.comparison_baseline_budget)
        payload["comparison_baseline_shares"] = os.path.abspath(args.comparison_baseline_shares)
        payload["comparison_baseline_role"] = "full_coverage135_budget"
        payload["preserved_budget_role"] = "reproduction_anchor_before_coverage135"
        payload["combined_change"] = comparison["combined"]
        with open(path, "w") as handle:
            json.dump(payload, handle)
            handle.write("\n")
        print("updated %s" % path)
    print("comparison_only excluded %s" % sorted(excluded))
    print("version_included_count left at %s" % json.load(open(os.path.join(args.output, "provenance.json")))["version_included_count"])


def main():
    args = parse_args()
    if(args.comparison_only):
        rewrite_saved_comparison(args)
        return
    excluded = [item.strip() for item in args.exclude_sources.split(",") if(item.strip() != "")]
    sector_kinds = selected_sector_kinds(args.sector_kinds)
    status_label = version_status(excluded, sector_kinds)
    coverage_payload, by_fit = load_coverage(args.coverage)
    drops, known_fits = drop_map(by_fit)
    reproduce = None
    mismatches = None
    if(args.skip_reproduction or (len(excluded) > 0)):
        print("reproduction skipped")
    else:
        print("reproduction aggregation, coverage filter off")
        reproduce = aggregate({}, args.reproduce_dir, False, args.preserved_norm, None, "reproduce_without_coverage")
        mismatches = compare_reproduction(
            os.path.join(args.reproduce_dir, "budget.json"),
            os.path.join(args.reproduce_dir, "per_bin_source_shares.json"),
            args.preserved_budget,
            args.preserved_shares,
        )
        if(len(mismatches) > 0):
            for line in mismatches[:40]:
                print(line)
            raise SystemExit("reproduction does not match the preserved budget (%d mismatches)" % len(mismatches))
        print("reproduction matches the preserved per-source RMS, combined RMS, and table shares")
    print("coverage aggregation")
    write_live = (len(excluded) == 0) and (not args.no_write_live)
    covered = aggregate(drops, args.output, write_live, args.preserved_norm, known_fits, status_label, excluded, sector_kinds)
    audit = write_audit(
        coverage_payload, by_fit, reproduce, covered, args.output,
        set(covered["excluded_paths"]), args.coverage,
        covered["not_in_study_paths"], covered["active_sector_ids"],
    )
    comparison = write_comparison(
        args.preserved_budget, args.preserved_shares, covered, args.output, set(excluded),
    )
    if(args.normalized_out != ""):
        live_path = os.path.join(CAMP, "corrected", "spline", "normalized_bc.json")
        write_version_normalized(live_path, covered, args.normalized_out, status_label)
    analysis, revision = git_revision()
    reproduction = {
        "git_root": analysis,
        "git_revision": revision,
        "script": os.path.abspath(__file__),
        "script_sha256": sha256(os.path.abspath(__file__)),
        "coverage_records": os.path.abspath(args.coverage),
        "jobs": coverage_payload["jobs_path"],
        "exclusions": EXCLUSIONS_PATH,
        "preserved_budget": os.path.abspath(args.preserved_budget),
        "preserved_norm": os.path.abspath(args.preserved_norm),
        "threshold_deg": 135.0,
        "pass_rule": coverage_payload["pass_rule"],
        "scale_definition": "archived spline A0 / pre-refinement spline BC raw A; unweighted normalized A0 / pre-refinement unweighted BC raw A for the 5D pair and the physics-injection A0 difference",
        "aggregation": "per bin, RMS over the variations present in that bin; missing variations omitted, not entered as zero; source RMS is the RMS of those per-bin values; table share is the bin-weighted share of summed squared per-bin contributions",
        "quality_rule": "NDF < 1, non-finite coefficient, |B| > 10, |C| > 10, or |A| < 1, applied to sector comparisons only",
        "reproduction_mismatches": mismatches,
        "reproduction_ran": reproduce is not None,
        "comparison_baseline": os.path.abspath(args.preserved_budget),
        "excluded_sources": covered["excluded_sources"],
        "excluded_paths": covered["excluded_paths"],
        "included_sources": covered["final_names"],
        "sector_kinds": covered["sector_kinds"],
        "active_sector_ids": covered["active_sector_ids"],
        "sector_defined_variations": covered["sector_defined_variations"],
        "not_in_study_count": audit["not_in_study_count"],
        "coverage_records_role": "historical_full_campaign_scan",
        "nominals": coverage_payload["nominals"],
        "reference": coverage_payload["reference"],
        "sector_unmatched": covered["sector_unmatched"],
        "incremental_count": audit["incremental_count"],
        "included_count": audit["included_count"],
        "version_included_count": audit["version_included_count"],
        "source_excluded_count": audit["source_excluded_count"],
        "coverage_fail_count": audit["coverage_fail_count"],
        "overlap_manual_count": audit["overlap_manual_count"],
        "overlap_quality_count": audit["overlap_quality_count"],
        "combined_change": comparison["combined"],
    }
    path = os.path.join(args.output, "reproduction.json")
    with open(path, "w") as handle:
        json.dump(reproduction, handle)
        handle.write("\n")
    print("wrote %s" % path)
    provenance_path = os.path.join(args.output, "provenance.json")
    with open(provenance_path, "w") as handle:
        json.dump(reproduction, handle)
        handle.write("\n")
    print("wrote %s" % provenance_path)


if(__name__ == "__main__"):
    main()
