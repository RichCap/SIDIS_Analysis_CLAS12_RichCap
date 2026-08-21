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

---

# 5D follow-up campaign

3D results frozen. 5D spline windows (median B width 0.021 vs baseline 0.17) put ~80% of 5D Bayesian/RC B and C on the limit. Restart 5D from `Phi_h_Fit_Parameters_Initialize.py` (no `--use_spline_init`).

## 5D-A — restart remake from manual baseline

No `--use_spline_init`. 3D JSON families unchanged vs pre-campaign snapshot.

| Family | n | nan A | empty | redχ² med | p95 | n>3 | n>5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 5D Bayesian | 469 | 0 | 4 | 1.66 | 7.00 | 80 | 39 |
| 5D RC | 465 | 0 | 4 | 1.65 | 11.01 | 84 | 48 |
| 5D BC+RC | 465 | 11 | 4 | 1.21 | 6.11 | 41 | 28 |

Restart alone is not enough. Worst bins still have much smaller |B| than the successful 3D counterparts, e.g. (9,19) 5D B=-0.044 vs 3D B=-0.208 (red 98.8 vs 0.89). (12,13) 5D B/C ~ -0.51 runaway vs 3D ~ -0.08. Tight 5D spline keys were trapping fits; they were removed.

## 5D-B — wide 3D-initialized 5D keys (no spline range)

Removed remaining tight 5D / 5D-RC spline keys. Added 80 `("q","z","5D")`, 84 `("q","z","5D","RC")`, 41 `("q","z","5D","BC")` keys: B/C initialized from the current 3D result for the same (Q²-y, z-pT) bin, with wide windows B ±0.35 and C ±0.22. 3D keys untouched. Hand BC C-guards kept. Total keys 1739.

Remake 5D only with `--use_spline_init` so the new 5D-tagged keys apply.

| Family | n | nan A | empty | redχ² med | p95 | n>3 | n>5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 5D Bayesian | 469 | 0 | 4 | 1.54 | 3.11 | 29 | 5 |
| 5D RC | 465 | 0 | 4 | 1.55 | 3.22 | 29 | 6 |
| 5D BC+RC | 465 | 11 | 4 | 1.15 | 2.46 | 3 | 1 |
| 3D Bayesian (unchanged) | 465 | 0 | 0 | 1.55 | 3.28 | 29 | 6 |

3D JSON families are bitwise unchanged vs 5D-A. 5D p95 now matches the 3D benchmark except one regression: (12,13) A collapsed (~4100→620) because the first φ bin is a near-empty acceptance hole (y=28 vs plateau ~5200) that is not auto-excluded. Wide 3D-like B/C then let the second `Allow_Multiple_Fits` pass lock the collapsed A. In-memory probe: `fit_range` 15–345 restores redχ² 251→1.62 with B≈-0.19. (9,19) and (14,15) are already at the 3-parameter minimum (stronger 5D modulation / one pathological error bar); range changes do not help.

## 5D-C — (12,13) φ-range only

Optional per-bin `fit_range_lower/upper` in `Fitting_Phi_Function` (applied only when those fields exist; 3D keys do not have them). (12,13) 5D/RC/BC keys: range 15–345, 3D-based B/C with moderate windows.

| Family | n | nan A | empty | redχ² med | p95 | n>3 | n>5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 5D Bayesian | 469 | 0 | 4 | 1.54 | 3.08 | 28 | 4 |
| 5D RC | 465 | 0 | 4 | 1.55 | 3.19 | 28 | 5 |
| 5D BC+RC | 465 | 11 | 4 | 1.15 | 2.46 | 2 | 0 |
| 3D Bayesian (unchanged) | 465 | 0 | 0 | 1.55 | 3.28 | 29 | 6 |

(12,13) 5D Bayesian A=4973, B=-0.189, C=-0.094, red=1.62 (ROOT range 15–345). No other bin got worse vs 5D-B. 3D JSON still bitwise identical.

Stopped here: remaining red>5 bins are either already better than their 3D counterparts or the 3-parameter form is at its visual minimum. Did not rebuild a 5D spline into the universal file (tight `std_multiple=0.3` ranges were the original trap; a rebuild would also drop the (12,13) `fit_range` fields).

See `report_5D.md`.

---

# Final validation pass (3D + 5D)

Attached `*_AsymErr` graphs were ignored for this remake round only (`USE_ASYM_ERRORS_FOR_FIT = False` in `Fitting_Phi_Function`); restored to True after publication. Histogram TH1 bin errors were used.

## Named bins

- **5D (4,23):** untagged B ∈ [−0.22, −0.15] was forcing Cosφ onto a flat 5D histogram. Added 5D/5D-BC keys with B near 0. Bayesian red 2.20 → **1.09** (B −0.075 → −0.017). BC red 2.94 → **0.52**. RC already near 0 (left). Did **not** copy 3D B = −0.24.
- **5D (6,6):** same class (flat 5D vs large-modulation 3D/neighbor 5D (6,5)). 3D/5D parameter matching is not safe. Added 5D keys with B near 0; rewrote the 3D-like 5D-RC key. Bayesian red 2.47 → **0.48**. RC 1.42 → **0.46**. BC 2.30 → **0.57**. Overlay now follows the plateau (edge spike remains).
- **5D (4,28):** real Cosφ, noisy; probes did not beat red ~3.50. **Left.**
- **3D (15,24):** tight 3D spline window undershot the 180° peak. Loosened 3D/3D-RC/3D-BC B/C. Bayesian red 4.10 → **2.74** (B −0.185 → −0.229, C −0.003 → +0.062). Still cannot make a narrow peak with 3-cosine. 5D counterpart left (different, milder shape).

Full 3D remake: only (15,24) redχ² changed in each 3D family. Full 5D remake segfaulted at Q²-y 17 after ~all Bayesian bins; Q²-y **4 and 6** remake succeeded (the only 5D keys changed). 5D Bayesian B changed in exactly 2 bins vs 5D-C.

Published JSON + 18 `HybridV2_4D_xB_*.pkl` (+ npz) to `End_of_Iteration_Scripts/` with `--apply_A_corr --log_A`. See `report.md` final-pass section.

