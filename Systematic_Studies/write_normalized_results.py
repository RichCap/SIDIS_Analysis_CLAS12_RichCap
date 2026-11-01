#!/usr/bin/env python3
# Attach provisional systematics and normalize A0 once for each campaign.

import json
import os
import sys

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, THIS_DIR)
import sidis_physics_lib as phys
from Cross_Section_Normalization import Cross_Section_Normalization


class NormArgs:
    verbose = False
    pT2 = True
    no_apply_beam_corrections = False


def main():
    budgets = json.load(open(os.path.join(THIS_DIR, "physics_campaign", "budgets.json")))
    for campaign in ["unweighted", "spline"]:
        fit_path = os.path.join(THIS_DIR, "physics_campaign", "corrected", campaign, "fit.json")
        payload = json.load(open(fit_path))
        cells = payload["Fit_Pars_from_3D_BC_RC_Bayesian"]
        totals = budgets["budgets"][campaign]["totals"]
        prepared = {}
        scales = {}
        for bin_name, cell in cells.items():
            q2y = int(bin_name.split("Q2_y_Bin_")[1].split(")")[0])
            zpt = int(bin_name.split("z_pT_Bin_")[1].split(")")[0])
            _, area, lumi, flux = Cross_Section_Normalization(Histo=None, Q2_y_Bin=q2y, z_pT_Bin=zpt, args_in=NormArgs())
            scales[bin_name] = float(area) * float(lumi) * float(flux)
            updated = dict(cell)
            total = totals.get(bin_name, {})
            for parameter, field in phys.FIT_FIELDS.items():
                piece = total.get(parameter, {})
                sys_value = piece.get("up")
                if(sys_value is None):
                    raise SystemExit("missing systematic for %s %s" % (campaign, bin_name))
                updated[field + "_SYS"] = float(sys_value)
            prepared[bin_name] = updated
        stat_copy = phys.normalize_campaign_copy(prepared, "statistical", scales)
        sys_copy = phys.normalize_campaign_copy(prepared, "systematic", scales)
        merged = phys.merge_normalized(stat_copy, sys_copy)
        out = {
            "normalization_status": "applied",
            "campaign": campaign,
            "provisional_systematic": True,
            "unassigned_factor_uncertainty": True,
            "Fit_Pars_from_3D_BC_RC_Bayesian": merged["cells"],
        }
        dest = os.path.join(THIS_DIR, "physics_campaign", "corrected", campaign, "normalized.json")
        phys.write_json(dest, out)
        print(campaign, "bins", len(merged["cells"]), dest)


if(__name__ == "__main__"):
    main()
