# Nominal spline refinement inventory, 2026-11-08

## Thesis products

The plotted measurement is the spline-weighted 3D result after acceptance unfolding, the event-yield radiative correction, and event bin centering. An acceptance-only or RC-only file is not a substitute for it. The authoritative normalized moments remain `physics_campaign/corrected/spline/normalized_bc.json`. This run did not rewrite that file, `budgets.json`, the dated budget copies, or `budgets/sector_fit_exclusions_20261106.json`.

The three families were refined on copies. The files under `fits/`, `corrected/`, and `alternatives/` were not modified. Shared `Phi_h_Fit_Parameters_Initialize.py` and `Prepare_Next_Iteration/Phi_h_Fit_Parameters_from_Spline.py` were not edited. Each family used one run-local guide passed with `--fit_init_file` and did not also pass `--use_spline_init`.

| Product | Role | Current directory | This run |
|---|---|---|---|
| Acceptance Bayesian | unfolded acceptance | `fits/spline/nominal/nominal` | refined copy in `refinement_20261108/spline/nominal/acceptance` |
| Event-yield RC | RC-model baseline | `corrected/spline/rc` | refined copy in `refinement_20261108/spline/nominal/rc`. `fit_before_guide.json` kept as history. The baseline was not switched to a later guided file. |
| BC+RC Bayesian | plotted measurement | `corrected/spline/bc` | refined copy in `refinement_20261108/spline/nominal/bc` |
| Normalized moments | thesis A0 table | `corrected/spline/normalized_bc.json` | not refit |
| Budgets and sector exclusions | systematic tables | `budgets.json`, `budgets/` | not edited |
| Alternatives | not in the nominal quadrature | `alternatives/spline` and `alternatives/unweighted` | not refit |

## Current fit directories

Count of existing `refinement_note.json` files under `fits` and `corrected`, excluding this run: 89 (85 under `fits`, 4 under `corrected`). The 2026-11-08 audit classified each as verified because the stated after-quality matches the stored fit. That classification was not repeated here and is not a skip list.

Directories with `fit.json` and no refinement note are initial fits. The iterative procedure has not been run there. That includes both spline and unweighted alternatives, and the parent `corrected/spline` and `corrected/unweighted` files whose stage notes live in `rc/` and `bc/`.

- `alternatives/spline/bcs_aep`: initial fit only (fit.json, no refinement note, iterative procedure not done)
- `alternatives/spline/bcs_spline`: initial fit only (fit.json, no refinement note, iterative procedure not done)
- `alternatives/spline/rc_sf0`: initial fit only (fit.json, no refinement note, iterative procedure not done)
- `alternatives/spline/rc_sf2`: initial fit only (fit.json, no refinement note, iterative procedure not done)
- `alternatives/spline/sub_phi_5`: initial fit only (fit.json, no refinement note, iterative procedure not done)
- `alternatives/spline/sub_phi_7`: initial fit only (fit.json, no refinement note, iterative procedure not done)
- `alternatives/spline/sub_phi_9`: initial fit only (fit.json, no refinement note, iterative procedure not done)
- `alternatives/spline/sub_pt_3`: initial fit only (fit.json, no refinement note, iterative procedure not done)
- `alternatives/spline/sub_pt_5`: initial fit only (fit.json, no refinement note, iterative procedure not done)
- `alternatives/spline/sub_pt_7`: initial fit only (fit.json, no refinement note, iterative procedure not done)
- `alternatives/spline/sub_q2_3`: initial fit only (fit.json, no refinement note, iterative procedure not done)
- `alternatives/spline/sub_q2_5`: initial fit only (fit.json, no refinement note, iterative procedure not done)
- `alternatives/spline/sub_q2_7`: initial fit only (fit.json, no refinement note, iterative procedure not done)
- `alternatives/spline/sub_y_3`: initial fit only (fit.json, no refinement note, iterative procedure not done)
- `alternatives/spline/sub_y_5`: initial fit only (fit.json, no refinement note, iterative procedure not done)
- `alternatives/spline/sub_y_7`: initial fit only (fit.json, no refinement note, iterative procedure not done)
- `alternatives/spline/sub_z_3`: initial fit only (fit.json, no refinement note, iterative procedure not done)
- `alternatives/spline/sub_z_5`: initial fit only (fit.json, no refinement note, iterative procedure not done)
- `alternatives/spline/sub_z_7`: initial fit only (fit.json, no refinement note, iterative procedure not done)
- `alternatives/unweighted/bcs_spline`: initial fit only (fit.json, no refinement note, iterative procedure not done)
- `alternatives/unweighted/rc_sf0`: initial fit only (fit.json, no refinement note, iterative procedure not done)
- `alternatives/unweighted/rc_sf2`: initial fit only (fit.json, no refinement note, iterative procedure not done)
- `alternatives/unweighted/sub_phi_5`: initial fit only (fit.json, no refinement note, iterative procedure not done)
- `alternatives/unweighted/sub_phi_7`: initial fit only (fit.json, no refinement note, iterative procedure not done)
- `alternatives/unweighted/sub_phi_9`: initial fit only (fit.json, no refinement note, iterative procedure not done)
- `alternatives/unweighted/sub_pt_3`: initial fit only (fit.json, no refinement note, iterative procedure not done)
- `alternatives/unweighted/sub_pt_5`: initial fit only (fit.json, no refinement note, iterative procedure not done)
- `alternatives/unweighted/sub_pt_7`: initial fit only (fit.json, no refinement note, iterative procedure not done)
- `alternatives/unweighted/sub_q2_3`: initial fit only (fit.json, no refinement note, iterative procedure not done)
- `alternatives/unweighted/sub_q2_5`: initial fit only (fit.json, no refinement note, iterative procedure not done)
- `alternatives/unweighted/sub_q2_7`: initial fit only (fit.json, no refinement note, iterative procedure not done)
- `alternatives/unweighted/sub_y_3`: initial fit only (fit.json, no refinement note, iterative procedure not done)
- `alternatives/unweighted/sub_y_5`: initial fit only (fit.json, no refinement note, iterative procedure not done)
- `alternatives/unweighted/sub_y_7`: initial fit only (fit.json, no refinement note, iterative procedure not done)
- `alternatives/unweighted/sub_z_3`: initial fit only (fit.json, no refinement note, iterative procedure not done)
- `alternatives/unweighted/sub_z_5`: initial fit only (fit.json, no refinement note, iterative procedure not done)
- `alternatives/unweighted/sub_z_7`: initial fit only (fit.json, no refinement note, iterative procedure not done)
- `corrected/spline`: initial fit only (fit.json, no refinement note, iterative procedure not done)
- `corrected/spline/bc`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `corrected/spline/rc`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `corrected/unweighted`: initial fit only (fit.json, no refinement note, iterative procedure not done)
- `corrected/unweighted/bc`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `corrected/unweighted/rc`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/spline/acceptance_reweighting/AccSpline`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/spline/acceptance_threshold/Acc015`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/spline/acceptance_threshold/Acc025`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/spline/bayes_iteration/BayesMinus1`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/spline/bayes_iteration/BayesPlus1`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/spline/chi2_strict_pip/chi2_strict_pip`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/spline/correction_method/BinByBin`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/spline/dcfid_el/loose`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/spline/dcfid_el/tight`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/spline/dcfid_pip/loose`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/spline/dcfid_pip/tight`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/spline/dcfidref_el/loose`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/spline/dcfidref_el/tight`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/spline/dcv_el/loose`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/spline/dcv_el/tight`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/spline/dvz_pip/loose`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/spline/dvz_pip/tight`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/spline/ecband_el/loose`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/spline/ecband_el/tight`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/spline/ecthr_el/loose`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/spline/ecthr_el/tight`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/spline/electron_sector/eS1o`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/spline/electron_sector/eS2o`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/spline/electron_sector/eS3o`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/spline/electron_sector/eS4o`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/spline/electron_sector/eS5o`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/spline/electron_sector/eS6o`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/spline/noSmear/noSmear`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/spline/no_pip_testdc/no_pip_testdc`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/spline/no_sector_pcal/no_sector_pcal`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/spline/no_valerii_knockout/no_valerii_knockout`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/spline/nominal/nominal`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/spline/pcalvol/loose`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/spline/pcalvol/tight`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/spline/phi_bins/Phi12`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/spline/pion_sector/pipS1o`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/spline/pion_sector/pipS2o`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/spline/pion_sector/pipS3o`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/spline/pion_sector/pipS4o`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/spline/pion_sector/pipS5o`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/spline/pion_sector/pipS6o`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/spline/rho0_subtraction/NoRho0`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/unweighted/acceptance_reweighting/Acc`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/unweighted/acceptance_threshold/Acc015`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/unweighted/acceptance_threshold/Acc025`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/unweighted/bayes_iteration/BayesMinus1`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/unweighted/bayes_iteration/BayesPlus1`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/unweighted/chi2_strict_pip/chi2_strict_pip`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/unweighted/correction_method/BinByBin`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/unweighted/dcfid_el/loose`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/unweighted/dcfid_el/tight`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/unweighted/dcfid_pip/loose`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/unweighted/dcfid_pip/tight`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/unweighted/dcfidref_el/loose`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/unweighted/dcfidref_el/tight`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/unweighted/dcv_el/loose`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/unweighted/dcv_el/tight`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/unweighted/dimension/5D`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/unweighted/dvz_pip/loose`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/unweighted/dvz_pip/tight`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/unweighted/ecband_el/loose`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/unweighted/ecband_el/tight`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/unweighted/ecthr_el/loose`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/unweighted/ecthr_el/tight`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/unweighted/electron_sector/eS1o`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/unweighted/electron_sector/eS2o`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/unweighted/electron_sector/eS3o`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/unweighted/electron_sector/eS4o`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/unweighted/electron_sector/eS5o`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/unweighted/electron_sector/eS6o`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/unweighted/noSmear/noSmear`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/unweighted/no_pip_testdc/no_pip_testdc`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/unweighted/no_sector_pcal/no_sector_pcal`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/unweighted/no_valerii_knockout/no_valerii_knockout`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/unweighted/nominal/nominal`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/unweighted/pcalvol/loose`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/unweighted/pcalvol/tight`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/unweighted/phi_bins/Phi12`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/unweighted/pion_sector/pipS1o`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/unweighted/pion_sector/pipS2o`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/unweighted/pion_sector/pipS3o`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/unweighted/pion_sector/pipS4o`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/unweighted/pion_sector/pipS5o`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/unweighted/pion_sector/pipS6o`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)
- `fits/unweighted/rho0_subtraction/NoRho0`: verified refinement note (2026-11-08 audit: stated after-quality matches the stored fit; not re-audited and not a skip list)

This run wrote new notes, not resumes. The destination did not already contain `refinement_note.json` and `fit.json` for these three families.

- `refinement_20261108/spline/nominal/acceptance`: iterative refinement, 452 Bayesian bins, 0 range mismatches
- `refinement_20261108/spline/nominal/rc`: iterative refinement, 452 RC_Bayesian bins, 0 range mismatches
- `refinement_20261108/spline/nominal/bc`: iterative refinement, 452 BC_RC_Bayesian bins, 0 range mismatches

## Fit-range check

The fit uses ROOT option R, so only the TF1 range enters the chi-squared. The remake sets that range from the first nonempty bin edge through the last nonempty bin edge. Empty bins between those edges stay inside the range. Empty bins outside it must not enter. A stored TF1 whose range is already the filled window is not a defect. A drawing that extends a curve past the fit is not a reason to widen the fit to 0-360, and a fit is not changed only to match a drawing.

The three nominal files refit here were checked after the corrected full-histogram search. All 452 acceptance, 452 RC, and 452 BC histograms match the filled window. There are no nominal range mismatches. For `(Q2_y_Bin_1)-(z_pT_Bin_8)` the filled window and the TF1 are both 60 to 300 degrees, with 16 bins inside the range and NDF 13.

The stored spline sector Bayesian fits were not refit. All 286 range mismatches are in the twelve electron and pion sector files, out of 5049 checked histograms: eS1o 25 of 418, eS2o 24 of 420, eS3o 19 of 422, eS4o 21 of 421, eS5o 26 of 421, eS6o 25 of 421, pipS1o 19 of 421, pipS2o 27 of 421, pipS3o 27 of 421, pipS4o 28 of 420, pipS5o 23 of 420, and pipS6o 22 of 423. Example: spline eS6o `(Q2_y_Bin_1)-(z_pT_Bin_1)` is filled from 75 to 180 degrees, while the stored TF1 runs from 75 to 360. Seven bins in that TF1 range have a positive error and twelve have zero error, so the empty extension did not enter the chi-squared. The curve is long because the stored range is long. NDF 4 is the positive-error count minus three.

Unweighted sector files have the same pattern and were not refit. The check found 294 mismatches out of 5088 Bayesian histograms: eS1o 23 of 422, eS2o 28 of 424, eS3o 18 of 426, eS4o 22 of 424, eS5o 30 of 424, eS6o 27 of 424, pipS1o 16 of 425, pipS2o 28 of 423, pipS3o 30 of 425, pipS4o 25 of 421, pipS5o 25 of 425, and pipS6o 22 of 425.

