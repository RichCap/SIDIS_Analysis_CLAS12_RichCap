# φ_h fit refinement report

Hybrid ROOT: `Hybrid_Unfolded_Parallel_SIDIS_epip_from_3D_and_5D_1st_Order_V2.root`  
Unused backup (never used as `--root`): `Hybrid_Unfolded_Parallel_SIDIS_epip_from_3D_and_5D_1st_Order_V2_pre_refinement.root`  
Manual baseline (not overwritten): `Phi_h_Fit_Parameters_Initialize.py`  
Universal initializer: `Prepare_Next_Iteration/Phi_h_Fit_Parameters_from_Spline.py`  
Fit JSON: `Fit_Pars_from_Simple_RooUnfold_SelfContained_using_Hybrid_Unfolded_Parallel_SIDIS_epip_from_3D_and_5D_1st_Order_V2.json`  
Catalogs: `Prepare_Next_Iteration/Fit_Refinement/catalogs/`  
Log: `Prepare_Next_Iteration/Fit_Refinement/CAMPAIGN_LOG.md`

Histogram contents were not rewritten by unfolding, RC application, or BC creation. Fit objects (`Fit_Function`, `Chi_Squared`, `Fit_Par_*`) in the hybrid file were updated. `--Apply_RC` and `--Apply_BC` were never passed.

## Branch status

| Branch | JSON key | Iterations (3D/5D remakes) | Status |
|---|---|---|---|
| 3D acceptance | `Fit_Pars_from_3D_Bayesian` | 4 remakes after iter 0 | Stable. 465 bins, 0 non-finite A. redχ² median 1.55, p95 3.28. |
| 3D acc+RC | `Fit_Pars_from_3D_RC_Bayesian` | same | Stable. 465 bins, 0 non-finite A. median 1.55, p95 3.08. |
| 3D acc+RC+BC | `Fit_Pars_from_3D_BC_RC_Bayesian` | same | Mostly stable; **11 bins have non-finite A**. Finite-bin median 1.11, p95 2.05 (best family). |
| 5D acceptance | `Fit_Pars_from_5D_Bayesian` | same | 469 bins, 4 unused empty (A=0). median 1.74, p95 7.33. Longer tail than 3D. |
| 5D acc+RC | `Fit_Pars_from_5D_RC_Bayesian` | same | 465 bins, 4 empty. median 1.87, p95 9.87. Longest tail. |
| 5D acc+RC+BC | `Fit_Pars_from_5D_BC_RC_Bayesian` | same | Same **11 non-finite A** bins as 3D BC+RC. Finite-bin median 1.21, p95 6.11. |

Convergence was judged per family from the iteration-0 χ² distributions (do not use a global redχ² < 1 cut). 3D p95 is about 3; 5D p95 is 7–11. Averages look acceptable while individual pathological bins remain; those are listed below rather than hidden.

## Iterations

0. Manual baseline (`Phi_h_Fit_Parameters_Initialize.py`). First 3D and 5D remakes. Created 5D RC/BC JSON (previously empty).  
1. Built 4D_xB splines with `--apply_A_corr`; merged tagged keys into the universal file; remade with `--use_spline_init`. BC spline was trained on A=nan / C=1 and leaked into other bins.  
2. Removed poisoned `("q","z","3D"|"5D","BC")` keys except six hand-tuned bins. Remade. Dimension-only `("q","z","3D")` keys still fell back onto BC/RC histograms.  
3. Lookup fixed: dimension-only keys apply only to acceptance-only histograms. Remade.  
4. Rebuilt the universal file as **manual baseline + tagged 3D/5D keys only** (dropped leftover untagged spline keys). Final remakes.

Further retuning of the 11 non-finite-A BC+RC bins is not statistically defensible from the guide alone: A stays nan after C is bounded to ±0.12 and after reverting to the baseline. Those BC+RC φ_h histograms do not support a finite amplitude.

## Final commands

```bash
conda activate updated_python
export PATH="$(conda info --base)/envs/updated_python/bin:$PATH"   # needed here so ./script.py sees env python3

./Simple_RooUnfold_SelfContained.py \
  --root "Hybrid_Unfolded_Parallel_SIDIS_epip_from_3D_and_5D_1st_Order_V2.root" \
  --Use_TTree --unfolding_3D --fit --remake_fit --smear --save_json \
  --use_spline_init

./Simple_RooUnfold_SelfContained.py \
  --root "Hybrid_Unfolded_Parallel_SIDIS_epip_from_3D_and_5D_1st_Order_V2.root" \
  --Use_TTree --unfolding_5D --fit --remake_fit --smear --save_json \
  --use_spline_init
```

Spline / initializer (from `Prepare_Next_Iteration/`, `--apply_A_corr` for A):

```bash
./Create_Continuous_4D_Moments_From_JSON.py \
  --save_init Phi_h_Fit_Parameters_from_Spline.py --generate_init \
  --smoothing_factor_A 0.05 --smoothing_factor 0.00005 \
  --dimension_mode 4D_xB --output_prefix FitRefinement_iter00 \
  --std_multiple 0.3 \
  --json_file ../Fit_Pars_from_Simple_RooUnfold_SelfContained_using_Hybrid_Unfolded_Parallel_SIDIS_epip_from_3D_and_5D_1st_Order_V2.json \
  --fit_set Fit_Pars_from_<3D|5D>_<Bayesian|RC_Bayesian|BC_RC_Bayesian> \
  --kernel_A thin_plate_spline --log_A --kernel gaussian --epsilon 0.75 \
  --apply_A_corr
```

Ordinary histogram fits were **not** cross-section normalized. Spline A uses the existing transformation `A / (Bin_Width_Area_Scale × Luminosity)`.

## Histogram-fit quality (final JSON)

| Family | n | nan A | empty | redχ² median | p95 | n(red>3) | n(red>5) |
|---|---:|---:|---:|---:|---:|---:|---:|
| 3D Bayesian | 465 | 0 | 0 | 1.55 | 3.28 | 29 | 6 |
| 3D RC | 465 | 0 | 0 | 1.55 | 3.08 | 26 | 4 |
| 3D BC+RC | 465 | 11 | 0 | 1.11 | 2.05 | 3 | 1 |
| 5D Bayesian | 469 | 0 | 4 | 1.74 | 7.33 | 91 | 41 |
| 5D RC | 465 | 0 | 4 | 1.87 | 9.87 | 119 | 60 |
| 5D BC+RC | 465 | 11 | 4 | 1.21 | 6.11 | 41 | 28 |

Empty 5D bins are unused high-z cells (including 17-25…28), not failed physics fits.

## Bins with substantive intervention

Hand-tuned in the universal file (C_initial=0, C_limits=[-0.12, 0.12], B from the manual baseline):

- `("7","5","3D","BC")`, `("8","9","3D","BC")`, `("15","3","3D","BC")`
- `("7","5","5D","BC")`, `("8","9","5D","BC")`, `("15","3","5D","BC")`

These stopped C from running to 1. A remains non-finite. **Unresolved.**

Rolled back: all other dimension-tagged BC spline keys (trained on nan/C=1) and leftover untagged spline keys that were not the manual baseline.

## Unresolved / questionable

**Non-finite A (3D and 5D BC+RC):**  
`(4,11)`, `(7,5)`, `(8,9)`, `(8,10)`, `(12,9)`, `(12,10)`, `(12,15)`, `(15,3)`, `(15,4)`, `(15,10)`, `(17,5)`.

`(7,5)`, `(8,9)`, `(15,3)` failed already at iteration 0 (C→1, then A=nan). The others appeared after the first spline-informed remake and did not recover when BC spline keys were removed and the baseline was restored. Treat as BC+RC histogram / fit-numerics problems, not as missing init.

**High redχ² retained (distribution likely supports a large modulation, or a single bad cell):**

- 3D Bayesian / RC: `(12,15)` red ~12–14; `(10,10)` ~7–8; `(1,7)`, `(1,32)`, `(3,29)` ~5–7.
- 5D Bayesian / RC: `(12,13)` red ~326 — **pathological, unresolved**. Then `(9,13)`, `(14,9)`, `(10,17)`, `(13,13)`, `(14,15)`, `(3,12)` in the 20–30 range.
- 5D BC+RC (finite A): `(10,11)` ~41; `(3,17)` ~29; `(14,15)` ~28; `(9,19)` ~24.

These were **not** forced onto the spline. Neighbor disagreement alone was not treated as a reason to overwrite a finite, large-modulation solution.

## Guided toward the spline

Only the six BC+RC C windows above. Evidence: iteration-0 C=1 with A=nan is not a physical Cos2φ moment; the spline trained on that C is not usable. Bounding C to ±0.12 matches the scale of successful neighboring bins. A still failed, so the change is retained only as a guard against C=1, not as a successful amplitude recovery.

## Source changes

- `Simple_RooUnfold_SelfContained.py`: `--json_name` (next to `--save_json`); `--fit_init_file`; method/dimension-aware key lookup; commented-out skip of existing BC histos; JSON save of all present families; per-bin JSON merge; Chi2/NDF in JSON; RooUnfold import optional for `--Use_TTree`; Find_RC import only if `--Apply_RC`; Python 3.13 f-string backslash in `Update_Email`.
- `Create_Continuous_4D_Moments_From_JSON.py`: iFarm-first same-repo import path; merge `--save_init` by family tags; skip non-finite points; zero-area guard on `--apply_A_corr`.
- `Full_Moment_Plots_Creation_From_JSON.py` and `Cross_Section_Normalization.py`: iFarm-first same-repo paths / local `Data_Files_Groovy` charge JSON.

ROOT open/save mode was not changed.

## What was not completed

- Visual gallery of every φ_h overlay: ROOT/PyROOT 3.13 segfaulted after the first canvas. Ranking used χ², parameter errors, and worst-bin inspection instead.
- `--generate_spline_code`: local SciPy is 1.18.0 vs farm 1.16.2; not forced by changing the exporter.
- Full smoothness of 5D parameter curves: not the objective. Several high-redχ² 5D bins remain as data-driven outliers.

---

# Final validation pass (3D + 5D) and publication

Histogram fits remain unnormalized. `--apply_A_corr` (`A / (Bin_Width_Area_Scale × Luminosity)`) was used only for the published 4D_xB A splines (`--log_A`) and for A-level consistency, not as a fit χ² metric.

This remake round fitted TH1 bin errors only (attached `*_AsymErr` / `histo.asym_errors` skipped). That switch was restored to use the asymmetric graphs when present after the products were written. No pptx or presentation builders were modified.

## Refinements kept

| Bin | Action | Result |
|---|---|---|
| 5D (4,23) | 5D-tagged keys with B near 0; do not copy 3D B = −0.24 (5D histogram is flat + last-bin spike) | Bay red 2.20 → 1.09, B −0.075 → −0.017; BC 2.94 → 0.52 |
| 5D (6,6) | Same; 3D/5D shapes are not comparable. Neighbor 5D (6,5) is a large Cosφ, not a target | Bay 2.47 → 0.48; RC 1.42 → 0.46; BC 2.30 → 0.57 |
| 5D (4,28) | Probed ranges/inits; no better 3-cosine | Unchanged, red ~3.50 |
| 3D (15,24) | Loosened tight 3D B/C windows | Bay 4.10 → 2.74, B −0.185 → −0.229, C −0.003 → +0.062. Peak still slightly under-fit (functional form) |

3D remake of all Q²-y: **one** bin changed per 3D family ((15,24)). 5D full remake segfaulted at Q²-y 17; Q²-y 4 and 6 remake applied the new 5D keys (2 Bayesian B values changed vs 5D-C).

## 3D/5D agreement

- **Not enforced:** 5D (4,23) and (6,6) vs 3D. The 5D φ_h distributions are flat; 3D has a large Cosφ. Copying 3D B would worsen the 5D overlay.
- **Not enforced:** 3D (15,24) vs 5D (15,24). 3D has a sharper 180° peak; 5D is milder + an edge spike.
- No pairs were dragged together when that would have hurt the histogram fit.

## Final family stats

| Family | n | nan A | empty | redχ² med | p95 | n>3 | n>5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 3D Bayesian | 465 | 0 | 0 | 1.55 | 3.18 | 28 | 6 |
| 3D RC | 465 | 0 | 0 | 1.55 | 3.00 | 25 | 4 |
| 3D BC+RC | 465 | 11 | 0 | 1.11 | 2.05 | 3 | 1 |
| 5D Bayesian | 469 | 0 | 4 | 1.53 | 3.08 | 28 | 4 |
| 5D RC | 465 | 0 | 4 | 1.55 | 3.19 | 28 | 5 |
| 5D BC+RC | 465 | 11 | 4 | 1.15 | 2.43 | 2 | 0 |

Unresolved (unchanged): (9,19), (14,15), (1,7), (1,32), (9,14) RC, 11 BC+RC nan-A bins, and 5D (4,28) as a noisy but real Cosφ. The retained set is the best defensible balance of histogram description, neighbors, and 3D/5D agreement.

## Publication

Copied into `/Users/richardcapobianco/Desktop/Work_Offline.nosync/End_of_Iteration_Scripts/`:

- `Fit_Pars_from_Simple_RooUnfold_SelfContained_using_Hybrid_Unfolded_Parallel_SIDIS_epip_from_3D_and_5D_1st_Order_V2.json` (previous current file renamed `_V2_Old.json`)
- 18 `HybridV2_4D_xB_<fit_set>_Fit_Par_{A,B,C}.pkl` and matching `.npz`, built with `--dimension_mode 4D_xB --apply_A_corr --log_A` and the plotting-workflow failed-bin filter (`A≤0`, `|B|≥1`, `|C|≥1`, zero/non-finite errors, Chi2 0/non-finite → drop the whole bin).
