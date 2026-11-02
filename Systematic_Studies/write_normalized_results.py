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
    # Writes normalized_bc.json. The older normalized.json is left in place.
    output_dir = os.path.join(THIS_DIR, "physics_campaign")
    budget_path = os.path.join(output_dir, "budgets.json")
    budgets = json.load(open(budget_path))
    for campaign in ["unweighted", "spline"]:
        fit_path = os.path.join(output_dir, "corrected", campaign, "bc", "fit.json")
        payload = json.load(open(fit_path))
        cells = payload["Fit_Pars_from_3D_BC_RC_Bayesian"]
        totals = budgets["budgets"][campaign]["totals"]
        scales = {}
        for bin_name in cells.keys():
            q2y = int(bin_name.split("Q2_y_Bin_")[1].split(")")[0])
            zpt = int(bin_name.split("z_pT_Bin_")[1].split(")")[0])
            _, area, lumi, flux = Cross_Section_Normalization(Histo=None, Q2_y_Bin=q2y, z_pT_Bin=zpt, args_in=NormArgs())
            scales[bin_name] = float(area) * float(lumi) * float(flux)
        document = phys.build_normalized_document(cells, totals, scales, campaign, fit_path, budget_path)
        dest = phys.normalized_bc_path(output_dir, campaign)
        if(os.path.isfile(dest)):
            raise SystemExit("refusing to replace %s without a separate execution authorization" % dest)
        phys.write_json(dest, document)
        print(campaign, "bins", len(document["Fit_Pars_from_3D_BC_RC_Bayesian"]), dest)


if(__name__ == "__main__"):
    main()
