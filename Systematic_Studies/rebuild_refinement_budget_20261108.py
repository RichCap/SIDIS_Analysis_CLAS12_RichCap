#!/usr/bin/env python3
# Rebuild the systematic budget from the accepted 2026-11-08 refinements.
# Pairings match rebuild_final_systematic_budget.py. This file does not refit.

import hashlib
import json
import math
import os
import shutil

import rebuild_final_systematic_budget as base

CAMP = base.CAMP
REF = os.path.join(CAMP, "refinement_20261108")
OUT = os.path.join(CAMP, "budgets", "rerun_refinement_20261108")
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


def main():
    before = protected_hashes()
    os.makedirs(OUT, exist_ok=True)
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
        maps = []
        used = []
        for rel in relatives:
            path = os.path.join(REF, rel)
            cells = load_key(path, KEY_BAYES)
            maps.append(base.pair_shifts(bayes, cells, scale, phi_half=phi_half))
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
    bin_shifts = base.pair_shifts(bayes, bin_cells, scale)
    path_5d = os.path.join(REF, "unweighted", "dimension", "5D", "fit.json")
    five_cells = load_key(path_5d, KEY_5D)
    five_shifts = base.pair_shifts(unw_bayes, five_cells, scale_unw)
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
    for index in range(1, 7):
        for kind, folder in (("eS", "electron_sector"), ("pipS", "pion_sector")):
            var_id = base.sector_variation_id(kind, index)
            path = os.path.join(REF, "spline", folder, var_id, "fit.json")
            cells = load_key(path, KEY_BAYES)
            sector_paths.append(path)
            kept = {}
            listed = sector_exclusions.get(var_id, set())
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
                kept[key] = shift
                sector_shift_rows.append((var_id, key, shift))
            sector_maps.append(kept)
            sector_kept_by_id[var_id] = set(kept.keys())
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

    path_sf0 = os.path.join(REF, "spline", "rc_model", "rc_sf0", "fit.json")
    path_sf2 = os.path.join(REF, "spline", "rc_model", "rc_sf2", "fit.json")
    sf0 = load_key(path_sf0, KEY_RC)
    sf2 = load_key(path_sf2, KEY_RC)
    rc_base = load_key(path_rc, KEY_RC)
    rc_maps = [base.pair_shifts(rc_base, sf0, scale), base.pair_shifts(rc_base, sf2, scale)]
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
        shifts = base.pair_shifts(nominal_bc, cells, scale)
        kin_maps.append(shifts)
        kin_paths.append(path)
        kin_by_name[name] = shifts
    kin_piece, kin_counts = base.family_rms(kin_maps)
    pairs.append(("bc_sampling", kin_piece, kin_counts, kin_paths))
    signed["bc_sampling"] = kin_maps

    path_spline = os.path.join(REF, "spline", "spline_bc", "bcs_spline", "fit.json")
    spline_cells = load_key(path_spline, KEY_BC)
    spline_map = base.pair_shifts(nominal_bc, spline_cells, scale)
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

    order = ["eS%do" % index for index in range(1, 7)] + ["pipS%do" % index for index in range(1, 7)]

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
        "status": "refinement_20261108",
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
    budget_path = os.path.join(OUT, "budget.json")
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
    share_path = os.path.join(OUT, "per_bin_source_shares.json")
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
    numbers_path = os.path.join(OUT, "propagate_numbers.json")
    with open(numbers_path, "w") as handle:
        json.dump(numbers, handle)
        handle.write("\n")
    print("wrote %s" % numbers_path)

    if(not os.path.isfile(archive_norm)):
        shutil.copy2(path_now, archive_norm)
        print("archived live normalized results to %s" % archive_norm)
    else:
        print("archive already present: %s" % archive_norm)
    archived = json.load(open(archive_norm))
    live = json.load(open(archive_norm))
    live_cells = live[KEY_BC]
    if(set(live_cells) != set(new_sys)):
        raise SystemExit("normalized bins and the new systematic budget differ")
    changed_lookup = {}
    for row in changed_central:
        changed_lookup[(row["bin"], row["letter"])] = row
    for key, cell in live_cells.items():
        archived_cell = archived[KEY_BC][key]
        for letter in LETTERS:
            row = changed_lookup.get((key, letter))
            if(row is None):
                if(cell["Fit_Par_%s" % letter] != archived_cell["Fit_Par_%s" % letter]):
                    raise SystemExit("central value changed outside the accepted BC refit in %s %s" % (key, letter))
                if(cell["Fit_Par_%s_ERR" % letter] != archived_cell["Fit_Par_%s_ERR" % letter]):
                    raise SystemExit("statistical uncertainty changed outside the accepted BC refit in %s %s" % (key, letter))
            else:
                cell["Fit_Par_%s" % letter] = row["new"]
                cell["Fit_Par_%s_ERR" % letter] = row["new_err"]
            cell["Fit_Par_%s_SYS" % letter] = new_sys[key][letter]
    live["final_systematic_budget"] = "rerun_refinement_20261108"
    live["budget_path"] = budget_path
    live["budget_fingerprint"] = {"mtime": os.path.getmtime(budget_path), "size": os.path.getsize(budget_path)}
    with open(path_now, "w") as handle:
        json.dump(live, handle)
        handle.write("\n")
    print("updated systematic fields in %s" % path_now)
    print("central values updated: %d" % len(changed_central))
    print("statistical errors left unchanged despite a refined error: %d" % len(stat_left))

    fit_rms = {}
    updated = live[KEY_BC]
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
    with open(os.path.join(OUT, "versus_fit.json"), "w") as handle:
        json.dump({"fit_rms": fit_rms, "marks": marks, "combined": combined_marks}, handle)
        handle.write("\n")

    after = protected_hashes()
    for path, digest in before.items():
        if(after[path] != digest):
            raise SystemExit("protected file changed: %s" % path)
    print("protected files unchanged")


if(__name__ == "__main__"):
    main()
