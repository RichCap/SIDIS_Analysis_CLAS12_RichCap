# SIDIS physics-results campaign

This note describes the Unweighted and Spline campaigns that are already on disk. Both budgets are provisional. Neither campaign is selected as the quoted result.

## Nominals

- unweighted: weight tag ``, file `Sys3D_nominal_only_20261030_inherited_Unweighted.root`, status `verified`.
- spline: weight tag `Spline`, file `Sys3D_nominal_only_20261030_inherited_Spline.root`, status `verified`.

Iteration 0 is Unweighted. Iteration 1 is Spline. Acc and AccSpline are acceptance-reweighting variations.

## Uncertainty budgets

### unweighted

- Provisional: `True`.
- Bins in the total: `452`.
- Sources in the table: acceptance_reweighting, acceptance_threshold, bayes_iteration, chi2_strict_pip, correction_method, dcfid_el, dcfid_pip, dcfidref_el, dcv_el, dimension, dvz_pip, ecband_el, ecthr_el, electron_sector, noSmear, no_pip_testdc, no_sector_pcal, no_valerii_knockout, pcalvol, phi_bins, pion_sector, rho0_subtraction.
- Excluded from the sum: radiative systematic pending; no number; not zero; bin-centering method blocked; systematic null; not in the sum; bin-centering iteration blocked; not_combined; no number; unweighted versus spline is not_combined and is not added to either total; electron_sector and pion_sector stay not_combined; empty bins are omitted and are not zero; bayesian 1D is disabled and contributes no number; bin-centering subdivision has no 15 observable shifts; not entered; not zero.

### spline

- Provisional: `True`.
- Bins in the total: `452`.
- Sources in the table: acceptance_reweighting, acceptance_threshold, bayes_iteration, chi2_strict_pip, correction_method, dcfid_el, dcfid_pip, dcfidref_el, dcv_el, dvz_pip, ecband_el, ecthr_el, electron_sector, noSmear, no_pip_testdc, no_sector_pcal, no_valerii_knockout, pcalvol, phi_bins, pion_sector, rho0_subtraction.
- Excluded from the sum: radiative systematic pending; no number; not zero; bin-centering method blocked; systematic null; not in the sum; bin-centering iteration blocked; not_combined; no number; unweighted versus spline is not_combined and is not added to either total; electron_sector and pion_sector stay not_combined; empty bins are omitted and are not zero; bayesian 1D is disabled and contributes no number; spline 5D is absent; no number; not zero; bin-centering subdivision is not copied into the Spline budget.

That exclusion text is what the first aggregation wrote. The manifest now uses `inherited_Spline.root` as the Spline nominal, `inherited_Acc.root` as the Unweighted acceptance variation, and the corrected same-weight method branches. Those comparisons are not in the budget file yet and were not fit for this update.

The subdivision systematic is one Unweighted RMS of 15 observable shifts. Those fitted shifts are not in this directory yet, so the source is not in the sum and is not entered as zero. The five variable RMS values are diagnostics. The Spline budget does not receive this source.

## Fit quality and sector failures

The first fits are a single remake. `refine-phi-fits` was not completed, so a return code of 0 is an initial fit, not a finished refinement.

Registry failures recorded in the budget file: `0`.

Unweighted eS1o stopped while fitting `(Q2_y_Bin_3)-(z_pT_Bin_4)`. That unfolded histogram has integral 0 and 24 empty phi bins. The same nominal bin is filled. eS1o has 422 filled and 30 empty Bayesian histograms. The nominal file has 452 filled and none empty. `TH1::Fit` on the empty histogram calls `Warning()`, and that warning segfaults inside CPyCppyy. Return code 129 is the status after the printed segmentation violation. The fitter now skips a histogram whose integral is 0 and keeps ROOT at error level during `TH1::Fit`. The 24 sector jobs were not refit. They stay `not_combined` and are not zero.

## Corrections and kT2

- unweighted corrections wrote `452` histograms. Problems: `0`.
- unweighted normalization status `applied`. Provisional systematic `True`. Factor uncertainty unassigned: `True`.
- unweighted kT2 rows `91`, status counts `{'ok': 78, 'poor': 13, 'rows': 91}`. Source file `kt2/unweighted/kt2_results.tsv`.
- spline corrections wrote `452` histograms. Problems: `0`.
- spline normalization status `applied`. Provisional systematic `True`. Factor uncertainty unassigned: `True`.
- spline kT2 rows `91`, status counts `{'ok': 84, 'poor': 7, 'rows': 91}`. Source file `kt2/spline/kt2_results.tsv`.

B and C are not rescaled by the A0 factor. Their `_SYS` values stay on the unfolded scale.

## Bin centering

Nominal event factors are the 2026-10-26 JSON. `BC_Factor` is the unweighted sub-bin mean divided by the center sub-bin. The injection spline file is `acc020_3D_BC_RC_rawA_4D_xB_Fit_Pars_from_3D_BC_RC_Bayesian_Compute_SplineWeight.txt`.

The updated post-refit spline is not named by the campaign configuration, so the iteration comparison stays blocked. EvGen evaluation at the same points is deferred.

## Agent records

Run `20261101T184840` has `13` distinct agent records.
- `aggregate` / `both` / `budgets` / `aggregate`: `physics_campaign/reports/agents/20261101T184840/aggregate/both/budgets/aggregate.md`.
- `bin_centering` / `both` / `status` / `bin_centering`: `physics_campaign/reports/agents/20261101T184840/bin_centering/both/status/bin_centering.md`.
- `kt2` / `both` / `nominal` / `kt2`: `physics_campaign/reports/agents/20261101T184840/kt2/both/nominal/kt2.md`.
- `mosaic` / `both` / `nominal` / `mosaic`: `physics_campaign/reports/agents/20261101T184840/mosaic/both/nominal/mosaic.md`.
- `nominal` / `unweighted` / `shard-0` / `nominal`: `physics_campaign/reports/agents/20261101T184840/nominal/unweighted/shard-0/nominal.md`.
- `nominal_bc` / `both` / `nominal` / `bc`: `physics_campaign/reports/agents/20261101T184840/nominal_bc/both/nominal/bc.md`.
- `nominal_rc` / `both` / `nominal` / `rc`: `physics_campaign/reports/agents/20261101T184840/nominal_rc/both/nominal/rc.md`.
- `phi_figures` / `both` / `all` / `phi-figures`: `physics_campaign/reports/agents/20261101T184840/phi_figures/both/all/phi-figures.md`.
- `radiative` / `both` / `evgen` / `radiative`: `physics_campaign/reports/agents/20261101T184840/radiative/both/evgen/radiative.md`.
- `refine` / `both` / `variation_shard_1` / `shard`: `physics_campaign/reports/agents/20261101T184840/refine/both/variation_shard_1/shard.md`.
- `refine` / `spline` / `nominal_shard_1` / `nominal`: `physics_campaign/reports/agents/20261101T184840/refine/spline/nominal_shard_1/nominal.md`.
- `resolve` / `both` / `manifest` / `resolve`: `physics_campaign/reports/agents/20261101T184840/resolve/both/manifest/resolve.md`.
- `variations` / `both` / `shard-0` / `variation`: `physics_campaign/reports/agents/20261101T184840/variations/both/shard-0/variation.md`.

## Sector coverage

Sector studies stay out of quadrature. Empty histograms are N/A and are not zeroes. Fitted count is from saved JSON, which is zero while those jobs remain failed.

- `spline` `eS1o`: expected `452`, fitted `0`, N/A empty `34`, other failures `0`, empty fraction `0.0752212389380531`, filled but not saved `418`.
- `unweighted` `eS1o`: expected `452`, fitted `0`, N/A empty `30`, other failures `0`, empty fraction `0.06637168141592921`, filled but not saved `422`.
- `spline` `eS2o`: expected `452`, fitted `0`, N/A empty `32`, other failures `0`, empty fraction `0.07079646017699115`, filled but not saved `420`.
- `unweighted` `eS2o`: expected `452`, fitted `0`, N/A empty `28`, other failures `0`, empty fraction `0.061946902654867256`, filled but not saved `424`.
- `spline` `eS3o`: expected `452`, fitted `0`, N/A empty `30`, other failures `0`, empty fraction `0.06637168141592921`, filled but not saved `422`.
- `unweighted` `eS3o`: expected `452`, fitted `0`, N/A empty `26`, other failures `0`, empty fraction `0.05752212389380531`, filled but not saved `426`.
- `spline` `eS4o`: expected `452`, fitted `0`, N/A empty `31`, other failures `0`, empty fraction `0.06858407079646017`, filled but not saved `421`.
- `unweighted` `eS4o`: expected `452`, fitted `0`, N/A empty `28`, other failures `0`, empty fraction `0.061946902654867256`, filled but not saved `424`.
- `spline` `eS5o`: expected `452`, fitted `0`, N/A empty `31`, other failures `0`, empty fraction `0.06858407079646017`, filled but not saved `421`.
- `unweighted` `eS5o`: expected `452`, fitted `0`, N/A empty `28`, other failures `0`, empty fraction `0.061946902654867256`, filled but not saved `424`.
- `spline` `eS6o`: expected `452`, fitted `0`, N/A empty `31`, other failures `0`, empty fraction `0.06858407079646017`, filled but not saved `421`.
- `unweighted` `eS6o`: expected `452`, fitted `0`, N/A empty `28`, other failures `0`, empty fraction `0.061946902654867256`, filled but not saved `424`.
- `spline` `pipS1o`: expected `452`, fitted `0`, N/A empty `31`, other failures `0`, empty fraction `0.06858407079646017`, filled but not saved `421`.
- `unweighted` `pipS1o`: expected `452`, fitted `0`, N/A empty `27`, other failures `0`, empty fraction `0.059734513274336286`, filled but not saved `425`.
- `spline` `pipS2o`: expected `452`, fitted `0`, N/A empty `31`, other failures `0`, empty fraction `0.06858407079646017`, filled but not saved `421`.
- `unweighted` `pipS2o`: expected `452`, fitted `0`, N/A empty `29`, other failures `0`, empty fraction `0.06415929203539823`, filled but not saved `423`.
- `spline` `pipS3o`: expected `452`, fitted `0`, N/A empty `31`, other failures `0`, empty fraction `0.06858407079646017`, filled but not saved `421`.
- `unweighted` `pipS3o`: expected `452`, fitted `0`, N/A empty `27`, other failures `0`, empty fraction `0.059734513274336286`, filled but not saved `425`.
- `spline` `pipS4o`: expected `452`, fitted `0`, N/A empty `32`, other failures `0`, empty fraction `0.07079646017699115`, filled but not saved `420`.
- `unweighted` `pipS4o`: expected `452`, fitted `0`, N/A empty `31`, other failures `0`, empty fraction `0.06858407079646017`, filled but not saved `421`.
- `spline` `pipS5o`: expected `452`, fitted `0`, N/A empty `32`, other failures `0`, empty fraction `0.07079646017699115`, filled but not saved `420`.
- `unweighted` `pipS5o`: expected `452`, fitted `0`, N/A empty `27`, other failures `0`, empty fraction `0.059734513274336286`, filled but not saved `425`.
- `spline` `pipS6o`: expected `452`, fitted `0`, N/A empty `29`, other failures `0`, empty fraction `0.06415929203539823`, filled but not saved `423`.
- `unweighted` `pipS6o`: expected `452`, fitted `0`, N/A empty `27`, other failures `0`, empty fraction `0.059734513274336286`, filled but not saved `425`.

No sector has an empty fraction at or above 0.25. A separate lower-acceptance unfold is not indicated by this coverage cut. Empty bins remain N/A.

## Correction stages

Stage A is the acceptance `Bayesian` fit. Stage B writes `RC_Bayesian` from that acceptance file and is refined on its own. Stage C writes `BC_RC_Bayesian` from the nominal RC file. A missing radiative alternative stays pending and does not block Stage B. A missing BC alternative does not block Stage C.

## Figures

Mosaic commands use z, P_T, and P_T2, a logarithmic A0 axis, `bin_Q2y` pad labels, series legends, and separate statistical and systematic files. Phi_h figures, when drawn, use `consolidate-thesis-phi-figures` for `unfolded_ac`, `unfolded_rc`, and `unfolded_bc` only.

Artifact directory: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign`.
