# φ_h fit refinement campaign log

Working ROOT (fits updated here): `Hybrid_Unfolded_Parallel_SIDIS_epip_from_3D_and_5D_1st_Order_V2.root`

Unused backup (never `--root`): `Hybrid_Unfolded_Parallel_SIDIS_epip_from_3D_and_5D_1st_Order_V2_pre_refinement.root`

Manual baseline (not overwritten): `Phi_h_Fit_Parameters_Initialize.py`

Universal initializer: `Prepare_Next_Iteration/Phi_h_Fit_Parameters_from_Spline.py`

## Iteration 0

Started from the manual baseline (no `--use_spline_init`).

- 3D remake: 2790 fits, ~15 min, JSON `Fit_Pars_from_3D_{Bayesian,RC_Bayesian,BC_RC_Bayesian}` each 465 bins with Chi2/NDF.
- 5D remake: JSON `Fit_Pars_from_5D_{Bayesian,RC_Bayesian,BC_RC_Bayesian}` 469/465/465 bins.
- Typical redχ² medians: 3D ~1.1–1.5, 5D ~1.2–1.7. 5D tails are longer (p95 ~7–11).
- Failed/unphysical BC+RC fits (A=nan, C=1): (7,5), (8,9), (15,3) in both 3D and 5D. Baseline C was None, so C ran to 1.
- 5D Bayesian has 4 empty A=0 bins (high-z unused).
- Splines built with `--apply_A_corr` into `Phi_h_Fit_Parameters_from_Spline.py` (tagged 3D/5D × default/RC/BC). 5D Bayesian first failed on zero bin-area; guard added. Non-finite A/B/C now skipped in spline training.

## Iteration 1

Targeted BC+RC keys for the six failed bins: C_initial=0, C_limits=[-0.12,0.12], B from the manual baseline. Then remake 3D and 5D with `--use_spline_init`.

Iteration 1 BC spline keys (trained on A=nan / C=1) created additional non-finite A bins. Rolled back: removed all `("q","z","3D"|"5D","BC")` keys except the six hand-tuned bins so other BC histograms fall back to the manual baseline.

## Iteration 2

Remake 3D and 5D with the cleaned universal initializer (`--use_spline_init`).

Dimension-only keys `("q","z","3D")` were still being applied to BC/RC histograms as a fallback, so Bayesian spline inits leaked into BC+RC and kept A=nan. Lookup now uses dimension-only keys only for acceptance-only histograms.

## Iteration 3

Remake 3D and 5D with the corrected lookup.

## Iteration 4

Rebuilt `Phi_h_Fit_Parameters_from_Spline.py` as the manual baseline plus tagged 3D/5D keys only. Final 3D and 5D remakes. See `report.md`.
