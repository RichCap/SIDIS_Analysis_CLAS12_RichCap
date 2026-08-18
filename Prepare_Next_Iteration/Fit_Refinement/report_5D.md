# 5D φ_h fit follow-up report

Hybrid ROOT (fits updated): `Hybrid_Unfolded_Parallel_SIDIS_epip_from_3D_and_5D_1st_Order_V2.root`  
Universal initializer: `Prepare_Next_Iteration/Phi_h_Fit_Parameters_from_Spline.py`  
Manual baseline (not overwritten): `Phi_h_Fit_Parameters_Initialize.py`  
Fit JSON: `Fit_Pars_from_Simple_RooUnfold_SelfContained_using_Hybrid_Unfolded_Parallel_SIDIS_epip_from_3D_and_5D_1st_Order_V2.json`  
Log: `Prepare_Next_Iteration/Fit_Refinement/CAMPAIGN_LOG.md`  
Catalogs: `Prepare_Next_Iteration/Fit_Refinement/catalogs/5D_iter{A,B,C}_*`  
Overlays: `Prepare_Next_Iteration/Fit_Refinement/plots/5D_iterC/`

3D remakes were not run. 3D JSON families are bitwise identical to the pre-campaign snapshot.

## Starting-guide decision

The previous campaign’s **tight 5D spline guidance was discarded**, not retained.

Evidence from that campaign and from 5D-A:

- Median 5D spline B window was 0.021 vs baseline 0.17; ~80% of 5D Bayesian/RC B and C sat on a limit.
- Restarting 5D from `Phi_h_Fit_Parameters_Initialize.py` (no `--use_spline_init`) only moved 5D Bayesian p95 from 7.33 → 7.00 and n(red>5) 41 → 39. The 5D histograms still needed more freedom than the leftover tight 5D keys allowed.
- Several of the worst 5D bins had much smaller |B| than the successful 3D counterpart, e.g. (9,19) 5D B = −0.044 vs 3D B = −0.208 (red 98.8 vs 0.89).

So 5D was **restarted from the manual baseline**, then the remaining tight 5D / 5D-RC spline keys were **replaced** by 80 / 84 / 41 wide 5D-only keys. Those keys take B/C from the current 3D result in the same (Q²-y, z-pT) bin, with windows B ± 0.35 and C ± 0.22. 3D keys and the six hand BC C-guards were left untouched.

A later 5D spline rebuild was **not** merged back into the universal file. Re-training at `std_multiple=0.3` would re-tighten the windows that caused the original trap and would drop the (12,13) `fit_range` fields.

## Iterations (5D only)

| Iter | What | 5D Bayesian p95 / n>5 | 5D RC p95 / n>5 | 5D BC+RC p95 / n>5 |
|---|---|---:|---:|---:|
| Pre-campaign (tight spline) | frozen 3D; 5D trapped | 7.33 / 41 | 9.87 / 60 | 6.11 / 28 |
| **5D-A** | remake from manual baseline | 7.00 / 39 | 11.01 / 48 | 6.11 / 28 |
| **5D-B** | wide 3D-initialized 5D keys | 3.11 / 5 | 3.22 / 6 | 2.46 / 1 |
| **5D-C** | (12,13) φ range 15–345 | **3.08 / 4** | **3.19 / 5** | **2.46 / 0** |
| 3D benchmark (unchanged) | not remade | 3.28 / 6 | 3.08 / 4 | 2.05 / 1 |

Three 5D remakes. No 3D remake.

## Problem classes

1. **Over-tight 5D spline windows.** Fits sat on B/C limits and could not follow the 5D φ_h shape. Dominant failure of the previous campaign.
2. **Suppressed |B| vs the 3D counterpart.** Same kinematic bin, much smaller 5D Cosφ term, χ² in the tens to ~100. Fixed in 5D-B by starting from the 3D B/C with wide limits.
3. **Acceptance hole that is not quite empty.** (12,13) first φ bin is y ≈ 28 vs a plateau of ~5200. Auto range only skips *exactly* empty bins, so the hole stayed in the fit, drove B+C → −1, and collapsed A (~4100 → ~620). 5D-B made this worse (red 24 → 251). 5D-C excludes φ < 15°.
4. **3-parameter shape residual.** A few bins ((9,19), (14,15), (1,7), …) have a slightly flatter peak or boxier shoulders than A(1 + B cosφ + C cos2φ). χ² stays high while the overlay is already the best that form can do.
5. **Single-bin edge spikes / pathological errors.** (1,32) last bin; (9,14) RC edges; (9,19) one bin with e ≈ 89 vs neighbors ~350. Not an initialization problem.
6. **Non-finite A on BC+RC.** Same 11 bins as 3D BC+RC. Unchanged and not reopened.

## Changes that actually improved 5D

- Dropping the tight 5D spline keys and restarting from the manual baseline (so the 5D-B keys were not refining a trapped state).
- Wide 5D-only keys initialized from the *3D* B/C, not from the failed 5D spline. This is what moved p95 from ~7–11 to ~3.1.
- Per-bin `fit_range_lower/upper` in `Fitting_Phi_Function`, applied **only** when those fields exist. Used solely on (12,13) 5D / 5D-RC / 5D-BC. 3D keys have no such fields, so 3D behavior is unchanged. (12,13) redχ²: 251 → 1.62 / 1.62 / 1.15.

In-memory probes showed that changing the range or B/C of (9,19) and (14,15) does not lower χ². Those bins were left at the 5D-B solution.

## Final 5D fit quality vs 3D benchmark

| Family | n | nan A | empty | redχ² med | p95 | n(red>3) | n(red>5) |
|---|---:|---:|---:|---:|---:|---:|---:|
| 5D Bayesian | 469 | 0 | 4 | 1.54 | 3.08 | 28 | 4 |
| 5D RC | 465 | 0 | 4 | 1.55 | 3.19 | 28 | 5 |
| 5D BC+RC | 465 | 11 | 4 | 1.15 | 2.46 | 2 | 0 |
| 3D Bayesian | 465 | 0 | 0 | 1.55 | 3.28 | 29 | 6 |
| 3D RC | 465 | 0 | 0 | 1.55 | 3.08 | 26 | 4 |
| 3D BC+RC | 465 | 11 | 0 | 1.11 | 2.05 | 3 | 1 |

5D Bayesian now matches or beats 3D on median, p95, n>3, and n>5. 5D RC is at the 3D p95 scale (3.19 vs 3.08) with one extra red>5 bin. 5D BC+RC has *fewer* red>3 / red>5 bins than 3D; its p95 is still a bit higher (2.46 vs 2.05) because the remaining (9,19) sits at 4.48.

Empty 5D cells are the unused high-z bins (17, 25–28), not failed fits.

red>5 by Q²-y after 5D-C is no longer “several outliers in every region”:

- Bayesian: Q²-y 1 (2), 9 (1), 14 (1)
- RC: Q²-y 1 (2), 9 (2), 14 (1)
- BC+RC: none

## Remaining unresolved bins

| Bin | 5D redχ² | 3D redχ² | Why it stops here |
|---|---|---|---|
| (9,19) | Bay 10.79, RC 10.93, BC 4.48 | 0.89 / 0.90 / 0.66 | Stronger 5D Cosφ than 3D (B ≈ −0.30 vs −0.21). Overlay follows the histogram; residual is a flatter peak than a 3-cosine can make, plus one bin with an abnormally small error. Range/init changes do not help. |
| (14,15) | Bay 5.67, RC 5.51 | 1.02 / 1.00 | Same class: larger 5D modulation (B ≈ −0.38 vs −0.09), visually good, boxier shoulders than the functional form. |
| (1,7) | Bay 6.18, RC 5.16 | 6.56 / 5.46 | **Better than 3D.** Same hard bin the 3D campaign already accepted. |
| (1,32) | Bay 5.43, RC 5.40, BC 3.96 | 5.76 / 5.73 / 4.14 | **Better than 3D.** Single last-bin spike at φ ≈ 352.5°. |
| (9,14) RC | 5.43 | 2.71 | Well-measured center is nearly flat; edges have huge errors and a spike. 3D B = −0.43 would wreck the center. |
| BC+RC nan A | same 11 bins as 3D | same 11 | Histogram / numerics; C-guards already in place. Not reopened. |

Typical Q²-y bins (example: (8,17) Bayesian, red = 0.56) now show the same visual quality as the 3D campaign.

## 3D results were not degraded

- No 3D remake.
- 3D JSON vs 5D-A / 5D-B / pre-campaign: 0 changed bins in all three families.
- The only shared source change is optional per-bin `fit_range_*` in `Fitting_Phi_Function`. It runs only when those fields are present. No 3D key has them.
- 3D (15,24) was left as-is, as requested.

## Commands (5D remakes)

```bash
conda activate updated_python
export PATH="$(conda info --base)/envs/updated_python/bin:$PATH"

# 5D-A: restart from manual baseline
./Simple_RooUnfold_SelfContained.py \
  --root "Hybrid_Unfolded_Parallel_SIDIS_epip_from_3D_and_5D_1st_Order_V2.root" \
  --Use_TTree --unfolding_5D --fit --remake_fit --smear --save_json

# 5D-B and 5D-C: wide 5D keys in the universal initializer
./Simple_RooUnfold_SelfContained.py \
  --root "Hybrid_Unfolded_Parallel_SIDIS_epip_from_3D_and_5D_1st_Order_V2.root" \
  --Use_TTree --unfolding_5D --fit --remake_fit --smear --save_json \
  --use_spline_init
```
