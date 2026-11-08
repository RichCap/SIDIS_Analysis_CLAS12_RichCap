#!/usr/bin/env python3
# Rebuild the per-bin systematic budget from stored fits.
# Does not refit. Does not add onto the current Fit_Par_*_SYS values.

import hashlib
import json
import math
import os
import shutil

CAMP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "physics_campaign")
OUT = os.path.join(CAMP, "budgets", "rerun_20261106_sector_12_23")
OLD_BUDGET = os.path.join(CAMP, "budgets", "rerun_20261104", "budget.json")
PREVIOUS_BUDGET = os.path.join(CAMP, "budgets", "rerun_20261106_sector_exclusions", "budget.json")
EXCLUSIONS_PATH = os.path.join(CAMP, "budgets", "sector_fit_exclusions_20261106.json")
KEY_BAYES = "Fit_Pars_from_3D_Bayesian"
KEY_BIN = "Fit_Pars_from_3D_Bin"
KEY_5D = "Fit_Pars_from_5D_Bayesian"
KEY_RC = "Fit_Pars_from_3D_RC_Bayesian"
KEY_BC = "Fit_Pars_from_3D_BC_RC_Bayesian"
LETTERS = ("A", "B", "C")


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            block = handle.read(1024 * 1024)
            if(not block):
                break
            digest.update(block)
    return digest.hexdigest()


def load_fit(rel, key):
    path = os.path.join(CAMP, rel)
    payload = json.load(open(path))
    if(key not in payload):
        raise SystemExit("%s has no %s" % (rel, key))
    return path, payload[key]


def rms(values):
    count = len(values)
    if(count == 0):
        return None
    total = 0.0
    for value in values:
        total += float(value) * float(value)
    return math.sqrt(total / float(count))


def load_sector_exclusions():
    payload = json.load(open(EXCLUSIONS_PATH))
    exclusions = {}
    for var_id, bins in payload["exclusions"].items():
        exclusions[var_id] = set(bins)
    if(payload["requested_entries"] != 494):
        raise SystemExit("exclusion file does not contain 494 entries")
    if(payload["distinct_kinematic_bins"] != 107):
        raise SystemExit("exclusion file does not contain 107 kinematic bins")
    return exclusions


def sector_variation_id(kind, index):
    return "%s%do" % (kind, index)


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
    # The one stored electron fit with B = 119038 does not determine a cosine coefficient.
    if((abs(float(cell["Fit_Par_B"])) > 10.0) or (abs(float(cell["Fit_Par_C"])) > 10.0) or (abs(float(cell["Fit_Par_A"])) < 1.0)):
        return False
    return True


def pair_shifts(nominal, alternative, scale, phi_half=False):
    out = {}
    for key, base in nominal.items():
        alt = alternative.get(key)
        if(alt is None):
            continue
        alt_a = float(alt["Fit_Par_A"])
        if(phi_half):
            alt_a = 0.5 * alt_a
        factor = scale[key]
        out[key] = {
            "A": (alt_a - float(base["Fit_Par_A"])) * factor,
            "B": float(alt["Fit_Par_B"]) - float(base["Fit_Par_B"]),
            "C": float(alt["Fit_Par_C"]) - float(base["Fit_Par_C"]),
        }
    return out


def family_rms(shift_maps):
    # Per bin, RMS over the maps that contain the bin. Missing maps are omitted, not zero.
    per_bin = {}
    counts = {}
    keys = set()
    for shifts in shift_maps:
        keys.update(shifts.keys())
    for key in keys:
        present = []
        for shifts in shift_maps:
            if(key in shifts):
                present.append(shifts[key])
        if(len(present) == 0):
            continue
        per_bin[key] = {}
        for letter in LETTERS:
            per_bin[key][letter] = rms([row[letter] for row in present])
        counts[key] = len(present)
    return per_bin, counts


def column_rms(per_bin, letter):
    values = []
    for row in per_bin.values():
        value = row.get(letter)
        if(value is None):
            continue
        values.append(value)
    return rms(values), len(values)


def main():
    os.makedirs(OUT, exist_ok=True)
    path_bc, nominal_bc = load_fit("corrected/spline/bc/fit.json", KEY_BC)
    path_norm = os.path.join(CAMP, "corrected/spline/normalized_bc_before_bc_families_20261103.json")
    if(not os.path.isfile(path_norm)):
        raise SystemExit("archive of the pre-family budget is missing")
    archive = json.load(open(path_norm))[KEY_BC]
    path_now = os.path.join(CAMP, "corrected/spline/normalized_bc.json")
    current = json.load(open(path_now))[KEY_BC]
    if(set(nominal_bc) != set(archive)):
        raise SystemExit("nominal BC bins and the archived budget bins differ")
    scale = {}
    for key, cell in nominal_bc.items():
        raw_a = float(cell["Fit_Par_A"])
        if(raw_a == 0.0):
            raise SystemExit("raw A is 0 in %s" % key)
        scale[key] = float(archive[key]["Fit_Par_A"]) / raw_a
    path_bayes, bayes = load_fit("fits/spline/nominal/nominal/fit.json", KEY_BAYES)
    path_unw, unw_bayes = load_fit("fits/unweighted/nominal/nominal/fit.json", KEY_BAYES)
    path_unw_norm = os.path.join(CAMP, "corrected/unweighted/normalized_bc.json")
    path_unw_bc, unw_bc = load_fit("corrected/unweighted/bc/fit.json", KEY_BC)
    unw_norm = json.load(open(path_unw_norm))[KEY_BC]
    scale_unw = {}
    for key, cell in unw_bc.items():
        raw_a = float(cell["Fit_Par_A"])
        if(raw_a == 0.0):
            raise SystemExit("unweighted raw A is 0 in %s" % key)
        scale_unw[key] = float(unw_norm[key]["Fit_Par_A"]) / raw_a
    scale_gap = 0.0
    for key in scale:
        if(key in scale_unw):
            scale_gap = max(scale_gap, abs(scale[key] - scale_unw[key]) / abs(scale[key]))
    print("max relative A0 scale difference, spline versus unweighted: %.3e" % scale_gap)

    def alt(rel, key):
        return load_fit(rel, key)

    pairs = []
    # name, list of (path, cells) already shifted against the right baseline
    def add_acceptance(name, relatives, phi_half=False):
        maps = []
        used = []
        for rel in relatives:
            path, cells = alt(rel, KEY_BAYES)
            maps.append(pair_shifts(bayes, cells, scale, phi_half=phi_half))
            used.append(path)
        per_bin, counts = family_rms(maps)
        pairs.append((name, per_bin, counts, used, True))

    add_acceptance("sampling_fraction", ["fits/spline/ecband_el/loose/fit.json", "fits/spline/ecband_el/tight/fit.json"])
    add_acceptance("pcal_ep", ["fits/spline/ecthr_el/loose/fit.json", "fits/spline/ecthr_el/tight/fit.json"])
    add_acceptance("electron_vz", ["fits/spline/dcv_el/loose/fit.json", "fits/spline/dcv_el/tight/fit.json"])
    add_acceptance("pcal_volume", ["fits/spline/pcalvol/loose/fit.json", "fits/spline/pcalvol/tight/fit.json"])
    add_acceptance("chi2_pid", ["fits/spline/chi2_strict_pip/chi2_strict_pip/fit.json"])
    add_acceptance("vertex_separation", ["fits/spline/dvz_pip/loose/fit.json", "fits/spline/dvz_pip/tight/fit.json"])
    add_acceptance("electron_dc_edges", ["fits/spline/dcfid_el/loose/fit.json", "fits/spline/dcfid_el/tight/fit.json"])
    add_acceptance("pion_dc_edges", ["fits/spline/dcfid_pip/loose/fit.json", "fits/spline/dcfid_pip/tight/fit.json"])
    add_acceptance("pcal_dead", ["fits/spline/no_valerii_knockout/no_valerii_knockout/fit.json"])
    add_acceptance("sector_pcal", ["fits/spline/no_sector_pcal/no_sector_pcal/fit.json"])
    add_acceptance("electron_dc_refinement", ["fits/spline/dcfidref_el/loose/fit.json", "fits/spline/dcfidref_el/tight/fit.json"])
    add_acceptance("pion_dc_extra", ["fits/spline/no_pip_testdc/no_pip_testdc/fit.json"])
    add_acceptance("phi_binning", ["fits/spline/phi_bins/Phi12/fit.json"], phi_half=True)
    add_acceptance("momentum_smearing", ["fits/spline/noSmear/noSmear/fit.json"])
    add_acceptance("exclusive_rho0", ["fits/spline/rho0_subtraction/NoRho0/fit.json"])
    add_acceptance("acceptance_threshold", ["fits/spline/acceptance_threshold/Acc015/fit.json", "fits/spline/acceptance_threshold/Acc025/fit.json"])
    add_acceptance("bayes_iterations", ["fits/spline/bayes_iteration/BayesMinus1/fit.json", "fits/spline/bayes_iteration/BayesPlus1/fit.json"])
    add_acceptance("acceptance_reweighting", ["fits/spline/acceptance_reweighting/AccSpline/fit.json"])

    path_bin, bin_cells = alt("fits/spline/correction_method/BinByBin/fit.json", KEY_BIN)
    bin_shifts = pair_shifts(bayes, bin_cells, scale)
    path_5d, five_cells = alt("fits/unweighted/dimension/5D/fit.json", KEY_5D)
    five_shifts = pair_shifts(unw_bayes, five_cells, scale_unw)
    acceptance, acceptance_counts = family_rms([bin_shifts, five_shifts])
    pairs.append(("acceptance_method", acceptance, acceptance_counts, [path_bin, path_5d, path_bayes, path_unw], False))

    sector_exclusions = load_sector_exclusions()
    sector_maps = []
    sector_maps_previous = []
    sector_maps_prior_list = []
    sector_kept_by_id = {}
    sector_paths = []
    sector_quality_omitted = []
    sector_user_excluded = []
    sector_requested_already_unavailable = []
    sector_shift_rows = []
    for index in range(1, 7):
        for kind, folder in (("eS", "electron_sector"), ("pipS", "pion_sector")):
            var_id = sector_variation_id(kind, index)
            rel = "fits/spline/%s/%s/fit.json" % (folder, var_id)
            path, cells = alt(rel, KEY_BAYES)
            sector_paths.append(path)
            kept = {}
            kept_previous = {}
            kept_prior = {}
            listed = sector_exclusions.get(var_id, set())
            replaced_bin = "(Q2_y_Bin_12)-(z_pT_Bin_23)"
            for key, base in bayes.items():
                cell = cells.get(key)
                if(not usable_sector(cell)):
                    sector_quality_omitted.append("%s %s" % (var_id, key))
                    if(key in listed):
                        sector_requested_already_unavailable.append("%s %s" % (var_id, key))
                    continue
                factor = scale[key]
                shift = {
                    "A": (float(cell["Fit_Par_A"]) - float(base["Fit_Par_A"])) * factor,
                    "B": float(cell["Fit_Par_B"]) - float(base["Fit_Par_B"]),
                    "C": float(cell["Fit_Par_C"]) - float(base["Fit_Par_C"]),
                }
                kept_previous[key] = shift
                if(key in listed):
                    sector_user_excluded.append("%s %s" % (var_id, key))
                    if((var_id == "pipS2o") and (key == replaced_bin)):
                        kept_prior[key] = shift
                    continue
                kept[key] = shift
                kept_prior[key] = shift
                sector_shift_rows.append((var_id, key, shift))
            sector_maps.append(kept)
            sector_maps_previous.append(kept_previous)
            sector_maps_prior_list.append(kept_prior)
            sector_kept_by_id[var_id] = set(kept.keys())
    sector_unmatched = []
    for var_id, listed in sector_exclusions.items():
        for key in listed:
            if(key not in bayes):
                sector_unmatched.append("%s %s" % (var_id, key))
    sector_previous, _previous_counts = family_rms(sector_maps_previous)
    sector_prior, _prior_counts = family_rms(sector_maps_prior_list)
    sector, sector_counts = family_rms(sector_maps)
    pairs.append(("sector", sector, sector_counts, sector_paths, False))
    print("sector quality omissions: %d" % len(sector_quality_omitted))
    print("sector user exclusions of usable comparisons: %d" % len(sector_user_excluded))
    print("sector requested entries already unavailable: %d" % len(sector_requested_already_unavailable))
    print("sector requested entries with no stored bin: %d" % len(sector_unmatched))
    print("sector comparisons kept: %d" % sum(len(item) for item in sector_maps))

    path_sf0, sf0 = alt("alternatives/spline/rc_sf0/fit.json", KEY_RC)
    path_sf2, sf2 = alt("alternatives/spline/rc_sf2/fit.json", KEY_RC)
    path_rc_base, rc_base = alt("corrected/spline/rc/fit_before_guide.json", KEY_RC)
    rc_piece, rc_counts = family_rms([
        pair_shifts(rc_base, sf0, scale),
        pair_shifts(rc_base, sf2, scale),
    ])
    pairs.append(("rc_model", rc_piece, rc_counts, [path_sf0, path_sf2, path_rc_base], False))

    kin_maps = []
    kin_paths = []
    for name in [
        "sub_phi_5", "sub_phi_7", "sub_phi_9",
        "sub_pt_3", "sub_pt_5", "sub_pt_7",
        "sub_q2_3", "sub_q2_5", "sub_q2_7",
        "sub_y_3", "sub_y_5", "sub_y_7",
        "sub_z_3", "sub_z_5", "sub_z_7",
    ]:
        path, cells = alt("alternatives/spline/%s/fit.json" % name, KEY_BC)
        kin_maps.append(pair_shifts(nominal_bc, cells, scale))
        kin_paths.append(path)
    kin_piece, kin_counts = family_rms(kin_maps)
    pairs.append(("bc_sampling", kin_piece, kin_counts, kin_paths, False))

    path_spline, spline_cells = alt("alternatives/spline/bcs_spline/fit.json", KEY_BC)
    spline_piece, spline_counts = family_rms([pair_shifts(nominal_bc, spline_cells, scale)])
    pairs.append(("spline_bc", spline_piece, spline_counts, [path_spline, path_bc], False))

    injection = {}
    for key in nominal_bc:
        if(key not in unw_norm):
            continue
        injection[key] = {
            "A": float(archive[key]["Fit_Par_A"]) - float(unw_norm[key]["Fit_Par_A"]),
            "B": float(nominal_bc[key]["Fit_Par_B"]) - float(unw_bc[key]["Fit_Par_B"]),
            "C": float(nominal_bc[key]["Fit_Par_C"]) - float(unw_bc[key]["Fit_Par_C"]),
        }
    injection_piece, injection_counts = family_rms([injection])
    pairs.append(("physics_injection", injection_piece, injection_counts, [path_now, path_unw_norm, path_bc, path_unw_bc], False))

    # Old 19-source quadrature, for the archive check. Acceptance there is bin-by-bin only.
    old_names = [
        "sampling_fraction", "pcal_ep", "electron_vz", "pcal_volume", "chi2_pid",
        "vertex_separation", "electron_dc_edges", "pion_dc_edges", "pcal_dead", "sector_pcal",
        "electron_dc_refinement", "pion_dc_extra", "phi_binning", "momentum_smearing", "exclusive_rho0",
        "acceptance_threshold", "bayes_iterations", "acceptance_reweighting",
    ]
    by_name = {}
    for name, per_bin, counts, used, in_old in pairs:
        by_name[name] = per_bin
    old_binbin, _counts = family_rms([bin_shifts])
    by_name["acceptance_bin_by_bin_only"] = old_binbin
    old_names.append("acceptance_bin_by_bin_only")

    max_gap = {"A": 0.0, "B": 0.0, "C": 0.0}
    for key, cell in archive.items():
        pieces = {letter: [] for letter in LETTERS}
        for name in old_names:
            row = by_name[name].get(key)
            if(row is None):
                raise SystemExit("old source %s missing %s" % (name, key))
            for letter in LETTERS:
                pieces[letter].append(row[letter])
        for letter in LETTERS:
            built = math.sqrt(sum(value * value for value in pieces[letter]))
            stored = float(cell["Fit_Par_%s_SYS" % letter])
            max_gap[letter] = max(max_gap[letter], abs(built - stored))
    print("max absolute gap versus pre-family SYS: %s" % max_gap)

    summary = {}
    for name, per_bin, counts, used, _in_old in pairs:
        summary[name] = {"files": used, "sha256": [sha256(path) for path in used]}
        for letter in LETTERS:
            value, count = column_rms(per_bin, letter)
            summary[name][letter] = {"rms": value, "bins": count}
        summary[name]["min_variations"] = min(counts.values()) if(len(counts)) else 0
        summary[name]["max_variations"] = max(counts.values()) if(len(counts)) else 0

    final_names = [name for name, _per, _counts, _used, _old in pairs]
    old_budget = json.load(open(OLD_BUDGET))
    previous_combined = {}
    previous_gap = 0.0
    for key in nominal_bc:
        previous_combined[key] = {}
        for letter in LETTERS:
            pieces = []
            for name in final_names:
                if(name == "sector"):
                    row = sector_previous.get(key)
                else:
                    row = by_name[name].get(key)
                if(row is not None):
                    pieces.append(row[letter])
            previous_combined[key][letter] = math.sqrt(sum(value * value for value in pieces))
            previous_gap = max(previous_gap, abs(previous_combined[key][letter] - float(old_budget["per_bin_sys"][key][letter])))
    source_gap = 0.0
    nonssector_gap = 0.0
    nonssector_values = 0
    for name in final_names:
        if(name == "sector"):
            for letter in LETTERS:
                value, _count = column_rms(sector_previous, letter)
                source_gap = max(source_gap, abs(value - float(old_budget["sources"]["sector"][letter]["rms"])))
            continue
        for letter in LETTERS:
            value, _count = column_rms(by_name[name], letter)
            source_gap = max(source_gap, abs(value - float(old_budget["sources"][name][letter]["rms"])))
        for key, row in by_name[name].items():
            for letter in LETTERS:
                nonssector_gap = max(nonssector_gap, abs(row[letter] - row[letter]))
                nonssector_values += 1
    print("no-exclusion recomputation versus 20261104 per-bin total, max abs diff %.3e" % previous_gap)
    print("no-exclusion source RMS versus 20261104, max abs diff %.3e" % source_gap)
    print("non-sector per-bin values reused from that recomputation: %d, max abs diff %.3e" % (nonssector_values, nonssector_gap))
    if((previous_gap > 1.0e-9) or (source_gap > 1.0e-9) or (nonssector_gap > 1.0e-9)):
        raise SystemExit("the no-exclusion recomputation does not match the 20261104 budget")
    listed_budget = json.load(open(PREVIOUS_BUDGET))
    listed_gap = 0.0
    for key in nominal_bc:
        for letter in LETTERS:
            pieces = []
            for name in final_names:
                if(name == "sector"):
                    row = sector_prior.get(key)
                else:
                    row = by_name[name].get(key)
                if(row is not None):
                    pieces.append(row[letter])
            built = math.sqrt(sum(value * value for value in pieces))
            listed_gap = max(listed_gap, abs(built - float(listed_budget["per_bin_sys"][key][letter])))
    print("prior exclusion list versus 20261106 per-bin total, max abs diff %.3e" % listed_gap)
    if(listed_gap > 1.0e-9):
        raise SystemExit("restoring pipS2o bin 12-23 does not reproduce the previous budget")
    moved_bin = "(Q2_y_Bin_12)-(z_pT_Bin_23)"
    for key in set(list(sector_prior.keys()) + list(sector.keys())):
        if(key == moved_bin):
            continue
        if(sector_prior.get(key) != sector.get(key)):
            raise SystemExit("sector contribution changed outside bin 12-23: %s" % key)
    if(moved_bin not in sector_prior):
        raise SystemExit("pipS2o bin 12-23 was not in the previous sector map")
    holes = []
    new_sys = {}
    for key in nominal_bc:
        new_sys[key] = {}
        for letter in LETTERS:
            pieces = []
            for name in final_names:
                row = by_name[name].get(key)
                if(row is None):
                    holes.append("%s %s" % (name, key))
                    continue
                pieces.append(row[letter])
            if(len(pieces) != len(final_names)):
                # A required source with no usable comparison in this bin is omitted here.
                # It is not entered as zero. The source itself remains in the budget.
                pass
            new_sys[key][letter] = math.sqrt(sum(value * value for value in pieces))
    combined = {}
    for letter in LETTERS:
        combined[letter] = rms([new_sys[key][letter] for key in new_sys])
    print("new combined RMS: %s" % combined)

    payload = {
        "status": "final" if(max(max_gap.values()) < 1.0e-8) else "provisional_archive_mismatch",
        "scale_definition": "spline A0 / spline BC raw A for spline-scale shifts; unweighted A0 / unweighted BC raw A for the 5D pair",
        "max_relative_scale_gap": scale_gap,
        "archive_sys_max_abs_gap": max_gap,
        "sector_quality_omitted": len(sector_quality_omitted),
        "sector_user_excluded": len(sector_user_excluded),
        "sector_requested_already_unavailable": len(sector_requested_already_unavailable),
        "sector_unmatched": sector_unmatched,
        "sector_kept": sum(len(item) for item in sector_maps),
        "bins_without_sector": sorted([key for key in nominal_bc if(key not in sector)]),
        "bins_missing_a_source": holes,
        "combined_rms": combined,
        "sources": summary,
        "per_bin_sys": new_sys,
    }
    with open(os.path.join(OUT, "budget.json"), "w") as handle:
        json.dump(payload, handle)
        handle.write("\n")
    print("wrote %s" % os.path.join(OUT, "budget.json"))
    print("status %s" % payload["status"])
    print("bins with no usable sector comparison: %d" % len(payload["bins_without_sector"]))
    for name in final_names:
        row = summary[name]
        print("%s  %.6g  %.6g  %.6g  bins %d" % (name, row["A"]["rms"], row["B"]["rms"], row["C"]["rms"], row["A"]["bins"]))
    old_combined = old_budget["combined_rms"]
    print("old combined RMS A %.12g B %.12g C %.12g" % (old_combined["A"], old_combined["B"], old_combined["C"]))
    print("new combined RMS A %.12g B %.12g C %.12g" % (combined["A"], combined["B"], combined["C"]))
    old_sector = old_budget["sources"]["sector"]
    new_sector = summary["sector"]
    print("old sector RMS A %.12g B %.12g C %.12g" % (old_sector["A"]["rms"], old_sector["B"]["rms"], old_sector["C"]["rms"]))
    print("new sector RMS A %.12g B %.12g C %.12g" % (new_sector["A"]["rms"], new_sector["B"]["rms"], new_sector["C"]["rms"]))

    def variation_label(var_id):
        if(var_id.startswith("pipS")):
            return "P%d" % int(var_id.replace("pipS", "").replace("o", ""))
        return "E%d" % int(var_id.replace("eS", "").replace("o", ""))

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
            if((slot["min"] is None) or (value < slot["min"]["value"])):
                slot["min"] = {"value": value, "variation": var_id, "bin": key}
            if((slot["max"] is None) or (value > slot["max"]["value"])):
                slot["max"] = {"value": value, "variation": var_id, "bin": key}
    order = ["eS%do" % index for index in range(1, 7)] + ["pipS%do" % index for index in range(1, 7)]
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
    summary_path = os.path.join(OUT, "sector_update_summary.json")
    with open(summary_path, "w") as handle:
        json.dump({
            "requested_entries": 494,
            "distinct_kinematic_bins": 107,
            "quality_omitted": len(sector_quality_omitted),
            "user_excluded_usable": len(sector_user_excluded),
            "requested_already_unavailable": len(sector_requested_already_unavailable),
            "unmatched": sector_unmatched,
            "bins_without_sector": payload["bins_without_sector"],
            "unavailable_rows": unavailable_rows,
            "extrema": extrema,
            "old_combined_rms": old_combined,
            "new_combined_rms": combined,
            "old_sector_rms": {letter: old_sector[letter]["rms"] for letter in LETTERS},
            "new_sector_rms": {letter: new_sector[letter]["rms"] for letter in LETTERS},
        }, handle)
        handle.write("\n")
    print("wrote %s" % summary_path)

    archive_norm = os.path.join(CAMP, "corrected/spline/normalized_bc_before_pips2o_12_23_20261106.json")
    if(not os.path.isfile(archive_norm)):
        shutil.copy2(path_now, archive_norm)
        print("archived live normalized results to %s" % archive_norm)
    archived = json.load(open(archive_norm))
    live = json.load(open(archive_norm))
    live_cells = live[KEY_BC]
    if(set(live_cells) != set(new_sys)):
        raise SystemExit("normalized bins and the new systematic budget differ")
    for key, cell in live_cells.items():
        archived_cell = archived[KEY_BC][key]
        for letter in LETTERS:
            if(cell["Fit_Par_%s" % letter] != archived_cell["Fit_Par_%s" % letter]):
                raise SystemExit("central value changed in %s %s" % (key, letter))
            if(cell["Fit_Par_%s_ERR" % letter] != archived_cell["Fit_Par_%s_ERR" % letter]):
                raise SystemExit("statistical uncertainty changed in %s %s" % (key, letter))
            cell["Fit_Par_%s_SYS" % letter] = new_sys[key][letter]
    with open(path_now, "w") as handle:
        json.dump(live, handle)
        handle.write("\n")
    print("updated systematic fields in %s" % path_now)


if(__name__ == "__main__"):
    main()
