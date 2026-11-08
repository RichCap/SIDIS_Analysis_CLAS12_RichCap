#!/usr/bin/env python3
# Spline-model and kinematic bin-centering shifts on the spline-weighted measurement.
# A is scaled to A0 with the nominal per-bin factor. B and C are not rescaled.

import json
import math
import os
import shutil

STUDY = os.path.dirname(os.path.abspath(__file__))
CAMP = os.path.join(STUDY, "physics_campaign")
KEY = "Fit_Pars_from_3D_BC_RC_Bayesian"
NOMINAL_FIT = os.path.join(CAMP, "corrected/spline/bc/fit.json")
NOMINAL_NORM = os.path.join(CAMP, "corrected/spline/normalized_bc.json")
ARCHIVE_NORM = os.path.join(CAMP, "corrected/spline/normalized_bc_before_bc_families_20261103.json")
RAWA_FIT = os.path.join(CAMP, "alternatives/spline/bcs_spline/fit.json")
AEP_FIT = os.path.join(CAMP, "alternatives/spline/bcs_aep/fit.json")
REPORT = os.path.join(CAMP, "reports/bin_centering_families_20261103.json")
KIN_NAMES = [
    "sub_phi_5", "sub_phi_7", "sub_phi_9",
    "sub_pt_3", "sub_pt_5", "sub_pt_7",
    "sub_q2_3", "sub_q2_5", "sub_q2_7",
    "sub_y_3", "sub_y_5", "sub_y_7",
    "sub_z_3", "sub_z_5", "sub_z_7",
]
LETTERS = ("A", "B", "C")


def load_cells(path):
    payload = json.load(open(path))
    cells = payload[KEY]
    if(len(cells) != 452):
        raise SystemExit("%s has %d bins" % (path, len(cells)))
    return payload, cells


def rms(values):
    if(len(values) == 0):
        return None
    return math.sqrt(sum(value * value for value in values) / float(len(values)))


def shifts_for(nominal_cells, alt_cells, scales):
    # Per-bin (dA0, dB, dC). A missing alternative bin is omitted, not set to zero.
    out = {}
    for key, nominal in nominal_cells.items():
        alt = alt_cells.get(key)
        if(alt is None):
            continue
        scale = scales[key]
        dA = float(alt["Fit_Par_A"]) * scale - float(nominal["Fit_Par_A"]) * scale
        dB = float(alt["Fit_Par_B"]) - float(nominal["Fit_Par_B"])
        dC = float(alt["Fit_Par_C"]) - float(nominal["Fit_Par_C"])
        out[key] = {"A": dA, "B": dB, "C": dC}
    return out


def family_bin(shift_list):
    # RMS across the alternatives that exist in this bin.
    per_bin = {}
    keys = set()
    for shifts in shift_list:
        keys.update(shifts.keys())
    for key in keys:
        piece = {"A": [], "B": [], "C": []}
        for shifts in shift_list:
            if(key not in shifts):
                continue
            for letter in LETTERS:
                piece[letter].append(shifts[key][letter])
        per_bin[key] = {}
        for letter in LETTERS:
            per_bin[key][letter] = rms(piece[letter])
    return per_bin


def column_rms(per_bin, letter):
    values = []
    for key, row in per_bin.items():
        value = row.get(letter)
        if(value is None):
            continue
        values.append(value)
    return rms(values), len(values)


def main():
    nominal_payload, nominal_cells = load_cells(NOMINAL_FIT)
    norm_payload, norm_cells = load_cells(NOMINAL_NORM)
    if(set(nominal_cells) != set(norm_cells)):
        raise SystemExit("nominal fit and normalized JSON bins differ")
    scales = {}
    for key, cell in nominal_cells.items():
        raw_A = float(cell["Fit_Par_A"])
        if(raw_A == 0.0):
            raise SystemExit("nominal raw A is 0 in %s" % key)
        scales[key] = float(norm_cells[key]["Fit_Par_A"]) / raw_A
    _, rawa_cells = load_cells(RAWA_FIT)
    _, aep_cells = load_cells(AEP_FIT)
    rawa_shifts = shifts_for(nominal_cells, rawa_cells, scales)
    aep_shifts = shifts_for(nominal_cells, aep_cells, scales)
    kin_shifts = []
    for name in KIN_NAMES:
        path = os.path.join(CAMP, "alternatives/spline", name, "fit.json")
        _, cells = load_cells(path)
        kin_shifts.append(shifts_for(nominal_cells, cells, scales))
    spline_bin = family_bin([rawa_shifts, aep_shifts])
    kin_bin = family_bin(kin_shifts)
    if((len(spline_bin) != 452) or (len(kin_bin) != 452)):
        raise SystemExit("family coverage spline %d kinematic %d" % (len(spline_bin), len(kin_bin)))
    report = {
        "nominal_fit": NOMINAL_FIT,
        "normalized": NOMINAL_NORM,
        "A_scale": "nominal A0 / nominal raw A, applied to every alternative amplitude",
        "B_C_scale": "none",
        "spline_models": {
            "initial_rawA": RAWA_FIT,
            "final_Aep": AEP_FIT,
            "combination": "rms of the two shifts in each bin, then rms over bins",
        },
        "kinematic_variations": KIN_NAMES,
        "kinematic_combination": "rms of the 15 shifts in each bin, then rms over bins",
    }
    for label, shifts in (("initial_rawA", rawa_shifts), ("final_Aep", aep_shifts)):
        report[label] = {}
        for letter in LETTERS:
            values = [shifts[key][letter] for key in shifts]
            report[label][letter] = {"rms": rms(values), "n": len(values)}
    report["spline_family"] = {}
    report["kinematic_family"] = {}
    for letter in LETTERS:
        spline_rms, spline_n = column_rms(spline_bin, letter)
        kin_rms, kin_n = column_rms(kin_bin, letter)
        report["spline_family"][letter] = {"rms": spline_rms, "n": spline_n}
        report["kinematic_family"][letter] = {"rms": kin_rms, "n": kin_n}
    if(not os.path.isfile(ARCHIVE_NORM)):
        shutil.copy2(NOMINAL_NORM, ARCHIVE_NORM)
    updated = 0
    for key, cell in norm_cells.items():
        for letter in LETTERS:
            old = float(cell["Fit_Par_%s_SYS" % letter])
            spline_piece = spline_bin[key][letter]
            kin_piece = kin_bin[key][letter]
            if((spline_piece is None) or (kin_piece is None)):
                raise SystemExit("missing family contribution in %s" % key)
            cell["Fit_Par_%s_SYS" % letter] = math.sqrt(old * old + spline_piece * spline_piece + kin_piece * kin_piece)
        updated += 1
    combined = {}
    err_rms = {}
    for letter in LETTERS:
        sys_values = [float(cell["Fit_Par_%s_SYS" % letter]) for cell in norm_cells.values()]
        err_values = [float(cell["Fit_Par_%s_ERR" % letter]) for cell in norm_cells.values()]
        combined[letter] = {"rms": rms(sys_values), "n": len(sys_values)}
        err_rms[letter] = {"rms": rms(err_values), "n": len(err_values)}
    report["combined_with_both_families"] = combined
    report["fit_uncertainty_rms"] = err_rms
    report["updated_bins"] = updated
    report["archive"] = ARCHIVE_NORM
    norm_payload["bin_centering_families"] = {
        "spline_model": "rms of initial rawA and stored Aep alternatives, added once",
        "kinematic": "rms of 15 subdivision alternatives, added once",
        "previous_budget_retained": True,
    }
    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    with open(REPORT, "w") as handle:
        json.dump(report, handle, indent=2)
        handle.write("\n")
    temporary = NOMINAL_NORM + ".partial"
    with open(temporary, "w") as handle:
        json.dump(norm_payload, handle, indent=2)
        handle.write("\n")
    os.replace(temporary, NOMINAL_NORM)
    print(json.dumps({
        "initial_rawA": report["initial_rawA"],
        "final_Aep": report["final_Aep"],
        "spline_family": report["spline_family"],
        "kinematic_family": report["kinematic_family"],
        "combined": combined,
    }, indent=2))


if(__name__ == "__main__"):
    main()
