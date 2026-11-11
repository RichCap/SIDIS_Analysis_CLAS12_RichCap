# φ_h missing-coverage scan

This pass measures coverage only. It does not select a threshold and it does not recalculate systematic uncertainties.

## Execution

Command:

```
/Users/richardcapobianco/opt/miniforge3/envs/updated_python/bin/python /Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/phi_h_coverage_20261109/scan_phi_h_coverage.py
```

Inputs:

- Comparison manifest: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/review_comparisons_v3/jobs.json`
- Contribution shares: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/budgets/rerun_refinement_20261108/per_bin_source_shares.json`
- Manual sector exclusions: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/budgets/sector_fit_exclusions_20261106.json`
- Histogram files: the distinct baseline and variation ROOT paths in the manifest, under `physics_campaign/refinement_20261108/`.

## Rules

The reporting population is the retained kinematic bins, Q²–y bins 1–17, after `skip_condition_z_pT_bins` and before manual sector exclusions. This run has 452 retained bins.

An in-range φ_h bin is empty when its content is finite and exactly zero. Negative nonzero contents are not empty. Missing coverage is the sum of the widths of the empty bins on the full stored axis, excluding underflow and overflow, so an internal gap counts. A present histogram with every bin empty has 360° missing. Widths are read from the histogram, so a 12-bin distribution is scored in degrees.

A histogram with any non-finite bin content is invalid. Invalid histograms are counted separately and are omitted from threshold pass/fail counts and from the sector comparison counts. A missing histogram object is counted separately and is not assigned a coverage.

A histogram passes a threshold when its missing coverage is less than or equal to the threshold. The thresholds are 90°, 120°, 135°, 150°, and 180°. For 15° bins those limits are 6, 8, 9, 10, and 12 empty bins. The failure percentage denominator is the assessed count: histograms that are present and not invalid.

A nominal failure is only a candidate bin dropped after unfolding. A variation failure is only a candidate unavailable comparison for that variation.

## Summary

Percentages are failures divided by that row's assessed count.

| Input | Stage | Expected | Assessed | Missing | Invalid | >90° | >120° | >135° | >150° | >180° |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nominal spline acceptance | spline, acceptance | 452 | 452 | 0 | 0 | 17/452 (3.8%) | 3/452 (0.7%) | 0/452 (0.0%) | 0/452 (0.0%) | 0/452 (0.0%) |
| nominal unweighted acceptance | unweighted, acceptance | 452 | 452 | 0 | 0 | 16/452 (3.5%) | 3/452 (0.7%) | 1/452 (0.2%) | 0/452 (0.0%) | 0/452 (0.0%) |
| nominal spline radiative correction | spline, radiative correction | 452 | 452 | 0 | 0 | 17/452 (3.8%) | 3/452 (0.7%) | 0/452 (0.0%) | 0/452 (0.0%) | 0/452 (0.0%) |
| nominal spline bin centering | spline, bin centering | 452 | 452 | 0 | 0 | 17/452 (3.8%) | 3/452 (0.7%) | 0/452 (0.0%) | 0/452 (0.0%) | 0/452 (0.0%) |
| acceptance_reweighting / Acceptance weights | spline, acceptance | 452 | 452 | 0 | 0 | 19/452 (4.2%) | 3/452 (0.7%) | 1/452 (0.2%) | 0/452 (0.0%) | 0/452 (0.0%) |
| sector / E1 | spline, acceptance | 452 | 452 | 0 | 0 | 303/452 (67.0%) | 246/452 (54.4%) | 223/452 (49.3%) | 192/452 (42.5%) | 124/452 (27.4%) |
| sector / P1 | spline, acceptance | 452 | 452 | 0 | 0 | 271/452 (60.0%) | 210/452 (46.5%) | 185/452 (40.9%) | 158/452 (35.0%) | 99/452 (21.9%) |
| sector / E2 | spline, acceptance | 452 | 452 | 0 | 0 | 286/452 (63.3%) | 235/452 (52.0%) | 209/452 (46.2%) | 171/452 (37.8%) | 113/452 (25.0%) |
| sector / P2 | spline, acceptance | 452 | 452 | 0 | 0 | 298/452 (65.9%) | 238/452 (52.7%) | 216/452 (47.8%) | 182/452 (40.3%) | 125/452 (27.7%) |
| sector / E3 | spline, acceptance | 452 | 452 | 0 | 0 | 278/452 (61.5%) | 218/452 (48.2%) | 189/452 (41.8%) | 161/452 (35.6%) | 106/452 (23.5%) |
| sector / P3 | spline, acceptance | 452 | 452 | 0 | 0 | 305/452 (67.5%) | 250/452 (55.3%) | 229/452 (50.7%) | 195/452 (43.1%) | 123/452 (27.2%) |
| sector / E4 | spline, acceptance | 452 | 452 | 0 | 0 | 283/452 (62.6%) | 225/452 (49.8%) | 197/452 (43.6%) | 167/452 (36.9%) | 110/452 (24.3%) |
| sector / P4 | spline, acceptance | 452 | 452 | 0 | 0 | 285/452 (63.1%) | 233/452 (51.5%) | 211/452 (46.7%) | 179/452 (39.6%) | 119/452 (26.3%) |
| sector / E5 | spline, acceptance | 452 | 452 | 0 | 0 | 290/452 (64.2%) | 235/452 (52.0%) | 215/452 (47.6%) | 182/452 (40.3%) | 122/452 (27.0%) |
| sector / P5 | spline, acceptance | 452 | 452 | 0 | 0 | 289/452 (63.9%) | 232/452 (51.3%) | 209/452 (46.2%) | 169/452 (37.4%) | 114/452 (25.2%) |
| sector / E6 | spline, acceptance | 452 | 452 | 0 | 0 | 292/452 (64.6%) | 240/452 (53.1%) | 216/452 (47.8%) | 181/452 (40.0%) | 114/452 (25.2%) |
| sector / P6 | spline, acceptance | 452 | 452 | 0 | 0 | 279/452 (61.7%) | 226/452 (50.0%) | 199/452 (44.0%) | 170/452 (37.6%) | 108/452 (23.9%) |
| chi2_pid / Stricter bound | spline, acceptance | 452 | 452 | 0 | 0 | 32/452 (7.1%) | 11/452 (2.4%) | 7/452 (1.5%) | 4/452 (0.9%) | 1/452 (0.2%) |
| physics_injection / Zeroth-order unweighted | unweighted, bin centering | 452 | 452 | 0 | 0 | 16/452 (3.5%) | 3/452 (0.7%) | 1/452 (0.2%) | 0/452 (0.0%) | 0/452 (0.0%) |
| acceptance_method / Bin-by-bin | spline, bin-by-bin | 452 | 452 | 0 | 0 | 17/452 (3.8%) | 3/452 (0.7%) | 0/452 (0.0%) | 0/452 (0.0%) | 0/452 (0.0%) |
| acceptance_method / Unweighted 5D | unweighted, 5D acceptance | 452 | 452 | 0 | 0 | 16/452 (3.5%) | 3/452 (0.7%) | 1/452 (0.2%) | 0/452 (0.0%) | 0/452 (0.0%) |
| pion_dc_extra / Boundaries removed | spline, acceptance | 452 | 452 | 0 | 0 | 8/452 (1.8%) | 0/452 (0.0%) | 0/452 (0.0%) | 0/452 (0.0%) | 0/452 (0.0%) |
| pcal_volume / Loose | spline, acceptance | 452 | 452 | 0 | 0 | 17/452 (3.8%) | 3/452 (0.7%) | 0/452 (0.0%) | 0/452 (0.0%) | 0/452 (0.0%) |
| pcal_volume / Tight | spline, acceptance | 452 | 452 | 0 | 0 | 22/452 (4.9%) | 4/452 (0.9%) | 3/452 (0.7%) | 1/452 (0.2%) | 0/452 (0.0%) |
| spline_bc / Initial injection spline | spline, bin centering | 452 | 452 | 0 | 0 | 17/452 (3.8%) | 3/452 (0.7%) | 0/452 (0.0%) | 0/452 (0.0%) | 0/452 (0.0%) |
| bc_sampling / sub\_phi\_5 | spline, bin centering | 452 | 452 | 0 | 0 | 17/452 (3.8%) | 3/452 (0.7%) | 0/452 (0.0%) | 0/452 (0.0%) | 0/452 (0.0%) |
| bc_sampling / sub\_phi\_7 | spline, bin centering | 452 | 452 | 0 | 0 | 17/452 (3.8%) | 3/452 (0.7%) | 0/452 (0.0%) | 0/452 (0.0%) | 0/452 (0.0%) |
| bc_sampling / sub\_phi\_9 | spline, bin centering | 452 | 452 | 0 | 0 | 17/452 (3.8%) | 3/452 (0.7%) | 0/452 (0.0%) | 0/452 (0.0%) | 0/452 (0.0%) |
| bc_sampling / sub\_pt\_3 | spline, bin centering | 452 | 452 | 0 | 0 | 17/452 (3.8%) | 3/452 (0.7%) | 0/452 (0.0%) | 0/452 (0.0%) | 0/452 (0.0%) |
| bc_sampling / sub\_pt\_5 | spline, bin centering | 452 | 452 | 0 | 0 | 17/452 (3.8%) | 3/452 (0.7%) | 0/452 (0.0%) | 0/452 (0.0%) | 0/452 (0.0%) |
| bc_sampling / sub\_pt\_7 | spline, bin centering | 452 | 452 | 0 | 0 | 17/452 (3.8%) | 3/452 (0.7%) | 0/452 (0.0%) | 0/452 (0.0%) | 0/452 (0.0%) |
| bc_sampling / sub\_q2\_3 | spline, bin centering | 452 | 452 | 0 | 0 | 17/452 (3.8%) | 3/452 (0.7%) | 0/452 (0.0%) | 0/452 (0.0%) | 0/452 (0.0%) |
| bc_sampling / sub\_q2\_5 | spline, bin centering | 452 | 452 | 0 | 0 | 17/452 (3.8%) | 3/452 (0.7%) | 0/452 (0.0%) | 0/452 (0.0%) | 0/452 (0.0%) |
| bc_sampling / sub\_q2\_7 | spline, bin centering | 452 | 452 | 0 | 0 | 17/452 (3.8%) | 3/452 (0.7%) | 0/452 (0.0%) | 0/452 (0.0%) | 0/452 (0.0%) |
| bc_sampling / sub\_y\_3 | spline, bin centering | 452 | 452 | 0 | 0 | 17/452 (3.8%) | 3/452 (0.7%) | 0/452 (0.0%) | 0/452 (0.0%) | 0/452 (0.0%) |
| bc_sampling / sub\_y\_5 | spline, bin centering | 452 | 452 | 0 | 0 | 17/452 (3.8%) | 3/452 (0.7%) | 0/452 (0.0%) | 0/452 (0.0%) | 0/452 (0.0%) |
| bc_sampling / sub\_y\_7 | spline, bin centering | 452 | 452 | 0 | 0 | 17/452 (3.8%) | 3/452 (0.7%) | 0/452 (0.0%) | 0/452 (0.0%) | 0/452 (0.0%) |
| bc_sampling / sub\_z\_3 | spline, bin centering | 452 | 452 | 0 | 0 | 17/452 (3.8%) | 3/452 (0.7%) | 0/452 (0.0%) | 0/452 (0.0%) | 0/452 (0.0%) |
| bc_sampling / sub\_z\_5 | spline, bin centering | 452 | 452 | 0 | 0 | 17/452 (3.8%) | 3/452 (0.7%) | 0/452 (0.0%) | 0/452 (0.0%) | 0/452 (0.0%) |
| bc_sampling / sub\_z\_7 | spline, bin centering | 452 | 452 | 0 | 0 | 17/452 (3.8%) | 3/452 (0.7%) | 0/452 (0.0%) | 0/452 (0.0%) | 0/452 (0.0%) |
| rc_model / Initial-model bin center | spline, radiative correction | 452 | 452 | 0 | 0 | 17/452 (3.8%) | 3/452 (0.7%) | 0/452 (0.0%) | 0/452 (0.0%) | 0/452 (0.0%) |
| rc_model / First-iteration bin center | spline, radiative correction | 452 | 452 | 0 | 0 | 17/452 (3.8%) | 3/452 (0.7%) | 0/452 (0.0%) | 0/452 (0.0%) | 0/452 (0.0%) |
| exclusive_rho0 / Subtraction omitted | spline, acceptance | 452 | 452 | 0 | 0 | 17/452 (3.8%) | 3/452 (0.7%) | 0/452 (0.0%) | 0/452 (0.0%) | 0/452 (0.0%) |
| phi_binning / 12 bins | spline, acceptance | 452 | 452 | 0 | 0 | 19/452 (4.2%) | 2/452 (0.4%) | 2/452 (0.4%) | 0/452 (0.0%) | 0/452 (0.0%) |
| sector_pcal / Vetoes removed | spline, acceptance | 452 | 452 | 0 | 0 | 17/452 (3.8%) | 3/452 (0.7%) | 0/452 (0.0%) | 0/452 (0.0%) | 0/452 (0.0%) |
| electron_dc_refinement / Loose | spline, acceptance | 452 | 452 | 0 | 0 | 16/452 (3.5%) | 2/452 (0.4%) | 0/452 (0.0%) | 0/452 (0.0%) | 0/452 (0.0%) |
| electron_dc_refinement / Tight | spline, acceptance | 452 | 452 | 0 | 0 | 19/452 (4.2%) | 4/452 (0.9%) | 3/452 (0.7%) | 1/452 (0.2%) | 0/452 (0.0%) |
| acceptance_threshold / 0.015 | spline, acceptance | 452 | 452 | 0 | 0 | 13/452 (2.9%) | 1/452 (0.2%) | 0/452 (0.0%) | 0/452 (0.0%) | 0/452 (0.0%) |
| acceptance_threshold / 0.025 | spline, acceptance | 452 | 452 | 0 | 0 | 26/452 (5.8%) | 5/452 (1.1%) | 4/452 (0.9%) | 2/452 (0.4%) | 0/452 (0.0%) |
| pion_dc_edges / Loose | spline, acceptance | 452 | 452 | 0 | 0 | 17/452 (3.8%) | 2/452 (0.4%) | 0/452 (0.0%) | 0/452 (0.0%) | 0/452 (0.0%) |
| pion_dc_edges / Tight | spline, acceptance | 452 | 452 | 0 | 0 | 19/452 (4.2%) | 3/452 (0.7%) | 1/452 (0.2%) | 1/452 (0.2%) | 0/452 (0.0%) |
| electron_vz / Loose | spline, acceptance | 452 | 452 | 0 | 0 | 17/452 (3.8%) | 3/452 (0.7%) | 0/452 (0.0%) | 0/452 (0.0%) | 0/452 (0.0%) |
| electron_vz / Tight | spline, acceptance | 452 | 452 | 0 | 0 | 17/452 (3.8%) | 3/452 (0.7%) | 1/452 (0.2%) | 0/452 (0.0%) | 0/452 (0.0%) |
| momentum_smearing / Smearing removed | spline, acceptance | 452 | 452 | 0 | 0 | 17/452 (3.8%) | 3/452 (0.7%) | 0/452 (0.0%) | 0/452 (0.0%) | 0/452 (0.0%) |
| pcal_dead / Strips removed | spline, acceptance | 452 | 452 | 0 | 0 | 17/452 (3.8%) | 3/452 (0.7%) | 0/452 (0.0%) | 0/452 (0.0%) | 0/452 (0.0%) |
| bayes_iterations / $k-1$ | spline, acceptance | 452 | 452 | 0 | 0 | 17/452 (3.8%) | 3/452 (0.7%) | 0/452 (0.0%) | 0/452 (0.0%) | 0/452 (0.0%) |
| bayes_iterations / $k+1$ | spline, acceptance | 452 | 452 | 0 | 0 | 17/452 (3.8%) | 3/452 (0.7%) | 0/452 (0.0%) | 0/452 (0.0%) | 0/452 (0.0%) |
| pcal_ep / Loose | spline, acceptance | 452 | 452 | 0 | 0 | 17/452 (3.8%) | 3/452 (0.7%) | 0/452 (0.0%) | 0/452 (0.0%) | 0/452 (0.0%) |
| pcal_ep / Tight | spline, acceptance | 452 | 452 | 0 | 0 | 17/452 (3.8%) | 3/452 (0.7%) | 0/452 (0.0%) | 0/452 (0.0%) | 0/452 (0.0%) |
| sampling_fraction / Loose | spline, acceptance | 452 | 452 | 0 | 0 | 17/452 (3.8%) | 3/452 (0.7%) | 0/452 (0.0%) | 0/452 (0.0%) | 0/452 (0.0%) |
| sampling_fraction / Tight | spline, acceptance | 452 | 452 | 0 | 0 | 17/452 (3.8%) | 3/452 (0.7%) | 0/452 (0.0%) | 0/452 (0.0%) | 0/452 (0.0%) |
| vertex_separation / Loose | spline, acceptance | 452 | 452 | 0 | 0 | 17/452 (3.8%) | 3/452 (0.7%) | 0/452 (0.0%) | 0/452 (0.0%) | 0/452 (0.0%) |
| vertex_separation / Tight | spline, acceptance | 452 | 452 | 0 | 0 | 17/452 (3.8%) | 3/452 (0.7%) | 0/452 (0.0%) | 0/452 (0.0%) | 0/452 (0.0%) |
| electron_dc_edges / Loose | spline, acceptance | 452 | 452 | 0 | 0 | 17/452 (3.8%) | 3/452 (0.7%) | 0/452 (0.0%) | 0/452 (0.0%) | 0/452 (0.0%) |
| electron_dc_edges / Tight | spline, acceptance | 452 | 452 | 0 | 0 | 17/452 (3.8%) | 3/452 (0.7%) | 0/452 (0.0%) | 0/452 (0.0%) | 0/452 (0.0%) |

Histograms with at least one negative nonzero bin: 0. Those bins were not counted as empty.
Histograms whose axis does not run from 0° to 360°: 0.

## Source order

Variation sources are ordered by the largest of their A₀, cos φ_h, and cos 2φ_h table contribution shares in `table_shares_percent`. The share is not a fraction of the combined systematic row.

- `acceptance_reweighting` (Acceptance reweighting): largest share 67.52% for cos phi_h.
- `sector` (Sector dependence): largest share 36.72% for cos 2phi_h.
- `chi2_pid` (Pion $\chi^{2}_{\mathrm{PID}}$): largest share 26.47% for A0.
- `physics_injection` (Physics injection): largest share 15.75% for A0.
- `acceptance_method` (Acceptance method): largest share 15.72% for A0.
- `pion_dc_extra` (Additional $\pi^{+}$ DC fiducial): largest share 11.69% for cos 2phi_h.
- `pcal_volume` (PCAL volume): largest share 5.33% for A0.
- `spline_bc` (Spline BC): largest share 4.05% for A0.
- `bc_sampling` (BC kinematics): largest share 3.58% for A0.
- `rc_model` (RC model): largest share 2.15% for cos 2phi_h.
- `exclusive_rho0` (Exclusive $\rho^{0}$): largest share 2.14% for A0.
- `phi_binning` ($\phi_h$ binning): largest share 1.53% for cos 2phi_h.
- `sector_pcal` (Sector PCAL fiducial): largest share 0.80% for A0.
- `electron_dc_refinement` (Electron DC refinement): largest share 0.48% for cos 2phi_h.
- `acceptance_threshold` (Acceptance threshold): largest share 0.42% for cos 2phi_h.
- `pion_dc_edges` ($\pi^{+}$ DC edges): largest share 0.37% for cos 2phi_h.
- `electron_vz` (Electron $v_z$): largest share 0.35% for A0.
- `momentum_smearing` (MC momentum smearing): largest share 0.33% for cos 2phi_h.
- `pcal_dead` (PCAL dead channels): largest share 0.25% for A0.
- `bayes_iterations` (Bayesian iterations): largest share 0.24% for cos 2phi_h.
- `pcal_ep` (PCAL $E/p$): largest share 0.24% for cos 2phi_h.
- `sampling_fraction` (Sampling fraction): largest share 0.22% for cos 2phi_h.
- `vertex_separation` ($|\Delta v_z|$): largest share 0.22% for cos 2phi_h.
- `electron_dc_edges` (Electron DC edges): largest share 0.22% for cos 2phi_h.

## Nominal failing bins

These are candidate bins dropped after unfolding. They are not variation comparisons.

### nominal spline acceptance

File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/nominal/acceptance/fit_copy.root`

Above 90° (17/452 (3.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)

Above 135° (0/452 (0.0%)):

None.

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

### nominal unweighted acceptance

File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/unweighted/nominal/acceptance/fit_copy.root`

Above 90° (16/452 (3.5%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (105.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°)
(Q2_y_Bin_5)-(z_pT_Bin_2) (120.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°)
(Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)

Above 135° (1/452 (0.2%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (150.0°)

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

### nominal spline radiative correction

File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/nominal/rc/corrected.root`

Above 90° (17/452 (3.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)

Above 135° (0/452 (0.0%)):

None.

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

### nominal spline bin centering

File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/nominal/bc/corrected.root`

Above 90° (17/452 (3.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)

Above 135° (0/452 (0.0%)):

None.

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

## Variation failing bins

## Source `acceptance_reweighting` — largest table share 67.52% (cos phi_h)

### acceptance_reweighting / Acceptance weights

Stage: spline, acceptance. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/acceptance_reweighting/AccSpline/fit_copy.root`

Above 90° (19/452 (4.2%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_2)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°)
(Q2_y_Bin_4)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (105.0°)
(Q2_y_Bin_4)-(z_pT_Bin_7) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_5)-(z_pT_Bin_7) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°)
(Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (150.0°)

Above 135° (1/452 (0.2%)):

(Q2_y_Bin_4)-(z_pT_Bin_10) (150.0°)

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

## Source `sector` — largest table share 36.72% (cos 2phi_h)

### sector / E1

Stage: spline, acceptance. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/electron_sector/eS1o/fit_copy.root`

Above 90° (303/452 (67.0%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (270.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_11) (120.0°)
(Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_16) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_17) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_2) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_23) (150.0°)
(Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (210.0°)
(Q2_y_Bin_1)-(z_pT_Bin_31) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_32) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_4) (240.0°)
(Q2_y_Bin_1)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_6) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_7) (165.0°)
(Q2_y_Bin_1)-(z_pT_Bin_8) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_10)-(z_pT_Bin_1) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_10) (135.0°), (Q2_y_Bin_10)-(z_pT_Bin_11) (135.0°), (Q2_y_Bin_10)-(z_pT_Bin_12) (105.0°)
(Q2_y_Bin_10)-(z_pT_Bin_13) (105.0°), (Q2_y_Bin_10)-(z_pT_Bin_15) (135.0°), (Q2_y_Bin_10)-(z_pT_Bin_16) (120.0°)
(Q2_y_Bin_10)-(z_pT_Bin_2) (150.0°), (Q2_y_Bin_10)-(z_pT_Bin_20) (120.0°), (Q2_y_Bin_10)-(z_pT_Bin_21) (120.0°)
(Q2_y_Bin_10)-(z_pT_Bin_26) (150.0°), (Q2_y_Bin_10)-(z_pT_Bin_3) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_31) (165.0°)
(Q2_y_Bin_10)-(z_pT_Bin_32) (195.0°), (Q2_y_Bin_10)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_10)-(z_pT_Bin_4) (165.0°)
(Q2_y_Bin_10)-(z_pT_Bin_5) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_7) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_9) (120.0°), (Q2_y_Bin_11)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_11)-(z_pT_Bin_10) (165.0°)
(Q2_y_Bin_11)-(z_pT_Bin_11) (120.0°), (Q2_y_Bin_11)-(z_pT_Bin_13) (135.0°), (Q2_y_Bin_11)-(z_pT_Bin_14) (150.0°)
(Q2_y_Bin_11)-(z_pT_Bin_15) (180.0°), (Q2_y_Bin_11)-(z_pT_Bin_18) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_19) (150.0°)
(Q2_y_Bin_11)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_11)-(z_pT_Bin_20) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_21) (240.0°)
(Q2_y_Bin_11)-(z_pT_Bin_22) (240.0°), (Q2_y_Bin_11)-(z_pT_Bin_23) (270.0°), (Q2_y_Bin_11)-(z_pT_Bin_24) (315.0°)
(Q2_y_Bin_11)-(z_pT_Bin_3) (255.0°), (Q2_y_Bin_11)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_11)-(z_pT_Bin_6) (165.0°)
(Q2_y_Bin_11)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_11)-(z_pT_Bin_9) (165.0°), (Q2_y_Bin_12)-(z_pT_Bin_11) (210.0°)
(Q2_y_Bin_12)-(z_pT_Bin_12) (120.0°), (Q2_y_Bin_12)-(z_pT_Bin_13) (120.0°), (Q2_y_Bin_12)-(z_pT_Bin_14) (360.0°)
(Q2_y_Bin_12)-(z_pT_Bin_16) (120.0°), (Q2_y_Bin_12)-(z_pT_Bin_18) (120.0°), (Q2_y_Bin_12)-(z_pT_Bin_19) (285.0°)
(Q2_y_Bin_12)-(z_pT_Bin_21) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_22) (345.0°), (Q2_y_Bin_12)-(z_pT_Bin_23) (345.0°)
(Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_6) (225.0°), (Q2_y_Bin_12)-(z_pT_Bin_7) (315.0°)
(Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_13)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_13)-(z_pT_Bin_12) (105.0°)
(Q2_y_Bin_13)-(z_pT_Bin_17) (105.0°), (Q2_y_Bin_13)-(z_pT_Bin_2) (120.0°), (Q2_y_Bin_13)-(z_pT_Bin_26) (120.0°)
(Q2_y_Bin_13)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_13)-(z_pT_Bin_4) (135.0°), (Q2_y_Bin_13)-(z_pT_Bin_5) (120.0°)
(Q2_y_Bin_13)-(z_pT_Bin_7) (105.0°), (Q2_y_Bin_13)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_13)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_14)-(z_pT_Bin_1) (120.0°), (Q2_y_Bin_14)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_14)-(z_pT_Bin_3) (105.0°)
(Q2_y_Bin_14)-(z_pT_Bin_32) (150.0°), (Q2_y_Bin_14)-(z_pT_Bin_4) (135.0°), (Q2_y_Bin_14)-(z_pT_Bin_5) (210.0°)
(Q2_y_Bin_15)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_14) (120.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (255.0°)
(Q2_y_Bin_15)-(z_pT_Bin_19) (135.0°), (Q2_y_Bin_15)-(z_pT_Bin_2) (210.0°), (Q2_y_Bin_15)-(z_pT_Bin_21) (150.0°)
(Q2_y_Bin_15)-(z_pT_Bin_22) (210.0°), (Q2_y_Bin_15)-(z_pT_Bin_23) (210.0°), (Q2_y_Bin_15)-(z_pT_Bin_24) (285.0°)
(Q2_y_Bin_15)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_16)-(z_pT_Bin_1) (120.0°), (Q2_y_Bin_16)-(z_pT_Bin_3) (105.0°)
(Q2_y_Bin_16)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_16)-(z_pT_Bin_5) (150.0°), (Q2_y_Bin_16)-(z_pT_Bin_6) (165.0°)
(Q2_y_Bin_16)-(z_pT_Bin_9) (105.0°), (Q2_y_Bin_17)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_17)-(z_pT_Bin_4) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_1) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_11) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_12) (105.0°), (Q2_y_Bin_2)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_15) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_16) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_18) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_19) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_2) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_20) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_21) (135.0°), (Q2_y_Bin_2)-(z_pT_Bin_23) (120.0°), (Q2_y_Bin_2)-(z_pT_Bin_25) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_26) (135.0°), (Q2_y_Bin_2)-(z_pT_Bin_27) (120.0°), (Q2_y_Bin_2)-(z_pT_Bin_28) (120.0°)
(Q2_y_Bin_2)-(z_pT_Bin_29) (105.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°)
(Q2_y_Bin_2)-(z_pT_Bin_32) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_33) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_34) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_4) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_8) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_9) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_12) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_14) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_15) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_17) (165.0°)
(Q2_y_Bin_3)-(z_pT_Bin_18) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_19) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_20) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_21) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_22) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_23) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_3) (285.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_8) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_14) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_15) (330.0°), (Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_19) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_20) (120.0°)
(Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (315.0°), (Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_26) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_27) (240.0°)
(Q2_y_Bin_4)-(z_pT_Bin_28) (315.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (285.0°), (Q2_y_Bin_5)-(z_pT_Bin_10) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_11) (135.0°)
(Q2_y_Bin_5)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_15) (150.0°)
(Q2_y_Bin_5)-(z_pT_Bin_16) (120.0°), (Q2_y_Bin_5)-(z_pT_Bin_19) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (255.0°)
(Q2_y_Bin_5)-(z_pT_Bin_20) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_21) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_25) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_26) (120.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_5)-(z_pT_Bin_31) (210.0°)
(Q2_y_Bin_5)-(z_pT_Bin_32) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_33) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_4) (225.0°)
(Q2_y_Bin_5)-(z_pT_Bin_5) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_6) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_7) (240.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_9) (210.0°), (Q2_y_Bin_6)-(z_pT_Bin_1) (195.0°)
(Q2_y_Bin_6)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_11) (105.0°), (Q2_y_Bin_6)-(z_pT_Bin_13) (120.0°)
(Q2_y_Bin_6)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_15) (135.0°), (Q2_y_Bin_6)-(z_pT_Bin_16) (120.0°)
(Q2_y_Bin_6)-(z_pT_Bin_19) (135.0°), (Q2_y_Bin_6)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_20) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_25) (255.0°), (Q2_y_Bin_6)-(z_pT_Bin_26) (270.0°), (Q2_y_Bin_6)-(z_pT_Bin_27) (195.0°)
(Q2_y_Bin_6)-(z_pT_Bin_28) (195.0°), (Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_7) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_8) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_9) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_1) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°)
(Q2_y_Bin_7)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_15) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_16) (135.0°)
(Q2_y_Bin_7)-(z_pT_Bin_17) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_18) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_19) (105.0°)
(Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_20) (105.0°), (Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°)
(Q2_y_Bin_7)-(z_pT_Bin_22) (120.0°), (Q2_y_Bin_7)-(z_pT_Bin_23) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_24) (210.0°)
(Q2_y_Bin_7)-(z_pT_Bin_25) (105.0°), (Q2_y_Bin_7)-(z_pT_Bin_26) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_27) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_28) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_29) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°)
(Q2_y_Bin_7)-(z_pT_Bin_31) (255.0°), (Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°), (Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°)
(Q2_y_Bin_7)-(z_pT_Bin_34) (300.0°), (Q2_y_Bin_7)-(z_pT_Bin_35) (330.0°), (Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°)
(Q2_y_Bin_7)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_7)-(z_pT_Bin_9) (150.0°)
(Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_12) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_13) (180.0°)
(Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_16) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_18) (135.0°)
(Q2_y_Bin_8)-(z_pT_Bin_19) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_21) (135.0°)
(Q2_y_Bin_8)-(z_pT_Bin_23) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_24) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_25) (345.0°)
(Q2_y_Bin_8)-(z_pT_Bin_26) (120.0°), (Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°)
(Q2_y_Bin_8)-(z_pT_Bin_30) (330.0°), (Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_9)-(z_pT_Bin_1) (225.0°)
(Q2_y_Bin_9)-(z_pT_Bin_10) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_11) (120.0°), (Q2_y_Bin_9)-(z_pT_Bin_15) (120.0°)
(Q2_y_Bin_9)-(z_pT_Bin_16) (150.0°), (Q2_y_Bin_9)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_9)-(z_pT_Bin_22) (120.0°)
(Q2_y_Bin_9)-(z_pT_Bin_23) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_29) (195.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (180.0°)
(Q2_y_Bin_9)-(z_pT_Bin_30) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_4) (150.0°), (Q2_y_Bin_9)-(z_pT_Bin_5) (150.0°)
(Q2_y_Bin_9)-(z_pT_Bin_6) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_9) (135.0°)

Above 120° (246/452 (54.4%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (270.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_16) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_17) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (225.0°)
(Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_23) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_31) (150.0°)
(Q2_y_Bin_1)-(z_pT_Bin_32) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_4) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_5) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_6) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_10)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_10)-(z_pT_Bin_11) (135.0°), (Q2_y_Bin_10)-(z_pT_Bin_15) (135.0°), (Q2_y_Bin_10)-(z_pT_Bin_2) (150.0°)
(Q2_y_Bin_10)-(z_pT_Bin_26) (150.0°), (Q2_y_Bin_10)-(z_pT_Bin_3) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_31) (165.0°)
(Q2_y_Bin_10)-(z_pT_Bin_32) (195.0°), (Q2_y_Bin_10)-(z_pT_Bin_4) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_5) (210.0°)
(Q2_y_Bin_10)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_7) (180.0°), (Q2_y_Bin_11)-(z_pT_Bin_1) (180.0°)
(Q2_y_Bin_11)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_13) (135.0°), (Q2_y_Bin_11)-(z_pT_Bin_14) (150.0°)
(Q2_y_Bin_11)-(z_pT_Bin_15) (180.0°), (Q2_y_Bin_11)-(z_pT_Bin_18) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_19) (150.0°)
(Q2_y_Bin_11)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_11)-(z_pT_Bin_20) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_21) (240.0°)
(Q2_y_Bin_11)-(z_pT_Bin_22) (240.0°), (Q2_y_Bin_11)-(z_pT_Bin_23) (270.0°), (Q2_y_Bin_11)-(z_pT_Bin_24) (315.0°)
(Q2_y_Bin_11)-(z_pT_Bin_3) (255.0°), (Q2_y_Bin_11)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_11)-(z_pT_Bin_6) (165.0°)
(Q2_y_Bin_11)-(z_pT_Bin_9) (165.0°), (Q2_y_Bin_12)-(z_pT_Bin_11) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_14) (360.0°)
(Q2_y_Bin_12)-(z_pT_Bin_19) (285.0°), (Q2_y_Bin_12)-(z_pT_Bin_21) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_22) (345.0°)
(Q2_y_Bin_12)-(z_pT_Bin_23) (345.0°), (Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_6) (225.0°)
(Q2_y_Bin_12)-(z_pT_Bin_7) (315.0°), (Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_13)-(z_pT_Bin_1) (180.0°)
(Q2_y_Bin_13)-(z_pT_Bin_4) (135.0°), (Q2_y_Bin_14)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_14)-(z_pT_Bin_32) (150.0°)
(Q2_y_Bin_14)-(z_pT_Bin_4) (135.0°), (Q2_y_Bin_14)-(z_pT_Bin_5) (210.0°), (Q2_y_Bin_15)-(z_pT_Bin_1) (195.0°)
(Q2_y_Bin_15)-(z_pT_Bin_15) (255.0°), (Q2_y_Bin_15)-(z_pT_Bin_19) (135.0°), (Q2_y_Bin_15)-(z_pT_Bin_2) (210.0°)
(Q2_y_Bin_15)-(z_pT_Bin_21) (150.0°), (Q2_y_Bin_15)-(z_pT_Bin_22) (210.0°), (Q2_y_Bin_15)-(z_pT_Bin_23) (210.0°)
(Q2_y_Bin_15)-(z_pT_Bin_24) (285.0°), (Q2_y_Bin_15)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_16)-(z_pT_Bin_5) (150.0°)
(Q2_y_Bin_16)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_17)-(z_pT_Bin_4) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_1) (225.0°)
(Q2_y_Bin_2)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_11) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_13) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_15) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_16) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_19) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_2) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_20) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_21) (135.0°), (Q2_y_Bin_2)-(z_pT_Bin_25) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_26) (135.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_32) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_33) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_34) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_4) (225.0°)
(Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_7) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_8) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_12) (165.0°)
(Q2_y_Bin_3)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_14) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_15) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_17) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_18) (165.0°)
(Q2_y_Bin_3)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_20) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_21) (165.0°)
(Q2_y_Bin_3)-(z_pT_Bin_22) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_23) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_24) (255.0°)
(Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_3) (285.0°)
(Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_8) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_14) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_15) (330.0°)
(Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_19) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (315.0°), (Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_26) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_27) (240.0°)
(Q2_y_Bin_4)-(z_pT_Bin_28) (315.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (285.0°), (Q2_y_Bin_5)-(z_pT_Bin_10) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_11) (135.0°)
(Q2_y_Bin_5)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_15) (150.0°)
(Q2_y_Bin_5)-(z_pT_Bin_19) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (255.0°), (Q2_y_Bin_5)-(z_pT_Bin_20) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_25) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_5)-(z_pT_Bin_31) (210.0°)
(Q2_y_Bin_5)-(z_pT_Bin_32) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_4) (225.0°), (Q2_y_Bin_5)-(z_pT_Bin_5) (240.0°)
(Q2_y_Bin_5)-(z_pT_Bin_6) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_7) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (195.0°)
(Q2_y_Bin_5)-(z_pT_Bin_9) (210.0°), (Q2_y_Bin_6)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_6)-(z_pT_Bin_10) (150.0°)
(Q2_y_Bin_6)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_15) (135.0°), (Q2_y_Bin_6)-(z_pT_Bin_19) (135.0°)
(Q2_y_Bin_6)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_20) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_25) (255.0°)
(Q2_y_Bin_6)-(z_pT_Bin_26) (270.0°), (Q2_y_Bin_6)-(z_pT_Bin_27) (195.0°), (Q2_y_Bin_6)-(z_pT_Bin_28) (195.0°)
(Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_8) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_9) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_10) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_13) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_15) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_16) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_17) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_18) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°)
(Q2_y_Bin_7)-(z_pT_Bin_23) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_24) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_26) (135.0°)
(Q2_y_Bin_7)-(z_pT_Bin_27) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_28) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_29) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_31) (255.0°), (Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°)
(Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_34) (300.0°), (Q2_y_Bin_7)-(z_pT_Bin_35) (330.0°)
(Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_7)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_9) (150.0°)
(Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_12) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_13) (180.0°)
(Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_16) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_18) (135.0°)
(Q2_y_Bin_8)-(z_pT_Bin_19) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_21) (135.0°)
(Q2_y_Bin_8)-(z_pT_Bin_23) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_24) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_25) (345.0°)
(Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_30) (330.0°)
(Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_9)-(z_pT_Bin_1) (225.0°), (Q2_y_Bin_9)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_9)-(z_pT_Bin_16) (150.0°), (Q2_y_Bin_9)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_9)-(z_pT_Bin_29) (195.0°)
(Q2_y_Bin_9)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_30) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_4) (150.0°)
(Q2_y_Bin_9)-(z_pT_Bin_5) (150.0°), (Q2_y_Bin_9)-(z_pT_Bin_6) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_9) (135.0°)

Above 135° (223/452 (49.3%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (270.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_16) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°)
(Q2_y_Bin_1)-(z_pT_Bin_23) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°)
(Q2_y_Bin_1)-(z_pT_Bin_30) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_31) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_32) (165.0°)
(Q2_y_Bin_1)-(z_pT_Bin_4) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_6) (180.0°)
(Q2_y_Bin_1)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (195.0°)
(Q2_y_Bin_10)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_2) (150.0°), (Q2_y_Bin_10)-(z_pT_Bin_26) (150.0°)
(Q2_y_Bin_10)-(z_pT_Bin_3) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_31) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_32) (195.0°)
(Q2_y_Bin_10)-(z_pT_Bin_4) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_5) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_10)-(z_pT_Bin_7) (180.0°), (Q2_y_Bin_11)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_11)-(z_pT_Bin_10) (165.0°)
(Q2_y_Bin_11)-(z_pT_Bin_14) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_15) (180.0°), (Q2_y_Bin_11)-(z_pT_Bin_18) (150.0°)
(Q2_y_Bin_11)-(z_pT_Bin_19) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_11)-(z_pT_Bin_20) (210.0°)
(Q2_y_Bin_11)-(z_pT_Bin_21) (240.0°), (Q2_y_Bin_11)-(z_pT_Bin_22) (240.0°), (Q2_y_Bin_11)-(z_pT_Bin_23) (270.0°)
(Q2_y_Bin_11)-(z_pT_Bin_24) (315.0°), (Q2_y_Bin_11)-(z_pT_Bin_3) (255.0°), (Q2_y_Bin_11)-(z_pT_Bin_4) (360.0°)
(Q2_y_Bin_11)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_9) (165.0°), (Q2_y_Bin_12)-(z_pT_Bin_11) (210.0°)
(Q2_y_Bin_12)-(z_pT_Bin_14) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_19) (285.0°), (Q2_y_Bin_12)-(z_pT_Bin_21) (360.0°)
(Q2_y_Bin_12)-(z_pT_Bin_22) (345.0°), (Q2_y_Bin_12)-(z_pT_Bin_23) (345.0°), (Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°)
(Q2_y_Bin_12)-(z_pT_Bin_6) (225.0°), (Q2_y_Bin_12)-(z_pT_Bin_7) (315.0°), (Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_13)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_14)-(z_pT_Bin_32) (150.0°), (Q2_y_Bin_14)-(z_pT_Bin_5) (210.0°)
(Q2_y_Bin_15)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (255.0°), (Q2_y_Bin_15)-(z_pT_Bin_2) (210.0°)
(Q2_y_Bin_15)-(z_pT_Bin_21) (150.0°), (Q2_y_Bin_15)-(z_pT_Bin_22) (210.0°), (Q2_y_Bin_15)-(z_pT_Bin_23) (210.0°)
(Q2_y_Bin_15)-(z_pT_Bin_24) (285.0°), (Q2_y_Bin_15)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_16)-(z_pT_Bin_5) (150.0°)
(Q2_y_Bin_16)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_17)-(z_pT_Bin_4) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_1) (225.0°)
(Q2_y_Bin_2)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_11) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_13) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_15) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_16) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_19) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_2) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_20) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_25) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°)
(Q2_y_Bin_2)-(z_pT_Bin_32) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_33) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_34) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_4) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_8) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_9) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_12) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_14) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_15) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_17) (165.0°)
(Q2_y_Bin_3)-(z_pT_Bin_18) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_20) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_21) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_22) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_23) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_3) (285.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_8) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_9) (180.0°)
(Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_14) (150.0°)
(Q2_y_Bin_4)-(z_pT_Bin_15) (330.0°), (Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_19) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (315.0°)
(Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_26) (150.0°)
(Q2_y_Bin_4)-(z_pT_Bin_27) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_28) (315.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (285.0°), (Q2_y_Bin_5)-(z_pT_Bin_10) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_15) (150.0°)
(Q2_y_Bin_5)-(z_pT_Bin_19) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (255.0°), (Q2_y_Bin_5)-(z_pT_Bin_20) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_25) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_5)-(z_pT_Bin_31) (210.0°)
(Q2_y_Bin_5)-(z_pT_Bin_32) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_4) (225.0°), (Q2_y_Bin_5)-(z_pT_Bin_5) (240.0°)
(Q2_y_Bin_5)-(z_pT_Bin_6) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_7) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (195.0°)
(Q2_y_Bin_5)-(z_pT_Bin_9) (210.0°), (Q2_y_Bin_6)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_6)-(z_pT_Bin_10) (150.0°)
(Q2_y_Bin_6)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_20) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_25) (255.0°), (Q2_y_Bin_6)-(z_pT_Bin_26) (270.0°), (Q2_y_Bin_6)-(z_pT_Bin_27) (195.0°)
(Q2_y_Bin_6)-(z_pT_Bin_28) (195.0°), (Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_7) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_8) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_9) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_1) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°)
(Q2_y_Bin_7)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_15) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_17) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_18) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°)
(Q2_y_Bin_7)-(z_pT_Bin_23) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_24) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_27) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_28) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_29) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°)
(Q2_y_Bin_7)-(z_pT_Bin_31) (255.0°), (Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°), (Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°)
(Q2_y_Bin_7)-(z_pT_Bin_34) (300.0°), (Q2_y_Bin_7)-(z_pT_Bin_35) (330.0°), (Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°)
(Q2_y_Bin_7)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_9) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°)
(Q2_y_Bin_8)-(z_pT_Bin_13) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_16) (195.0°)
(Q2_y_Bin_8)-(z_pT_Bin_19) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_23) (150.0°)
(Q2_y_Bin_8)-(z_pT_Bin_24) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_25) (345.0°), (Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°)
(Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_30) (330.0°), (Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_9)-(z_pT_Bin_1) (225.0°), (Q2_y_Bin_9)-(z_pT_Bin_16) (150.0°), (Q2_y_Bin_9)-(z_pT_Bin_2) (165.0°)
(Q2_y_Bin_9)-(z_pT_Bin_29) (195.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_4) (150.0°)
(Q2_y_Bin_9)-(z_pT_Bin_5) (150.0°)

Above 150° (192/452 (42.5%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (270.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_16) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°)
(Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (210.0°)
(Q2_y_Bin_1)-(z_pT_Bin_32) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_4) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_5) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_6) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_10)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_3) (165.0°)
(Q2_y_Bin_10)-(z_pT_Bin_31) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_32) (195.0°), (Q2_y_Bin_10)-(z_pT_Bin_4) (165.0°)
(Q2_y_Bin_10)-(z_pT_Bin_5) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_7) (180.0°)
(Q2_y_Bin_11)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_11)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_15) (180.0°)
(Q2_y_Bin_11)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_11)-(z_pT_Bin_20) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_21) (240.0°)
(Q2_y_Bin_11)-(z_pT_Bin_22) (240.0°), (Q2_y_Bin_11)-(z_pT_Bin_23) (270.0°), (Q2_y_Bin_11)-(z_pT_Bin_24) (315.0°)
(Q2_y_Bin_11)-(z_pT_Bin_3) (255.0°), (Q2_y_Bin_11)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_11)-(z_pT_Bin_6) (165.0°)
(Q2_y_Bin_11)-(z_pT_Bin_9) (165.0°), (Q2_y_Bin_12)-(z_pT_Bin_11) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_14) (360.0°)
(Q2_y_Bin_12)-(z_pT_Bin_19) (285.0°), (Q2_y_Bin_12)-(z_pT_Bin_21) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_22) (345.0°)
(Q2_y_Bin_12)-(z_pT_Bin_23) (345.0°), (Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_6) (225.0°)
(Q2_y_Bin_12)-(z_pT_Bin_7) (315.0°), (Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_13)-(z_pT_Bin_1) (180.0°)
(Q2_y_Bin_14)-(z_pT_Bin_5) (210.0°), (Q2_y_Bin_15)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (255.0°)
(Q2_y_Bin_15)-(z_pT_Bin_2) (210.0°), (Q2_y_Bin_15)-(z_pT_Bin_22) (210.0°), (Q2_y_Bin_15)-(z_pT_Bin_23) (210.0°)
(Q2_y_Bin_15)-(z_pT_Bin_24) (285.0°), (Q2_y_Bin_15)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_16)-(z_pT_Bin_6) (165.0°)
(Q2_y_Bin_17)-(z_pT_Bin_4) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_1) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_10) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_15) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_19) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_2) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_20) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_25) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°)
(Q2_y_Bin_2)-(z_pT_Bin_32) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_33) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_34) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_4) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_8) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_9) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_12) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_15) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_17) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_18) (165.0°)
(Q2_y_Bin_3)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_20) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_21) (165.0°)
(Q2_y_Bin_3)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_3) (285.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_15) (330.0°), (Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_19) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_22) (315.0°), (Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°)
(Q2_y_Bin_4)-(z_pT_Bin_27) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_28) (315.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (285.0°), (Q2_y_Bin_5)-(z_pT_Bin_10) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_19) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_2) (255.0°), (Q2_y_Bin_5)-(z_pT_Bin_20) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_25) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_5)-(z_pT_Bin_31) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_32) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_4) (225.0°), (Q2_y_Bin_5)-(z_pT_Bin_5) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_6) (195.0°)
(Q2_y_Bin_5)-(z_pT_Bin_7) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_9) (210.0°)
(Q2_y_Bin_6)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_6)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_2) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_20) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_25) (255.0°), (Q2_y_Bin_6)-(z_pT_Bin_26) (270.0°)
(Q2_y_Bin_6)-(z_pT_Bin_27) (195.0°), (Q2_y_Bin_6)-(z_pT_Bin_28) (195.0°), (Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_6) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_8) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_9) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°)
(Q2_y_Bin_7)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_18) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_24) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_29) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_31) (255.0°), (Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°)
(Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_34) (300.0°), (Q2_y_Bin_7)-(z_pT_Bin_35) (330.0°)
(Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_7)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°)
(Q2_y_Bin_8)-(z_pT_Bin_13) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_16) (195.0°)
(Q2_y_Bin_8)-(z_pT_Bin_19) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_24) (240.0°)
(Q2_y_Bin_8)-(z_pT_Bin_25) (345.0°), (Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°)
(Q2_y_Bin_8)-(z_pT_Bin_30) (330.0°), (Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_9)-(z_pT_Bin_1) (225.0°)
(Q2_y_Bin_9)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_9)-(z_pT_Bin_29) (195.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (180.0°)

Above 180° (124/452 (27.4%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (270.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_2) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°)
(Q2_y_Bin_1)-(z_pT_Bin_30) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_4) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_5) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_8) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_10)-(z_pT_Bin_32) (195.0°)
(Q2_y_Bin_10)-(z_pT_Bin_5) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_11)-(z_pT_Bin_20) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_21) (240.0°), (Q2_y_Bin_11)-(z_pT_Bin_22) (240.0°)
(Q2_y_Bin_11)-(z_pT_Bin_23) (270.0°), (Q2_y_Bin_11)-(z_pT_Bin_24) (315.0°), (Q2_y_Bin_11)-(z_pT_Bin_3) (255.0°)
(Q2_y_Bin_11)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_11) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_14) (360.0°)
(Q2_y_Bin_12)-(z_pT_Bin_19) (285.0°), (Q2_y_Bin_12)-(z_pT_Bin_21) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_22) (345.0°)
(Q2_y_Bin_12)-(z_pT_Bin_23) (345.0°), (Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_6) (225.0°)
(Q2_y_Bin_12)-(z_pT_Bin_7) (315.0°), (Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_14)-(z_pT_Bin_5) (210.0°)
(Q2_y_Bin_15)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (255.0°), (Q2_y_Bin_15)-(z_pT_Bin_2) (210.0°)
(Q2_y_Bin_15)-(z_pT_Bin_22) (210.0°), (Q2_y_Bin_15)-(z_pT_Bin_23) (210.0°), (Q2_y_Bin_15)-(z_pT_Bin_24) (285.0°)
(Q2_y_Bin_2)-(z_pT_Bin_1) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_2) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_4) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_9) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_3) (285.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_15) (330.0°), (Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_19) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (315.0°)
(Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_27) (240.0°)
(Q2_y_Bin_4)-(z_pT_Bin_28) (315.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (285.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (255.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (225.0°)
(Q2_y_Bin_5)-(z_pT_Bin_31) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_4) (225.0°), (Q2_y_Bin_5)-(z_pT_Bin_5) (240.0°)
(Q2_y_Bin_5)-(z_pT_Bin_6) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_7) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (195.0°)
(Q2_y_Bin_5)-(z_pT_Bin_9) (210.0°), (Q2_y_Bin_6)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_6)-(z_pT_Bin_25) (255.0°)
(Q2_y_Bin_6)-(z_pT_Bin_26) (270.0°), (Q2_y_Bin_6)-(z_pT_Bin_27) (195.0°), (Q2_y_Bin_6)-(z_pT_Bin_28) (195.0°)
(Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_24) (210.0°)
(Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_31) (255.0°), (Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°)
(Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_34) (300.0°), (Q2_y_Bin_7)-(z_pT_Bin_35) (330.0°)
(Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_16) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_19) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_24) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_25) (345.0°), (Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°)
(Q2_y_Bin_8)-(z_pT_Bin_30) (330.0°), (Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_9)-(z_pT_Bin_1) (225.0°)
(Q2_y_Bin_9)-(z_pT_Bin_29) (195.0°)

### sector / P1

Stage: spline, acceptance. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/pion_sector/pipS1o/fit_copy.root`

Above 90° (271/452 (60.0%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (270.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_11) (105.0°)
(Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_16) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_17) (105.0°)
(Q2_y_Bin_1)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_23) (120.0°)
(Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_31) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_32) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_4) (225.0°)
(Q2_y_Bin_1)-(z_pT_Bin_5) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_6) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_7) (150.0°)
(Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_1) (150.0°)
(Q2_y_Bin_10)-(z_pT_Bin_10) (120.0°), (Q2_y_Bin_10)-(z_pT_Bin_15) (105.0°), (Q2_y_Bin_10)-(z_pT_Bin_2) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_20) (105.0°), (Q2_y_Bin_10)-(z_pT_Bin_26) (105.0°), (Q2_y_Bin_10)-(z_pT_Bin_3) (150.0°)
(Q2_y_Bin_10)-(z_pT_Bin_31) (120.0°), (Q2_y_Bin_10)-(z_pT_Bin_32) (135.0°), (Q2_y_Bin_10)-(z_pT_Bin_4) (165.0°)
(Q2_y_Bin_10)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_6) (195.0°), (Q2_y_Bin_10)-(z_pT_Bin_7) (150.0°)
(Q2_y_Bin_10)-(z_pT_Bin_9) (120.0°), (Q2_y_Bin_11)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_10) (120.0°)
(Q2_y_Bin_11)-(z_pT_Bin_13) (105.0°), (Q2_y_Bin_11)-(z_pT_Bin_15) (105.0°), (Q2_y_Bin_11)-(z_pT_Bin_18) (105.0°)
(Q2_y_Bin_11)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_20) (135.0°), (Q2_y_Bin_11)-(z_pT_Bin_21) (150.0°)
(Q2_y_Bin_11)-(z_pT_Bin_22) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_23) (180.0°), (Q2_y_Bin_11)-(z_pT_Bin_24) (255.0°)
(Q2_y_Bin_11)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_4) (270.0°), (Q2_y_Bin_11)-(z_pT_Bin_6) (150.0°)
(Q2_y_Bin_11)-(z_pT_Bin_9) (105.0°), (Q2_y_Bin_12)-(z_pT_Bin_11) (165.0°), (Q2_y_Bin_12)-(z_pT_Bin_13) (105.0°)
(Q2_y_Bin_12)-(z_pT_Bin_14) (270.0°), (Q2_y_Bin_12)-(z_pT_Bin_16) (105.0°), (Q2_y_Bin_12)-(z_pT_Bin_18) (120.0°)
(Q2_y_Bin_12)-(z_pT_Bin_19) (255.0°), (Q2_y_Bin_12)-(z_pT_Bin_21) (315.0°), (Q2_y_Bin_12)-(z_pT_Bin_22) (165.0°)
(Q2_y_Bin_12)-(z_pT_Bin_23) (255.0°), (Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_13)-(z_pT_Bin_1) (180.0°)
(Q2_y_Bin_13)-(z_pT_Bin_12) (105.0°), (Q2_y_Bin_13)-(z_pT_Bin_2) (150.0°), (Q2_y_Bin_13)-(z_pT_Bin_26) (105.0°)
(Q2_y_Bin_13)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_13)-(z_pT_Bin_4) (135.0°), (Q2_y_Bin_13)-(z_pT_Bin_5) (105.0°)
(Q2_y_Bin_13)-(z_pT_Bin_7) (105.0°), (Q2_y_Bin_13)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_13)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_14)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_14)-(z_pT_Bin_2) (150.0°), (Q2_y_Bin_14)-(z_pT_Bin_4) (105.0°)
(Q2_y_Bin_14)-(z_pT_Bin_5) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (180.0°)
(Q2_y_Bin_15)-(z_pT_Bin_19) (105.0°), (Q2_y_Bin_15)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_22) (120.0°)
(Q2_y_Bin_15)-(z_pT_Bin_23) (150.0°), (Q2_y_Bin_15)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_15)-(z_pT_Bin_9) (120.0°)
(Q2_y_Bin_16)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_16)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_16)-(z_pT_Bin_6) (150.0°)
(Q2_y_Bin_16)-(z_pT_Bin_9) (105.0°), (Q2_y_Bin_17)-(z_pT_Bin_4) (105.0°), (Q2_y_Bin_2)-(z_pT_Bin_1) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_11) (135.0°), (Q2_y_Bin_2)-(z_pT_Bin_13) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_15) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_16) (135.0°)
(Q2_y_Bin_2)-(z_pT_Bin_19) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_20) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_21) (120.0°), (Q2_y_Bin_2)-(z_pT_Bin_25) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_26) (135.0°)
(Q2_y_Bin_2)-(z_pT_Bin_27) (105.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°)
(Q2_y_Bin_2)-(z_pT_Bin_32) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_33) (135.0°), (Q2_y_Bin_2)-(z_pT_Bin_34) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_4) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_8) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_9) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_12) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_14) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_15) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_17) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_18) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_19) (135.0°), (Q2_y_Bin_3)-(z_pT_Bin_2) (240.0°)
(Q2_y_Bin_3)-(z_pT_Bin_20) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_21) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_22) (135.0°)
(Q2_y_Bin_3)-(z_pT_Bin_23) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_8) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_14) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_15) (330.0°), (Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_19) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_20) (120.0°)
(Q2_y_Bin_4)-(z_pT_Bin_21) (195.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (300.0°), (Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_26) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_27) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_28) (285.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_13) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_14) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_15) (135.0°), (Q2_y_Bin_5)-(z_pT_Bin_19) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_2) (255.0°), (Q2_y_Bin_5)-(z_pT_Bin_20) (135.0°), (Q2_y_Bin_5)-(z_pT_Bin_25) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_26) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_31) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_32) (135.0°), (Q2_y_Bin_5)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_5) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_7) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_10) (120.0°)
(Q2_y_Bin_6)-(z_pT_Bin_11) (105.0°), (Q2_y_Bin_6)-(z_pT_Bin_13) (120.0°), (Q2_y_Bin_6)-(z_pT_Bin_14) (120.0°)
(Q2_y_Bin_6)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_6)-(z_pT_Bin_19) (120.0°), (Q2_y_Bin_6)-(z_pT_Bin_2) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_20) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_25) (210.0°), (Q2_y_Bin_6)-(z_pT_Bin_26) (225.0°)
(Q2_y_Bin_6)-(z_pT_Bin_27) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_28) (135.0°), (Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_6) (150.0°)
(Q2_y_Bin_6)-(z_pT_Bin_7) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_8) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_9) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_15) (120.0°)
(Q2_y_Bin_7)-(z_pT_Bin_16) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_17) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_18) (120.0°)
(Q2_y_Bin_7)-(z_pT_Bin_19) (120.0°), (Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_20) (120.0°)
(Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_22) (120.0°), (Q2_y_Bin_7)-(z_pT_Bin_23) (105.0°)
(Q2_y_Bin_7)-(z_pT_Bin_24) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_26) (120.0°), (Q2_y_Bin_7)-(z_pT_Bin_27) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_28) (120.0°), (Q2_y_Bin_7)-(z_pT_Bin_29) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°)
(Q2_y_Bin_7)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°), (Q2_y_Bin_7)-(z_pT_Bin_33) (255.0°)
(Q2_y_Bin_7)-(z_pT_Bin_34) (255.0°), (Q2_y_Bin_7)-(z_pT_Bin_35) (300.0°), (Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°)
(Q2_y_Bin_7)-(z_pT_Bin_7) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_7)-(z_pT_Bin_9) (135.0°)
(Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_12) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_13) (165.0°)
(Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_16) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_18) (135.0°)
(Q2_y_Bin_8)-(z_pT_Bin_19) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_21) (135.0°)
(Q2_y_Bin_8)-(z_pT_Bin_23) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_24) (225.0°), (Q2_y_Bin_8)-(z_pT_Bin_25) (330.0°)
(Q2_y_Bin_8)-(z_pT_Bin_26) (120.0°), (Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°)
(Q2_y_Bin_8)-(z_pT_Bin_30) (315.0°), (Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_9)-(z_pT_Bin_1) (225.0°)
(Q2_y_Bin_9)-(z_pT_Bin_10) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_11) (120.0°), (Q2_y_Bin_9)-(z_pT_Bin_15) (120.0°)
(Q2_y_Bin_9)-(z_pT_Bin_16) (120.0°), (Q2_y_Bin_9)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_22) (120.0°)
(Q2_y_Bin_9)-(z_pT_Bin_29) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_4) (150.0°)
(Q2_y_Bin_9)-(z_pT_Bin_5) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_6) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_8) (120.0°)
(Q2_y_Bin_9)-(z_pT_Bin_9) (135.0°)

Above 120° (210/452 (46.5%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (270.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_16) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°)
(Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_4) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_5) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_6) (180.0°)
(Q2_y_Bin_1)-(z_pT_Bin_7) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (210.0°)
(Q2_y_Bin_10)-(z_pT_Bin_1) (150.0°), (Q2_y_Bin_10)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_3) (150.0°)
(Q2_y_Bin_10)-(z_pT_Bin_32) (135.0°), (Q2_y_Bin_10)-(z_pT_Bin_4) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_5) (165.0°)
(Q2_y_Bin_10)-(z_pT_Bin_6) (195.0°), (Q2_y_Bin_10)-(z_pT_Bin_7) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_1) (165.0°)
(Q2_y_Bin_11)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_20) (135.0°), (Q2_y_Bin_11)-(z_pT_Bin_21) (150.0°)
(Q2_y_Bin_11)-(z_pT_Bin_22) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_23) (180.0°), (Q2_y_Bin_11)-(z_pT_Bin_24) (255.0°)
(Q2_y_Bin_11)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_4) (270.0°), (Q2_y_Bin_11)-(z_pT_Bin_6) (150.0°)
(Q2_y_Bin_12)-(z_pT_Bin_11) (165.0°), (Q2_y_Bin_12)-(z_pT_Bin_14) (270.0°), (Q2_y_Bin_12)-(z_pT_Bin_19) (255.0°)
(Q2_y_Bin_12)-(z_pT_Bin_21) (315.0°), (Q2_y_Bin_12)-(z_pT_Bin_22) (165.0°), (Q2_y_Bin_12)-(z_pT_Bin_23) (255.0°)
(Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°)
(Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_13)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_13)-(z_pT_Bin_2) (150.0°)
(Q2_y_Bin_13)-(z_pT_Bin_4) (135.0°), (Q2_y_Bin_14)-(z_pT_Bin_2) (150.0°), (Q2_y_Bin_14)-(z_pT_Bin_5) (180.0°)
(Q2_y_Bin_15)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_2) (180.0°)
(Q2_y_Bin_15)-(z_pT_Bin_23) (150.0°), (Q2_y_Bin_15)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_16)-(z_pT_Bin_6) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_1) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_11) (135.0°)
(Q2_y_Bin_2)-(z_pT_Bin_13) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_15) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_16) (135.0°), (Q2_y_Bin_2)-(z_pT_Bin_19) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_2) (240.0°)
(Q2_y_Bin_2)-(z_pT_Bin_20) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_25) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_26) (135.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_32) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_33) (135.0°), (Q2_y_Bin_2)-(z_pT_Bin_34) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_4) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°)
(Q2_y_Bin_2)-(z_pT_Bin_8) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_12) (165.0°)
(Q2_y_Bin_3)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_14) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_15) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_17) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_18) (165.0°)
(Q2_y_Bin_3)-(z_pT_Bin_19) (135.0°), (Q2_y_Bin_3)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_3)-(z_pT_Bin_20) (165.0°)
(Q2_y_Bin_3)-(z_pT_Bin_21) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_22) (135.0°), (Q2_y_Bin_3)-(z_pT_Bin_23) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_9) (195.0°)
(Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_14) (150.0°)
(Q2_y_Bin_4)-(z_pT_Bin_15) (330.0°), (Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_19) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_21) (195.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (300.0°)
(Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_26) (150.0°)
(Q2_y_Bin_4)-(z_pT_Bin_27) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_28) (285.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_10) (150.0°)
(Q2_y_Bin_5)-(z_pT_Bin_13) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_14) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_15) (135.0°)
(Q2_y_Bin_5)-(z_pT_Bin_19) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (255.0°), (Q2_y_Bin_5)-(z_pT_Bin_20) (135.0°)
(Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_31) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_32) (135.0°)
(Q2_y_Bin_5)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_5) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_6) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_7) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_9) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_20) (150.0°)
(Q2_y_Bin_6)-(z_pT_Bin_25) (210.0°), (Q2_y_Bin_6)-(z_pT_Bin_26) (225.0°), (Q2_y_Bin_6)-(z_pT_Bin_27) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_28) (135.0°), (Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_6) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_7) (150.0°)
(Q2_y_Bin_6)-(z_pT_Bin_8) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_9) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_1) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°)
(Q2_y_Bin_7)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_16) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_17) (135.0°)
(Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_24) (180.0°)
(Q2_y_Bin_7)-(z_pT_Bin_27) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_29) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°)
(Q2_y_Bin_7)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°), (Q2_y_Bin_7)-(z_pT_Bin_33) (255.0°)
(Q2_y_Bin_7)-(z_pT_Bin_34) (255.0°), (Q2_y_Bin_7)-(z_pT_Bin_35) (300.0°), (Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°)
(Q2_y_Bin_7)-(z_pT_Bin_7) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_9) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°)
(Q2_y_Bin_8)-(z_pT_Bin_12) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_16) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_18) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_19) (210.0°)
(Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_21) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_23) (135.0°)
(Q2_y_Bin_8)-(z_pT_Bin_24) (225.0°), (Q2_y_Bin_8)-(z_pT_Bin_25) (330.0°), (Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°)
(Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_30) (315.0°), (Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_9)-(z_pT_Bin_1) (225.0°), (Q2_y_Bin_9)-(z_pT_Bin_10) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_2) (180.0°)
(Q2_y_Bin_9)-(z_pT_Bin_29) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_4) (150.0°)
(Q2_y_Bin_9)-(z_pT_Bin_5) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_6) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_9) (135.0°)

Above 135° (185/452 (40.9%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (270.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_16) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°)
(Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_4) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_5) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_6) (180.0°)
(Q2_y_Bin_1)-(z_pT_Bin_7) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (210.0°)
(Q2_y_Bin_10)-(z_pT_Bin_1) (150.0°), (Q2_y_Bin_10)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_3) (150.0°)
(Q2_y_Bin_10)-(z_pT_Bin_4) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_6) (195.0°)
(Q2_y_Bin_10)-(z_pT_Bin_7) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_2) (165.0°)
(Q2_y_Bin_11)-(z_pT_Bin_21) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_22) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_23) (180.0°)
(Q2_y_Bin_11)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_11)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_4) (270.0°)
(Q2_y_Bin_11)-(z_pT_Bin_6) (150.0°), (Q2_y_Bin_12)-(z_pT_Bin_11) (165.0°), (Q2_y_Bin_12)-(z_pT_Bin_14) (270.0°)
(Q2_y_Bin_12)-(z_pT_Bin_19) (255.0°), (Q2_y_Bin_12)-(z_pT_Bin_21) (315.0°), (Q2_y_Bin_12)-(z_pT_Bin_22) (165.0°)
(Q2_y_Bin_12)-(z_pT_Bin_23) (255.0°), (Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_13)-(z_pT_Bin_1) (180.0°)
(Q2_y_Bin_13)-(z_pT_Bin_2) (150.0°), (Q2_y_Bin_14)-(z_pT_Bin_2) (150.0°), (Q2_y_Bin_14)-(z_pT_Bin_5) (180.0°)
(Q2_y_Bin_15)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_2) (180.0°)
(Q2_y_Bin_15)-(z_pT_Bin_23) (150.0°), (Q2_y_Bin_15)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_16)-(z_pT_Bin_6) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_1) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_13) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_15) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_19) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_20) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_25) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_32) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_34) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_4) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_8) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°)
(Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_12) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_13) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_14) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_15) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_16) (165.0°)
(Q2_y_Bin_3)-(z_pT_Bin_17) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_18) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_2) (240.0°)
(Q2_y_Bin_3)-(z_pT_Bin_20) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_21) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_23) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_9) (195.0°)
(Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_14) (150.0°)
(Q2_y_Bin_4)-(z_pT_Bin_15) (330.0°), (Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_19) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_21) (195.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (300.0°)
(Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_26) (150.0°)
(Q2_y_Bin_4)-(z_pT_Bin_27) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_28) (285.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_10) (150.0°)
(Q2_y_Bin_5)-(z_pT_Bin_13) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_14) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_19) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_2) (255.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_31) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_5) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_6) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_7) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_9) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_20) (150.0°)
(Q2_y_Bin_6)-(z_pT_Bin_25) (210.0°), (Q2_y_Bin_6)-(z_pT_Bin_26) (225.0°), (Q2_y_Bin_6)-(z_pT_Bin_27) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_6) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_7) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_8) (150.0°)
(Q2_y_Bin_6)-(z_pT_Bin_9) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_10) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_13) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_24) (180.0°)
(Q2_y_Bin_7)-(z_pT_Bin_27) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_29) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°)
(Q2_y_Bin_7)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°), (Q2_y_Bin_7)-(z_pT_Bin_33) (255.0°)
(Q2_y_Bin_7)-(z_pT_Bin_34) (255.0°), (Q2_y_Bin_7)-(z_pT_Bin_35) (300.0°), (Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°)
(Q2_y_Bin_7)-(z_pT_Bin_7) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_13) (165.0°)
(Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_16) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_19) (210.0°)
(Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_24) (225.0°), (Q2_y_Bin_8)-(z_pT_Bin_25) (330.0°)
(Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_30) (315.0°)
(Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_9)-(z_pT_Bin_1) (225.0°), (Q2_y_Bin_9)-(z_pT_Bin_2) (180.0°)
(Q2_y_Bin_9)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_4) (150.0°)

Above 150° (158/452 (35.0%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (270.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_16) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°)
(Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_4) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_5) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_6) (180.0°)
(Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_2) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_4) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_6) (195.0°)
(Q2_y_Bin_11)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_22) (210.0°)
(Q2_y_Bin_11)-(z_pT_Bin_23) (180.0°), (Q2_y_Bin_11)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_11)-(z_pT_Bin_3) (225.0°)
(Q2_y_Bin_11)-(z_pT_Bin_4) (270.0°), (Q2_y_Bin_12)-(z_pT_Bin_11) (165.0°), (Q2_y_Bin_12)-(z_pT_Bin_14) (270.0°)
(Q2_y_Bin_12)-(z_pT_Bin_19) (255.0°), (Q2_y_Bin_12)-(z_pT_Bin_21) (315.0°), (Q2_y_Bin_12)-(z_pT_Bin_22) (165.0°)
(Q2_y_Bin_12)-(z_pT_Bin_23) (255.0°), (Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_13)-(z_pT_Bin_1) (180.0°)
(Q2_y_Bin_14)-(z_pT_Bin_5) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (180.0°)
(Q2_y_Bin_15)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_2)-(z_pT_Bin_1) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_13) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_15) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_19) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_2) (240.0°)
(Q2_y_Bin_2)-(z_pT_Bin_20) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_25) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_32) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_4) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°)
(Q2_y_Bin_2)-(z_pT_Bin_8) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_12) (165.0°)
(Q2_y_Bin_3)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_15) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_16) (165.0°)
(Q2_y_Bin_3)-(z_pT_Bin_18) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_3)-(z_pT_Bin_20) (165.0°)
(Q2_y_Bin_3)-(z_pT_Bin_21) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_8) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_15) (330.0°), (Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_19) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_21) (195.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (300.0°)
(Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_27) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_28) (285.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_13) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_19) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_2) (255.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_31) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_5) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_6) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_7) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_9) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_25) (210.0°)
(Q2_y_Bin_6)-(z_pT_Bin_26) (225.0°), (Q2_y_Bin_6)-(z_pT_Bin_27) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_9) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°)
(Q2_y_Bin_7)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°)
(Q2_y_Bin_7)-(z_pT_Bin_24) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_31) (240.0°)
(Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°), (Q2_y_Bin_7)-(z_pT_Bin_33) (255.0°), (Q2_y_Bin_7)-(z_pT_Bin_34) (255.0°)
(Q2_y_Bin_7)-(z_pT_Bin_35) (300.0°), (Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°)
(Q2_y_Bin_8)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_16) (195.0°)
(Q2_y_Bin_8)-(z_pT_Bin_19) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_24) (225.0°)
(Q2_y_Bin_8)-(z_pT_Bin_25) (330.0°), (Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°)
(Q2_y_Bin_8)-(z_pT_Bin_30) (315.0°), (Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_9)-(z_pT_Bin_1) (225.0°)
(Q2_y_Bin_9)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (180.0°)

Above 180° (99/452 (21.9%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (270.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (240.0°)
(Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_4) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (210.0°)
(Q2_y_Bin_10)-(z_pT_Bin_6) (195.0°), (Q2_y_Bin_11)-(z_pT_Bin_22) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_24) (255.0°)
(Q2_y_Bin_11)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_4) (270.0°), (Q2_y_Bin_12)-(z_pT_Bin_14) (270.0°)
(Q2_y_Bin_12)-(z_pT_Bin_19) (255.0°), (Q2_y_Bin_12)-(z_pT_Bin_21) (315.0°), (Q2_y_Bin_12)-(z_pT_Bin_23) (255.0°)
(Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°)
(Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_15)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_2)-(z_pT_Bin_1) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°)
(Q2_y_Bin_2)-(z_pT_Bin_4) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°), (Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°)
(Q2_y_Bin_3)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_3)-(z_pT_Bin_24) (255.0°)
(Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_3) (270.0°)
(Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_15) (330.0°), (Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_19) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_21) (195.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (300.0°)
(Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_27) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_28) (285.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (255.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°)
(Q2_y_Bin_5)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_7) (240.0°), (Q2_y_Bin_6)-(z_pT_Bin_25) (210.0°)
(Q2_y_Bin_6)-(z_pT_Bin_26) (225.0°), (Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°)
(Q2_y_Bin_7)-(z_pT_Bin_33) (255.0°), (Q2_y_Bin_7)-(z_pT_Bin_34) (255.0°), (Q2_y_Bin_7)-(z_pT_Bin_35) (300.0°)
(Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_16) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_19) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_24) (225.0°), (Q2_y_Bin_8)-(z_pT_Bin_25) (330.0°), (Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°)
(Q2_y_Bin_8)-(z_pT_Bin_30) (315.0°), (Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_9)-(z_pT_Bin_1) (225.0°)

### sector / E2

Stage: spline, acceptance. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/electron_sector/eS2o/fit_copy.root`

Above 90° (286/452 (63.3%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_11) (120.0°)
(Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_16) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_17) (120.0°)
(Q2_y_Bin_1)-(z_pT_Bin_2) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_23) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_31) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_32) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_4) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_5) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_7) (150.0°)
(Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_10)-(z_pT_Bin_1) (150.0°)
(Q2_y_Bin_10)-(z_pT_Bin_10) (120.0°), (Q2_y_Bin_10)-(z_pT_Bin_11) (105.0°), (Q2_y_Bin_10)-(z_pT_Bin_13) (120.0°)
(Q2_y_Bin_10)-(z_pT_Bin_14) (105.0°), (Q2_y_Bin_10)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_10)-(z_pT_Bin_19) (105.0°)
(Q2_y_Bin_10)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_20) (120.0°), (Q2_y_Bin_10)-(z_pT_Bin_26) (135.0°)
(Q2_y_Bin_10)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_31) (150.0°), (Q2_y_Bin_10)-(z_pT_Bin_32) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_10)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_5) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_7) (150.0°), (Q2_y_Bin_10)-(z_pT_Bin_8) (120.0°)
(Q2_y_Bin_10)-(z_pT_Bin_9) (135.0°), (Q2_y_Bin_11)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_11)-(z_pT_Bin_11) (105.0°), (Q2_y_Bin_11)-(z_pT_Bin_13) (105.0°), (Q2_y_Bin_11)-(z_pT_Bin_18) (105.0°)
(Q2_y_Bin_11)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_20) (135.0°), (Q2_y_Bin_11)-(z_pT_Bin_21) (150.0°)
(Q2_y_Bin_11)-(z_pT_Bin_22) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_23) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_24) (225.0°)
(Q2_y_Bin_11)-(z_pT_Bin_3) (195.0°), (Q2_y_Bin_11)-(z_pT_Bin_4) (330.0°), (Q2_y_Bin_11)-(z_pT_Bin_6) (165.0°)
(Q2_y_Bin_11)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_11)-(z_pT_Bin_9) (120.0°), (Q2_y_Bin_12)-(z_pT_Bin_11) (195.0°)
(Q2_y_Bin_12)-(z_pT_Bin_13) (120.0°), (Q2_y_Bin_12)-(z_pT_Bin_14) (270.0°), (Q2_y_Bin_12)-(z_pT_Bin_16) (135.0°)
(Q2_y_Bin_12)-(z_pT_Bin_18) (120.0°), (Q2_y_Bin_12)-(z_pT_Bin_19) (255.0°), (Q2_y_Bin_12)-(z_pT_Bin_21) (360.0°)
(Q2_y_Bin_12)-(z_pT_Bin_22) (195.0°), (Q2_y_Bin_12)-(z_pT_Bin_23) (240.0°), (Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°)
(Q2_y_Bin_12)-(z_pT_Bin_6) (225.0°), (Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_13)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_13)-(z_pT_Bin_12) (105.0°), (Q2_y_Bin_13)-(z_pT_Bin_2) (150.0°)
(Q2_y_Bin_13)-(z_pT_Bin_26) (120.0°), (Q2_y_Bin_13)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_13)-(z_pT_Bin_4) (135.0°)
(Q2_y_Bin_13)-(z_pT_Bin_5) (105.0°), (Q2_y_Bin_13)-(z_pT_Bin_7) (105.0°), (Q2_y_Bin_13)-(z_pT_Bin_8) (105.0°)
(Q2_y_Bin_14)-(z_pT_Bin_1) (120.0°), (Q2_y_Bin_14)-(z_pT_Bin_2) (150.0°), (Q2_y_Bin_14)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_14)-(z_pT_Bin_32) (135.0°), (Q2_y_Bin_14)-(z_pT_Bin_4) (150.0°), (Q2_y_Bin_14)-(z_pT_Bin_5) (195.0°)
(Q2_y_Bin_15)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (225.0°), (Q2_y_Bin_15)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_15)-(z_pT_Bin_21) (135.0°), (Q2_y_Bin_15)-(z_pT_Bin_22) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_23) (180.0°)
(Q2_y_Bin_15)-(z_pT_Bin_24) (270.0°), (Q2_y_Bin_15)-(z_pT_Bin_6) (135.0°), (Q2_y_Bin_15)-(z_pT_Bin_9) (150.0°)
(Q2_y_Bin_16)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_16)-(z_pT_Bin_4) (105.0°), (Q2_y_Bin_16)-(z_pT_Bin_5) (120.0°)
(Q2_y_Bin_16)-(z_pT_Bin_6) (150.0°), (Q2_y_Bin_17)-(z_pT_Bin_1) (120.0°), (Q2_y_Bin_17)-(z_pT_Bin_4) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_1) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_10) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_11) (135.0°)
(Q2_y_Bin_2)-(z_pT_Bin_12) (105.0°), (Q2_y_Bin_2)-(z_pT_Bin_13) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_15) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_16) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_19) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_2) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_20) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_21) (120.0°)
(Q2_y_Bin_2)-(z_pT_Bin_25) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_26) (135.0°), (Q2_y_Bin_2)-(z_pT_Bin_27) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_28) (120.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°)
(Q2_y_Bin_2)-(z_pT_Bin_32) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_33) (135.0°), (Q2_y_Bin_2)-(z_pT_Bin_34) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_4) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_9) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_12) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_14) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_15) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_17) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_18) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_19) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_20) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_21) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_22) (135.0°)
(Q2_y_Bin_3)-(z_pT_Bin_23) (135.0°), (Q2_y_Bin_3)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_8) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_4)-(z_pT_Bin_15) (315.0°), (Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_19) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_20) (120.0°)
(Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (270.0°), (Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_26) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_27) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_28) (300.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_11) (105.0°)
(Q2_y_Bin_5)-(z_pT_Bin_13) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_15) (150.0°)
(Q2_y_Bin_5)-(z_pT_Bin_19) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (270.0°), (Q2_y_Bin_5)-(z_pT_Bin_20) (150.0°)
(Q2_y_Bin_5)-(z_pT_Bin_25) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_26) (120.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°)
(Q2_y_Bin_5)-(z_pT_Bin_31) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_32) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_4) (195.0°)
(Q2_y_Bin_5)-(z_pT_Bin_5) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_7) (240.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_1) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_13) (120.0°), (Q2_y_Bin_6)-(z_pT_Bin_14) (150.0°)
(Q2_y_Bin_6)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_6)-(z_pT_Bin_19) (135.0°), (Q2_y_Bin_6)-(z_pT_Bin_2) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_20) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_25) (225.0°), (Q2_y_Bin_6)-(z_pT_Bin_26) (240.0°)
(Q2_y_Bin_6)-(z_pT_Bin_27) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_28) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_6) (150.0°)
(Q2_y_Bin_6)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_8) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_9) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_15) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_16) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_17) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_18) (120.0°)
(Q2_y_Bin_7)-(z_pT_Bin_19) (120.0°), (Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_20) (105.0°)
(Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_22) (120.0°), (Q2_y_Bin_7)-(z_pT_Bin_23) (120.0°)
(Q2_y_Bin_7)-(z_pT_Bin_24) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_25) (105.0°), (Q2_y_Bin_7)-(z_pT_Bin_26) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_27) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_28) (120.0°), (Q2_y_Bin_7)-(z_pT_Bin_29) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_31) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°)
(Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_34) (225.0°), (Q2_y_Bin_7)-(z_pT_Bin_35) (315.0°)
(Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_7)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_8) (135.0°)
(Q2_y_Bin_7)-(z_pT_Bin_9) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_12) (135.0°)
(Q2_y_Bin_8)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_16) (195.0°)
(Q2_y_Bin_8)-(z_pT_Bin_18) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_19) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_21) (165.0°), (Q2_y_Bin_8)-(z_pT_Bin_23) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_24) (210.0°)
(Q2_y_Bin_8)-(z_pT_Bin_25) (330.0°), (Q2_y_Bin_8)-(z_pT_Bin_26) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°)
(Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_30) (300.0°), (Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_9)-(z_pT_Bin_1) (210.0°), (Q2_y_Bin_9)-(z_pT_Bin_10) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_11) (120.0°)
(Q2_y_Bin_9)-(z_pT_Bin_15) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_16) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_9)-(z_pT_Bin_22) (120.0°), (Q2_y_Bin_9)-(z_pT_Bin_23) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_29) (195.0°)
(Q2_y_Bin_9)-(z_pT_Bin_3) (195.0°), (Q2_y_Bin_9)-(z_pT_Bin_30) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_4) (195.0°)
(Q2_y_Bin_9)-(z_pT_Bin_5) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_6) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_8) (150.0°)
(Q2_y_Bin_9)-(z_pT_Bin_9) (120.0°)

Above 120° (235/452 (52.0%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_16) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°)
(Q2_y_Bin_1)-(z_pT_Bin_23) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°)
(Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_31) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_4) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_5) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_7) (150.0°)
(Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_10)-(z_pT_Bin_1) (150.0°)
(Q2_y_Bin_10)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_26) (135.0°), (Q2_y_Bin_10)-(z_pT_Bin_3) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_31) (150.0°), (Q2_y_Bin_10)-(z_pT_Bin_32) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_4) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_5) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_7) (150.0°)
(Q2_y_Bin_10)-(z_pT_Bin_9) (135.0°), (Q2_y_Bin_11)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_11)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_20) (135.0°), (Q2_y_Bin_11)-(z_pT_Bin_21) (150.0°)
(Q2_y_Bin_11)-(z_pT_Bin_22) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_23) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_24) (225.0°)
(Q2_y_Bin_11)-(z_pT_Bin_3) (195.0°), (Q2_y_Bin_11)-(z_pT_Bin_4) (330.0°), (Q2_y_Bin_11)-(z_pT_Bin_6) (165.0°)
(Q2_y_Bin_12)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_12)-(z_pT_Bin_14) (270.0°), (Q2_y_Bin_12)-(z_pT_Bin_16) (135.0°)
(Q2_y_Bin_12)-(z_pT_Bin_19) (255.0°), (Q2_y_Bin_12)-(z_pT_Bin_21) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_22) (195.0°)
(Q2_y_Bin_12)-(z_pT_Bin_23) (240.0°), (Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_6) (225.0°)
(Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_13)-(z_pT_Bin_1) (180.0°)
(Q2_y_Bin_13)-(z_pT_Bin_2) (150.0°), (Q2_y_Bin_13)-(z_pT_Bin_4) (135.0°), (Q2_y_Bin_14)-(z_pT_Bin_2) (150.0°)
(Q2_y_Bin_14)-(z_pT_Bin_32) (135.0°), (Q2_y_Bin_14)-(z_pT_Bin_4) (150.0°), (Q2_y_Bin_14)-(z_pT_Bin_5) (195.0°)
(Q2_y_Bin_15)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (225.0°), (Q2_y_Bin_15)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_15)-(z_pT_Bin_21) (135.0°), (Q2_y_Bin_15)-(z_pT_Bin_22) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_23) (180.0°)
(Q2_y_Bin_15)-(z_pT_Bin_24) (270.0°), (Q2_y_Bin_15)-(z_pT_Bin_6) (135.0°), (Q2_y_Bin_15)-(z_pT_Bin_9) (150.0°)
(Q2_y_Bin_16)-(z_pT_Bin_6) (150.0°), (Q2_y_Bin_17)-(z_pT_Bin_4) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_1) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_10) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_11) (135.0°), (Q2_y_Bin_2)-(z_pT_Bin_13) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_15) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_16) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_19) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_2) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_20) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_25) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_26) (135.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_32) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_33) (135.0°)
(Q2_y_Bin_2)-(z_pT_Bin_34) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_4) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_8) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°)
(Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_12) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_13) (210.0°)
(Q2_y_Bin_3)-(z_pT_Bin_14) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_15) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_16) (165.0°)
(Q2_y_Bin_3)-(z_pT_Bin_17) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_18) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_19) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_20) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_21) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_22) (135.0°), (Q2_y_Bin_3)-(z_pT_Bin_23) (135.0°), (Q2_y_Bin_3)-(z_pT_Bin_24) (255.0°)
(Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_3) (270.0°)
(Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_8) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_4)-(z_pT_Bin_15) (315.0°)
(Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_19) (240.0°)
(Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (270.0°), (Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_26) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_27) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_28) (300.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_13) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_15) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_19) (150.0°)
(Q2_y_Bin_5)-(z_pT_Bin_2) (270.0°), (Q2_y_Bin_5)-(z_pT_Bin_20) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_25) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_31) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_32) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_5) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_6) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_7) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_9) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_14) (150.0°)
(Q2_y_Bin_6)-(z_pT_Bin_19) (135.0°), (Q2_y_Bin_6)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_20) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_25) (225.0°), (Q2_y_Bin_6)-(z_pT_Bin_26) (240.0°), (Q2_y_Bin_6)-(z_pT_Bin_27) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_28) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_6) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_7) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_8) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_9) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_1) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°)
(Q2_y_Bin_7)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_15) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_16) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_17) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°)
(Q2_y_Bin_7)-(z_pT_Bin_24) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_26) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_27) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_29) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_31) (270.0°)
(Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°), (Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_34) (225.0°)
(Q2_y_Bin_7)-(z_pT_Bin_35) (315.0°), (Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_7)-(z_pT_Bin_7) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_8) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_9) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°)
(Q2_y_Bin_8)-(z_pT_Bin_12) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_16) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_18) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_19) (210.0°)
(Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_21) (165.0°), (Q2_y_Bin_8)-(z_pT_Bin_23) (150.0°)
(Q2_y_Bin_8)-(z_pT_Bin_24) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_25) (330.0°), (Q2_y_Bin_8)-(z_pT_Bin_26) (135.0°)
(Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_30) (300.0°)
(Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_9)-(z_pT_Bin_1) (210.0°), (Q2_y_Bin_9)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_9)-(z_pT_Bin_15) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_16) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_9)-(z_pT_Bin_29) (195.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (195.0°), (Q2_y_Bin_9)-(z_pT_Bin_30) (135.0°)
(Q2_y_Bin_9)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_9)-(z_pT_Bin_5) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_6) (135.0°)
(Q2_y_Bin_9)-(z_pT_Bin_8) (150.0°)

Above 135° (209/452 (46.2%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_16) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°)
(Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_31) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_5) (180.0°)
(Q2_y_Bin_1)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_7) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°)
(Q2_y_Bin_1)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_10)-(z_pT_Bin_1) (150.0°), (Q2_y_Bin_10)-(z_pT_Bin_2) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_31) (150.0°), (Q2_y_Bin_10)-(z_pT_Bin_32) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_5) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_10)-(z_pT_Bin_7) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_2) (165.0°)
(Q2_y_Bin_11)-(z_pT_Bin_21) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_22) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_23) (210.0°)
(Q2_y_Bin_11)-(z_pT_Bin_24) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_3) (195.0°), (Q2_y_Bin_11)-(z_pT_Bin_4) (330.0°)
(Q2_y_Bin_11)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_12)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_12)-(z_pT_Bin_14) (270.0°)
(Q2_y_Bin_12)-(z_pT_Bin_19) (255.0°), (Q2_y_Bin_12)-(z_pT_Bin_21) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_22) (195.0°)
(Q2_y_Bin_12)-(z_pT_Bin_23) (240.0°), (Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_6) (225.0°)
(Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_13)-(z_pT_Bin_1) (180.0°)
(Q2_y_Bin_13)-(z_pT_Bin_2) (150.0°), (Q2_y_Bin_14)-(z_pT_Bin_2) (150.0°), (Q2_y_Bin_14)-(z_pT_Bin_4) (150.0°)
(Q2_y_Bin_14)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (225.0°)
(Q2_y_Bin_15)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_22) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_23) (180.0°)
(Q2_y_Bin_15)-(z_pT_Bin_24) (270.0°), (Q2_y_Bin_15)-(z_pT_Bin_9) (150.0°), (Q2_y_Bin_16)-(z_pT_Bin_6) (150.0°)
(Q2_y_Bin_17)-(z_pT_Bin_4) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_1) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_10) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_13) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_15) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_16) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_19) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_2) (225.0°)
(Q2_y_Bin_2)-(z_pT_Bin_20) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_25) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_32) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_34) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_4) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_9) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_12) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_14) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_15) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_17) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_18) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_19) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_20) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_21) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_24) (255.0°)
(Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_3) (270.0°)
(Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_8) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_4)-(z_pT_Bin_15) (315.0°)
(Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_19) (240.0°)
(Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (270.0°), (Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_26) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_27) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_28) (300.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_13) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_15) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_19) (150.0°)
(Q2_y_Bin_5)-(z_pT_Bin_2) (270.0°), (Q2_y_Bin_5)-(z_pT_Bin_20) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_25) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_31) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_32) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_5) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_6) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_7) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_9) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_14) (150.0°)
(Q2_y_Bin_6)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_20) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_25) (225.0°)
(Q2_y_Bin_6)-(z_pT_Bin_26) (240.0°), (Q2_y_Bin_6)-(z_pT_Bin_27) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_28) (150.0°)
(Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_6) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_8) (150.0°)
(Q2_y_Bin_6)-(z_pT_Bin_9) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_10) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_13) (195.0°)
(Q2_y_Bin_7)-(z_pT_Bin_15) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_16) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_17) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_24) (195.0°)
(Q2_y_Bin_7)-(z_pT_Bin_26) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_27) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_29) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_31) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°)
(Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_34) (225.0°), (Q2_y_Bin_7)-(z_pT_Bin_35) (315.0°)
(Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_7)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°)
(Q2_y_Bin_8)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_16) (195.0°)
(Q2_y_Bin_8)-(z_pT_Bin_19) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_21) (165.0°)
(Q2_y_Bin_8)-(z_pT_Bin_23) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_24) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_25) (330.0°)
(Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_30) (300.0°)
(Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_9)-(z_pT_Bin_1) (210.0°), (Q2_y_Bin_9)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_9)-(z_pT_Bin_29) (195.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (195.0°), (Q2_y_Bin_9)-(z_pT_Bin_4) (195.0°)
(Q2_y_Bin_9)-(z_pT_Bin_5) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_8) (150.0°)

Above 150° (171/452 (37.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_16) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°)
(Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_5) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_6) (165.0°)
(Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_10)-(z_pT_Bin_2) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_32) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_4) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_5) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_1) (165.0°)
(Q2_y_Bin_11)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_22) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_23) (210.0°)
(Q2_y_Bin_11)-(z_pT_Bin_24) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_3) (195.0°), (Q2_y_Bin_11)-(z_pT_Bin_4) (330.0°)
(Q2_y_Bin_11)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_12)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_12)-(z_pT_Bin_14) (270.0°)
(Q2_y_Bin_12)-(z_pT_Bin_19) (255.0°), (Q2_y_Bin_12)-(z_pT_Bin_21) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_22) (195.0°)
(Q2_y_Bin_12)-(z_pT_Bin_23) (240.0°), (Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_6) (225.0°)
(Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_13)-(z_pT_Bin_1) (180.0°)
(Q2_y_Bin_14)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (225.0°)
(Q2_y_Bin_15)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_22) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_23) (180.0°)
(Q2_y_Bin_15)-(z_pT_Bin_24) (270.0°), (Q2_y_Bin_2)-(z_pT_Bin_1) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_10) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_15) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_19) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_2) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_20) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_25) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_32) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_4) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_9) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_12) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_15) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_20) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_21) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_9) (180.0°)
(Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_14) (165.0°)
(Q2_y_Bin_4)-(z_pT_Bin_15) (315.0°), (Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_19) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (270.0°)
(Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_27) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_28) (300.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_13) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (270.0°), (Q2_y_Bin_5)-(z_pT_Bin_25) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_31) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_32) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_5) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_6) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_7) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_9) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_20) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_25) (225.0°), (Q2_y_Bin_6)-(z_pT_Bin_26) (240.0°), (Q2_y_Bin_6)-(z_pT_Bin_27) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_9) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_1) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_13) (195.0°)
(Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_24) (195.0°)
(Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_31) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°)
(Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_34) (225.0°), (Q2_y_Bin_7)-(z_pT_Bin_35) (315.0°)
(Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_7)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°)
(Q2_y_Bin_8)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_16) (195.0°)
(Q2_y_Bin_8)-(z_pT_Bin_19) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_21) (165.0°)
(Q2_y_Bin_8)-(z_pT_Bin_24) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_25) (330.0°), (Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°)
(Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_30) (300.0°), (Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_9)-(z_pT_Bin_1) (210.0°), (Q2_y_Bin_9)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_9)-(z_pT_Bin_29) (195.0°)
(Q2_y_Bin_9)-(z_pT_Bin_3) (195.0°), (Q2_y_Bin_9)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_9)-(z_pT_Bin_5) (180.0°)

Above 180° (113/452 (25.0%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (225.0°)
(Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (195.0°)
(Q2_y_Bin_10)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_22) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_23) (210.0°)
(Q2_y_Bin_11)-(z_pT_Bin_24) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_3) (195.0°), (Q2_y_Bin_11)-(z_pT_Bin_4) (330.0°)
(Q2_y_Bin_12)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_12)-(z_pT_Bin_14) (270.0°), (Q2_y_Bin_12)-(z_pT_Bin_19) (255.0°)
(Q2_y_Bin_12)-(z_pT_Bin_21) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_22) (195.0°), (Q2_y_Bin_12)-(z_pT_Bin_23) (240.0°)
(Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_6) (225.0°), (Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°)
(Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_14)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (225.0°)
(Q2_y_Bin_15)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_24) (270.0°), (Q2_y_Bin_2)-(z_pT_Bin_1) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_2) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°)
(Q2_y_Bin_2)-(z_pT_Bin_4) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_15) (315.0°), (Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_19) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (270.0°)
(Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_27) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_28) (300.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (270.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°)
(Q2_y_Bin_5)-(z_pT_Bin_31) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_5) (210.0°)
(Q2_y_Bin_5)-(z_pT_Bin_7) (240.0°), (Q2_y_Bin_6)-(z_pT_Bin_25) (225.0°), (Q2_y_Bin_6)-(z_pT_Bin_26) (240.0°)
(Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_7)-(z_pT_Bin_24) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_31) (270.0°)
(Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°), (Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_34) (225.0°)
(Q2_y_Bin_7)-(z_pT_Bin_35) (315.0°), (Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°)
(Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_16) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_19) (210.0°)
(Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_24) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_25) (330.0°)
(Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_30) (300.0°), (Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_9)-(z_pT_Bin_1) (210.0°), (Q2_y_Bin_9)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_9)-(z_pT_Bin_29) (195.0°)
(Q2_y_Bin_9)-(z_pT_Bin_3) (195.0°), (Q2_y_Bin_9)-(z_pT_Bin_4) (195.0°)

### sector / P2

Stage: spline, acceptance. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/pion_sector/pipS2o/fit_copy.root`

Above 90° (298/452 (65.9%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (270.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_11) (120.0°)
(Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_16) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_17) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_2) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_23) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_31) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_32) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_4) (225.0°)
(Q2_y_Bin_1)-(z_pT_Bin_5) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_6) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_7) (165.0°)
(Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_1) (150.0°)
(Q2_y_Bin_10)-(z_pT_Bin_10) (120.0°), (Q2_y_Bin_10)-(z_pT_Bin_13) (105.0°), (Q2_y_Bin_10)-(z_pT_Bin_15) (135.0°)
(Q2_y_Bin_10)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_10)-(z_pT_Bin_20) (120.0°), (Q2_y_Bin_10)-(z_pT_Bin_26) (135.0°)
(Q2_y_Bin_10)-(z_pT_Bin_3) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_31) (120.0°), (Q2_y_Bin_10)-(z_pT_Bin_32) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_5) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_6) (195.0°)
(Q2_y_Bin_10)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_10)-(z_pT_Bin_9) (120.0°)
(Q2_y_Bin_11)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_11) (105.0°)
(Q2_y_Bin_11)-(z_pT_Bin_13) (120.0°), (Q2_y_Bin_11)-(z_pT_Bin_15) (105.0°), (Q2_y_Bin_11)-(z_pT_Bin_18) (105.0°)
(Q2_y_Bin_11)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_20) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_21) (165.0°)
(Q2_y_Bin_11)-(z_pT_Bin_22) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_23) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_24) (270.0°)
(Q2_y_Bin_11)-(z_pT_Bin_3) (240.0°), (Q2_y_Bin_11)-(z_pT_Bin_4) (300.0°), (Q2_y_Bin_11)-(z_pT_Bin_6) (150.0°)
(Q2_y_Bin_11)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_11)-(z_pT_Bin_9) (135.0°), (Q2_y_Bin_12)-(z_pT_Bin_11) (195.0°)
(Q2_y_Bin_12)-(z_pT_Bin_12) (105.0°), (Q2_y_Bin_12)-(z_pT_Bin_13) (120.0°), (Q2_y_Bin_12)-(z_pT_Bin_14) (315.0°)
(Q2_y_Bin_12)-(z_pT_Bin_16) (105.0°), (Q2_y_Bin_12)-(z_pT_Bin_18) (120.0°), (Q2_y_Bin_12)-(z_pT_Bin_19) (255.0°)
(Q2_y_Bin_12)-(z_pT_Bin_21) (315.0°), (Q2_y_Bin_12)-(z_pT_Bin_22) (225.0°), (Q2_y_Bin_12)-(z_pT_Bin_23) (255.0°)
(Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°)
(Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_13)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_13)-(z_pT_Bin_12) (120.0°)
(Q2_y_Bin_13)-(z_pT_Bin_13) (105.0°), (Q2_y_Bin_13)-(z_pT_Bin_17) (105.0°), (Q2_y_Bin_13)-(z_pT_Bin_2) (180.0°)
(Q2_y_Bin_13)-(z_pT_Bin_26) (120.0°), (Q2_y_Bin_13)-(z_pT_Bin_3) (135.0°), (Q2_y_Bin_13)-(z_pT_Bin_4) (150.0°)
(Q2_y_Bin_13)-(z_pT_Bin_5) (135.0°), (Q2_y_Bin_13)-(z_pT_Bin_7) (105.0°), (Q2_y_Bin_13)-(z_pT_Bin_8) (120.0°)
(Q2_y_Bin_13)-(z_pT_Bin_9) (105.0°), (Q2_y_Bin_14)-(z_pT_Bin_1) (120.0°), (Q2_y_Bin_14)-(z_pT_Bin_10) (105.0°)
(Q2_y_Bin_14)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_14)-(z_pT_Bin_26) (105.0°), (Q2_y_Bin_14)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_14)-(z_pT_Bin_32) (150.0°), (Q2_y_Bin_14)-(z_pT_Bin_4) (135.0°), (Q2_y_Bin_14)-(z_pT_Bin_5) (180.0°)
(Q2_y_Bin_15)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_19) (120.0°)
(Q2_y_Bin_15)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_21) (120.0°), (Q2_y_Bin_15)-(z_pT_Bin_22) (150.0°)
(Q2_y_Bin_15)-(z_pT_Bin_23) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_24) (240.0°), (Q2_y_Bin_15)-(z_pT_Bin_9) (120.0°)
(Q2_y_Bin_16)-(z_pT_Bin_1) (120.0°), (Q2_y_Bin_16)-(z_pT_Bin_14) (105.0°), (Q2_y_Bin_16)-(z_pT_Bin_3) (105.0°)
(Q2_y_Bin_16)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_16)-(z_pT_Bin_5) (150.0°), (Q2_y_Bin_16)-(z_pT_Bin_6) (150.0°)
(Q2_y_Bin_16)-(z_pT_Bin_9) (105.0°), (Q2_y_Bin_17)-(z_pT_Bin_4) (105.0°), (Q2_y_Bin_2)-(z_pT_Bin_1) (225.0°)
(Q2_y_Bin_2)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_11) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_12) (120.0°)
(Q2_y_Bin_2)-(z_pT_Bin_13) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_15) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_16) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_17) (105.0°), (Q2_y_Bin_2)-(z_pT_Bin_18) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_19) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_2) (255.0°), (Q2_y_Bin_2)-(z_pT_Bin_20) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_21) (135.0°), (Q2_y_Bin_2)-(z_pT_Bin_22) (105.0°), (Q2_y_Bin_2)-(z_pT_Bin_23) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_25) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_26) (135.0°), (Q2_y_Bin_2)-(z_pT_Bin_27) (135.0°)
(Q2_y_Bin_2)-(z_pT_Bin_28) (120.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°)
(Q2_y_Bin_2)-(z_pT_Bin_32) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_33) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_34) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_4) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_6) (225.0°)
(Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_9) (210.0°)
(Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_12) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_14) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_15) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_17) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_18) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_19) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_2) (240.0°)
(Q2_y_Bin_3)-(z_pT_Bin_20) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_21) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_22) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_23) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_24) (270.0°), (Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_3) (285.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_8) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_4)-(z_pT_Bin_15) (345.0°), (Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_19) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_20) (150.0°)
(Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (315.0°), (Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_26) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_27) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_28) (300.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (255.0°), (Q2_y_Bin_5)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_11) (105.0°)
(Q2_y_Bin_5)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_15) (150.0°)
(Q2_y_Bin_5)-(z_pT_Bin_16) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_19) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (270.0°)
(Q2_y_Bin_5)-(z_pT_Bin_20) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_25) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_26) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_31) (225.0°), (Q2_y_Bin_5)-(z_pT_Bin_32) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_5) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_6) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_7) (255.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_9) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_11) (105.0°)
(Q2_y_Bin_6)-(z_pT_Bin_13) (120.0°), (Q2_y_Bin_6)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_15) (120.0°)
(Q2_y_Bin_6)-(z_pT_Bin_16) (105.0°), (Q2_y_Bin_6)-(z_pT_Bin_19) (135.0°), (Q2_y_Bin_6)-(z_pT_Bin_2) (210.0°)
(Q2_y_Bin_6)-(z_pT_Bin_20) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_25) (255.0°), (Q2_y_Bin_6)-(z_pT_Bin_26) (255.0°)
(Q2_y_Bin_6)-(z_pT_Bin_27) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_28) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_6) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_6)-(z_pT_Bin_8) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_9) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_15) (135.0°)
(Q2_y_Bin_7)-(z_pT_Bin_16) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_17) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_18) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_19) (120.0°), (Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_20) (120.0°)
(Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_22) (120.0°), (Q2_y_Bin_7)-(z_pT_Bin_23) (120.0°)
(Q2_y_Bin_7)-(z_pT_Bin_24) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_25) (105.0°), (Q2_y_Bin_7)-(z_pT_Bin_26) (135.0°)
(Q2_y_Bin_7)-(z_pT_Bin_27) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_28) (120.0°), (Q2_y_Bin_7)-(z_pT_Bin_29) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_31) (225.0°), (Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°)
(Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_34) (255.0°), (Q2_y_Bin_7)-(z_pT_Bin_35) (300.0°)
(Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_7)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_8) (135.0°)
(Q2_y_Bin_7)-(z_pT_Bin_9) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_12) (135.0°)
(Q2_y_Bin_8)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_16) (210.0°)
(Q2_y_Bin_8)-(z_pT_Bin_18) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_19) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_21) (165.0°), (Q2_y_Bin_8)-(z_pT_Bin_23) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_24) (225.0°)
(Q2_y_Bin_8)-(z_pT_Bin_25) (345.0°), (Q2_y_Bin_8)-(z_pT_Bin_26) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°)
(Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_30) (315.0°), (Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_9)-(z_pT_Bin_1) (225.0°), (Q2_y_Bin_9)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_9)-(z_pT_Bin_11) (120.0°)
(Q2_y_Bin_9)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_9)-(z_pT_Bin_16) (150.0°), (Q2_y_Bin_9)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_9)-(z_pT_Bin_22) (120.0°), (Q2_y_Bin_9)-(z_pT_Bin_23) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_29) (195.0°)
(Q2_y_Bin_9)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_30) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_4) (195.0°)
(Q2_y_Bin_9)-(z_pT_Bin_5) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_6) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_8) (165.0°)
(Q2_y_Bin_9)-(z_pT_Bin_9) (135.0°)

Above 120° (238/452 (52.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (270.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_16) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_17) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (255.0°)
(Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_23) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_31) (150.0°)
(Q2_y_Bin_1)-(z_pT_Bin_32) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_4) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_5) (210.0°)
(Q2_y_Bin_1)-(z_pT_Bin_6) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°)
(Q2_y_Bin_1)-(z_pT_Bin_9) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_1) (150.0°), (Q2_y_Bin_10)-(z_pT_Bin_15) (135.0°)
(Q2_y_Bin_10)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_10)-(z_pT_Bin_26) (135.0°), (Q2_y_Bin_10)-(z_pT_Bin_3) (165.0°)
(Q2_y_Bin_10)-(z_pT_Bin_32) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_5) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_6) (195.0°), (Q2_y_Bin_10)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_1) (165.0°)
(Q2_y_Bin_11)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_20) (165.0°)
(Q2_y_Bin_11)-(z_pT_Bin_21) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_22) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_23) (210.0°)
(Q2_y_Bin_11)-(z_pT_Bin_24) (270.0°), (Q2_y_Bin_11)-(z_pT_Bin_3) (240.0°), (Q2_y_Bin_11)-(z_pT_Bin_4) (300.0°)
(Q2_y_Bin_11)-(z_pT_Bin_6) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_9) (135.0°), (Q2_y_Bin_12)-(z_pT_Bin_11) (195.0°)
(Q2_y_Bin_12)-(z_pT_Bin_14) (315.0°), (Q2_y_Bin_12)-(z_pT_Bin_19) (255.0°), (Q2_y_Bin_12)-(z_pT_Bin_21) (315.0°)
(Q2_y_Bin_12)-(z_pT_Bin_22) (225.0°), (Q2_y_Bin_12)-(z_pT_Bin_23) (255.0°), (Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°)
(Q2_y_Bin_12)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_13)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_13)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_13)-(z_pT_Bin_3) (135.0°)
(Q2_y_Bin_13)-(z_pT_Bin_4) (150.0°), (Q2_y_Bin_13)-(z_pT_Bin_5) (135.0°), (Q2_y_Bin_14)-(z_pT_Bin_2) (165.0°)
(Q2_y_Bin_14)-(z_pT_Bin_32) (150.0°), (Q2_y_Bin_14)-(z_pT_Bin_4) (135.0°), (Q2_y_Bin_14)-(z_pT_Bin_5) (180.0°)
(Q2_y_Bin_15)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_15)-(z_pT_Bin_22) (150.0°), (Q2_y_Bin_15)-(z_pT_Bin_23) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_24) (240.0°)
(Q2_y_Bin_16)-(z_pT_Bin_5) (150.0°), (Q2_y_Bin_16)-(z_pT_Bin_6) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_1) (225.0°)
(Q2_y_Bin_2)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_11) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_13) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_15) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_16) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_19) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_2) (255.0°), (Q2_y_Bin_2)-(z_pT_Bin_20) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_21) (135.0°), (Q2_y_Bin_2)-(z_pT_Bin_25) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_26) (135.0°)
(Q2_y_Bin_2)-(z_pT_Bin_27) (135.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°)
(Q2_y_Bin_2)-(z_pT_Bin_32) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_33) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_34) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_4) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_6) (225.0°)
(Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_9) (210.0°)
(Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_12) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_14) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_15) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_17) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_18) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_19) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_2) (240.0°)
(Q2_y_Bin_3)-(z_pT_Bin_20) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_21) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_22) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_23) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_24) (270.0°), (Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_3) (285.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_8) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_4)-(z_pT_Bin_15) (345.0°), (Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_19) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_20) (150.0°)
(Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (315.0°), (Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_26) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_27) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_28) (300.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (255.0°), (Q2_y_Bin_5)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_13) (195.0°)
(Q2_y_Bin_5)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_15) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_19) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_2) (270.0°), (Q2_y_Bin_5)-(z_pT_Bin_20) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_25) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_31) (225.0°), (Q2_y_Bin_5)-(z_pT_Bin_32) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_5) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_6) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_7) (255.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_9) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_14) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_19) (135.0°), (Q2_y_Bin_6)-(z_pT_Bin_2) (210.0°), (Q2_y_Bin_6)-(z_pT_Bin_20) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_25) (255.0°), (Q2_y_Bin_6)-(z_pT_Bin_26) (255.0°), (Q2_y_Bin_6)-(z_pT_Bin_27) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_28) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_7) (195.0°)
(Q2_y_Bin_6)-(z_pT_Bin_8) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_9) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_1) (195.0°)
(Q2_y_Bin_7)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°)
(Q2_y_Bin_7)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_15) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_16) (135.0°)
(Q2_y_Bin_7)-(z_pT_Bin_17) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_18) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_24) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_26) (135.0°)
(Q2_y_Bin_7)-(z_pT_Bin_27) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_29) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°)
(Q2_y_Bin_7)-(z_pT_Bin_31) (225.0°), (Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°), (Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°)
(Q2_y_Bin_7)-(z_pT_Bin_34) (255.0°), (Q2_y_Bin_7)-(z_pT_Bin_35) (300.0°), (Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°)
(Q2_y_Bin_7)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_8) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_9) (150.0°)
(Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_12) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_13) (195.0°)
(Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_16) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_18) (150.0°)
(Q2_y_Bin_8)-(z_pT_Bin_19) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_21) (165.0°)
(Q2_y_Bin_8)-(z_pT_Bin_23) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_24) (225.0°), (Q2_y_Bin_8)-(z_pT_Bin_25) (345.0°)
(Q2_y_Bin_8)-(z_pT_Bin_26) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°)
(Q2_y_Bin_8)-(z_pT_Bin_30) (315.0°), (Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_9)-(z_pT_Bin_1) (225.0°)
(Q2_y_Bin_9)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_9)-(z_pT_Bin_16) (150.0°), (Q2_y_Bin_9)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_9)-(z_pT_Bin_29) (195.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_4) (195.0°)
(Q2_y_Bin_9)-(z_pT_Bin_5) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_6) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_8) (165.0°)
(Q2_y_Bin_9)-(z_pT_Bin_9) (135.0°)

Above 135° (216/452 (47.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (270.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_16) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°)
(Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_31) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_32) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_4) (225.0°)
(Q2_y_Bin_1)-(z_pT_Bin_5) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_6) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_7) (165.0°)
(Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_1) (150.0°)
(Q2_y_Bin_10)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_10)-(z_pT_Bin_3) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_32) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_5) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_6) (195.0°)
(Q2_y_Bin_10)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_10) (150.0°)
(Q2_y_Bin_11)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_20) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_21) (165.0°)
(Q2_y_Bin_11)-(z_pT_Bin_22) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_23) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_24) (270.0°)
(Q2_y_Bin_11)-(z_pT_Bin_3) (240.0°), (Q2_y_Bin_11)-(z_pT_Bin_4) (300.0°), (Q2_y_Bin_11)-(z_pT_Bin_6) (150.0°)
(Q2_y_Bin_12)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_12)-(z_pT_Bin_14) (315.0°), (Q2_y_Bin_12)-(z_pT_Bin_19) (255.0°)
(Q2_y_Bin_12)-(z_pT_Bin_21) (315.0°), (Q2_y_Bin_12)-(z_pT_Bin_22) (225.0°), (Q2_y_Bin_12)-(z_pT_Bin_23) (255.0°)
(Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°)
(Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_13)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_13)-(z_pT_Bin_2) (180.0°)
(Q2_y_Bin_13)-(z_pT_Bin_4) (150.0°), (Q2_y_Bin_14)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_14)-(z_pT_Bin_32) (150.0°)
(Q2_y_Bin_14)-(z_pT_Bin_5) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_15)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_22) (150.0°), (Q2_y_Bin_15)-(z_pT_Bin_23) (180.0°)
(Q2_y_Bin_15)-(z_pT_Bin_24) (240.0°), (Q2_y_Bin_16)-(z_pT_Bin_5) (150.0°), (Q2_y_Bin_16)-(z_pT_Bin_6) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_1) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_11) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_13) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_15) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_16) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_19) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_2) (255.0°)
(Q2_y_Bin_2)-(z_pT_Bin_20) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_25) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_32) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_33) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_34) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_4) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_6) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_8) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_9) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°)
(Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_12) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_13) (210.0°)
(Q2_y_Bin_3)-(z_pT_Bin_14) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_15) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_16) (165.0°)
(Q2_y_Bin_3)-(z_pT_Bin_17) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_18) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_19) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_3)-(z_pT_Bin_20) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_21) (165.0°)
(Q2_y_Bin_3)-(z_pT_Bin_22) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_23) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_24) (270.0°)
(Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_3) (285.0°)
(Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_4)-(z_pT_Bin_15) (345.0°)
(Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_19) (240.0°)
(Q2_y_Bin_4)-(z_pT_Bin_20) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (315.0°)
(Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_26) (150.0°)
(Q2_y_Bin_4)-(z_pT_Bin_27) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_28) (300.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (255.0°), (Q2_y_Bin_5)-(z_pT_Bin_10) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_15) (150.0°)
(Q2_y_Bin_5)-(z_pT_Bin_19) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (270.0°), (Q2_y_Bin_5)-(z_pT_Bin_20) (150.0°)
(Q2_y_Bin_5)-(z_pT_Bin_25) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_31) (225.0°)
(Q2_y_Bin_5)-(z_pT_Bin_32) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_5) (210.0°)
(Q2_y_Bin_5)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_7) (255.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_10) (150.0°)
(Q2_y_Bin_6)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_2) (210.0°), (Q2_y_Bin_6)-(z_pT_Bin_20) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_25) (255.0°), (Q2_y_Bin_6)-(z_pT_Bin_26) (255.0°), (Q2_y_Bin_6)-(z_pT_Bin_27) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_28) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_7) (195.0°)
(Q2_y_Bin_6)-(z_pT_Bin_8) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_9) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_1) (195.0°)
(Q2_y_Bin_7)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°)
(Q2_y_Bin_7)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_18) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_24) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_27) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_29) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_31) (225.0°)
(Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°), (Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_34) (255.0°)
(Q2_y_Bin_7)-(z_pT_Bin_35) (300.0°), (Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_7)-(z_pT_Bin_7) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_9) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_13) (195.0°)
(Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_16) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_18) (150.0°)
(Q2_y_Bin_8)-(z_pT_Bin_19) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_21) (165.0°)
(Q2_y_Bin_8)-(z_pT_Bin_23) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_24) (225.0°), (Q2_y_Bin_8)-(z_pT_Bin_25) (345.0°)
(Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_30) (315.0°)
(Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_9)-(z_pT_Bin_1) (225.0°), (Q2_y_Bin_9)-(z_pT_Bin_10) (150.0°)
(Q2_y_Bin_9)-(z_pT_Bin_16) (150.0°), (Q2_y_Bin_9)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_9)-(z_pT_Bin_29) (195.0°)
(Q2_y_Bin_9)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_9)-(z_pT_Bin_8) (165.0°)

Above 150° (182/452 (40.3%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (270.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_16) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°)
(Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_4) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_5) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_6) (180.0°)
(Q2_y_Bin_1)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (210.0°)
(Q2_y_Bin_10)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_10)-(z_pT_Bin_3) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_32) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_5) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_6) (195.0°)
(Q2_y_Bin_10)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_2) (165.0°)
(Q2_y_Bin_11)-(z_pT_Bin_20) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_21) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_22) (225.0°)
(Q2_y_Bin_11)-(z_pT_Bin_23) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_24) (270.0°), (Q2_y_Bin_11)-(z_pT_Bin_3) (240.0°)
(Q2_y_Bin_11)-(z_pT_Bin_4) (300.0°), (Q2_y_Bin_12)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_12)-(z_pT_Bin_14) (315.0°)
(Q2_y_Bin_12)-(z_pT_Bin_19) (255.0°), (Q2_y_Bin_12)-(z_pT_Bin_21) (315.0°), (Q2_y_Bin_12)-(z_pT_Bin_22) (225.0°)
(Q2_y_Bin_12)-(z_pT_Bin_23) (255.0°), (Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_13)-(z_pT_Bin_1) (195.0°)
(Q2_y_Bin_13)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_14)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_14)-(z_pT_Bin_5) (180.0°)
(Q2_y_Bin_15)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_15)-(z_pT_Bin_23) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_24) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_1) (225.0°)
(Q2_y_Bin_2)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_13) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_15) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_19) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_2) (255.0°)
(Q2_y_Bin_2)-(z_pT_Bin_20) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_25) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_32) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_4) (225.0°)
(Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_6) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°)
(Q2_y_Bin_2)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_9) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_12) (165.0°)
(Q2_y_Bin_3)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_15) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_16) (165.0°)
(Q2_y_Bin_3)-(z_pT_Bin_18) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_3)-(z_pT_Bin_20) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_21) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_24) (270.0°), (Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_3) (285.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_8) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_4)-(z_pT_Bin_15) (345.0°), (Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_19) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_22) (315.0°), (Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°)
(Q2_y_Bin_4)-(z_pT_Bin_27) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_28) (300.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (255.0°), (Q2_y_Bin_5)-(z_pT_Bin_10) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_19) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_2) (270.0°), (Q2_y_Bin_5)-(z_pT_Bin_25) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°)
(Q2_y_Bin_5)-(z_pT_Bin_31) (225.0°), (Q2_y_Bin_5)-(z_pT_Bin_32) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_4) (195.0°)
(Q2_y_Bin_5)-(z_pT_Bin_5) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_7) (255.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_1) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_2) (210.0°), (Q2_y_Bin_6)-(z_pT_Bin_20) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_25) (255.0°), (Q2_y_Bin_6)-(z_pT_Bin_26) (255.0°), (Q2_y_Bin_6)-(z_pT_Bin_27) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_6)-(z_pT_Bin_9) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°)
(Q2_y_Bin_7)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°)
(Q2_y_Bin_7)-(z_pT_Bin_24) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_29) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°)
(Q2_y_Bin_7)-(z_pT_Bin_31) (225.0°), (Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°), (Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°)
(Q2_y_Bin_7)-(z_pT_Bin_34) (255.0°), (Q2_y_Bin_7)-(z_pT_Bin_35) (300.0°), (Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°)
(Q2_y_Bin_7)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_13) (195.0°)
(Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_16) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_19) (210.0°)
(Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_21) (165.0°), (Q2_y_Bin_8)-(z_pT_Bin_24) (225.0°)
(Q2_y_Bin_8)-(z_pT_Bin_25) (345.0°), (Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°)
(Q2_y_Bin_8)-(z_pT_Bin_30) (315.0°), (Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_9)-(z_pT_Bin_1) (225.0°)
(Q2_y_Bin_9)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_9)-(z_pT_Bin_29) (195.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (180.0°)
(Q2_y_Bin_9)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_9)-(z_pT_Bin_8) (165.0°)

Above 180° (125/452 (27.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (270.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_2) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°)
(Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_4) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_5) (210.0°)
(Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_10)-(z_pT_Bin_6) (195.0°), (Q2_y_Bin_11)-(z_pT_Bin_22) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_23) (210.0°)
(Q2_y_Bin_11)-(z_pT_Bin_24) (270.0°), (Q2_y_Bin_11)-(z_pT_Bin_3) (240.0°), (Q2_y_Bin_11)-(z_pT_Bin_4) (300.0°)
(Q2_y_Bin_12)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_12)-(z_pT_Bin_14) (315.0°), (Q2_y_Bin_12)-(z_pT_Bin_19) (255.0°)
(Q2_y_Bin_12)-(z_pT_Bin_21) (315.0°), (Q2_y_Bin_12)-(z_pT_Bin_22) (225.0°), (Q2_y_Bin_12)-(z_pT_Bin_23) (255.0°)
(Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°)
(Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_13)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_15)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_24) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_1) (225.0°)
(Q2_y_Bin_2)-(z_pT_Bin_19) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_2) (255.0°), (Q2_y_Bin_2)-(z_pT_Bin_20) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_32) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_4) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_6) (225.0°)
(Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_9) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_2) (240.0°)
(Q2_y_Bin_3)-(z_pT_Bin_20) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_24) (270.0°), (Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_3) (285.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_9) (195.0°)
(Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_15) (345.0°)
(Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_19) (240.0°)
(Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (315.0°), (Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_27) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_28) (300.0°)
(Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (255.0°)
(Q2_y_Bin_5)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (270.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°)
(Q2_y_Bin_5)-(z_pT_Bin_31) (225.0°), (Q2_y_Bin_5)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_5) (210.0°)
(Q2_y_Bin_5)-(z_pT_Bin_7) (255.0°), (Q2_y_Bin_6)-(z_pT_Bin_2) (210.0°), (Q2_y_Bin_6)-(z_pT_Bin_25) (255.0°)
(Q2_y_Bin_6)-(z_pT_Bin_26) (255.0°), (Q2_y_Bin_6)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_1) (195.0°)
(Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_7)-(z_pT_Bin_24) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_31) (225.0°)
(Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°), (Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_34) (255.0°)
(Q2_y_Bin_7)-(z_pT_Bin_35) (300.0°), (Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°)
(Q2_y_Bin_8)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_16) (210.0°)
(Q2_y_Bin_8)-(z_pT_Bin_19) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_24) (225.0°)
(Q2_y_Bin_8)-(z_pT_Bin_25) (345.0°), (Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_30) (315.0°)
(Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_9)-(z_pT_Bin_1) (225.0°), (Q2_y_Bin_9)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_9)-(z_pT_Bin_29) (195.0°), (Q2_y_Bin_9)-(z_pT_Bin_4) (195.0°)

### sector / E3

Stage: spline, acceptance. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/electron_sector/eS3o/fit_copy.root`

Above 90° (278/452 (61.5%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_11) (105.0°)
(Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_16) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_17) (120.0°)
(Q2_y_Bin_1)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_23) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_31) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_32) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_4) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_7) (150.0°)
(Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_1) (150.0°)
(Q2_y_Bin_10)-(z_pT_Bin_10) (120.0°), (Q2_y_Bin_10)-(z_pT_Bin_15) (135.0°), (Q2_y_Bin_10)-(z_pT_Bin_2) (165.0°)
(Q2_y_Bin_10)-(z_pT_Bin_20) (120.0°), (Q2_y_Bin_10)-(z_pT_Bin_26) (135.0°), (Q2_y_Bin_10)-(z_pT_Bin_3) (165.0°)
(Q2_y_Bin_10)-(z_pT_Bin_31) (120.0°), (Q2_y_Bin_10)-(z_pT_Bin_32) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_4) (150.0°)
(Q2_y_Bin_10)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_6) (195.0°), (Q2_y_Bin_10)-(z_pT_Bin_7) (150.0°)
(Q2_y_Bin_10)-(z_pT_Bin_9) (120.0°), (Q2_y_Bin_11)-(z_pT_Bin_1) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_10) (120.0°)
(Q2_y_Bin_11)-(z_pT_Bin_13) (105.0°), (Q2_y_Bin_11)-(z_pT_Bin_15) (105.0°), (Q2_y_Bin_11)-(z_pT_Bin_18) (105.0°)
(Q2_y_Bin_11)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_20) (120.0°), (Q2_y_Bin_11)-(z_pT_Bin_21) (135.0°)
(Q2_y_Bin_11)-(z_pT_Bin_22) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_23) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_24) (255.0°)
(Q2_y_Bin_11)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_4) (270.0°), (Q2_y_Bin_11)-(z_pT_Bin_6) (150.0°)
(Q2_y_Bin_11)-(z_pT_Bin_9) (120.0°), (Q2_y_Bin_12)-(z_pT_Bin_11) (180.0°), (Q2_y_Bin_12)-(z_pT_Bin_13) (120.0°)
(Q2_y_Bin_12)-(z_pT_Bin_14) (270.0°), (Q2_y_Bin_12)-(z_pT_Bin_16) (105.0°), (Q2_y_Bin_12)-(z_pT_Bin_18) (120.0°)
(Q2_y_Bin_12)-(z_pT_Bin_19) (255.0°), (Q2_y_Bin_12)-(z_pT_Bin_21) (300.0°), (Q2_y_Bin_12)-(z_pT_Bin_22) (195.0°)
(Q2_y_Bin_12)-(z_pT_Bin_23) (240.0°), (Q2_y_Bin_12)-(z_pT_Bin_24) (345.0°), (Q2_y_Bin_12)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_13)-(z_pT_Bin_1) (165.0°)
(Q2_y_Bin_13)-(z_pT_Bin_12) (105.0°), (Q2_y_Bin_13)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_13)-(z_pT_Bin_26) (120.0°)
(Q2_y_Bin_13)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_13)-(z_pT_Bin_4) (135.0°), (Q2_y_Bin_13)-(z_pT_Bin_5) (105.0°)
(Q2_y_Bin_13)-(z_pT_Bin_7) (105.0°), (Q2_y_Bin_13)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_14)-(z_pT_Bin_1) (105.0°)
(Q2_y_Bin_14)-(z_pT_Bin_2) (120.0°), (Q2_y_Bin_14)-(z_pT_Bin_32) (135.0°), (Q2_y_Bin_14)-(z_pT_Bin_4) (105.0°)
(Q2_y_Bin_14)-(z_pT_Bin_5) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (180.0°)
(Q2_y_Bin_15)-(z_pT_Bin_19) (105.0°), (Q2_y_Bin_15)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_22) (150.0°)
(Q2_y_Bin_15)-(z_pT_Bin_23) (165.0°), (Q2_y_Bin_15)-(z_pT_Bin_24) (210.0°), (Q2_y_Bin_15)-(z_pT_Bin_9) (120.0°)
(Q2_y_Bin_16)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_16)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_16)-(z_pT_Bin_5) (120.0°)
(Q2_y_Bin_16)-(z_pT_Bin_6) (150.0°), (Q2_y_Bin_16)-(z_pT_Bin_9) (105.0°), (Q2_y_Bin_17)-(z_pT_Bin_4) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_11) (135.0°)
(Q2_y_Bin_2)-(z_pT_Bin_12) (120.0°), (Q2_y_Bin_2)-(z_pT_Bin_13) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_15) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_16) (135.0°), (Q2_y_Bin_2)-(z_pT_Bin_19) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_20) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_21) (135.0°)
(Q2_y_Bin_2)-(z_pT_Bin_22) (105.0°), (Q2_y_Bin_2)-(z_pT_Bin_25) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_26) (135.0°)
(Q2_y_Bin_2)-(z_pT_Bin_27) (120.0°), (Q2_y_Bin_2)-(z_pT_Bin_28) (105.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_32) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_33) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_34) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_4) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_8) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°)
(Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_12) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_13) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_14) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_15) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_16) (165.0°)
(Q2_y_Bin_3)-(z_pT_Bin_17) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_18) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_19) (135.0°)
(Q2_y_Bin_3)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_20) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_21) (165.0°)
(Q2_y_Bin_3)-(z_pT_Bin_22) (135.0°), (Q2_y_Bin_3)-(z_pT_Bin_23) (135.0°), (Q2_y_Bin_3)-(z_pT_Bin_24) (255.0°)
(Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_3) (285.0°)
(Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_14) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_15) (315.0°)
(Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_19) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_20) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_21) (195.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (315.0°)
(Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_26) (165.0°)
(Q2_y_Bin_4)-(z_pT_Bin_27) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_28) (300.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (225.0°), (Q2_y_Bin_5)-(z_pT_Bin_10) (150.0°)
(Q2_y_Bin_5)-(z_pT_Bin_11) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_14) (150.0°)
(Q2_y_Bin_5)-(z_pT_Bin_15) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_16) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_19) (150.0°)
(Q2_y_Bin_5)-(z_pT_Bin_2) (255.0°), (Q2_y_Bin_5)-(z_pT_Bin_20) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_25) (135.0°)
(Q2_y_Bin_5)-(z_pT_Bin_26) (120.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_31) (210.0°)
(Q2_y_Bin_5)-(z_pT_Bin_32) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_5) (195.0°)
(Q2_y_Bin_5)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_7) (225.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_10) (120.0°)
(Q2_y_Bin_6)-(z_pT_Bin_11) (105.0°), (Q2_y_Bin_6)-(z_pT_Bin_13) (120.0°), (Q2_y_Bin_6)-(z_pT_Bin_14) (150.0°)
(Q2_y_Bin_6)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_6)-(z_pT_Bin_19) (120.0°), (Q2_y_Bin_6)-(z_pT_Bin_2) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_20) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_25) (210.0°), (Q2_y_Bin_6)-(z_pT_Bin_26) (240.0°)
(Q2_y_Bin_6)-(z_pT_Bin_27) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_28) (135.0°), (Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_6) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_7) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_8) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_9) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_15) (120.0°)
(Q2_y_Bin_7)-(z_pT_Bin_16) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_17) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_18) (120.0°)
(Q2_y_Bin_7)-(z_pT_Bin_19) (120.0°), (Q2_y_Bin_7)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_20) (120.0°)
(Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_22) (120.0°), (Q2_y_Bin_7)-(z_pT_Bin_23) (105.0°)
(Q2_y_Bin_7)-(z_pT_Bin_24) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_26) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_27) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_28) (120.0°), (Q2_y_Bin_7)-(z_pT_Bin_29) (120.0°), (Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°)
(Q2_y_Bin_7)-(z_pT_Bin_31) (255.0°), (Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°), (Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°)
(Q2_y_Bin_7)-(z_pT_Bin_34) (240.0°), (Q2_y_Bin_7)-(z_pT_Bin_35) (300.0°), (Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°)
(Q2_y_Bin_7)-(z_pT_Bin_7) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_7)-(z_pT_Bin_9) (150.0°)
(Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_12) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_13) (165.0°)
(Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_16) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_18) (135.0°)
(Q2_y_Bin_8)-(z_pT_Bin_19) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_21) (135.0°)
(Q2_y_Bin_8)-(z_pT_Bin_23) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_24) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_25) (315.0°)
(Q2_y_Bin_8)-(z_pT_Bin_26) (120.0°), (Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_29) (225.0°)
(Q2_y_Bin_8)-(z_pT_Bin_30) (285.0°), (Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_9)-(z_pT_Bin_1) (210.0°)
(Q2_y_Bin_9)-(z_pT_Bin_10) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_11) (120.0°), (Q2_y_Bin_9)-(z_pT_Bin_15) (120.0°)
(Q2_y_Bin_9)-(z_pT_Bin_16) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_22) (120.0°)
(Q2_y_Bin_9)-(z_pT_Bin_29) (165.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (150.0°), (Q2_y_Bin_9)-(z_pT_Bin_30) (105.0°)
(Q2_y_Bin_9)-(z_pT_Bin_4) (150.0°), (Q2_y_Bin_9)-(z_pT_Bin_5) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_6) (135.0°)
(Q2_y_Bin_9)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_9)-(z_pT_Bin_9) (135.0°)

Above 120° (218/452 (48.2%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_16) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°)
(Q2_y_Bin_1)-(z_pT_Bin_23) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°)
(Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_31) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_4) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_7) (150.0°)
(Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_1) (150.0°)
(Q2_y_Bin_10)-(z_pT_Bin_15) (135.0°), (Q2_y_Bin_10)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_26) (135.0°)
(Q2_y_Bin_10)-(z_pT_Bin_3) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_32) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_4) (150.0°)
(Q2_y_Bin_10)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_6) (195.0°), (Q2_y_Bin_10)-(z_pT_Bin_7) (150.0°)
(Q2_y_Bin_11)-(z_pT_Bin_1) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_21) (135.0°)
(Q2_y_Bin_11)-(z_pT_Bin_22) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_23) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_24) (255.0°)
(Q2_y_Bin_11)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_4) (270.0°), (Q2_y_Bin_11)-(z_pT_Bin_6) (150.0°)
(Q2_y_Bin_12)-(z_pT_Bin_11) (180.0°), (Q2_y_Bin_12)-(z_pT_Bin_14) (270.0°), (Q2_y_Bin_12)-(z_pT_Bin_19) (255.0°)
(Q2_y_Bin_12)-(z_pT_Bin_21) (300.0°), (Q2_y_Bin_12)-(z_pT_Bin_22) (195.0°), (Q2_y_Bin_12)-(z_pT_Bin_23) (240.0°)
(Q2_y_Bin_12)-(z_pT_Bin_24) (345.0°), (Q2_y_Bin_12)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°)
(Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_13)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_13)-(z_pT_Bin_4) (135.0°)
(Q2_y_Bin_14)-(z_pT_Bin_32) (135.0°), (Q2_y_Bin_14)-(z_pT_Bin_5) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_1) (165.0°)
(Q2_y_Bin_15)-(z_pT_Bin_15) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_22) (150.0°)
(Q2_y_Bin_15)-(z_pT_Bin_23) (165.0°), (Q2_y_Bin_15)-(z_pT_Bin_24) (210.0°), (Q2_y_Bin_16)-(z_pT_Bin_6) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_11) (135.0°)
(Q2_y_Bin_2)-(z_pT_Bin_13) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_15) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_16) (135.0°), (Q2_y_Bin_2)-(z_pT_Bin_19) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_2) (240.0°)
(Q2_y_Bin_2)-(z_pT_Bin_20) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_21) (135.0°), (Q2_y_Bin_2)-(z_pT_Bin_25) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_26) (135.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°)
(Q2_y_Bin_2)-(z_pT_Bin_32) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_33) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_34) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_4) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_8) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_9) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_12) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_14) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_15) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_17) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_18) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_19) (135.0°), (Q2_y_Bin_3)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_20) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_21) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_22) (135.0°)
(Q2_y_Bin_3)-(z_pT_Bin_23) (135.0°), (Q2_y_Bin_3)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_3) (285.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_8) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_14) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_15) (315.0°), (Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_19) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_20) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_21) (195.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (315.0°), (Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_26) (165.0°), (Q2_y_Bin_4)-(z_pT_Bin_27) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_28) (300.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (225.0°), (Q2_y_Bin_5)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_13) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_14) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_15) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_19) (150.0°)
(Q2_y_Bin_5)-(z_pT_Bin_2) (255.0°), (Q2_y_Bin_5)-(z_pT_Bin_20) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_25) (135.0°)
(Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_31) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_32) (150.0°)
(Q2_y_Bin_5)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_6) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_7) (225.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_9) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_14) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_2) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_20) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_25) (210.0°), (Q2_y_Bin_6)-(z_pT_Bin_26) (240.0°)
(Q2_y_Bin_6)-(z_pT_Bin_27) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_28) (135.0°), (Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_6) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_7) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_8) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_9) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_16) (135.0°)
(Q2_y_Bin_7)-(z_pT_Bin_17) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°)
(Q2_y_Bin_7)-(z_pT_Bin_24) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_26) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_27) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_31) (255.0°), (Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°)
(Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_34) (240.0°), (Q2_y_Bin_7)-(z_pT_Bin_35) (300.0°)
(Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_7)-(z_pT_Bin_7) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_9) (150.0°)
(Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_12) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_13) (165.0°)
(Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_16) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_18) (135.0°)
(Q2_y_Bin_8)-(z_pT_Bin_19) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_21) (135.0°)
(Q2_y_Bin_8)-(z_pT_Bin_23) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_24) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_25) (315.0°)
(Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_29) (225.0°), (Q2_y_Bin_8)-(z_pT_Bin_30) (285.0°)
(Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_9)-(z_pT_Bin_1) (210.0°), (Q2_y_Bin_9)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_9)-(z_pT_Bin_16) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_29) (165.0°)
(Q2_y_Bin_9)-(z_pT_Bin_3) (150.0°), (Q2_y_Bin_9)-(z_pT_Bin_4) (150.0°), (Q2_y_Bin_9)-(z_pT_Bin_5) (135.0°)
(Q2_y_Bin_9)-(z_pT_Bin_6) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_9) (135.0°)

Above 135° (189/452 (41.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_16) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°)
(Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_6) (165.0°)
(Q2_y_Bin_1)-(z_pT_Bin_7) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (210.0°)
(Q2_y_Bin_10)-(z_pT_Bin_1) (150.0°), (Q2_y_Bin_10)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_3) (165.0°)
(Q2_y_Bin_10)-(z_pT_Bin_32) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_4) (150.0°), (Q2_y_Bin_10)-(z_pT_Bin_5) (165.0°)
(Q2_y_Bin_10)-(z_pT_Bin_6) (195.0°), (Q2_y_Bin_10)-(z_pT_Bin_7) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_1) (150.0°)
(Q2_y_Bin_11)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_22) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_23) (225.0°)
(Q2_y_Bin_11)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_11)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_4) (270.0°)
(Q2_y_Bin_11)-(z_pT_Bin_6) (150.0°), (Q2_y_Bin_12)-(z_pT_Bin_11) (180.0°), (Q2_y_Bin_12)-(z_pT_Bin_14) (270.0°)
(Q2_y_Bin_12)-(z_pT_Bin_19) (255.0°), (Q2_y_Bin_12)-(z_pT_Bin_21) (300.0°), (Q2_y_Bin_12)-(z_pT_Bin_22) (195.0°)
(Q2_y_Bin_12)-(z_pT_Bin_23) (240.0°), (Q2_y_Bin_12)-(z_pT_Bin_24) (345.0°), (Q2_y_Bin_12)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_13)-(z_pT_Bin_1) (165.0°)
(Q2_y_Bin_14)-(z_pT_Bin_5) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (180.0°)
(Q2_y_Bin_15)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_22) (150.0°), (Q2_y_Bin_15)-(z_pT_Bin_23) (165.0°)
(Q2_y_Bin_15)-(z_pT_Bin_24) (210.0°), (Q2_y_Bin_16)-(z_pT_Bin_6) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_1) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_13) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_15) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_19) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_2) (240.0°)
(Q2_y_Bin_2)-(z_pT_Bin_20) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_25) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_32) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_33) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_34) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_4) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_8) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°)
(Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_12) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_13) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_14) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_15) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_16) (165.0°)
(Q2_y_Bin_3)-(z_pT_Bin_17) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_18) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_20) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_21) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_24) (255.0°)
(Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_3) (285.0°)
(Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_14) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_15) (315.0°)
(Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_19) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_21) (195.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (315.0°), (Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_26) (165.0°), (Q2_y_Bin_4)-(z_pT_Bin_27) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_28) (300.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (225.0°), (Q2_y_Bin_5)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_13) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_14) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_15) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_19) (150.0°)
(Q2_y_Bin_5)-(z_pT_Bin_2) (255.0°), (Q2_y_Bin_5)-(z_pT_Bin_20) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°)
(Q2_y_Bin_5)-(z_pT_Bin_31) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_32) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_4) (195.0°)
(Q2_y_Bin_5)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_7) (225.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_1) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_14) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_20) (150.0°)
(Q2_y_Bin_6)-(z_pT_Bin_25) (210.0°), (Q2_y_Bin_6)-(z_pT_Bin_26) (240.0°), (Q2_y_Bin_6)-(z_pT_Bin_27) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_7) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_8) (150.0°)
(Q2_y_Bin_6)-(z_pT_Bin_9) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_10) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_13) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_24) (195.0°)
(Q2_y_Bin_7)-(z_pT_Bin_27) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_31) (255.0°)
(Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°), (Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_34) (240.0°)
(Q2_y_Bin_7)-(z_pT_Bin_35) (300.0°), (Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_7)-(z_pT_Bin_7) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_9) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_13) (165.0°)
(Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_16) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_19) (210.0°)
(Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_24) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_25) (315.0°)
(Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_29) (225.0°), (Q2_y_Bin_8)-(z_pT_Bin_30) (285.0°)
(Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_9)-(z_pT_Bin_1) (210.0°), (Q2_y_Bin_9)-(z_pT_Bin_2) (180.0°)
(Q2_y_Bin_9)-(z_pT_Bin_29) (165.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (150.0°), (Q2_y_Bin_9)-(z_pT_Bin_4) (150.0°)

Above 150° (161/452 (35.6%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_16) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°)
(Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_6) (165.0°)
(Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_2) (165.0°)
(Q2_y_Bin_10)-(z_pT_Bin_3) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_32) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_5) (165.0°)
(Q2_y_Bin_10)-(z_pT_Bin_6) (195.0°), (Q2_y_Bin_11)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_22) (210.0°)
(Q2_y_Bin_11)-(z_pT_Bin_23) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_11)-(z_pT_Bin_3) (210.0°)
(Q2_y_Bin_11)-(z_pT_Bin_4) (270.0°), (Q2_y_Bin_12)-(z_pT_Bin_11) (180.0°), (Q2_y_Bin_12)-(z_pT_Bin_14) (270.0°)
(Q2_y_Bin_12)-(z_pT_Bin_19) (255.0°), (Q2_y_Bin_12)-(z_pT_Bin_21) (300.0°), (Q2_y_Bin_12)-(z_pT_Bin_22) (195.0°)
(Q2_y_Bin_12)-(z_pT_Bin_23) (240.0°), (Q2_y_Bin_12)-(z_pT_Bin_24) (345.0°), (Q2_y_Bin_12)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_13)-(z_pT_Bin_1) (165.0°)
(Q2_y_Bin_14)-(z_pT_Bin_5) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (180.0°)
(Q2_y_Bin_15)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_23) (165.0°), (Q2_y_Bin_15)-(z_pT_Bin_24) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_13) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_15) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_19) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_20) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_25) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_32) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_33) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_34) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_4) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°)
(Q2_y_Bin_2)-(z_pT_Bin_8) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_12) (165.0°)
(Q2_y_Bin_3)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_15) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_16) (165.0°)
(Q2_y_Bin_3)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_20) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_21) (165.0°)
(Q2_y_Bin_3)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_3) (285.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_9) (195.0°)
(Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_15) (315.0°)
(Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_19) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_21) (195.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (315.0°), (Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_26) (165.0°), (Q2_y_Bin_4)-(z_pT_Bin_27) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_28) (300.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (225.0°), (Q2_y_Bin_5)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (255.0°)
(Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_31) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_4) (195.0°)
(Q2_y_Bin_5)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_7) (225.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_1) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_25) (210.0°), (Q2_y_Bin_6)-(z_pT_Bin_26) (240.0°)
(Q2_y_Bin_6)-(z_pT_Bin_27) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_9) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°)
(Q2_y_Bin_7)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°)
(Q2_y_Bin_7)-(z_pT_Bin_24) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_31) (255.0°)
(Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°), (Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_34) (240.0°)
(Q2_y_Bin_7)-(z_pT_Bin_35) (300.0°), (Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°)
(Q2_y_Bin_8)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_16) (195.0°)
(Q2_y_Bin_8)-(z_pT_Bin_19) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_24) (210.0°)
(Q2_y_Bin_8)-(z_pT_Bin_25) (315.0°), (Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_29) (225.0°)
(Q2_y_Bin_8)-(z_pT_Bin_30) (285.0°), (Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_9)-(z_pT_Bin_1) (210.0°)
(Q2_y_Bin_9)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_29) (165.0°)

Above 180° (106/452 (23.5%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (240.0°)
(Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (210.0°)
(Q2_y_Bin_10)-(z_pT_Bin_6) (195.0°), (Q2_y_Bin_11)-(z_pT_Bin_22) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_23) (225.0°)
(Q2_y_Bin_11)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_11)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_4) (270.0°)
(Q2_y_Bin_12)-(z_pT_Bin_14) (270.0°), (Q2_y_Bin_12)-(z_pT_Bin_19) (255.0°), (Q2_y_Bin_12)-(z_pT_Bin_21) (300.0°)
(Q2_y_Bin_12)-(z_pT_Bin_22) (195.0°), (Q2_y_Bin_12)-(z_pT_Bin_23) (240.0°), (Q2_y_Bin_12)-(z_pT_Bin_24) (345.0°)
(Q2_y_Bin_12)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_15)-(z_pT_Bin_24) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_2) (240.0°)
(Q2_y_Bin_2)-(z_pT_Bin_20) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°)
(Q2_y_Bin_2)-(z_pT_Bin_32) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_4) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°), (Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_20) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_3) (285.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_9) (195.0°)
(Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_15) (315.0°)
(Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_19) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_21) (195.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (315.0°), (Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_27) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_28) (300.0°)
(Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (225.0°)
(Q2_y_Bin_5)-(z_pT_Bin_2) (255.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_31) (210.0°)
(Q2_y_Bin_5)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_7) (225.0°)
(Q2_y_Bin_6)-(z_pT_Bin_25) (210.0°), (Q2_y_Bin_6)-(z_pT_Bin_26) (240.0°), (Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°)
(Q2_y_Bin_7)-(z_pT_Bin_24) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_31) (255.0°)
(Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°), (Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_34) (240.0°)
(Q2_y_Bin_7)-(z_pT_Bin_35) (300.0°), (Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°)
(Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_16) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_19) (210.0°)
(Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_24) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_25) (315.0°)
(Q2_y_Bin_8)-(z_pT_Bin_29) (225.0°), (Q2_y_Bin_8)-(z_pT_Bin_30) (285.0°), (Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_9)-(z_pT_Bin_1) (210.0°)

### sector / P3

Stage: spline, acceptance. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/pion_sector/pipS3o/fit_copy.root`

Above 90° (305/452 (67.5%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_11) (120.0°)
(Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_17) (120.0°)
(Q2_y_Bin_1)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_23) (165.0°)
(Q2_y_Bin_1)-(z_pT_Bin_29) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_31) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_32) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_4) (240.0°)
(Q2_y_Bin_1)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_7) (150.0°)
(Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_1) (150.0°)
(Q2_y_Bin_10)-(z_pT_Bin_10) (135.0°), (Q2_y_Bin_10)-(z_pT_Bin_11) (120.0°), (Q2_y_Bin_10)-(z_pT_Bin_12) (105.0°)
(Q2_y_Bin_10)-(z_pT_Bin_13) (105.0°), (Q2_y_Bin_10)-(z_pT_Bin_15) (135.0°), (Q2_y_Bin_10)-(z_pT_Bin_2) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_20) (120.0°), (Q2_y_Bin_10)-(z_pT_Bin_21) (120.0°), (Q2_y_Bin_10)-(z_pT_Bin_26) (135.0°)
(Q2_y_Bin_10)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_31) (150.0°), (Q2_y_Bin_10)-(z_pT_Bin_32) (210.0°)
(Q2_y_Bin_10)-(z_pT_Bin_34) (105.0°), (Q2_y_Bin_10)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_5) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_7) (150.0°), (Q2_y_Bin_10)-(z_pT_Bin_8) (105.0°)
(Q2_y_Bin_10)-(z_pT_Bin_9) (120.0°), (Q2_y_Bin_11)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_10) (150.0°)
(Q2_y_Bin_11)-(z_pT_Bin_11) (105.0°), (Q2_y_Bin_11)-(z_pT_Bin_13) (105.0°), (Q2_y_Bin_11)-(z_pT_Bin_14) (105.0°)
(Q2_y_Bin_11)-(z_pT_Bin_15) (135.0°), (Q2_y_Bin_11)-(z_pT_Bin_18) (135.0°), (Q2_y_Bin_11)-(z_pT_Bin_19) (135.0°)
(Q2_y_Bin_11)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_11)-(z_pT_Bin_20) (180.0°), (Q2_y_Bin_11)-(z_pT_Bin_21) (165.0°)
(Q2_y_Bin_11)-(z_pT_Bin_22) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_23) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_24) (255.0°)
(Q2_y_Bin_11)-(z_pT_Bin_3) (240.0°), (Q2_y_Bin_11)-(z_pT_Bin_4) (300.0°), (Q2_y_Bin_11)-(z_pT_Bin_6) (165.0°)
(Q2_y_Bin_11)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_11)-(z_pT_Bin_9) (135.0°), (Q2_y_Bin_12)-(z_pT_Bin_11) (210.0°)
(Q2_y_Bin_12)-(z_pT_Bin_12) (120.0°), (Q2_y_Bin_12)-(z_pT_Bin_13) (135.0°), (Q2_y_Bin_12)-(z_pT_Bin_14) (270.0°)
(Q2_y_Bin_12)-(z_pT_Bin_16) (135.0°), (Q2_y_Bin_12)-(z_pT_Bin_18) (120.0°), (Q2_y_Bin_12)-(z_pT_Bin_19) (255.0°)
(Q2_y_Bin_12)-(z_pT_Bin_21) (345.0°), (Q2_y_Bin_12)-(z_pT_Bin_22) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_23) (270.0°)
(Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°)
(Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_13)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_13)-(z_pT_Bin_12) (105.0°)
(Q2_y_Bin_13)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_13)-(z_pT_Bin_26) (120.0°), (Q2_y_Bin_13)-(z_pT_Bin_3) (150.0°)
(Q2_y_Bin_13)-(z_pT_Bin_4) (135.0°), (Q2_y_Bin_13)-(z_pT_Bin_5) (120.0°), (Q2_y_Bin_13)-(z_pT_Bin_7) (105.0°)
(Q2_y_Bin_13)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_13)-(z_pT_Bin_9) (105.0°), (Q2_y_Bin_14)-(z_pT_Bin_1) (120.0°)
(Q2_y_Bin_14)-(z_pT_Bin_2) (150.0°), (Q2_y_Bin_14)-(z_pT_Bin_3) (135.0°), (Q2_y_Bin_14)-(z_pT_Bin_32) (150.0°)
(Q2_y_Bin_14)-(z_pT_Bin_4) (165.0°), (Q2_y_Bin_14)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_1) (180.0°)
(Q2_y_Bin_15)-(z_pT_Bin_14) (105.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (225.0°), (Q2_y_Bin_15)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_15)-(z_pT_Bin_21) (105.0°), (Q2_y_Bin_15)-(z_pT_Bin_22) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_23) (195.0°)
(Q2_y_Bin_15)-(z_pT_Bin_24) (285.0°), (Q2_y_Bin_15)-(z_pT_Bin_6) (105.0°), (Q2_y_Bin_15)-(z_pT_Bin_9) (150.0°)
(Q2_y_Bin_16)-(z_pT_Bin_1) (120.0°), (Q2_y_Bin_16)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_16)-(z_pT_Bin_4) (120.0°)
(Q2_y_Bin_16)-(z_pT_Bin_5) (135.0°), (Q2_y_Bin_16)-(z_pT_Bin_6) (180.0°), (Q2_y_Bin_16)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_17)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_17)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_17)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_17)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_1) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_10) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_11) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_12) (120.0°), (Q2_y_Bin_2)-(z_pT_Bin_13) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_15) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_16) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_17) (105.0°), (Q2_y_Bin_2)-(z_pT_Bin_18) (120.0°), (Q2_y_Bin_2)-(z_pT_Bin_19) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_20) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_21) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_23) (120.0°), (Q2_y_Bin_2)-(z_pT_Bin_25) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_26) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_27) (135.0°), (Q2_y_Bin_2)-(z_pT_Bin_28) (120.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_32) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_33) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_34) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_4) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_5) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_8) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°)
(Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_12) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_13) (210.0°)
(Q2_y_Bin_3)-(z_pT_Bin_14) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_15) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_16) (165.0°)
(Q2_y_Bin_3)-(z_pT_Bin_17) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_18) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_19) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_2) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_20) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_21) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_22) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_23) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_24) (270.0°)
(Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_3) (285.0°)
(Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_4)-(z_pT_Bin_15) (345.0°)
(Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_19) (225.0°)
(Q2_y_Bin_4)-(z_pT_Bin_20) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (345.0°)
(Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_25) (255.0°), (Q2_y_Bin_4)-(z_pT_Bin_26) (165.0°)
(Q2_y_Bin_4)-(z_pT_Bin_27) (225.0°), (Q2_y_Bin_4)-(z_pT_Bin_28) (300.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_10) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_11) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_13) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_14) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_15) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_19) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (240.0°)
(Q2_y_Bin_5)-(z_pT_Bin_20) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_21) (120.0°), (Q2_y_Bin_5)-(z_pT_Bin_25) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_26) (120.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_31) (210.0°)
(Q2_y_Bin_5)-(z_pT_Bin_32) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_5) (225.0°)
(Q2_y_Bin_5)-(z_pT_Bin_6) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_7) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_10) (150.0°)
(Q2_y_Bin_6)-(z_pT_Bin_11) (105.0°), (Q2_y_Bin_6)-(z_pT_Bin_13) (120.0°), (Q2_y_Bin_6)-(z_pT_Bin_14) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_15) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_16) (120.0°), (Q2_y_Bin_6)-(z_pT_Bin_19) (135.0°)
(Q2_y_Bin_6)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_6)-(z_pT_Bin_20) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_21) (105.0°)
(Q2_y_Bin_6)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_6)-(z_pT_Bin_26) (270.0°), (Q2_y_Bin_6)-(z_pT_Bin_27) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_28) (195.0°), (Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_7) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_8) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_9) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_1) (180.0°)
(Q2_y_Bin_7)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°)
(Q2_y_Bin_7)-(z_pT_Bin_13) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_14) (105.0°), (Q2_y_Bin_7)-(z_pT_Bin_15) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_16) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_17) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_18) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_19) (120.0°), (Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_20) (120.0°)
(Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_22) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_23) (135.0°)
(Q2_y_Bin_7)-(z_pT_Bin_24) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_25) (105.0°), (Q2_y_Bin_7)-(z_pT_Bin_26) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_27) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_28) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_29) (135.0°)
(Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_31) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°)
(Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_34) (285.0°), (Q2_y_Bin_7)-(z_pT_Bin_35) (330.0°)
(Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_7)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_8) (120.0°)
(Q2_y_Bin_7)-(z_pT_Bin_9) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_12) (150.0°)
(Q2_y_Bin_8)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_16) (210.0°)
(Q2_y_Bin_8)-(z_pT_Bin_17) (105.0°), (Q2_y_Bin_8)-(z_pT_Bin_18) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_19) (225.0°)
(Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_21) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_23) (150.0°)
(Q2_y_Bin_8)-(z_pT_Bin_24) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_25) (315.0°), (Q2_y_Bin_8)-(z_pT_Bin_26) (150.0°)
(Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_30) (330.0°)
(Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_9)-(z_pT_Bin_1) (210.0°), (Q2_y_Bin_9)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_9)-(z_pT_Bin_11) (120.0°), (Q2_y_Bin_9)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_9)-(z_pT_Bin_16) (135.0°)
(Q2_y_Bin_9)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_22) (120.0°), (Q2_y_Bin_9)-(z_pT_Bin_29) (180.0°)
(Q2_y_Bin_9)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_30) (120.0°), (Q2_y_Bin_9)-(z_pT_Bin_4) (180.0°)
(Q2_y_Bin_9)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_9)-(z_pT_Bin_6) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_7) (120.0°)
(Q2_y_Bin_9)-(z_pT_Bin_8) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_9) (120.0°)

Above 120° (250/452 (55.3%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°)
(Q2_y_Bin_1)-(z_pT_Bin_23) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_29) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°)
(Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_31) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_32) (165.0°)
(Q2_y_Bin_1)-(z_pT_Bin_4) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_6) (165.0°)
(Q2_y_Bin_1)-(z_pT_Bin_7) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (210.0°)
(Q2_y_Bin_10)-(z_pT_Bin_1) (150.0°), (Q2_y_Bin_10)-(z_pT_Bin_10) (135.0°), (Q2_y_Bin_10)-(z_pT_Bin_15) (135.0°)
(Q2_y_Bin_10)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_26) (135.0°), (Q2_y_Bin_10)-(z_pT_Bin_3) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_31) (150.0°), (Q2_y_Bin_10)-(z_pT_Bin_32) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_4) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_5) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_7) (150.0°)
(Q2_y_Bin_11)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_15) (135.0°)
(Q2_y_Bin_11)-(z_pT_Bin_18) (135.0°), (Q2_y_Bin_11)-(z_pT_Bin_19) (135.0°), (Q2_y_Bin_11)-(z_pT_Bin_2) (180.0°)
(Q2_y_Bin_11)-(z_pT_Bin_20) (180.0°), (Q2_y_Bin_11)-(z_pT_Bin_21) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_22) (225.0°)
(Q2_y_Bin_11)-(z_pT_Bin_23) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_11)-(z_pT_Bin_3) (240.0°)
(Q2_y_Bin_11)-(z_pT_Bin_4) (300.0°), (Q2_y_Bin_11)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_9) (135.0°)
(Q2_y_Bin_12)-(z_pT_Bin_11) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_13) (135.0°), (Q2_y_Bin_12)-(z_pT_Bin_14) (270.0°)
(Q2_y_Bin_12)-(z_pT_Bin_16) (135.0°), (Q2_y_Bin_12)-(z_pT_Bin_19) (255.0°), (Q2_y_Bin_12)-(z_pT_Bin_21) (345.0°)
(Q2_y_Bin_12)-(z_pT_Bin_22) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_23) (270.0°), (Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°)
(Q2_y_Bin_12)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_13)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_13)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_13)-(z_pT_Bin_3) (150.0°)
(Q2_y_Bin_13)-(z_pT_Bin_4) (135.0°), (Q2_y_Bin_14)-(z_pT_Bin_2) (150.0°), (Q2_y_Bin_14)-(z_pT_Bin_3) (135.0°)
(Q2_y_Bin_14)-(z_pT_Bin_32) (150.0°), (Q2_y_Bin_14)-(z_pT_Bin_4) (165.0°), (Q2_y_Bin_14)-(z_pT_Bin_5) (195.0°)
(Q2_y_Bin_15)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (225.0°), (Q2_y_Bin_15)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_15)-(z_pT_Bin_22) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_23) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_24) (285.0°)
(Q2_y_Bin_15)-(z_pT_Bin_9) (150.0°), (Q2_y_Bin_16)-(z_pT_Bin_5) (135.0°), (Q2_y_Bin_16)-(z_pT_Bin_6) (180.0°)
(Q2_y_Bin_17)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_17)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_17)-(z_pT_Bin_4) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_1) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_10) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_11) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_15) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_19) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_2) (240.0°)
(Q2_y_Bin_2)-(z_pT_Bin_20) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_21) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_25) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_26) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_27) (135.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_32) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_33) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_34) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_4) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_5) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_8) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°)
(Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_12) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_13) (210.0°)
(Q2_y_Bin_3)-(z_pT_Bin_14) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_15) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_16) (165.0°)
(Q2_y_Bin_3)-(z_pT_Bin_17) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_18) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_19) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_2) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_20) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_21) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_22) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_23) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_24) (270.0°)
(Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_3) (285.0°)
(Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_4)-(z_pT_Bin_15) (345.0°)
(Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_19) (225.0°)
(Q2_y_Bin_4)-(z_pT_Bin_20) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (345.0°)
(Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_25) (255.0°), (Q2_y_Bin_4)-(z_pT_Bin_26) (165.0°)
(Q2_y_Bin_4)-(z_pT_Bin_27) (225.0°), (Q2_y_Bin_4)-(z_pT_Bin_28) (300.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_10) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_13) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_15) (150.0°)
(Q2_y_Bin_5)-(z_pT_Bin_19) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_20) (150.0°)
(Q2_y_Bin_5)-(z_pT_Bin_25) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_31) (210.0°)
(Q2_y_Bin_5)-(z_pT_Bin_32) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_5) (225.0°)
(Q2_y_Bin_5)-(z_pT_Bin_6) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_7) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_10) (150.0°)
(Q2_y_Bin_6)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_15) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_19) (135.0°)
(Q2_y_Bin_6)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_6)-(z_pT_Bin_20) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_25) (240.0°)
(Q2_y_Bin_6)-(z_pT_Bin_26) (270.0°), (Q2_y_Bin_6)-(z_pT_Bin_27) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_28) (195.0°)
(Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_7) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_8) (150.0°)
(Q2_y_Bin_6)-(z_pT_Bin_9) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_10) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_13) (180.0°)
(Q2_y_Bin_7)-(z_pT_Bin_15) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_16) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_17) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_18) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°)
(Q2_y_Bin_7)-(z_pT_Bin_22) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_23) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_24) (210.0°)
(Q2_y_Bin_7)-(z_pT_Bin_26) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_27) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_28) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_29) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_31) (270.0°)
(Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°), (Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_34) (285.0°)
(Q2_y_Bin_7)-(z_pT_Bin_35) (330.0°), (Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_7)-(z_pT_Bin_7) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_9) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_12) (150.0°)
(Q2_y_Bin_8)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_16) (210.0°)
(Q2_y_Bin_8)-(z_pT_Bin_18) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_19) (225.0°), (Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_21) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_23) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_24) (240.0°)
(Q2_y_Bin_8)-(z_pT_Bin_25) (315.0°), (Q2_y_Bin_8)-(z_pT_Bin_26) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°)
(Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_30) (330.0°), (Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_9)-(z_pT_Bin_1) (210.0°), (Q2_y_Bin_9)-(z_pT_Bin_10) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_16) (135.0°)
(Q2_y_Bin_9)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_29) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (180.0°)
(Q2_y_Bin_9)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_9)-(z_pT_Bin_6) (135.0°)
(Q2_y_Bin_9)-(z_pT_Bin_8) (135.0°)

Above 135° (229/452 (50.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°)
(Q2_y_Bin_1)-(z_pT_Bin_23) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_29) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°)
(Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_31) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_32) (165.0°)
(Q2_y_Bin_1)-(z_pT_Bin_4) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_6) (165.0°)
(Q2_y_Bin_1)-(z_pT_Bin_7) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (210.0°)
(Q2_y_Bin_10)-(z_pT_Bin_1) (150.0°), (Q2_y_Bin_10)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_3) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_31) (150.0°), (Q2_y_Bin_10)-(z_pT_Bin_32) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_4) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_5) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_7) (150.0°)
(Q2_y_Bin_11)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_2) (180.0°)
(Q2_y_Bin_11)-(z_pT_Bin_20) (180.0°), (Q2_y_Bin_11)-(z_pT_Bin_21) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_22) (225.0°)
(Q2_y_Bin_11)-(z_pT_Bin_23) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_11)-(z_pT_Bin_3) (240.0°)
(Q2_y_Bin_11)-(z_pT_Bin_4) (300.0°), (Q2_y_Bin_11)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_12)-(z_pT_Bin_11) (210.0°)
(Q2_y_Bin_12)-(z_pT_Bin_14) (270.0°), (Q2_y_Bin_12)-(z_pT_Bin_19) (255.0°), (Q2_y_Bin_12)-(z_pT_Bin_21) (345.0°)
(Q2_y_Bin_12)-(z_pT_Bin_22) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_23) (270.0°), (Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°)
(Q2_y_Bin_12)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_13)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_13)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_13)-(z_pT_Bin_3) (150.0°)
(Q2_y_Bin_14)-(z_pT_Bin_2) (150.0°), (Q2_y_Bin_14)-(z_pT_Bin_32) (150.0°), (Q2_y_Bin_14)-(z_pT_Bin_4) (165.0°)
(Q2_y_Bin_14)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (225.0°)
(Q2_y_Bin_15)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_22) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_23) (195.0°)
(Q2_y_Bin_15)-(z_pT_Bin_24) (285.0°), (Q2_y_Bin_15)-(z_pT_Bin_9) (150.0°), (Q2_y_Bin_16)-(z_pT_Bin_6) (180.0°)
(Q2_y_Bin_17)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_17)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_1) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_10) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_11) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_13) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_15) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_16) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_19) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_20) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_21) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_25) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_26) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_32) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_33) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_34) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_4) (240.0°)
(Q2_y_Bin_2)-(z_pT_Bin_5) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°)
(Q2_y_Bin_2)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_12) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_14) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_17) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_18) (165.0°)
(Q2_y_Bin_3)-(z_pT_Bin_19) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_2) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_20) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_21) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_22) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_23) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_24) (270.0°), (Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_3) (285.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_9) (180.0°)
(Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_14) (165.0°)
(Q2_y_Bin_4)-(z_pT_Bin_15) (345.0°), (Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_19) (225.0°), (Q2_y_Bin_4)-(z_pT_Bin_20) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_22) (345.0°), (Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_25) (255.0°)
(Q2_y_Bin_4)-(z_pT_Bin_26) (165.0°), (Q2_y_Bin_4)-(z_pT_Bin_27) (225.0°), (Q2_y_Bin_4)-(z_pT_Bin_28) (300.0°)
(Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (240.0°)
(Q2_y_Bin_5)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_13) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_14) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_15) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_19) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (240.0°)
(Q2_y_Bin_5)-(z_pT_Bin_20) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_25) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°)
(Q2_y_Bin_5)-(z_pT_Bin_31) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_32) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_4) (195.0°)
(Q2_y_Bin_5)-(z_pT_Bin_5) (225.0°), (Q2_y_Bin_5)-(z_pT_Bin_6) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_7) (240.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_1) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_15) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_6)-(z_pT_Bin_20) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_25) (240.0°)
(Q2_y_Bin_6)-(z_pT_Bin_26) (270.0°), (Q2_y_Bin_6)-(z_pT_Bin_27) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_28) (195.0°)
(Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_7) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_8) (150.0°)
(Q2_y_Bin_6)-(z_pT_Bin_9) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_10) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_13) (180.0°)
(Q2_y_Bin_7)-(z_pT_Bin_15) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_16) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_17) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_18) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°)
(Q2_y_Bin_7)-(z_pT_Bin_22) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_24) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_26) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_27) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_28) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°)
(Q2_y_Bin_7)-(z_pT_Bin_31) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°), (Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°)
(Q2_y_Bin_7)-(z_pT_Bin_34) (285.0°), (Q2_y_Bin_7)-(z_pT_Bin_35) (330.0°), (Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°)
(Q2_y_Bin_7)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_9) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°)
(Q2_y_Bin_8)-(z_pT_Bin_12) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_16) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_18) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_19) (225.0°)
(Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_21) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_23) (150.0°)
(Q2_y_Bin_8)-(z_pT_Bin_24) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_25) (315.0°), (Q2_y_Bin_8)-(z_pT_Bin_26) (150.0°)
(Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_30) (330.0°)
(Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_9)-(z_pT_Bin_1) (210.0°), (Q2_y_Bin_9)-(z_pT_Bin_2) (180.0°)
(Q2_y_Bin_9)-(z_pT_Bin_29) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_4) (180.0°)
(Q2_y_Bin_9)-(z_pT_Bin_5) (165.0°)

Above 150° (195/452 (43.1%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°)
(Q2_y_Bin_1)-(z_pT_Bin_23) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_29) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°)
(Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_32) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_4) (240.0°)
(Q2_y_Bin_1)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°)
(Q2_y_Bin_1)-(z_pT_Bin_9) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_3) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_32) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_5) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_2) (180.0°)
(Q2_y_Bin_11)-(z_pT_Bin_20) (180.0°), (Q2_y_Bin_11)-(z_pT_Bin_21) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_22) (225.0°)
(Q2_y_Bin_11)-(z_pT_Bin_23) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_11)-(z_pT_Bin_3) (240.0°)
(Q2_y_Bin_11)-(z_pT_Bin_4) (300.0°), (Q2_y_Bin_11)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_12)-(z_pT_Bin_11) (210.0°)
(Q2_y_Bin_12)-(z_pT_Bin_14) (270.0°), (Q2_y_Bin_12)-(z_pT_Bin_19) (255.0°), (Q2_y_Bin_12)-(z_pT_Bin_21) (345.0°)
(Q2_y_Bin_12)-(z_pT_Bin_22) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_23) (270.0°), (Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°)
(Q2_y_Bin_12)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_13)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_13)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_14)-(z_pT_Bin_4) (165.0°)
(Q2_y_Bin_14)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (225.0°)
(Q2_y_Bin_15)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_22) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_23) (195.0°)
(Q2_y_Bin_15)-(z_pT_Bin_24) (285.0°), (Q2_y_Bin_16)-(z_pT_Bin_6) (180.0°), (Q2_y_Bin_17)-(z_pT_Bin_2) (165.0°)
(Q2_y_Bin_17)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_1) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_10) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_15) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_19) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_2) (240.0°)
(Q2_y_Bin_2)-(z_pT_Bin_20) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_25) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_32) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_33) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_34) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_4) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_5) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_8) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°)
(Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_12) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_13) (210.0°)
(Q2_y_Bin_3)-(z_pT_Bin_15) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_17) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_18) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_2) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_20) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_21) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_22) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_24) (270.0°)
(Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_3) (285.0°)
(Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_4)-(z_pT_Bin_15) (345.0°)
(Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_19) (225.0°)
(Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (345.0°), (Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_25) (255.0°), (Q2_y_Bin_4)-(z_pT_Bin_26) (165.0°), (Q2_y_Bin_4)-(z_pT_Bin_27) (225.0°)
(Q2_y_Bin_4)-(z_pT_Bin_28) (300.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_13) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_19) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (240.0°)
(Q2_y_Bin_5)-(z_pT_Bin_25) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_31) (210.0°)
(Q2_y_Bin_5)-(z_pT_Bin_32) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_5) (225.0°)
(Q2_y_Bin_5)-(z_pT_Bin_6) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_7) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_14) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_15) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_6)-(z_pT_Bin_20) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_6)-(z_pT_Bin_26) (270.0°), (Q2_y_Bin_6)-(z_pT_Bin_27) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_28) (195.0°), (Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_7) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_9) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_13) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_24) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_26) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_31) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°)
(Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_34) (285.0°), (Q2_y_Bin_7)-(z_pT_Bin_35) (330.0°)
(Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_7)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°)
(Q2_y_Bin_8)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_16) (210.0°)
(Q2_y_Bin_8)-(z_pT_Bin_19) (225.0°), (Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_21) (180.0°)
(Q2_y_Bin_8)-(z_pT_Bin_24) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_25) (315.0°), (Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°)
(Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_30) (330.0°), (Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_9)-(z_pT_Bin_1) (210.0°), (Q2_y_Bin_9)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_29) (180.0°)
(Q2_y_Bin_9)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_5) (165.0°)

Above 180° (123/452 (27.2%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_29) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°)
(Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_4) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_5) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_32) (210.0°)
(Q2_y_Bin_10)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_22) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_23) (225.0°)
(Q2_y_Bin_11)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_11)-(z_pT_Bin_3) (240.0°), (Q2_y_Bin_11)-(z_pT_Bin_4) (300.0°)
(Q2_y_Bin_12)-(z_pT_Bin_11) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_14) (270.0°), (Q2_y_Bin_12)-(z_pT_Bin_19) (255.0°)
(Q2_y_Bin_12)-(z_pT_Bin_21) (345.0°), (Q2_y_Bin_12)-(z_pT_Bin_22) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_23) (270.0°)
(Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°)
(Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_14)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (225.0°)
(Q2_y_Bin_15)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_23) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_24) (285.0°)
(Q2_y_Bin_2)-(z_pT_Bin_1) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_10) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_19) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_20) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_32) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_4) (240.0°)
(Q2_y_Bin_2)-(z_pT_Bin_5) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°)
(Q2_y_Bin_2)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°)
(Q2_y_Bin_3)-(z_pT_Bin_12) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_2) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_20) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_21) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_24) (270.0°), (Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_3) (285.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_15) (345.0°), (Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_19) (225.0°), (Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (345.0°)
(Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_25) (255.0°), (Q2_y_Bin_4)-(z_pT_Bin_27) (225.0°)
(Q2_y_Bin_4)-(z_pT_Bin_28) (300.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°)
(Q2_y_Bin_5)-(z_pT_Bin_31) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_5) (225.0°)
(Q2_y_Bin_5)-(z_pT_Bin_7) (240.0°), (Q2_y_Bin_6)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_6)-(z_pT_Bin_25) (240.0°)
(Q2_y_Bin_6)-(z_pT_Bin_26) (270.0°), (Q2_y_Bin_6)-(z_pT_Bin_28) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°)
(Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_24) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°)
(Q2_y_Bin_7)-(z_pT_Bin_31) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°), (Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°)
(Q2_y_Bin_7)-(z_pT_Bin_34) (285.0°), (Q2_y_Bin_7)-(z_pT_Bin_35) (330.0°), (Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_16) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_19) (225.0°), (Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_24) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_25) (315.0°), (Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°)
(Q2_y_Bin_8)-(z_pT_Bin_30) (330.0°), (Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_9)-(z_pT_Bin_1) (210.0°)

### sector / E4

Stage: spline, acceptance. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/electron_sector/eS4o/fit_copy.root`

Above 90° (283/452 (62.6%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (270.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_11) (105.0°)
(Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_17) (105.0°)
(Q2_y_Bin_1)-(z_pT_Bin_2) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_23) (120.0°)
(Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_31) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_32) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_4) (210.0°)
(Q2_y_Bin_1)-(z_pT_Bin_5) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_7) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_1) (150.0°)
(Q2_y_Bin_10)-(z_pT_Bin_10) (120.0°), (Q2_y_Bin_10)-(z_pT_Bin_15) (105.0°), (Q2_y_Bin_10)-(z_pT_Bin_2) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_20) (105.0°), (Q2_y_Bin_10)-(z_pT_Bin_26) (120.0°), (Q2_y_Bin_10)-(z_pT_Bin_3) (165.0°)
(Q2_y_Bin_10)-(z_pT_Bin_31) (120.0°), (Q2_y_Bin_10)-(z_pT_Bin_32) (150.0°), (Q2_y_Bin_10)-(z_pT_Bin_4) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_6) (195.0°), (Q2_y_Bin_10)-(z_pT_Bin_7) (150.0°)
(Q2_y_Bin_10)-(z_pT_Bin_9) (120.0°), (Q2_y_Bin_11)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_11)-(z_pT_Bin_13) (120.0°), (Q2_y_Bin_11)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_11)-(z_pT_Bin_18) (105.0°)
(Q2_y_Bin_11)-(z_pT_Bin_19) (105.0°), (Q2_y_Bin_11)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_20) (150.0°)
(Q2_y_Bin_11)-(z_pT_Bin_21) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_22) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_23) (195.0°)
(Q2_y_Bin_11)-(z_pT_Bin_24) (270.0°), (Q2_y_Bin_11)-(z_pT_Bin_3) (240.0°), (Q2_y_Bin_11)-(z_pT_Bin_4) (285.0°)
(Q2_y_Bin_11)-(z_pT_Bin_6) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_9) (120.0°), (Q2_y_Bin_12)-(z_pT_Bin_11) (195.0°)
(Q2_y_Bin_12)-(z_pT_Bin_13) (105.0°), (Q2_y_Bin_12)-(z_pT_Bin_14) (285.0°), (Q2_y_Bin_12)-(z_pT_Bin_16) (105.0°)
(Q2_y_Bin_12)-(z_pT_Bin_18) (120.0°), (Q2_y_Bin_12)-(z_pT_Bin_19) (255.0°), (Q2_y_Bin_12)-(z_pT_Bin_21) (315.0°)
(Q2_y_Bin_12)-(z_pT_Bin_22) (195.0°), (Q2_y_Bin_12)-(z_pT_Bin_23) (255.0°), (Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°)
(Q2_y_Bin_12)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_13)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_13)-(z_pT_Bin_12) (105.0°), (Q2_y_Bin_13)-(z_pT_Bin_17) (105.0°)
(Q2_y_Bin_13)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_13)-(z_pT_Bin_26) (120.0°), (Q2_y_Bin_13)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_13)-(z_pT_Bin_4) (150.0°), (Q2_y_Bin_13)-(z_pT_Bin_5) (105.0°), (Q2_y_Bin_13)-(z_pT_Bin_7) (105.0°)
(Q2_y_Bin_14)-(z_pT_Bin_1) (120.0°), (Q2_y_Bin_14)-(z_pT_Bin_2) (150.0°), (Q2_y_Bin_14)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_14)-(z_pT_Bin_32) (135.0°), (Q2_y_Bin_14)-(z_pT_Bin_4) (105.0°), (Q2_y_Bin_14)-(z_pT_Bin_5) (180.0°)
(Q2_y_Bin_15)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (210.0°), (Q2_y_Bin_15)-(z_pT_Bin_19) (105.0°)
(Q2_y_Bin_15)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_21) (105.0°), (Q2_y_Bin_15)-(z_pT_Bin_22) (135.0°)
(Q2_y_Bin_15)-(z_pT_Bin_23) (165.0°), (Q2_y_Bin_15)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_15)-(z_pT_Bin_9) (120.0°)
(Q2_y_Bin_16)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_16)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_16)-(z_pT_Bin_4) (120.0°)
(Q2_y_Bin_16)-(z_pT_Bin_5) (105.0°), (Q2_y_Bin_16)-(z_pT_Bin_6) (150.0°), (Q2_y_Bin_16)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_17)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_2)-(z_pT_Bin_1) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_10) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_11) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_12) (120.0°), (Q2_y_Bin_2)-(z_pT_Bin_13) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_15) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_16) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_18) (105.0°), (Q2_y_Bin_2)-(z_pT_Bin_19) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_2) (255.0°)
(Q2_y_Bin_2)-(z_pT_Bin_20) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_21) (135.0°), (Q2_y_Bin_2)-(z_pT_Bin_23) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_25) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_26) (135.0°), (Q2_y_Bin_2)-(z_pT_Bin_27) (135.0°)
(Q2_y_Bin_2)-(z_pT_Bin_28) (105.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°)
(Q2_y_Bin_2)-(z_pT_Bin_32) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_33) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_34) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_4) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_8) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_9) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_12) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_14) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_15) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_17) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_18) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_19) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_2) (240.0°)
(Q2_y_Bin_3)-(z_pT_Bin_20) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_21) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_22) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_23) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_24) (270.0°), (Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_29) (345.0°), (Q2_y_Bin_3)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_8) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_4)-(z_pT_Bin_15) (345.0°), (Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_19) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_20) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (300.0°), (Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_26) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_27) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_28) (315.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_10) (135.0°), (Q2_y_Bin_5)-(z_pT_Bin_13) (195.0°)
(Q2_y_Bin_5)-(z_pT_Bin_14) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_15) (135.0°), (Q2_y_Bin_5)-(z_pT_Bin_19) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_2) (255.0°), (Q2_y_Bin_5)-(z_pT_Bin_20) (135.0°), (Q2_y_Bin_5)-(z_pT_Bin_25) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_26) (120.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_31) (195.0°)
(Q2_y_Bin_5)-(z_pT_Bin_32) (135.0°), (Q2_y_Bin_5)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_5) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_7) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_6)-(z_pT_Bin_11) (105.0°), (Q2_y_Bin_6)-(z_pT_Bin_13) (120.0°), (Q2_y_Bin_6)-(z_pT_Bin_14) (150.0°)
(Q2_y_Bin_6)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_6)-(z_pT_Bin_16) (120.0°), (Q2_y_Bin_6)-(z_pT_Bin_19) (120.0°)
(Q2_y_Bin_6)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_6)-(z_pT_Bin_20) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_25) (240.0°)
(Q2_y_Bin_6)-(z_pT_Bin_26) (225.0°), (Q2_y_Bin_6)-(z_pT_Bin_27) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_28) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_6) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_6)-(z_pT_Bin_8) (150.0°)
(Q2_y_Bin_6)-(z_pT_Bin_9) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_10) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_13) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_15) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_16) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_17) (135.0°)
(Q2_y_Bin_7)-(z_pT_Bin_18) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_19) (120.0°), (Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_7)-(z_pT_Bin_20) (120.0°), (Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_22) (120.0°)
(Q2_y_Bin_7)-(z_pT_Bin_23) (120.0°), (Q2_y_Bin_7)-(z_pT_Bin_24) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_25) (105.0°)
(Q2_y_Bin_7)-(z_pT_Bin_26) (120.0°), (Q2_y_Bin_7)-(z_pT_Bin_27) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_28) (120.0°)
(Q2_y_Bin_7)-(z_pT_Bin_29) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_31) (225.0°)
(Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°), (Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_34) (255.0°)
(Q2_y_Bin_7)-(z_pT_Bin_35) (330.0°), (Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_7)-(z_pT_Bin_7) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_8) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_9) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°)
(Q2_y_Bin_8)-(z_pT_Bin_12) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_16) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_18) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_19) (210.0°)
(Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_21) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_23) (135.0°)
(Q2_y_Bin_8)-(z_pT_Bin_24) (225.0°), (Q2_y_Bin_8)-(z_pT_Bin_25) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_26) (135.0°)
(Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_30) (315.0°)
(Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_9)-(z_pT_Bin_1) (225.0°), (Q2_y_Bin_9)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_9)-(z_pT_Bin_11) (120.0°), (Q2_y_Bin_9)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_9)-(z_pT_Bin_16) (120.0°)
(Q2_y_Bin_9)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_9)-(z_pT_Bin_22) (120.0°), (Q2_y_Bin_9)-(z_pT_Bin_29) (150.0°)
(Q2_y_Bin_9)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_30) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_4) (180.0°)
(Q2_y_Bin_9)-(z_pT_Bin_5) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_6) (120.0°), (Q2_y_Bin_9)-(z_pT_Bin_8) (150.0°)
(Q2_y_Bin_9)-(z_pT_Bin_9) (135.0°)

Above 120° (225/452 (49.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (270.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°)
(Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_31) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_32) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_4) (210.0°)
(Q2_y_Bin_1)-(z_pT_Bin_5) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_7) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_1) (150.0°)
(Q2_y_Bin_10)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_3) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_32) (150.0°)
(Q2_y_Bin_10)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_6) (195.0°)
(Q2_y_Bin_10)-(z_pT_Bin_7) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_11)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_20) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_21) (165.0°)
(Q2_y_Bin_11)-(z_pT_Bin_22) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_23) (195.0°), (Q2_y_Bin_11)-(z_pT_Bin_24) (270.0°)
(Q2_y_Bin_11)-(z_pT_Bin_3) (240.0°), (Q2_y_Bin_11)-(z_pT_Bin_4) (285.0°), (Q2_y_Bin_11)-(z_pT_Bin_6) (150.0°)
(Q2_y_Bin_12)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_12)-(z_pT_Bin_14) (285.0°), (Q2_y_Bin_12)-(z_pT_Bin_19) (255.0°)
(Q2_y_Bin_12)-(z_pT_Bin_21) (315.0°), (Q2_y_Bin_12)-(z_pT_Bin_22) (195.0°), (Q2_y_Bin_12)-(z_pT_Bin_23) (255.0°)
(Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°)
(Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_13)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_13)-(z_pT_Bin_2) (165.0°)
(Q2_y_Bin_13)-(z_pT_Bin_4) (150.0°), (Q2_y_Bin_14)-(z_pT_Bin_2) (150.0°), (Q2_y_Bin_14)-(z_pT_Bin_32) (135.0°)
(Q2_y_Bin_14)-(z_pT_Bin_5) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (210.0°)
(Q2_y_Bin_15)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_22) (135.0°), (Q2_y_Bin_15)-(z_pT_Bin_23) (165.0°)
(Q2_y_Bin_15)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_16)-(z_pT_Bin_6) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_1) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_11) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_13) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_15) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_16) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_19) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_2) (255.0°), (Q2_y_Bin_2)-(z_pT_Bin_20) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_21) (135.0°), (Q2_y_Bin_2)-(z_pT_Bin_25) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_26) (135.0°)
(Q2_y_Bin_2)-(z_pT_Bin_27) (135.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°)
(Q2_y_Bin_2)-(z_pT_Bin_32) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_33) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_34) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_4) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_8) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_9) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_12) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_14) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_15) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_17) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_18) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_19) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_2) (240.0°)
(Q2_y_Bin_3)-(z_pT_Bin_20) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_21) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_22) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_23) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_24) (270.0°), (Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_29) (345.0°), (Q2_y_Bin_3)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_8) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_4)-(z_pT_Bin_15) (345.0°), (Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_19) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_20) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (300.0°), (Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_26) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_27) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_28) (315.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_10) (135.0°), (Q2_y_Bin_5)-(z_pT_Bin_13) (195.0°)
(Q2_y_Bin_5)-(z_pT_Bin_14) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_15) (135.0°), (Q2_y_Bin_5)-(z_pT_Bin_19) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_2) (255.0°), (Q2_y_Bin_5)-(z_pT_Bin_20) (135.0°), (Q2_y_Bin_5)-(z_pT_Bin_25) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_31) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_32) (135.0°)
(Q2_y_Bin_5)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_5) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_6) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_7) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_9) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_10) (135.0°), (Q2_y_Bin_6)-(z_pT_Bin_14) (150.0°)
(Q2_y_Bin_6)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_6)-(z_pT_Bin_20) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_25) (240.0°)
(Q2_y_Bin_6)-(z_pT_Bin_26) (225.0°), (Q2_y_Bin_6)-(z_pT_Bin_27) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_28) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_6) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_6)-(z_pT_Bin_8) (150.0°)
(Q2_y_Bin_6)-(z_pT_Bin_9) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_10) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_13) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_15) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_16) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_17) (135.0°)
(Q2_y_Bin_7)-(z_pT_Bin_18) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°)
(Q2_y_Bin_7)-(z_pT_Bin_24) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_27) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_29) (135.0°)
(Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_31) (225.0°), (Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°)
(Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_34) (255.0°), (Q2_y_Bin_7)-(z_pT_Bin_35) (330.0°)
(Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_7)-(z_pT_Bin_7) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_8) (135.0°)
(Q2_y_Bin_7)-(z_pT_Bin_9) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_12) (135.0°)
(Q2_y_Bin_8)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_16) (195.0°)
(Q2_y_Bin_8)-(z_pT_Bin_18) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_19) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_21) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_23) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_24) (225.0°)
(Q2_y_Bin_8)-(z_pT_Bin_25) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_26) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°)
(Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_30) (315.0°), (Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_9)-(z_pT_Bin_1) (225.0°), (Q2_y_Bin_9)-(z_pT_Bin_10) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_9)-(z_pT_Bin_29) (150.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_4) (180.0°)
(Q2_y_Bin_9)-(z_pT_Bin_5) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_8) (150.0°), (Q2_y_Bin_9)-(z_pT_Bin_9) (135.0°)

Above 135° (197/452 (43.6%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (270.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°)
(Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_4) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_5) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_6) (165.0°)
(Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_1) (150.0°)
(Q2_y_Bin_10)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_3) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_32) (150.0°)
(Q2_y_Bin_10)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_6) (195.0°)
(Q2_y_Bin_10)-(z_pT_Bin_7) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_2) (165.0°)
(Q2_y_Bin_11)-(z_pT_Bin_20) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_21) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_22) (210.0°)
(Q2_y_Bin_11)-(z_pT_Bin_23) (195.0°), (Q2_y_Bin_11)-(z_pT_Bin_24) (270.0°), (Q2_y_Bin_11)-(z_pT_Bin_3) (240.0°)
(Q2_y_Bin_11)-(z_pT_Bin_4) (285.0°), (Q2_y_Bin_11)-(z_pT_Bin_6) (150.0°), (Q2_y_Bin_12)-(z_pT_Bin_11) (195.0°)
(Q2_y_Bin_12)-(z_pT_Bin_14) (285.0°), (Q2_y_Bin_12)-(z_pT_Bin_19) (255.0°), (Q2_y_Bin_12)-(z_pT_Bin_21) (315.0°)
(Q2_y_Bin_12)-(z_pT_Bin_22) (195.0°), (Q2_y_Bin_12)-(z_pT_Bin_23) (255.0°), (Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°)
(Q2_y_Bin_12)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_13)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_13)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_13)-(z_pT_Bin_4) (150.0°)
(Q2_y_Bin_14)-(z_pT_Bin_2) (150.0°), (Q2_y_Bin_14)-(z_pT_Bin_5) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_1) (165.0°)
(Q2_y_Bin_15)-(z_pT_Bin_15) (210.0°), (Q2_y_Bin_15)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_23) (165.0°)
(Q2_y_Bin_15)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_16)-(z_pT_Bin_6) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_1) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_11) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_13) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_15) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_16) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_19) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_2) (255.0°), (Q2_y_Bin_2)-(z_pT_Bin_20) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_25) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°)
(Q2_y_Bin_2)-(z_pT_Bin_32) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_33) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_34) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_4) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_8) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_9) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_12) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_14) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_15) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_17) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_18) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_19) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_2) (240.0°)
(Q2_y_Bin_3)-(z_pT_Bin_20) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_21) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_22) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_23) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_24) (270.0°), (Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_29) (345.0°), (Q2_y_Bin_3)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_8) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_4)-(z_pT_Bin_15) (345.0°), (Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_19) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_22) (300.0°), (Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°)
(Q2_y_Bin_4)-(z_pT_Bin_26) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_27) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_28) (315.0°)
(Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (240.0°)
(Q2_y_Bin_5)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_14) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_19) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_2) (255.0°), (Q2_y_Bin_5)-(z_pT_Bin_25) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°)
(Q2_y_Bin_5)-(z_pT_Bin_31) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_5) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_7) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_14) (150.0°)
(Q2_y_Bin_6)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_6)-(z_pT_Bin_20) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_25) (240.0°)
(Q2_y_Bin_6)-(z_pT_Bin_26) (225.0°), (Q2_y_Bin_6)-(z_pT_Bin_27) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_28) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_6) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_6)-(z_pT_Bin_8) (150.0°)
(Q2_y_Bin_6)-(z_pT_Bin_9) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_10) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_13) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_24) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_27) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_31) (225.0°)
(Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°), (Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_34) (255.0°)
(Q2_y_Bin_7)-(z_pT_Bin_35) (330.0°), (Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_7)-(z_pT_Bin_7) (150.0°)
(Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_16) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_18) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_19) (210.0°)
(Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_21) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_24) (225.0°)
(Q2_y_Bin_8)-(z_pT_Bin_25) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°)
(Q2_y_Bin_8)-(z_pT_Bin_30) (315.0°), (Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_9)-(z_pT_Bin_1) (225.0°)
(Q2_y_Bin_9)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_9)-(z_pT_Bin_29) (150.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (180.0°)
(Q2_y_Bin_9)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_8) (150.0°)

Above 150° (167/452 (36.9%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (270.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°)
(Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_4) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_5) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_6) (165.0°)
(Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_2) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_3) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_5) (165.0°)
(Q2_y_Bin_10)-(z_pT_Bin_6) (195.0°), (Q2_y_Bin_11)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_2) (165.0°)
(Q2_y_Bin_11)-(z_pT_Bin_21) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_22) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_23) (195.0°)
(Q2_y_Bin_11)-(z_pT_Bin_24) (270.0°), (Q2_y_Bin_11)-(z_pT_Bin_3) (240.0°), (Q2_y_Bin_11)-(z_pT_Bin_4) (285.0°)
(Q2_y_Bin_12)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_12)-(z_pT_Bin_14) (285.0°), (Q2_y_Bin_12)-(z_pT_Bin_19) (255.0°)
(Q2_y_Bin_12)-(z_pT_Bin_21) (315.0°), (Q2_y_Bin_12)-(z_pT_Bin_22) (195.0°), (Q2_y_Bin_12)-(z_pT_Bin_23) (255.0°)
(Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°)
(Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_13)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_13)-(z_pT_Bin_2) (165.0°)
(Q2_y_Bin_14)-(z_pT_Bin_5) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (210.0°)
(Q2_y_Bin_15)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_23) (165.0°), (Q2_y_Bin_15)-(z_pT_Bin_24) (255.0°)
(Q2_y_Bin_2)-(z_pT_Bin_1) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_13) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_15) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_19) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_2) (255.0°), (Q2_y_Bin_2)-(z_pT_Bin_20) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_25) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_32) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_4) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_8) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_9) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_12) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_15) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_18) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_2) (240.0°)
(Q2_y_Bin_3)-(z_pT_Bin_20) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_21) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_24) (270.0°)
(Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_29) (345.0°), (Q2_y_Bin_3)-(z_pT_Bin_3) (270.0°)
(Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_4)-(z_pT_Bin_15) (345.0°)
(Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_19) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (300.0°), (Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_27) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_28) (315.0°)
(Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (240.0°)
(Q2_y_Bin_5)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_19) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (255.0°)
(Q2_y_Bin_5)-(z_pT_Bin_25) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_31) (195.0°)
(Q2_y_Bin_5)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_5) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_6) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_7) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_9) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_6)-(z_pT_Bin_25) (240.0°)
(Q2_y_Bin_6)-(z_pT_Bin_26) (225.0°), (Q2_y_Bin_6)-(z_pT_Bin_27) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_28) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_6)-(z_pT_Bin_9) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_1) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_13) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_24) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_31) (225.0°), (Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°)
(Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_34) (255.0°), (Q2_y_Bin_7)-(z_pT_Bin_35) (330.0°)
(Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_13) (165.0°)
(Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_16) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_19) (210.0°)
(Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_24) (225.0°), (Q2_y_Bin_8)-(z_pT_Bin_25) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_30) (315.0°)
(Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_9)-(z_pT_Bin_1) (225.0°), (Q2_y_Bin_9)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_9)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_4) (180.0°)

Above 180° (110/452 (24.3%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (270.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_2) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°)
(Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_4) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°)
(Q2_y_Bin_1)-(z_pT_Bin_9) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_6) (195.0°), (Q2_y_Bin_11)-(z_pT_Bin_22) (210.0°)
(Q2_y_Bin_11)-(z_pT_Bin_23) (195.0°), (Q2_y_Bin_11)-(z_pT_Bin_24) (270.0°), (Q2_y_Bin_11)-(z_pT_Bin_3) (240.0°)
(Q2_y_Bin_11)-(z_pT_Bin_4) (285.0°), (Q2_y_Bin_12)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_12)-(z_pT_Bin_14) (285.0°)
(Q2_y_Bin_12)-(z_pT_Bin_19) (255.0°), (Q2_y_Bin_12)-(z_pT_Bin_21) (315.0°), (Q2_y_Bin_12)-(z_pT_Bin_22) (195.0°)
(Q2_y_Bin_12)-(z_pT_Bin_23) (255.0°), (Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (210.0°)
(Q2_y_Bin_15)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_2)-(z_pT_Bin_1) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_2) (255.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_32) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_4) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°), (Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°)
(Q2_y_Bin_3)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_3)-(z_pT_Bin_24) (270.0°)
(Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_29) (345.0°), (Q2_y_Bin_3)-(z_pT_Bin_3) (270.0°)
(Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_15) (345.0°), (Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_19) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (300.0°)
(Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_27) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_28) (315.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (255.0°)
(Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_31) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_4) (195.0°)
(Q2_y_Bin_5)-(z_pT_Bin_7) (240.0°), (Q2_y_Bin_6)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_6)-(z_pT_Bin_25) (240.0°)
(Q2_y_Bin_6)-(z_pT_Bin_26) (225.0°), (Q2_y_Bin_6)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°)
(Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_31) (225.0°)
(Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°), (Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_34) (255.0°)
(Q2_y_Bin_7)-(z_pT_Bin_35) (330.0°), (Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°)
(Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_16) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_19) (210.0°)
(Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_24) (225.0°), (Q2_y_Bin_8)-(z_pT_Bin_25) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_30) (315.0°), (Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_9)-(z_pT_Bin_1) (225.0°), (Q2_y_Bin_9)-(z_pT_Bin_2) (195.0°)

### sector / P4

Stage: spline, acceptance. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/pion_sector/pipS4o/fit_copy.root`

Above 90° (285/452 (63.1%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (270.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_11) (120.0°)
(Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_17) (120.0°)
(Q2_y_Bin_1)-(z_pT_Bin_2) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_23) (120.0°)
(Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (210.0°)
(Q2_y_Bin_1)-(z_pT_Bin_31) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_32) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_4) (210.0°)
(Q2_y_Bin_1)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_6) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_7) (150.0°)
(Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_10)-(z_pT_Bin_1) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_10) (120.0°), (Q2_y_Bin_10)-(z_pT_Bin_13) (105.0°), (Q2_y_Bin_10)-(z_pT_Bin_15) (105.0°)
(Q2_y_Bin_10)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_20) (105.0°), (Q2_y_Bin_10)-(z_pT_Bin_26) (105.0°)
(Q2_y_Bin_10)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_31) (135.0°), (Q2_y_Bin_10)-(z_pT_Bin_32) (120.0°)
(Q2_y_Bin_10)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_10)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_10)-(z_pT_Bin_7) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_9) (120.0°), (Q2_y_Bin_11)-(z_pT_Bin_1) (180.0°)
(Q2_y_Bin_11)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_11) (120.0°), (Q2_y_Bin_11)-(z_pT_Bin_13) (120.0°)
(Q2_y_Bin_11)-(z_pT_Bin_14) (120.0°), (Q2_y_Bin_11)-(z_pT_Bin_15) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_18) (120.0°)
(Q2_y_Bin_11)-(z_pT_Bin_19) (120.0°), (Q2_y_Bin_11)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_11)-(z_pT_Bin_20) (150.0°)
(Q2_y_Bin_11)-(z_pT_Bin_21) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_22) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_23) (225.0°)
(Q2_y_Bin_11)-(z_pT_Bin_24) (270.0°), (Q2_y_Bin_11)-(z_pT_Bin_3) (240.0°), (Q2_y_Bin_11)-(z_pT_Bin_4) (345.0°)
(Q2_y_Bin_11)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_11)-(z_pT_Bin_9) (150.0°)
(Q2_y_Bin_12)-(z_pT_Bin_11) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_12) (105.0°), (Q2_y_Bin_12)-(z_pT_Bin_13) (120.0°)
(Q2_y_Bin_12)-(z_pT_Bin_14) (345.0°), (Q2_y_Bin_12)-(z_pT_Bin_16) (105.0°), (Q2_y_Bin_12)-(z_pT_Bin_18) (120.0°)
(Q2_y_Bin_12)-(z_pT_Bin_19) (300.0°), (Q2_y_Bin_12)-(z_pT_Bin_21) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_22) (270.0°)
(Q2_y_Bin_12)-(z_pT_Bin_23) (315.0°), (Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_6) (225.0°)
(Q2_y_Bin_12)-(z_pT_Bin_7) (315.0°), (Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_13)-(z_pT_Bin_1) (195.0°)
(Q2_y_Bin_13)-(z_pT_Bin_12) (105.0°), (Q2_y_Bin_13)-(z_pT_Bin_2) (120.0°), (Q2_y_Bin_13)-(z_pT_Bin_26) (120.0°)
(Q2_y_Bin_13)-(z_pT_Bin_3) (135.0°), (Q2_y_Bin_13)-(z_pT_Bin_4) (150.0°), (Q2_y_Bin_13)-(z_pT_Bin_5) (150.0°)
(Q2_y_Bin_13)-(z_pT_Bin_7) (105.0°), (Q2_y_Bin_13)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_14)-(z_pT_Bin_1) (135.0°)
(Q2_y_Bin_14)-(z_pT_Bin_2) (150.0°), (Q2_y_Bin_14)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_14)-(z_pT_Bin_32) (120.0°)
(Q2_y_Bin_14)-(z_pT_Bin_4) (165.0°), (Q2_y_Bin_14)-(z_pT_Bin_5) (210.0°), (Q2_y_Bin_15)-(z_pT_Bin_1) (195.0°)
(Q2_y_Bin_15)-(z_pT_Bin_15) (240.0°), (Q2_y_Bin_15)-(z_pT_Bin_19) (135.0°), (Q2_y_Bin_15)-(z_pT_Bin_2) (210.0°)
(Q2_y_Bin_15)-(z_pT_Bin_21) (135.0°), (Q2_y_Bin_15)-(z_pT_Bin_22) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_23) (180.0°)
(Q2_y_Bin_15)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_15)-(z_pT_Bin_9) (165.0°), (Q2_y_Bin_16)-(z_pT_Bin_1) (105.0°)
(Q2_y_Bin_16)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_16)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_16)-(z_pT_Bin_5) (150.0°)
(Q2_y_Bin_16)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_17)-(z_pT_Bin_4) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_1) (225.0°)
(Q2_y_Bin_2)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_11) (135.0°), (Q2_y_Bin_2)-(z_pT_Bin_12) (120.0°)
(Q2_y_Bin_2)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_15) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_16) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_18) (120.0°), (Q2_y_Bin_2)-(z_pT_Bin_19) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_2) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_20) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_21) (120.0°)
(Q2_y_Bin_2)-(z_pT_Bin_25) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_26) (135.0°), (Q2_y_Bin_2)-(z_pT_Bin_27) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_28) (120.0°), (Q2_y_Bin_2)-(z_pT_Bin_29) (120.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_32) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_33) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_34) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_4) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_8) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°)
(Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_12) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_13) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_14) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_15) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_16) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_17) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_18) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_19) (120.0°)
(Q2_y_Bin_3)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_20) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_21) (165.0°)
(Q2_y_Bin_3)-(z_pT_Bin_22) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_23) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_24) (270.0°)
(Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_3) (300.0°)
(Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_8) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_4)-(z_pT_Bin_15) (330.0°)
(Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_19) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_20) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (330.0°)
(Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_26) (150.0°)
(Q2_y_Bin_4)-(z_pT_Bin_27) (255.0°), (Q2_y_Bin_4)-(z_pT_Bin_28) (330.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (285.0°), (Q2_y_Bin_5)-(z_pT_Bin_10) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_11) (120.0°), (Q2_y_Bin_5)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_14) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_15) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_19) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (255.0°)
(Q2_y_Bin_5)-(z_pT_Bin_20) (135.0°), (Q2_y_Bin_5)-(z_pT_Bin_25) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (225.0°)
(Q2_y_Bin_5)-(z_pT_Bin_31) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_32) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_4) (210.0°)
(Q2_y_Bin_5)-(z_pT_Bin_5) (225.0°), (Q2_y_Bin_5)-(z_pT_Bin_6) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_7) (240.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_6)-(z_pT_Bin_1) (195.0°)
(Q2_y_Bin_6)-(z_pT_Bin_10) (135.0°), (Q2_y_Bin_6)-(z_pT_Bin_11) (105.0°), (Q2_y_Bin_6)-(z_pT_Bin_13) (120.0°)
(Q2_y_Bin_6)-(z_pT_Bin_14) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_6)-(z_pT_Bin_19) (135.0°)
(Q2_y_Bin_6)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_20) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_25) (240.0°)
(Q2_y_Bin_6)-(z_pT_Bin_26) (255.0°), (Q2_y_Bin_6)-(z_pT_Bin_27) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_28) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_6) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_8) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_10) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_13) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_15) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_16) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_17) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_18) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_19) (105.0°), (Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_7)-(z_pT_Bin_20) (105.0°), (Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_22) (135.0°)
(Q2_y_Bin_7)-(z_pT_Bin_23) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_24) (225.0°), (Q2_y_Bin_7)-(z_pT_Bin_25) (105.0°)
(Q2_y_Bin_7)-(z_pT_Bin_26) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_27) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_28) (135.0°)
(Q2_y_Bin_7)-(z_pT_Bin_29) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_31) (270.0°)
(Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°), (Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_34) (270.0°)
(Q2_y_Bin_7)-(z_pT_Bin_35) (315.0°), (Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_7)-(z_pT_Bin_7) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_7)-(z_pT_Bin_9) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°)
(Q2_y_Bin_8)-(z_pT_Bin_12) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_13) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_16) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_18) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_19) (240.0°)
(Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_21) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_23) (150.0°)
(Q2_y_Bin_8)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_8)-(z_pT_Bin_25) (330.0°), (Q2_y_Bin_8)-(z_pT_Bin_26) (120.0°)
(Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_30) (330.0°)
(Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_9)-(z_pT_Bin_1) (225.0°), (Q2_y_Bin_9)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_9)-(z_pT_Bin_15) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_16) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_2) (165.0°)
(Q2_y_Bin_9)-(z_pT_Bin_22) (120.0°), (Q2_y_Bin_9)-(z_pT_Bin_29) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (180.0°)
(Q2_y_Bin_9)-(z_pT_Bin_30) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_5) (150.0°)
(Q2_y_Bin_9)-(z_pT_Bin_6) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_9) (135.0°)

Above 120° (233/452 (51.5%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (270.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°)
(Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (210.0°)
(Q2_y_Bin_1)-(z_pT_Bin_31) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_4) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_5) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_6) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_7) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°)
(Q2_y_Bin_1)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_10)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_2) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_31) (135.0°), (Q2_y_Bin_10)-(z_pT_Bin_4) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_10)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_7) (180.0°)
(Q2_y_Bin_11)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_11)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_15) (150.0°)
(Q2_y_Bin_11)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_11)-(z_pT_Bin_20) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_21) (210.0°)
(Q2_y_Bin_11)-(z_pT_Bin_22) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_23) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_24) (270.0°)
(Q2_y_Bin_11)-(z_pT_Bin_3) (240.0°), (Q2_y_Bin_11)-(z_pT_Bin_4) (345.0°), (Q2_y_Bin_11)-(z_pT_Bin_6) (165.0°)
(Q2_y_Bin_11)-(z_pT_Bin_9) (150.0°), (Q2_y_Bin_12)-(z_pT_Bin_11) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_14) (345.0°)
(Q2_y_Bin_12)-(z_pT_Bin_19) (300.0°), (Q2_y_Bin_12)-(z_pT_Bin_21) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_22) (270.0°)
(Q2_y_Bin_12)-(z_pT_Bin_23) (315.0°), (Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_6) (225.0°)
(Q2_y_Bin_12)-(z_pT_Bin_7) (315.0°), (Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_13)-(z_pT_Bin_1) (195.0°)
(Q2_y_Bin_13)-(z_pT_Bin_3) (135.0°), (Q2_y_Bin_13)-(z_pT_Bin_4) (150.0°), (Q2_y_Bin_13)-(z_pT_Bin_5) (150.0°)
(Q2_y_Bin_14)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_14)-(z_pT_Bin_2) (150.0°), (Q2_y_Bin_14)-(z_pT_Bin_4) (165.0°)
(Q2_y_Bin_14)-(z_pT_Bin_5) (210.0°), (Q2_y_Bin_15)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (240.0°)
(Q2_y_Bin_15)-(z_pT_Bin_19) (135.0°), (Q2_y_Bin_15)-(z_pT_Bin_2) (210.0°), (Q2_y_Bin_15)-(z_pT_Bin_21) (135.0°)
(Q2_y_Bin_15)-(z_pT_Bin_22) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_23) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_24) (255.0°)
(Q2_y_Bin_15)-(z_pT_Bin_9) (165.0°), (Q2_y_Bin_16)-(z_pT_Bin_5) (150.0°), (Q2_y_Bin_16)-(z_pT_Bin_6) (165.0°)
(Q2_y_Bin_17)-(z_pT_Bin_4) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_1) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_10) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_11) (135.0°), (Q2_y_Bin_2)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_15) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_16) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_19) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_2) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_20) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_25) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_26) (135.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°)
(Q2_y_Bin_2)-(z_pT_Bin_32) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_33) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_34) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_4) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_8) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_9) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_12) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_13) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_14) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_15) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_16) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_17) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_18) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_20) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_21) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_22) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_23) (165.0°)
(Q2_y_Bin_3)-(z_pT_Bin_24) (270.0°), (Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_3) (300.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_8) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_9) (195.0°)
(Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_14) (165.0°)
(Q2_y_Bin_4)-(z_pT_Bin_15) (330.0°), (Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_19) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (330.0°)
(Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_26) (150.0°)
(Q2_y_Bin_4)-(z_pT_Bin_27) (255.0°), (Q2_y_Bin_4)-(z_pT_Bin_28) (330.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (285.0°), (Q2_y_Bin_5)-(z_pT_Bin_10) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_15) (150.0°)
(Q2_y_Bin_5)-(z_pT_Bin_19) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (255.0°), (Q2_y_Bin_5)-(z_pT_Bin_20) (135.0°)
(Q2_y_Bin_5)-(z_pT_Bin_25) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_5)-(z_pT_Bin_31) (210.0°)
(Q2_y_Bin_5)-(z_pT_Bin_32) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_4) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_5) (225.0°)
(Q2_y_Bin_5)-(z_pT_Bin_6) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_7) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (195.0°)
(Q2_y_Bin_5)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_6)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_6)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_6)-(z_pT_Bin_14) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_19) (135.0°), (Q2_y_Bin_6)-(z_pT_Bin_2) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_20) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_6)-(z_pT_Bin_26) (255.0°)
(Q2_y_Bin_6)-(z_pT_Bin_27) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_28) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_6) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_8) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_9) (180.0°)
(Q2_y_Bin_7)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_15) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_16) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_17) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_18) (135.0°)
(Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_22) (135.0°)
(Q2_y_Bin_7)-(z_pT_Bin_23) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_24) (225.0°), (Q2_y_Bin_7)-(z_pT_Bin_26) (135.0°)
(Q2_y_Bin_7)-(z_pT_Bin_27) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_28) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_29) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_31) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°)
(Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_34) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_35) (315.0°)
(Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_7)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_9) (150.0°)
(Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_12) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_13) (180.0°)
(Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_16) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_18) (135.0°)
(Q2_y_Bin_8)-(z_pT_Bin_19) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_21) (150.0°)
(Q2_y_Bin_8)-(z_pT_Bin_23) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_8)-(z_pT_Bin_25) (330.0°)
(Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_30) (330.0°)
(Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_9)-(z_pT_Bin_1) (225.0°), (Q2_y_Bin_9)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_9)-(z_pT_Bin_16) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_9)-(z_pT_Bin_29) (180.0°)
(Q2_y_Bin_9)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_5) (150.0°)
(Q2_y_Bin_9)-(z_pT_Bin_6) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_9) (135.0°)

Above 135° (211/452 (46.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (270.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°)
(Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (210.0°)
(Q2_y_Bin_1)-(z_pT_Bin_31) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_4) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_5) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_6) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_7) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°)
(Q2_y_Bin_1)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_10)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_2) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_5) (195.0°)
(Q2_y_Bin_10)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_7) (180.0°), (Q2_y_Bin_11)-(z_pT_Bin_1) (180.0°)
(Q2_y_Bin_11)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_15) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_11)-(z_pT_Bin_20) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_21) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_22) (225.0°)
(Q2_y_Bin_11)-(z_pT_Bin_23) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_24) (270.0°), (Q2_y_Bin_11)-(z_pT_Bin_3) (240.0°)
(Q2_y_Bin_11)-(z_pT_Bin_4) (345.0°), (Q2_y_Bin_11)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_9) (150.0°)
(Q2_y_Bin_12)-(z_pT_Bin_11) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_14) (345.0°), (Q2_y_Bin_12)-(z_pT_Bin_19) (300.0°)
(Q2_y_Bin_12)-(z_pT_Bin_21) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_22) (270.0°), (Q2_y_Bin_12)-(z_pT_Bin_23) (315.0°)
(Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_6) (225.0°), (Q2_y_Bin_12)-(z_pT_Bin_7) (315.0°)
(Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_13)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_13)-(z_pT_Bin_4) (150.0°)
(Q2_y_Bin_13)-(z_pT_Bin_5) (150.0°), (Q2_y_Bin_14)-(z_pT_Bin_2) (150.0°), (Q2_y_Bin_14)-(z_pT_Bin_4) (165.0°)
(Q2_y_Bin_14)-(z_pT_Bin_5) (210.0°), (Q2_y_Bin_15)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (240.0°)
(Q2_y_Bin_15)-(z_pT_Bin_2) (210.0°), (Q2_y_Bin_15)-(z_pT_Bin_22) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_23) (180.0°)
(Q2_y_Bin_15)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_15)-(z_pT_Bin_9) (165.0°), (Q2_y_Bin_16)-(z_pT_Bin_5) (150.0°)
(Q2_y_Bin_16)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_17)-(z_pT_Bin_4) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_1) (225.0°)
(Q2_y_Bin_2)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_15) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_16) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_19) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_2) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_20) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_25) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_32) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_33) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_34) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_4) (225.0°)
(Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°)
(Q2_y_Bin_2)-(z_pT_Bin_8) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_12) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_13) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_14) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_16) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_17) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_18) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_20) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_21) (165.0°)
(Q2_y_Bin_3)-(z_pT_Bin_22) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_23) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_24) (270.0°)
(Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_3) (300.0°)
(Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_8) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_4)-(z_pT_Bin_15) (330.0°)
(Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_19) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (330.0°), (Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_26) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_27) (255.0°)
(Q2_y_Bin_4)-(z_pT_Bin_28) (330.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (285.0°), (Q2_y_Bin_5)-(z_pT_Bin_10) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_13) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_15) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_19) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_2) (255.0°), (Q2_y_Bin_5)-(z_pT_Bin_25) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (225.0°)
(Q2_y_Bin_5)-(z_pT_Bin_31) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_32) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_4) (210.0°)
(Q2_y_Bin_5)-(z_pT_Bin_5) (225.0°), (Q2_y_Bin_5)-(z_pT_Bin_6) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_7) (240.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_6)-(z_pT_Bin_1) (195.0°)
(Q2_y_Bin_6)-(z_pT_Bin_14) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_20) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_6)-(z_pT_Bin_26) (255.0°), (Q2_y_Bin_6)-(z_pT_Bin_27) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_28) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_6) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_7) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_8) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_1) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°)
(Q2_y_Bin_7)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_15) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_17) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_24) (225.0°)
(Q2_y_Bin_7)-(z_pT_Bin_27) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_29) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°)
(Q2_y_Bin_7)-(z_pT_Bin_31) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°), (Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°)
(Q2_y_Bin_7)-(z_pT_Bin_34) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_35) (315.0°), (Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°)
(Q2_y_Bin_7)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_9) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°)
(Q2_y_Bin_8)-(z_pT_Bin_13) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_16) (195.0°)
(Q2_y_Bin_8)-(z_pT_Bin_19) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_21) (150.0°)
(Q2_y_Bin_8)-(z_pT_Bin_23) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_8)-(z_pT_Bin_25) (330.0°)
(Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_30) (330.0°)
(Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_9)-(z_pT_Bin_1) (225.0°), (Q2_y_Bin_9)-(z_pT_Bin_2) (165.0°)
(Q2_y_Bin_9)-(z_pT_Bin_29) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_4) (180.0°)
(Q2_y_Bin_9)-(z_pT_Bin_5) (150.0°)

Above 150° (179/452 (39.6%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (270.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°)
(Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (210.0°)
(Q2_y_Bin_1)-(z_pT_Bin_4) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_6) (180.0°)
(Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_10)-(z_pT_Bin_1) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_4) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_10)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_7) (180.0°)
(Q2_y_Bin_11)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_11)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_11)-(z_pT_Bin_21) (210.0°)
(Q2_y_Bin_11)-(z_pT_Bin_22) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_23) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_24) (270.0°)
(Q2_y_Bin_11)-(z_pT_Bin_3) (240.0°), (Q2_y_Bin_11)-(z_pT_Bin_4) (345.0°), (Q2_y_Bin_11)-(z_pT_Bin_6) (165.0°)
(Q2_y_Bin_12)-(z_pT_Bin_11) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_14) (345.0°), (Q2_y_Bin_12)-(z_pT_Bin_19) (300.0°)
(Q2_y_Bin_12)-(z_pT_Bin_21) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_22) (270.0°), (Q2_y_Bin_12)-(z_pT_Bin_23) (315.0°)
(Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_6) (225.0°), (Q2_y_Bin_12)-(z_pT_Bin_7) (315.0°)
(Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_13)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_14)-(z_pT_Bin_4) (165.0°)
(Q2_y_Bin_14)-(z_pT_Bin_5) (210.0°), (Q2_y_Bin_15)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (240.0°)
(Q2_y_Bin_15)-(z_pT_Bin_2) (210.0°), (Q2_y_Bin_15)-(z_pT_Bin_22) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_23) (180.0°)
(Q2_y_Bin_15)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_15)-(z_pT_Bin_9) (165.0°), (Q2_y_Bin_16)-(z_pT_Bin_6) (165.0°)
(Q2_y_Bin_17)-(z_pT_Bin_4) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_1) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_10) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_2) (225.0°)
(Q2_y_Bin_2)-(z_pT_Bin_20) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_25) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_32) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_34) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_4) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_8) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_9) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_12) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_13) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_18) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_20) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_21) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_23) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_24) (270.0°)
(Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_3) (300.0°)
(Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_4)-(z_pT_Bin_15) (330.0°), (Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_19) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_22) (330.0°), (Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°)
(Q2_y_Bin_4)-(z_pT_Bin_27) (255.0°), (Q2_y_Bin_4)-(z_pT_Bin_28) (330.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (285.0°), (Q2_y_Bin_5)-(z_pT_Bin_10) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_19) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_2) (255.0°), (Q2_y_Bin_5)-(z_pT_Bin_25) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (225.0°)
(Q2_y_Bin_5)-(z_pT_Bin_31) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_4) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_5) (225.0°)
(Q2_y_Bin_5)-(z_pT_Bin_6) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_7) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (195.0°)
(Q2_y_Bin_5)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_6)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_6)-(z_pT_Bin_2) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_20) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_6)-(z_pT_Bin_26) (255.0°)
(Q2_y_Bin_6)-(z_pT_Bin_27) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_28) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_6) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_8) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_9) (180.0°)
(Q2_y_Bin_7)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°)
(Q2_y_Bin_7)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°)
(Q2_y_Bin_7)-(z_pT_Bin_24) (225.0°), (Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_31) (270.0°)
(Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°), (Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_34) (270.0°)
(Q2_y_Bin_7)-(z_pT_Bin_35) (315.0°), (Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_7)-(z_pT_Bin_7) (165.0°)
(Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_13) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_16) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_19) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_8)-(z_pT_Bin_25) (330.0°), (Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°)
(Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_30) (330.0°), (Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_9)-(z_pT_Bin_1) (225.0°), (Q2_y_Bin_9)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_9)-(z_pT_Bin_29) (180.0°)
(Q2_y_Bin_9)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_4) (180.0°)

Above 180° (119/452 (26.3%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (270.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (225.0°)
(Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (210.0°)
(Q2_y_Bin_1)-(z_pT_Bin_4) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°)
(Q2_y_Bin_1)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_10)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_10)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_11)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_11)-(z_pT_Bin_21) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_22) (225.0°)
(Q2_y_Bin_11)-(z_pT_Bin_23) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_24) (270.0°), (Q2_y_Bin_11)-(z_pT_Bin_3) (240.0°)
(Q2_y_Bin_11)-(z_pT_Bin_4) (345.0°), (Q2_y_Bin_12)-(z_pT_Bin_11) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_14) (345.0°)
(Q2_y_Bin_12)-(z_pT_Bin_19) (300.0°), (Q2_y_Bin_12)-(z_pT_Bin_21) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_22) (270.0°)
(Q2_y_Bin_12)-(z_pT_Bin_23) (315.0°), (Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_6) (225.0°)
(Q2_y_Bin_12)-(z_pT_Bin_7) (315.0°), (Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_13)-(z_pT_Bin_1) (195.0°)
(Q2_y_Bin_14)-(z_pT_Bin_5) (210.0°), (Q2_y_Bin_15)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (240.0°)
(Q2_y_Bin_15)-(z_pT_Bin_2) (210.0°), (Q2_y_Bin_15)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_2)-(z_pT_Bin_1) (225.0°)
(Q2_y_Bin_2)-(z_pT_Bin_2) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°)
(Q2_y_Bin_2)-(z_pT_Bin_4) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_15) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_24) (270.0°), (Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_3) (300.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_15) (330.0°), (Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_19) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_22) (330.0°), (Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°)
(Q2_y_Bin_4)-(z_pT_Bin_27) (255.0°), (Q2_y_Bin_4)-(z_pT_Bin_28) (330.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (285.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (255.0°)
(Q2_y_Bin_5)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_5)-(z_pT_Bin_31) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_4) (210.0°)
(Q2_y_Bin_5)-(z_pT_Bin_5) (225.0°), (Q2_y_Bin_5)-(z_pT_Bin_6) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_7) (240.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_6)-(z_pT_Bin_1) (195.0°)
(Q2_y_Bin_6)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_6)-(z_pT_Bin_26) (255.0°), (Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°)
(Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_24) (225.0°), (Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°)
(Q2_y_Bin_7)-(z_pT_Bin_31) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°), (Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°)
(Q2_y_Bin_7)-(z_pT_Bin_34) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_35) (315.0°), (Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_16) (195.0°)
(Q2_y_Bin_8)-(z_pT_Bin_19) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_24) (255.0°)
(Q2_y_Bin_8)-(z_pT_Bin_25) (330.0°), (Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_30) (330.0°)
(Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_9)-(z_pT_Bin_1) (225.0°)

### sector / E5

Stage: spline, acceptance. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/electron_sector/eS5o/fit_copy.root`

Above 90° (290/452 (64.2%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (270.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_11) (120.0°)
(Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_17) (120.0°)
(Q2_y_Bin_1)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_23) (150.0°)
(Q2_y_Bin_1)-(z_pT_Bin_29) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_31) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_32) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_4) (225.0°)
(Q2_y_Bin_1)-(z_pT_Bin_5) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_6) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_7) (150.0°)
(Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_1) (150.0°)
(Q2_y_Bin_10)-(z_pT_Bin_10) (120.0°), (Q2_y_Bin_10)-(z_pT_Bin_13) (105.0°), (Q2_y_Bin_10)-(z_pT_Bin_15) (105.0°)
(Q2_y_Bin_10)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_10)-(z_pT_Bin_20) (120.0°), (Q2_y_Bin_10)-(z_pT_Bin_26) (120.0°)
(Q2_y_Bin_10)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_31) (135.0°), (Q2_y_Bin_10)-(z_pT_Bin_32) (150.0°)
(Q2_y_Bin_10)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_10)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_10)-(z_pT_Bin_9) (120.0°)
(Q2_y_Bin_11)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_11) (105.0°)
(Q2_y_Bin_11)-(z_pT_Bin_13) (105.0°), (Q2_y_Bin_11)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_11)-(z_pT_Bin_18) (105.0°)
(Q2_y_Bin_11)-(z_pT_Bin_19) (105.0°), (Q2_y_Bin_11)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_20) (150.0°)
(Q2_y_Bin_11)-(z_pT_Bin_21) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_22) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_23) (195.0°)
(Q2_y_Bin_11)-(z_pT_Bin_24) (240.0°), (Q2_y_Bin_11)-(z_pT_Bin_3) (240.0°), (Q2_y_Bin_11)-(z_pT_Bin_4) (300.0°)
(Q2_y_Bin_11)-(z_pT_Bin_6) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_11)-(z_pT_Bin_9) (120.0°)
(Q2_y_Bin_12)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_12)-(z_pT_Bin_12) (105.0°), (Q2_y_Bin_12)-(z_pT_Bin_13) (120.0°)
(Q2_y_Bin_12)-(z_pT_Bin_14) (300.0°), (Q2_y_Bin_12)-(z_pT_Bin_16) (135.0°), (Q2_y_Bin_12)-(z_pT_Bin_18) (120.0°)
(Q2_y_Bin_12)-(z_pT_Bin_19) (255.0°), (Q2_y_Bin_12)-(z_pT_Bin_21) (315.0°), (Q2_y_Bin_12)-(z_pT_Bin_22) (225.0°)
(Q2_y_Bin_12)-(z_pT_Bin_23) (270.0°), (Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_13)-(z_pT_Bin_1) (195.0°)
(Q2_y_Bin_13)-(z_pT_Bin_12) (105.0°), (Q2_y_Bin_13)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_13)-(z_pT_Bin_26) (120.0°)
(Q2_y_Bin_13)-(z_pT_Bin_3) (135.0°), (Q2_y_Bin_13)-(z_pT_Bin_4) (135.0°), (Q2_y_Bin_13)-(z_pT_Bin_5) (120.0°)
(Q2_y_Bin_13)-(z_pT_Bin_7) (105.0°), (Q2_y_Bin_13)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_14)-(z_pT_Bin_1) (120.0°)
(Q2_y_Bin_14)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_14)-(z_pT_Bin_3) (135.0°), (Q2_y_Bin_14)-(z_pT_Bin_32) (105.0°)
(Q2_y_Bin_14)-(z_pT_Bin_4) (165.0°), (Q2_y_Bin_14)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_1) (165.0°)
(Q2_y_Bin_15)-(z_pT_Bin_15) (210.0°), (Q2_y_Bin_15)-(z_pT_Bin_19) (105.0°), (Q2_y_Bin_15)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_15)-(z_pT_Bin_21) (120.0°), (Q2_y_Bin_15)-(z_pT_Bin_22) (165.0°), (Q2_y_Bin_15)-(z_pT_Bin_23) (195.0°)
(Q2_y_Bin_15)-(z_pT_Bin_24) (240.0°), (Q2_y_Bin_15)-(z_pT_Bin_6) (120.0°), (Q2_y_Bin_15)-(z_pT_Bin_9) (150.0°)
(Q2_y_Bin_16)-(z_pT_Bin_1) (120.0°), (Q2_y_Bin_16)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_16)-(z_pT_Bin_4) (120.0°)
(Q2_y_Bin_16)-(z_pT_Bin_5) (120.0°), (Q2_y_Bin_16)-(z_pT_Bin_6) (150.0°), (Q2_y_Bin_16)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_17)-(z_pT_Bin_2) (120.0°), (Q2_y_Bin_17)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_1) (225.0°)
(Q2_y_Bin_2)-(z_pT_Bin_10) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_11) (135.0°), (Q2_y_Bin_2)-(z_pT_Bin_12) (120.0°)
(Q2_y_Bin_2)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_15) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_16) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_18) (120.0°), (Q2_y_Bin_2)-(z_pT_Bin_19) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_2) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_20) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_21) (120.0°)
(Q2_y_Bin_2)-(z_pT_Bin_23) (105.0°), (Q2_y_Bin_2)-(z_pT_Bin_25) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_26) (135.0°)
(Q2_y_Bin_2)-(z_pT_Bin_27) (120.0°), (Q2_y_Bin_2)-(z_pT_Bin_28) (120.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_32) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_33) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_34) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_4) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_8) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°)
(Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_12) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_13) (210.0°)
(Q2_y_Bin_3)-(z_pT_Bin_14) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_15) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_16) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_17) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_18) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_19) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_3)-(z_pT_Bin_20) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_21) (165.0°)
(Q2_y_Bin_3)-(z_pT_Bin_22) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_23) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_24) (270.0°)
(Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_3) (285.0°)
(Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_4)-(z_pT_Bin_15) (345.0°)
(Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_19) (240.0°)
(Q2_y_Bin_4)-(z_pT_Bin_20) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (345.0°)
(Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_26) (150.0°)
(Q2_y_Bin_4)-(z_pT_Bin_27) (225.0°), (Q2_y_Bin_4)-(z_pT_Bin_28) (285.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (255.0°), (Q2_y_Bin_5)-(z_pT_Bin_10) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_11) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_14) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_15) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_19) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (255.0°)
(Q2_y_Bin_5)-(z_pT_Bin_20) (135.0°), (Q2_y_Bin_5)-(z_pT_Bin_25) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_26) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_31) (225.0°), (Q2_y_Bin_5)-(z_pT_Bin_32) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_6) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_7) (255.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_9) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_11) (105.0°)
(Q2_y_Bin_6)-(z_pT_Bin_13) (120.0°), (Q2_y_Bin_6)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_15) (135.0°)
(Q2_y_Bin_6)-(z_pT_Bin_19) (135.0°), (Q2_y_Bin_6)-(z_pT_Bin_2) (210.0°), (Q2_y_Bin_6)-(z_pT_Bin_20) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_6)-(z_pT_Bin_26) (255.0°), (Q2_y_Bin_6)-(z_pT_Bin_27) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_28) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_7) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_8) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_9) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_1) (195.0°)
(Q2_y_Bin_7)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°)
(Q2_y_Bin_7)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_14) (105.0°), (Q2_y_Bin_7)-(z_pT_Bin_15) (135.0°)
(Q2_y_Bin_7)-(z_pT_Bin_16) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_17) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_18) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_19) (120.0°), (Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_20) (120.0°)
(Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_22) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_23) (135.0°)
(Q2_y_Bin_7)-(z_pT_Bin_24) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_25) (105.0°), (Q2_y_Bin_7)-(z_pT_Bin_26) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_27) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_28) (120.0°), (Q2_y_Bin_7)-(z_pT_Bin_29) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_31) (255.0°), (Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°)
(Q2_y_Bin_7)-(z_pT_Bin_33) (255.0°), (Q2_y_Bin_7)-(z_pT_Bin_34) (255.0°), (Q2_y_Bin_7)-(z_pT_Bin_35) (300.0°)
(Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_7)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_8) (135.0°)
(Q2_y_Bin_7)-(z_pT_Bin_9) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_12) (150.0°)
(Q2_y_Bin_8)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_16) (210.0°)
(Q2_y_Bin_8)-(z_pT_Bin_17) (105.0°), (Q2_y_Bin_8)-(z_pT_Bin_18) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_19) (210.0°)
(Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_21) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_23) (150.0°)
(Q2_y_Bin_8)-(z_pT_Bin_24) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_25) (315.0°), (Q2_y_Bin_8)-(z_pT_Bin_26) (135.0°)
(Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_30) (330.0°)
(Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_9)-(z_pT_Bin_1) (225.0°), (Q2_y_Bin_9)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_9)-(z_pT_Bin_15) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_16) (120.0°), (Q2_y_Bin_9)-(z_pT_Bin_2) (180.0°)
(Q2_y_Bin_9)-(z_pT_Bin_22) (120.0°), (Q2_y_Bin_9)-(z_pT_Bin_29) (195.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (180.0°)
(Q2_y_Bin_9)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_5) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_6) (135.0°)
(Q2_y_Bin_9)-(z_pT_Bin_8) (150.0°), (Q2_y_Bin_9)-(z_pT_Bin_9) (120.0°)

Above 120° (235/452 (52.0%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (270.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°)
(Q2_y_Bin_1)-(z_pT_Bin_23) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_29) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°)
(Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_31) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_4) (225.0°)
(Q2_y_Bin_1)-(z_pT_Bin_5) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_6) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_7) (150.0°)
(Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_1) (150.0°)
(Q2_y_Bin_10)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_10)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_31) (135.0°)
(Q2_y_Bin_10)-(z_pT_Bin_32) (150.0°), (Q2_y_Bin_10)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_5) (165.0°)
(Q2_y_Bin_10)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_1) (165.0°)
(Q2_y_Bin_11)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_20) (150.0°)
(Q2_y_Bin_11)-(z_pT_Bin_21) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_22) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_23) (195.0°)
(Q2_y_Bin_11)-(z_pT_Bin_24) (240.0°), (Q2_y_Bin_11)-(z_pT_Bin_3) (240.0°), (Q2_y_Bin_11)-(z_pT_Bin_4) (300.0°)
(Q2_y_Bin_11)-(z_pT_Bin_6) (150.0°), (Q2_y_Bin_12)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_12)-(z_pT_Bin_14) (300.0°)
(Q2_y_Bin_12)-(z_pT_Bin_16) (135.0°), (Q2_y_Bin_12)-(z_pT_Bin_19) (255.0°), (Q2_y_Bin_12)-(z_pT_Bin_21) (315.0°)
(Q2_y_Bin_12)-(z_pT_Bin_22) (225.0°), (Q2_y_Bin_12)-(z_pT_Bin_23) (270.0°), (Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°)
(Q2_y_Bin_12)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_13)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_13)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_13)-(z_pT_Bin_3) (135.0°)
(Q2_y_Bin_13)-(z_pT_Bin_4) (135.0°), (Q2_y_Bin_14)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_14)-(z_pT_Bin_3) (135.0°)
(Q2_y_Bin_14)-(z_pT_Bin_4) (165.0°), (Q2_y_Bin_14)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_1) (165.0°)
(Q2_y_Bin_15)-(z_pT_Bin_15) (210.0°), (Q2_y_Bin_15)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_22) (165.0°)
(Q2_y_Bin_15)-(z_pT_Bin_23) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_24) (240.0°), (Q2_y_Bin_15)-(z_pT_Bin_9) (150.0°)
(Q2_y_Bin_16)-(z_pT_Bin_6) (150.0°), (Q2_y_Bin_17)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_1) (225.0°)
(Q2_y_Bin_2)-(z_pT_Bin_10) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_11) (135.0°), (Q2_y_Bin_2)-(z_pT_Bin_13) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_15) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_16) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_19) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_2) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_20) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_25) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_26) (135.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_32) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_33) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_34) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_4) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_8) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°)
(Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_12) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_13) (210.0°)
(Q2_y_Bin_3)-(z_pT_Bin_14) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_15) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_16) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_17) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_18) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_19) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_3)-(z_pT_Bin_20) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_21) (165.0°)
(Q2_y_Bin_3)-(z_pT_Bin_22) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_23) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_24) (270.0°)
(Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_3) (285.0°)
(Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_4)-(z_pT_Bin_15) (345.0°)
(Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_19) (240.0°)
(Q2_y_Bin_4)-(z_pT_Bin_20) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (345.0°)
(Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_26) (150.0°)
(Q2_y_Bin_4)-(z_pT_Bin_27) (225.0°), (Q2_y_Bin_4)-(z_pT_Bin_28) (285.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (255.0°), (Q2_y_Bin_5)-(z_pT_Bin_10) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_15) (150.0°)
(Q2_y_Bin_5)-(z_pT_Bin_19) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (255.0°), (Q2_y_Bin_5)-(z_pT_Bin_20) (135.0°)
(Q2_y_Bin_5)-(z_pT_Bin_25) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_31) (225.0°)
(Q2_y_Bin_5)-(z_pT_Bin_32) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_5) (195.0°)
(Q2_y_Bin_5)-(z_pT_Bin_6) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_7) (255.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_10) (150.0°)
(Q2_y_Bin_6)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_15) (135.0°), (Q2_y_Bin_6)-(z_pT_Bin_19) (135.0°)
(Q2_y_Bin_6)-(z_pT_Bin_2) (210.0°), (Q2_y_Bin_6)-(z_pT_Bin_20) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_25) (240.0°)
(Q2_y_Bin_6)-(z_pT_Bin_26) (255.0°), (Q2_y_Bin_6)-(z_pT_Bin_27) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_28) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_7) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_8) (150.0°)
(Q2_y_Bin_6)-(z_pT_Bin_9) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_10) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_13) (195.0°)
(Q2_y_Bin_7)-(z_pT_Bin_15) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_16) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_17) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_18) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°)
(Q2_y_Bin_7)-(z_pT_Bin_22) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_23) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_24) (180.0°)
(Q2_y_Bin_7)-(z_pT_Bin_26) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_27) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_29) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_31) (255.0°), (Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°)
(Q2_y_Bin_7)-(z_pT_Bin_33) (255.0°), (Q2_y_Bin_7)-(z_pT_Bin_34) (255.0°), (Q2_y_Bin_7)-(z_pT_Bin_35) (300.0°)
(Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_7)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_8) (135.0°)
(Q2_y_Bin_7)-(z_pT_Bin_9) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_12) (150.0°)
(Q2_y_Bin_8)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_16) (210.0°)
(Q2_y_Bin_8)-(z_pT_Bin_18) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_19) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_21) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_23) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_24) (240.0°)
(Q2_y_Bin_8)-(z_pT_Bin_25) (315.0°), (Q2_y_Bin_8)-(z_pT_Bin_26) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°)
(Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_30) (330.0°), (Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_9)-(z_pT_Bin_1) (225.0°), (Q2_y_Bin_9)-(z_pT_Bin_10) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_15) (135.0°)
(Q2_y_Bin_9)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_29) (195.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (180.0°)
(Q2_y_Bin_9)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_5) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_6) (135.0°)
(Q2_y_Bin_9)-(z_pT_Bin_8) (150.0°)

Above 135° (215/452 (47.6%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (270.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°)
(Q2_y_Bin_1)-(z_pT_Bin_23) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_29) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°)
(Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_31) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_4) (225.0°)
(Q2_y_Bin_1)-(z_pT_Bin_5) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_6) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_7) (150.0°)
(Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_1) (150.0°)
(Q2_y_Bin_10)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_10)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_32) (150.0°)
(Q2_y_Bin_10)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_10)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_10) (150.0°)
(Q2_y_Bin_11)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_20) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_21) (165.0°)
(Q2_y_Bin_11)-(z_pT_Bin_22) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_23) (195.0°), (Q2_y_Bin_11)-(z_pT_Bin_24) (240.0°)
(Q2_y_Bin_11)-(z_pT_Bin_3) (240.0°), (Q2_y_Bin_11)-(z_pT_Bin_4) (300.0°), (Q2_y_Bin_11)-(z_pT_Bin_6) (150.0°)
(Q2_y_Bin_12)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_12)-(z_pT_Bin_14) (300.0°), (Q2_y_Bin_12)-(z_pT_Bin_19) (255.0°)
(Q2_y_Bin_12)-(z_pT_Bin_21) (315.0°), (Q2_y_Bin_12)-(z_pT_Bin_22) (225.0°), (Q2_y_Bin_12)-(z_pT_Bin_23) (270.0°)
(Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°)
(Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_13)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_13)-(z_pT_Bin_2) (180.0°)
(Q2_y_Bin_14)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_14)-(z_pT_Bin_4) (165.0°), (Q2_y_Bin_14)-(z_pT_Bin_5) (195.0°)
(Q2_y_Bin_15)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (210.0°), (Q2_y_Bin_15)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_15)-(z_pT_Bin_22) (165.0°), (Q2_y_Bin_15)-(z_pT_Bin_23) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_24) (240.0°)
(Q2_y_Bin_15)-(z_pT_Bin_9) (150.0°), (Q2_y_Bin_16)-(z_pT_Bin_6) (150.0°), (Q2_y_Bin_17)-(z_pT_Bin_4) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_1) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_10) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_13) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_15) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_16) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_19) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_2) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_20) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_25) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°)
(Q2_y_Bin_2)-(z_pT_Bin_32) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_33) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_34) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_4) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_9) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_12) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_14) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_15) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_16) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_17) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_18) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_19) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_2) (240.0°)
(Q2_y_Bin_3)-(z_pT_Bin_20) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_21) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_22) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_23) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_24) (270.0°), (Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_3) (285.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_8) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_4)-(z_pT_Bin_15) (345.0°), (Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_19) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_20) (150.0°)
(Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (345.0°), (Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_26) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_27) (225.0°)
(Q2_y_Bin_4)-(z_pT_Bin_28) (285.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (255.0°), (Q2_y_Bin_5)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_13) (195.0°)
(Q2_y_Bin_5)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_15) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_19) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_2) (255.0°), (Q2_y_Bin_5)-(z_pT_Bin_25) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°)
(Q2_y_Bin_5)-(z_pT_Bin_31) (225.0°), (Q2_y_Bin_5)-(z_pT_Bin_32) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_4) (195.0°)
(Q2_y_Bin_5)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_6) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_7) (255.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_1) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_2) (210.0°)
(Q2_y_Bin_6)-(z_pT_Bin_20) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_6)-(z_pT_Bin_26) (255.0°)
(Q2_y_Bin_6)-(z_pT_Bin_27) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_28) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_6) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_7) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_8) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_9) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_16) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_17) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_18) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_24) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_26) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_27) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_29) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°)
(Q2_y_Bin_7)-(z_pT_Bin_31) (255.0°), (Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°), (Q2_y_Bin_7)-(z_pT_Bin_33) (255.0°)
(Q2_y_Bin_7)-(z_pT_Bin_34) (255.0°), (Q2_y_Bin_7)-(z_pT_Bin_35) (300.0°), (Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°)
(Q2_y_Bin_7)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_9) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°)
(Q2_y_Bin_8)-(z_pT_Bin_12) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_16) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_19) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_21) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_23) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_24) (240.0°)
(Q2_y_Bin_8)-(z_pT_Bin_25) (315.0°), (Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°)
(Q2_y_Bin_8)-(z_pT_Bin_30) (330.0°), (Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_9)-(z_pT_Bin_1) (225.0°)
(Q2_y_Bin_9)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_29) (195.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (180.0°)
(Q2_y_Bin_9)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_8) (150.0°)

Above 150° (182/452 (40.3%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (270.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°)
(Q2_y_Bin_1)-(z_pT_Bin_29) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_4) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_5) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_6) (180.0°)
(Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_10)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_5) (165.0°)
(Q2_y_Bin_10)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_1) (165.0°)
(Q2_y_Bin_11)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_21) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_22) (225.0°)
(Q2_y_Bin_11)-(z_pT_Bin_23) (195.0°), (Q2_y_Bin_11)-(z_pT_Bin_24) (240.0°), (Q2_y_Bin_11)-(z_pT_Bin_3) (240.0°)
(Q2_y_Bin_11)-(z_pT_Bin_4) (300.0°), (Q2_y_Bin_12)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_12)-(z_pT_Bin_14) (300.0°)
(Q2_y_Bin_12)-(z_pT_Bin_19) (255.0°), (Q2_y_Bin_12)-(z_pT_Bin_21) (315.0°), (Q2_y_Bin_12)-(z_pT_Bin_22) (225.0°)
(Q2_y_Bin_12)-(z_pT_Bin_23) (270.0°), (Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_13)-(z_pT_Bin_1) (195.0°)
(Q2_y_Bin_13)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_14)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_14)-(z_pT_Bin_4) (165.0°)
(Q2_y_Bin_14)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (210.0°)
(Q2_y_Bin_15)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_22) (165.0°), (Q2_y_Bin_15)-(z_pT_Bin_23) (195.0°)
(Q2_y_Bin_15)-(z_pT_Bin_24) (240.0°), (Q2_y_Bin_17)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_1) (225.0°)
(Q2_y_Bin_2)-(z_pT_Bin_10) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_15) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_19) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_2) (225.0°)
(Q2_y_Bin_2)-(z_pT_Bin_20) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_25) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_32) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_4) (225.0°)
(Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°)
(Q2_y_Bin_2)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_12) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_15) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_18) (165.0°)
(Q2_y_Bin_3)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_3)-(z_pT_Bin_20) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_21) (165.0°)
(Q2_y_Bin_3)-(z_pT_Bin_23) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_24) (270.0°), (Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_3) (285.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_8) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_4)-(z_pT_Bin_15) (345.0°), (Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_19) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_22) (345.0°), (Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°)
(Q2_y_Bin_4)-(z_pT_Bin_27) (225.0°), (Q2_y_Bin_4)-(z_pT_Bin_28) (285.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (255.0°), (Q2_y_Bin_5)-(z_pT_Bin_10) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_19) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_2) (255.0°), (Q2_y_Bin_5)-(z_pT_Bin_25) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°)
(Q2_y_Bin_5)-(z_pT_Bin_31) (225.0°), (Q2_y_Bin_5)-(z_pT_Bin_32) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_4) (195.0°)
(Q2_y_Bin_5)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_6) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_7) (255.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_1) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_2) (210.0°), (Q2_y_Bin_6)-(z_pT_Bin_20) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_6)-(z_pT_Bin_26) (255.0°), (Q2_y_Bin_6)-(z_pT_Bin_27) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_28) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_7) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_9) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_24) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_29) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_31) (255.0°), (Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°)
(Q2_y_Bin_7)-(z_pT_Bin_33) (255.0°), (Q2_y_Bin_7)-(z_pT_Bin_34) (255.0°), (Q2_y_Bin_7)-(z_pT_Bin_35) (300.0°)
(Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_7)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°)
(Q2_y_Bin_8)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_16) (210.0°)
(Q2_y_Bin_8)-(z_pT_Bin_19) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_21) (180.0°)
(Q2_y_Bin_8)-(z_pT_Bin_24) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_25) (315.0°), (Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°)
(Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_30) (330.0°), (Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_9)-(z_pT_Bin_1) (225.0°), (Q2_y_Bin_9)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_29) (195.0°)
(Q2_y_Bin_9)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_4) (180.0°)

Above 180° (122/452 (27.0%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (270.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (240.0°)
(Q2_y_Bin_1)-(z_pT_Bin_29) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_4) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_5) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°)
(Q2_y_Bin_1)-(z_pT_Bin_9) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_10)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_11)-(z_pT_Bin_22) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_23) (195.0°), (Q2_y_Bin_11)-(z_pT_Bin_24) (240.0°)
(Q2_y_Bin_11)-(z_pT_Bin_3) (240.0°), (Q2_y_Bin_11)-(z_pT_Bin_4) (300.0°), (Q2_y_Bin_12)-(z_pT_Bin_11) (195.0°)
(Q2_y_Bin_12)-(z_pT_Bin_14) (300.0°), (Q2_y_Bin_12)-(z_pT_Bin_19) (255.0°), (Q2_y_Bin_12)-(z_pT_Bin_21) (315.0°)
(Q2_y_Bin_12)-(z_pT_Bin_22) (225.0°), (Q2_y_Bin_12)-(z_pT_Bin_23) (270.0°), (Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°)
(Q2_y_Bin_12)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_13)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_14)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (210.0°)
(Q2_y_Bin_15)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_23) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_24) (240.0°)
(Q2_y_Bin_2)-(z_pT_Bin_1) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_19) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_2) (225.0°)
(Q2_y_Bin_2)-(z_pT_Bin_20) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°)
(Q2_y_Bin_2)-(z_pT_Bin_4) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_12) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_13) (210.0°)
(Q2_y_Bin_3)-(z_pT_Bin_15) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_3)-(z_pT_Bin_20) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_24) (270.0°), (Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_3) (285.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_15) (345.0°), (Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_19) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (345.0°)
(Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_27) (225.0°)
(Q2_y_Bin_4)-(z_pT_Bin_28) (285.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (255.0°), (Q2_y_Bin_5)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (255.0°)
(Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_31) (225.0°), (Q2_y_Bin_5)-(z_pT_Bin_4) (195.0°)
(Q2_y_Bin_5)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_7) (255.0°), (Q2_y_Bin_6)-(z_pT_Bin_2) (210.0°)
(Q2_y_Bin_6)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_6)-(z_pT_Bin_26) (255.0°), (Q2_y_Bin_7)-(z_pT_Bin_1) (195.0°)
(Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_31) (255.0°), (Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°)
(Q2_y_Bin_7)-(z_pT_Bin_33) (255.0°), (Q2_y_Bin_7)-(z_pT_Bin_34) (255.0°), (Q2_y_Bin_7)-(z_pT_Bin_35) (300.0°)
(Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_13) (210.0°)
(Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_16) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_19) (210.0°)
(Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_24) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_25) (315.0°)
(Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_30) (330.0°), (Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_9)-(z_pT_Bin_1) (225.0°), (Q2_y_Bin_9)-(z_pT_Bin_29) (195.0°)

### sector / P5

Stage: spline, acceptance. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/pion_sector/pipS5o/fit_copy.root`

Above 90° (289/452 (63.9%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_11) (120.0°)
(Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_17) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_2) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_23) (150.0°)
(Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_31) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_32) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_4) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_7) (120.0°)
(Q2_y_Bin_1)-(z_pT_Bin_8) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_10)-(z_pT_Bin_1) (150.0°)
(Q2_y_Bin_10)-(z_pT_Bin_10) (120.0°), (Q2_y_Bin_10)-(z_pT_Bin_11) (105.0°), (Q2_y_Bin_10)-(z_pT_Bin_15) (150.0°)
(Q2_y_Bin_10)-(z_pT_Bin_2) (150.0°), (Q2_y_Bin_10)-(z_pT_Bin_20) (120.0°), (Q2_y_Bin_10)-(z_pT_Bin_26) (150.0°)
(Q2_y_Bin_10)-(z_pT_Bin_3) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_31) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_32) (165.0°)
(Q2_y_Bin_10)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_10)-(z_pT_Bin_4) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_5) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_7) (150.0°), (Q2_y_Bin_10)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_11)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_13) (120.0°)
(Q2_y_Bin_11)-(z_pT_Bin_14) (105.0°), (Q2_y_Bin_11)-(z_pT_Bin_15) (105.0°), (Q2_y_Bin_11)-(z_pT_Bin_18) (120.0°)
(Q2_y_Bin_11)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_20) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_21) (180.0°)
(Q2_y_Bin_11)-(z_pT_Bin_22) (240.0°), (Q2_y_Bin_11)-(z_pT_Bin_23) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_24) (255.0°)
(Q2_y_Bin_11)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_4) (345.0°), (Q2_y_Bin_11)-(z_pT_Bin_6) (165.0°)
(Q2_y_Bin_11)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_11)-(z_pT_Bin_9) (135.0°), (Q2_y_Bin_12)-(z_pT_Bin_11) (195.0°)
(Q2_y_Bin_12)-(z_pT_Bin_12) (105.0°), (Q2_y_Bin_12)-(z_pT_Bin_13) (120.0°), (Q2_y_Bin_12)-(z_pT_Bin_14) (315.0°)
(Q2_y_Bin_12)-(z_pT_Bin_16) (120.0°), (Q2_y_Bin_12)-(z_pT_Bin_18) (120.0°), (Q2_y_Bin_12)-(z_pT_Bin_19) (255.0°)
(Q2_y_Bin_12)-(z_pT_Bin_21) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_22) (270.0°), (Q2_y_Bin_12)-(z_pT_Bin_23) (285.0°)
(Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_6) (225.0°), (Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°)
(Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_13)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_13)-(z_pT_Bin_12) (105.0°)
(Q2_y_Bin_13)-(z_pT_Bin_2) (120.0°), (Q2_y_Bin_13)-(z_pT_Bin_26) (120.0°), (Q2_y_Bin_13)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_13)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_13)-(z_pT_Bin_5) (105.0°), (Q2_y_Bin_13)-(z_pT_Bin_7) (105.0°)
(Q2_y_Bin_13)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_14)-(z_pT_Bin_1) (120.0°), (Q2_y_Bin_14)-(z_pT_Bin_2) (150.0°)
(Q2_y_Bin_14)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_14)-(z_pT_Bin_32) (150.0°), (Q2_y_Bin_14)-(z_pT_Bin_4) (150.0°)
(Q2_y_Bin_14)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_13) (105.0°)
(Q2_y_Bin_15)-(z_pT_Bin_14) (105.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (225.0°), (Q2_y_Bin_15)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_15)-(z_pT_Bin_21) (135.0°), (Q2_y_Bin_15)-(z_pT_Bin_22) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_23) (195.0°)
(Q2_y_Bin_15)-(z_pT_Bin_24) (240.0°), (Q2_y_Bin_15)-(z_pT_Bin_9) (165.0°), (Q2_y_Bin_16)-(z_pT_Bin_4) (105.0°)
(Q2_y_Bin_16)-(z_pT_Bin_6) (150.0°), (Q2_y_Bin_17)-(z_pT_Bin_2) (120.0°), (Q2_y_Bin_17)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_17)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_1) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_10) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_11) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_12) (105.0°), (Q2_y_Bin_2)-(z_pT_Bin_13) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_15) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_16) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_17) (105.0°), (Q2_y_Bin_2)-(z_pT_Bin_19) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_2) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_20) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_21) (135.0°), (Q2_y_Bin_2)-(z_pT_Bin_22) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_23) (105.0°), (Q2_y_Bin_2)-(z_pT_Bin_25) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_26) (135.0°)
(Q2_y_Bin_2)-(z_pT_Bin_27) (135.0°), (Q2_y_Bin_2)-(z_pT_Bin_28) (120.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_32) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_33) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_34) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_4) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_8) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°)
(Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_12) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_13) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_14) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_15) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_16) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_17) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_18) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_19) (120.0°)
(Q2_y_Bin_3)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_20) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_21) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_22) (135.0°), (Q2_y_Bin_3)-(z_pT_Bin_23) (135.0°), (Q2_y_Bin_3)-(z_pT_Bin_24) (255.0°)
(Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_3) (255.0°)
(Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_8) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_14) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_15) (330.0°)
(Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_19) (240.0°)
(Q2_y_Bin_4)-(z_pT_Bin_20) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (300.0°)
(Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_26) (150.0°)
(Q2_y_Bin_4)-(z_pT_Bin_27) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_28) (300.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_10) (150.0°)
(Q2_y_Bin_5)-(z_pT_Bin_11) (120.0°), (Q2_y_Bin_5)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_14) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_15) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_16) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_19) (150.0°)
(Q2_y_Bin_5)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_20) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_25) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_26) (120.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_31) (210.0°)
(Q2_y_Bin_5)-(z_pT_Bin_32) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_4) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_5) (195.0°)
(Q2_y_Bin_5)-(z_pT_Bin_6) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_7) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_6)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_10) (150.0°)
(Q2_y_Bin_6)-(z_pT_Bin_11) (105.0°), (Q2_y_Bin_6)-(z_pT_Bin_13) (120.0°), (Q2_y_Bin_6)-(z_pT_Bin_14) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_15) (105.0°), (Q2_y_Bin_6)-(z_pT_Bin_16) (105.0°), (Q2_y_Bin_6)-(z_pT_Bin_19) (135.0°)
(Q2_y_Bin_6)-(z_pT_Bin_2) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_20) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_25) (240.0°)
(Q2_y_Bin_6)-(z_pT_Bin_26) (270.0°), (Q2_y_Bin_6)-(z_pT_Bin_27) (195.0°), (Q2_y_Bin_6)-(z_pT_Bin_28) (150.0°)
(Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_6) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_7) (135.0°), (Q2_y_Bin_6)-(z_pT_Bin_8) (150.0°)
(Q2_y_Bin_6)-(z_pT_Bin_9) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_10) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_13) (195.0°)
(Q2_y_Bin_7)-(z_pT_Bin_15) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_16) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_17) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_18) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_19) (105.0°), (Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_7)-(z_pT_Bin_20) (105.0°), (Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_22) (120.0°)
(Q2_y_Bin_7)-(z_pT_Bin_23) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_24) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_25) (105.0°)
(Q2_y_Bin_7)-(z_pT_Bin_26) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_27) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_28) (120.0°)
(Q2_y_Bin_7)-(z_pT_Bin_29) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_31) (240.0°)
(Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°), (Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_34) (255.0°)
(Q2_y_Bin_7)-(z_pT_Bin_35) (300.0°), (Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_7)-(z_pT_Bin_7) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_7)-(z_pT_Bin_9) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°)
(Q2_y_Bin_8)-(z_pT_Bin_12) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_16) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_18) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_19) (210.0°)
(Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_21) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_23) (150.0°)
(Q2_y_Bin_8)-(z_pT_Bin_24) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_25) (330.0°), (Q2_y_Bin_8)-(z_pT_Bin_26) (120.0°)
(Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_30) (315.0°)
(Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_9)-(z_pT_Bin_1) (210.0°), (Q2_y_Bin_9)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_9)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_9)-(z_pT_Bin_16) (150.0°), (Q2_y_Bin_9)-(z_pT_Bin_2) (180.0°)
(Q2_y_Bin_9)-(z_pT_Bin_22) (120.0°), (Q2_y_Bin_9)-(z_pT_Bin_23) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_29) (195.0°)
(Q2_y_Bin_9)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_4) (165.0°), (Q2_y_Bin_9)-(z_pT_Bin_5) (135.0°)
(Q2_y_Bin_9)-(z_pT_Bin_6) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_7) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_8) (120.0°)
(Q2_y_Bin_9)-(z_pT_Bin_9) (135.0°)

Above 120° (232/452 (51.3%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_17) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (225.0°)
(Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_23) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_31) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_32) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_5) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (195.0°)
(Q2_y_Bin_10)-(z_pT_Bin_1) (150.0°), (Q2_y_Bin_10)-(z_pT_Bin_15) (150.0°), (Q2_y_Bin_10)-(z_pT_Bin_2) (150.0°)
(Q2_y_Bin_10)-(z_pT_Bin_26) (150.0°), (Q2_y_Bin_10)-(z_pT_Bin_3) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_31) (165.0°)
(Q2_y_Bin_10)-(z_pT_Bin_32) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_4) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_5) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_7) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_1) (165.0°)
(Q2_y_Bin_11)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_20) (150.0°)
(Q2_y_Bin_11)-(z_pT_Bin_21) (180.0°), (Q2_y_Bin_11)-(z_pT_Bin_22) (240.0°), (Q2_y_Bin_11)-(z_pT_Bin_23) (225.0°)
(Q2_y_Bin_11)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_11)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_4) (345.0°)
(Q2_y_Bin_11)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_9) (135.0°), (Q2_y_Bin_12)-(z_pT_Bin_11) (195.0°)
(Q2_y_Bin_12)-(z_pT_Bin_14) (315.0°), (Q2_y_Bin_12)-(z_pT_Bin_19) (255.0°), (Q2_y_Bin_12)-(z_pT_Bin_21) (360.0°)
(Q2_y_Bin_12)-(z_pT_Bin_22) (270.0°), (Q2_y_Bin_12)-(z_pT_Bin_23) (285.0°), (Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°)
(Q2_y_Bin_12)-(z_pT_Bin_6) (225.0°), (Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_13)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_14)-(z_pT_Bin_2) (150.0°), (Q2_y_Bin_14)-(z_pT_Bin_32) (150.0°)
(Q2_y_Bin_14)-(z_pT_Bin_4) (150.0°), (Q2_y_Bin_14)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_1) (180.0°)
(Q2_y_Bin_15)-(z_pT_Bin_15) (225.0°), (Q2_y_Bin_15)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_21) (135.0°)
(Q2_y_Bin_15)-(z_pT_Bin_22) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_23) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_24) (240.0°)
(Q2_y_Bin_15)-(z_pT_Bin_9) (165.0°), (Q2_y_Bin_16)-(z_pT_Bin_6) (150.0°), (Q2_y_Bin_17)-(z_pT_Bin_4) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_1) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_10) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_11) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_13) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_15) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_16) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_19) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_2) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_20) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_21) (135.0°), (Q2_y_Bin_2)-(z_pT_Bin_25) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_26) (135.0°), (Q2_y_Bin_2)-(z_pT_Bin_27) (135.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_32) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_33) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_34) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_4) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_8) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°)
(Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_12) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_13) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_14) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_15) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_16) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_17) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_18) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_20) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_21) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_22) (135.0°)
(Q2_y_Bin_3)-(z_pT_Bin_23) (135.0°), (Q2_y_Bin_3)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_3) (255.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_8) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_14) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_15) (330.0°), (Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_19) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_22) (300.0°), (Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°)
(Q2_y_Bin_4)-(z_pT_Bin_26) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_27) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_28) (300.0°)
(Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (240.0°)
(Q2_y_Bin_5)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_14) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_15) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_19) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (240.0°)
(Q2_y_Bin_5)-(z_pT_Bin_20) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_25) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°)
(Q2_y_Bin_5)-(z_pT_Bin_31) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_32) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_4) (210.0°)
(Q2_y_Bin_5)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_6) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_7) (240.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_6)-(z_pT_Bin_1) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_19) (135.0°)
(Q2_y_Bin_6)-(z_pT_Bin_2) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_20) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_25) (240.0°)
(Q2_y_Bin_6)-(z_pT_Bin_26) (270.0°), (Q2_y_Bin_6)-(z_pT_Bin_27) (195.0°), (Q2_y_Bin_6)-(z_pT_Bin_28) (150.0°)
(Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_6) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_7) (135.0°), (Q2_y_Bin_6)-(z_pT_Bin_8) (150.0°)
(Q2_y_Bin_6)-(z_pT_Bin_9) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_10) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_13) (195.0°)
(Q2_y_Bin_7)-(z_pT_Bin_15) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_16) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_17) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_18) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°)
(Q2_y_Bin_7)-(z_pT_Bin_23) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_24) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_26) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_27) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_29) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°)
(Q2_y_Bin_7)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°), (Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°)
(Q2_y_Bin_7)-(z_pT_Bin_34) (255.0°), (Q2_y_Bin_7)-(z_pT_Bin_35) (300.0°), (Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°)
(Q2_y_Bin_7)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_9) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°)
(Q2_y_Bin_8)-(z_pT_Bin_12) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_16) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_18) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_19) (210.0°)
(Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_21) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_23) (150.0°)
(Q2_y_Bin_8)-(z_pT_Bin_24) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_25) (330.0°), (Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°)
(Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_30) (315.0°), (Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_9)-(z_pT_Bin_1) (210.0°), (Q2_y_Bin_9)-(z_pT_Bin_10) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_16) (150.0°)
(Q2_y_Bin_9)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_29) (195.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (180.0°)
(Q2_y_Bin_9)-(z_pT_Bin_4) (165.0°), (Q2_y_Bin_9)-(z_pT_Bin_5) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_6) (135.0°)
(Q2_y_Bin_9)-(z_pT_Bin_9) (135.0°)

Above 135° (209/452 (46.2%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°)
(Q2_y_Bin_1)-(z_pT_Bin_23) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°)
(Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_5) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (195.0°)
(Q2_y_Bin_10)-(z_pT_Bin_1) (150.0°), (Q2_y_Bin_10)-(z_pT_Bin_15) (150.0°), (Q2_y_Bin_10)-(z_pT_Bin_2) (150.0°)
(Q2_y_Bin_10)-(z_pT_Bin_26) (150.0°), (Q2_y_Bin_10)-(z_pT_Bin_3) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_31) (165.0°)
(Q2_y_Bin_10)-(z_pT_Bin_32) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_4) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_5) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_7) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_1) (165.0°)
(Q2_y_Bin_11)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_20) (150.0°)
(Q2_y_Bin_11)-(z_pT_Bin_21) (180.0°), (Q2_y_Bin_11)-(z_pT_Bin_22) (240.0°), (Q2_y_Bin_11)-(z_pT_Bin_23) (225.0°)
(Q2_y_Bin_11)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_11)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_4) (345.0°)
(Q2_y_Bin_11)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_12)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_12)-(z_pT_Bin_14) (315.0°)
(Q2_y_Bin_12)-(z_pT_Bin_19) (255.0°), (Q2_y_Bin_12)-(z_pT_Bin_21) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_22) (270.0°)
(Q2_y_Bin_12)-(z_pT_Bin_23) (285.0°), (Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_6) (225.0°)
(Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_13)-(z_pT_Bin_1) (180.0°)
(Q2_y_Bin_14)-(z_pT_Bin_2) (150.0°), (Q2_y_Bin_14)-(z_pT_Bin_32) (150.0°), (Q2_y_Bin_14)-(z_pT_Bin_4) (150.0°)
(Q2_y_Bin_14)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (225.0°)
(Q2_y_Bin_15)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_22) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_23) (195.0°)
(Q2_y_Bin_15)-(z_pT_Bin_24) (240.0°), (Q2_y_Bin_15)-(z_pT_Bin_9) (165.0°), (Q2_y_Bin_16)-(z_pT_Bin_6) (150.0°)
(Q2_y_Bin_17)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_1) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_10) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_11) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_13) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_15) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_16) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_19) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_2) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_20) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_25) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_32) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_33) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_34) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_4) (225.0°)
(Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_7) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_12) (165.0°)
(Q2_y_Bin_3)-(z_pT_Bin_13) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_14) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_15) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_16) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_17) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_18) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_20) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_21) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_3) (255.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_8) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_9) (180.0°)
(Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_14) (150.0°)
(Q2_y_Bin_4)-(z_pT_Bin_15) (330.0°), (Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_19) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (300.0°)
(Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_26) (150.0°)
(Q2_y_Bin_4)-(z_pT_Bin_27) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_28) (300.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_10) (150.0°)
(Q2_y_Bin_5)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_15) (150.0°)
(Q2_y_Bin_5)-(z_pT_Bin_19) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_20) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_25) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_31) (210.0°)
(Q2_y_Bin_5)-(z_pT_Bin_32) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_4) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_5) (195.0°)
(Q2_y_Bin_5)-(z_pT_Bin_6) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_7) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_6)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_10) (150.0°)
(Q2_y_Bin_6)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_2) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_20) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_6)-(z_pT_Bin_26) (270.0°), (Q2_y_Bin_6)-(z_pT_Bin_27) (195.0°)
(Q2_y_Bin_6)-(z_pT_Bin_28) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_6) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_8) (150.0°)
(Q2_y_Bin_6)-(z_pT_Bin_9) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_10) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_13) (195.0°)
(Q2_y_Bin_7)-(z_pT_Bin_15) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_16) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_17) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_24) (195.0°)
(Q2_y_Bin_7)-(z_pT_Bin_26) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_31) (240.0°)
(Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°), (Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_34) (255.0°)
(Q2_y_Bin_7)-(z_pT_Bin_35) (300.0°), (Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_7)-(z_pT_Bin_7) (165.0°)
(Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_16) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_19) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_21) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_23) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_24) (210.0°)
(Q2_y_Bin_8)-(z_pT_Bin_25) (330.0°), (Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°)
(Q2_y_Bin_8)-(z_pT_Bin_30) (315.0°), (Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_9)-(z_pT_Bin_1) (210.0°)
(Q2_y_Bin_9)-(z_pT_Bin_16) (150.0°), (Q2_y_Bin_9)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_29) (195.0°)
(Q2_y_Bin_9)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_4) (165.0°)

Above 150° (169/452 (37.4%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°)
(Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_6) (165.0°)
(Q2_y_Bin_1)-(z_pT_Bin_8) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_10)-(z_pT_Bin_3) (165.0°)
(Q2_y_Bin_10)-(z_pT_Bin_31) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_32) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_4) (165.0°)
(Q2_y_Bin_10)-(z_pT_Bin_5) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_1) (165.0°)
(Q2_y_Bin_11)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_21) (180.0°), (Q2_y_Bin_11)-(z_pT_Bin_22) (240.0°)
(Q2_y_Bin_11)-(z_pT_Bin_23) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_11)-(z_pT_Bin_3) (210.0°)
(Q2_y_Bin_11)-(z_pT_Bin_4) (345.0°), (Q2_y_Bin_11)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_12)-(z_pT_Bin_11) (195.0°)
(Q2_y_Bin_12)-(z_pT_Bin_14) (315.0°), (Q2_y_Bin_12)-(z_pT_Bin_19) (255.0°), (Q2_y_Bin_12)-(z_pT_Bin_21) (360.0°)
(Q2_y_Bin_12)-(z_pT_Bin_22) (270.0°), (Q2_y_Bin_12)-(z_pT_Bin_23) (285.0°), (Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°)
(Q2_y_Bin_12)-(z_pT_Bin_6) (225.0°), (Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_13)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_14)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_1) (180.0°)
(Q2_y_Bin_15)-(z_pT_Bin_15) (225.0°), (Q2_y_Bin_15)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_22) (195.0°)
(Q2_y_Bin_15)-(z_pT_Bin_23) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_24) (240.0°), (Q2_y_Bin_15)-(z_pT_Bin_9) (165.0°)
(Q2_y_Bin_17)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_1) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_10) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_19) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_2) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_20) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_25) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_32) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_33) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_4) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_9) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_12) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_13) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_15) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_20) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_21) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_3) (255.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_15) (330.0°), (Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_19) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_22) (300.0°), (Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°)
(Q2_y_Bin_4)-(z_pT_Bin_27) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_28) (300.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_13) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_20) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_25) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_31) (210.0°)
(Q2_y_Bin_5)-(z_pT_Bin_32) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_4) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_5) (195.0°)
(Q2_y_Bin_5)-(z_pT_Bin_6) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_7) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_6)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_14) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_20) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_6)-(z_pT_Bin_26) (270.0°)
(Q2_y_Bin_6)-(z_pT_Bin_27) (195.0°), (Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_9) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_1) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_13) (195.0°)
(Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_24) (195.0°)
(Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°)
(Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_34) (255.0°), (Q2_y_Bin_7)-(z_pT_Bin_35) (300.0°)
(Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_7)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°)
(Q2_y_Bin_8)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_16) (195.0°)
(Q2_y_Bin_8)-(z_pT_Bin_19) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_24) (210.0°)
(Q2_y_Bin_8)-(z_pT_Bin_25) (330.0°), (Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°)
(Q2_y_Bin_8)-(z_pT_Bin_30) (315.0°), (Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_9)-(z_pT_Bin_1) (210.0°)
(Q2_y_Bin_9)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_29) (195.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (180.0°)
(Q2_y_Bin_9)-(z_pT_Bin_4) (165.0°)

Above 180° (114/452 (25.2%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (225.0°)
(Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_10)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_22) (240.0°)
(Q2_y_Bin_11)-(z_pT_Bin_23) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_11)-(z_pT_Bin_3) (210.0°)
(Q2_y_Bin_11)-(z_pT_Bin_4) (345.0°), (Q2_y_Bin_12)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_12)-(z_pT_Bin_14) (315.0°)
(Q2_y_Bin_12)-(z_pT_Bin_19) (255.0°), (Q2_y_Bin_12)-(z_pT_Bin_21) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_22) (270.0°)
(Q2_y_Bin_12)-(z_pT_Bin_23) (285.0°), (Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_6) (225.0°)
(Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_14)-(z_pT_Bin_5) (195.0°)
(Q2_y_Bin_15)-(z_pT_Bin_15) (225.0°), (Q2_y_Bin_15)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_22) (195.0°)
(Q2_y_Bin_15)-(z_pT_Bin_23) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_24) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_1) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_2) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°)
(Q2_y_Bin_2)-(z_pT_Bin_4) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_24) (255.0°)
(Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_3) (255.0°)
(Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°)
(Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_15) (330.0°)
(Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_19) (240.0°)
(Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (300.0°), (Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_27) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_28) (300.0°)
(Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (240.0°)
(Q2_y_Bin_5)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_31) (210.0°)
(Q2_y_Bin_5)-(z_pT_Bin_4) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_7) (240.0°)
(Q2_y_Bin_5)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_6)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_6)-(z_pT_Bin_26) (270.0°)
(Q2_y_Bin_6)-(z_pT_Bin_27) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_13) (195.0°)
(Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_24) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°)
(Q2_y_Bin_7)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°), (Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°)
(Q2_y_Bin_7)-(z_pT_Bin_34) (255.0°), (Q2_y_Bin_7)-(z_pT_Bin_35) (300.0°), (Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_16) (195.0°)
(Q2_y_Bin_8)-(z_pT_Bin_19) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_24) (210.0°)
(Q2_y_Bin_8)-(z_pT_Bin_25) (330.0°), (Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_30) (315.0°)
(Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_9)-(z_pT_Bin_1) (210.0°), (Q2_y_Bin_9)-(z_pT_Bin_29) (195.0°)

### sector / E6

Stage: spline, acceptance. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/electron_sector/eS6o/fit_copy.root`

Above 90° (292/452 (64.6%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_11) (120.0°)
(Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_17) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_23) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_31) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_32) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_4) (225.0°)
(Q2_y_Bin_1)-(z_pT_Bin_5) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_6) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_7) (120.0°)
(Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_1) (150.0°)
(Q2_y_Bin_10)-(z_pT_Bin_10) (120.0°), (Q2_y_Bin_10)-(z_pT_Bin_11) (105.0°), (Q2_y_Bin_10)-(z_pT_Bin_15) (135.0°)
(Q2_y_Bin_10)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_20) (120.0°), (Q2_y_Bin_10)-(z_pT_Bin_26) (135.0°)
(Q2_y_Bin_10)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_31) (120.0°), (Q2_y_Bin_10)-(z_pT_Bin_32) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_5) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_10)-(z_pT_Bin_7) (150.0°), (Q2_y_Bin_10)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_10)-(z_pT_Bin_9) (120.0°)
(Q2_y_Bin_11)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_11) (105.0°)
(Q2_y_Bin_11)-(z_pT_Bin_13) (105.0°), (Q2_y_Bin_11)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_11)-(z_pT_Bin_18) (105.0°)
(Q2_y_Bin_11)-(z_pT_Bin_19) (105.0°), (Q2_y_Bin_11)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_11)-(z_pT_Bin_20) (150.0°)
(Q2_y_Bin_11)-(z_pT_Bin_21) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_22) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_23) (210.0°)
(Q2_y_Bin_11)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_11)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_4) (315.0°)
(Q2_y_Bin_11)-(z_pT_Bin_6) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_11)-(z_pT_Bin_9) (135.0°)
(Q2_y_Bin_12)-(z_pT_Bin_11) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_12) (105.0°), (Q2_y_Bin_12)-(z_pT_Bin_13) (135.0°)
(Q2_y_Bin_12)-(z_pT_Bin_14) (300.0°), (Q2_y_Bin_12)-(z_pT_Bin_16) (105.0°), (Q2_y_Bin_12)-(z_pT_Bin_18) (120.0°)
(Q2_y_Bin_12)-(z_pT_Bin_19) (270.0°), (Q2_y_Bin_12)-(z_pT_Bin_21) (345.0°), (Q2_y_Bin_12)-(z_pT_Bin_22) (195.0°)
(Q2_y_Bin_12)-(z_pT_Bin_23) (270.0°), (Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_13)-(z_pT_Bin_1) (180.0°)
(Q2_y_Bin_13)-(z_pT_Bin_12) (105.0°), (Q2_y_Bin_13)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_13)-(z_pT_Bin_26) (120.0°)
(Q2_y_Bin_13)-(z_pT_Bin_3) (135.0°), (Q2_y_Bin_13)-(z_pT_Bin_4) (150.0°), (Q2_y_Bin_13)-(z_pT_Bin_5) (135.0°)
(Q2_y_Bin_13)-(z_pT_Bin_7) (105.0°), (Q2_y_Bin_13)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_14)-(z_pT_Bin_1) (120.0°)
(Q2_y_Bin_14)-(z_pT_Bin_10) (105.0°), (Q2_y_Bin_14)-(z_pT_Bin_2) (150.0°), (Q2_y_Bin_14)-(z_pT_Bin_26) (105.0°)
(Q2_y_Bin_14)-(z_pT_Bin_3) (135.0°), (Q2_y_Bin_14)-(z_pT_Bin_32) (120.0°), (Q2_y_Bin_14)-(z_pT_Bin_4) (165.0°)
(Q2_y_Bin_14)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_15)-(z_pT_Bin_19) (105.0°), (Q2_y_Bin_15)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_21) (105.0°)
(Q2_y_Bin_15)-(z_pT_Bin_22) (165.0°), (Q2_y_Bin_15)-(z_pT_Bin_23) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_24) (225.0°)
(Q2_y_Bin_15)-(z_pT_Bin_9) (150.0°), (Q2_y_Bin_16)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_16)-(z_pT_Bin_4) (120.0°)
(Q2_y_Bin_16)-(z_pT_Bin_5) (150.0°), (Q2_y_Bin_16)-(z_pT_Bin_6) (180.0°), (Q2_y_Bin_16)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_17)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_17)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_17)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_17)-(z_pT_Bin_4) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_1) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_10) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_11) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_12) (105.0°), (Q2_y_Bin_2)-(z_pT_Bin_13) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_15) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_16) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_17) (105.0°), (Q2_y_Bin_2)-(z_pT_Bin_18) (105.0°), (Q2_y_Bin_2)-(z_pT_Bin_19) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_20) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_21) (120.0°)
(Q2_y_Bin_2)-(z_pT_Bin_22) (105.0°), (Q2_y_Bin_2)-(z_pT_Bin_25) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_26) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_27) (120.0°), (Q2_y_Bin_2)-(z_pT_Bin_28) (120.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_32) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_33) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_34) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_4) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_5) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_6) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_8) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_9) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°)
(Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_12) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_13) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_14) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_15) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_16) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_17) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_18) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_19) (120.0°)
(Q2_y_Bin_3)-(z_pT_Bin_2) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_20) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_21) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_22) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_23) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_24) (270.0°)
(Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_3) (285.0°)
(Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_4)-(z_pT_Bin_15) (345.0°)
(Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_19) (225.0°)
(Q2_y_Bin_4)-(z_pT_Bin_20) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (330.0°)
(Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_25) (255.0°), (Q2_y_Bin_4)-(z_pT_Bin_26) (165.0°)
(Q2_y_Bin_4)-(z_pT_Bin_27) (225.0°), (Q2_y_Bin_4)-(z_pT_Bin_28) (315.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_10) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_11) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_14) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_15) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_19) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (225.0°)
(Q2_y_Bin_5)-(z_pT_Bin_20) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_25) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_26) (105.0°)
(Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_31) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_32) (150.0°)
(Q2_y_Bin_5)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_5) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_6) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_7) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_9) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_10) (135.0°), (Q2_y_Bin_6)-(z_pT_Bin_11) (105.0°)
(Q2_y_Bin_6)-(z_pT_Bin_13) (120.0°), (Q2_y_Bin_6)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_15) (135.0°)
(Q2_y_Bin_6)-(z_pT_Bin_19) (135.0°), (Q2_y_Bin_6)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_20) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_21) (105.0°), (Q2_y_Bin_6)-(z_pT_Bin_25) (225.0°), (Q2_y_Bin_6)-(z_pT_Bin_26) (270.0°)
(Q2_y_Bin_6)-(z_pT_Bin_27) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_28) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_6) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_7) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_8) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_9) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_13) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_15) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_16) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_17) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_18) (135.0°)
(Q2_y_Bin_7)-(z_pT_Bin_19) (105.0°), (Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_20) (120.0°)
(Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_22) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_23) (120.0°)
(Q2_y_Bin_7)-(z_pT_Bin_24) (225.0°), (Q2_y_Bin_7)-(z_pT_Bin_25) (105.0°), (Q2_y_Bin_7)-(z_pT_Bin_26) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_27) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_28) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_29) (135.0°)
(Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_31) (255.0°), (Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°)
(Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_34) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_35) (300.0°)
(Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_7)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_8) (105.0°)
(Q2_y_Bin_7)-(z_pT_Bin_9) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_12) (135.0°)
(Q2_y_Bin_8)-(z_pT_Bin_13) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_16) (210.0°)
(Q2_y_Bin_8)-(z_pT_Bin_18) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_19) (225.0°), (Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_21) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_23) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_24) (240.0°)
(Q2_y_Bin_8)-(z_pT_Bin_25) (330.0°), (Q2_y_Bin_8)-(z_pT_Bin_26) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°)
(Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_30) (330.0°), (Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_9)-(z_pT_Bin_1) (210.0°), (Q2_y_Bin_9)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_9)-(z_pT_Bin_15) (105.0°)
(Q2_y_Bin_9)-(z_pT_Bin_16) (150.0°), (Q2_y_Bin_9)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_22) (120.0°)
(Q2_y_Bin_9)-(z_pT_Bin_29) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_4) (180.0°)
(Q2_y_Bin_9)-(z_pT_Bin_5) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_6) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_8) (120.0°)
(Q2_y_Bin_9)-(z_pT_Bin_9) (135.0°)

Above 120° (240/452 (53.1%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_17) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (240.0°)
(Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_23) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_31) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_32) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_4) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_5) (210.0°)
(Q2_y_Bin_1)-(z_pT_Bin_6) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (210.0°)
(Q2_y_Bin_10)-(z_pT_Bin_1) (150.0°), (Q2_y_Bin_10)-(z_pT_Bin_15) (135.0°), (Q2_y_Bin_10)-(z_pT_Bin_2) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_26) (135.0°), (Q2_y_Bin_10)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_32) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_5) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_10)-(z_pT_Bin_7) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_10) (150.0°)
(Q2_y_Bin_11)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_11)-(z_pT_Bin_20) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_21) (150.0°)
(Q2_y_Bin_11)-(z_pT_Bin_22) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_23) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_24) (255.0°)
(Q2_y_Bin_11)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_4) (315.0°), (Q2_y_Bin_11)-(z_pT_Bin_6) (150.0°)
(Q2_y_Bin_11)-(z_pT_Bin_9) (135.0°), (Q2_y_Bin_12)-(z_pT_Bin_11) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_13) (135.0°)
(Q2_y_Bin_12)-(z_pT_Bin_14) (300.0°), (Q2_y_Bin_12)-(z_pT_Bin_19) (270.0°), (Q2_y_Bin_12)-(z_pT_Bin_21) (345.0°)
(Q2_y_Bin_12)-(z_pT_Bin_22) (195.0°), (Q2_y_Bin_12)-(z_pT_Bin_23) (270.0°), (Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°)
(Q2_y_Bin_12)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_13)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_13)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_13)-(z_pT_Bin_3) (135.0°)
(Q2_y_Bin_13)-(z_pT_Bin_4) (150.0°), (Q2_y_Bin_13)-(z_pT_Bin_5) (135.0°), (Q2_y_Bin_14)-(z_pT_Bin_2) (150.0°)
(Q2_y_Bin_14)-(z_pT_Bin_3) (135.0°), (Q2_y_Bin_14)-(z_pT_Bin_4) (165.0°), (Q2_y_Bin_14)-(z_pT_Bin_5) (195.0°)
(Q2_y_Bin_15)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_15)-(z_pT_Bin_22) (165.0°), (Q2_y_Bin_15)-(z_pT_Bin_23) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_24) (225.0°)
(Q2_y_Bin_15)-(z_pT_Bin_9) (150.0°), (Q2_y_Bin_16)-(z_pT_Bin_5) (150.0°), (Q2_y_Bin_16)-(z_pT_Bin_6) (180.0°)
(Q2_y_Bin_17)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_17)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_17)-(z_pT_Bin_4) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_1) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_10) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_11) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_15) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_19) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_2) (240.0°)
(Q2_y_Bin_2)-(z_pT_Bin_20) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_25) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_26) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_32) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_33) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_34) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_4) (240.0°)
(Q2_y_Bin_2)-(z_pT_Bin_5) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_6) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°)
(Q2_y_Bin_2)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_9) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_12) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_14) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_16) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_17) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_18) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_2) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_20) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_21) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_22) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_23) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_24) (270.0°)
(Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_3) (285.0°)
(Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_4)-(z_pT_Bin_15) (345.0°)
(Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_19) (225.0°)
(Q2_y_Bin_4)-(z_pT_Bin_20) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (330.0°)
(Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_25) (255.0°), (Q2_y_Bin_4)-(z_pT_Bin_26) (165.0°)
(Q2_y_Bin_4)-(z_pT_Bin_27) (225.0°), (Q2_y_Bin_4)-(z_pT_Bin_28) (315.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_10) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_15) (150.0°)
(Q2_y_Bin_5)-(z_pT_Bin_19) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (225.0°), (Q2_y_Bin_5)-(z_pT_Bin_20) (150.0°)
(Q2_y_Bin_5)-(z_pT_Bin_25) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_31) (210.0°)
(Q2_y_Bin_5)-(z_pT_Bin_32) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_5) (210.0°)
(Q2_y_Bin_5)-(z_pT_Bin_6) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_7) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_6)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_15) (135.0°), (Q2_y_Bin_6)-(z_pT_Bin_19) (135.0°)
(Q2_y_Bin_6)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_20) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_25) (225.0°)
(Q2_y_Bin_6)-(z_pT_Bin_26) (270.0°), (Q2_y_Bin_6)-(z_pT_Bin_27) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_28) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_7) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_8) (150.0°)
(Q2_y_Bin_6)-(z_pT_Bin_9) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_10) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_13) (180.0°)
(Q2_y_Bin_7)-(z_pT_Bin_15) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_16) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_17) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_18) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°)
(Q2_y_Bin_7)-(z_pT_Bin_22) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_24) (225.0°), (Q2_y_Bin_7)-(z_pT_Bin_26) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_27) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_28) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_29) (135.0°)
(Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_31) (255.0°), (Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°)
(Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_34) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_35) (300.0°)
(Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_7)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_9) (150.0°)
(Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_12) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_13) (180.0°)
(Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_16) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_18) (150.0°)
(Q2_y_Bin_8)-(z_pT_Bin_19) (225.0°), (Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_21) (150.0°)
(Q2_y_Bin_8)-(z_pT_Bin_23) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_24) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_25) (330.0°)
(Q2_y_Bin_8)-(z_pT_Bin_26) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°)
(Q2_y_Bin_8)-(z_pT_Bin_30) (330.0°), (Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_9)-(z_pT_Bin_1) (210.0°)
(Q2_y_Bin_9)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_9)-(z_pT_Bin_16) (150.0°), (Q2_y_Bin_9)-(z_pT_Bin_2) (180.0°)
(Q2_y_Bin_9)-(z_pT_Bin_29) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_4) (180.0°)
(Q2_y_Bin_9)-(z_pT_Bin_5) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_6) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_9) (135.0°)

Above 135° (216/452 (47.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°)
(Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_4) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_5) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_6) (180.0°)
(Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_1) (150.0°)
(Q2_y_Bin_10)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_32) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_5) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_10)-(z_pT_Bin_7) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_10) (150.0°)
(Q2_y_Bin_11)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_11)-(z_pT_Bin_20) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_21) (150.0°)
(Q2_y_Bin_11)-(z_pT_Bin_22) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_23) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_24) (255.0°)
(Q2_y_Bin_11)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_4) (315.0°), (Q2_y_Bin_11)-(z_pT_Bin_6) (150.0°)
(Q2_y_Bin_12)-(z_pT_Bin_11) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_14) (300.0°), (Q2_y_Bin_12)-(z_pT_Bin_19) (270.0°)
(Q2_y_Bin_12)-(z_pT_Bin_21) (345.0°), (Q2_y_Bin_12)-(z_pT_Bin_22) (195.0°), (Q2_y_Bin_12)-(z_pT_Bin_23) (270.0°)
(Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°)
(Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_13)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_13)-(z_pT_Bin_4) (150.0°)
(Q2_y_Bin_14)-(z_pT_Bin_2) (150.0°), (Q2_y_Bin_14)-(z_pT_Bin_4) (165.0°), (Q2_y_Bin_14)-(z_pT_Bin_5) (195.0°)
(Q2_y_Bin_15)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_15)-(z_pT_Bin_22) (165.0°), (Q2_y_Bin_15)-(z_pT_Bin_23) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_24) (225.0°)
(Q2_y_Bin_15)-(z_pT_Bin_9) (150.0°), (Q2_y_Bin_16)-(z_pT_Bin_5) (150.0°), (Q2_y_Bin_16)-(z_pT_Bin_6) (180.0°)
(Q2_y_Bin_17)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_17)-(z_pT_Bin_4) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_1) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_10) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_11) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_13) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_15) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_16) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_19) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_20) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_25) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_26) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_32) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_33) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_34) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_4) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_5) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_6) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_8) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_9) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°)
(Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_12) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_13) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_14) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_15) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_16) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_17) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_18) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_2) (210.0°)
(Q2_y_Bin_3)-(z_pT_Bin_20) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_21) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_22) (165.0°)
(Q2_y_Bin_3)-(z_pT_Bin_23) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_24) (270.0°), (Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_3) (285.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_8) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_4)-(z_pT_Bin_15) (345.0°), (Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_19) (225.0°), (Q2_y_Bin_4)-(z_pT_Bin_20) (150.0°)
(Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (330.0°), (Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_25) (255.0°), (Q2_y_Bin_4)-(z_pT_Bin_26) (165.0°), (Q2_y_Bin_4)-(z_pT_Bin_27) (225.0°)
(Q2_y_Bin_4)-(z_pT_Bin_28) (315.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_13) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_15) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_19) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_2) (225.0°), (Q2_y_Bin_5)-(z_pT_Bin_20) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_25) (150.0°)
(Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_31) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_32) (150.0°)
(Q2_y_Bin_5)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_5) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_6) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_7) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_9) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_2) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_20) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_25) (225.0°), (Q2_y_Bin_6)-(z_pT_Bin_26) (270.0°)
(Q2_y_Bin_6)-(z_pT_Bin_27) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_28) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_6) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_7) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_8) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_9) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_13) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_15) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_16) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_17) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_22) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_24) (225.0°)
(Q2_y_Bin_7)-(z_pT_Bin_26) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_28) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°)
(Q2_y_Bin_7)-(z_pT_Bin_31) (255.0°), (Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°), (Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°)
(Q2_y_Bin_7)-(z_pT_Bin_34) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_35) (300.0°), (Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°)
(Q2_y_Bin_7)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_9) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°)
(Q2_y_Bin_8)-(z_pT_Bin_13) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_16) (210.0°)
(Q2_y_Bin_8)-(z_pT_Bin_18) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_19) (225.0°), (Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_21) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_23) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_24) (240.0°)
(Q2_y_Bin_8)-(z_pT_Bin_25) (330.0°), (Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°)
(Q2_y_Bin_8)-(z_pT_Bin_30) (330.0°), (Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_9)-(z_pT_Bin_1) (210.0°)
(Q2_y_Bin_9)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_9)-(z_pT_Bin_16) (150.0°), (Q2_y_Bin_9)-(z_pT_Bin_2) (180.0°)
(Q2_y_Bin_9)-(z_pT_Bin_29) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_4) (180.0°)

Above 150° (181/452 (40.0%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°)
(Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_4) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_5) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_6) (180.0°)
(Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_2) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_32) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_4) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_5) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_1) (165.0°)
(Q2_y_Bin_11)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_11)-(z_pT_Bin_22) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_23) (210.0°)
(Q2_y_Bin_11)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_11)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_4) (315.0°)
(Q2_y_Bin_12)-(z_pT_Bin_11) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_14) (300.0°), (Q2_y_Bin_12)-(z_pT_Bin_19) (270.0°)
(Q2_y_Bin_12)-(z_pT_Bin_21) (345.0°), (Q2_y_Bin_12)-(z_pT_Bin_22) (195.0°), (Q2_y_Bin_12)-(z_pT_Bin_23) (270.0°)
(Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°)
(Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_13)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_14)-(z_pT_Bin_4) (165.0°)
(Q2_y_Bin_14)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_15)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_22) (165.0°), (Q2_y_Bin_15)-(z_pT_Bin_23) (180.0°)
(Q2_y_Bin_15)-(z_pT_Bin_24) (225.0°), (Q2_y_Bin_16)-(z_pT_Bin_6) (180.0°), (Q2_y_Bin_17)-(z_pT_Bin_2) (165.0°)
(Q2_y_Bin_17)-(z_pT_Bin_4) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_1) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_10) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_15) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_19) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_2) (240.0°)
(Q2_y_Bin_2)-(z_pT_Bin_20) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_25) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_32) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_34) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_4) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_5) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_6) (225.0°)
(Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_9) (210.0°)
(Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_12) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_17) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_18) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_2) (210.0°)
(Q2_y_Bin_3)-(z_pT_Bin_20) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_21) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_22) (165.0°)
(Q2_y_Bin_3)-(z_pT_Bin_24) (270.0°), (Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_3) (285.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_9) (195.0°)
(Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_14) (165.0°)
(Q2_y_Bin_4)-(z_pT_Bin_15) (345.0°), (Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_19) (225.0°), (Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (330.0°)
(Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_25) (255.0°), (Q2_y_Bin_4)-(z_pT_Bin_26) (165.0°)
(Q2_y_Bin_4)-(z_pT_Bin_27) (225.0°), (Q2_y_Bin_4)-(z_pT_Bin_28) (315.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_10) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_19) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_2) (225.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_31) (210.0°)
(Q2_y_Bin_5)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_5) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_6) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_7) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_9) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_2) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_20) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_25) (225.0°), (Q2_y_Bin_6)-(z_pT_Bin_26) (270.0°)
(Q2_y_Bin_6)-(z_pT_Bin_27) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_28) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_6) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_9) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_1) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_13) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_24) (225.0°), (Q2_y_Bin_7)-(z_pT_Bin_26) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_31) (255.0°), (Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°)
(Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_34) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_35) (300.0°)
(Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_7)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°)
(Q2_y_Bin_8)-(z_pT_Bin_13) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_16) (210.0°)
(Q2_y_Bin_8)-(z_pT_Bin_19) (225.0°), (Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_24) (240.0°)
(Q2_y_Bin_8)-(z_pT_Bin_25) (330.0°), (Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°)
(Q2_y_Bin_8)-(z_pT_Bin_30) (330.0°), (Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_9)-(z_pT_Bin_1) (210.0°)
(Q2_y_Bin_9)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_29) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (180.0°)
(Q2_y_Bin_9)-(z_pT_Bin_4) (180.0°)

Above 180° (114/452 (25.2%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (240.0°)
(Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_4) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_5) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°)
(Q2_y_Bin_1)-(z_pT_Bin_9) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_22) (225.0°)
(Q2_y_Bin_11)-(z_pT_Bin_23) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_11)-(z_pT_Bin_3) (225.0°)
(Q2_y_Bin_11)-(z_pT_Bin_4) (315.0°), (Q2_y_Bin_12)-(z_pT_Bin_11) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_14) (300.0°)
(Q2_y_Bin_12)-(z_pT_Bin_19) (270.0°), (Q2_y_Bin_12)-(z_pT_Bin_21) (345.0°), (Q2_y_Bin_12)-(z_pT_Bin_22) (195.0°)
(Q2_y_Bin_12)-(z_pT_Bin_23) (270.0°), (Q2_y_Bin_12)-(z_pT_Bin_24) (360.0°), (Q2_y_Bin_12)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_14)-(z_pT_Bin_5) (195.0°)
(Q2_y_Bin_15)-(z_pT_Bin_15) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_24) (225.0°)
(Q2_y_Bin_2)-(z_pT_Bin_1) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_20) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_4) (240.0°)
(Q2_y_Bin_2)-(z_pT_Bin_5) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_6) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°)
(Q2_y_Bin_2)-(z_pT_Bin_9) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°)
(Q2_y_Bin_3)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_15) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_2) (210.0°)
(Q2_y_Bin_3)-(z_pT_Bin_20) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_21) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_24) (270.0°)
(Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_3) (285.0°)
(Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_9) (195.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_15) (345.0°), (Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_19) (225.0°), (Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (330.0°)
(Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_25) (255.0°), (Q2_y_Bin_4)-(z_pT_Bin_27) (225.0°)
(Q2_y_Bin_4)-(z_pT_Bin_28) (315.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (240.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (225.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°)
(Q2_y_Bin_5)-(z_pT_Bin_31) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_5) (210.0°)
(Q2_y_Bin_5)-(z_pT_Bin_7) (240.0°), (Q2_y_Bin_6)-(z_pT_Bin_25) (225.0°), (Q2_y_Bin_6)-(z_pT_Bin_26) (270.0°)
(Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_7)-(z_pT_Bin_24) (225.0°)
(Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_31) (255.0°), (Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°)
(Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_34) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_35) (300.0°)
(Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_16) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_19) (225.0°), (Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_24) (240.0°), (Q2_y_Bin_8)-(z_pT_Bin_25) (330.0°), (Q2_y_Bin_8)-(z_pT_Bin_29) (240.0°)
(Q2_y_Bin_8)-(z_pT_Bin_30) (330.0°), (Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_9)-(z_pT_Bin_1) (210.0°)

### sector / P6

Stage: spline, acceptance. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/pion_sector/pipS6o/fit_copy.root`

Above 90° (279/452 (61.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_11) (105.0°)
(Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_16) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_17) (120.0°)
(Q2_y_Bin_1)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_23) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_31) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_32) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_4) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_7) (150.0°)
(Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_1) (150.0°)
(Q2_y_Bin_10)-(z_pT_Bin_10) (120.0°), (Q2_y_Bin_10)-(z_pT_Bin_13) (120.0°), (Q2_y_Bin_10)-(z_pT_Bin_15) (120.0°)
(Q2_y_Bin_10)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_20) (120.0°), (Q2_y_Bin_10)-(z_pT_Bin_26) (135.0°)
(Q2_y_Bin_10)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_31) (135.0°), (Q2_y_Bin_10)-(z_pT_Bin_32) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_6) (195.0°)
(Q2_y_Bin_10)-(z_pT_Bin_7) (150.0°), (Q2_y_Bin_10)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_10)-(z_pT_Bin_9) (120.0°)
(Q2_y_Bin_11)-(z_pT_Bin_1) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_10) (135.0°), (Q2_y_Bin_11)-(z_pT_Bin_13) (105.0°)
(Q2_y_Bin_11)-(z_pT_Bin_15) (105.0°), (Q2_y_Bin_11)-(z_pT_Bin_18) (105.0°), (Q2_y_Bin_11)-(z_pT_Bin_2) (165.0°)
(Q2_y_Bin_11)-(z_pT_Bin_20) (120.0°), (Q2_y_Bin_11)-(z_pT_Bin_21) (135.0°), (Q2_y_Bin_11)-(z_pT_Bin_22) (210.0°)
(Q2_y_Bin_11)-(z_pT_Bin_23) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_11)-(z_pT_Bin_3) (210.0°)
(Q2_y_Bin_11)-(z_pT_Bin_4) (300.0°), (Q2_y_Bin_11)-(z_pT_Bin_6) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_12)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_12)-(z_pT_Bin_13) (120.0°), (Q2_y_Bin_12)-(z_pT_Bin_14) (270.0°)
(Q2_y_Bin_12)-(z_pT_Bin_16) (120.0°), (Q2_y_Bin_12)-(z_pT_Bin_18) (120.0°), (Q2_y_Bin_12)-(z_pT_Bin_19) (255.0°)
(Q2_y_Bin_12)-(z_pT_Bin_21) (300.0°), (Q2_y_Bin_12)-(z_pT_Bin_22) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_23) (240.0°)
(Q2_y_Bin_12)-(z_pT_Bin_24) (345.0°), (Q2_y_Bin_12)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°)
(Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_13)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_13)-(z_pT_Bin_12) (105.0°)
(Q2_y_Bin_13)-(z_pT_Bin_2) (120.0°), (Q2_y_Bin_13)-(z_pT_Bin_26) (120.0°), (Q2_y_Bin_13)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_13)-(z_pT_Bin_4) (135.0°), (Q2_y_Bin_13)-(z_pT_Bin_5) (105.0°), (Q2_y_Bin_13)-(z_pT_Bin_7) (105.0°)
(Q2_y_Bin_13)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_14)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_14)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_14)-(z_pT_Bin_32) (150.0°), (Q2_y_Bin_14)-(z_pT_Bin_4) (135.0°), (Q2_y_Bin_14)-(z_pT_Bin_5) (195.0°)
(Q2_y_Bin_15)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_19) (105.0°)
(Q2_y_Bin_15)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_21) (120.0°), (Q2_y_Bin_15)-(z_pT_Bin_22) (180.0°)
(Q2_y_Bin_15)-(z_pT_Bin_23) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_24) (240.0°), (Q2_y_Bin_15)-(z_pT_Bin_6) (105.0°)
(Q2_y_Bin_15)-(z_pT_Bin_9) (150.0°), (Q2_y_Bin_16)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_16)-(z_pT_Bin_4) (120.0°)
(Q2_y_Bin_16)-(z_pT_Bin_6) (150.0°), (Q2_y_Bin_17)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_2)-(z_pT_Bin_1) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_11) (135.0°), (Q2_y_Bin_2)-(z_pT_Bin_12) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_15) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_16) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_19) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_2) (225.0°)
(Q2_y_Bin_2)-(z_pT_Bin_20) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_21) (135.0°), (Q2_y_Bin_2)-(z_pT_Bin_25) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_26) (135.0°), (Q2_y_Bin_2)-(z_pT_Bin_27) (105.0°), (Q2_y_Bin_2)-(z_pT_Bin_28) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_32) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_33) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_34) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_4) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°)
(Q2_y_Bin_2)-(z_pT_Bin_8) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_12) (165.0°)
(Q2_y_Bin_3)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_14) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_15) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_17) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_18) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_19) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_20) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_21) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_22) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_23) (135.0°)
(Q2_y_Bin_3)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_29) (345.0°)
(Q2_y_Bin_3)-(z_pT_Bin_3) (285.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_9) (180.0°)
(Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_14) (165.0°)
(Q2_y_Bin_4)-(z_pT_Bin_15) (315.0°), (Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_19) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_20) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_22) (285.0°), (Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°)
(Q2_y_Bin_4)-(z_pT_Bin_26) (165.0°), (Q2_y_Bin_4)-(z_pT_Bin_27) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_28) (315.0°)
(Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (225.0°)
(Q2_y_Bin_5)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_13) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_14) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_15) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_19) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (255.0°)
(Q2_y_Bin_5)-(z_pT_Bin_20) (135.0°), (Q2_y_Bin_5)-(z_pT_Bin_25) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_26) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_31) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_32) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_6) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_7) (225.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_9) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_10) (135.0°), (Q2_y_Bin_6)-(z_pT_Bin_11) (105.0°)
(Q2_y_Bin_6)-(z_pT_Bin_13) (120.0°), (Q2_y_Bin_6)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_15) (120.0°)
(Q2_y_Bin_6)-(z_pT_Bin_16) (105.0°), (Q2_y_Bin_6)-(z_pT_Bin_19) (120.0°), (Q2_y_Bin_6)-(z_pT_Bin_2) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_20) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_25) (210.0°), (Q2_y_Bin_6)-(z_pT_Bin_26) (225.0°)
(Q2_y_Bin_6)-(z_pT_Bin_27) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_28) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_6) (150.0°)
(Q2_y_Bin_6)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_8) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_9) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_15) (135.0°)
(Q2_y_Bin_7)-(z_pT_Bin_16) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_17) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_18) (120.0°)
(Q2_y_Bin_7)-(z_pT_Bin_19) (120.0°), (Q2_y_Bin_7)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_20) (120.0°)
(Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_22) (120.0°), (Q2_y_Bin_7)-(z_pT_Bin_23) (120.0°)
(Q2_y_Bin_7)-(z_pT_Bin_24) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_25) (105.0°), (Q2_y_Bin_7)-(z_pT_Bin_26) (135.0°)
(Q2_y_Bin_7)-(z_pT_Bin_27) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_28) (120.0°), (Q2_y_Bin_7)-(z_pT_Bin_29) (135.0°)
(Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_31) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°)
(Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_34) (225.0°), (Q2_y_Bin_7)-(z_pT_Bin_35) (330.0°)
(Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_7)-(z_pT_Bin_7) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_8) (120.0°)
(Q2_y_Bin_7)-(z_pT_Bin_9) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_12) (135.0°)
(Q2_y_Bin_8)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_16) (195.0°)
(Q2_y_Bin_8)-(z_pT_Bin_18) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_19) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_21) (165.0°), (Q2_y_Bin_8)-(z_pT_Bin_23) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_24) (210.0°)
(Q2_y_Bin_8)-(z_pT_Bin_25) (345.0°), (Q2_y_Bin_8)-(z_pT_Bin_26) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°)
(Q2_y_Bin_8)-(z_pT_Bin_29) (225.0°), (Q2_y_Bin_8)-(z_pT_Bin_30) (285.0°), (Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_9)-(z_pT_Bin_1) (210.0°), (Q2_y_Bin_9)-(z_pT_Bin_10) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_11) (105.0°)
(Q2_y_Bin_9)-(z_pT_Bin_15) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_16) (120.0°), (Q2_y_Bin_9)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_9)-(z_pT_Bin_22) (120.0°), (Q2_y_Bin_9)-(z_pT_Bin_29) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (195.0°)
(Q2_y_Bin_9)-(z_pT_Bin_30) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_4) (165.0°), (Q2_y_Bin_9)-(z_pT_Bin_5) (135.0°)
(Q2_y_Bin_9)-(z_pT_Bin_6) (120.0°), (Q2_y_Bin_9)-(z_pT_Bin_8) (150.0°), (Q2_y_Bin_9)-(z_pT_Bin_9) (120.0°)

Above 120° (226/452 (50.0%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_16) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°)
(Q2_y_Bin_1)-(z_pT_Bin_23) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°)
(Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_31) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_32) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_6) (165.0°)
(Q2_y_Bin_1)-(z_pT_Bin_7) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (210.0°)
(Q2_y_Bin_10)-(z_pT_Bin_1) (150.0°), (Q2_y_Bin_10)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_26) (135.0°)
(Q2_y_Bin_10)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_31) (135.0°), (Q2_y_Bin_10)-(z_pT_Bin_32) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_6) (195.0°)
(Q2_y_Bin_10)-(z_pT_Bin_7) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_1) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_11)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_21) (135.0°), (Q2_y_Bin_11)-(z_pT_Bin_22) (210.0°)
(Q2_y_Bin_11)-(z_pT_Bin_23) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_11)-(z_pT_Bin_3) (210.0°)
(Q2_y_Bin_11)-(z_pT_Bin_4) (300.0°), (Q2_y_Bin_11)-(z_pT_Bin_6) (150.0°), (Q2_y_Bin_12)-(z_pT_Bin_11) (195.0°)
(Q2_y_Bin_12)-(z_pT_Bin_14) (270.0°), (Q2_y_Bin_12)-(z_pT_Bin_19) (255.0°), (Q2_y_Bin_12)-(z_pT_Bin_21) (300.0°)
(Q2_y_Bin_12)-(z_pT_Bin_22) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_23) (240.0°), (Q2_y_Bin_12)-(z_pT_Bin_24) (345.0°)
(Q2_y_Bin_12)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_13)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_13)-(z_pT_Bin_4) (135.0°), (Q2_y_Bin_14)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_14)-(z_pT_Bin_32) (150.0°), (Q2_y_Bin_14)-(z_pT_Bin_4) (135.0°), (Q2_y_Bin_14)-(z_pT_Bin_5) (195.0°)
(Q2_y_Bin_15)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_2) (180.0°)
(Q2_y_Bin_15)-(z_pT_Bin_22) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_23) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_24) (240.0°)
(Q2_y_Bin_15)-(z_pT_Bin_9) (150.0°), (Q2_y_Bin_16)-(z_pT_Bin_6) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_1) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_11) (135.0°), (Q2_y_Bin_2)-(z_pT_Bin_13) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_15) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_16) (150.0°)
(Q2_y_Bin_2)-(z_pT_Bin_19) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_2) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_20) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_21) (135.0°), (Q2_y_Bin_2)-(z_pT_Bin_25) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_26) (135.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_32) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_33) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_34) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_4) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°)
(Q2_y_Bin_2)-(z_pT_Bin_8) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_12) (165.0°)
(Q2_y_Bin_3)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_14) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_15) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_17) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_18) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_19) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_20) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_21) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_22) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_23) (135.0°)
(Q2_y_Bin_3)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_29) (345.0°)
(Q2_y_Bin_3)-(z_pT_Bin_3) (285.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_9) (180.0°)
(Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_14) (165.0°)
(Q2_y_Bin_4)-(z_pT_Bin_15) (315.0°), (Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_19) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_20) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_22) (285.0°), (Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°)
(Q2_y_Bin_4)-(z_pT_Bin_26) (165.0°), (Q2_y_Bin_4)-(z_pT_Bin_27) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_28) (315.0°)
(Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (225.0°)
(Q2_y_Bin_5)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_13) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_14) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_15) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_19) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (255.0°)
(Q2_y_Bin_5)-(z_pT_Bin_20) (135.0°), (Q2_y_Bin_5)-(z_pT_Bin_25) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°)
(Q2_y_Bin_5)-(z_pT_Bin_31) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_32) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_4) (195.0°)
(Q2_y_Bin_5)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_7) (225.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_1) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_10) (135.0°), (Q2_y_Bin_6)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_2) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_20) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_25) (210.0°), (Q2_y_Bin_6)-(z_pT_Bin_26) (225.0°)
(Q2_y_Bin_6)-(z_pT_Bin_27) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_28) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_6) (150.0°)
(Q2_y_Bin_6)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_8) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_9) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_15) (135.0°)
(Q2_y_Bin_7)-(z_pT_Bin_16) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_17) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_2) (180.0°)
(Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_24) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_26) (135.0°)
(Q2_y_Bin_7)-(z_pT_Bin_27) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_29) (135.0°), (Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°)
(Q2_y_Bin_7)-(z_pT_Bin_31) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°), (Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°)
(Q2_y_Bin_7)-(z_pT_Bin_34) (225.0°), (Q2_y_Bin_7)-(z_pT_Bin_35) (330.0°), (Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°)
(Q2_y_Bin_7)-(z_pT_Bin_7) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_9) (150.0°), (Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°)
(Q2_y_Bin_8)-(z_pT_Bin_12) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_16) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_18) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_19) (210.0°)
(Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_21) (165.0°), (Q2_y_Bin_8)-(z_pT_Bin_23) (135.0°)
(Q2_y_Bin_8)-(z_pT_Bin_24) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_25) (345.0°), (Q2_y_Bin_8)-(z_pT_Bin_26) (135.0°)
(Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_29) (225.0°), (Q2_y_Bin_8)-(z_pT_Bin_30) (285.0°)
(Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_9)-(z_pT_Bin_1) (210.0°), (Q2_y_Bin_9)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_9)-(z_pT_Bin_15) (135.0°), (Q2_y_Bin_9)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_9)-(z_pT_Bin_29) (180.0°)
(Q2_y_Bin_9)-(z_pT_Bin_3) (195.0°), (Q2_y_Bin_9)-(z_pT_Bin_4) (165.0°), (Q2_y_Bin_9)-(z_pT_Bin_5) (135.0°)
(Q2_y_Bin_9)-(z_pT_Bin_8) (150.0°)

Above 135° (199/452 (44.0%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_16) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°)
(Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_31) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_5) (165.0°)
(Q2_y_Bin_1)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_7) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°)
(Q2_y_Bin_1)-(z_pT_Bin_9) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_1) (150.0°), (Q2_y_Bin_10)-(z_pT_Bin_2) (165.0°)
(Q2_y_Bin_10)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_32) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_4) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_6) (195.0°), (Q2_y_Bin_10)-(z_pT_Bin_7) (150.0°)
(Q2_y_Bin_11)-(z_pT_Bin_1) (150.0°), (Q2_y_Bin_11)-(z_pT_Bin_2) (165.0°), (Q2_y_Bin_11)-(z_pT_Bin_22) (210.0°)
(Q2_y_Bin_11)-(z_pT_Bin_23) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_11)-(z_pT_Bin_3) (210.0°)
(Q2_y_Bin_11)-(z_pT_Bin_4) (300.0°), (Q2_y_Bin_11)-(z_pT_Bin_6) (150.0°), (Q2_y_Bin_12)-(z_pT_Bin_11) (195.0°)
(Q2_y_Bin_12)-(z_pT_Bin_14) (270.0°), (Q2_y_Bin_12)-(z_pT_Bin_19) (255.0°), (Q2_y_Bin_12)-(z_pT_Bin_21) (300.0°)
(Q2_y_Bin_12)-(z_pT_Bin_22) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_23) (240.0°), (Q2_y_Bin_12)-(z_pT_Bin_24) (345.0°)
(Q2_y_Bin_12)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_13)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_14)-(z_pT_Bin_32) (150.0°), (Q2_y_Bin_14)-(z_pT_Bin_5) (195.0°)
(Q2_y_Bin_15)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_2) (180.0°)
(Q2_y_Bin_15)-(z_pT_Bin_22) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_23) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_24) (240.0°)
(Q2_y_Bin_15)-(z_pT_Bin_9) (150.0°), (Q2_y_Bin_16)-(z_pT_Bin_6) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_1) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_15) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_16) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_19) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_2) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_20) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_25) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_32) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_33) (150.0°), (Q2_y_Bin_2)-(z_pT_Bin_34) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_4) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°)
(Q2_y_Bin_2)-(z_pT_Bin_8) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_12) (165.0°)
(Q2_y_Bin_3)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_14) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_15) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_17) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_18) (150.0°)
(Q2_y_Bin_3)-(z_pT_Bin_19) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_20) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_21) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_22) (150.0°), (Q2_y_Bin_3)-(z_pT_Bin_24) (255.0°)
(Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_29) (345.0°), (Q2_y_Bin_3)-(z_pT_Bin_3) (285.0°)
(Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_3)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_4)-(z_pT_Bin_15) (315.0°)
(Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_19) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_20) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (285.0°)
(Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_26) (165.0°)
(Q2_y_Bin_4)-(z_pT_Bin_27) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_28) (315.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (225.0°), (Q2_y_Bin_5)-(z_pT_Bin_10) (150.0°)
(Q2_y_Bin_5)-(z_pT_Bin_13) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_15) (150.0°)
(Q2_y_Bin_5)-(z_pT_Bin_19) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (255.0°), (Q2_y_Bin_5)-(z_pT_Bin_25) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_31) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_32) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_6) (165.0°)
(Q2_y_Bin_5)-(z_pT_Bin_7) (225.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_9) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_2) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_20) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_25) (210.0°), (Q2_y_Bin_6)-(z_pT_Bin_26) (225.0°)
(Q2_y_Bin_6)-(z_pT_Bin_27) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_28) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_6) (150.0°)
(Q2_y_Bin_6)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_8) (150.0°), (Q2_y_Bin_6)-(z_pT_Bin_9) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_2) (180.0°)
(Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_24) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_27) (150.0°)
(Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_31) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°)
(Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_34) (225.0°), (Q2_y_Bin_7)-(z_pT_Bin_35) (330.0°)
(Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_7)-(z_pT_Bin_7) (150.0°), (Q2_y_Bin_7)-(z_pT_Bin_9) (150.0°)
(Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_16) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_19) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_21) (165.0°), (Q2_y_Bin_8)-(z_pT_Bin_24) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_25) (345.0°)
(Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°), (Q2_y_Bin_8)-(z_pT_Bin_29) (225.0°), (Q2_y_Bin_8)-(z_pT_Bin_30) (285.0°)
(Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_9)-(z_pT_Bin_1) (210.0°), (Q2_y_Bin_9)-(z_pT_Bin_2) (195.0°)
(Q2_y_Bin_9)-(z_pT_Bin_29) (180.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (195.0°), (Q2_y_Bin_9)-(z_pT_Bin_4) (165.0°)
(Q2_y_Bin_9)-(z_pT_Bin_8) (150.0°)

Above 150° (170/452 (37.6%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_10) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_16) (180.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_22) (180.0°)
(Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_6) (165.0°)
(Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (210.0°), (Q2_y_Bin_10)-(z_pT_Bin_2) (165.0°)
(Q2_y_Bin_10)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_32) (180.0°), (Q2_y_Bin_10)-(z_pT_Bin_4) (180.0°)
(Q2_y_Bin_10)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_10)-(z_pT_Bin_6) (195.0°), (Q2_y_Bin_11)-(z_pT_Bin_2) (165.0°)
(Q2_y_Bin_11)-(z_pT_Bin_22) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_23) (225.0°), (Q2_y_Bin_11)-(z_pT_Bin_24) (255.0°)
(Q2_y_Bin_11)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_4) (300.0°), (Q2_y_Bin_12)-(z_pT_Bin_11) (195.0°)
(Q2_y_Bin_12)-(z_pT_Bin_14) (270.0°), (Q2_y_Bin_12)-(z_pT_Bin_19) (255.0°), (Q2_y_Bin_12)-(z_pT_Bin_21) (300.0°)
(Q2_y_Bin_12)-(z_pT_Bin_22) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_23) (240.0°), (Q2_y_Bin_12)-(z_pT_Bin_24) (345.0°)
(Q2_y_Bin_12)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_13)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_14)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_1) (165.0°)
(Q2_y_Bin_15)-(z_pT_Bin_15) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_22) (180.0°)
(Q2_y_Bin_15)-(z_pT_Bin_23) (180.0°), (Q2_y_Bin_15)-(z_pT_Bin_24) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_1) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_10) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_14) (180.0°)
(Q2_y_Bin_2)-(z_pT_Bin_15) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_19) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_2) (225.0°)
(Q2_y_Bin_2)-(z_pT_Bin_20) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_25) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (195.0°)
(Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_32) (180.0°), (Q2_y_Bin_2)-(z_pT_Bin_34) (165.0°)
(Q2_y_Bin_2)-(z_pT_Bin_4) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°), (Q2_y_Bin_2)-(z_pT_Bin_8) (165.0°), (Q2_y_Bin_2)-(z_pT_Bin_9) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°), (Q2_y_Bin_3)-(z_pT_Bin_11) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_12) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_15) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_16) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_20) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_21) (165.0°), (Q2_y_Bin_3)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_29) (345.0°), (Q2_y_Bin_3)-(z_pT_Bin_3) (285.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_8) (180.0°)
(Q2_y_Bin_3)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_4)-(z_pT_Bin_15) (315.0°), (Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_19) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_22) (285.0°), (Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°)
(Q2_y_Bin_4)-(z_pT_Bin_26) (165.0°), (Q2_y_Bin_4)-(z_pT_Bin_27) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_28) (315.0°)
(Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (225.0°)
(Q2_y_Bin_5)-(z_pT_Bin_13) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_14) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (255.0°)
(Q2_y_Bin_5)-(z_pT_Bin_25) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_31) (210.0°)
(Q2_y_Bin_5)-(z_pT_Bin_32) (180.0°), (Q2_y_Bin_5)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_5) (195.0°)
(Q2_y_Bin_5)-(z_pT_Bin_6) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_7) (225.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (180.0°)
(Q2_y_Bin_5)-(z_pT_Bin_9) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_14) (165.0°)
(Q2_y_Bin_6)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_25) (210.0°), (Q2_y_Bin_6)-(z_pT_Bin_26) (225.0°)
(Q2_y_Bin_6)-(z_pT_Bin_27) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_3) (180.0°), (Q2_y_Bin_6)-(z_pT_Bin_4) (180.0°)
(Q2_y_Bin_6)-(z_pT_Bin_5) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_7) (165.0°), (Q2_y_Bin_6)-(z_pT_Bin_9) (165.0°)
(Q2_y_Bin_7)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_11) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°)
(Q2_y_Bin_7)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_7)-(z_pT_Bin_2) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_21) (180.0°)
(Q2_y_Bin_7)-(z_pT_Bin_24) (180.0°), (Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_31) (270.0°)
(Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°), (Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_34) (225.0°)
(Q2_y_Bin_7)-(z_pT_Bin_35) (330.0°), (Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°)
(Q2_y_Bin_8)-(z_pT_Bin_13) (165.0°), (Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_16) (195.0°)
(Q2_y_Bin_8)-(z_pT_Bin_19) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_21) (165.0°)
(Q2_y_Bin_8)-(z_pT_Bin_24) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_25) (345.0°), (Q2_y_Bin_8)-(z_pT_Bin_28) (180.0°)
(Q2_y_Bin_8)-(z_pT_Bin_29) (225.0°), (Q2_y_Bin_8)-(z_pT_Bin_30) (285.0°), (Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_9)-(z_pT_Bin_1) (210.0°), (Q2_y_Bin_9)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_9)-(z_pT_Bin_29) (180.0°)
(Q2_y_Bin_9)-(z_pT_Bin_3) (195.0°), (Q2_y_Bin_9)-(z_pT_Bin_4) (165.0°)

Above 180° (108/452 (23.9%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (255.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (240.0°)
(Q2_y_Bin_1)-(z_pT_Bin_29) (240.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (225.0°), (Q2_y_Bin_1)-(z_pT_Bin_30) (195.0°)
(Q2_y_Bin_1)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (210.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (210.0°)
(Q2_y_Bin_10)-(z_pT_Bin_6) (195.0°), (Q2_y_Bin_11)-(z_pT_Bin_22) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_23) (225.0°)
(Q2_y_Bin_11)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_11)-(z_pT_Bin_3) (210.0°), (Q2_y_Bin_11)-(z_pT_Bin_4) (300.0°)
(Q2_y_Bin_12)-(z_pT_Bin_11) (195.0°), (Q2_y_Bin_12)-(z_pT_Bin_14) (270.0°), (Q2_y_Bin_12)-(z_pT_Bin_19) (255.0°)
(Q2_y_Bin_12)-(z_pT_Bin_21) (300.0°), (Q2_y_Bin_12)-(z_pT_Bin_22) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_23) (240.0°)
(Q2_y_Bin_12)-(z_pT_Bin_24) (345.0°), (Q2_y_Bin_12)-(z_pT_Bin_6) (210.0°), (Q2_y_Bin_12)-(z_pT_Bin_7) (210.0°)
(Q2_y_Bin_12)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_14)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_15)-(z_pT_Bin_15) (195.0°)
(Q2_y_Bin_15)-(z_pT_Bin_24) (240.0°), (Q2_y_Bin_2)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_2) (225.0°)
(Q2_y_Bin_2)-(z_pT_Bin_20) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_31) (240.0°)
(Q2_y_Bin_2)-(z_pT_Bin_4) (210.0°), (Q2_y_Bin_2)-(z_pT_Bin_5) (195.0°), (Q2_y_Bin_2)-(z_pT_Bin_6) (210.0°)
(Q2_y_Bin_2)-(z_pT_Bin_7) (225.0°), (Q2_y_Bin_3)-(z_pT_Bin_1) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_10) (210.0°)
(Q2_y_Bin_3)-(z_pT_Bin_13) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_3)-(z_pT_Bin_20) (195.0°)
(Q2_y_Bin_3)-(z_pT_Bin_24) (255.0°), (Q2_y_Bin_3)-(z_pT_Bin_25) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_26) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_27) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_28) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_29) (345.0°)
(Q2_y_Bin_3)-(z_pT_Bin_3) (285.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_3)-(z_pT_Bin_5) (360.0°)
(Q2_y_Bin_3)-(z_pT_Bin_7) (195.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_13) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_15) (315.0°), (Q2_y_Bin_4)-(z_pT_Bin_16) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_17) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_19) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_21) (210.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (285.0°)
(Q2_y_Bin_4)-(z_pT_Bin_23) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_25) (240.0°), (Q2_y_Bin_4)-(z_pT_Bin_27) (210.0°)
(Q2_y_Bin_4)-(z_pT_Bin_28) (315.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_4)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_8) (360.0°), (Q2_y_Bin_4)-(z_pT_Bin_9) (360.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (225.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (255.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (210.0°)
(Q2_y_Bin_5)-(z_pT_Bin_31) (210.0°), (Q2_y_Bin_5)-(z_pT_Bin_4) (195.0°), (Q2_y_Bin_5)-(z_pT_Bin_5) (195.0°)
(Q2_y_Bin_5)-(z_pT_Bin_7) (225.0°), (Q2_y_Bin_6)-(z_pT_Bin_25) (210.0°), (Q2_y_Bin_6)-(z_pT_Bin_26) (225.0°)
(Q2_y_Bin_7)-(z_pT_Bin_12) (210.0°), (Q2_y_Bin_7)-(z_pT_Bin_3) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_31) (270.0°)
(Q2_y_Bin_7)-(z_pT_Bin_32) (240.0°), (Q2_y_Bin_7)-(z_pT_Bin_33) (270.0°), (Q2_y_Bin_7)-(z_pT_Bin_34) (225.0°)
(Q2_y_Bin_7)-(z_pT_Bin_35) (330.0°), (Q2_y_Bin_7)-(z_pT_Bin_4) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_11) (195.0°)
(Q2_y_Bin_8)-(z_pT_Bin_14) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_16) (195.0°), (Q2_y_Bin_8)-(z_pT_Bin_19) (210.0°)
(Q2_y_Bin_8)-(z_pT_Bin_20) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_24) (210.0°), (Q2_y_Bin_8)-(z_pT_Bin_25) (345.0°)
(Q2_y_Bin_8)-(z_pT_Bin_29) (225.0°), (Q2_y_Bin_8)-(z_pT_Bin_30) (285.0°), (Q2_y_Bin_8)-(z_pT_Bin_31) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_32) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_33) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_34) (360.0°)
(Q2_y_Bin_8)-(z_pT_Bin_6) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_7) (360.0°), (Q2_y_Bin_8)-(z_pT_Bin_8) (360.0°)
(Q2_y_Bin_9)-(z_pT_Bin_1) (210.0°), (Q2_y_Bin_9)-(z_pT_Bin_2) (195.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (195.0°)

## Source `chi2_pid` — largest table share 26.47% (A0)

### chi2_pid / Stricter bound

Stage: spline, acceptance. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/chi2_strict_pip/chi2_strict_pip/fit_copy.root`

Above 90° (32/452 (7.1%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_2)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°)
(Q2_y_Bin_3)-(z_pT_Bin_5) (105.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_16) (120.0°)
(Q2_y_Bin_4)-(z_pT_Bin_17) (165.0°), (Q2_y_Bin_4)-(z_pT_Bin_22) (105.0°), (Q2_y_Bin_4)-(z_pT_Bin_23) (120.0°)
(Q2_y_Bin_4)-(z_pT_Bin_27) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_31) (120.0°)
(Q2_y_Bin_4)-(z_pT_Bin_32) (165.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (180.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (195.0°)
(Q2_y_Bin_4)-(z_pT_Bin_7) (135.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (105.0°)
(Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_5)-(z_pT_Bin_7) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°)
(Q2_y_Bin_8)-(z_pT_Bin_30) (120.0°), (Q2_y_Bin_8)-(z_pT_Bin_33) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_34) (105.0°)
(Q2_y_Bin_8)-(z_pT_Bin_6) (120.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (11/452 (2.4%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (150.0°)
(Q2_y_Bin_4)-(z_pT_Bin_17) (165.0°), (Q2_y_Bin_4)-(z_pT_Bin_27) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_29) (150.0°)
(Q2_y_Bin_4)-(z_pT_Bin_32) (165.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (180.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (195.0°)
(Q2_y_Bin_4)-(z_pT_Bin_7) (135.0°), (Q2_y_Bin_8)-(z_pT_Bin_33) (135.0°)

Above 135° (7/452 (1.5%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_17) (165.0°)
(Q2_y_Bin_4)-(z_pT_Bin_29) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_32) (165.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (180.0°)
(Q2_y_Bin_4)-(z_pT_Bin_34) (195.0°)

Above 150° (4/452 (0.9%)):

(Q2_y_Bin_4)-(z_pT_Bin_17) (165.0°), (Q2_y_Bin_4)-(z_pT_Bin_32) (165.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (180.0°)
(Q2_y_Bin_4)-(z_pT_Bin_34) (195.0°)

Above 180° (1/452 (0.2%)):

(Q2_y_Bin_4)-(z_pT_Bin_34) (195.0°)

## Source `physics_injection` — largest table share 15.75% (A0)

### physics_injection / Zeroth-order unweighted

Stage: unweighted, bin centering. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/unweighted/nominal/bc/corrected.root`

Above 90° (16/452 (3.5%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (105.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°)
(Q2_y_Bin_5)-(z_pT_Bin_2) (120.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°)
(Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)

Above 135° (1/452 (0.2%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (150.0°)

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

## Source `acceptance_method` — largest table share 15.72% (A0)

### acceptance_method / Bin-by-bin

Stage: spline, bin-by-bin. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/correction_method/BinByBin/fit_copy.root`

Above 90° (17/452 (3.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)

Above 135° (0/452 (0.0%)):

None.

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

### acceptance_method / Unweighted 5D

Stage: unweighted, 5D acceptance. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/unweighted/dimension/5D/fit_copy.root`

Above 90° (16/452 (3.5%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (105.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°)
(Q2_y_Bin_5)-(z_pT_Bin_2) (120.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°)
(Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)

Above 135° (1/452 (0.2%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (150.0°)

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

## Source `pion_dc_extra` — largest table share 11.69% (cos 2phi_h)

### pion_dc_extra / Boundaries removed

Stage: spline, acceptance. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/no_pip_testdc/no_pip_testdc/fit_copy.root`

Above 90° (8/452 (1.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (120.0°)
(Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (105.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (105.0°)
(Q2_y_Bin_5)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°)

Above 120° (0/452 (0.0%)):

None.

Above 135° (0/452 (0.0%)):

None.

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

## Source `pcal_volume` — largest table share 5.33% (A0)

### pcal_volume / Loose

Stage: spline, acceptance. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/pcalvol/loose/fit_copy.root`

Above 90° (17/452 (3.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)

Above 135° (0/452 (0.0%)):

None.

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

### pcal_volume / Tight

Stage: spline, acceptance. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/pcalvol/tight/fit_copy.root`

Above 90° (22/452 (4.9%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_2)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_2)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_5) (105.0°)
(Q2_y_Bin_4)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_32) (105.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (120.0°)
(Q2_y_Bin_4)-(z_pT_Bin_34) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°)
(Q2_y_Bin_5)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°)
(Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (4/452 (0.9%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (150.0°)
(Q2_y_Bin_4)-(z_pT_Bin_34) (150.0°)

Above 135° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (150.0°)

Above 150° (1/452 (0.2%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (165.0°)

Above 180° (0/452 (0.0%)):

None.

## Source `spline_bc` — largest table share 4.05% (A0)

### spline_bc / Initial injection spline

Stage: spline, bin centering. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/spline_bc/bcs_spline/histograms.root`

Above 90° (17/452 (3.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)

Above 135° (0/452 (0.0%)):

None.

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

## Source `bc_sampling` — largest table share 3.58% (A0)

### bc_sampling / sub\_phi\_5

Stage: spline, bin centering. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/bc_sampling/sub_phi_5/fit_copy.root`

Above 90° (17/452 (3.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)

Above 135° (0/452 (0.0%)):

None.

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

### bc_sampling / sub\_phi\_7

Stage: spline, bin centering. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/bc_sampling/sub_phi_7/fit_copy.root`

Above 90° (17/452 (3.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)

Above 135° (0/452 (0.0%)):

None.

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

### bc_sampling / sub\_phi\_9

Stage: spline, bin centering. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/bc_sampling/sub_phi_9/fit_copy.root`

Above 90° (17/452 (3.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)

Above 135° (0/452 (0.0%)):

None.

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

### bc_sampling / sub\_pt\_3

Stage: spline, bin centering. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/bc_sampling/sub_pt_3/fit_copy.root`

Above 90° (17/452 (3.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)

Above 135° (0/452 (0.0%)):

None.

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

### bc_sampling / sub\_pt\_5

Stage: spline, bin centering. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/bc_sampling/sub_pt_5/fit_copy.root`

Above 90° (17/452 (3.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)

Above 135° (0/452 (0.0%)):

None.

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

### bc_sampling / sub\_pt\_7

Stage: spline, bin centering. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/bc_sampling/sub_pt_7/fit_copy.root`

Above 90° (17/452 (3.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)

Above 135° (0/452 (0.0%)):

None.

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

### bc_sampling / sub\_q2\_3

Stage: spline, bin centering. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/bc_sampling/sub_q2_3/fit_copy.root`

Above 90° (17/452 (3.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)

Above 135° (0/452 (0.0%)):

None.

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

### bc_sampling / sub\_q2\_5

Stage: spline, bin centering. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/bc_sampling/sub_q2_5/fit_copy.root`

Above 90° (17/452 (3.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)

Above 135° (0/452 (0.0%)):

None.

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

### bc_sampling / sub\_q2\_7

Stage: spline, bin centering. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/bc_sampling/sub_q2_7/fit_copy.root`

Above 90° (17/452 (3.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)

Above 135° (0/452 (0.0%)):

None.

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

### bc_sampling / sub\_y\_3

Stage: spline, bin centering. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/bc_sampling/sub_y_3/fit_copy.root`

Above 90° (17/452 (3.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)

Above 135° (0/452 (0.0%)):

None.

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

### bc_sampling / sub\_y\_5

Stage: spline, bin centering. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/bc_sampling/sub_y_5/fit_copy.root`

Above 90° (17/452 (3.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)

Above 135° (0/452 (0.0%)):

None.

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

### bc_sampling / sub\_y\_7

Stage: spline, bin centering. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/bc_sampling/sub_y_7/fit_copy.root`

Above 90° (17/452 (3.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)

Above 135° (0/452 (0.0%)):

None.

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

### bc_sampling / sub\_z\_3

Stage: spline, bin centering. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/bc_sampling/sub_z_3/fit_copy.root`

Above 90° (17/452 (3.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)

Above 135° (0/452 (0.0%)):

None.

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

### bc_sampling / sub\_z\_5

Stage: spline, bin centering. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/bc_sampling/sub_z_5/fit_copy.root`

Above 90° (17/452 (3.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)

Above 135° (0/452 (0.0%)):

None.

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

### bc_sampling / sub\_z\_7

Stage: spline, bin centering. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/bc_sampling/sub_z_7/fit_copy.root`

Above 90° (17/452 (3.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)

Above 135° (0/452 (0.0%)):

None.

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

## Source `rc_model` — largest table share 2.15% (cos 2phi_h)

### rc_model / Initial-model bin center

Stage: spline, radiative correction. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/rc_model/rc_sf0/histograms.root`

Above 90° (17/452 (3.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)

Above 135° (0/452 (0.0%)):

None.

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

### rc_model / First-iteration bin center

Stage: spline, radiative correction. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/rc_model/rc_sf2/histograms.root`

Above 90° (17/452 (3.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)

Above 135° (0/452 (0.0%)):

None.

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

## Source `exclusive_rho0` — largest table share 2.14% (A0)

### exclusive_rho0 / Subtraction omitted

Stage: spline, acceptance. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/rho0_subtraction/NoRho0/fit_copy.root`

Above 90° (17/452 (3.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)

Above 135° (0/452 (0.0%)):

None.

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

## Source `phi_binning` — largest table share 1.53% (cos 2phi_h)

### phi_binning / 12 bins

Stage: spline, acceptance. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/phi_bins/Phi12/fit_copy.root`

Above 90° (19/452 (4.2%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (120.0°)
(Q2_y_Bin_1)-(z_pT_Bin_22) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°)
(Q2_y_Bin_2)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (120.0°)
(Q2_y_Bin_4)-(z_pT_Bin_34) (120.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (120.0°), (Q2_y_Bin_5)-(z_pT_Bin_14) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_2) (120.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_5)-(z_pT_Bin_4) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_5) (120.0°), (Q2_y_Bin_5)-(z_pT_Bin_7) (120.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_9) (120.0°)

Above 120° (2/452 (0.4%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (150.0°)

Above 135° (2/452 (0.4%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_3) (150.0°)

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

## Source `sector_pcal` — largest table share 0.80% (A0)

### sector_pcal / Vetoes removed

Stage: spline, acceptance. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/no_sector_pcal/no_sector_pcal/fit_copy.root`

Above 90° (17/452 (3.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)

Above 135° (0/452 (0.0%)):

None.

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

## Source `electron_dc_refinement` — largest table share 0.48% (cos 2phi_h)

### electron_dc_refinement / Loose

Stage: spline, acceptance. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/dcfidref_el/loose/fit_copy.root`

Above 90° (16/452 (3.5%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (105.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (105.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°)
(Q2_y_Bin_5)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°)
(Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (2/452 (0.4%)):

(Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)

Above 135° (0/452 (0.0%)):

None.

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

### electron_dc_refinement / Tight

Stage: spline, acceptance. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/dcfidref_el/tight/fit_copy.root`

Above 90° (19/452 (4.2%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°)
(Q2_y_Bin_3)-(z_pT_Bin_5) (105.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (120.0°)
(Q2_y_Bin_4)-(z_pT_Bin_34) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°)
(Q2_y_Bin_5)-(z_pT_Bin_2) (120.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°)
(Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (4/452 (0.9%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (150.0°)
(Q2_y_Bin_4)-(z_pT_Bin_34) (150.0°)

Above 135° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (150.0°)

Above 150° (1/452 (0.2%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (165.0°)

Above 180° (0/452 (0.0%)):

None.

## Source `acceptance_threshold` — largest table share 0.42% (cos 2phi_h)

### acceptance_threshold / 0.015

Stage: spline, acceptance. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/acceptance_threshold/Acc015/fit_copy.root`

Above 90° (13/452 (2.9%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (105.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (105.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°)

Above 120° (1/452 (0.2%)):

(Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)

Above 135° (0/452 (0.0%)):

None.

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

### acceptance_threshold / 0.025

Stage: spline, acceptance. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/acceptance_threshold/Acc025/fit_copy.root`

Above 90° (26/452 (5.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_2)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_2)-(z_pT_Bin_4) (105.0°), (Q2_y_Bin_2)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°)
(Q2_y_Bin_3)-(z_pT_Bin_5) (105.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_17) (105.0°)
(Q2_y_Bin_4)-(z_pT_Bin_32) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (150.0°)
(Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_5)-(z_pT_Bin_5) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_7) (105.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (5/452 (1.1%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (150.0°)
(Q2_y_Bin_4)-(z_pT_Bin_34) (150.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (165.0°)

Above 135° (4/452 (0.9%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (150.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (150.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (165.0°)

Above 150° (2/452 (0.4%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (165.0°)

Above 180° (0/452 (0.0%)):

None.

## Source `pion_dc_edges` — largest table share 0.37% (cos 2phi_h)

### pion_dc_edges / Loose

Stage: spline, acceptance. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/dcfid_pip/loose/fit_copy.root`

Above 90° (17/452 (3.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (2/452 (0.4%)):

(Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)

Above 135° (0/452 (0.0%)):

None.

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

### pion_dc_edges / Tight

Stage: spline, acceptance. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/dcfid_pip/tight/fit_copy.root`

Above 90° (19/452 (4.2%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_2)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°)
(Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (120.0°)
(Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°), (Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_5)-(z_pT_Bin_7) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°)
(Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (165.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)

Above 135° (1/452 (0.2%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (165.0°)

Above 150° (1/452 (0.2%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (165.0°)

Above 180° (0/452 (0.0%)):

None.

## Source `electron_vz` — largest table share 0.35% (A0)

### electron_vz / Loose

Stage: spline, acceptance. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/dcv_el/loose/fit_copy.root`

Above 90° (17/452 (3.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)

Above 135° (0/452 (0.0%)):

None.

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

### electron_vz / Tight

Stage: spline, acceptance. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/dcv_el/tight/fit_copy.root`

Above 90° (17/452 (3.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (150.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)

Above 135° (1/452 (0.2%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (150.0°)

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

## Source `momentum_smearing` — largest table share 0.33% (cos 2phi_h)

### momentum_smearing / Smearing removed

Stage: spline, acceptance. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/noSmear/noSmear/fit_copy.root`

Above 90° (17/452 (3.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)

Above 135° (0/452 (0.0%)):

None.

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

## Source `pcal_dead` — largest table share 0.25% (A0)

### pcal_dead / Strips removed

Stage: spline, acceptance. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/no_valerii_knockout/no_valerii_knockout/fit_copy.root`

Above 90° (17/452 (3.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)

Above 135° (0/452 (0.0%)):

None.

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

## Source `bayes_iterations` — largest table share 0.24% (cos 2phi_h)

### bayes_iterations / $k-1$

Stage: spline, acceptance. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/bayes_iteration/BayesMinus1/fit_copy.root`

Above 90° (17/452 (3.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)

Above 135° (0/452 (0.0%)):

None.

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

### bayes_iterations / $k+1$

Stage: spline, acceptance. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/bayes_iteration/BayesPlus1/fit_copy.root`

Above 90° (17/452 (3.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)

Above 135° (0/452 (0.0%)):

None.

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

## Source `pcal_ep` — largest table share 0.24% (cos 2phi_h)

### pcal_ep / Loose

Stage: spline, acceptance. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/ecthr_el/loose/fit_copy.root`

Above 90° (17/452 (3.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)

Above 135° (0/452 (0.0%)):

None.

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

### pcal_ep / Tight

Stage: spline, acceptance. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/ecthr_el/tight/fit_copy.root`

Above 90° (17/452 (3.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)

Above 135° (0/452 (0.0%)):

None.

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

## Source `sampling_fraction` — largest table share 0.22% (cos 2phi_h)

### sampling_fraction / Loose

Stage: spline, acceptance. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/ecband_el/loose/fit_copy.root`

Above 90° (17/452 (3.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)

Above 135° (0/452 (0.0%)):

None.

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

### sampling_fraction / Tight

Stage: spline, acceptance. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/ecband_el/tight/fit_copy.root`

Above 90° (17/452 (3.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)

Above 135° (0/452 (0.0%)):

None.

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

## Source `vertex_separation` — largest table share 0.22% (cos 2phi_h)

### vertex_separation / Loose

Stage: spline, acceptance. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/dvz_pip/loose/fit_copy.root`

Above 90° (17/452 (3.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)

Above 135° (0/452 (0.0%)):

None.

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

### vertex_separation / Tight

Stage: spline, acceptance. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/dvz_pip/tight/fit_copy.root`

Above 90° (17/452 (3.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)

Above 135° (0/452 (0.0%)):

None.

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

## Source `electron_dc_edges` — largest table share 0.22% (cos 2phi_h)

### electron_dc_edges / Loose

Stage: spline, acceptance. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/dcfid_el/loose/fit_copy.root`

Above 90° (17/452 (3.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)

Above 135° (0/452 (0.0%)):

None.

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

### electron_dc_edges / Tight

Stage: spline, acceptance. File: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Systematic_Studies/physics_campaign/refinement_20261108/spline/dcfid_el/tight/fit_copy.root`

Above 90° (17/452 (3.8%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_15) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°)
(Q2_y_Bin_1)-(z_pT_Bin_3) (105.0°), (Q2_y_Bin_1)-(z_pT_Bin_8) (120.0°), (Q2_y_Bin_1)-(z_pT_Bin_9) (105.0°)
(Q2_y_Bin_2)-(z_pT_Bin_3) (120.0°), (Q2_y_Bin_3)-(z_pT_Bin_4) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)
(Q2_y_Bin_4)-(z_pT_Bin_33) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_34) (120.0°), (Q2_y_Bin_4)-(z_pT_Bin_7) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_1) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_2) (105.0°), (Q2_y_Bin_5)-(z_pT_Bin_3) (120.0°)
(Q2_y_Bin_5)-(z_pT_Bin_8) (105.0°), (Q2_y_Bin_9)-(z_pT_Bin_3) (105.0°)

Above 120° (3/452 (0.7%)):

(Q2_y_Bin_1)-(z_pT_Bin_1) (135.0°), (Q2_y_Bin_1)-(z_pT_Bin_2) (135.0°), (Q2_y_Bin_4)-(z_pT_Bin_10) (135.0°)

Above 135° (0/452 (0.0%)):

None.

Above 150° (0/452 (0.0%)):

None.

Above 180° (0/452 (0.0%)):

None.

## Sector exclusions

Electron labels E1–E6 are `eS1o`–`eS6o`. Pion labels P1–P6 are `pipS1o`–`pipS6o`. The four counts use assessed histograms only. Fit-quality omissions use the stored acceptance fit: NDF below 1, a non-finite coefficient, `|B|>10`, `|C|>10`, or `|A|<1`. They are not manual exclusions. A bracketed note marks a disagreement that is also a fit-quality omission.

| Sector | Threshold | Excluded and fails | Excluded and passes | Not excluded and fails | Not excluded and passes |
| --- | --- | --- | --- | --- | --- |
| eS1o | 90° | 30 | 0 | 273 | 149 |
| eS1o | 120° | 30 | 0 | 216 | 206 |
| eS1o | 135° | 30 | 0 | 193 | 229 |
| eS1o | 150° | 30 | 0 | 162 | 260 |
| eS1o | 180° | 30 | 0 | 94 | 328 |
| eS2o | 90° | 31 | 0 | 255 | 166 |
| eS2o | 120° | 31 | 0 | 204 | 217 |
| eS2o | 135° | 31 | 0 | 178 | 243 |
| eS2o | 150° | 30 | 1 | 141 | 280 |
| eS2o | 180° | 28 | 3 | 85 | 336 |
| eS3o | 90° | 40 | 0 | 238 | 174 |
| eS3o | 120° | 40 | 0 | 178 | 234 |
| eS3o | 135° | 40 | 0 | 149 | 263 |
| eS3o | 150° | 40 | 0 | 121 | 291 |
| eS3o | 180° | 36 | 4 | 70 | 342 |
| eS4o | 90° | 49 | 0 | 234 | 169 |
| eS4o | 120° | 49 | 0 | 176 | 227 |
| eS4o | 135° | 48 | 1 | 149 | 254 |
| eS4o | 150° | 46 | 3 | 121 | 282 |
| eS4o | 180° | 43 | 6 | 67 | 336 |
| eS5o | 90° | 46 | 0 | 244 | 162 |
| eS5o | 120° | 46 | 0 | 189 | 217 |
| eS5o | 135° | 46 | 0 | 169 | 237 |
| eS5o | 150° | 46 | 0 | 136 | 270 |
| eS5o | 180° | 40 | 6 | 82 | 324 |
| eS6o | 90° | 59 | 0 | 233 | 160 |
| eS6o | 120° | 59 | 0 | 181 | 212 |
| eS6o | 135° | 59 | 0 | 157 | 236 |
| eS6o | 150° | 57 | 2 | 124 | 269 |
| eS6o | 180° | 47 | 12 | 67 | 326 |
| pipS1o | 90° | 28 | 0 | 243 | 181 |
| pipS1o | 120° | 28 | 0 | 182 | 242 |
| pipS1o | 135° | 28 | 0 | 157 | 267 |
| pipS1o | 150° | 28 | 0 | 130 | 294 |
| pipS1o | 180° | 28 | 0 | 71 | 353 |
| pipS2o | 90° | 29 | 0 | 269 | 154 |
| pipS2o | 120° | 29 | 0 | 209 | 214 |
| pipS2o | 135° | 29 | 0 | 187 | 236 |
| pipS2o | 150° | 29 | 0 | 153 | 270 |
| pipS2o | 180° | 29 | 0 | 96 | 327 |
| pipS3o | 90° | 40 | 0 | 265 | 147 |
| pipS3o | 120° | 40 | 0 | 210 | 202 |
| pipS3o | 135° | 40 | 0 | 189 | 223 |
| pipS3o | 150° | 40 | 0 | 155 | 257 |
| pipS3o | 180° | 36 | 4 | 87 | 325 |
| pipS4o | 90° | 48 | 0 | 237 | 167 |
| pipS4o | 120° | 48 | 0 | 185 | 219 |
| pipS4o | 135° | 47 | 1 | 164 | 240 |
| pipS4o | 150° | 45 | 3 | 134 | 270 |
| pipS4o | 180° | 41 | 7 | 78 | 326 |
| pipS5o | 90° | 40 | 0 | 249 | 163 |
| pipS5o | 120° | 40 | 0 | 192 | 220 |
| pipS5o | 135° | 39 | 1 | 170 | 242 |
| pipS5o | 150° | 37 | 3 | 132 | 280 |
| pipS5o | 180° | 35 | 5 | 79 | 333 |
| pipS6o | 90° | 52 | 0 | 227 | 173 |
| pipS6o | 120° | 52 | 0 | 174 | 226 |
| pipS6o | 135° | 52 | 0 | 147 | 253 |
| pipS6o | 150° | 51 | 1 | 119 | 281 |
| pipS6o | 180° | 40 | 12 | 68 | 332 |

### eS1o

Manual list entries: 31. Fit-quality omissions relative to the nominal acceptance bins: 44. Comparisons the budget still keeps: 387.

Manual entries outside the retained population:

(Q2_y_Bin_8)-(z_pT_Bin_35)

#### 90°

The rule fails every assessable manual exclusion (30).

Manually excluded but passes:

None.

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_11), (Q2_y_Bin_1)-(z_pT_Bin_15)
(Q2_y_Bin_1)-(z_pT_Bin_16), (Q2_y_Bin_1)-(z_pT_Bin_17), (Q2_y_Bin_1)-(z_pT_Bin_2)
(Q2_y_Bin_1)-(z_pT_Bin_22), (Q2_y_Bin_1)-(z_pT_Bin_23), (Q2_y_Bin_1)-(z_pT_Bin_3)
(Q2_y_Bin_1)-(z_pT_Bin_30), (Q2_y_Bin_1)-(z_pT_Bin_31), (Q2_y_Bin_1)-(z_pT_Bin_32)
(Q2_y_Bin_1)-(z_pT_Bin_5), (Q2_y_Bin_1)-(z_pT_Bin_6), (Q2_y_Bin_1)-(z_pT_Bin_7)
(Q2_y_Bin_1)-(z_pT_Bin_8), (Q2_y_Bin_1)-(z_pT_Bin_9), (Q2_y_Bin_10)-(z_pT_Bin_1)
(Q2_y_Bin_10)-(z_pT_Bin_10), (Q2_y_Bin_10)-(z_pT_Bin_11), (Q2_y_Bin_10)-(z_pT_Bin_12)
(Q2_y_Bin_10)-(z_pT_Bin_13), (Q2_y_Bin_10)-(z_pT_Bin_15), (Q2_y_Bin_10)-(z_pT_Bin_16)
(Q2_y_Bin_10)-(z_pT_Bin_2), (Q2_y_Bin_10)-(z_pT_Bin_20), (Q2_y_Bin_10)-(z_pT_Bin_21)
(Q2_y_Bin_10)-(z_pT_Bin_26), (Q2_y_Bin_10)-(z_pT_Bin_3), (Q2_y_Bin_10)-(z_pT_Bin_31)
(Q2_y_Bin_10)-(z_pT_Bin_32), (Q2_y_Bin_10)-(z_pT_Bin_33), (Q2_y_Bin_10)-(z_pT_Bin_4)
(Q2_y_Bin_10)-(z_pT_Bin_5), (Q2_y_Bin_10)-(z_pT_Bin_6), (Q2_y_Bin_10)-(z_pT_Bin_7)
(Q2_y_Bin_10)-(z_pT_Bin_9), (Q2_y_Bin_11)-(z_pT_Bin_1), (Q2_y_Bin_11)-(z_pT_Bin_10)
(Q2_y_Bin_11)-(z_pT_Bin_11), (Q2_y_Bin_11)-(z_pT_Bin_13), (Q2_y_Bin_11)-(z_pT_Bin_14)
(Q2_y_Bin_11)-(z_pT_Bin_15), (Q2_y_Bin_11)-(z_pT_Bin_18), (Q2_y_Bin_11)-(z_pT_Bin_19)
(Q2_y_Bin_11)-(z_pT_Bin_2), (Q2_y_Bin_11)-(z_pT_Bin_20), (Q2_y_Bin_11)-(z_pT_Bin_3)
(Q2_y_Bin_11)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_11)-(z_pT_Bin_6), (Q2_y_Bin_11)-(z_pT_Bin_8)
(Q2_y_Bin_11)-(z_pT_Bin_9), (Q2_y_Bin_12)-(z_pT_Bin_11), (Q2_y_Bin_12)-(z_pT_Bin_12)
(Q2_y_Bin_12)-(z_pT_Bin_13), (Q2_y_Bin_12)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_16)
(Q2_y_Bin_12)-(z_pT_Bin_18), (Q2_y_Bin_12)-(z_pT_Bin_21) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission]
(Q2_y_Bin_12)-(z_pT_Bin_6), (Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_13)-(z_pT_Bin_1)
(Q2_y_Bin_13)-(z_pT_Bin_12), (Q2_y_Bin_13)-(z_pT_Bin_17), (Q2_y_Bin_13)-(z_pT_Bin_2)
(Q2_y_Bin_13)-(z_pT_Bin_26), (Q2_y_Bin_13)-(z_pT_Bin_3), (Q2_y_Bin_13)-(z_pT_Bin_4)
(Q2_y_Bin_13)-(z_pT_Bin_5), (Q2_y_Bin_13)-(z_pT_Bin_7), (Q2_y_Bin_13)-(z_pT_Bin_8)
(Q2_y_Bin_13)-(z_pT_Bin_9), (Q2_y_Bin_14)-(z_pT_Bin_1), (Q2_y_Bin_14)-(z_pT_Bin_2)
(Q2_y_Bin_14)-(z_pT_Bin_3), (Q2_y_Bin_14)-(z_pT_Bin_32), (Q2_y_Bin_14)-(z_pT_Bin_4)
(Q2_y_Bin_14)-(z_pT_Bin_5), (Q2_y_Bin_15)-(z_pT_Bin_1), (Q2_y_Bin_15)-(z_pT_Bin_14)
(Q2_y_Bin_15)-(z_pT_Bin_19), (Q2_y_Bin_15)-(z_pT_Bin_2), (Q2_y_Bin_15)-(z_pT_Bin_21)
(Q2_y_Bin_15)-(z_pT_Bin_22), (Q2_y_Bin_15)-(z_pT_Bin_23), (Q2_y_Bin_15)-(z_pT_Bin_9)
(Q2_y_Bin_16)-(z_pT_Bin_1), (Q2_y_Bin_16)-(z_pT_Bin_3), (Q2_y_Bin_16)-(z_pT_Bin_4)
(Q2_y_Bin_16)-(z_pT_Bin_5), (Q2_y_Bin_16)-(z_pT_Bin_6), (Q2_y_Bin_16)-(z_pT_Bin_9)
(Q2_y_Bin_17)-(z_pT_Bin_2), (Q2_y_Bin_17)-(z_pT_Bin_4), (Q2_y_Bin_2)-(z_pT_Bin_1)
(Q2_y_Bin_2)-(z_pT_Bin_10), (Q2_y_Bin_2)-(z_pT_Bin_11), (Q2_y_Bin_2)-(z_pT_Bin_12)
(Q2_y_Bin_2)-(z_pT_Bin_13), (Q2_y_Bin_2)-(z_pT_Bin_14), (Q2_y_Bin_2)-(z_pT_Bin_15)
(Q2_y_Bin_2)-(z_pT_Bin_16), (Q2_y_Bin_2)-(z_pT_Bin_18), (Q2_y_Bin_2)-(z_pT_Bin_19)
(Q2_y_Bin_2)-(z_pT_Bin_20), (Q2_y_Bin_2)-(z_pT_Bin_21), (Q2_y_Bin_2)-(z_pT_Bin_23)
(Q2_y_Bin_2)-(z_pT_Bin_25), (Q2_y_Bin_2)-(z_pT_Bin_26), (Q2_y_Bin_2)-(z_pT_Bin_27)
(Q2_y_Bin_2)-(z_pT_Bin_28), (Q2_y_Bin_2)-(z_pT_Bin_29), (Q2_y_Bin_2)-(z_pT_Bin_3)
(Q2_y_Bin_2)-(z_pT_Bin_32), (Q2_y_Bin_2)-(z_pT_Bin_33), (Q2_y_Bin_2)-(z_pT_Bin_34)
(Q2_y_Bin_2)-(z_pT_Bin_4), (Q2_y_Bin_2)-(z_pT_Bin_5), (Q2_y_Bin_2)-(z_pT_Bin_6)
(Q2_y_Bin_2)-(z_pT_Bin_7), (Q2_y_Bin_2)-(z_pT_Bin_8), (Q2_y_Bin_2)-(z_pT_Bin_9)
(Q2_y_Bin_3)-(z_pT_Bin_1), (Q2_y_Bin_3)-(z_pT_Bin_10), (Q2_y_Bin_3)-(z_pT_Bin_11)
(Q2_y_Bin_3)-(z_pT_Bin_12), (Q2_y_Bin_3)-(z_pT_Bin_13), (Q2_y_Bin_3)-(z_pT_Bin_14)
(Q2_y_Bin_3)-(z_pT_Bin_15), (Q2_y_Bin_3)-(z_pT_Bin_16), (Q2_y_Bin_3)-(z_pT_Bin_17)
(Q2_y_Bin_3)-(z_pT_Bin_18), (Q2_y_Bin_3)-(z_pT_Bin_19), (Q2_y_Bin_3)-(z_pT_Bin_2)
(Q2_y_Bin_3)-(z_pT_Bin_20), (Q2_y_Bin_3)-(z_pT_Bin_21), (Q2_y_Bin_3)-(z_pT_Bin_22)
(Q2_y_Bin_3)-(z_pT_Bin_23), (Q2_y_Bin_3)-(z_pT_Bin_24), (Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_7), (Q2_y_Bin_3)-(z_pT_Bin_8), (Q2_y_Bin_3)-(z_pT_Bin_9)
(Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_13), (Q2_y_Bin_4)-(z_pT_Bin_14)
(Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_19)
(Q2_y_Bin_4)-(z_pT_Bin_20), (Q2_y_Bin_4)-(z_pT_Bin_21), (Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_25), (Q2_y_Bin_4)-(z_pT_Bin_26), (Q2_y_Bin_4)-(z_pT_Bin_27)
(Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission], (Q2_y_Bin_5)-(z_pT_Bin_10)
(Q2_y_Bin_5)-(z_pT_Bin_11), (Q2_y_Bin_5)-(z_pT_Bin_13), (Q2_y_Bin_5)-(z_pT_Bin_14)
(Q2_y_Bin_5)-(z_pT_Bin_15), (Q2_y_Bin_5)-(z_pT_Bin_16), (Q2_y_Bin_5)-(z_pT_Bin_19)
(Q2_y_Bin_5)-(z_pT_Bin_2), (Q2_y_Bin_5)-(z_pT_Bin_20), (Q2_y_Bin_5)-(z_pT_Bin_21)
(Q2_y_Bin_5)-(z_pT_Bin_25), (Q2_y_Bin_5)-(z_pT_Bin_26), (Q2_y_Bin_5)-(z_pT_Bin_3)
(Q2_y_Bin_5)-(z_pT_Bin_31), (Q2_y_Bin_5)-(z_pT_Bin_32), (Q2_y_Bin_5)-(z_pT_Bin_33)
(Q2_y_Bin_5)-(z_pT_Bin_4), (Q2_y_Bin_5)-(z_pT_Bin_5), (Q2_y_Bin_5)-(z_pT_Bin_6)
(Q2_y_Bin_5)-(z_pT_Bin_7), (Q2_y_Bin_5)-(z_pT_Bin_8), (Q2_y_Bin_5)-(z_pT_Bin_9)
(Q2_y_Bin_6)-(z_pT_Bin_1), (Q2_y_Bin_6)-(z_pT_Bin_10), (Q2_y_Bin_6)-(z_pT_Bin_11)
(Q2_y_Bin_6)-(z_pT_Bin_13), (Q2_y_Bin_6)-(z_pT_Bin_14), (Q2_y_Bin_6)-(z_pT_Bin_15)
(Q2_y_Bin_6)-(z_pT_Bin_16), (Q2_y_Bin_6)-(z_pT_Bin_19), (Q2_y_Bin_6)-(z_pT_Bin_2)
(Q2_y_Bin_6)-(z_pT_Bin_20), (Q2_y_Bin_6)-(z_pT_Bin_27), (Q2_y_Bin_6)-(z_pT_Bin_28)
(Q2_y_Bin_6)-(z_pT_Bin_3), (Q2_y_Bin_6)-(z_pT_Bin_4), (Q2_y_Bin_6)-(z_pT_Bin_5)
(Q2_y_Bin_6)-(z_pT_Bin_6), (Q2_y_Bin_6)-(z_pT_Bin_7), (Q2_y_Bin_6)-(z_pT_Bin_8)
(Q2_y_Bin_6)-(z_pT_Bin_9), (Q2_y_Bin_7)-(z_pT_Bin_1), (Q2_y_Bin_7)-(z_pT_Bin_10)
(Q2_y_Bin_7)-(z_pT_Bin_11), (Q2_y_Bin_7)-(z_pT_Bin_12), (Q2_y_Bin_7)-(z_pT_Bin_13)
(Q2_y_Bin_7)-(z_pT_Bin_15), (Q2_y_Bin_7)-(z_pT_Bin_16), (Q2_y_Bin_7)-(z_pT_Bin_17)
(Q2_y_Bin_7)-(z_pT_Bin_18), (Q2_y_Bin_7)-(z_pT_Bin_19), (Q2_y_Bin_7)-(z_pT_Bin_2)
(Q2_y_Bin_7)-(z_pT_Bin_20), (Q2_y_Bin_7)-(z_pT_Bin_21), (Q2_y_Bin_7)-(z_pT_Bin_22)
(Q2_y_Bin_7)-(z_pT_Bin_23), (Q2_y_Bin_7)-(z_pT_Bin_24), (Q2_y_Bin_7)-(z_pT_Bin_25)
(Q2_y_Bin_7)-(z_pT_Bin_26), (Q2_y_Bin_7)-(z_pT_Bin_27), (Q2_y_Bin_7)-(z_pT_Bin_28)
(Q2_y_Bin_7)-(z_pT_Bin_29), (Q2_y_Bin_7)-(z_pT_Bin_3), (Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission]
(Q2_y_Bin_7)-(z_pT_Bin_7), (Q2_y_Bin_7)-(z_pT_Bin_8), (Q2_y_Bin_7)-(z_pT_Bin_9)
(Q2_y_Bin_8)-(z_pT_Bin_11), (Q2_y_Bin_8)-(z_pT_Bin_12), (Q2_y_Bin_8)-(z_pT_Bin_13)
(Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16), (Q2_y_Bin_8)-(z_pT_Bin_18)
(Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_21), (Q2_y_Bin_8)-(z_pT_Bin_23)
(Q2_y_Bin_8)-(z_pT_Bin_24), (Q2_y_Bin_8)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_26)
(Q2_y_Bin_8)-(z_pT_Bin_28), (Q2_y_Bin_8)-(z_pT_Bin_29), (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_9)-(z_pT_Bin_10), (Q2_y_Bin_9)-(z_pT_Bin_11), (Q2_y_Bin_9)-(z_pT_Bin_15)
(Q2_y_Bin_9)-(z_pT_Bin_16), (Q2_y_Bin_9)-(z_pT_Bin_2), (Q2_y_Bin_9)-(z_pT_Bin_22)
(Q2_y_Bin_9)-(z_pT_Bin_23), (Q2_y_Bin_9)-(z_pT_Bin_29), (Q2_y_Bin_9)-(z_pT_Bin_3)
(Q2_y_Bin_9)-(z_pT_Bin_30), (Q2_y_Bin_9)-(z_pT_Bin_4), (Q2_y_Bin_9)-(z_pT_Bin_5)
(Q2_y_Bin_9)-(z_pT_Bin_6), (Q2_y_Bin_9)-(z_pT_Bin_8), (Q2_y_Bin_9)-(z_pT_Bin_9)

#### 120°

The rule fails every assessable manual exclusion (30).

Manually excluded but passes:

None.

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_15), (Q2_y_Bin_1)-(z_pT_Bin_16)
(Q2_y_Bin_1)-(z_pT_Bin_17), (Q2_y_Bin_1)-(z_pT_Bin_2), (Q2_y_Bin_1)-(z_pT_Bin_22)
(Q2_y_Bin_1)-(z_pT_Bin_23), (Q2_y_Bin_1)-(z_pT_Bin_3), (Q2_y_Bin_1)-(z_pT_Bin_30)
(Q2_y_Bin_1)-(z_pT_Bin_31), (Q2_y_Bin_1)-(z_pT_Bin_32), (Q2_y_Bin_1)-(z_pT_Bin_5)
(Q2_y_Bin_1)-(z_pT_Bin_6), (Q2_y_Bin_1)-(z_pT_Bin_7), (Q2_y_Bin_1)-(z_pT_Bin_8)
(Q2_y_Bin_1)-(z_pT_Bin_9), (Q2_y_Bin_10)-(z_pT_Bin_1), (Q2_y_Bin_10)-(z_pT_Bin_10)
(Q2_y_Bin_10)-(z_pT_Bin_11), (Q2_y_Bin_10)-(z_pT_Bin_15), (Q2_y_Bin_10)-(z_pT_Bin_2)
(Q2_y_Bin_10)-(z_pT_Bin_26), (Q2_y_Bin_10)-(z_pT_Bin_3), (Q2_y_Bin_10)-(z_pT_Bin_31)
(Q2_y_Bin_10)-(z_pT_Bin_32), (Q2_y_Bin_10)-(z_pT_Bin_4), (Q2_y_Bin_10)-(z_pT_Bin_5)
(Q2_y_Bin_10)-(z_pT_Bin_6), (Q2_y_Bin_10)-(z_pT_Bin_7), (Q2_y_Bin_11)-(z_pT_Bin_1)
(Q2_y_Bin_11)-(z_pT_Bin_10), (Q2_y_Bin_11)-(z_pT_Bin_13), (Q2_y_Bin_11)-(z_pT_Bin_14)
(Q2_y_Bin_11)-(z_pT_Bin_15), (Q2_y_Bin_11)-(z_pT_Bin_18), (Q2_y_Bin_11)-(z_pT_Bin_19)
(Q2_y_Bin_11)-(z_pT_Bin_2), (Q2_y_Bin_11)-(z_pT_Bin_20), (Q2_y_Bin_11)-(z_pT_Bin_3)
(Q2_y_Bin_11)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_11)-(z_pT_Bin_6), (Q2_y_Bin_11)-(z_pT_Bin_9)
(Q2_y_Bin_12)-(z_pT_Bin_11), (Q2_y_Bin_12)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_21) [fit-quality omission]
(Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_6), (Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_13)-(z_pT_Bin_1), (Q2_y_Bin_13)-(z_pT_Bin_4), (Q2_y_Bin_14)-(z_pT_Bin_2)
(Q2_y_Bin_14)-(z_pT_Bin_32), (Q2_y_Bin_14)-(z_pT_Bin_4), (Q2_y_Bin_14)-(z_pT_Bin_5)
(Q2_y_Bin_15)-(z_pT_Bin_1), (Q2_y_Bin_15)-(z_pT_Bin_19), (Q2_y_Bin_15)-(z_pT_Bin_2)
(Q2_y_Bin_15)-(z_pT_Bin_21), (Q2_y_Bin_15)-(z_pT_Bin_22), (Q2_y_Bin_15)-(z_pT_Bin_23)
(Q2_y_Bin_15)-(z_pT_Bin_9), (Q2_y_Bin_16)-(z_pT_Bin_5), (Q2_y_Bin_16)-(z_pT_Bin_6)
(Q2_y_Bin_17)-(z_pT_Bin_4), (Q2_y_Bin_2)-(z_pT_Bin_1), (Q2_y_Bin_2)-(z_pT_Bin_10)
(Q2_y_Bin_2)-(z_pT_Bin_11), (Q2_y_Bin_2)-(z_pT_Bin_13), (Q2_y_Bin_2)-(z_pT_Bin_14)
(Q2_y_Bin_2)-(z_pT_Bin_15), (Q2_y_Bin_2)-(z_pT_Bin_16), (Q2_y_Bin_2)-(z_pT_Bin_19)
(Q2_y_Bin_2)-(z_pT_Bin_20), (Q2_y_Bin_2)-(z_pT_Bin_21), (Q2_y_Bin_2)-(z_pT_Bin_25)
(Q2_y_Bin_2)-(z_pT_Bin_26), (Q2_y_Bin_2)-(z_pT_Bin_3), (Q2_y_Bin_2)-(z_pT_Bin_32)
(Q2_y_Bin_2)-(z_pT_Bin_33), (Q2_y_Bin_2)-(z_pT_Bin_34), (Q2_y_Bin_2)-(z_pT_Bin_4)
(Q2_y_Bin_2)-(z_pT_Bin_5), (Q2_y_Bin_2)-(z_pT_Bin_6), (Q2_y_Bin_2)-(z_pT_Bin_7)
(Q2_y_Bin_2)-(z_pT_Bin_8), (Q2_y_Bin_2)-(z_pT_Bin_9), (Q2_y_Bin_3)-(z_pT_Bin_1)
(Q2_y_Bin_3)-(z_pT_Bin_10), (Q2_y_Bin_3)-(z_pT_Bin_11), (Q2_y_Bin_3)-(z_pT_Bin_12)
(Q2_y_Bin_3)-(z_pT_Bin_13), (Q2_y_Bin_3)-(z_pT_Bin_14), (Q2_y_Bin_3)-(z_pT_Bin_15)
(Q2_y_Bin_3)-(z_pT_Bin_16), (Q2_y_Bin_3)-(z_pT_Bin_17), (Q2_y_Bin_3)-(z_pT_Bin_18)
(Q2_y_Bin_3)-(z_pT_Bin_2), (Q2_y_Bin_3)-(z_pT_Bin_20), (Q2_y_Bin_3)-(z_pT_Bin_21)
(Q2_y_Bin_3)-(z_pT_Bin_22), (Q2_y_Bin_3)-(z_pT_Bin_23), (Q2_y_Bin_3)-(z_pT_Bin_24)
(Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_7), (Q2_y_Bin_3)-(z_pT_Bin_8)
(Q2_y_Bin_3)-(z_pT_Bin_9), (Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_13)
(Q2_y_Bin_4)-(z_pT_Bin_14), (Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_19), (Q2_y_Bin_4)-(z_pT_Bin_21), (Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_25), (Q2_y_Bin_4)-(z_pT_Bin_26), (Q2_y_Bin_4)-(z_pT_Bin_27)
(Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission], (Q2_y_Bin_5)-(z_pT_Bin_10)
(Q2_y_Bin_5)-(z_pT_Bin_11), (Q2_y_Bin_5)-(z_pT_Bin_13), (Q2_y_Bin_5)-(z_pT_Bin_14)
(Q2_y_Bin_5)-(z_pT_Bin_15), (Q2_y_Bin_5)-(z_pT_Bin_19), (Q2_y_Bin_5)-(z_pT_Bin_2)
(Q2_y_Bin_5)-(z_pT_Bin_20), (Q2_y_Bin_5)-(z_pT_Bin_25), (Q2_y_Bin_5)-(z_pT_Bin_3)
(Q2_y_Bin_5)-(z_pT_Bin_31), (Q2_y_Bin_5)-(z_pT_Bin_32), (Q2_y_Bin_5)-(z_pT_Bin_4)
(Q2_y_Bin_5)-(z_pT_Bin_5), (Q2_y_Bin_5)-(z_pT_Bin_6), (Q2_y_Bin_5)-(z_pT_Bin_7)
(Q2_y_Bin_5)-(z_pT_Bin_8), (Q2_y_Bin_5)-(z_pT_Bin_9), (Q2_y_Bin_6)-(z_pT_Bin_1)
(Q2_y_Bin_6)-(z_pT_Bin_10), (Q2_y_Bin_6)-(z_pT_Bin_14), (Q2_y_Bin_6)-(z_pT_Bin_15)
(Q2_y_Bin_6)-(z_pT_Bin_19), (Q2_y_Bin_6)-(z_pT_Bin_2), (Q2_y_Bin_6)-(z_pT_Bin_20)
(Q2_y_Bin_6)-(z_pT_Bin_27), (Q2_y_Bin_6)-(z_pT_Bin_28), (Q2_y_Bin_6)-(z_pT_Bin_3)
(Q2_y_Bin_6)-(z_pT_Bin_4), (Q2_y_Bin_6)-(z_pT_Bin_5), (Q2_y_Bin_6)-(z_pT_Bin_6)
(Q2_y_Bin_6)-(z_pT_Bin_7), (Q2_y_Bin_6)-(z_pT_Bin_8), (Q2_y_Bin_6)-(z_pT_Bin_9)
(Q2_y_Bin_7)-(z_pT_Bin_1), (Q2_y_Bin_7)-(z_pT_Bin_10), (Q2_y_Bin_7)-(z_pT_Bin_11)
(Q2_y_Bin_7)-(z_pT_Bin_12), (Q2_y_Bin_7)-(z_pT_Bin_13), (Q2_y_Bin_7)-(z_pT_Bin_15)
(Q2_y_Bin_7)-(z_pT_Bin_16), (Q2_y_Bin_7)-(z_pT_Bin_17), (Q2_y_Bin_7)-(z_pT_Bin_18)
(Q2_y_Bin_7)-(z_pT_Bin_2), (Q2_y_Bin_7)-(z_pT_Bin_21), (Q2_y_Bin_7)-(z_pT_Bin_23)
(Q2_y_Bin_7)-(z_pT_Bin_24), (Q2_y_Bin_7)-(z_pT_Bin_26), (Q2_y_Bin_7)-(z_pT_Bin_27)
(Q2_y_Bin_7)-(z_pT_Bin_28), (Q2_y_Bin_7)-(z_pT_Bin_29), (Q2_y_Bin_7)-(z_pT_Bin_3)
(Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_7)-(z_pT_Bin_7), (Q2_y_Bin_7)-(z_pT_Bin_9)
(Q2_y_Bin_8)-(z_pT_Bin_11), (Q2_y_Bin_8)-(z_pT_Bin_12), (Q2_y_Bin_8)-(z_pT_Bin_13)
(Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16), (Q2_y_Bin_8)-(z_pT_Bin_18)
(Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_21), (Q2_y_Bin_8)-(z_pT_Bin_23)
(Q2_y_Bin_8)-(z_pT_Bin_24), (Q2_y_Bin_8)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_28)
(Q2_y_Bin_8)-(z_pT_Bin_29), (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_9)-(z_pT_Bin_10)
(Q2_y_Bin_9)-(z_pT_Bin_16), (Q2_y_Bin_9)-(z_pT_Bin_2), (Q2_y_Bin_9)-(z_pT_Bin_29)
(Q2_y_Bin_9)-(z_pT_Bin_3), (Q2_y_Bin_9)-(z_pT_Bin_30), (Q2_y_Bin_9)-(z_pT_Bin_4)
(Q2_y_Bin_9)-(z_pT_Bin_5), (Q2_y_Bin_9)-(z_pT_Bin_6), (Q2_y_Bin_9)-(z_pT_Bin_9)

#### 135°

The rule fails every assessable manual exclusion (30).

Manually excluded but passes:

None.

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_15), (Q2_y_Bin_1)-(z_pT_Bin_16)
(Q2_y_Bin_1)-(z_pT_Bin_2), (Q2_y_Bin_1)-(z_pT_Bin_22), (Q2_y_Bin_1)-(z_pT_Bin_23)
(Q2_y_Bin_1)-(z_pT_Bin_3), (Q2_y_Bin_1)-(z_pT_Bin_30), (Q2_y_Bin_1)-(z_pT_Bin_31)
(Q2_y_Bin_1)-(z_pT_Bin_32), (Q2_y_Bin_1)-(z_pT_Bin_5), (Q2_y_Bin_1)-(z_pT_Bin_6)
(Q2_y_Bin_1)-(z_pT_Bin_7), (Q2_y_Bin_1)-(z_pT_Bin_8), (Q2_y_Bin_1)-(z_pT_Bin_9)
(Q2_y_Bin_10)-(z_pT_Bin_1), (Q2_y_Bin_10)-(z_pT_Bin_2), (Q2_y_Bin_10)-(z_pT_Bin_26)
(Q2_y_Bin_10)-(z_pT_Bin_3), (Q2_y_Bin_10)-(z_pT_Bin_31), (Q2_y_Bin_10)-(z_pT_Bin_32)
(Q2_y_Bin_10)-(z_pT_Bin_4), (Q2_y_Bin_10)-(z_pT_Bin_5), (Q2_y_Bin_10)-(z_pT_Bin_6)
(Q2_y_Bin_10)-(z_pT_Bin_7), (Q2_y_Bin_11)-(z_pT_Bin_1), (Q2_y_Bin_11)-(z_pT_Bin_10)
(Q2_y_Bin_11)-(z_pT_Bin_14), (Q2_y_Bin_11)-(z_pT_Bin_15), (Q2_y_Bin_11)-(z_pT_Bin_18)
(Q2_y_Bin_11)-(z_pT_Bin_19), (Q2_y_Bin_11)-(z_pT_Bin_2), (Q2_y_Bin_11)-(z_pT_Bin_20)
(Q2_y_Bin_11)-(z_pT_Bin_3), (Q2_y_Bin_11)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_11)-(z_pT_Bin_6)
(Q2_y_Bin_11)-(z_pT_Bin_9), (Q2_y_Bin_12)-(z_pT_Bin_11), (Q2_y_Bin_12)-(z_pT_Bin_14) [fit-quality omission]
(Q2_y_Bin_12)-(z_pT_Bin_21) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_6)
(Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_13)-(z_pT_Bin_1), (Q2_y_Bin_14)-(z_pT_Bin_32)
(Q2_y_Bin_14)-(z_pT_Bin_5), (Q2_y_Bin_15)-(z_pT_Bin_1), (Q2_y_Bin_15)-(z_pT_Bin_2)
(Q2_y_Bin_15)-(z_pT_Bin_21), (Q2_y_Bin_15)-(z_pT_Bin_22), (Q2_y_Bin_15)-(z_pT_Bin_23)
(Q2_y_Bin_15)-(z_pT_Bin_9), (Q2_y_Bin_16)-(z_pT_Bin_5), (Q2_y_Bin_16)-(z_pT_Bin_6)
(Q2_y_Bin_17)-(z_pT_Bin_4), (Q2_y_Bin_2)-(z_pT_Bin_1), (Q2_y_Bin_2)-(z_pT_Bin_10)
(Q2_y_Bin_2)-(z_pT_Bin_11), (Q2_y_Bin_2)-(z_pT_Bin_13), (Q2_y_Bin_2)-(z_pT_Bin_14)
(Q2_y_Bin_2)-(z_pT_Bin_15), (Q2_y_Bin_2)-(z_pT_Bin_16), (Q2_y_Bin_2)-(z_pT_Bin_19)
(Q2_y_Bin_2)-(z_pT_Bin_20), (Q2_y_Bin_2)-(z_pT_Bin_25), (Q2_y_Bin_2)-(z_pT_Bin_3)
(Q2_y_Bin_2)-(z_pT_Bin_32), (Q2_y_Bin_2)-(z_pT_Bin_33), (Q2_y_Bin_2)-(z_pT_Bin_34)
(Q2_y_Bin_2)-(z_pT_Bin_4), (Q2_y_Bin_2)-(z_pT_Bin_5), (Q2_y_Bin_2)-(z_pT_Bin_6)
(Q2_y_Bin_2)-(z_pT_Bin_7), (Q2_y_Bin_2)-(z_pT_Bin_8), (Q2_y_Bin_2)-(z_pT_Bin_9)
(Q2_y_Bin_3)-(z_pT_Bin_1), (Q2_y_Bin_3)-(z_pT_Bin_10), (Q2_y_Bin_3)-(z_pT_Bin_11)
(Q2_y_Bin_3)-(z_pT_Bin_12), (Q2_y_Bin_3)-(z_pT_Bin_13), (Q2_y_Bin_3)-(z_pT_Bin_14)
(Q2_y_Bin_3)-(z_pT_Bin_15), (Q2_y_Bin_3)-(z_pT_Bin_16), (Q2_y_Bin_3)-(z_pT_Bin_17)
(Q2_y_Bin_3)-(z_pT_Bin_18), (Q2_y_Bin_3)-(z_pT_Bin_2), (Q2_y_Bin_3)-(z_pT_Bin_20)
(Q2_y_Bin_3)-(z_pT_Bin_21), (Q2_y_Bin_3)-(z_pT_Bin_22), (Q2_y_Bin_3)-(z_pT_Bin_23)
(Q2_y_Bin_3)-(z_pT_Bin_24), (Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_7)
(Q2_y_Bin_3)-(z_pT_Bin_8), (Q2_y_Bin_3)-(z_pT_Bin_9), (Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_13), (Q2_y_Bin_4)-(z_pT_Bin_14), (Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_19), (Q2_y_Bin_4)-(z_pT_Bin_21)
(Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_25), (Q2_y_Bin_4)-(z_pT_Bin_26)
(Q2_y_Bin_4)-(z_pT_Bin_27), (Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission]
(Q2_y_Bin_5)-(z_pT_Bin_10), (Q2_y_Bin_5)-(z_pT_Bin_13), (Q2_y_Bin_5)-(z_pT_Bin_14)
(Q2_y_Bin_5)-(z_pT_Bin_15), (Q2_y_Bin_5)-(z_pT_Bin_19), (Q2_y_Bin_5)-(z_pT_Bin_2)
(Q2_y_Bin_5)-(z_pT_Bin_20), (Q2_y_Bin_5)-(z_pT_Bin_25), (Q2_y_Bin_5)-(z_pT_Bin_3)
(Q2_y_Bin_5)-(z_pT_Bin_31), (Q2_y_Bin_5)-(z_pT_Bin_32), (Q2_y_Bin_5)-(z_pT_Bin_4)
(Q2_y_Bin_5)-(z_pT_Bin_5), (Q2_y_Bin_5)-(z_pT_Bin_6), (Q2_y_Bin_5)-(z_pT_Bin_7)
(Q2_y_Bin_5)-(z_pT_Bin_8), (Q2_y_Bin_5)-(z_pT_Bin_9), (Q2_y_Bin_6)-(z_pT_Bin_1)
(Q2_y_Bin_6)-(z_pT_Bin_10), (Q2_y_Bin_6)-(z_pT_Bin_14), (Q2_y_Bin_6)-(z_pT_Bin_2)
(Q2_y_Bin_6)-(z_pT_Bin_20), (Q2_y_Bin_6)-(z_pT_Bin_27), (Q2_y_Bin_6)-(z_pT_Bin_28)
(Q2_y_Bin_6)-(z_pT_Bin_3), (Q2_y_Bin_6)-(z_pT_Bin_4), (Q2_y_Bin_6)-(z_pT_Bin_5)
(Q2_y_Bin_6)-(z_pT_Bin_6), (Q2_y_Bin_6)-(z_pT_Bin_7), (Q2_y_Bin_6)-(z_pT_Bin_8)
(Q2_y_Bin_6)-(z_pT_Bin_9), (Q2_y_Bin_7)-(z_pT_Bin_1), (Q2_y_Bin_7)-(z_pT_Bin_10)
(Q2_y_Bin_7)-(z_pT_Bin_11), (Q2_y_Bin_7)-(z_pT_Bin_12), (Q2_y_Bin_7)-(z_pT_Bin_13)
(Q2_y_Bin_7)-(z_pT_Bin_15), (Q2_y_Bin_7)-(z_pT_Bin_17), (Q2_y_Bin_7)-(z_pT_Bin_18)
(Q2_y_Bin_7)-(z_pT_Bin_2), (Q2_y_Bin_7)-(z_pT_Bin_21), (Q2_y_Bin_7)-(z_pT_Bin_23)
(Q2_y_Bin_7)-(z_pT_Bin_24), (Q2_y_Bin_7)-(z_pT_Bin_27), (Q2_y_Bin_7)-(z_pT_Bin_28)
(Q2_y_Bin_7)-(z_pT_Bin_29), (Q2_y_Bin_7)-(z_pT_Bin_3), (Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission]
(Q2_y_Bin_7)-(z_pT_Bin_7), (Q2_y_Bin_7)-(z_pT_Bin_9), (Q2_y_Bin_8)-(z_pT_Bin_11)
(Q2_y_Bin_8)-(z_pT_Bin_13), (Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16)
(Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_23), (Q2_y_Bin_8)-(z_pT_Bin_24)
(Q2_y_Bin_8)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_28), (Q2_y_Bin_8)-(z_pT_Bin_29)
(Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_9)-(z_pT_Bin_16), (Q2_y_Bin_9)-(z_pT_Bin_2)
(Q2_y_Bin_9)-(z_pT_Bin_29), (Q2_y_Bin_9)-(z_pT_Bin_3), (Q2_y_Bin_9)-(z_pT_Bin_4)
(Q2_y_Bin_9)-(z_pT_Bin_5)

#### 150°

The rule fails every assessable manual exclusion (30).

Manually excluded but passes:

None.

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_15), (Q2_y_Bin_1)-(z_pT_Bin_16)
(Q2_y_Bin_1)-(z_pT_Bin_2), (Q2_y_Bin_1)-(z_pT_Bin_22), (Q2_y_Bin_1)-(z_pT_Bin_3)
(Q2_y_Bin_1)-(z_pT_Bin_30), (Q2_y_Bin_1)-(z_pT_Bin_32), (Q2_y_Bin_1)-(z_pT_Bin_5)
(Q2_y_Bin_1)-(z_pT_Bin_6), (Q2_y_Bin_1)-(z_pT_Bin_7), (Q2_y_Bin_1)-(z_pT_Bin_8)
(Q2_y_Bin_1)-(z_pT_Bin_9), (Q2_y_Bin_10)-(z_pT_Bin_1), (Q2_y_Bin_10)-(z_pT_Bin_3)
(Q2_y_Bin_10)-(z_pT_Bin_31), (Q2_y_Bin_10)-(z_pT_Bin_32), (Q2_y_Bin_10)-(z_pT_Bin_4)
(Q2_y_Bin_10)-(z_pT_Bin_5), (Q2_y_Bin_10)-(z_pT_Bin_6), (Q2_y_Bin_10)-(z_pT_Bin_7)
(Q2_y_Bin_11)-(z_pT_Bin_1), (Q2_y_Bin_11)-(z_pT_Bin_10), (Q2_y_Bin_11)-(z_pT_Bin_15)
(Q2_y_Bin_11)-(z_pT_Bin_2), (Q2_y_Bin_11)-(z_pT_Bin_20), (Q2_y_Bin_11)-(z_pT_Bin_3)
(Q2_y_Bin_11)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_11)-(z_pT_Bin_6), (Q2_y_Bin_11)-(z_pT_Bin_9)
(Q2_y_Bin_12)-(z_pT_Bin_11), (Q2_y_Bin_12)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_21) [fit-quality omission]
(Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_6), (Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_13)-(z_pT_Bin_1), (Q2_y_Bin_14)-(z_pT_Bin_5), (Q2_y_Bin_15)-(z_pT_Bin_1)
(Q2_y_Bin_15)-(z_pT_Bin_2), (Q2_y_Bin_15)-(z_pT_Bin_22), (Q2_y_Bin_15)-(z_pT_Bin_23)
(Q2_y_Bin_15)-(z_pT_Bin_9), (Q2_y_Bin_16)-(z_pT_Bin_6), (Q2_y_Bin_17)-(z_pT_Bin_4)
(Q2_y_Bin_2)-(z_pT_Bin_1), (Q2_y_Bin_2)-(z_pT_Bin_10), (Q2_y_Bin_2)-(z_pT_Bin_13)
(Q2_y_Bin_2)-(z_pT_Bin_14), (Q2_y_Bin_2)-(z_pT_Bin_15), (Q2_y_Bin_2)-(z_pT_Bin_19)
(Q2_y_Bin_2)-(z_pT_Bin_20), (Q2_y_Bin_2)-(z_pT_Bin_25), (Q2_y_Bin_2)-(z_pT_Bin_3)
(Q2_y_Bin_2)-(z_pT_Bin_32), (Q2_y_Bin_2)-(z_pT_Bin_33), (Q2_y_Bin_2)-(z_pT_Bin_34)
(Q2_y_Bin_2)-(z_pT_Bin_4), (Q2_y_Bin_2)-(z_pT_Bin_5), (Q2_y_Bin_2)-(z_pT_Bin_6)
(Q2_y_Bin_2)-(z_pT_Bin_7), (Q2_y_Bin_2)-(z_pT_Bin_8), (Q2_y_Bin_2)-(z_pT_Bin_9)
(Q2_y_Bin_3)-(z_pT_Bin_1), (Q2_y_Bin_3)-(z_pT_Bin_10), (Q2_y_Bin_3)-(z_pT_Bin_11)
(Q2_y_Bin_3)-(z_pT_Bin_12), (Q2_y_Bin_3)-(z_pT_Bin_13), (Q2_y_Bin_3)-(z_pT_Bin_15)
(Q2_y_Bin_3)-(z_pT_Bin_16), (Q2_y_Bin_3)-(z_pT_Bin_17), (Q2_y_Bin_3)-(z_pT_Bin_18)
(Q2_y_Bin_3)-(z_pT_Bin_2), (Q2_y_Bin_3)-(z_pT_Bin_20), (Q2_y_Bin_3)-(z_pT_Bin_21)
(Q2_y_Bin_3)-(z_pT_Bin_24), (Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_7)
(Q2_y_Bin_3)-(z_pT_Bin_9), (Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_13)
(Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_19)
(Q2_y_Bin_4)-(z_pT_Bin_21), (Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_25)
(Q2_y_Bin_4)-(z_pT_Bin_27), (Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission]
(Q2_y_Bin_5)-(z_pT_Bin_10), (Q2_y_Bin_5)-(z_pT_Bin_13), (Q2_y_Bin_5)-(z_pT_Bin_14)
(Q2_y_Bin_5)-(z_pT_Bin_19), (Q2_y_Bin_5)-(z_pT_Bin_2), (Q2_y_Bin_5)-(z_pT_Bin_20)
(Q2_y_Bin_5)-(z_pT_Bin_25), (Q2_y_Bin_5)-(z_pT_Bin_3), (Q2_y_Bin_5)-(z_pT_Bin_31)
(Q2_y_Bin_5)-(z_pT_Bin_32), (Q2_y_Bin_5)-(z_pT_Bin_4), (Q2_y_Bin_5)-(z_pT_Bin_5)
(Q2_y_Bin_5)-(z_pT_Bin_6), (Q2_y_Bin_5)-(z_pT_Bin_7), (Q2_y_Bin_5)-(z_pT_Bin_8)
(Q2_y_Bin_5)-(z_pT_Bin_9), (Q2_y_Bin_6)-(z_pT_Bin_1), (Q2_y_Bin_6)-(z_pT_Bin_14)
(Q2_y_Bin_6)-(z_pT_Bin_2), (Q2_y_Bin_6)-(z_pT_Bin_20), (Q2_y_Bin_6)-(z_pT_Bin_27)
(Q2_y_Bin_6)-(z_pT_Bin_28), (Q2_y_Bin_6)-(z_pT_Bin_3), (Q2_y_Bin_6)-(z_pT_Bin_4)
(Q2_y_Bin_6)-(z_pT_Bin_5), (Q2_y_Bin_6)-(z_pT_Bin_6), (Q2_y_Bin_6)-(z_pT_Bin_7)
(Q2_y_Bin_6)-(z_pT_Bin_8), (Q2_y_Bin_6)-(z_pT_Bin_9), (Q2_y_Bin_7)-(z_pT_Bin_1)
(Q2_y_Bin_7)-(z_pT_Bin_11), (Q2_y_Bin_7)-(z_pT_Bin_12), (Q2_y_Bin_7)-(z_pT_Bin_13)
(Q2_y_Bin_7)-(z_pT_Bin_18), (Q2_y_Bin_7)-(z_pT_Bin_2), (Q2_y_Bin_7)-(z_pT_Bin_21)
(Q2_y_Bin_7)-(z_pT_Bin_24), (Q2_y_Bin_7)-(z_pT_Bin_29), (Q2_y_Bin_7)-(z_pT_Bin_3)
(Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_7)-(z_pT_Bin_7), (Q2_y_Bin_8)-(z_pT_Bin_11)
(Q2_y_Bin_8)-(z_pT_Bin_13), (Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16)
(Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_24), (Q2_y_Bin_8)-(z_pT_Bin_25) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_28), (Q2_y_Bin_8)-(z_pT_Bin_29), (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_9)-(z_pT_Bin_2), (Q2_y_Bin_9)-(z_pT_Bin_29), (Q2_y_Bin_9)-(z_pT_Bin_3)

#### 180°

The rule fails every assessable manual exclusion (30).

Manually excluded but passes:

None.

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_15), (Q2_y_Bin_1)-(z_pT_Bin_2)
(Q2_y_Bin_1)-(z_pT_Bin_3), (Q2_y_Bin_1)-(z_pT_Bin_30), (Q2_y_Bin_1)-(z_pT_Bin_5)
(Q2_y_Bin_1)-(z_pT_Bin_8), (Q2_y_Bin_1)-(z_pT_Bin_9), (Q2_y_Bin_10)-(z_pT_Bin_32)
(Q2_y_Bin_10)-(z_pT_Bin_5), (Q2_y_Bin_10)-(z_pT_Bin_6), (Q2_y_Bin_11)-(z_pT_Bin_2)
(Q2_y_Bin_11)-(z_pT_Bin_20), (Q2_y_Bin_11)-(z_pT_Bin_3), (Q2_y_Bin_11)-(z_pT_Bin_4) [fit-quality omission]
(Q2_y_Bin_12)-(z_pT_Bin_11), (Q2_y_Bin_12)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_21) [fit-quality omission]
(Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_6), (Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_14)-(z_pT_Bin_5), (Q2_y_Bin_15)-(z_pT_Bin_1), (Q2_y_Bin_15)-(z_pT_Bin_2)
(Q2_y_Bin_15)-(z_pT_Bin_22), (Q2_y_Bin_15)-(z_pT_Bin_23), (Q2_y_Bin_2)-(z_pT_Bin_1)
(Q2_y_Bin_2)-(z_pT_Bin_3), (Q2_y_Bin_2)-(z_pT_Bin_4), (Q2_y_Bin_2)-(z_pT_Bin_5)
(Q2_y_Bin_2)-(z_pT_Bin_6), (Q2_y_Bin_2)-(z_pT_Bin_7), (Q2_y_Bin_2)-(z_pT_Bin_9)
(Q2_y_Bin_3)-(z_pT_Bin_1), (Q2_y_Bin_3)-(z_pT_Bin_10), (Q2_y_Bin_3)-(z_pT_Bin_2)
(Q2_y_Bin_3)-(z_pT_Bin_24), (Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_7)
(Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_13), (Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_19), (Q2_y_Bin_4)-(z_pT_Bin_21)
(Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_25), (Q2_y_Bin_4)-(z_pT_Bin_27)
(Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission], (Q2_y_Bin_5)-(z_pT_Bin_2)
(Q2_y_Bin_5)-(z_pT_Bin_3), (Q2_y_Bin_5)-(z_pT_Bin_31), (Q2_y_Bin_5)-(z_pT_Bin_4)
(Q2_y_Bin_5)-(z_pT_Bin_5), (Q2_y_Bin_5)-(z_pT_Bin_6), (Q2_y_Bin_5)-(z_pT_Bin_7)
(Q2_y_Bin_5)-(z_pT_Bin_8), (Q2_y_Bin_5)-(z_pT_Bin_9), (Q2_y_Bin_6)-(z_pT_Bin_1)
(Q2_y_Bin_6)-(z_pT_Bin_27), (Q2_y_Bin_6)-(z_pT_Bin_28), (Q2_y_Bin_7)-(z_pT_Bin_12)
(Q2_y_Bin_7)-(z_pT_Bin_2), (Q2_y_Bin_7)-(z_pT_Bin_24), (Q2_y_Bin_7)-(z_pT_Bin_3)
(Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_11), (Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_16), (Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_24)
(Q2_y_Bin_8)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_29), (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_9)-(z_pT_Bin_29)

### eS2o

Manual list entries: 31. Fit-quality omissions relative to the nominal acceptance bins: 37. Comparisons the budget still keeps: 389.

#### 90°

The rule fails every assessable manual exclusion (31).

Manually excluded but passes:

None.

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_1), (Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_11)
(Q2_y_Bin_1)-(z_pT_Bin_15), (Q2_y_Bin_1)-(z_pT_Bin_16), (Q2_y_Bin_1)-(z_pT_Bin_17)
(Q2_y_Bin_1)-(z_pT_Bin_22), (Q2_y_Bin_1)-(z_pT_Bin_23), (Q2_y_Bin_1)-(z_pT_Bin_30)
(Q2_y_Bin_1)-(z_pT_Bin_31), (Q2_y_Bin_1)-(z_pT_Bin_32), (Q2_y_Bin_1)-(z_pT_Bin_4)
(Q2_y_Bin_1)-(z_pT_Bin_5), (Q2_y_Bin_1)-(z_pT_Bin_6), (Q2_y_Bin_1)-(z_pT_Bin_7)
(Q2_y_Bin_1)-(z_pT_Bin_8), (Q2_y_Bin_1)-(z_pT_Bin_9), (Q2_y_Bin_10)-(z_pT_Bin_1)
(Q2_y_Bin_10)-(z_pT_Bin_10), (Q2_y_Bin_10)-(z_pT_Bin_11), (Q2_y_Bin_10)-(z_pT_Bin_13)
(Q2_y_Bin_10)-(z_pT_Bin_14), (Q2_y_Bin_10)-(z_pT_Bin_15), (Q2_y_Bin_10)-(z_pT_Bin_19)
(Q2_y_Bin_10)-(z_pT_Bin_2), (Q2_y_Bin_10)-(z_pT_Bin_20), (Q2_y_Bin_10)-(z_pT_Bin_26)
(Q2_y_Bin_10)-(z_pT_Bin_3), (Q2_y_Bin_10)-(z_pT_Bin_31), (Q2_y_Bin_10)-(z_pT_Bin_32)
(Q2_y_Bin_10)-(z_pT_Bin_33), (Q2_y_Bin_10)-(z_pT_Bin_4), (Q2_y_Bin_10)-(z_pT_Bin_5)
(Q2_y_Bin_10)-(z_pT_Bin_6), (Q2_y_Bin_10)-(z_pT_Bin_7), (Q2_y_Bin_10)-(z_pT_Bin_8)
(Q2_y_Bin_10)-(z_pT_Bin_9), (Q2_y_Bin_11)-(z_pT_Bin_1), (Q2_y_Bin_11)-(z_pT_Bin_10)
(Q2_y_Bin_11)-(z_pT_Bin_11), (Q2_y_Bin_11)-(z_pT_Bin_13), (Q2_y_Bin_11)-(z_pT_Bin_18)
(Q2_y_Bin_11)-(z_pT_Bin_2), (Q2_y_Bin_11)-(z_pT_Bin_20), (Q2_y_Bin_11)-(z_pT_Bin_21)
(Q2_y_Bin_11)-(z_pT_Bin_22), (Q2_y_Bin_11)-(z_pT_Bin_23), (Q2_y_Bin_11)-(z_pT_Bin_24)
(Q2_y_Bin_11)-(z_pT_Bin_3), (Q2_y_Bin_11)-(z_pT_Bin_6), (Q2_y_Bin_11)-(z_pT_Bin_8)
(Q2_y_Bin_11)-(z_pT_Bin_9), (Q2_y_Bin_12)-(z_pT_Bin_11), (Q2_y_Bin_12)-(z_pT_Bin_13)
(Q2_y_Bin_12)-(z_pT_Bin_16), (Q2_y_Bin_12)-(z_pT_Bin_18), (Q2_y_Bin_12)-(z_pT_Bin_21) [fit-quality omission]
(Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_6), (Q2_y_Bin_12)-(z_pT_Bin_7)
(Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_13)-(z_pT_Bin_1), (Q2_y_Bin_13)-(z_pT_Bin_12)
(Q2_y_Bin_13)-(z_pT_Bin_2), (Q2_y_Bin_13)-(z_pT_Bin_26), (Q2_y_Bin_13)-(z_pT_Bin_3)
(Q2_y_Bin_13)-(z_pT_Bin_4), (Q2_y_Bin_13)-(z_pT_Bin_5), (Q2_y_Bin_13)-(z_pT_Bin_7)
(Q2_y_Bin_13)-(z_pT_Bin_8), (Q2_y_Bin_14)-(z_pT_Bin_1), (Q2_y_Bin_14)-(z_pT_Bin_2)
(Q2_y_Bin_14)-(z_pT_Bin_3), (Q2_y_Bin_14)-(z_pT_Bin_32), (Q2_y_Bin_14)-(z_pT_Bin_4)
(Q2_y_Bin_14)-(z_pT_Bin_5), (Q2_y_Bin_15)-(z_pT_Bin_1), (Q2_y_Bin_15)-(z_pT_Bin_15)
(Q2_y_Bin_15)-(z_pT_Bin_2), (Q2_y_Bin_15)-(z_pT_Bin_21), (Q2_y_Bin_15)-(z_pT_Bin_22)
(Q2_y_Bin_15)-(z_pT_Bin_23), (Q2_y_Bin_15)-(z_pT_Bin_6), (Q2_y_Bin_15)-(z_pT_Bin_9)
(Q2_y_Bin_16)-(z_pT_Bin_1), (Q2_y_Bin_16)-(z_pT_Bin_4), (Q2_y_Bin_16)-(z_pT_Bin_5)
(Q2_y_Bin_16)-(z_pT_Bin_6), (Q2_y_Bin_17)-(z_pT_Bin_1), (Q2_y_Bin_17)-(z_pT_Bin_4)
(Q2_y_Bin_2)-(z_pT_Bin_1), (Q2_y_Bin_2)-(z_pT_Bin_10), (Q2_y_Bin_2)-(z_pT_Bin_11)
(Q2_y_Bin_2)-(z_pT_Bin_12), (Q2_y_Bin_2)-(z_pT_Bin_13), (Q2_y_Bin_2)-(z_pT_Bin_14)
(Q2_y_Bin_2)-(z_pT_Bin_15), (Q2_y_Bin_2)-(z_pT_Bin_16), (Q2_y_Bin_2)-(z_pT_Bin_19)
(Q2_y_Bin_2)-(z_pT_Bin_2), (Q2_y_Bin_2)-(z_pT_Bin_20), (Q2_y_Bin_2)-(z_pT_Bin_21)
(Q2_y_Bin_2)-(z_pT_Bin_25), (Q2_y_Bin_2)-(z_pT_Bin_26), (Q2_y_Bin_2)-(z_pT_Bin_27)
(Q2_y_Bin_2)-(z_pT_Bin_28), (Q2_y_Bin_2)-(z_pT_Bin_3), (Q2_y_Bin_2)-(z_pT_Bin_32)
(Q2_y_Bin_2)-(z_pT_Bin_33), (Q2_y_Bin_2)-(z_pT_Bin_34), (Q2_y_Bin_2)-(z_pT_Bin_4)
(Q2_y_Bin_2)-(z_pT_Bin_5), (Q2_y_Bin_2)-(z_pT_Bin_6), (Q2_y_Bin_2)-(z_pT_Bin_7)
(Q2_y_Bin_2)-(z_pT_Bin_8), (Q2_y_Bin_2)-(z_pT_Bin_9), (Q2_y_Bin_3)-(z_pT_Bin_1)
(Q2_y_Bin_3)-(z_pT_Bin_11), (Q2_y_Bin_3)-(z_pT_Bin_12), (Q2_y_Bin_3)-(z_pT_Bin_13)
(Q2_y_Bin_3)-(z_pT_Bin_14), (Q2_y_Bin_3)-(z_pT_Bin_16), (Q2_y_Bin_3)-(z_pT_Bin_17)
(Q2_y_Bin_3)-(z_pT_Bin_18), (Q2_y_Bin_3)-(z_pT_Bin_19), (Q2_y_Bin_3)-(z_pT_Bin_2)
(Q2_y_Bin_3)-(z_pT_Bin_20), (Q2_y_Bin_3)-(z_pT_Bin_21), (Q2_y_Bin_3)-(z_pT_Bin_22)
(Q2_y_Bin_3)-(z_pT_Bin_23), (Q2_y_Bin_3)-(z_pT_Bin_24), (Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_7), (Q2_y_Bin_3)-(z_pT_Bin_8), (Q2_y_Bin_3)-(z_pT_Bin_9)
(Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_14), (Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_19), (Q2_y_Bin_4)-(z_pT_Bin_20)
(Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_26), (Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission], (Q2_y_Bin_5)-(z_pT_Bin_1), (Q2_y_Bin_5)-(z_pT_Bin_10)
(Q2_y_Bin_5)-(z_pT_Bin_11), (Q2_y_Bin_5)-(z_pT_Bin_13), (Q2_y_Bin_5)-(z_pT_Bin_14)
(Q2_y_Bin_5)-(z_pT_Bin_15), (Q2_y_Bin_5)-(z_pT_Bin_19), (Q2_y_Bin_5)-(z_pT_Bin_20)
(Q2_y_Bin_5)-(z_pT_Bin_25), (Q2_y_Bin_5)-(z_pT_Bin_26), (Q2_y_Bin_5)-(z_pT_Bin_3)
(Q2_y_Bin_5)-(z_pT_Bin_31), (Q2_y_Bin_5)-(z_pT_Bin_32), (Q2_y_Bin_5)-(z_pT_Bin_4)
(Q2_y_Bin_5)-(z_pT_Bin_5), (Q2_y_Bin_5)-(z_pT_Bin_6), (Q2_y_Bin_5)-(z_pT_Bin_7)
(Q2_y_Bin_5)-(z_pT_Bin_8), (Q2_y_Bin_5)-(z_pT_Bin_9), (Q2_y_Bin_6)-(z_pT_Bin_1)
(Q2_y_Bin_6)-(z_pT_Bin_10), (Q2_y_Bin_6)-(z_pT_Bin_13), (Q2_y_Bin_6)-(z_pT_Bin_14)
(Q2_y_Bin_6)-(z_pT_Bin_15), (Q2_y_Bin_6)-(z_pT_Bin_19), (Q2_y_Bin_6)-(z_pT_Bin_2)
(Q2_y_Bin_6)-(z_pT_Bin_20), (Q2_y_Bin_6)-(z_pT_Bin_26), (Q2_y_Bin_6)-(z_pT_Bin_27)
(Q2_y_Bin_6)-(z_pT_Bin_28), (Q2_y_Bin_6)-(z_pT_Bin_3), (Q2_y_Bin_6)-(z_pT_Bin_4)
(Q2_y_Bin_6)-(z_pT_Bin_5), (Q2_y_Bin_6)-(z_pT_Bin_6), (Q2_y_Bin_6)-(z_pT_Bin_7)
(Q2_y_Bin_7)-(z_pT_Bin_1), (Q2_y_Bin_7)-(z_pT_Bin_10), (Q2_y_Bin_7)-(z_pT_Bin_11)
(Q2_y_Bin_7)-(z_pT_Bin_12), (Q2_y_Bin_7)-(z_pT_Bin_13), (Q2_y_Bin_7)-(z_pT_Bin_15)
(Q2_y_Bin_7)-(z_pT_Bin_16), (Q2_y_Bin_7)-(z_pT_Bin_17), (Q2_y_Bin_7)-(z_pT_Bin_18)
(Q2_y_Bin_7)-(z_pT_Bin_19), (Q2_y_Bin_7)-(z_pT_Bin_2), (Q2_y_Bin_7)-(z_pT_Bin_20)
(Q2_y_Bin_7)-(z_pT_Bin_21), (Q2_y_Bin_7)-(z_pT_Bin_22), (Q2_y_Bin_7)-(z_pT_Bin_23)
(Q2_y_Bin_7)-(z_pT_Bin_24), (Q2_y_Bin_7)-(z_pT_Bin_25), (Q2_y_Bin_7)-(z_pT_Bin_26)
(Q2_y_Bin_7)-(z_pT_Bin_27), (Q2_y_Bin_7)-(z_pT_Bin_28), (Q2_y_Bin_7)-(z_pT_Bin_29)
(Q2_y_Bin_7)-(z_pT_Bin_34), (Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_7)-(z_pT_Bin_7)
(Q2_y_Bin_7)-(z_pT_Bin_8), (Q2_y_Bin_7)-(z_pT_Bin_9), (Q2_y_Bin_8)-(z_pT_Bin_11)
(Q2_y_Bin_8)-(z_pT_Bin_12), (Q2_y_Bin_8)-(z_pT_Bin_13), (Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_16), (Q2_y_Bin_8)-(z_pT_Bin_18), (Q2_y_Bin_8)-(z_pT_Bin_19)
(Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_21), (Q2_y_Bin_8)-(z_pT_Bin_23)
(Q2_y_Bin_8)-(z_pT_Bin_24), (Q2_y_Bin_8)-(z_pT_Bin_26), (Q2_y_Bin_8)-(z_pT_Bin_28)
(Q2_y_Bin_8)-(z_pT_Bin_29), (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_9)-(z_pT_Bin_1)
(Q2_y_Bin_9)-(z_pT_Bin_10), (Q2_y_Bin_9)-(z_pT_Bin_11), (Q2_y_Bin_9)-(z_pT_Bin_15)
(Q2_y_Bin_9)-(z_pT_Bin_16), (Q2_y_Bin_9)-(z_pT_Bin_2), (Q2_y_Bin_9)-(z_pT_Bin_22)
(Q2_y_Bin_9)-(z_pT_Bin_23), (Q2_y_Bin_9)-(z_pT_Bin_29), (Q2_y_Bin_9)-(z_pT_Bin_3)
(Q2_y_Bin_9)-(z_pT_Bin_30), (Q2_y_Bin_9)-(z_pT_Bin_4), (Q2_y_Bin_9)-(z_pT_Bin_5)
(Q2_y_Bin_9)-(z_pT_Bin_6), (Q2_y_Bin_9)-(z_pT_Bin_8), (Q2_y_Bin_9)-(z_pT_Bin_9)

#### 120°

The rule fails every assessable manual exclusion (31).

Manually excluded but passes:

None.

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_1), (Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_15)
(Q2_y_Bin_1)-(z_pT_Bin_16), (Q2_y_Bin_1)-(z_pT_Bin_22), (Q2_y_Bin_1)-(z_pT_Bin_23)
(Q2_y_Bin_1)-(z_pT_Bin_30), (Q2_y_Bin_1)-(z_pT_Bin_31), (Q2_y_Bin_1)-(z_pT_Bin_4)
(Q2_y_Bin_1)-(z_pT_Bin_5), (Q2_y_Bin_1)-(z_pT_Bin_6), (Q2_y_Bin_1)-(z_pT_Bin_7)
(Q2_y_Bin_1)-(z_pT_Bin_8), (Q2_y_Bin_1)-(z_pT_Bin_9), (Q2_y_Bin_10)-(z_pT_Bin_1)
(Q2_y_Bin_10)-(z_pT_Bin_2), (Q2_y_Bin_10)-(z_pT_Bin_26), (Q2_y_Bin_10)-(z_pT_Bin_3)
(Q2_y_Bin_10)-(z_pT_Bin_31), (Q2_y_Bin_10)-(z_pT_Bin_32), (Q2_y_Bin_10)-(z_pT_Bin_4)
(Q2_y_Bin_10)-(z_pT_Bin_5), (Q2_y_Bin_10)-(z_pT_Bin_6), (Q2_y_Bin_10)-(z_pT_Bin_7)
(Q2_y_Bin_10)-(z_pT_Bin_9), (Q2_y_Bin_11)-(z_pT_Bin_1), (Q2_y_Bin_11)-(z_pT_Bin_10)
(Q2_y_Bin_11)-(z_pT_Bin_2), (Q2_y_Bin_11)-(z_pT_Bin_20), (Q2_y_Bin_11)-(z_pT_Bin_21)
(Q2_y_Bin_11)-(z_pT_Bin_22), (Q2_y_Bin_11)-(z_pT_Bin_23), (Q2_y_Bin_11)-(z_pT_Bin_24)
(Q2_y_Bin_11)-(z_pT_Bin_3), (Q2_y_Bin_11)-(z_pT_Bin_6), (Q2_y_Bin_12)-(z_pT_Bin_11)
(Q2_y_Bin_12)-(z_pT_Bin_16), (Q2_y_Bin_12)-(z_pT_Bin_21) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission]
(Q2_y_Bin_12)-(z_pT_Bin_6), (Q2_y_Bin_12)-(z_pT_Bin_7), (Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_13)-(z_pT_Bin_1), (Q2_y_Bin_13)-(z_pT_Bin_2), (Q2_y_Bin_13)-(z_pT_Bin_4)
(Q2_y_Bin_14)-(z_pT_Bin_2), (Q2_y_Bin_14)-(z_pT_Bin_32), (Q2_y_Bin_14)-(z_pT_Bin_4)
(Q2_y_Bin_14)-(z_pT_Bin_5), (Q2_y_Bin_15)-(z_pT_Bin_1), (Q2_y_Bin_15)-(z_pT_Bin_15)
(Q2_y_Bin_15)-(z_pT_Bin_2), (Q2_y_Bin_15)-(z_pT_Bin_21), (Q2_y_Bin_15)-(z_pT_Bin_22)
(Q2_y_Bin_15)-(z_pT_Bin_23), (Q2_y_Bin_15)-(z_pT_Bin_6), (Q2_y_Bin_15)-(z_pT_Bin_9)
(Q2_y_Bin_16)-(z_pT_Bin_6), (Q2_y_Bin_17)-(z_pT_Bin_4), (Q2_y_Bin_2)-(z_pT_Bin_1)
(Q2_y_Bin_2)-(z_pT_Bin_10), (Q2_y_Bin_2)-(z_pT_Bin_11), (Q2_y_Bin_2)-(z_pT_Bin_13)
(Q2_y_Bin_2)-(z_pT_Bin_14), (Q2_y_Bin_2)-(z_pT_Bin_15), (Q2_y_Bin_2)-(z_pT_Bin_16)
(Q2_y_Bin_2)-(z_pT_Bin_19), (Q2_y_Bin_2)-(z_pT_Bin_2), (Q2_y_Bin_2)-(z_pT_Bin_20)
(Q2_y_Bin_2)-(z_pT_Bin_25), (Q2_y_Bin_2)-(z_pT_Bin_26), (Q2_y_Bin_2)-(z_pT_Bin_3)
(Q2_y_Bin_2)-(z_pT_Bin_32), (Q2_y_Bin_2)-(z_pT_Bin_33), (Q2_y_Bin_2)-(z_pT_Bin_34)
(Q2_y_Bin_2)-(z_pT_Bin_4), (Q2_y_Bin_2)-(z_pT_Bin_5), (Q2_y_Bin_2)-(z_pT_Bin_6)
(Q2_y_Bin_2)-(z_pT_Bin_7), (Q2_y_Bin_2)-(z_pT_Bin_8), (Q2_y_Bin_2)-(z_pT_Bin_9)
(Q2_y_Bin_3)-(z_pT_Bin_1), (Q2_y_Bin_3)-(z_pT_Bin_11), (Q2_y_Bin_3)-(z_pT_Bin_12)
(Q2_y_Bin_3)-(z_pT_Bin_13), (Q2_y_Bin_3)-(z_pT_Bin_14), (Q2_y_Bin_3)-(z_pT_Bin_16)
(Q2_y_Bin_3)-(z_pT_Bin_17), (Q2_y_Bin_3)-(z_pT_Bin_18), (Q2_y_Bin_3)-(z_pT_Bin_19)
(Q2_y_Bin_3)-(z_pT_Bin_2), (Q2_y_Bin_3)-(z_pT_Bin_20), (Q2_y_Bin_3)-(z_pT_Bin_21)
(Q2_y_Bin_3)-(z_pT_Bin_22), (Q2_y_Bin_3)-(z_pT_Bin_23), (Q2_y_Bin_3)-(z_pT_Bin_24)
(Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_7), (Q2_y_Bin_3)-(z_pT_Bin_8)
(Q2_y_Bin_3)-(z_pT_Bin_9), (Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_14)
(Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_19)
(Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_26), (Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission], (Q2_y_Bin_5)-(z_pT_Bin_1), (Q2_y_Bin_5)-(z_pT_Bin_10)
(Q2_y_Bin_5)-(z_pT_Bin_13), (Q2_y_Bin_5)-(z_pT_Bin_14), (Q2_y_Bin_5)-(z_pT_Bin_15)
(Q2_y_Bin_5)-(z_pT_Bin_19), (Q2_y_Bin_5)-(z_pT_Bin_20), (Q2_y_Bin_5)-(z_pT_Bin_25)
(Q2_y_Bin_5)-(z_pT_Bin_3), (Q2_y_Bin_5)-(z_pT_Bin_31), (Q2_y_Bin_5)-(z_pT_Bin_32)
(Q2_y_Bin_5)-(z_pT_Bin_4), (Q2_y_Bin_5)-(z_pT_Bin_5), (Q2_y_Bin_5)-(z_pT_Bin_6)
(Q2_y_Bin_5)-(z_pT_Bin_7), (Q2_y_Bin_5)-(z_pT_Bin_8), (Q2_y_Bin_5)-(z_pT_Bin_9)
(Q2_y_Bin_6)-(z_pT_Bin_1), (Q2_y_Bin_6)-(z_pT_Bin_10), (Q2_y_Bin_6)-(z_pT_Bin_14)
(Q2_y_Bin_6)-(z_pT_Bin_19), (Q2_y_Bin_6)-(z_pT_Bin_2), (Q2_y_Bin_6)-(z_pT_Bin_20)
(Q2_y_Bin_6)-(z_pT_Bin_26), (Q2_y_Bin_6)-(z_pT_Bin_27), (Q2_y_Bin_6)-(z_pT_Bin_28)
(Q2_y_Bin_6)-(z_pT_Bin_3), (Q2_y_Bin_6)-(z_pT_Bin_4), (Q2_y_Bin_6)-(z_pT_Bin_5)
(Q2_y_Bin_6)-(z_pT_Bin_6), (Q2_y_Bin_6)-(z_pT_Bin_7), (Q2_y_Bin_7)-(z_pT_Bin_1)
(Q2_y_Bin_7)-(z_pT_Bin_10), (Q2_y_Bin_7)-(z_pT_Bin_11), (Q2_y_Bin_7)-(z_pT_Bin_12)
(Q2_y_Bin_7)-(z_pT_Bin_13), (Q2_y_Bin_7)-(z_pT_Bin_15), (Q2_y_Bin_7)-(z_pT_Bin_16)
(Q2_y_Bin_7)-(z_pT_Bin_17), (Q2_y_Bin_7)-(z_pT_Bin_2), (Q2_y_Bin_7)-(z_pT_Bin_21)
(Q2_y_Bin_7)-(z_pT_Bin_24), (Q2_y_Bin_7)-(z_pT_Bin_26), (Q2_y_Bin_7)-(z_pT_Bin_27)
(Q2_y_Bin_7)-(z_pT_Bin_29), (Q2_y_Bin_7)-(z_pT_Bin_34), (Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission]
(Q2_y_Bin_7)-(z_pT_Bin_7), (Q2_y_Bin_7)-(z_pT_Bin_8), (Q2_y_Bin_7)-(z_pT_Bin_9)
(Q2_y_Bin_8)-(z_pT_Bin_11), (Q2_y_Bin_8)-(z_pT_Bin_12), (Q2_y_Bin_8)-(z_pT_Bin_13)
(Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16), (Q2_y_Bin_8)-(z_pT_Bin_18)
(Q2_y_Bin_8)-(z_pT_Bin_19), (Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_21)
(Q2_y_Bin_8)-(z_pT_Bin_23), (Q2_y_Bin_8)-(z_pT_Bin_24), (Q2_y_Bin_8)-(z_pT_Bin_26)
(Q2_y_Bin_8)-(z_pT_Bin_28), (Q2_y_Bin_8)-(z_pT_Bin_29), (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_9)-(z_pT_Bin_1), (Q2_y_Bin_9)-(z_pT_Bin_10), (Q2_y_Bin_9)-(z_pT_Bin_15)
(Q2_y_Bin_9)-(z_pT_Bin_16), (Q2_y_Bin_9)-(z_pT_Bin_2), (Q2_y_Bin_9)-(z_pT_Bin_29)
(Q2_y_Bin_9)-(z_pT_Bin_3), (Q2_y_Bin_9)-(z_pT_Bin_30), (Q2_y_Bin_9)-(z_pT_Bin_4)
(Q2_y_Bin_9)-(z_pT_Bin_5), (Q2_y_Bin_9)-(z_pT_Bin_6), (Q2_y_Bin_9)-(z_pT_Bin_8)

#### 135°

The rule fails every assessable manual exclusion (31).

Manually excluded but passes:

None.

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_1), (Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_15)
(Q2_y_Bin_1)-(z_pT_Bin_16), (Q2_y_Bin_1)-(z_pT_Bin_22), (Q2_y_Bin_1)-(z_pT_Bin_30)
(Q2_y_Bin_1)-(z_pT_Bin_31), (Q2_y_Bin_1)-(z_pT_Bin_4), (Q2_y_Bin_1)-(z_pT_Bin_5)
(Q2_y_Bin_1)-(z_pT_Bin_6), (Q2_y_Bin_1)-(z_pT_Bin_7), (Q2_y_Bin_1)-(z_pT_Bin_8)
(Q2_y_Bin_1)-(z_pT_Bin_9), (Q2_y_Bin_10)-(z_pT_Bin_1), (Q2_y_Bin_10)-(z_pT_Bin_2)
(Q2_y_Bin_10)-(z_pT_Bin_3), (Q2_y_Bin_10)-(z_pT_Bin_31), (Q2_y_Bin_10)-(z_pT_Bin_32)
(Q2_y_Bin_10)-(z_pT_Bin_4), (Q2_y_Bin_10)-(z_pT_Bin_5), (Q2_y_Bin_10)-(z_pT_Bin_6)
(Q2_y_Bin_10)-(z_pT_Bin_7), (Q2_y_Bin_11)-(z_pT_Bin_1), (Q2_y_Bin_11)-(z_pT_Bin_2)
(Q2_y_Bin_11)-(z_pT_Bin_21), (Q2_y_Bin_11)-(z_pT_Bin_22), (Q2_y_Bin_11)-(z_pT_Bin_23)
(Q2_y_Bin_11)-(z_pT_Bin_24), (Q2_y_Bin_11)-(z_pT_Bin_3), (Q2_y_Bin_11)-(z_pT_Bin_6)
(Q2_y_Bin_12)-(z_pT_Bin_11), (Q2_y_Bin_12)-(z_pT_Bin_21) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission]
(Q2_y_Bin_12)-(z_pT_Bin_6), (Q2_y_Bin_12)-(z_pT_Bin_7), (Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_13)-(z_pT_Bin_1), (Q2_y_Bin_13)-(z_pT_Bin_2), (Q2_y_Bin_14)-(z_pT_Bin_2)
(Q2_y_Bin_14)-(z_pT_Bin_4), (Q2_y_Bin_14)-(z_pT_Bin_5), (Q2_y_Bin_15)-(z_pT_Bin_1)
(Q2_y_Bin_15)-(z_pT_Bin_15), (Q2_y_Bin_15)-(z_pT_Bin_2), (Q2_y_Bin_15)-(z_pT_Bin_22)
(Q2_y_Bin_15)-(z_pT_Bin_23), (Q2_y_Bin_15)-(z_pT_Bin_9), (Q2_y_Bin_16)-(z_pT_Bin_6)
(Q2_y_Bin_17)-(z_pT_Bin_4), (Q2_y_Bin_2)-(z_pT_Bin_1), (Q2_y_Bin_2)-(z_pT_Bin_10)
(Q2_y_Bin_2)-(z_pT_Bin_13), (Q2_y_Bin_2)-(z_pT_Bin_14), (Q2_y_Bin_2)-(z_pT_Bin_15)
(Q2_y_Bin_2)-(z_pT_Bin_16), (Q2_y_Bin_2)-(z_pT_Bin_19), (Q2_y_Bin_2)-(z_pT_Bin_2)
(Q2_y_Bin_2)-(z_pT_Bin_20), (Q2_y_Bin_2)-(z_pT_Bin_25), (Q2_y_Bin_2)-(z_pT_Bin_3)
(Q2_y_Bin_2)-(z_pT_Bin_32), (Q2_y_Bin_2)-(z_pT_Bin_34), (Q2_y_Bin_2)-(z_pT_Bin_4)
(Q2_y_Bin_2)-(z_pT_Bin_5), (Q2_y_Bin_2)-(z_pT_Bin_6), (Q2_y_Bin_2)-(z_pT_Bin_7)
(Q2_y_Bin_2)-(z_pT_Bin_8), (Q2_y_Bin_2)-(z_pT_Bin_9), (Q2_y_Bin_3)-(z_pT_Bin_1)
(Q2_y_Bin_3)-(z_pT_Bin_11), (Q2_y_Bin_3)-(z_pT_Bin_12), (Q2_y_Bin_3)-(z_pT_Bin_13)
(Q2_y_Bin_3)-(z_pT_Bin_14), (Q2_y_Bin_3)-(z_pT_Bin_16), (Q2_y_Bin_3)-(z_pT_Bin_17)
(Q2_y_Bin_3)-(z_pT_Bin_18), (Q2_y_Bin_3)-(z_pT_Bin_19), (Q2_y_Bin_3)-(z_pT_Bin_2)
(Q2_y_Bin_3)-(z_pT_Bin_20), (Q2_y_Bin_3)-(z_pT_Bin_21), (Q2_y_Bin_3)-(z_pT_Bin_24)
(Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_7), (Q2_y_Bin_3)-(z_pT_Bin_8)
(Q2_y_Bin_3)-(z_pT_Bin_9), (Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_14)
(Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_19)
(Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_26), (Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission], (Q2_y_Bin_5)-(z_pT_Bin_1), (Q2_y_Bin_5)-(z_pT_Bin_10)
(Q2_y_Bin_5)-(z_pT_Bin_13), (Q2_y_Bin_5)-(z_pT_Bin_14), (Q2_y_Bin_5)-(z_pT_Bin_15)
(Q2_y_Bin_5)-(z_pT_Bin_19), (Q2_y_Bin_5)-(z_pT_Bin_20), (Q2_y_Bin_5)-(z_pT_Bin_25)
(Q2_y_Bin_5)-(z_pT_Bin_3), (Q2_y_Bin_5)-(z_pT_Bin_31), (Q2_y_Bin_5)-(z_pT_Bin_32)
(Q2_y_Bin_5)-(z_pT_Bin_4), (Q2_y_Bin_5)-(z_pT_Bin_5), (Q2_y_Bin_5)-(z_pT_Bin_6)
(Q2_y_Bin_5)-(z_pT_Bin_7), (Q2_y_Bin_5)-(z_pT_Bin_8), (Q2_y_Bin_5)-(z_pT_Bin_9)
(Q2_y_Bin_6)-(z_pT_Bin_1), (Q2_y_Bin_6)-(z_pT_Bin_10), (Q2_y_Bin_6)-(z_pT_Bin_14)
(Q2_y_Bin_6)-(z_pT_Bin_2), (Q2_y_Bin_6)-(z_pT_Bin_20), (Q2_y_Bin_6)-(z_pT_Bin_26)
(Q2_y_Bin_6)-(z_pT_Bin_27), (Q2_y_Bin_6)-(z_pT_Bin_28), (Q2_y_Bin_6)-(z_pT_Bin_3)
(Q2_y_Bin_6)-(z_pT_Bin_4), (Q2_y_Bin_6)-(z_pT_Bin_5), (Q2_y_Bin_6)-(z_pT_Bin_6)
(Q2_y_Bin_6)-(z_pT_Bin_7), (Q2_y_Bin_7)-(z_pT_Bin_1), (Q2_y_Bin_7)-(z_pT_Bin_10)
(Q2_y_Bin_7)-(z_pT_Bin_11), (Q2_y_Bin_7)-(z_pT_Bin_12), (Q2_y_Bin_7)-(z_pT_Bin_13)
(Q2_y_Bin_7)-(z_pT_Bin_15), (Q2_y_Bin_7)-(z_pT_Bin_16), (Q2_y_Bin_7)-(z_pT_Bin_17)
(Q2_y_Bin_7)-(z_pT_Bin_2), (Q2_y_Bin_7)-(z_pT_Bin_21), (Q2_y_Bin_7)-(z_pT_Bin_24)
(Q2_y_Bin_7)-(z_pT_Bin_26), (Q2_y_Bin_7)-(z_pT_Bin_27), (Q2_y_Bin_7)-(z_pT_Bin_29)
(Q2_y_Bin_7)-(z_pT_Bin_34), (Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_7)-(z_pT_Bin_7)
(Q2_y_Bin_8)-(z_pT_Bin_11), (Q2_y_Bin_8)-(z_pT_Bin_13), (Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_16), (Q2_y_Bin_8)-(z_pT_Bin_19), (Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_21), (Q2_y_Bin_8)-(z_pT_Bin_23), (Q2_y_Bin_8)-(z_pT_Bin_24)
(Q2_y_Bin_8)-(z_pT_Bin_28), (Q2_y_Bin_8)-(z_pT_Bin_29), (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_9)-(z_pT_Bin_1), (Q2_y_Bin_9)-(z_pT_Bin_2), (Q2_y_Bin_9)-(z_pT_Bin_29)
(Q2_y_Bin_9)-(z_pT_Bin_3), (Q2_y_Bin_9)-(z_pT_Bin_4), (Q2_y_Bin_9)-(z_pT_Bin_5)
(Q2_y_Bin_9)-(z_pT_Bin_8)

#### 150°

The rule does not fail every assessable manual exclusion: 1 of 31 pass.

Manually excluded but passes:

(Q2_y_Bin_6)-(z_pT_Bin_8)

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_1), (Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_15)
(Q2_y_Bin_1)-(z_pT_Bin_16), (Q2_y_Bin_1)-(z_pT_Bin_22), (Q2_y_Bin_1)-(z_pT_Bin_30)
(Q2_y_Bin_1)-(z_pT_Bin_4), (Q2_y_Bin_1)-(z_pT_Bin_5), (Q2_y_Bin_1)-(z_pT_Bin_6)
(Q2_y_Bin_1)-(z_pT_Bin_8), (Q2_y_Bin_1)-(z_pT_Bin_9), (Q2_y_Bin_10)-(z_pT_Bin_2)
(Q2_y_Bin_10)-(z_pT_Bin_3), (Q2_y_Bin_10)-(z_pT_Bin_32), (Q2_y_Bin_10)-(z_pT_Bin_4)
(Q2_y_Bin_10)-(z_pT_Bin_5), (Q2_y_Bin_10)-(z_pT_Bin_6), (Q2_y_Bin_11)-(z_pT_Bin_1)
(Q2_y_Bin_11)-(z_pT_Bin_2), (Q2_y_Bin_11)-(z_pT_Bin_22), (Q2_y_Bin_11)-(z_pT_Bin_23)
(Q2_y_Bin_11)-(z_pT_Bin_24), (Q2_y_Bin_11)-(z_pT_Bin_3), (Q2_y_Bin_11)-(z_pT_Bin_6)
(Q2_y_Bin_12)-(z_pT_Bin_11), (Q2_y_Bin_12)-(z_pT_Bin_21) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission]
(Q2_y_Bin_12)-(z_pT_Bin_6), (Q2_y_Bin_12)-(z_pT_Bin_7), (Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_13)-(z_pT_Bin_1), (Q2_y_Bin_14)-(z_pT_Bin_5), (Q2_y_Bin_15)-(z_pT_Bin_1)
(Q2_y_Bin_15)-(z_pT_Bin_15), (Q2_y_Bin_15)-(z_pT_Bin_2), (Q2_y_Bin_15)-(z_pT_Bin_22)
(Q2_y_Bin_15)-(z_pT_Bin_23), (Q2_y_Bin_2)-(z_pT_Bin_1), (Q2_y_Bin_2)-(z_pT_Bin_10)
(Q2_y_Bin_2)-(z_pT_Bin_14), (Q2_y_Bin_2)-(z_pT_Bin_15), (Q2_y_Bin_2)-(z_pT_Bin_19)
(Q2_y_Bin_2)-(z_pT_Bin_2), (Q2_y_Bin_2)-(z_pT_Bin_20), (Q2_y_Bin_2)-(z_pT_Bin_25)
(Q2_y_Bin_2)-(z_pT_Bin_3), (Q2_y_Bin_2)-(z_pT_Bin_32), (Q2_y_Bin_2)-(z_pT_Bin_4)
(Q2_y_Bin_2)-(z_pT_Bin_5), (Q2_y_Bin_2)-(z_pT_Bin_6), (Q2_y_Bin_2)-(z_pT_Bin_7)
(Q2_y_Bin_2)-(z_pT_Bin_8), (Q2_y_Bin_2)-(z_pT_Bin_9), (Q2_y_Bin_3)-(z_pT_Bin_1)
(Q2_y_Bin_3)-(z_pT_Bin_11), (Q2_y_Bin_3)-(z_pT_Bin_12), (Q2_y_Bin_3)-(z_pT_Bin_13)
(Q2_y_Bin_3)-(z_pT_Bin_16), (Q2_y_Bin_3)-(z_pT_Bin_2), (Q2_y_Bin_3)-(z_pT_Bin_20)
(Q2_y_Bin_3)-(z_pT_Bin_21), (Q2_y_Bin_3)-(z_pT_Bin_24), (Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_7), (Q2_y_Bin_3)-(z_pT_Bin_9), (Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_14), (Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_19), (Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission], (Q2_y_Bin_5)-(z_pT_Bin_1), (Q2_y_Bin_5)-(z_pT_Bin_10)
(Q2_y_Bin_5)-(z_pT_Bin_13), (Q2_y_Bin_5)-(z_pT_Bin_14), (Q2_y_Bin_5)-(z_pT_Bin_25)
(Q2_y_Bin_5)-(z_pT_Bin_3), (Q2_y_Bin_5)-(z_pT_Bin_31), (Q2_y_Bin_5)-(z_pT_Bin_32)
(Q2_y_Bin_5)-(z_pT_Bin_4), (Q2_y_Bin_5)-(z_pT_Bin_5), (Q2_y_Bin_5)-(z_pT_Bin_6)
(Q2_y_Bin_5)-(z_pT_Bin_7), (Q2_y_Bin_5)-(z_pT_Bin_8), (Q2_y_Bin_5)-(z_pT_Bin_9)
(Q2_y_Bin_6)-(z_pT_Bin_1), (Q2_y_Bin_6)-(z_pT_Bin_2), (Q2_y_Bin_6)-(z_pT_Bin_20)
(Q2_y_Bin_6)-(z_pT_Bin_26), (Q2_y_Bin_6)-(z_pT_Bin_27), (Q2_y_Bin_6)-(z_pT_Bin_3)
(Q2_y_Bin_6)-(z_pT_Bin_4), (Q2_y_Bin_6)-(z_pT_Bin_5), (Q2_y_Bin_6)-(z_pT_Bin_7)
(Q2_y_Bin_7)-(z_pT_Bin_1), (Q2_y_Bin_7)-(z_pT_Bin_11), (Q2_y_Bin_7)-(z_pT_Bin_12)
(Q2_y_Bin_7)-(z_pT_Bin_13), (Q2_y_Bin_7)-(z_pT_Bin_2), (Q2_y_Bin_7)-(z_pT_Bin_21)
(Q2_y_Bin_7)-(z_pT_Bin_24), (Q2_y_Bin_7)-(z_pT_Bin_34), (Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission]
(Q2_y_Bin_7)-(z_pT_Bin_7), (Q2_y_Bin_8)-(z_pT_Bin_11), (Q2_y_Bin_8)-(z_pT_Bin_13)
(Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16), (Q2_y_Bin_8)-(z_pT_Bin_19)
(Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_21), (Q2_y_Bin_8)-(z_pT_Bin_24)
(Q2_y_Bin_8)-(z_pT_Bin_28), (Q2_y_Bin_8)-(z_pT_Bin_29), (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_9)-(z_pT_Bin_1), (Q2_y_Bin_9)-(z_pT_Bin_2), (Q2_y_Bin_9)-(z_pT_Bin_29)
(Q2_y_Bin_9)-(z_pT_Bin_3), (Q2_y_Bin_9)-(z_pT_Bin_4), (Q2_y_Bin_9)-(z_pT_Bin_5)

#### 180°

The rule does not fail every assessable manual exclusion: 3 of 31 pass.

Manually excluded but passes:

(Q2_y_Bin_3)-(z_pT_Bin_15), (Q2_y_Bin_6)-(z_pT_Bin_8), (Q2_y_Bin_6)-(z_pT_Bin_9)

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_1), (Q2_y_Bin_1)-(z_pT_Bin_15), (Q2_y_Bin_1)-(z_pT_Bin_30)
(Q2_y_Bin_1)-(z_pT_Bin_4), (Q2_y_Bin_1)-(z_pT_Bin_8), (Q2_y_Bin_1)-(z_pT_Bin_9)
(Q2_y_Bin_10)-(z_pT_Bin_6), (Q2_y_Bin_11)-(z_pT_Bin_22), (Q2_y_Bin_11)-(z_pT_Bin_23)
(Q2_y_Bin_11)-(z_pT_Bin_24), (Q2_y_Bin_11)-(z_pT_Bin_3), (Q2_y_Bin_12)-(z_pT_Bin_11)
(Q2_y_Bin_12)-(z_pT_Bin_21) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_6)
(Q2_y_Bin_12)-(z_pT_Bin_7), (Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_14)-(z_pT_Bin_5)
(Q2_y_Bin_15)-(z_pT_Bin_15), (Q2_y_Bin_15)-(z_pT_Bin_2), (Q2_y_Bin_2)-(z_pT_Bin_1)
(Q2_y_Bin_2)-(z_pT_Bin_2), (Q2_y_Bin_2)-(z_pT_Bin_3), (Q2_y_Bin_2)-(z_pT_Bin_4)
(Q2_y_Bin_2)-(z_pT_Bin_5), (Q2_y_Bin_2)-(z_pT_Bin_6), (Q2_y_Bin_2)-(z_pT_Bin_7)
(Q2_y_Bin_2)-(z_pT_Bin_9), (Q2_y_Bin_3)-(z_pT_Bin_1), (Q2_y_Bin_3)-(z_pT_Bin_13)
(Q2_y_Bin_3)-(z_pT_Bin_2), (Q2_y_Bin_3)-(z_pT_Bin_24), (Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_7), (Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_19), (Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission], (Q2_y_Bin_5)-(z_pT_Bin_1)
(Q2_y_Bin_5)-(z_pT_Bin_3), (Q2_y_Bin_5)-(z_pT_Bin_31), (Q2_y_Bin_5)-(z_pT_Bin_4)
(Q2_y_Bin_5)-(z_pT_Bin_5), (Q2_y_Bin_5)-(z_pT_Bin_7), (Q2_y_Bin_6)-(z_pT_Bin_26)
(Q2_y_Bin_7)-(z_pT_Bin_12), (Q2_y_Bin_7)-(z_pT_Bin_13), (Q2_y_Bin_7)-(z_pT_Bin_2)
(Q2_y_Bin_7)-(z_pT_Bin_24), (Q2_y_Bin_7)-(z_pT_Bin_34), (Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_11), (Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16)
(Q2_y_Bin_8)-(z_pT_Bin_19), (Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_24)
(Q2_y_Bin_8)-(z_pT_Bin_29), (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_9)-(z_pT_Bin_1)
(Q2_y_Bin_9)-(z_pT_Bin_2), (Q2_y_Bin_9)-(z_pT_Bin_29), (Q2_y_Bin_9)-(z_pT_Bin_3)
(Q2_y_Bin_9)-(z_pT_Bin_4)

### eS3o

Manual list entries: 40. Fit-quality omissions relative to the nominal acceptance bins: 34. Comparisons the budget still keeps: 382.

#### 90°

The rule fails every assessable manual exclusion (40).

Manually excluded but passes:

None.

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_1), (Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_11)
(Q2_y_Bin_1)-(z_pT_Bin_16), (Q2_y_Bin_1)-(z_pT_Bin_17), (Q2_y_Bin_1)-(z_pT_Bin_2)
(Q2_y_Bin_1)-(z_pT_Bin_23), (Q2_y_Bin_1)-(z_pT_Bin_3), (Q2_y_Bin_1)-(z_pT_Bin_31)
(Q2_y_Bin_1)-(z_pT_Bin_32), (Q2_y_Bin_1)-(z_pT_Bin_4), (Q2_y_Bin_1)-(z_pT_Bin_5)
(Q2_y_Bin_1)-(z_pT_Bin_6), (Q2_y_Bin_1)-(z_pT_Bin_7), (Q2_y_Bin_1)-(z_pT_Bin_8)
(Q2_y_Bin_1)-(z_pT_Bin_9), (Q2_y_Bin_10)-(z_pT_Bin_1), (Q2_y_Bin_10)-(z_pT_Bin_10)
(Q2_y_Bin_10)-(z_pT_Bin_15), (Q2_y_Bin_10)-(z_pT_Bin_2), (Q2_y_Bin_10)-(z_pT_Bin_20)
(Q2_y_Bin_10)-(z_pT_Bin_26), (Q2_y_Bin_10)-(z_pT_Bin_3), (Q2_y_Bin_10)-(z_pT_Bin_31)
(Q2_y_Bin_10)-(z_pT_Bin_32), (Q2_y_Bin_10)-(z_pT_Bin_4), (Q2_y_Bin_10)-(z_pT_Bin_5)
(Q2_y_Bin_10)-(z_pT_Bin_6), (Q2_y_Bin_10)-(z_pT_Bin_7), (Q2_y_Bin_10)-(z_pT_Bin_9)
(Q2_y_Bin_11)-(z_pT_Bin_1), (Q2_y_Bin_11)-(z_pT_Bin_10), (Q2_y_Bin_11)-(z_pT_Bin_13)
(Q2_y_Bin_11)-(z_pT_Bin_15), (Q2_y_Bin_11)-(z_pT_Bin_18), (Q2_y_Bin_11)-(z_pT_Bin_2)
(Q2_y_Bin_11)-(z_pT_Bin_20), (Q2_y_Bin_11)-(z_pT_Bin_21), (Q2_y_Bin_11)-(z_pT_Bin_23)
(Q2_y_Bin_11)-(z_pT_Bin_3), (Q2_y_Bin_11)-(z_pT_Bin_6), (Q2_y_Bin_11)-(z_pT_Bin_9)
(Q2_y_Bin_12)-(z_pT_Bin_11), (Q2_y_Bin_12)-(z_pT_Bin_13), (Q2_y_Bin_12)-(z_pT_Bin_16)
(Q2_y_Bin_12)-(z_pT_Bin_18), (Q2_y_Bin_12)-(z_pT_Bin_22), (Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_13)-(z_pT_Bin_1), (Q2_y_Bin_13)-(z_pT_Bin_12), (Q2_y_Bin_13)-(z_pT_Bin_2)
(Q2_y_Bin_13)-(z_pT_Bin_26), (Q2_y_Bin_13)-(z_pT_Bin_3), (Q2_y_Bin_13)-(z_pT_Bin_4)
(Q2_y_Bin_13)-(z_pT_Bin_5), (Q2_y_Bin_13)-(z_pT_Bin_7), (Q2_y_Bin_13)-(z_pT_Bin_8)
(Q2_y_Bin_14)-(z_pT_Bin_1), (Q2_y_Bin_14)-(z_pT_Bin_2), (Q2_y_Bin_14)-(z_pT_Bin_32)
(Q2_y_Bin_14)-(z_pT_Bin_4), (Q2_y_Bin_14)-(z_pT_Bin_5), (Q2_y_Bin_15)-(z_pT_Bin_1)
(Q2_y_Bin_15)-(z_pT_Bin_15), (Q2_y_Bin_15)-(z_pT_Bin_19), (Q2_y_Bin_15)-(z_pT_Bin_2)
(Q2_y_Bin_15)-(z_pT_Bin_22), (Q2_y_Bin_15)-(z_pT_Bin_23), (Q2_y_Bin_15)-(z_pT_Bin_24)
(Q2_y_Bin_15)-(z_pT_Bin_9), (Q2_y_Bin_16)-(z_pT_Bin_3), (Q2_y_Bin_16)-(z_pT_Bin_4)
(Q2_y_Bin_16)-(z_pT_Bin_5), (Q2_y_Bin_16)-(z_pT_Bin_6), (Q2_y_Bin_16)-(z_pT_Bin_9)
(Q2_y_Bin_17)-(z_pT_Bin_4), (Q2_y_Bin_2)-(z_pT_Bin_1), (Q2_y_Bin_2)-(z_pT_Bin_10)
(Q2_y_Bin_2)-(z_pT_Bin_11), (Q2_y_Bin_2)-(z_pT_Bin_12), (Q2_y_Bin_2)-(z_pT_Bin_14)
(Q2_y_Bin_2)-(z_pT_Bin_15), (Q2_y_Bin_2)-(z_pT_Bin_16), (Q2_y_Bin_2)-(z_pT_Bin_2)
(Q2_y_Bin_2)-(z_pT_Bin_20), (Q2_y_Bin_2)-(z_pT_Bin_21), (Q2_y_Bin_2)-(z_pT_Bin_22)
(Q2_y_Bin_2)-(z_pT_Bin_25), (Q2_y_Bin_2)-(z_pT_Bin_26), (Q2_y_Bin_2)-(z_pT_Bin_27)
(Q2_y_Bin_2)-(z_pT_Bin_28), (Q2_y_Bin_2)-(z_pT_Bin_3), (Q2_y_Bin_2)-(z_pT_Bin_32)
(Q2_y_Bin_2)-(z_pT_Bin_33), (Q2_y_Bin_2)-(z_pT_Bin_34), (Q2_y_Bin_2)-(z_pT_Bin_4)
(Q2_y_Bin_2)-(z_pT_Bin_5), (Q2_y_Bin_2)-(z_pT_Bin_6), (Q2_y_Bin_2)-(z_pT_Bin_7)
(Q2_y_Bin_2)-(z_pT_Bin_8), (Q2_y_Bin_2)-(z_pT_Bin_9), (Q2_y_Bin_3)-(z_pT_Bin_1)
(Q2_y_Bin_3)-(z_pT_Bin_11), (Q2_y_Bin_3)-(z_pT_Bin_12), (Q2_y_Bin_3)-(z_pT_Bin_13)
(Q2_y_Bin_3)-(z_pT_Bin_14), (Q2_y_Bin_3)-(z_pT_Bin_15), (Q2_y_Bin_3)-(z_pT_Bin_16)
(Q2_y_Bin_3)-(z_pT_Bin_17), (Q2_y_Bin_3)-(z_pT_Bin_18), (Q2_y_Bin_3)-(z_pT_Bin_19)
(Q2_y_Bin_3)-(z_pT_Bin_2), (Q2_y_Bin_3)-(z_pT_Bin_21), (Q2_y_Bin_3)-(z_pT_Bin_22)
(Q2_y_Bin_3)-(z_pT_Bin_23), (Q2_y_Bin_3)-(z_pT_Bin_24), (Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_7), (Q2_y_Bin_3)-(z_pT_Bin_8), (Q2_y_Bin_3)-(z_pT_Bin_9)
(Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_13), (Q2_y_Bin_4)-(z_pT_Bin_14)
(Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_20)
(Q2_y_Bin_4)-(z_pT_Bin_21), (Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_26)
(Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission], (Q2_y_Bin_5)-(z_pT_Bin_1)
(Q2_y_Bin_5)-(z_pT_Bin_10), (Q2_y_Bin_5)-(z_pT_Bin_11), (Q2_y_Bin_5)-(z_pT_Bin_13)
(Q2_y_Bin_5)-(z_pT_Bin_14), (Q2_y_Bin_5)-(z_pT_Bin_15), (Q2_y_Bin_5)-(z_pT_Bin_16)
(Q2_y_Bin_5)-(z_pT_Bin_19), (Q2_y_Bin_5)-(z_pT_Bin_20), (Q2_y_Bin_5)-(z_pT_Bin_25)
(Q2_y_Bin_5)-(z_pT_Bin_26), (Q2_y_Bin_5)-(z_pT_Bin_3), (Q2_y_Bin_5)-(z_pT_Bin_32)
(Q2_y_Bin_5)-(z_pT_Bin_4), (Q2_y_Bin_5)-(z_pT_Bin_5), (Q2_y_Bin_5)-(z_pT_Bin_6)
(Q2_y_Bin_5)-(z_pT_Bin_7), (Q2_y_Bin_5)-(z_pT_Bin_8), (Q2_y_Bin_5)-(z_pT_Bin_9)
(Q2_y_Bin_6)-(z_pT_Bin_1), (Q2_y_Bin_6)-(z_pT_Bin_10), (Q2_y_Bin_6)-(z_pT_Bin_11)
(Q2_y_Bin_6)-(z_pT_Bin_13), (Q2_y_Bin_6)-(z_pT_Bin_14), (Q2_y_Bin_6)-(z_pT_Bin_15)
(Q2_y_Bin_6)-(z_pT_Bin_19), (Q2_y_Bin_6)-(z_pT_Bin_2), (Q2_y_Bin_6)-(z_pT_Bin_20)
(Q2_y_Bin_6)-(z_pT_Bin_27), (Q2_y_Bin_6)-(z_pT_Bin_28), (Q2_y_Bin_6)-(z_pT_Bin_3)
(Q2_y_Bin_6)-(z_pT_Bin_4), (Q2_y_Bin_6)-(z_pT_Bin_5), (Q2_y_Bin_6)-(z_pT_Bin_6)
(Q2_y_Bin_6)-(z_pT_Bin_7), (Q2_y_Bin_6)-(z_pT_Bin_8), (Q2_y_Bin_6)-(z_pT_Bin_9)
(Q2_y_Bin_7)-(z_pT_Bin_1), (Q2_y_Bin_7)-(z_pT_Bin_10), (Q2_y_Bin_7)-(z_pT_Bin_11)
(Q2_y_Bin_7)-(z_pT_Bin_12), (Q2_y_Bin_7)-(z_pT_Bin_13), (Q2_y_Bin_7)-(z_pT_Bin_15)
(Q2_y_Bin_7)-(z_pT_Bin_16), (Q2_y_Bin_7)-(z_pT_Bin_17), (Q2_y_Bin_7)-(z_pT_Bin_18)
(Q2_y_Bin_7)-(z_pT_Bin_19), (Q2_y_Bin_7)-(z_pT_Bin_2), (Q2_y_Bin_7)-(z_pT_Bin_20)
(Q2_y_Bin_7)-(z_pT_Bin_21), (Q2_y_Bin_7)-(z_pT_Bin_22), (Q2_y_Bin_7)-(z_pT_Bin_23)
(Q2_y_Bin_7)-(z_pT_Bin_24), (Q2_y_Bin_7)-(z_pT_Bin_26), (Q2_y_Bin_7)-(z_pT_Bin_27)
(Q2_y_Bin_7)-(z_pT_Bin_28), (Q2_y_Bin_7)-(z_pT_Bin_29), (Q2_y_Bin_7)-(z_pT_Bin_34)
(Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_7)-(z_pT_Bin_7), (Q2_y_Bin_7)-(z_pT_Bin_8)
(Q2_y_Bin_7)-(z_pT_Bin_9), (Q2_y_Bin_8)-(z_pT_Bin_11), (Q2_y_Bin_8)-(z_pT_Bin_12)
(Q2_y_Bin_8)-(z_pT_Bin_13), (Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16)
(Q2_y_Bin_8)-(z_pT_Bin_18), (Q2_y_Bin_8)-(z_pT_Bin_19), (Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_21), (Q2_y_Bin_8)-(z_pT_Bin_23), (Q2_y_Bin_8)-(z_pT_Bin_26)
(Q2_y_Bin_8)-(z_pT_Bin_28), (Q2_y_Bin_8)-(z_pT_Bin_29), (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_9)-(z_pT_Bin_10), (Q2_y_Bin_9)-(z_pT_Bin_11), (Q2_y_Bin_9)-(z_pT_Bin_15)
(Q2_y_Bin_9)-(z_pT_Bin_16), (Q2_y_Bin_9)-(z_pT_Bin_2), (Q2_y_Bin_9)-(z_pT_Bin_22)
(Q2_y_Bin_9)-(z_pT_Bin_3), (Q2_y_Bin_9)-(z_pT_Bin_30), (Q2_y_Bin_9)-(z_pT_Bin_4)
(Q2_y_Bin_9)-(z_pT_Bin_5), (Q2_y_Bin_9)-(z_pT_Bin_6), (Q2_y_Bin_9)-(z_pT_Bin_8)
(Q2_y_Bin_9)-(z_pT_Bin_9)

#### 120°

The rule fails every assessable manual exclusion (40).

Manually excluded but passes:

None.

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_1), (Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_16)
(Q2_y_Bin_1)-(z_pT_Bin_2), (Q2_y_Bin_1)-(z_pT_Bin_23), (Q2_y_Bin_1)-(z_pT_Bin_3)
(Q2_y_Bin_1)-(z_pT_Bin_31), (Q2_y_Bin_1)-(z_pT_Bin_4), (Q2_y_Bin_1)-(z_pT_Bin_5)
(Q2_y_Bin_1)-(z_pT_Bin_6), (Q2_y_Bin_1)-(z_pT_Bin_7), (Q2_y_Bin_1)-(z_pT_Bin_8)
(Q2_y_Bin_1)-(z_pT_Bin_9), (Q2_y_Bin_10)-(z_pT_Bin_1), (Q2_y_Bin_10)-(z_pT_Bin_15)
(Q2_y_Bin_10)-(z_pT_Bin_2), (Q2_y_Bin_10)-(z_pT_Bin_26), (Q2_y_Bin_10)-(z_pT_Bin_3)
(Q2_y_Bin_10)-(z_pT_Bin_32), (Q2_y_Bin_10)-(z_pT_Bin_4), (Q2_y_Bin_10)-(z_pT_Bin_5)
(Q2_y_Bin_10)-(z_pT_Bin_6), (Q2_y_Bin_10)-(z_pT_Bin_7), (Q2_y_Bin_11)-(z_pT_Bin_1)
(Q2_y_Bin_11)-(z_pT_Bin_2), (Q2_y_Bin_11)-(z_pT_Bin_21), (Q2_y_Bin_11)-(z_pT_Bin_23)
(Q2_y_Bin_11)-(z_pT_Bin_3), (Q2_y_Bin_11)-(z_pT_Bin_6), (Q2_y_Bin_12)-(z_pT_Bin_11)
(Q2_y_Bin_12)-(z_pT_Bin_22), (Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_13)-(z_pT_Bin_1)
(Q2_y_Bin_13)-(z_pT_Bin_4), (Q2_y_Bin_14)-(z_pT_Bin_32), (Q2_y_Bin_14)-(z_pT_Bin_5)
(Q2_y_Bin_15)-(z_pT_Bin_1), (Q2_y_Bin_15)-(z_pT_Bin_15), (Q2_y_Bin_15)-(z_pT_Bin_2)
(Q2_y_Bin_15)-(z_pT_Bin_22), (Q2_y_Bin_15)-(z_pT_Bin_23), (Q2_y_Bin_15)-(z_pT_Bin_24)
(Q2_y_Bin_16)-(z_pT_Bin_6), (Q2_y_Bin_2)-(z_pT_Bin_1), (Q2_y_Bin_2)-(z_pT_Bin_10)
(Q2_y_Bin_2)-(z_pT_Bin_11), (Q2_y_Bin_2)-(z_pT_Bin_14), (Q2_y_Bin_2)-(z_pT_Bin_15)
(Q2_y_Bin_2)-(z_pT_Bin_16), (Q2_y_Bin_2)-(z_pT_Bin_2), (Q2_y_Bin_2)-(z_pT_Bin_20)
(Q2_y_Bin_2)-(z_pT_Bin_21), (Q2_y_Bin_2)-(z_pT_Bin_25), (Q2_y_Bin_2)-(z_pT_Bin_26)
(Q2_y_Bin_2)-(z_pT_Bin_3), (Q2_y_Bin_2)-(z_pT_Bin_32), (Q2_y_Bin_2)-(z_pT_Bin_33)
(Q2_y_Bin_2)-(z_pT_Bin_34), (Q2_y_Bin_2)-(z_pT_Bin_4), (Q2_y_Bin_2)-(z_pT_Bin_5)
(Q2_y_Bin_2)-(z_pT_Bin_6), (Q2_y_Bin_2)-(z_pT_Bin_7), (Q2_y_Bin_2)-(z_pT_Bin_8)
(Q2_y_Bin_2)-(z_pT_Bin_9), (Q2_y_Bin_3)-(z_pT_Bin_1), (Q2_y_Bin_3)-(z_pT_Bin_11)
(Q2_y_Bin_3)-(z_pT_Bin_12), (Q2_y_Bin_3)-(z_pT_Bin_13), (Q2_y_Bin_3)-(z_pT_Bin_14)
(Q2_y_Bin_3)-(z_pT_Bin_15), (Q2_y_Bin_3)-(z_pT_Bin_16), (Q2_y_Bin_3)-(z_pT_Bin_17)
(Q2_y_Bin_3)-(z_pT_Bin_18), (Q2_y_Bin_3)-(z_pT_Bin_19), (Q2_y_Bin_3)-(z_pT_Bin_2)
(Q2_y_Bin_3)-(z_pT_Bin_21), (Q2_y_Bin_3)-(z_pT_Bin_22), (Q2_y_Bin_3)-(z_pT_Bin_23)
(Q2_y_Bin_3)-(z_pT_Bin_24), (Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_7)
(Q2_y_Bin_3)-(z_pT_Bin_8), (Q2_y_Bin_3)-(z_pT_Bin_9), (Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_13), (Q2_y_Bin_4)-(z_pT_Bin_14), (Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_20), (Q2_y_Bin_4)-(z_pT_Bin_21)
(Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_26), (Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission], (Q2_y_Bin_5)-(z_pT_Bin_1), (Q2_y_Bin_5)-(z_pT_Bin_10)
(Q2_y_Bin_5)-(z_pT_Bin_13), (Q2_y_Bin_5)-(z_pT_Bin_14), (Q2_y_Bin_5)-(z_pT_Bin_15)
(Q2_y_Bin_5)-(z_pT_Bin_19), (Q2_y_Bin_5)-(z_pT_Bin_20), (Q2_y_Bin_5)-(z_pT_Bin_25)
(Q2_y_Bin_5)-(z_pT_Bin_3), (Q2_y_Bin_5)-(z_pT_Bin_32), (Q2_y_Bin_5)-(z_pT_Bin_4)
(Q2_y_Bin_5)-(z_pT_Bin_5), (Q2_y_Bin_5)-(z_pT_Bin_6), (Q2_y_Bin_5)-(z_pT_Bin_7)
(Q2_y_Bin_5)-(z_pT_Bin_8), (Q2_y_Bin_5)-(z_pT_Bin_9), (Q2_y_Bin_6)-(z_pT_Bin_1)
(Q2_y_Bin_6)-(z_pT_Bin_14), (Q2_y_Bin_6)-(z_pT_Bin_2), (Q2_y_Bin_6)-(z_pT_Bin_20)
(Q2_y_Bin_6)-(z_pT_Bin_27), (Q2_y_Bin_6)-(z_pT_Bin_28), (Q2_y_Bin_6)-(z_pT_Bin_3)
(Q2_y_Bin_6)-(z_pT_Bin_4), (Q2_y_Bin_6)-(z_pT_Bin_5), (Q2_y_Bin_6)-(z_pT_Bin_6)
(Q2_y_Bin_6)-(z_pT_Bin_7), (Q2_y_Bin_6)-(z_pT_Bin_8), (Q2_y_Bin_6)-(z_pT_Bin_9)
(Q2_y_Bin_7)-(z_pT_Bin_1), (Q2_y_Bin_7)-(z_pT_Bin_10), (Q2_y_Bin_7)-(z_pT_Bin_11)
(Q2_y_Bin_7)-(z_pT_Bin_12), (Q2_y_Bin_7)-(z_pT_Bin_13), (Q2_y_Bin_7)-(z_pT_Bin_16)
(Q2_y_Bin_7)-(z_pT_Bin_17), (Q2_y_Bin_7)-(z_pT_Bin_2), (Q2_y_Bin_7)-(z_pT_Bin_21)
(Q2_y_Bin_7)-(z_pT_Bin_24), (Q2_y_Bin_7)-(z_pT_Bin_26), (Q2_y_Bin_7)-(z_pT_Bin_27)
(Q2_y_Bin_7)-(z_pT_Bin_34), (Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_7)-(z_pT_Bin_7)
(Q2_y_Bin_7)-(z_pT_Bin_9), (Q2_y_Bin_8)-(z_pT_Bin_11), (Q2_y_Bin_8)-(z_pT_Bin_12)
(Q2_y_Bin_8)-(z_pT_Bin_13), (Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16)
(Q2_y_Bin_8)-(z_pT_Bin_18), (Q2_y_Bin_8)-(z_pT_Bin_19), (Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_21), (Q2_y_Bin_8)-(z_pT_Bin_23), (Q2_y_Bin_8)-(z_pT_Bin_28)
(Q2_y_Bin_8)-(z_pT_Bin_29), (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_9)-(z_pT_Bin_10)
(Q2_y_Bin_9)-(z_pT_Bin_16), (Q2_y_Bin_9)-(z_pT_Bin_2), (Q2_y_Bin_9)-(z_pT_Bin_3)
(Q2_y_Bin_9)-(z_pT_Bin_4), (Q2_y_Bin_9)-(z_pT_Bin_5), (Q2_y_Bin_9)-(z_pT_Bin_6)
(Q2_y_Bin_9)-(z_pT_Bin_9)

#### 135°

The rule fails every assessable manual exclusion (40).

Manually excluded but passes:

None.

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_1), (Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_16)
(Q2_y_Bin_1)-(z_pT_Bin_2), (Q2_y_Bin_1)-(z_pT_Bin_3), (Q2_y_Bin_1)-(z_pT_Bin_4)
(Q2_y_Bin_1)-(z_pT_Bin_5), (Q2_y_Bin_1)-(z_pT_Bin_6), (Q2_y_Bin_1)-(z_pT_Bin_7)
(Q2_y_Bin_1)-(z_pT_Bin_8), (Q2_y_Bin_1)-(z_pT_Bin_9), (Q2_y_Bin_10)-(z_pT_Bin_1)
(Q2_y_Bin_10)-(z_pT_Bin_2), (Q2_y_Bin_10)-(z_pT_Bin_3), (Q2_y_Bin_10)-(z_pT_Bin_32)
(Q2_y_Bin_10)-(z_pT_Bin_4), (Q2_y_Bin_10)-(z_pT_Bin_5), (Q2_y_Bin_10)-(z_pT_Bin_6)
(Q2_y_Bin_10)-(z_pT_Bin_7), (Q2_y_Bin_11)-(z_pT_Bin_1), (Q2_y_Bin_11)-(z_pT_Bin_2)
(Q2_y_Bin_11)-(z_pT_Bin_23), (Q2_y_Bin_11)-(z_pT_Bin_3), (Q2_y_Bin_11)-(z_pT_Bin_6)
(Q2_y_Bin_12)-(z_pT_Bin_11), (Q2_y_Bin_12)-(z_pT_Bin_22), (Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_13)-(z_pT_Bin_1), (Q2_y_Bin_14)-(z_pT_Bin_5), (Q2_y_Bin_15)-(z_pT_Bin_1)
(Q2_y_Bin_15)-(z_pT_Bin_15), (Q2_y_Bin_15)-(z_pT_Bin_2), (Q2_y_Bin_15)-(z_pT_Bin_22)
(Q2_y_Bin_15)-(z_pT_Bin_23), (Q2_y_Bin_15)-(z_pT_Bin_24), (Q2_y_Bin_16)-(z_pT_Bin_6)
(Q2_y_Bin_2)-(z_pT_Bin_1), (Q2_y_Bin_2)-(z_pT_Bin_10), (Q2_y_Bin_2)-(z_pT_Bin_14)
(Q2_y_Bin_2)-(z_pT_Bin_15), (Q2_y_Bin_2)-(z_pT_Bin_2), (Q2_y_Bin_2)-(z_pT_Bin_20)
(Q2_y_Bin_2)-(z_pT_Bin_25), (Q2_y_Bin_2)-(z_pT_Bin_3), (Q2_y_Bin_2)-(z_pT_Bin_32)
(Q2_y_Bin_2)-(z_pT_Bin_33), (Q2_y_Bin_2)-(z_pT_Bin_34), (Q2_y_Bin_2)-(z_pT_Bin_4)
(Q2_y_Bin_2)-(z_pT_Bin_5), (Q2_y_Bin_2)-(z_pT_Bin_6), (Q2_y_Bin_2)-(z_pT_Bin_7)
(Q2_y_Bin_2)-(z_pT_Bin_8), (Q2_y_Bin_2)-(z_pT_Bin_9), (Q2_y_Bin_3)-(z_pT_Bin_1)
(Q2_y_Bin_3)-(z_pT_Bin_11), (Q2_y_Bin_3)-(z_pT_Bin_12), (Q2_y_Bin_3)-(z_pT_Bin_13)
(Q2_y_Bin_3)-(z_pT_Bin_14), (Q2_y_Bin_3)-(z_pT_Bin_15), (Q2_y_Bin_3)-(z_pT_Bin_16)
(Q2_y_Bin_3)-(z_pT_Bin_17), (Q2_y_Bin_3)-(z_pT_Bin_18), (Q2_y_Bin_3)-(z_pT_Bin_2)
(Q2_y_Bin_3)-(z_pT_Bin_21), (Q2_y_Bin_3)-(z_pT_Bin_24), (Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_7), (Q2_y_Bin_3)-(z_pT_Bin_8), (Q2_y_Bin_3)-(z_pT_Bin_9)
(Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_13), (Q2_y_Bin_4)-(z_pT_Bin_14)
(Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_21)
(Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_26), (Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission], (Q2_y_Bin_5)-(z_pT_Bin_1), (Q2_y_Bin_5)-(z_pT_Bin_10)
(Q2_y_Bin_5)-(z_pT_Bin_13), (Q2_y_Bin_5)-(z_pT_Bin_14), (Q2_y_Bin_5)-(z_pT_Bin_15)
(Q2_y_Bin_5)-(z_pT_Bin_19), (Q2_y_Bin_5)-(z_pT_Bin_20), (Q2_y_Bin_5)-(z_pT_Bin_3)
(Q2_y_Bin_5)-(z_pT_Bin_32), (Q2_y_Bin_5)-(z_pT_Bin_4), (Q2_y_Bin_5)-(z_pT_Bin_5)
(Q2_y_Bin_5)-(z_pT_Bin_6), (Q2_y_Bin_5)-(z_pT_Bin_7), (Q2_y_Bin_5)-(z_pT_Bin_8)
(Q2_y_Bin_5)-(z_pT_Bin_9), (Q2_y_Bin_6)-(z_pT_Bin_1), (Q2_y_Bin_6)-(z_pT_Bin_14)
(Q2_y_Bin_6)-(z_pT_Bin_2), (Q2_y_Bin_6)-(z_pT_Bin_20), (Q2_y_Bin_6)-(z_pT_Bin_27)
(Q2_y_Bin_6)-(z_pT_Bin_3), (Q2_y_Bin_6)-(z_pT_Bin_4), (Q2_y_Bin_6)-(z_pT_Bin_5)
(Q2_y_Bin_6)-(z_pT_Bin_6), (Q2_y_Bin_6)-(z_pT_Bin_7), (Q2_y_Bin_6)-(z_pT_Bin_8)
(Q2_y_Bin_6)-(z_pT_Bin_9), (Q2_y_Bin_7)-(z_pT_Bin_1), (Q2_y_Bin_7)-(z_pT_Bin_10)
(Q2_y_Bin_7)-(z_pT_Bin_11), (Q2_y_Bin_7)-(z_pT_Bin_12), (Q2_y_Bin_7)-(z_pT_Bin_13)
(Q2_y_Bin_7)-(z_pT_Bin_2), (Q2_y_Bin_7)-(z_pT_Bin_21), (Q2_y_Bin_7)-(z_pT_Bin_24)
(Q2_y_Bin_7)-(z_pT_Bin_27), (Q2_y_Bin_7)-(z_pT_Bin_34), (Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission]
(Q2_y_Bin_7)-(z_pT_Bin_7), (Q2_y_Bin_7)-(z_pT_Bin_9), (Q2_y_Bin_8)-(z_pT_Bin_11)
(Q2_y_Bin_8)-(z_pT_Bin_13), (Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16)
(Q2_y_Bin_8)-(z_pT_Bin_19), (Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_28)
(Q2_y_Bin_8)-(z_pT_Bin_29), (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_9)-(z_pT_Bin_2)
(Q2_y_Bin_9)-(z_pT_Bin_3), (Q2_y_Bin_9)-(z_pT_Bin_4)

#### 150°

The rule fails every assessable manual exclusion (40).

Manually excluded but passes:

None.

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_1), (Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_16)
(Q2_y_Bin_1)-(z_pT_Bin_2), (Q2_y_Bin_1)-(z_pT_Bin_3), (Q2_y_Bin_1)-(z_pT_Bin_4)
(Q2_y_Bin_1)-(z_pT_Bin_5), (Q2_y_Bin_1)-(z_pT_Bin_6), (Q2_y_Bin_1)-(z_pT_Bin_8)
(Q2_y_Bin_1)-(z_pT_Bin_9), (Q2_y_Bin_10)-(z_pT_Bin_2), (Q2_y_Bin_10)-(z_pT_Bin_3)
(Q2_y_Bin_10)-(z_pT_Bin_32), (Q2_y_Bin_10)-(z_pT_Bin_5), (Q2_y_Bin_10)-(z_pT_Bin_6)
(Q2_y_Bin_11)-(z_pT_Bin_2), (Q2_y_Bin_11)-(z_pT_Bin_23), (Q2_y_Bin_11)-(z_pT_Bin_3)
(Q2_y_Bin_12)-(z_pT_Bin_11), (Q2_y_Bin_12)-(z_pT_Bin_22), (Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_13)-(z_pT_Bin_1), (Q2_y_Bin_14)-(z_pT_Bin_5), (Q2_y_Bin_15)-(z_pT_Bin_1)
(Q2_y_Bin_15)-(z_pT_Bin_15), (Q2_y_Bin_15)-(z_pT_Bin_2), (Q2_y_Bin_15)-(z_pT_Bin_23)
(Q2_y_Bin_15)-(z_pT_Bin_24), (Q2_y_Bin_2)-(z_pT_Bin_1), (Q2_y_Bin_2)-(z_pT_Bin_10)
(Q2_y_Bin_2)-(z_pT_Bin_14), (Q2_y_Bin_2)-(z_pT_Bin_15), (Q2_y_Bin_2)-(z_pT_Bin_2)
(Q2_y_Bin_2)-(z_pT_Bin_20), (Q2_y_Bin_2)-(z_pT_Bin_25), (Q2_y_Bin_2)-(z_pT_Bin_3)
(Q2_y_Bin_2)-(z_pT_Bin_32), (Q2_y_Bin_2)-(z_pT_Bin_33), (Q2_y_Bin_2)-(z_pT_Bin_34)
(Q2_y_Bin_2)-(z_pT_Bin_4), (Q2_y_Bin_2)-(z_pT_Bin_5), (Q2_y_Bin_2)-(z_pT_Bin_6)
(Q2_y_Bin_2)-(z_pT_Bin_7), (Q2_y_Bin_2)-(z_pT_Bin_8), (Q2_y_Bin_2)-(z_pT_Bin_9)
(Q2_y_Bin_3)-(z_pT_Bin_1), (Q2_y_Bin_3)-(z_pT_Bin_11), (Q2_y_Bin_3)-(z_pT_Bin_12)
(Q2_y_Bin_3)-(z_pT_Bin_13), (Q2_y_Bin_3)-(z_pT_Bin_15), (Q2_y_Bin_3)-(z_pT_Bin_16)
(Q2_y_Bin_3)-(z_pT_Bin_2), (Q2_y_Bin_3)-(z_pT_Bin_21), (Q2_y_Bin_3)-(z_pT_Bin_24)
(Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_7), (Q2_y_Bin_3)-(z_pT_Bin_8)
(Q2_y_Bin_3)-(z_pT_Bin_9), (Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_13)
(Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_21)
(Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_26), (Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission], (Q2_y_Bin_5)-(z_pT_Bin_1), (Q2_y_Bin_5)-(z_pT_Bin_13)
(Q2_y_Bin_5)-(z_pT_Bin_3), (Q2_y_Bin_5)-(z_pT_Bin_4), (Q2_y_Bin_5)-(z_pT_Bin_5)
(Q2_y_Bin_5)-(z_pT_Bin_6), (Q2_y_Bin_5)-(z_pT_Bin_7), (Q2_y_Bin_5)-(z_pT_Bin_8)
(Q2_y_Bin_5)-(z_pT_Bin_9), (Q2_y_Bin_6)-(z_pT_Bin_1), (Q2_y_Bin_6)-(z_pT_Bin_2)
(Q2_y_Bin_6)-(z_pT_Bin_27), (Q2_y_Bin_6)-(z_pT_Bin_3), (Q2_y_Bin_6)-(z_pT_Bin_4)
(Q2_y_Bin_6)-(z_pT_Bin_5), (Q2_y_Bin_6)-(z_pT_Bin_6), (Q2_y_Bin_6)-(z_pT_Bin_9)
(Q2_y_Bin_7)-(z_pT_Bin_1), (Q2_y_Bin_7)-(z_pT_Bin_11), (Q2_y_Bin_7)-(z_pT_Bin_12)
(Q2_y_Bin_7)-(z_pT_Bin_13), (Q2_y_Bin_7)-(z_pT_Bin_2), (Q2_y_Bin_7)-(z_pT_Bin_21)
(Q2_y_Bin_7)-(z_pT_Bin_24), (Q2_y_Bin_7)-(z_pT_Bin_34), (Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_11), (Q2_y_Bin_8)-(z_pT_Bin_13), (Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_16), (Q2_y_Bin_8)-(z_pT_Bin_19), (Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_28), (Q2_y_Bin_8)-(z_pT_Bin_29), (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_9)-(z_pT_Bin_2)

#### 180°

The rule does not fail every assessable manual exclusion: 4 of 40 pass.

Manually excluded but passes:

(Q2_y_Bin_1)-(z_pT_Bin_22), (Q2_y_Bin_2)-(z_pT_Bin_13), (Q2_y_Bin_2)-(z_pT_Bin_19)
(Q2_y_Bin_9)-(z_pT_Bin_29)

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_1), (Q2_y_Bin_1)-(z_pT_Bin_2), (Q2_y_Bin_1)-(z_pT_Bin_3)
(Q2_y_Bin_1)-(z_pT_Bin_4), (Q2_y_Bin_1)-(z_pT_Bin_8), (Q2_y_Bin_1)-(z_pT_Bin_9)
(Q2_y_Bin_10)-(z_pT_Bin_6), (Q2_y_Bin_11)-(z_pT_Bin_23), (Q2_y_Bin_11)-(z_pT_Bin_3)
(Q2_y_Bin_12)-(z_pT_Bin_22), (Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_15)-(z_pT_Bin_24)
(Q2_y_Bin_2)-(z_pT_Bin_1), (Q2_y_Bin_2)-(z_pT_Bin_2), (Q2_y_Bin_2)-(z_pT_Bin_20)
(Q2_y_Bin_2)-(z_pT_Bin_3), (Q2_y_Bin_2)-(z_pT_Bin_32), (Q2_y_Bin_2)-(z_pT_Bin_4)
(Q2_y_Bin_2)-(z_pT_Bin_5), (Q2_y_Bin_2)-(z_pT_Bin_6), (Q2_y_Bin_2)-(z_pT_Bin_7)
(Q2_y_Bin_3)-(z_pT_Bin_1), (Q2_y_Bin_3)-(z_pT_Bin_13), (Q2_y_Bin_3)-(z_pT_Bin_2)
(Q2_y_Bin_3)-(z_pT_Bin_24), (Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_7)
(Q2_y_Bin_3)-(z_pT_Bin_9), (Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_13)
(Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_21)
(Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission]
(Q2_y_Bin_5)-(z_pT_Bin_1), (Q2_y_Bin_5)-(z_pT_Bin_3), (Q2_y_Bin_5)-(z_pT_Bin_4)
(Q2_y_Bin_5)-(z_pT_Bin_5), (Q2_y_Bin_5)-(z_pT_Bin_7), (Q2_y_Bin_7)-(z_pT_Bin_12)
(Q2_y_Bin_7)-(z_pT_Bin_24), (Q2_y_Bin_7)-(z_pT_Bin_34), (Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_11), (Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16)
(Q2_y_Bin_8)-(z_pT_Bin_19), (Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_29)
(Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission]

### eS4o

Manual list entries: 49. Fit-quality omissions relative to the nominal acceptance bins: 37. Comparisons the budget still keeps: 372.

#### 90°

The rule fails every assessable manual exclusion (49).

Manually excluded but passes:

None.

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_11), (Q2_y_Bin_1)-(z_pT_Bin_15)
(Q2_y_Bin_1)-(z_pT_Bin_16), (Q2_y_Bin_1)-(z_pT_Bin_17), (Q2_y_Bin_1)-(z_pT_Bin_23)
(Q2_y_Bin_1)-(z_pT_Bin_31), (Q2_y_Bin_1)-(z_pT_Bin_32), (Q2_y_Bin_1)-(z_pT_Bin_4)
(Q2_y_Bin_1)-(z_pT_Bin_5), (Q2_y_Bin_1)-(z_pT_Bin_6), (Q2_y_Bin_1)-(z_pT_Bin_7)
(Q2_y_Bin_1)-(z_pT_Bin_9), (Q2_y_Bin_10)-(z_pT_Bin_1), (Q2_y_Bin_10)-(z_pT_Bin_10)
(Q2_y_Bin_10)-(z_pT_Bin_15), (Q2_y_Bin_10)-(z_pT_Bin_2), (Q2_y_Bin_10)-(z_pT_Bin_20)
(Q2_y_Bin_10)-(z_pT_Bin_26), (Q2_y_Bin_10)-(z_pT_Bin_3), (Q2_y_Bin_10)-(z_pT_Bin_31)
(Q2_y_Bin_10)-(z_pT_Bin_32), (Q2_y_Bin_10)-(z_pT_Bin_4), (Q2_y_Bin_10)-(z_pT_Bin_5)
(Q2_y_Bin_10)-(z_pT_Bin_6), (Q2_y_Bin_10)-(z_pT_Bin_7), (Q2_y_Bin_10)-(z_pT_Bin_9)
(Q2_y_Bin_11)-(z_pT_Bin_1), (Q2_y_Bin_11)-(z_pT_Bin_10), (Q2_y_Bin_11)-(z_pT_Bin_13)
(Q2_y_Bin_11)-(z_pT_Bin_15), (Q2_y_Bin_11)-(z_pT_Bin_18), (Q2_y_Bin_11)-(z_pT_Bin_19)
(Q2_y_Bin_11)-(z_pT_Bin_2), (Q2_y_Bin_11)-(z_pT_Bin_21), (Q2_y_Bin_11)-(z_pT_Bin_23)
(Q2_y_Bin_11)-(z_pT_Bin_4), (Q2_y_Bin_11)-(z_pT_Bin_6), (Q2_y_Bin_11)-(z_pT_Bin_9)
(Q2_y_Bin_12)-(z_pT_Bin_11), (Q2_y_Bin_12)-(z_pT_Bin_13), (Q2_y_Bin_12)-(z_pT_Bin_16)
(Q2_y_Bin_12)-(z_pT_Bin_18), (Q2_y_Bin_12)-(z_pT_Bin_22), (Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission]
(Q2_y_Bin_12)-(z_pT_Bin_6), (Q2_y_Bin_12)-(z_pT_Bin_7), (Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_13)-(z_pT_Bin_1), (Q2_y_Bin_13)-(z_pT_Bin_12), (Q2_y_Bin_13)-(z_pT_Bin_17)
(Q2_y_Bin_13)-(z_pT_Bin_2), (Q2_y_Bin_13)-(z_pT_Bin_26), (Q2_y_Bin_13)-(z_pT_Bin_3)
(Q2_y_Bin_13)-(z_pT_Bin_4), (Q2_y_Bin_13)-(z_pT_Bin_5), (Q2_y_Bin_13)-(z_pT_Bin_7)
(Q2_y_Bin_14)-(z_pT_Bin_1), (Q2_y_Bin_14)-(z_pT_Bin_2), (Q2_y_Bin_14)-(z_pT_Bin_3)
(Q2_y_Bin_14)-(z_pT_Bin_32), (Q2_y_Bin_14)-(z_pT_Bin_4), (Q2_y_Bin_14)-(z_pT_Bin_5)
(Q2_y_Bin_15)-(z_pT_Bin_1), (Q2_y_Bin_15)-(z_pT_Bin_19), (Q2_y_Bin_15)-(z_pT_Bin_2)
(Q2_y_Bin_15)-(z_pT_Bin_21), (Q2_y_Bin_15)-(z_pT_Bin_23), (Q2_y_Bin_15)-(z_pT_Bin_9)
(Q2_y_Bin_16)-(z_pT_Bin_1), (Q2_y_Bin_16)-(z_pT_Bin_3), (Q2_y_Bin_16)-(z_pT_Bin_4)
(Q2_y_Bin_16)-(z_pT_Bin_5), (Q2_y_Bin_16)-(z_pT_Bin_6), (Q2_y_Bin_16)-(z_pT_Bin_9)
(Q2_y_Bin_17)-(z_pT_Bin_4), (Q2_y_Bin_2)-(z_pT_Bin_10), (Q2_y_Bin_2)-(z_pT_Bin_11)
(Q2_y_Bin_2)-(z_pT_Bin_12), (Q2_y_Bin_2)-(z_pT_Bin_14), (Q2_y_Bin_2)-(z_pT_Bin_15)
(Q2_y_Bin_2)-(z_pT_Bin_16), (Q2_y_Bin_2)-(z_pT_Bin_18), (Q2_y_Bin_2)-(z_pT_Bin_19)
(Q2_y_Bin_2)-(z_pT_Bin_20), (Q2_y_Bin_2)-(z_pT_Bin_21), (Q2_y_Bin_2)-(z_pT_Bin_23)
(Q2_y_Bin_2)-(z_pT_Bin_25), (Q2_y_Bin_2)-(z_pT_Bin_26), (Q2_y_Bin_2)-(z_pT_Bin_27)
(Q2_y_Bin_2)-(z_pT_Bin_28), (Q2_y_Bin_2)-(z_pT_Bin_32), (Q2_y_Bin_2)-(z_pT_Bin_33)
(Q2_y_Bin_2)-(z_pT_Bin_34), (Q2_y_Bin_2)-(z_pT_Bin_5), (Q2_y_Bin_2)-(z_pT_Bin_6)
(Q2_y_Bin_2)-(z_pT_Bin_7), (Q2_y_Bin_2)-(z_pT_Bin_9), (Q2_y_Bin_3)-(z_pT_Bin_1)
(Q2_y_Bin_3)-(z_pT_Bin_10), (Q2_y_Bin_3)-(z_pT_Bin_11), (Q2_y_Bin_3)-(z_pT_Bin_12)
(Q2_y_Bin_3)-(z_pT_Bin_13), (Q2_y_Bin_3)-(z_pT_Bin_14), (Q2_y_Bin_3)-(z_pT_Bin_15)
(Q2_y_Bin_3)-(z_pT_Bin_16), (Q2_y_Bin_3)-(z_pT_Bin_17), (Q2_y_Bin_3)-(z_pT_Bin_18)
(Q2_y_Bin_3)-(z_pT_Bin_19), (Q2_y_Bin_3)-(z_pT_Bin_20), (Q2_y_Bin_3)-(z_pT_Bin_21)
(Q2_y_Bin_3)-(z_pT_Bin_22), (Q2_y_Bin_3)-(z_pT_Bin_23), (Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_7)
(Q2_y_Bin_3)-(z_pT_Bin_8), (Q2_y_Bin_3)-(z_pT_Bin_9), (Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_13), (Q2_y_Bin_4)-(z_pT_Bin_14), (Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_19), (Q2_y_Bin_4)-(z_pT_Bin_20)
(Q2_y_Bin_4)-(z_pT_Bin_21), (Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_25)
(Q2_y_Bin_4)-(z_pT_Bin_26), (Q2_y_Bin_4)-(z_pT_Bin_27), (Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission], (Q2_y_Bin_5)-(z_pT_Bin_10), (Q2_y_Bin_5)-(z_pT_Bin_14)
(Q2_y_Bin_5)-(z_pT_Bin_15), (Q2_y_Bin_5)-(z_pT_Bin_19), (Q2_y_Bin_5)-(z_pT_Bin_20)
(Q2_y_Bin_5)-(z_pT_Bin_25), (Q2_y_Bin_5)-(z_pT_Bin_26), (Q2_y_Bin_5)-(z_pT_Bin_3)
(Q2_y_Bin_5)-(z_pT_Bin_31), (Q2_y_Bin_5)-(z_pT_Bin_32), (Q2_y_Bin_5)-(z_pT_Bin_4)
(Q2_y_Bin_5)-(z_pT_Bin_5), (Q2_y_Bin_5)-(z_pT_Bin_6), (Q2_y_Bin_5)-(z_pT_Bin_8)
(Q2_y_Bin_5)-(z_pT_Bin_9), (Q2_y_Bin_6)-(z_pT_Bin_1), (Q2_y_Bin_6)-(z_pT_Bin_10)
(Q2_y_Bin_6)-(z_pT_Bin_11), (Q2_y_Bin_6)-(z_pT_Bin_13), (Q2_y_Bin_6)-(z_pT_Bin_14)
(Q2_y_Bin_6)-(z_pT_Bin_15), (Q2_y_Bin_6)-(z_pT_Bin_16), (Q2_y_Bin_6)-(z_pT_Bin_19)
(Q2_y_Bin_6)-(z_pT_Bin_2), (Q2_y_Bin_6)-(z_pT_Bin_20), (Q2_y_Bin_6)-(z_pT_Bin_27)
(Q2_y_Bin_6)-(z_pT_Bin_28), (Q2_y_Bin_6)-(z_pT_Bin_3), (Q2_y_Bin_6)-(z_pT_Bin_4)
(Q2_y_Bin_6)-(z_pT_Bin_5), (Q2_y_Bin_6)-(z_pT_Bin_6), (Q2_y_Bin_6)-(z_pT_Bin_7)
(Q2_y_Bin_6)-(z_pT_Bin_8), (Q2_y_Bin_6)-(z_pT_Bin_9), (Q2_y_Bin_7)-(z_pT_Bin_1)
(Q2_y_Bin_7)-(z_pT_Bin_10), (Q2_y_Bin_7)-(z_pT_Bin_11), (Q2_y_Bin_7)-(z_pT_Bin_12)
(Q2_y_Bin_7)-(z_pT_Bin_13), (Q2_y_Bin_7)-(z_pT_Bin_15), (Q2_y_Bin_7)-(z_pT_Bin_16)
(Q2_y_Bin_7)-(z_pT_Bin_17), (Q2_y_Bin_7)-(z_pT_Bin_18), (Q2_y_Bin_7)-(z_pT_Bin_19)
(Q2_y_Bin_7)-(z_pT_Bin_2), (Q2_y_Bin_7)-(z_pT_Bin_20), (Q2_y_Bin_7)-(z_pT_Bin_21)
(Q2_y_Bin_7)-(z_pT_Bin_22), (Q2_y_Bin_7)-(z_pT_Bin_23), (Q2_y_Bin_7)-(z_pT_Bin_24)
(Q2_y_Bin_7)-(z_pT_Bin_25), (Q2_y_Bin_7)-(z_pT_Bin_26), (Q2_y_Bin_7)-(z_pT_Bin_27)
(Q2_y_Bin_7)-(z_pT_Bin_28), (Q2_y_Bin_7)-(z_pT_Bin_29), (Q2_y_Bin_7)-(z_pT_Bin_31)
(Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_7)-(z_pT_Bin_7), (Q2_y_Bin_7)-(z_pT_Bin_8)
(Q2_y_Bin_7)-(z_pT_Bin_9), (Q2_y_Bin_8)-(z_pT_Bin_11), (Q2_y_Bin_8)-(z_pT_Bin_12)
(Q2_y_Bin_8)-(z_pT_Bin_13), (Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16)
(Q2_y_Bin_8)-(z_pT_Bin_18), (Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_21)
(Q2_y_Bin_8)-(z_pT_Bin_23), (Q2_y_Bin_8)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_26)
(Q2_y_Bin_8)-(z_pT_Bin_28), (Q2_y_Bin_8)-(z_pT_Bin_29), (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_9)-(z_pT_Bin_10), (Q2_y_Bin_9)-(z_pT_Bin_11), (Q2_y_Bin_9)-(z_pT_Bin_15)
(Q2_y_Bin_9)-(z_pT_Bin_16), (Q2_y_Bin_9)-(z_pT_Bin_22), (Q2_y_Bin_9)-(z_pT_Bin_3)
(Q2_y_Bin_9)-(z_pT_Bin_30), (Q2_y_Bin_9)-(z_pT_Bin_4), (Q2_y_Bin_9)-(z_pT_Bin_5)
(Q2_y_Bin_9)-(z_pT_Bin_6), (Q2_y_Bin_9)-(z_pT_Bin_8), (Q2_y_Bin_9)-(z_pT_Bin_9)

#### 120°

The rule fails every assessable manual exclusion (49).

Manually excluded but passes:

None.

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_15), (Q2_y_Bin_1)-(z_pT_Bin_16)
(Q2_y_Bin_1)-(z_pT_Bin_31), (Q2_y_Bin_1)-(z_pT_Bin_32), (Q2_y_Bin_1)-(z_pT_Bin_4)
(Q2_y_Bin_1)-(z_pT_Bin_5), (Q2_y_Bin_1)-(z_pT_Bin_6), (Q2_y_Bin_1)-(z_pT_Bin_7)
(Q2_y_Bin_1)-(z_pT_Bin_9), (Q2_y_Bin_10)-(z_pT_Bin_1), (Q2_y_Bin_10)-(z_pT_Bin_2)
(Q2_y_Bin_10)-(z_pT_Bin_3), (Q2_y_Bin_10)-(z_pT_Bin_32), (Q2_y_Bin_10)-(z_pT_Bin_4)
(Q2_y_Bin_10)-(z_pT_Bin_5), (Q2_y_Bin_10)-(z_pT_Bin_6), (Q2_y_Bin_10)-(z_pT_Bin_7)
(Q2_y_Bin_11)-(z_pT_Bin_1), (Q2_y_Bin_11)-(z_pT_Bin_10), (Q2_y_Bin_11)-(z_pT_Bin_2)
(Q2_y_Bin_11)-(z_pT_Bin_21), (Q2_y_Bin_11)-(z_pT_Bin_23), (Q2_y_Bin_11)-(z_pT_Bin_4)
(Q2_y_Bin_11)-(z_pT_Bin_6), (Q2_y_Bin_12)-(z_pT_Bin_11), (Q2_y_Bin_12)-(z_pT_Bin_22)
(Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_6), (Q2_y_Bin_12)-(z_pT_Bin_7)
(Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_13)-(z_pT_Bin_1), (Q2_y_Bin_13)-(z_pT_Bin_2)
(Q2_y_Bin_13)-(z_pT_Bin_4), (Q2_y_Bin_14)-(z_pT_Bin_2), (Q2_y_Bin_14)-(z_pT_Bin_32)
(Q2_y_Bin_14)-(z_pT_Bin_5), (Q2_y_Bin_15)-(z_pT_Bin_1), (Q2_y_Bin_15)-(z_pT_Bin_2)
(Q2_y_Bin_15)-(z_pT_Bin_23), (Q2_y_Bin_16)-(z_pT_Bin_6), (Q2_y_Bin_2)-(z_pT_Bin_10)
(Q2_y_Bin_2)-(z_pT_Bin_11), (Q2_y_Bin_2)-(z_pT_Bin_14), (Q2_y_Bin_2)-(z_pT_Bin_15)
(Q2_y_Bin_2)-(z_pT_Bin_16), (Q2_y_Bin_2)-(z_pT_Bin_19), (Q2_y_Bin_2)-(z_pT_Bin_20)
(Q2_y_Bin_2)-(z_pT_Bin_21), (Q2_y_Bin_2)-(z_pT_Bin_25), (Q2_y_Bin_2)-(z_pT_Bin_26)
(Q2_y_Bin_2)-(z_pT_Bin_27), (Q2_y_Bin_2)-(z_pT_Bin_32), (Q2_y_Bin_2)-(z_pT_Bin_33)
(Q2_y_Bin_2)-(z_pT_Bin_34), (Q2_y_Bin_2)-(z_pT_Bin_5), (Q2_y_Bin_2)-(z_pT_Bin_6)
(Q2_y_Bin_2)-(z_pT_Bin_7), (Q2_y_Bin_2)-(z_pT_Bin_9), (Q2_y_Bin_3)-(z_pT_Bin_1)
(Q2_y_Bin_3)-(z_pT_Bin_10), (Q2_y_Bin_3)-(z_pT_Bin_11), (Q2_y_Bin_3)-(z_pT_Bin_12)
(Q2_y_Bin_3)-(z_pT_Bin_13), (Q2_y_Bin_3)-(z_pT_Bin_14), (Q2_y_Bin_3)-(z_pT_Bin_15)
(Q2_y_Bin_3)-(z_pT_Bin_16), (Q2_y_Bin_3)-(z_pT_Bin_17), (Q2_y_Bin_3)-(z_pT_Bin_18)
(Q2_y_Bin_3)-(z_pT_Bin_19), (Q2_y_Bin_3)-(z_pT_Bin_20), (Q2_y_Bin_3)-(z_pT_Bin_21)
(Q2_y_Bin_3)-(z_pT_Bin_22), (Q2_y_Bin_3)-(z_pT_Bin_23), (Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_7)
(Q2_y_Bin_3)-(z_pT_Bin_8), (Q2_y_Bin_3)-(z_pT_Bin_9), (Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_13), (Q2_y_Bin_4)-(z_pT_Bin_14), (Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_19), (Q2_y_Bin_4)-(z_pT_Bin_20)
(Q2_y_Bin_4)-(z_pT_Bin_21), (Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_25)
(Q2_y_Bin_4)-(z_pT_Bin_26), (Q2_y_Bin_4)-(z_pT_Bin_27), (Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission], (Q2_y_Bin_5)-(z_pT_Bin_10), (Q2_y_Bin_5)-(z_pT_Bin_14)
(Q2_y_Bin_5)-(z_pT_Bin_15), (Q2_y_Bin_5)-(z_pT_Bin_19), (Q2_y_Bin_5)-(z_pT_Bin_20)
(Q2_y_Bin_5)-(z_pT_Bin_25), (Q2_y_Bin_5)-(z_pT_Bin_3), (Q2_y_Bin_5)-(z_pT_Bin_31)
(Q2_y_Bin_5)-(z_pT_Bin_32), (Q2_y_Bin_5)-(z_pT_Bin_4), (Q2_y_Bin_5)-(z_pT_Bin_5)
(Q2_y_Bin_5)-(z_pT_Bin_6), (Q2_y_Bin_5)-(z_pT_Bin_8), (Q2_y_Bin_5)-(z_pT_Bin_9)
(Q2_y_Bin_6)-(z_pT_Bin_1), (Q2_y_Bin_6)-(z_pT_Bin_10), (Q2_y_Bin_6)-(z_pT_Bin_14)
(Q2_y_Bin_6)-(z_pT_Bin_2), (Q2_y_Bin_6)-(z_pT_Bin_20), (Q2_y_Bin_6)-(z_pT_Bin_27)
(Q2_y_Bin_6)-(z_pT_Bin_28), (Q2_y_Bin_6)-(z_pT_Bin_3), (Q2_y_Bin_6)-(z_pT_Bin_4)
(Q2_y_Bin_6)-(z_pT_Bin_5), (Q2_y_Bin_6)-(z_pT_Bin_6), (Q2_y_Bin_6)-(z_pT_Bin_7)
(Q2_y_Bin_6)-(z_pT_Bin_8), (Q2_y_Bin_6)-(z_pT_Bin_9), (Q2_y_Bin_7)-(z_pT_Bin_1)
(Q2_y_Bin_7)-(z_pT_Bin_10), (Q2_y_Bin_7)-(z_pT_Bin_11), (Q2_y_Bin_7)-(z_pT_Bin_12)
(Q2_y_Bin_7)-(z_pT_Bin_13), (Q2_y_Bin_7)-(z_pT_Bin_15), (Q2_y_Bin_7)-(z_pT_Bin_16)
(Q2_y_Bin_7)-(z_pT_Bin_17), (Q2_y_Bin_7)-(z_pT_Bin_18), (Q2_y_Bin_7)-(z_pT_Bin_2)
(Q2_y_Bin_7)-(z_pT_Bin_21), (Q2_y_Bin_7)-(z_pT_Bin_24), (Q2_y_Bin_7)-(z_pT_Bin_27)
(Q2_y_Bin_7)-(z_pT_Bin_29), (Q2_y_Bin_7)-(z_pT_Bin_31), (Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission]
(Q2_y_Bin_7)-(z_pT_Bin_7), (Q2_y_Bin_7)-(z_pT_Bin_8), (Q2_y_Bin_7)-(z_pT_Bin_9)
(Q2_y_Bin_8)-(z_pT_Bin_11), (Q2_y_Bin_8)-(z_pT_Bin_12), (Q2_y_Bin_8)-(z_pT_Bin_13)
(Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16), (Q2_y_Bin_8)-(z_pT_Bin_18)
(Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_21), (Q2_y_Bin_8)-(z_pT_Bin_23)
(Q2_y_Bin_8)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_26), (Q2_y_Bin_8)-(z_pT_Bin_28)
(Q2_y_Bin_8)-(z_pT_Bin_29), (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_9)-(z_pT_Bin_10)
(Q2_y_Bin_9)-(z_pT_Bin_3), (Q2_y_Bin_9)-(z_pT_Bin_4), (Q2_y_Bin_9)-(z_pT_Bin_5)
(Q2_y_Bin_9)-(z_pT_Bin_8), (Q2_y_Bin_9)-(z_pT_Bin_9)

#### 135°

The rule does not fail every assessable manual exclusion: 1 of 49 pass.

Manually excluded but passes:

(Q2_y_Bin_15)-(z_pT_Bin_22)

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_15), (Q2_y_Bin_1)-(z_pT_Bin_16)
(Q2_y_Bin_1)-(z_pT_Bin_4), (Q2_y_Bin_1)-(z_pT_Bin_5), (Q2_y_Bin_1)-(z_pT_Bin_6)
(Q2_y_Bin_1)-(z_pT_Bin_9), (Q2_y_Bin_10)-(z_pT_Bin_1), (Q2_y_Bin_10)-(z_pT_Bin_2)
(Q2_y_Bin_10)-(z_pT_Bin_3), (Q2_y_Bin_10)-(z_pT_Bin_32), (Q2_y_Bin_10)-(z_pT_Bin_4)
(Q2_y_Bin_10)-(z_pT_Bin_5), (Q2_y_Bin_10)-(z_pT_Bin_6), (Q2_y_Bin_10)-(z_pT_Bin_7)
(Q2_y_Bin_11)-(z_pT_Bin_1), (Q2_y_Bin_11)-(z_pT_Bin_2), (Q2_y_Bin_11)-(z_pT_Bin_21)
(Q2_y_Bin_11)-(z_pT_Bin_23), (Q2_y_Bin_11)-(z_pT_Bin_4), (Q2_y_Bin_11)-(z_pT_Bin_6)
(Q2_y_Bin_12)-(z_pT_Bin_11), (Q2_y_Bin_12)-(z_pT_Bin_22), (Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission]
(Q2_y_Bin_12)-(z_pT_Bin_6), (Q2_y_Bin_12)-(z_pT_Bin_7), (Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_13)-(z_pT_Bin_1), (Q2_y_Bin_13)-(z_pT_Bin_2), (Q2_y_Bin_13)-(z_pT_Bin_4)
(Q2_y_Bin_14)-(z_pT_Bin_2), (Q2_y_Bin_14)-(z_pT_Bin_5), (Q2_y_Bin_15)-(z_pT_Bin_1)
(Q2_y_Bin_15)-(z_pT_Bin_2), (Q2_y_Bin_15)-(z_pT_Bin_23), (Q2_y_Bin_16)-(z_pT_Bin_6)
(Q2_y_Bin_2)-(z_pT_Bin_10), (Q2_y_Bin_2)-(z_pT_Bin_11), (Q2_y_Bin_2)-(z_pT_Bin_14)
(Q2_y_Bin_2)-(z_pT_Bin_15), (Q2_y_Bin_2)-(z_pT_Bin_16), (Q2_y_Bin_2)-(z_pT_Bin_19)
(Q2_y_Bin_2)-(z_pT_Bin_20), (Q2_y_Bin_2)-(z_pT_Bin_25), (Q2_y_Bin_2)-(z_pT_Bin_32)
(Q2_y_Bin_2)-(z_pT_Bin_33), (Q2_y_Bin_2)-(z_pT_Bin_34), (Q2_y_Bin_2)-(z_pT_Bin_5)
(Q2_y_Bin_2)-(z_pT_Bin_6), (Q2_y_Bin_2)-(z_pT_Bin_7), (Q2_y_Bin_2)-(z_pT_Bin_9)
(Q2_y_Bin_3)-(z_pT_Bin_1), (Q2_y_Bin_3)-(z_pT_Bin_10), (Q2_y_Bin_3)-(z_pT_Bin_11)
(Q2_y_Bin_3)-(z_pT_Bin_12), (Q2_y_Bin_3)-(z_pT_Bin_13), (Q2_y_Bin_3)-(z_pT_Bin_14)
(Q2_y_Bin_3)-(z_pT_Bin_15), (Q2_y_Bin_3)-(z_pT_Bin_16), (Q2_y_Bin_3)-(z_pT_Bin_17)
(Q2_y_Bin_3)-(z_pT_Bin_18), (Q2_y_Bin_3)-(z_pT_Bin_19), (Q2_y_Bin_3)-(z_pT_Bin_20)
(Q2_y_Bin_3)-(z_pT_Bin_21), (Q2_y_Bin_3)-(z_pT_Bin_22), (Q2_y_Bin_3)-(z_pT_Bin_23)
(Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_7), (Q2_y_Bin_3)-(z_pT_Bin_8), (Q2_y_Bin_3)-(z_pT_Bin_9)
(Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_13), (Q2_y_Bin_4)-(z_pT_Bin_14)
(Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_19)
(Q2_y_Bin_4)-(z_pT_Bin_21), (Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_25)
(Q2_y_Bin_4)-(z_pT_Bin_26), (Q2_y_Bin_4)-(z_pT_Bin_27), (Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission], (Q2_y_Bin_5)-(z_pT_Bin_14), (Q2_y_Bin_5)-(z_pT_Bin_19)
(Q2_y_Bin_5)-(z_pT_Bin_25), (Q2_y_Bin_5)-(z_pT_Bin_3), (Q2_y_Bin_5)-(z_pT_Bin_31)
(Q2_y_Bin_5)-(z_pT_Bin_4), (Q2_y_Bin_5)-(z_pT_Bin_5), (Q2_y_Bin_5)-(z_pT_Bin_6)
(Q2_y_Bin_5)-(z_pT_Bin_8), (Q2_y_Bin_5)-(z_pT_Bin_9), (Q2_y_Bin_6)-(z_pT_Bin_1)
(Q2_y_Bin_6)-(z_pT_Bin_14), (Q2_y_Bin_6)-(z_pT_Bin_2), (Q2_y_Bin_6)-(z_pT_Bin_20)
(Q2_y_Bin_6)-(z_pT_Bin_27), (Q2_y_Bin_6)-(z_pT_Bin_28), (Q2_y_Bin_6)-(z_pT_Bin_3)
(Q2_y_Bin_6)-(z_pT_Bin_4), (Q2_y_Bin_6)-(z_pT_Bin_5), (Q2_y_Bin_6)-(z_pT_Bin_6)
(Q2_y_Bin_6)-(z_pT_Bin_7), (Q2_y_Bin_6)-(z_pT_Bin_8), (Q2_y_Bin_6)-(z_pT_Bin_9)
(Q2_y_Bin_7)-(z_pT_Bin_1), (Q2_y_Bin_7)-(z_pT_Bin_10), (Q2_y_Bin_7)-(z_pT_Bin_11)
(Q2_y_Bin_7)-(z_pT_Bin_12), (Q2_y_Bin_7)-(z_pT_Bin_13), (Q2_y_Bin_7)-(z_pT_Bin_2)
(Q2_y_Bin_7)-(z_pT_Bin_21), (Q2_y_Bin_7)-(z_pT_Bin_24), (Q2_y_Bin_7)-(z_pT_Bin_27)
(Q2_y_Bin_7)-(z_pT_Bin_31), (Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_7)-(z_pT_Bin_7)
(Q2_y_Bin_8)-(z_pT_Bin_11), (Q2_y_Bin_8)-(z_pT_Bin_13), (Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_16), (Q2_y_Bin_8)-(z_pT_Bin_18), (Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_21), (Q2_y_Bin_8)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_28)
(Q2_y_Bin_8)-(z_pT_Bin_29), (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_9)-(z_pT_Bin_3)
(Q2_y_Bin_9)-(z_pT_Bin_4), (Q2_y_Bin_9)-(z_pT_Bin_8)

#### 150°

The rule does not fail every assessable manual exclusion: 3 of 49 pass.

Manually excluded but passes:

(Q2_y_Bin_11)-(z_pT_Bin_20), (Q2_y_Bin_15)-(z_pT_Bin_22), (Q2_y_Bin_9)-(z_pT_Bin_29)

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_15), (Q2_y_Bin_1)-(z_pT_Bin_16)
(Q2_y_Bin_1)-(z_pT_Bin_4), (Q2_y_Bin_1)-(z_pT_Bin_5), (Q2_y_Bin_1)-(z_pT_Bin_6)
(Q2_y_Bin_1)-(z_pT_Bin_9), (Q2_y_Bin_10)-(z_pT_Bin_2), (Q2_y_Bin_10)-(z_pT_Bin_3)
(Q2_y_Bin_10)-(z_pT_Bin_4), (Q2_y_Bin_10)-(z_pT_Bin_5), (Q2_y_Bin_10)-(z_pT_Bin_6)
(Q2_y_Bin_11)-(z_pT_Bin_1), (Q2_y_Bin_11)-(z_pT_Bin_2), (Q2_y_Bin_11)-(z_pT_Bin_21)
(Q2_y_Bin_11)-(z_pT_Bin_23), (Q2_y_Bin_11)-(z_pT_Bin_4), (Q2_y_Bin_12)-(z_pT_Bin_11)
(Q2_y_Bin_12)-(z_pT_Bin_22), (Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_6)
(Q2_y_Bin_12)-(z_pT_Bin_7), (Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_13)-(z_pT_Bin_1)
(Q2_y_Bin_13)-(z_pT_Bin_2), (Q2_y_Bin_14)-(z_pT_Bin_5), (Q2_y_Bin_15)-(z_pT_Bin_1)
(Q2_y_Bin_15)-(z_pT_Bin_2), (Q2_y_Bin_15)-(z_pT_Bin_23), (Q2_y_Bin_2)-(z_pT_Bin_10)
(Q2_y_Bin_2)-(z_pT_Bin_14), (Q2_y_Bin_2)-(z_pT_Bin_15), (Q2_y_Bin_2)-(z_pT_Bin_19)
(Q2_y_Bin_2)-(z_pT_Bin_20), (Q2_y_Bin_2)-(z_pT_Bin_25), (Q2_y_Bin_2)-(z_pT_Bin_32)
(Q2_y_Bin_2)-(z_pT_Bin_5), (Q2_y_Bin_2)-(z_pT_Bin_6), (Q2_y_Bin_2)-(z_pT_Bin_7)
(Q2_y_Bin_2)-(z_pT_Bin_9), (Q2_y_Bin_3)-(z_pT_Bin_1), (Q2_y_Bin_3)-(z_pT_Bin_10)
(Q2_y_Bin_3)-(z_pT_Bin_11), (Q2_y_Bin_3)-(z_pT_Bin_12), (Q2_y_Bin_3)-(z_pT_Bin_13)
(Q2_y_Bin_3)-(z_pT_Bin_15), (Q2_y_Bin_3)-(z_pT_Bin_16), (Q2_y_Bin_3)-(z_pT_Bin_18)
(Q2_y_Bin_3)-(z_pT_Bin_20), (Q2_y_Bin_3)-(z_pT_Bin_21), (Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_7)
(Q2_y_Bin_3)-(z_pT_Bin_8), (Q2_y_Bin_3)-(z_pT_Bin_9), (Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_13), (Q2_y_Bin_4)-(z_pT_Bin_14), (Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_19), (Q2_y_Bin_4)-(z_pT_Bin_21)
(Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_25), (Q2_y_Bin_4)-(z_pT_Bin_27)
(Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission], (Q2_y_Bin_5)-(z_pT_Bin_19)
(Q2_y_Bin_5)-(z_pT_Bin_25), (Q2_y_Bin_5)-(z_pT_Bin_3), (Q2_y_Bin_5)-(z_pT_Bin_31)
(Q2_y_Bin_5)-(z_pT_Bin_4), (Q2_y_Bin_5)-(z_pT_Bin_5), (Q2_y_Bin_5)-(z_pT_Bin_6)
(Q2_y_Bin_5)-(z_pT_Bin_8), (Q2_y_Bin_5)-(z_pT_Bin_9), (Q2_y_Bin_6)-(z_pT_Bin_1)
(Q2_y_Bin_6)-(z_pT_Bin_2), (Q2_y_Bin_6)-(z_pT_Bin_27), (Q2_y_Bin_6)-(z_pT_Bin_28)
(Q2_y_Bin_6)-(z_pT_Bin_3), (Q2_y_Bin_6)-(z_pT_Bin_4), (Q2_y_Bin_6)-(z_pT_Bin_5)
(Q2_y_Bin_6)-(z_pT_Bin_7), (Q2_y_Bin_6)-(z_pT_Bin_9), (Q2_y_Bin_7)-(z_pT_Bin_1)
(Q2_y_Bin_7)-(z_pT_Bin_11), (Q2_y_Bin_7)-(z_pT_Bin_12), (Q2_y_Bin_7)-(z_pT_Bin_13)
(Q2_y_Bin_7)-(z_pT_Bin_2), (Q2_y_Bin_7)-(z_pT_Bin_21), (Q2_y_Bin_7)-(z_pT_Bin_24)
(Q2_y_Bin_7)-(z_pT_Bin_31), (Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_11)
(Q2_y_Bin_8)-(z_pT_Bin_13), (Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16)
(Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_28)
(Q2_y_Bin_8)-(z_pT_Bin_29), (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_9)-(z_pT_Bin_3)
(Q2_y_Bin_9)-(z_pT_Bin_4)

#### 180°

The rule does not fail every assessable manual exclusion: 6 of 49 pass.

Manually excluded but passes:

(Q2_y_Bin_1)-(z_pT_Bin_22), (Q2_y_Bin_11)-(z_pT_Bin_20), (Q2_y_Bin_15)-(z_pT_Bin_22)
(Q2_y_Bin_2)-(z_pT_Bin_13), (Q2_y_Bin_2)-(z_pT_Bin_8), (Q2_y_Bin_9)-(z_pT_Bin_29)

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_15), (Q2_y_Bin_1)-(z_pT_Bin_4)
(Q2_y_Bin_1)-(z_pT_Bin_9), (Q2_y_Bin_10)-(z_pT_Bin_6), (Q2_y_Bin_11)-(z_pT_Bin_23)
(Q2_y_Bin_11)-(z_pT_Bin_4), (Q2_y_Bin_12)-(z_pT_Bin_11), (Q2_y_Bin_12)-(z_pT_Bin_22)
(Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_6), (Q2_y_Bin_12)-(z_pT_Bin_7)
(Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_2)-(z_pT_Bin_32), (Q2_y_Bin_2)-(z_pT_Bin_5)
(Q2_y_Bin_2)-(z_pT_Bin_6), (Q2_y_Bin_2)-(z_pT_Bin_7), (Q2_y_Bin_3)-(z_pT_Bin_1)
(Q2_y_Bin_3)-(z_pT_Bin_10), (Q2_y_Bin_3)-(z_pT_Bin_13), (Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_7)
(Q2_y_Bin_3)-(z_pT_Bin_9), (Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_13)
(Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_19)
(Q2_y_Bin_4)-(z_pT_Bin_21), (Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_25)
(Q2_y_Bin_4)-(z_pT_Bin_27), (Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission]
(Q2_y_Bin_5)-(z_pT_Bin_3), (Q2_y_Bin_5)-(z_pT_Bin_31), (Q2_y_Bin_5)-(z_pT_Bin_4)
(Q2_y_Bin_6)-(z_pT_Bin_2), (Q2_y_Bin_6)-(z_pT_Bin_7), (Q2_y_Bin_7)-(z_pT_Bin_12)
(Q2_y_Bin_7)-(z_pT_Bin_2), (Q2_y_Bin_7)-(z_pT_Bin_31), (Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_11), (Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16)
(Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_29)
(Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission]

### eS5o

Manual list entries: 46. Fit-quality omissions relative to the nominal acceptance bins: 36. Comparisons the budget still keeps: 375.

#### 90°

The rule fails every assessable manual exclusion (46).

Manually excluded but passes:

None.

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_11), (Q2_y_Bin_1)-(z_pT_Bin_15)
(Q2_y_Bin_1)-(z_pT_Bin_16), (Q2_y_Bin_1)-(z_pT_Bin_17), (Q2_y_Bin_1)-(z_pT_Bin_23)
(Q2_y_Bin_1)-(z_pT_Bin_30), (Q2_y_Bin_1)-(z_pT_Bin_31), (Q2_y_Bin_1)-(z_pT_Bin_32)
(Q2_y_Bin_1)-(z_pT_Bin_4), (Q2_y_Bin_1)-(z_pT_Bin_5), (Q2_y_Bin_1)-(z_pT_Bin_6)
(Q2_y_Bin_1)-(z_pT_Bin_7), (Q2_y_Bin_1)-(z_pT_Bin_8), (Q2_y_Bin_10)-(z_pT_Bin_1)
(Q2_y_Bin_10)-(z_pT_Bin_10), (Q2_y_Bin_10)-(z_pT_Bin_13), (Q2_y_Bin_10)-(z_pT_Bin_15)
(Q2_y_Bin_10)-(z_pT_Bin_2), (Q2_y_Bin_10)-(z_pT_Bin_20), (Q2_y_Bin_10)-(z_pT_Bin_26)
(Q2_y_Bin_10)-(z_pT_Bin_31), (Q2_y_Bin_10)-(z_pT_Bin_32), (Q2_y_Bin_10)-(z_pT_Bin_4)
(Q2_y_Bin_10)-(z_pT_Bin_5), (Q2_y_Bin_10)-(z_pT_Bin_6), (Q2_y_Bin_10)-(z_pT_Bin_7)
(Q2_y_Bin_10)-(z_pT_Bin_8), (Q2_y_Bin_10)-(z_pT_Bin_9), (Q2_y_Bin_11)-(z_pT_Bin_1)
(Q2_y_Bin_11)-(z_pT_Bin_10), (Q2_y_Bin_11)-(z_pT_Bin_11), (Q2_y_Bin_11)-(z_pT_Bin_13)
(Q2_y_Bin_11)-(z_pT_Bin_15), (Q2_y_Bin_11)-(z_pT_Bin_18), (Q2_y_Bin_11)-(z_pT_Bin_19)
(Q2_y_Bin_11)-(z_pT_Bin_2), (Q2_y_Bin_11)-(z_pT_Bin_20), (Q2_y_Bin_11)-(z_pT_Bin_21)
(Q2_y_Bin_11)-(z_pT_Bin_23), (Q2_y_Bin_11)-(z_pT_Bin_24), (Q2_y_Bin_11)-(z_pT_Bin_3)
(Q2_y_Bin_11)-(z_pT_Bin_6), (Q2_y_Bin_11)-(z_pT_Bin_8), (Q2_y_Bin_11)-(z_pT_Bin_9)
(Q2_y_Bin_12)-(z_pT_Bin_12), (Q2_y_Bin_12)-(z_pT_Bin_13), (Q2_y_Bin_12)-(z_pT_Bin_16)
(Q2_y_Bin_12)-(z_pT_Bin_18), (Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_13)-(z_pT_Bin_1), (Q2_y_Bin_13)-(z_pT_Bin_12), (Q2_y_Bin_13)-(z_pT_Bin_2)
(Q2_y_Bin_13)-(z_pT_Bin_26), (Q2_y_Bin_13)-(z_pT_Bin_3), (Q2_y_Bin_13)-(z_pT_Bin_4)
(Q2_y_Bin_13)-(z_pT_Bin_5), (Q2_y_Bin_13)-(z_pT_Bin_7), (Q2_y_Bin_13)-(z_pT_Bin_8)
(Q2_y_Bin_14)-(z_pT_Bin_1), (Q2_y_Bin_14)-(z_pT_Bin_2), (Q2_y_Bin_14)-(z_pT_Bin_3)
(Q2_y_Bin_14)-(z_pT_Bin_32), (Q2_y_Bin_14)-(z_pT_Bin_4), (Q2_y_Bin_14)-(z_pT_Bin_5)
(Q2_y_Bin_15)-(z_pT_Bin_1), (Q2_y_Bin_15)-(z_pT_Bin_15), (Q2_y_Bin_15)-(z_pT_Bin_19)
(Q2_y_Bin_15)-(z_pT_Bin_2), (Q2_y_Bin_15)-(z_pT_Bin_21), (Q2_y_Bin_15)-(z_pT_Bin_22)
(Q2_y_Bin_15)-(z_pT_Bin_23), (Q2_y_Bin_15)-(z_pT_Bin_6), (Q2_y_Bin_15)-(z_pT_Bin_9)
(Q2_y_Bin_16)-(z_pT_Bin_1), (Q2_y_Bin_16)-(z_pT_Bin_3), (Q2_y_Bin_16)-(z_pT_Bin_4)
(Q2_y_Bin_16)-(z_pT_Bin_5), (Q2_y_Bin_16)-(z_pT_Bin_6), (Q2_y_Bin_16)-(z_pT_Bin_9)
(Q2_y_Bin_17)-(z_pT_Bin_2), (Q2_y_Bin_17)-(z_pT_Bin_4), (Q2_y_Bin_2)-(z_pT_Bin_1)
(Q2_y_Bin_2)-(z_pT_Bin_10), (Q2_y_Bin_2)-(z_pT_Bin_11), (Q2_y_Bin_2)-(z_pT_Bin_12)
(Q2_y_Bin_2)-(z_pT_Bin_13), (Q2_y_Bin_2)-(z_pT_Bin_14), (Q2_y_Bin_2)-(z_pT_Bin_15)
(Q2_y_Bin_2)-(z_pT_Bin_16), (Q2_y_Bin_2)-(z_pT_Bin_18), (Q2_y_Bin_2)-(z_pT_Bin_19)
(Q2_y_Bin_2)-(z_pT_Bin_21), (Q2_y_Bin_2)-(z_pT_Bin_23), (Q2_y_Bin_2)-(z_pT_Bin_25)
(Q2_y_Bin_2)-(z_pT_Bin_26), (Q2_y_Bin_2)-(z_pT_Bin_27), (Q2_y_Bin_2)-(z_pT_Bin_28)
(Q2_y_Bin_2)-(z_pT_Bin_3), (Q2_y_Bin_2)-(z_pT_Bin_32), (Q2_y_Bin_2)-(z_pT_Bin_33)
(Q2_y_Bin_2)-(z_pT_Bin_34), (Q2_y_Bin_2)-(z_pT_Bin_4), (Q2_y_Bin_2)-(z_pT_Bin_5)
(Q2_y_Bin_2)-(z_pT_Bin_6), (Q2_y_Bin_2)-(z_pT_Bin_7), (Q2_y_Bin_2)-(z_pT_Bin_8)
(Q2_y_Bin_2)-(z_pT_Bin_9), (Q2_y_Bin_3)-(z_pT_Bin_1), (Q2_y_Bin_3)-(z_pT_Bin_10)
(Q2_y_Bin_3)-(z_pT_Bin_11), (Q2_y_Bin_3)-(z_pT_Bin_12), (Q2_y_Bin_3)-(z_pT_Bin_13)
(Q2_y_Bin_3)-(z_pT_Bin_14), (Q2_y_Bin_3)-(z_pT_Bin_16), (Q2_y_Bin_3)-(z_pT_Bin_17)
(Q2_y_Bin_3)-(z_pT_Bin_18), (Q2_y_Bin_3)-(z_pT_Bin_19), (Q2_y_Bin_3)-(z_pT_Bin_2)
(Q2_y_Bin_3)-(z_pT_Bin_20), (Q2_y_Bin_3)-(z_pT_Bin_21), (Q2_y_Bin_3)-(z_pT_Bin_22)
(Q2_y_Bin_3)-(z_pT_Bin_23), (Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_7)
(Q2_y_Bin_3)-(z_pT_Bin_8), (Q2_y_Bin_3)-(z_pT_Bin_9), (Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_13), (Q2_y_Bin_4)-(z_pT_Bin_14), (Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_19), (Q2_y_Bin_4)-(z_pT_Bin_20)
(Q2_y_Bin_4)-(z_pT_Bin_21), (Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_25)
(Q2_y_Bin_4)-(z_pT_Bin_26), (Q2_y_Bin_4)-(z_pT_Bin_27), (Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission], (Q2_y_Bin_5)-(z_pT_Bin_10), (Q2_y_Bin_5)-(z_pT_Bin_11)
(Q2_y_Bin_5)-(z_pT_Bin_13), (Q2_y_Bin_5)-(z_pT_Bin_14), (Q2_y_Bin_5)-(z_pT_Bin_15)
(Q2_y_Bin_5)-(z_pT_Bin_19), (Q2_y_Bin_5)-(z_pT_Bin_2), (Q2_y_Bin_5)-(z_pT_Bin_20)
(Q2_y_Bin_5)-(z_pT_Bin_26), (Q2_y_Bin_5)-(z_pT_Bin_3), (Q2_y_Bin_5)-(z_pT_Bin_32)
(Q2_y_Bin_5)-(z_pT_Bin_4), (Q2_y_Bin_5)-(z_pT_Bin_5), (Q2_y_Bin_5)-(z_pT_Bin_6)
(Q2_y_Bin_5)-(z_pT_Bin_8), (Q2_y_Bin_5)-(z_pT_Bin_9), (Q2_y_Bin_6)-(z_pT_Bin_1)
(Q2_y_Bin_6)-(z_pT_Bin_10), (Q2_y_Bin_6)-(z_pT_Bin_11), (Q2_y_Bin_6)-(z_pT_Bin_13)
(Q2_y_Bin_6)-(z_pT_Bin_14), (Q2_y_Bin_6)-(z_pT_Bin_15), (Q2_y_Bin_6)-(z_pT_Bin_19)
(Q2_y_Bin_6)-(z_pT_Bin_2), (Q2_y_Bin_6)-(z_pT_Bin_20), (Q2_y_Bin_6)-(z_pT_Bin_27)
(Q2_y_Bin_6)-(z_pT_Bin_28), (Q2_y_Bin_6)-(z_pT_Bin_3), (Q2_y_Bin_6)-(z_pT_Bin_5)
(Q2_y_Bin_6)-(z_pT_Bin_6), (Q2_y_Bin_6)-(z_pT_Bin_7), (Q2_y_Bin_6)-(z_pT_Bin_8)
(Q2_y_Bin_6)-(z_pT_Bin_9), (Q2_y_Bin_7)-(z_pT_Bin_1), (Q2_y_Bin_7)-(z_pT_Bin_10)
(Q2_y_Bin_7)-(z_pT_Bin_11), (Q2_y_Bin_7)-(z_pT_Bin_12), (Q2_y_Bin_7)-(z_pT_Bin_13)
(Q2_y_Bin_7)-(z_pT_Bin_14), (Q2_y_Bin_7)-(z_pT_Bin_15), (Q2_y_Bin_7)-(z_pT_Bin_16)
(Q2_y_Bin_7)-(z_pT_Bin_17), (Q2_y_Bin_7)-(z_pT_Bin_18), (Q2_y_Bin_7)-(z_pT_Bin_19)
(Q2_y_Bin_7)-(z_pT_Bin_2), (Q2_y_Bin_7)-(z_pT_Bin_20), (Q2_y_Bin_7)-(z_pT_Bin_22)
(Q2_y_Bin_7)-(z_pT_Bin_23), (Q2_y_Bin_7)-(z_pT_Bin_24), (Q2_y_Bin_7)-(z_pT_Bin_25)
(Q2_y_Bin_7)-(z_pT_Bin_26), (Q2_y_Bin_7)-(z_pT_Bin_27), (Q2_y_Bin_7)-(z_pT_Bin_28)
(Q2_y_Bin_7)-(z_pT_Bin_29), (Q2_y_Bin_7)-(z_pT_Bin_33), (Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission]
(Q2_y_Bin_7)-(z_pT_Bin_7), (Q2_y_Bin_7)-(z_pT_Bin_8), (Q2_y_Bin_7)-(z_pT_Bin_9)
(Q2_y_Bin_8)-(z_pT_Bin_11), (Q2_y_Bin_8)-(z_pT_Bin_12), (Q2_y_Bin_8)-(z_pT_Bin_13)
(Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16), (Q2_y_Bin_8)-(z_pT_Bin_17)
(Q2_y_Bin_8)-(z_pT_Bin_18), (Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_21)
(Q2_y_Bin_8)-(z_pT_Bin_23), (Q2_y_Bin_8)-(z_pT_Bin_26), (Q2_y_Bin_8)-(z_pT_Bin_28)
(Q2_y_Bin_8)-(z_pT_Bin_29), (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_9)-(z_pT_Bin_1)
(Q2_y_Bin_9)-(z_pT_Bin_10), (Q2_y_Bin_9)-(z_pT_Bin_15), (Q2_y_Bin_9)-(z_pT_Bin_16)
(Q2_y_Bin_9)-(z_pT_Bin_22), (Q2_y_Bin_9)-(z_pT_Bin_3), (Q2_y_Bin_9)-(z_pT_Bin_4)
(Q2_y_Bin_9)-(z_pT_Bin_5), (Q2_y_Bin_9)-(z_pT_Bin_6), (Q2_y_Bin_9)-(z_pT_Bin_8)
(Q2_y_Bin_9)-(z_pT_Bin_9)

#### 120°

The rule fails every assessable manual exclusion (46).

Manually excluded but passes:

None.

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_15), (Q2_y_Bin_1)-(z_pT_Bin_16)
(Q2_y_Bin_1)-(z_pT_Bin_23), (Q2_y_Bin_1)-(z_pT_Bin_30), (Q2_y_Bin_1)-(z_pT_Bin_31)
(Q2_y_Bin_1)-(z_pT_Bin_4), (Q2_y_Bin_1)-(z_pT_Bin_5), (Q2_y_Bin_1)-(z_pT_Bin_6)
(Q2_y_Bin_1)-(z_pT_Bin_7), (Q2_y_Bin_1)-(z_pT_Bin_8), (Q2_y_Bin_10)-(z_pT_Bin_1)
(Q2_y_Bin_10)-(z_pT_Bin_2), (Q2_y_Bin_10)-(z_pT_Bin_31), (Q2_y_Bin_10)-(z_pT_Bin_32)
(Q2_y_Bin_10)-(z_pT_Bin_4), (Q2_y_Bin_10)-(z_pT_Bin_5), (Q2_y_Bin_10)-(z_pT_Bin_6)
(Q2_y_Bin_10)-(z_pT_Bin_7), (Q2_y_Bin_11)-(z_pT_Bin_1), (Q2_y_Bin_11)-(z_pT_Bin_10)
(Q2_y_Bin_11)-(z_pT_Bin_2), (Q2_y_Bin_11)-(z_pT_Bin_20), (Q2_y_Bin_11)-(z_pT_Bin_21)
(Q2_y_Bin_11)-(z_pT_Bin_23), (Q2_y_Bin_11)-(z_pT_Bin_24), (Q2_y_Bin_11)-(z_pT_Bin_3)
(Q2_y_Bin_11)-(z_pT_Bin_6), (Q2_y_Bin_12)-(z_pT_Bin_16), (Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission]
(Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_13)-(z_pT_Bin_1), (Q2_y_Bin_13)-(z_pT_Bin_2)
(Q2_y_Bin_13)-(z_pT_Bin_3), (Q2_y_Bin_13)-(z_pT_Bin_4), (Q2_y_Bin_14)-(z_pT_Bin_2)
(Q2_y_Bin_14)-(z_pT_Bin_3), (Q2_y_Bin_14)-(z_pT_Bin_4), (Q2_y_Bin_14)-(z_pT_Bin_5)
(Q2_y_Bin_15)-(z_pT_Bin_1), (Q2_y_Bin_15)-(z_pT_Bin_15), (Q2_y_Bin_15)-(z_pT_Bin_2)
(Q2_y_Bin_15)-(z_pT_Bin_22), (Q2_y_Bin_15)-(z_pT_Bin_23), (Q2_y_Bin_15)-(z_pT_Bin_9)
(Q2_y_Bin_16)-(z_pT_Bin_6), (Q2_y_Bin_17)-(z_pT_Bin_4), (Q2_y_Bin_2)-(z_pT_Bin_1)
(Q2_y_Bin_2)-(z_pT_Bin_10), (Q2_y_Bin_2)-(z_pT_Bin_11), (Q2_y_Bin_2)-(z_pT_Bin_13)
(Q2_y_Bin_2)-(z_pT_Bin_14), (Q2_y_Bin_2)-(z_pT_Bin_15), (Q2_y_Bin_2)-(z_pT_Bin_16)
(Q2_y_Bin_2)-(z_pT_Bin_19), (Q2_y_Bin_2)-(z_pT_Bin_25), (Q2_y_Bin_2)-(z_pT_Bin_26)
(Q2_y_Bin_2)-(z_pT_Bin_3), (Q2_y_Bin_2)-(z_pT_Bin_32), (Q2_y_Bin_2)-(z_pT_Bin_33)
(Q2_y_Bin_2)-(z_pT_Bin_34), (Q2_y_Bin_2)-(z_pT_Bin_4), (Q2_y_Bin_2)-(z_pT_Bin_5)
(Q2_y_Bin_2)-(z_pT_Bin_6), (Q2_y_Bin_2)-(z_pT_Bin_7), (Q2_y_Bin_2)-(z_pT_Bin_8)
(Q2_y_Bin_2)-(z_pT_Bin_9), (Q2_y_Bin_3)-(z_pT_Bin_1), (Q2_y_Bin_3)-(z_pT_Bin_10)
(Q2_y_Bin_3)-(z_pT_Bin_11), (Q2_y_Bin_3)-(z_pT_Bin_12), (Q2_y_Bin_3)-(z_pT_Bin_13)
(Q2_y_Bin_3)-(z_pT_Bin_14), (Q2_y_Bin_3)-(z_pT_Bin_16), (Q2_y_Bin_3)-(z_pT_Bin_17)
(Q2_y_Bin_3)-(z_pT_Bin_18), (Q2_y_Bin_3)-(z_pT_Bin_19), (Q2_y_Bin_3)-(z_pT_Bin_2)
(Q2_y_Bin_3)-(z_pT_Bin_20), (Q2_y_Bin_3)-(z_pT_Bin_21), (Q2_y_Bin_3)-(z_pT_Bin_22)
(Q2_y_Bin_3)-(z_pT_Bin_23), (Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_7)
(Q2_y_Bin_3)-(z_pT_Bin_8), (Q2_y_Bin_3)-(z_pT_Bin_9), (Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_13), (Q2_y_Bin_4)-(z_pT_Bin_14), (Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_19), (Q2_y_Bin_4)-(z_pT_Bin_20)
(Q2_y_Bin_4)-(z_pT_Bin_21), (Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_25)
(Q2_y_Bin_4)-(z_pT_Bin_26), (Q2_y_Bin_4)-(z_pT_Bin_27), (Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission], (Q2_y_Bin_5)-(z_pT_Bin_10), (Q2_y_Bin_5)-(z_pT_Bin_13)
(Q2_y_Bin_5)-(z_pT_Bin_14), (Q2_y_Bin_5)-(z_pT_Bin_15), (Q2_y_Bin_5)-(z_pT_Bin_19)
(Q2_y_Bin_5)-(z_pT_Bin_2), (Q2_y_Bin_5)-(z_pT_Bin_20), (Q2_y_Bin_5)-(z_pT_Bin_3)
(Q2_y_Bin_5)-(z_pT_Bin_32), (Q2_y_Bin_5)-(z_pT_Bin_4), (Q2_y_Bin_5)-(z_pT_Bin_5)
(Q2_y_Bin_5)-(z_pT_Bin_6), (Q2_y_Bin_5)-(z_pT_Bin_8), (Q2_y_Bin_5)-(z_pT_Bin_9)
(Q2_y_Bin_6)-(z_pT_Bin_1), (Q2_y_Bin_6)-(z_pT_Bin_10), (Q2_y_Bin_6)-(z_pT_Bin_14)
(Q2_y_Bin_6)-(z_pT_Bin_15), (Q2_y_Bin_6)-(z_pT_Bin_19), (Q2_y_Bin_6)-(z_pT_Bin_2)
(Q2_y_Bin_6)-(z_pT_Bin_20), (Q2_y_Bin_6)-(z_pT_Bin_27), (Q2_y_Bin_6)-(z_pT_Bin_28)
(Q2_y_Bin_6)-(z_pT_Bin_3), (Q2_y_Bin_6)-(z_pT_Bin_5), (Q2_y_Bin_6)-(z_pT_Bin_6)
(Q2_y_Bin_6)-(z_pT_Bin_7), (Q2_y_Bin_6)-(z_pT_Bin_8), (Q2_y_Bin_6)-(z_pT_Bin_9)
(Q2_y_Bin_7)-(z_pT_Bin_1), (Q2_y_Bin_7)-(z_pT_Bin_10), (Q2_y_Bin_7)-(z_pT_Bin_11)
(Q2_y_Bin_7)-(z_pT_Bin_12), (Q2_y_Bin_7)-(z_pT_Bin_13), (Q2_y_Bin_7)-(z_pT_Bin_15)
(Q2_y_Bin_7)-(z_pT_Bin_16), (Q2_y_Bin_7)-(z_pT_Bin_17), (Q2_y_Bin_7)-(z_pT_Bin_18)
(Q2_y_Bin_7)-(z_pT_Bin_2), (Q2_y_Bin_7)-(z_pT_Bin_22), (Q2_y_Bin_7)-(z_pT_Bin_23)
(Q2_y_Bin_7)-(z_pT_Bin_24), (Q2_y_Bin_7)-(z_pT_Bin_26), (Q2_y_Bin_7)-(z_pT_Bin_27)
(Q2_y_Bin_7)-(z_pT_Bin_29), (Q2_y_Bin_7)-(z_pT_Bin_33), (Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission]
(Q2_y_Bin_7)-(z_pT_Bin_7), (Q2_y_Bin_7)-(z_pT_Bin_8), (Q2_y_Bin_7)-(z_pT_Bin_9)
(Q2_y_Bin_8)-(z_pT_Bin_11), (Q2_y_Bin_8)-(z_pT_Bin_12), (Q2_y_Bin_8)-(z_pT_Bin_13)
(Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16), (Q2_y_Bin_8)-(z_pT_Bin_18)
(Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_21), (Q2_y_Bin_8)-(z_pT_Bin_23)
(Q2_y_Bin_8)-(z_pT_Bin_26), (Q2_y_Bin_8)-(z_pT_Bin_28), (Q2_y_Bin_8)-(z_pT_Bin_29)
(Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_9)-(z_pT_Bin_1), (Q2_y_Bin_9)-(z_pT_Bin_10)
(Q2_y_Bin_9)-(z_pT_Bin_15), (Q2_y_Bin_9)-(z_pT_Bin_3), (Q2_y_Bin_9)-(z_pT_Bin_4)
(Q2_y_Bin_9)-(z_pT_Bin_5), (Q2_y_Bin_9)-(z_pT_Bin_6), (Q2_y_Bin_9)-(z_pT_Bin_8)

#### 135°

The rule fails every assessable manual exclusion (46).

Manually excluded but passes:

None.

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_15), (Q2_y_Bin_1)-(z_pT_Bin_16)
(Q2_y_Bin_1)-(z_pT_Bin_23), (Q2_y_Bin_1)-(z_pT_Bin_30), (Q2_y_Bin_1)-(z_pT_Bin_31)
(Q2_y_Bin_1)-(z_pT_Bin_4), (Q2_y_Bin_1)-(z_pT_Bin_5), (Q2_y_Bin_1)-(z_pT_Bin_6)
(Q2_y_Bin_1)-(z_pT_Bin_7), (Q2_y_Bin_1)-(z_pT_Bin_8), (Q2_y_Bin_10)-(z_pT_Bin_1)
(Q2_y_Bin_10)-(z_pT_Bin_2), (Q2_y_Bin_10)-(z_pT_Bin_32), (Q2_y_Bin_10)-(z_pT_Bin_4)
(Q2_y_Bin_10)-(z_pT_Bin_5), (Q2_y_Bin_10)-(z_pT_Bin_6), (Q2_y_Bin_10)-(z_pT_Bin_7)
(Q2_y_Bin_11)-(z_pT_Bin_1), (Q2_y_Bin_11)-(z_pT_Bin_10), (Q2_y_Bin_11)-(z_pT_Bin_2)
(Q2_y_Bin_11)-(z_pT_Bin_20), (Q2_y_Bin_11)-(z_pT_Bin_21), (Q2_y_Bin_11)-(z_pT_Bin_23)
(Q2_y_Bin_11)-(z_pT_Bin_24), (Q2_y_Bin_11)-(z_pT_Bin_3), (Q2_y_Bin_11)-(z_pT_Bin_6)
(Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_13)-(z_pT_Bin_1)
(Q2_y_Bin_13)-(z_pT_Bin_2), (Q2_y_Bin_14)-(z_pT_Bin_2), (Q2_y_Bin_14)-(z_pT_Bin_4)
(Q2_y_Bin_14)-(z_pT_Bin_5), (Q2_y_Bin_15)-(z_pT_Bin_1), (Q2_y_Bin_15)-(z_pT_Bin_15)
(Q2_y_Bin_15)-(z_pT_Bin_2), (Q2_y_Bin_15)-(z_pT_Bin_22), (Q2_y_Bin_15)-(z_pT_Bin_23)
(Q2_y_Bin_15)-(z_pT_Bin_9), (Q2_y_Bin_16)-(z_pT_Bin_6), (Q2_y_Bin_17)-(z_pT_Bin_4)
(Q2_y_Bin_2)-(z_pT_Bin_1), (Q2_y_Bin_2)-(z_pT_Bin_10), (Q2_y_Bin_2)-(z_pT_Bin_13)
(Q2_y_Bin_2)-(z_pT_Bin_14), (Q2_y_Bin_2)-(z_pT_Bin_15), (Q2_y_Bin_2)-(z_pT_Bin_16)
(Q2_y_Bin_2)-(z_pT_Bin_19), (Q2_y_Bin_2)-(z_pT_Bin_25), (Q2_y_Bin_2)-(z_pT_Bin_3)
(Q2_y_Bin_2)-(z_pT_Bin_32), (Q2_y_Bin_2)-(z_pT_Bin_33), (Q2_y_Bin_2)-(z_pT_Bin_34)
(Q2_y_Bin_2)-(z_pT_Bin_4), (Q2_y_Bin_2)-(z_pT_Bin_5), (Q2_y_Bin_2)-(z_pT_Bin_6)
(Q2_y_Bin_2)-(z_pT_Bin_7), (Q2_y_Bin_2)-(z_pT_Bin_8), (Q2_y_Bin_2)-(z_pT_Bin_9)
(Q2_y_Bin_3)-(z_pT_Bin_1), (Q2_y_Bin_3)-(z_pT_Bin_10), (Q2_y_Bin_3)-(z_pT_Bin_11)
(Q2_y_Bin_3)-(z_pT_Bin_12), (Q2_y_Bin_3)-(z_pT_Bin_13), (Q2_y_Bin_3)-(z_pT_Bin_14)
(Q2_y_Bin_3)-(z_pT_Bin_16), (Q2_y_Bin_3)-(z_pT_Bin_17), (Q2_y_Bin_3)-(z_pT_Bin_18)
(Q2_y_Bin_3)-(z_pT_Bin_19), (Q2_y_Bin_3)-(z_pT_Bin_2), (Q2_y_Bin_3)-(z_pT_Bin_20)
(Q2_y_Bin_3)-(z_pT_Bin_21), (Q2_y_Bin_3)-(z_pT_Bin_22), (Q2_y_Bin_3)-(z_pT_Bin_23)
(Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_7), (Q2_y_Bin_3)-(z_pT_Bin_8)
(Q2_y_Bin_3)-(z_pT_Bin_9), (Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_13)
(Q2_y_Bin_4)-(z_pT_Bin_14), (Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_19), (Q2_y_Bin_4)-(z_pT_Bin_20), (Q2_y_Bin_4)-(z_pT_Bin_21)
(Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_25), (Q2_y_Bin_4)-(z_pT_Bin_26)
(Q2_y_Bin_4)-(z_pT_Bin_27), (Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission]
(Q2_y_Bin_5)-(z_pT_Bin_10), (Q2_y_Bin_5)-(z_pT_Bin_13), (Q2_y_Bin_5)-(z_pT_Bin_14)
(Q2_y_Bin_5)-(z_pT_Bin_15), (Q2_y_Bin_5)-(z_pT_Bin_19), (Q2_y_Bin_5)-(z_pT_Bin_2)
(Q2_y_Bin_5)-(z_pT_Bin_3), (Q2_y_Bin_5)-(z_pT_Bin_32), (Q2_y_Bin_5)-(z_pT_Bin_4)
(Q2_y_Bin_5)-(z_pT_Bin_5), (Q2_y_Bin_5)-(z_pT_Bin_6), (Q2_y_Bin_5)-(z_pT_Bin_8)
(Q2_y_Bin_5)-(z_pT_Bin_9), (Q2_y_Bin_6)-(z_pT_Bin_1), (Q2_y_Bin_6)-(z_pT_Bin_10)
(Q2_y_Bin_6)-(z_pT_Bin_14), (Q2_y_Bin_6)-(z_pT_Bin_2), (Q2_y_Bin_6)-(z_pT_Bin_20)
(Q2_y_Bin_6)-(z_pT_Bin_27), (Q2_y_Bin_6)-(z_pT_Bin_28), (Q2_y_Bin_6)-(z_pT_Bin_3)
(Q2_y_Bin_6)-(z_pT_Bin_5), (Q2_y_Bin_6)-(z_pT_Bin_6), (Q2_y_Bin_6)-(z_pT_Bin_7)
(Q2_y_Bin_6)-(z_pT_Bin_8), (Q2_y_Bin_6)-(z_pT_Bin_9), (Q2_y_Bin_7)-(z_pT_Bin_1)
(Q2_y_Bin_7)-(z_pT_Bin_10), (Q2_y_Bin_7)-(z_pT_Bin_11), (Q2_y_Bin_7)-(z_pT_Bin_12)
(Q2_y_Bin_7)-(z_pT_Bin_13), (Q2_y_Bin_7)-(z_pT_Bin_16), (Q2_y_Bin_7)-(z_pT_Bin_17)
(Q2_y_Bin_7)-(z_pT_Bin_18), (Q2_y_Bin_7)-(z_pT_Bin_2), (Q2_y_Bin_7)-(z_pT_Bin_24)
(Q2_y_Bin_7)-(z_pT_Bin_26), (Q2_y_Bin_7)-(z_pT_Bin_27), (Q2_y_Bin_7)-(z_pT_Bin_29)
(Q2_y_Bin_7)-(z_pT_Bin_33), (Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_7)-(z_pT_Bin_7)
(Q2_y_Bin_7)-(z_pT_Bin_9), (Q2_y_Bin_8)-(z_pT_Bin_11), (Q2_y_Bin_8)-(z_pT_Bin_12)
(Q2_y_Bin_8)-(z_pT_Bin_13), (Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16)
(Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_21), (Q2_y_Bin_8)-(z_pT_Bin_23)
(Q2_y_Bin_8)-(z_pT_Bin_28), (Q2_y_Bin_8)-(z_pT_Bin_29), (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_9)-(z_pT_Bin_1), (Q2_y_Bin_9)-(z_pT_Bin_3), (Q2_y_Bin_9)-(z_pT_Bin_4)
(Q2_y_Bin_9)-(z_pT_Bin_8)

#### 150°

The rule fails every assessable manual exclusion (46).

Manually excluded but passes:

None.

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_15), (Q2_y_Bin_1)-(z_pT_Bin_16)
(Q2_y_Bin_1)-(z_pT_Bin_30), (Q2_y_Bin_1)-(z_pT_Bin_4), (Q2_y_Bin_1)-(z_pT_Bin_5)
(Q2_y_Bin_1)-(z_pT_Bin_6), (Q2_y_Bin_1)-(z_pT_Bin_8), (Q2_y_Bin_10)-(z_pT_Bin_2)
(Q2_y_Bin_10)-(z_pT_Bin_4), (Q2_y_Bin_10)-(z_pT_Bin_5), (Q2_y_Bin_10)-(z_pT_Bin_6)
(Q2_y_Bin_10)-(z_pT_Bin_7), (Q2_y_Bin_11)-(z_pT_Bin_1), (Q2_y_Bin_11)-(z_pT_Bin_2)
(Q2_y_Bin_11)-(z_pT_Bin_21), (Q2_y_Bin_11)-(z_pT_Bin_23), (Q2_y_Bin_11)-(z_pT_Bin_24)
(Q2_y_Bin_11)-(z_pT_Bin_3), (Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_13)-(z_pT_Bin_1), (Q2_y_Bin_13)-(z_pT_Bin_2), (Q2_y_Bin_14)-(z_pT_Bin_2)
(Q2_y_Bin_14)-(z_pT_Bin_4), (Q2_y_Bin_14)-(z_pT_Bin_5), (Q2_y_Bin_15)-(z_pT_Bin_1)
(Q2_y_Bin_15)-(z_pT_Bin_15), (Q2_y_Bin_15)-(z_pT_Bin_2), (Q2_y_Bin_15)-(z_pT_Bin_22)
(Q2_y_Bin_15)-(z_pT_Bin_23), (Q2_y_Bin_17)-(z_pT_Bin_4), (Q2_y_Bin_2)-(z_pT_Bin_1)
(Q2_y_Bin_2)-(z_pT_Bin_10), (Q2_y_Bin_2)-(z_pT_Bin_13), (Q2_y_Bin_2)-(z_pT_Bin_14)
(Q2_y_Bin_2)-(z_pT_Bin_15), (Q2_y_Bin_2)-(z_pT_Bin_19), (Q2_y_Bin_2)-(z_pT_Bin_25)
(Q2_y_Bin_2)-(z_pT_Bin_3), (Q2_y_Bin_2)-(z_pT_Bin_32), (Q2_y_Bin_2)-(z_pT_Bin_4)
(Q2_y_Bin_2)-(z_pT_Bin_5), (Q2_y_Bin_2)-(z_pT_Bin_6), (Q2_y_Bin_2)-(z_pT_Bin_7)
(Q2_y_Bin_2)-(z_pT_Bin_8), (Q2_y_Bin_2)-(z_pT_Bin_9), (Q2_y_Bin_3)-(z_pT_Bin_1)
(Q2_y_Bin_3)-(z_pT_Bin_10), (Q2_y_Bin_3)-(z_pT_Bin_11), (Q2_y_Bin_3)-(z_pT_Bin_12)
(Q2_y_Bin_3)-(z_pT_Bin_13), (Q2_y_Bin_3)-(z_pT_Bin_18), (Q2_y_Bin_3)-(z_pT_Bin_2)
(Q2_y_Bin_3)-(z_pT_Bin_20), (Q2_y_Bin_3)-(z_pT_Bin_21), (Q2_y_Bin_3)-(z_pT_Bin_23)
(Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_7), (Q2_y_Bin_3)-(z_pT_Bin_8)
(Q2_y_Bin_3)-(z_pT_Bin_9), (Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_13)
(Q2_y_Bin_4)-(z_pT_Bin_14), (Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_19), (Q2_y_Bin_4)-(z_pT_Bin_21), (Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_25), (Q2_y_Bin_4)-(z_pT_Bin_27), (Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission], (Q2_y_Bin_5)-(z_pT_Bin_10), (Q2_y_Bin_5)-(z_pT_Bin_13)
(Q2_y_Bin_5)-(z_pT_Bin_14), (Q2_y_Bin_5)-(z_pT_Bin_19), (Q2_y_Bin_5)-(z_pT_Bin_2)
(Q2_y_Bin_5)-(z_pT_Bin_3), (Q2_y_Bin_5)-(z_pT_Bin_32), (Q2_y_Bin_5)-(z_pT_Bin_4)
(Q2_y_Bin_5)-(z_pT_Bin_5), (Q2_y_Bin_5)-(z_pT_Bin_6), (Q2_y_Bin_5)-(z_pT_Bin_8)
(Q2_y_Bin_5)-(z_pT_Bin_9), (Q2_y_Bin_6)-(z_pT_Bin_1), (Q2_y_Bin_6)-(z_pT_Bin_14)
(Q2_y_Bin_6)-(z_pT_Bin_2), (Q2_y_Bin_6)-(z_pT_Bin_20), (Q2_y_Bin_6)-(z_pT_Bin_27)
(Q2_y_Bin_6)-(z_pT_Bin_28), (Q2_y_Bin_6)-(z_pT_Bin_3), (Q2_y_Bin_6)-(z_pT_Bin_5)
(Q2_y_Bin_6)-(z_pT_Bin_6), (Q2_y_Bin_6)-(z_pT_Bin_7), (Q2_y_Bin_6)-(z_pT_Bin_9)
(Q2_y_Bin_7)-(z_pT_Bin_1), (Q2_y_Bin_7)-(z_pT_Bin_11), (Q2_y_Bin_7)-(z_pT_Bin_12)
(Q2_y_Bin_7)-(z_pT_Bin_13), (Q2_y_Bin_7)-(z_pT_Bin_2), (Q2_y_Bin_7)-(z_pT_Bin_24)
(Q2_y_Bin_7)-(z_pT_Bin_29), (Q2_y_Bin_7)-(z_pT_Bin_33), (Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission]
(Q2_y_Bin_7)-(z_pT_Bin_7), (Q2_y_Bin_8)-(z_pT_Bin_11), (Q2_y_Bin_8)-(z_pT_Bin_13)
(Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16), (Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_21), (Q2_y_Bin_8)-(z_pT_Bin_28), (Q2_y_Bin_8)-(z_pT_Bin_29)
(Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_9)-(z_pT_Bin_1), (Q2_y_Bin_9)-(z_pT_Bin_3)
(Q2_y_Bin_9)-(z_pT_Bin_4)

#### 180°

The rule does not fail every assessable manual exclusion: 6 of 46 pass.

Manually excluded but passes:

(Q2_y_Bin_1)-(z_pT_Bin_22), (Q2_y_Bin_10)-(z_pT_Bin_3), (Q2_y_Bin_5)-(z_pT_Bin_25)
(Q2_y_Bin_6)-(z_pT_Bin_4), (Q2_y_Bin_7)-(z_pT_Bin_21), (Q2_y_Bin_9)-(z_pT_Bin_2)

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_15), (Q2_y_Bin_1)-(z_pT_Bin_30), (Q2_y_Bin_1)-(z_pT_Bin_4)
(Q2_y_Bin_1)-(z_pT_Bin_5), (Q2_y_Bin_1)-(z_pT_Bin_8), (Q2_y_Bin_10)-(z_pT_Bin_2)
(Q2_y_Bin_10)-(z_pT_Bin_6), (Q2_y_Bin_11)-(z_pT_Bin_23), (Q2_y_Bin_11)-(z_pT_Bin_24)
(Q2_y_Bin_11)-(z_pT_Bin_3), (Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_13)-(z_pT_Bin_1), (Q2_y_Bin_14)-(z_pT_Bin_5), (Q2_y_Bin_15)-(z_pT_Bin_15)
(Q2_y_Bin_15)-(z_pT_Bin_2), (Q2_y_Bin_15)-(z_pT_Bin_23), (Q2_y_Bin_2)-(z_pT_Bin_1)
(Q2_y_Bin_2)-(z_pT_Bin_19), (Q2_y_Bin_2)-(z_pT_Bin_3), (Q2_y_Bin_2)-(z_pT_Bin_4)
(Q2_y_Bin_2)-(z_pT_Bin_5), (Q2_y_Bin_2)-(z_pT_Bin_6), (Q2_y_Bin_2)-(z_pT_Bin_7)
(Q2_y_Bin_2)-(z_pT_Bin_9), (Q2_y_Bin_3)-(z_pT_Bin_1), (Q2_y_Bin_3)-(z_pT_Bin_10)
(Q2_y_Bin_3)-(z_pT_Bin_12), (Q2_y_Bin_3)-(z_pT_Bin_13), (Q2_y_Bin_3)-(z_pT_Bin_2)
(Q2_y_Bin_3)-(z_pT_Bin_20), (Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_7)
(Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_13), (Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_19), (Q2_y_Bin_4)-(z_pT_Bin_21)
(Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_25), (Q2_y_Bin_4)-(z_pT_Bin_27)
(Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission], (Q2_y_Bin_5)-(z_pT_Bin_13)
(Q2_y_Bin_5)-(z_pT_Bin_2), (Q2_y_Bin_5)-(z_pT_Bin_3), (Q2_y_Bin_5)-(z_pT_Bin_4)
(Q2_y_Bin_5)-(z_pT_Bin_5), (Q2_y_Bin_6)-(z_pT_Bin_2), (Q2_y_Bin_7)-(z_pT_Bin_1)
(Q2_y_Bin_7)-(z_pT_Bin_12), (Q2_y_Bin_7)-(z_pT_Bin_13), (Q2_y_Bin_7)-(z_pT_Bin_2)
(Q2_y_Bin_7)-(z_pT_Bin_33), (Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_11)
(Q2_y_Bin_8)-(z_pT_Bin_13), (Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16)
(Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_29), (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_9)-(z_pT_Bin_1)

### eS6o

Manual list entries: 59. Fit-quality omissions relative to the nominal acceptance bins: 38. Comparisons the budget still keeps: 362.

#### 90°

The rule fails every assessable manual exclusion (59).

Manually excluded but passes:

None.

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_11), (Q2_y_Bin_1)-(z_pT_Bin_16)
(Q2_y_Bin_1)-(z_pT_Bin_17), (Q2_y_Bin_1)-(z_pT_Bin_23), (Q2_y_Bin_1)-(z_pT_Bin_30)
(Q2_y_Bin_1)-(z_pT_Bin_31), (Q2_y_Bin_1)-(z_pT_Bin_32), (Q2_y_Bin_1)-(z_pT_Bin_4)
(Q2_y_Bin_1)-(z_pT_Bin_5), (Q2_y_Bin_1)-(z_pT_Bin_6), (Q2_y_Bin_1)-(z_pT_Bin_7)
(Q2_y_Bin_10)-(z_pT_Bin_1), (Q2_y_Bin_10)-(z_pT_Bin_10), (Q2_y_Bin_10)-(z_pT_Bin_11)
(Q2_y_Bin_10)-(z_pT_Bin_15), (Q2_y_Bin_10)-(z_pT_Bin_2), (Q2_y_Bin_10)-(z_pT_Bin_20)
(Q2_y_Bin_10)-(z_pT_Bin_26), (Q2_y_Bin_10)-(z_pT_Bin_3), (Q2_y_Bin_10)-(z_pT_Bin_31)
(Q2_y_Bin_10)-(z_pT_Bin_32), (Q2_y_Bin_10)-(z_pT_Bin_4), (Q2_y_Bin_10)-(z_pT_Bin_5)
(Q2_y_Bin_10)-(z_pT_Bin_6), (Q2_y_Bin_10)-(z_pT_Bin_7), (Q2_y_Bin_10)-(z_pT_Bin_8)
(Q2_y_Bin_10)-(z_pT_Bin_9), (Q2_y_Bin_11)-(z_pT_Bin_1), (Q2_y_Bin_11)-(z_pT_Bin_10)
(Q2_y_Bin_11)-(z_pT_Bin_11), (Q2_y_Bin_11)-(z_pT_Bin_13), (Q2_y_Bin_11)-(z_pT_Bin_15)
(Q2_y_Bin_11)-(z_pT_Bin_18), (Q2_y_Bin_11)-(z_pT_Bin_19), (Q2_y_Bin_11)-(z_pT_Bin_2)
(Q2_y_Bin_11)-(z_pT_Bin_20), (Q2_y_Bin_11)-(z_pT_Bin_21), (Q2_y_Bin_11)-(z_pT_Bin_22)
(Q2_y_Bin_11)-(z_pT_Bin_23), (Q2_y_Bin_11)-(z_pT_Bin_24), (Q2_y_Bin_11)-(z_pT_Bin_3)
(Q2_y_Bin_11)-(z_pT_Bin_6), (Q2_y_Bin_11)-(z_pT_Bin_8), (Q2_y_Bin_11)-(z_pT_Bin_9)
(Q2_y_Bin_12)-(z_pT_Bin_12), (Q2_y_Bin_12)-(z_pT_Bin_13), (Q2_y_Bin_12)-(z_pT_Bin_16)
(Q2_y_Bin_12)-(z_pT_Bin_18), (Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_13)-(z_pT_Bin_1), (Q2_y_Bin_13)-(z_pT_Bin_12), (Q2_y_Bin_13)-(z_pT_Bin_2)
(Q2_y_Bin_13)-(z_pT_Bin_26), (Q2_y_Bin_13)-(z_pT_Bin_3), (Q2_y_Bin_13)-(z_pT_Bin_4)
(Q2_y_Bin_13)-(z_pT_Bin_5), (Q2_y_Bin_13)-(z_pT_Bin_7), (Q2_y_Bin_13)-(z_pT_Bin_8)
(Q2_y_Bin_14)-(z_pT_Bin_1), (Q2_y_Bin_14)-(z_pT_Bin_10), (Q2_y_Bin_14)-(z_pT_Bin_2)
(Q2_y_Bin_14)-(z_pT_Bin_26), (Q2_y_Bin_14)-(z_pT_Bin_3), (Q2_y_Bin_14)-(z_pT_Bin_32)
(Q2_y_Bin_14)-(z_pT_Bin_4), (Q2_y_Bin_14)-(z_pT_Bin_5), (Q2_y_Bin_15)-(z_pT_Bin_1)
(Q2_y_Bin_15)-(z_pT_Bin_19), (Q2_y_Bin_15)-(z_pT_Bin_2), (Q2_y_Bin_15)-(z_pT_Bin_21)
(Q2_y_Bin_15)-(z_pT_Bin_22), (Q2_y_Bin_15)-(z_pT_Bin_23), (Q2_y_Bin_15)-(z_pT_Bin_9)
(Q2_y_Bin_16)-(z_pT_Bin_3), (Q2_y_Bin_16)-(z_pT_Bin_4), (Q2_y_Bin_16)-(z_pT_Bin_5)
(Q2_y_Bin_16)-(z_pT_Bin_6), (Q2_y_Bin_16)-(z_pT_Bin_9), (Q2_y_Bin_17)-(z_pT_Bin_1)
(Q2_y_Bin_17)-(z_pT_Bin_2), (Q2_y_Bin_17)-(z_pT_Bin_3), (Q2_y_Bin_2)-(z_pT_Bin_1)
(Q2_y_Bin_2)-(z_pT_Bin_10), (Q2_y_Bin_2)-(z_pT_Bin_11), (Q2_y_Bin_2)-(z_pT_Bin_12)
(Q2_y_Bin_2)-(z_pT_Bin_13), (Q2_y_Bin_2)-(z_pT_Bin_14), (Q2_y_Bin_2)-(z_pT_Bin_15)
(Q2_y_Bin_2)-(z_pT_Bin_16), (Q2_y_Bin_2)-(z_pT_Bin_17), (Q2_y_Bin_2)-(z_pT_Bin_18)
(Q2_y_Bin_2)-(z_pT_Bin_19), (Q2_y_Bin_2)-(z_pT_Bin_2), (Q2_y_Bin_2)-(z_pT_Bin_20)
(Q2_y_Bin_2)-(z_pT_Bin_21), (Q2_y_Bin_2)-(z_pT_Bin_22), (Q2_y_Bin_2)-(z_pT_Bin_25)
(Q2_y_Bin_2)-(z_pT_Bin_26), (Q2_y_Bin_2)-(z_pT_Bin_27), (Q2_y_Bin_2)-(z_pT_Bin_28)
(Q2_y_Bin_2)-(z_pT_Bin_3), (Q2_y_Bin_2)-(z_pT_Bin_32), (Q2_y_Bin_2)-(z_pT_Bin_33)
(Q2_y_Bin_2)-(z_pT_Bin_34), (Q2_y_Bin_2)-(z_pT_Bin_5), (Q2_y_Bin_2)-(z_pT_Bin_6)
(Q2_y_Bin_2)-(z_pT_Bin_7), (Q2_y_Bin_2)-(z_pT_Bin_9), (Q2_y_Bin_3)-(z_pT_Bin_10)
(Q2_y_Bin_3)-(z_pT_Bin_11), (Q2_y_Bin_3)-(z_pT_Bin_12), (Q2_y_Bin_3)-(z_pT_Bin_13)
(Q2_y_Bin_3)-(z_pT_Bin_14), (Q2_y_Bin_3)-(z_pT_Bin_15), (Q2_y_Bin_3)-(z_pT_Bin_16)
(Q2_y_Bin_3)-(z_pT_Bin_17), (Q2_y_Bin_3)-(z_pT_Bin_18), (Q2_y_Bin_3)-(z_pT_Bin_19)
(Q2_y_Bin_3)-(z_pT_Bin_20), (Q2_y_Bin_3)-(z_pT_Bin_21), (Q2_y_Bin_3)-(z_pT_Bin_22)
(Q2_y_Bin_3)-(z_pT_Bin_23), (Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_8)
(Q2_y_Bin_3)-(z_pT_Bin_9), (Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_13)
(Q2_y_Bin_4)-(z_pT_Bin_14), (Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_19), (Q2_y_Bin_4)-(z_pT_Bin_20), (Q2_y_Bin_4)-(z_pT_Bin_21)
(Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_25), (Q2_y_Bin_4)-(z_pT_Bin_26)
(Q2_y_Bin_4)-(z_pT_Bin_27), (Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission]
(Q2_y_Bin_5)-(z_pT_Bin_10), (Q2_y_Bin_5)-(z_pT_Bin_11), (Q2_y_Bin_5)-(z_pT_Bin_13)
(Q2_y_Bin_5)-(z_pT_Bin_14), (Q2_y_Bin_5)-(z_pT_Bin_15), (Q2_y_Bin_5)-(z_pT_Bin_19)
(Q2_y_Bin_5)-(z_pT_Bin_26), (Q2_y_Bin_5)-(z_pT_Bin_3), (Q2_y_Bin_5)-(z_pT_Bin_32)
(Q2_y_Bin_5)-(z_pT_Bin_4), (Q2_y_Bin_5)-(z_pT_Bin_5), (Q2_y_Bin_5)-(z_pT_Bin_6)
(Q2_y_Bin_5)-(z_pT_Bin_8), (Q2_y_Bin_5)-(z_pT_Bin_9), (Q2_y_Bin_6)-(z_pT_Bin_1)
(Q2_y_Bin_6)-(z_pT_Bin_10), (Q2_y_Bin_6)-(z_pT_Bin_11), (Q2_y_Bin_6)-(z_pT_Bin_13)
(Q2_y_Bin_6)-(z_pT_Bin_15), (Q2_y_Bin_6)-(z_pT_Bin_19), (Q2_y_Bin_6)-(z_pT_Bin_2)
(Q2_y_Bin_6)-(z_pT_Bin_20), (Q2_y_Bin_6)-(z_pT_Bin_21), (Q2_y_Bin_6)-(z_pT_Bin_27)
(Q2_y_Bin_6)-(z_pT_Bin_28), (Q2_y_Bin_6)-(z_pT_Bin_3), (Q2_y_Bin_6)-(z_pT_Bin_5)
(Q2_y_Bin_6)-(z_pT_Bin_6), (Q2_y_Bin_6)-(z_pT_Bin_7), (Q2_y_Bin_6)-(z_pT_Bin_8)
(Q2_y_Bin_6)-(z_pT_Bin_9), (Q2_y_Bin_7)-(z_pT_Bin_10), (Q2_y_Bin_7)-(z_pT_Bin_11)
(Q2_y_Bin_7)-(z_pT_Bin_12), (Q2_y_Bin_7)-(z_pT_Bin_15), (Q2_y_Bin_7)-(z_pT_Bin_16)
(Q2_y_Bin_7)-(z_pT_Bin_17), (Q2_y_Bin_7)-(z_pT_Bin_18), (Q2_y_Bin_7)-(z_pT_Bin_19)
(Q2_y_Bin_7)-(z_pT_Bin_20), (Q2_y_Bin_7)-(z_pT_Bin_21), (Q2_y_Bin_7)-(z_pT_Bin_22)
(Q2_y_Bin_7)-(z_pT_Bin_23), (Q2_y_Bin_7)-(z_pT_Bin_25), (Q2_y_Bin_7)-(z_pT_Bin_26)
(Q2_y_Bin_7)-(z_pT_Bin_27), (Q2_y_Bin_7)-(z_pT_Bin_28), (Q2_y_Bin_7)-(z_pT_Bin_29)
(Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_7)-(z_pT_Bin_8), (Q2_y_Bin_7)-(z_pT_Bin_9)
(Q2_y_Bin_8)-(z_pT_Bin_11), (Q2_y_Bin_8)-(z_pT_Bin_12), (Q2_y_Bin_8)-(z_pT_Bin_13)
(Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16), (Q2_y_Bin_8)-(z_pT_Bin_18)
(Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_21), (Q2_y_Bin_8)-(z_pT_Bin_23)
(Q2_y_Bin_8)-(z_pT_Bin_26), (Q2_y_Bin_8)-(z_pT_Bin_28), (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_9)-(z_pT_Bin_1), (Q2_y_Bin_9)-(z_pT_Bin_10), (Q2_y_Bin_9)-(z_pT_Bin_15)
(Q2_y_Bin_9)-(z_pT_Bin_16), (Q2_y_Bin_9)-(z_pT_Bin_22), (Q2_y_Bin_9)-(z_pT_Bin_3)
(Q2_y_Bin_9)-(z_pT_Bin_4), (Q2_y_Bin_9)-(z_pT_Bin_5), (Q2_y_Bin_9)-(z_pT_Bin_6)
(Q2_y_Bin_9)-(z_pT_Bin_8), (Q2_y_Bin_9)-(z_pT_Bin_9)

#### 120°

The rule fails every assessable manual exclusion (59).

Manually excluded but passes:

None.

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_16), (Q2_y_Bin_1)-(z_pT_Bin_17)
(Q2_y_Bin_1)-(z_pT_Bin_23), (Q2_y_Bin_1)-(z_pT_Bin_30), (Q2_y_Bin_1)-(z_pT_Bin_31)
(Q2_y_Bin_1)-(z_pT_Bin_32), (Q2_y_Bin_1)-(z_pT_Bin_4), (Q2_y_Bin_1)-(z_pT_Bin_5)
(Q2_y_Bin_1)-(z_pT_Bin_6), (Q2_y_Bin_10)-(z_pT_Bin_1), (Q2_y_Bin_10)-(z_pT_Bin_15)
(Q2_y_Bin_10)-(z_pT_Bin_2), (Q2_y_Bin_10)-(z_pT_Bin_26), (Q2_y_Bin_10)-(z_pT_Bin_3)
(Q2_y_Bin_10)-(z_pT_Bin_32), (Q2_y_Bin_10)-(z_pT_Bin_4), (Q2_y_Bin_10)-(z_pT_Bin_5)
(Q2_y_Bin_10)-(z_pT_Bin_6), (Q2_y_Bin_10)-(z_pT_Bin_7), (Q2_y_Bin_11)-(z_pT_Bin_1)
(Q2_y_Bin_11)-(z_pT_Bin_10), (Q2_y_Bin_11)-(z_pT_Bin_2), (Q2_y_Bin_11)-(z_pT_Bin_20)
(Q2_y_Bin_11)-(z_pT_Bin_21), (Q2_y_Bin_11)-(z_pT_Bin_22), (Q2_y_Bin_11)-(z_pT_Bin_23)
(Q2_y_Bin_11)-(z_pT_Bin_24), (Q2_y_Bin_11)-(z_pT_Bin_3), (Q2_y_Bin_11)-(z_pT_Bin_6)
(Q2_y_Bin_11)-(z_pT_Bin_9), (Q2_y_Bin_12)-(z_pT_Bin_13), (Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission]
(Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_13)-(z_pT_Bin_1), (Q2_y_Bin_13)-(z_pT_Bin_2)
(Q2_y_Bin_13)-(z_pT_Bin_3), (Q2_y_Bin_13)-(z_pT_Bin_4), (Q2_y_Bin_13)-(z_pT_Bin_5)
(Q2_y_Bin_14)-(z_pT_Bin_2), (Q2_y_Bin_14)-(z_pT_Bin_3), (Q2_y_Bin_14)-(z_pT_Bin_4)
(Q2_y_Bin_14)-(z_pT_Bin_5), (Q2_y_Bin_15)-(z_pT_Bin_1), (Q2_y_Bin_15)-(z_pT_Bin_2)
(Q2_y_Bin_15)-(z_pT_Bin_22), (Q2_y_Bin_15)-(z_pT_Bin_23), (Q2_y_Bin_15)-(z_pT_Bin_9)
(Q2_y_Bin_16)-(z_pT_Bin_5), (Q2_y_Bin_16)-(z_pT_Bin_6), (Q2_y_Bin_17)-(z_pT_Bin_1)
(Q2_y_Bin_17)-(z_pT_Bin_2), (Q2_y_Bin_2)-(z_pT_Bin_1), (Q2_y_Bin_2)-(z_pT_Bin_10)
(Q2_y_Bin_2)-(z_pT_Bin_11), (Q2_y_Bin_2)-(z_pT_Bin_13), (Q2_y_Bin_2)-(z_pT_Bin_14)
(Q2_y_Bin_2)-(z_pT_Bin_15), (Q2_y_Bin_2)-(z_pT_Bin_16), (Q2_y_Bin_2)-(z_pT_Bin_19)
(Q2_y_Bin_2)-(z_pT_Bin_2), (Q2_y_Bin_2)-(z_pT_Bin_20), (Q2_y_Bin_2)-(z_pT_Bin_25)
(Q2_y_Bin_2)-(z_pT_Bin_26), (Q2_y_Bin_2)-(z_pT_Bin_3), (Q2_y_Bin_2)-(z_pT_Bin_32)
(Q2_y_Bin_2)-(z_pT_Bin_33), (Q2_y_Bin_2)-(z_pT_Bin_34), (Q2_y_Bin_2)-(z_pT_Bin_5)
(Q2_y_Bin_2)-(z_pT_Bin_6), (Q2_y_Bin_2)-(z_pT_Bin_7), (Q2_y_Bin_2)-(z_pT_Bin_9)
(Q2_y_Bin_3)-(z_pT_Bin_10), (Q2_y_Bin_3)-(z_pT_Bin_11), (Q2_y_Bin_3)-(z_pT_Bin_12)
(Q2_y_Bin_3)-(z_pT_Bin_13), (Q2_y_Bin_3)-(z_pT_Bin_14), (Q2_y_Bin_3)-(z_pT_Bin_15)
(Q2_y_Bin_3)-(z_pT_Bin_16), (Q2_y_Bin_3)-(z_pT_Bin_17), (Q2_y_Bin_3)-(z_pT_Bin_18)
(Q2_y_Bin_3)-(z_pT_Bin_20), (Q2_y_Bin_3)-(z_pT_Bin_21), (Q2_y_Bin_3)-(z_pT_Bin_22)
(Q2_y_Bin_3)-(z_pT_Bin_23), (Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_8)
(Q2_y_Bin_3)-(z_pT_Bin_9), (Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_13)
(Q2_y_Bin_4)-(z_pT_Bin_14), (Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_19), (Q2_y_Bin_4)-(z_pT_Bin_20), (Q2_y_Bin_4)-(z_pT_Bin_21)
(Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_25), (Q2_y_Bin_4)-(z_pT_Bin_26)
(Q2_y_Bin_4)-(z_pT_Bin_27), (Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission]
(Q2_y_Bin_5)-(z_pT_Bin_10), (Q2_y_Bin_5)-(z_pT_Bin_13), (Q2_y_Bin_5)-(z_pT_Bin_14)
(Q2_y_Bin_5)-(z_pT_Bin_15), (Q2_y_Bin_5)-(z_pT_Bin_19), (Q2_y_Bin_5)-(z_pT_Bin_3)
(Q2_y_Bin_5)-(z_pT_Bin_32), (Q2_y_Bin_5)-(z_pT_Bin_4), (Q2_y_Bin_5)-(z_pT_Bin_5)
(Q2_y_Bin_5)-(z_pT_Bin_6), (Q2_y_Bin_5)-(z_pT_Bin_8), (Q2_y_Bin_5)-(z_pT_Bin_9)
(Q2_y_Bin_6)-(z_pT_Bin_1), (Q2_y_Bin_6)-(z_pT_Bin_10), (Q2_y_Bin_6)-(z_pT_Bin_15)
(Q2_y_Bin_6)-(z_pT_Bin_19), (Q2_y_Bin_6)-(z_pT_Bin_2), (Q2_y_Bin_6)-(z_pT_Bin_20)
(Q2_y_Bin_6)-(z_pT_Bin_27), (Q2_y_Bin_6)-(z_pT_Bin_28), (Q2_y_Bin_6)-(z_pT_Bin_3)
(Q2_y_Bin_6)-(z_pT_Bin_5), (Q2_y_Bin_6)-(z_pT_Bin_6), (Q2_y_Bin_6)-(z_pT_Bin_7)
(Q2_y_Bin_6)-(z_pT_Bin_8), (Q2_y_Bin_6)-(z_pT_Bin_9), (Q2_y_Bin_7)-(z_pT_Bin_10)
(Q2_y_Bin_7)-(z_pT_Bin_11), (Q2_y_Bin_7)-(z_pT_Bin_12), (Q2_y_Bin_7)-(z_pT_Bin_15)
(Q2_y_Bin_7)-(z_pT_Bin_16), (Q2_y_Bin_7)-(z_pT_Bin_17), (Q2_y_Bin_7)-(z_pT_Bin_18)
(Q2_y_Bin_7)-(z_pT_Bin_21), (Q2_y_Bin_7)-(z_pT_Bin_22), (Q2_y_Bin_7)-(z_pT_Bin_26)
(Q2_y_Bin_7)-(z_pT_Bin_27), (Q2_y_Bin_7)-(z_pT_Bin_28), (Q2_y_Bin_7)-(z_pT_Bin_29)
(Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_7)-(z_pT_Bin_9), (Q2_y_Bin_8)-(z_pT_Bin_11)
(Q2_y_Bin_8)-(z_pT_Bin_12), (Q2_y_Bin_8)-(z_pT_Bin_13), (Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_16), (Q2_y_Bin_8)-(z_pT_Bin_18), (Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_21), (Q2_y_Bin_8)-(z_pT_Bin_23), (Q2_y_Bin_8)-(z_pT_Bin_26)
(Q2_y_Bin_8)-(z_pT_Bin_28), (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_9)-(z_pT_Bin_1)
(Q2_y_Bin_9)-(z_pT_Bin_10), (Q2_y_Bin_9)-(z_pT_Bin_16), (Q2_y_Bin_9)-(z_pT_Bin_3)
(Q2_y_Bin_9)-(z_pT_Bin_4), (Q2_y_Bin_9)-(z_pT_Bin_5), (Q2_y_Bin_9)-(z_pT_Bin_6)
(Q2_y_Bin_9)-(z_pT_Bin_9)

#### 135°

The rule fails every assessable manual exclusion (59).

Manually excluded but passes:

None.

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_16), (Q2_y_Bin_1)-(z_pT_Bin_30)
(Q2_y_Bin_1)-(z_pT_Bin_4), (Q2_y_Bin_1)-(z_pT_Bin_5), (Q2_y_Bin_1)-(z_pT_Bin_6)
(Q2_y_Bin_10)-(z_pT_Bin_1), (Q2_y_Bin_10)-(z_pT_Bin_2), (Q2_y_Bin_10)-(z_pT_Bin_3)
(Q2_y_Bin_10)-(z_pT_Bin_32), (Q2_y_Bin_10)-(z_pT_Bin_4), (Q2_y_Bin_10)-(z_pT_Bin_5)
(Q2_y_Bin_10)-(z_pT_Bin_6), (Q2_y_Bin_10)-(z_pT_Bin_7), (Q2_y_Bin_11)-(z_pT_Bin_1)
(Q2_y_Bin_11)-(z_pT_Bin_10), (Q2_y_Bin_11)-(z_pT_Bin_2), (Q2_y_Bin_11)-(z_pT_Bin_20)
(Q2_y_Bin_11)-(z_pT_Bin_21), (Q2_y_Bin_11)-(z_pT_Bin_22), (Q2_y_Bin_11)-(z_pT_Bin_23)
(Q2_y_Bin_11)-(z_pT_Bin_24), (Q2_y_Bin_11)-(z_pT_Bin_3), (Q2_y_Bin_11)-(z_pT_Bin_6)
(Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_13)-(z_pT_Bin_1)
(Q2_y_Bin_13)-(z_pT_Bin_4), (Q2_y_Bin_14)-(z_pT_Bin_2), (Q2_y_Bin_14)-(z_pT_Bin_4)
(Q2_y_Bin_14)-(z_pT_Bin_5), (Q2_y_Bin_15)-(z_pT_Bin_1), (Q2_y_Bin_15)-(z_pT_Bin_2)
(Q2_y_Bin_15)-(z_pT_Bin_22), (Q2_y_Bin_15)-(z_pT_Bin_23), (Q2_y_Bin_15)-(z_pT_Bin_9)
(Q2_y_Bin_16)-(z_pT_Bin_5), (Q2_y_Bin_16)-(z_pT_Bin_6), (Q2_y_Bin_17)-(z_pT_Bin_2)
(Q2_y_Bin_2)-(z_pT_Bin_1), (Q2_y_Bin_2)-(z_pT_Bin_10), (Q2_y_Bin_2)-(z_pT_Bin_11)
(Q2_y_Bin_2)-(z_pT_Bin_13), (Q2_y_Bin_2)-(z_pT_Bin_14), (Q2_y_Bin_2)-(z_pT_Bin_15)
(Q2_y_Bin_2)-(z_pT_Bin_16), (Q2_y_Bin_2)-(z_pT_Bin_19), (Q2_y_Bin_2)-(z_pT_Bin_2)
(Q2_y_Bin_2)-(z_pT_Bin_20), (Q2_y_Bin_2)-(z_pT_Bin_25), (Q2_y_Bin_2)-(z_pT_Bin_26)
(Q2_y_Bin_2)-(z_pT_Bin_3), (Q2_y_Bin_2)-(z_pT_Bin_32), (Q2_y_Bin_2)-(z_pT_Bin_33)
(Q2_y_Bin_2)-(z_pT_Bin_34), (Q2_y_Bin_2)-(z_pT_Bin_5), (Q2_y_Bin_2)-(z_pT_Bin_6)
(Q2_y_Bin_2)-(z_pT_Bin_7), (Q2_y_Bin_2)-(z_pT_Bin_9), (Q2_y_Bin_3)-(z_pT_Bin_10)
(Q2_y_Bin_3)-(z_pT_Bin_11), (Q2_y_Bin_3)-(z_pT_Bin_12), (Q2_y_Bin_3)-(z_pT_Bin_13)
(Q2_y_Bin_3)-(z_pT_Bin_14), (Q2_y_Bin_3)-(z_pT_Bin_15), (Q2_y_Bin_3)-(z_pT_Bin_16)
(Q2_y_Bin_3)-(z_pT_Bin_17), (Q2_y_Bin_3)-(z_pT_Bin_18), (Q2_y_Bin_3)-(z_pT_Bin_20)
(Q2_y_Bin_3)-(z_pT_Bin_21), (Q2_y_Bin_3)-(z_pT_Bin_22), (Q2_y_Bin_3)-(z_pT_Bin_23)
(Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_8), (Q2_y_Bin_3)-(z_pT_Bin_9)
(Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_13), (Q2_y_Bin_4)-(z_pT_Bin_14)
(Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_19)
(Q2_y_Bin_4)-(z_pT_Bin_20), (Q2_y_Bin_4)-(z_pT_Bin_21), (Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_25), (Q2_y_Bin_4)-(z_pT_Bin_26), (Q2_y_Bin_4)-(z_pT_Bin_27)
(Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission], (Q2_y_Bin_5)-(z_pT_Bin_10)
(Q2_y_Bin_5)-(z_pT_Bin_13), (Q2_y_Bin_5)-(z_pT_Bin_14), (Q2_y_Bin_5)-(z_pT_Bin_15)
(Q2_y_Bin_5)-(z_pT_Bin_19), (Q2_y_Bin_5)-(z_pT_Bin_3), (Q2_y_Bin_5)-(z_pT_Bin_32)
(Q2_y_Bin_5)-(z_pT_Bin_4), (Q2_y_Bin_5)-(z_pT_Bin_5), (Q2_y_Bin_5)-(z_pT_Bin_6)
(Q2_y_Bin_5)-(z_pT_Bin_8), (Q2_y_Bin_5)-(z_pT_Bin_9), (Q2_y_Bin_6)-(z_pT_Bin_1)
(Q2_y_Bin_6)-(z_pT_Bin_2), (Q2_y_Bin_6)-(z_pT_Bin_20), (Q2_y_Bin_6)-(z_pT_Bin_27)
(Q2_y_Bin_6)-(z_pT_Bin_28), (Q2_y_Bin_6)-(z_pT_Bin_3), (Q2_y_Bin_6)-(z_pT_Bin_5)
(Q2_y_Bin_6)-(z_pT_Bin_6), (Q2_y_Bin_6)-(z_pT_Bin_7), (Q2_y_Bin_6)-(z_pT_Bin_8)
(Q2_y_Bin_6)-(z_pT_Bin_9), (Q2_y_Bin_7)-(z_pT_Bin_10), (Q2_y_Bin_7)-(z_pT_Bin_11)
(Q2_y_Bin_7)-(z_pT_Bin_12), (Q2_y_Bin_7)-(z_pT_Bin_15), (Q2_y_Bin_7)-(z_pT_Bin_16)
(Q2_y_Bin_7)-(z_pT_Bin_17), (Q2_y_Bin_7)-(z_pT_Bin_21), (Q2_y_Bin_7)-(z_pT_Bin_22)
(Q2_y_Bin_7)-(z_pT_Bin_26), (Q2_y_Bin_7)-(z_pT_Bin_28), (Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission]
(Q2_y_Bin_7)-(z_pT_Bin_9), (Q2_y_Bin_8)-(z_pT_Bin_11), (Q2_y_Bin_8)-(z_pT_Bin_13)
(Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16), (Q2_y_Bin_8)-(z_pT_Bin_18)
(Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_21), (Q2_y_Bin_8)-(z_pT_Bin_23)
(Q2_y_Bin_8)-(z_pT_Bin_28), (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_9)-(z_pT_Bin_1)
(Q2_y_Bin_9)-(z_pT_Bin_10), (Q2_y_Bin_9)-(z_pT_Bin_16), (Q2_y_Bin_9)-(z_pT_Bin_3)
(Q2_y_Bin_9)-(z_pT_Bin_4)

#### 150°

The rule does not fail every assessable manual exclusion: 2 of 59 pass.

Manually excluded but passes:

(Q2_y_Bin_5)-(z_pT_Bin_20), (Q2_y_Bin_5)-(z_pT_Bin_25)

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_16), (Q2_y_Bin_1)-(z_pT_Bin_30)
(Q2_y_Bin_1)-(z_pT_Bin_4), (Q2_y_Bin_1)-(z_pT_Bin_5), (Q2_y_Bin_1)-(z_pT_Bin_6)
(Q2_y_Bin_10)-(z_pT_Bin_2), (Q2_y_Bin_10)-(z_pT_Bin_3), (Q2_y_Bin_10)-(z_pT_Bin_32)
(Q2_y_Bin_10)-(z_pT_Bin_4), (Q2_y_Bin_10)-(z_pT_Bin_5), (Q2_y_Bin_10)-(z_pT_Bin_6)
(Q2_y_Bin_11)-(z_pT_Bin_1), (Q2_y_Bin_11)-(z_pT_Bin_2), (Q2_y_Bin_11)-(z_pT_Bin_22)
(Q2_y_Bin_11)-(z_pT_Bin_23), (Q2_y_Bin_11)-(z_pT_Bin_24), (Q2_y_Bin_11)-(z_pT_Bin_3)
(Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_13)-(z_pT_Bin_1)
(Q2_y_Bin_14)-(z_pT_Bin_4), (Q2_y_Bin_14)-(z_pT_Bin_5), (Q2_y_Bin_15)-(z_pT_Bin_1)
(Q2_y_Bin_15)-(z_pT_Bin_2), (Q2_y_Bin_15)-(z_pT_Bin_22), (Q2_y_Bin_15)-(z_pT_Bin_23)
(Q2_y_Bin_16)-(z_pT_Bin_6), (Q2_y_Bin_17)-(z_pT_Bin_2), (Q2_y_Bin_2)-(z_pT_Bin_1)
(Q2_y_Bin_2)-(z_pT_Bin_10), (Q2_y_Bin_2)-(z_pT_Bin_13), (Q2_y_Bin_2)-(z_pT_Bin_14)
(Q2_y_Bin_2)-(z_pT_Bin_15), (Q2_y_Bin_2)-(z_pT_Bin_16), (Q2_y_Bin_2)-(z_pT_Bin_19)
(Q2_y_Bin_2)-(z_pT_Bin_2), (Q2_y_Bin_2)-(z_pT_Bin_20), (Q2_y_Bin_2)-(z_pT_Bin_25)
(Q2_y_Bin_2)-(z_pT_Bin_3), (Q2_y_Bin_2)-(z_pT_Bin_32), (Q2_y_Bin_2)-(z_pT_Bin_34)
(Q2_y_Bin_2)-(z_pT_Bin_5), (Q2_y_Bin_2)-(z_pT_Bin_6), (Q2_y_Bin_2)-(z_pT_Bin_7)
(Q2_y_Bin_2)-(z_pT_Bin_9), (Q2_y_Bin_3)-(z_pT_Bin_10), (Q2_y_Bin_3)-(z_pT_Bin_11)
(Q2_y_Bin_3)-(z_pT_Bin_12), (Q2_y_Bin_3)-(z_pT_Bin_13), (Q2_y_Bin_3)-(z_pT_Bin_15)
(Q2_y_Bin_3)-(z_pT_Bin_17), (Q2_y_Bin_3)-(z_pT_Bin_18), (Q2_y_Bin_3)-(z_pT_Bin_20)
(Q2_y_Bin_3)-(z_pT_Bin_21), (Q2_y_Bin_3)-(z_pT_Bin_22), (Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_8), (Q2_y_Bin_3)-(z_pT_Bin_9), (Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_13), (Q2_y_Bin_4)-(z_pT_Bin_14), (Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_19), (Q2_y_Bin_4)-(z_pT_Bin_21)
(Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_25), (Q2_y_Bin_4)-(z_pT_Bin_26)
(Q2_y_Bin_4)-(z_pT_Bin_27), (Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission]
(Q2_y_Bin_5)-(z_pT_Bin_10), (Q2_y_Bin_5)-(z_pT_Bin_13), (Q2_y_Bin_5)-(z_pT_Bin_14)
(Q2_y_Bin_5)-(z_pT_Bin_19), (Q2_y_Bin_5)-(z_pT_Bin_3), (Q2_y_Bin_5)-(z_pT_Bin_4)
(Q2_y_Bin_5)-(z_pT_Bin_5), (Q2_y_Bin_5)-(z_pT_Bin_6), (Q2_y_Bin_5)-(z_pT_Bin_8)
(Q2_y_Bin_5)-(z_pT_Bin_9), (Q2_y_Bin_6)-(z_pT_Bin_1), (Q2_y_Bin_6)-(z_pT_Bin_2)
(Q2_y_Bin_6)-(z_pT_Bin_20), (Q2_y_Bin_6)-(z_pT_Bin_27), (Q2_y_Bin_6)-(z_pT_Bin_28)
(Q2_y_Bin_6)-(z_pT_Bin_3), (Q2_y_Bin_6)-(z_pT_Bin_5), (Q2_y_Bin_6)-(z_pT_Bin_6)
(Q2_y_Bin_6)-(z_pT_Bin_9), (Q2_y_Bin_7)-(z_pT_Bin_11), (Q2_y_Bin_7)-(z_pT_Bin_12)
(Q2_y_Bin_7)-(z_pT_Bin_21), (Q2_y_Bin_7)-(z_pT_Bin_26), (Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_11), (Q2_y_Bin_8)-(z_pT_Bin_13), (Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_16), (Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_28)
(Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_9)-(z_pT_Bin_1), (Q2_y_Bin_9)-(z_pT_Bin_3)
(Q2_y_Bin_9)-(z_pT_Bin_4)

#### 180°

The rule does not fail every assessable manual exclusion: 12 of 59 pass.

Manually excluded but passes:

(Q2_y_Bin_1)-(z_pT_Bin_22), (Q2_y_Bin_17)-(z_pT_Bin_4), (Q2_y_Bin_2)-(z_pT_Bin_8)
(Q2_y_Bin_5)-(z_pT_Bin_20), (Q2_y_Bin_5)-(z_pT_Bin_25), (Q2_y_Bin_6)-(z_pT_Bin_14)
(Q2_y_Bin_6)-(z_pT_Bin_4), (Q2_y_Bin_7)-(z_pT_Bin_1), (Q2_y_Bin_7)-(z_pT_Bin_13)
(Q2_y_Bin_7)-(z_pT_Bin_7), (Q2_y_Bin_9)-(z_pT_Bin_2), (Q2_y_Bin_9)-(z_pT_Bin_29)

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_30), (Q2_y_Bin_1)-(z_pT_Bin_4), (Q2_y_Bin_1)-(z_pT_Bin_5)
(Q2_y_Bin_10)-(z_pT_Bin_6), (Q2_y_Bin_11)-(z_pT_Bin_22), (Q2_y_Bin_11)-(z_pT_Bin_23)
(Q2_y_Bin_11)-(z_pT_Bin_24), (Q2_y_Bin_11)-(z_pT_Bin_3), (Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission]
(Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_14)-(z_pT_Bin_5), (Q2_y_Bin_15)-(z_pT_Bin_2)
(Q2_y_Bin_2)-(z_pT_Bin_1), (Q2_y_Bin_2)-(z_pT_Bin_2), (Q2_y_Bin_2)-(z_pT_Bin_20)
(Q2_y_Bin_2)-(z_pT_Bin_3), (Q2_y_Bin_2)-(z_pT_Bin_5), (Q2_y_Bin_2)-(z_pT_Bin_6)
(Q2_y_Bin_2)-(z_pT_Bin_7), (Q2_y_Bin_2)-(z_pT_Bin_9), (Q2_y_Bin_3)-(z_pT_Bin_10)
(Q2_y_Bin_3)-(z_pT_Bin_13), (Q2_y_Bin_3)-(z_pT_Bin_15), (Q2_y_Bin_3)-(z_pT_Bin_20)
(Q2_y_Bin_3)-(z_pT_Bin_21), (Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_9)
(Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_13), (Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_19), (Q2_y_Bin_4)-(z_pT_Bin_21)
(Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_25), (Q2_y_Bin_4)-(z_pT_Bin_27)
(Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission], (Q2_y_Bin_5)-(z_pT_Bin_3)
(Q2_y_Bin_5)-(z_pT_Bin_4), (Q2_y_Bin_5)-(z_pT_Bin_5), (Q2_y_Bin_7)-(z_pT_Bin_12)
(Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_11), (Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_16), (Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_9)-(z_pT_Bin_1)

### pipS1o

Manual list entries: 29. Fit-quality omissions relative to the nominal acceptance bins: 35. Comparisons the budget still keeps: 393.

Manual entries outside the retained population:

(Q2_y_Bin_1)-(z_pT_Bin_21)

#### 90°

The rule fails every assessable manual exclusion (28).

Manually excluded but passes:

None.

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_11), (Q2_y_Bin_1)-(z_pT_Bin_15)
(Q2_y_Bin_1)-(z_pT_Bin_16), (Q2_y_Bin_1)-(z_pT_Bin_17), (Q2_y_Bin_1)-(z_pT_Bin_22)
(Q2_y_Bin_1)-(z_pT_Bin_23), (Q2_y_Bin_1)-(z_pT_Bin_3), (Q2_y_Bin_1)-(z_pT_Bin_30)
(Q2_y_Bin_1)-(z_pT_Bin_31), (Q2_y_Bin_1)-(z_pT_Bin_32), (Q2_y_Bin_1)-(z_pT_Bin_4)
(Q2_y_Bin_1)-(z_pT_Bin_5), (Q2_y_Bin_1)-(z_pT_Bin_6), (Q2_y_Bin_1)-(z_pT_Bin_7)
(Q2_y_Bin_1)-(z_pT_Bin_9), (Q2_y_Bin_10)-(z_pT_Bin_1), (Q2_y_Bin_10)-(z_pT_Bin_10)
(Q2_y_Bin_10)-(z_pT_Bin_15), (Q2_y_Bin_10)-(z_pT_Bin_2), (Q2_y_Bin_10)-(z_pT_Bin_20)
(Q2_y_Bin_10)-(z_pT_Bin_26), (Q2_y_Bin_10)-(z_pT_Bin_3), (Q2_y_Bin_10)-(z_pT_Bin_31)
(Q2_y_Bin_10)-(z_pT_Bin_32), (Q2_y_Bin_10)-(z_pT_Bin_4), (Q2_y_Bin_10)-(z_pT_Bin_5)
(Q2_y_Bin_10)-(z_pT_Bin_6), (Q2_y_Bin_10)-(z_pT_Bin_7), (Q2_y_Bin_10)-(z_pT_Bin_9)
(Q2_y_Bin_11)-(z_pT_Bin_1), (Q2_y_Bin_11)-(z_pT_Bin_10), (Q2_y_Bin_11)-(z_pT_Bin_13)
(Q2_y_Bin_11)-(z_pT_Bin_15), (Q2_y_Bin_11)-(z_pT_Bin_18), (Q2_y_Bin_11)-(z_pT_Bin_2)
(Q2_y_Bin_11)-(z_pT_Bin_20), (Q2_y_Bin_11)-(z_pT_Bin_21), (Q2_y_Bin_11)-(z_pT_Bin_22)
(Q2_y_Bin_11)-(z_pT_Bin_23), (Q2_y_Bin_11)-(z_pT_Bin_24), (Q2_y_Bin_11)-(z_pT_Bin_3)
(Q2_y_Bin_11)-(z_pT_Bin_6), (Q2_y_Bin_11)-(z_pT_Bin_9), (Q2_y_Bin_12)-(z_pT_Bin_11)
(Q2_y_Bin_12)-(z_pT_Bin_13), (Q2_y_Bin_12)-(z_pT_Bin_16), (Q2_y_Bin_12)-(z_pT_Bin_18)
(Q2_y_Bin_12)-(z_pT_Bin_22), (Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_6)
(Q2_y_Bin_12)-(z_pT_Bin_7), (Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_13)-(z_pT_Bin_1)
(Q2_y_Bin_13)-(z_pT_Bin_12), (Q2_y_Bin_13)-(z_pT_Bin_2), (Q2_y_Bin_13)-(z_pT_Bin_26)
(Q2_y_Bin_13)-(z_pT_Bin_3), (Q2_y_Bin_13)-(z_pT_Bin_4), (Q2_y_Bin_13)-(z_pT_Bin_5)
(Q2_y_Bin_13)-(z_pT_Bin_7), (Q2_y_Bin_13)-(z_pT_Bin_8), (Q2_y_Bin_13)-(z_pT_Bin_9)
(Q2_y_Bin_14)-(z_pT_Bin_1), (Q2_y_Bin_14)-(z_pT_Bin_2), (Q2_y_Bin_14)-(z_pT_Bin_4)
(Q2_y_Bin_14)-(z_pT_Bin_5), (Q2_y_Bin_15)-(z_pT_Bin_1), (Q2_y_Bin_15)-(z_pT_Bin_15)
(Q2_y_Bin_15)-(z_pT_Bin_19), (Q2_y_Bin_15)-(z_pT_Bin_2), (Q2_y_Bin_15)-(z_pT_Bin_22)
(Q2_y_Bin_15)-(z_pT_Bin_23), (Q2_y_Bin_15)-(z_pT_Bin_24), (Q2_y_Bin_15)-(z_pT_Bin_9)
(Q2_y_Bin_16)-(z_pT_Bin_3), (Q2_y_Bin_16)-(z_pT_Bin_4), (Q2_y_Bin_16)-(z_pT_Bin_6)
(Q2_y_Bin_16)-(z_pT_Bin_9), (Q2_y_Bin_17)-(z_pT_Bin_4), (Q2_y_Bin_2)-(z_pT_Bin_1)
(Q2_y_Bin_2)-(z_pT_Bin_10), (Q2_y_Bin_2)-(z_pT_Bin_11), (Q2_y_Bin_2)-(z_pT_Bin_13)
(Q2_y_Bin_2)-(z_pT_Bin_14), (Q2_y_Bin_2)-(z_pT_Bin_15), (Q2_y_Bin_2)-(z_pT_Bin_16)
(Q2_y_Bin_2)-(z_pT_Bin_19), (Q2_y_Bin_2)-(z_pT_Bin_2), (Q2_y_Bin_2)-(z_pT_Bin_20)
(Q2_y_Bin_2)-(z_pT_Bin_21), (Q2_y_Bin_2)-(z_pT_Bin_25), (Q2_y_Bin_2)-(z_pT_Bin_26)
(Q2_y_Bin_2)-(z_pT_Bin_27), (Q2_y_Bin_2)-(z_pT_Bin_3), (Q2_y_Bin_2)-(z_pT_Bin_32)
(Q2_y_Bin_2)-(z_pT_Bin_33), (Q2_y_Bin_2)-(z_pT_Bin_34), (Q2_y_Bin_2)-(z_pT_Bin_4)
(Q2_y_Bin_2)-(z_pT_Bin_5), (Q2_y_Bin_2)-(z_pT_Bin_6), (Q2_y_Bin_2)-(z_pT_Bin_7)
(Q2_y_Bin_2)-(z_pT_Bin_8), (Q2_y_Bin_2)-(z_pT_Bin_9), (Q2_y_Bin_3)-(z_pT_Bin_1)
(Q2_y_Bin_3)-(z_pT_Bin_10), (Q2_y_Bin_3)-(z_pT_Bin_11), (Q2_y_Bin_3)-(z_pT_Bin_12)
(Q2_y_Bin_3)-(z_pT_Bin_13), (Q2_y_Bin_3)-(z_pT_Bin_14), (Q2_y_Bin_3)-(z_pT_Bin_15)
(Q2_y_Bin_3)-(z_pT_Bin_16), (Q2_y_Bin_3)-(z_pT_Bin_17), (Q2_y_Bin_3)-(z_pT_Bin_18)
(Q2_y_Bin_3)-(z_pT_Bin_19), (Q2_y_Bin_3)-(z_pT_Bin_20), (Q2_y_Bin_3)-(z_pT_Bin_21)
(Q2_y_Bin_3)-(z_pT_Bin_22), (Q2_y_Bin_3)-(z_pT_Bin_23), (Q2_y_Bin_3)-(z_pT_Bin_24)
(Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_7), (Q2_y_Bin_3)-(z_pT_Bin_8)
(Q2_y_Bin_3)-(z_pT_Bin_9), (Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_13)
(Q2_y_Bin_4)-(z_pT_Bin_14), (Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_19), (Q2_y_Bin_4)-(z_pT_Bin_20), (Q2_y_Bin_4)-(z_pT_Bin_21)
(Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_25), (Q2_y_Bin_4)-(z_pT_Bin_26)
(Q2_y_Bin_4)-(z_pT_Bin_27), (Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission]
(Q2_y_Bin_5)-(z_pT_Bin_10), (Q2_y_Bin_5)-(z_pT_Bin_13), (Q2_y_Bin_5)-(z_pT_Bin_14)
(Q2_y_Bin_5)-(z_pT_Bin_15), (Q2_y_Bin_5)-(z_pT_Bin_19), (Q2_y_Bin_5)-(z_pT_Bin_20)
(Q2_y_Bin_5)-(z_pT_Bin_25), (Q2_y_Bin_5)-(z_pT_Bin_26), (Q2_y_Bin_5)-(z_pT_Bin_3)
(Q2_y_Bin_5)-(z_pT_Bin_31), (Q2_y_Bin_5)-(z_pT_Bin_32), (Q2_y_Bin_5)-(z_pT_Bin_4)
(Q2_y_Bin_5)-(z_pT_Bin_5), (Q2_y_Bin_5)-(z_pT_Bin_6), (Q2_y_Bin_5)-(z_pT_Bin_8)
(Q2_y_Bin_5)-(z_pT_Bin_9), (Q2_y_Bin_6)-(z_pT_Bin_1), (Q2_y_Bin_6)-(z_pT_Bin_10)
(Q2_y_Bin_6)-(z_pT_Bin_11), (Q2_y_Bin_6)-(z_pT_Bin_13), (Q2_y_Bin_6)-(z_pT_Bin_14)
(Q2_y_Bin_6)-(z_pT_Bin_15), (Q2_y_Bin_6)-(z_pT_Bin_19), (Q2_y_Bin_6)-(z_pT_Bin_2)
(Q2_y_Bin_6)-(z_pT_Bin_20), (Q2_y_Bin_6)-(z_pT_Bin_25), (Q2_y_Bin_6)-(z_pT_Bin_26)
(Q2_y_Bin_6)-(z_pT_Bin_27), (Q2_y_Bin_6)-(z_pT_Bin_28), (Q2_y_Bin_6)-(z_pT_Bin_3)
(Q2_y_Bin_6)-(z_pT_Bin_4), (Q2_y_Bin_6)-(z_pT_Bin_5), (Q2_y_Bin_6)-(z_pT_Bin_6)
(Q2_y_Bin_6)-(z_pT_Bin_7), (Q2_y_Bin_6)-(z_pT_Bin_8), (Q2_y_Bin_6)-(z_pT_Bin_9)
(Q2_y_Bin_7)-(z_pT_Bin_1), (Q2_y_Bin_7)-(z_pT_Bin_10), (Q2_y_Bin_7)-(z_pT_Bin_11)
(Q2_y_Bin_7)-(z_pT_Bin_12), (Q2_y_Bin_7)-(z_pT_Bin_13), (Q2_y_Bin_7)-(z_pT_Bin_15)
(Q2_y_Bin_7)-(z_pT_Bin_16), (Q2_y_Bin_7)-(z_pT_Bin_17), (Q2_y_Bin_7)-(z_pT_Bin_18)
(Q2_y_Bin_7)-(z_pT_Bin_19), (Q2_y_Bin_7)-(z_pT_Bin_2), (Q2_y_Bin_7)-(z_pT_Bin_20)
(Q2_y_Bin_7)-(z_pT_Bin_21), (Q2_y_Bin_7)-(z_pT_Bin_22), (Q2_y_Bin_7)-(z_pT_Bin_23)
(Q2_y_Bin_7)-(z_pT_Bin_24), (Q2_y_Bin_7)-(z_pT_Bin_26), (Q2_y_Bin_7)-(z_pT_Bin_27)
(Q2_y_Bin_7)-(z_pT_Bin_28), (Q2_y_Bin_7)-(z_pT_Bin_29), (Q2_y_Bin_7)-(z_pT_Bin_31)
(Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_7)-(z_pT_Bin_7), (Q2_y_Bin_7)-(z_pT_Bin_8)
(Q2_y_Bin_7)-(z_pT_Bin_9), (Q2_y_Bin_8)-(z_pT_Bin_11), (Q2_y_Bin_8)-(z_pT_Bin_12)
(Q2_y_Bin_8)-(z_pT_Bin_13), (Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16)
(Q2_y_Bin_8)-(z_pT_Bin_18), (Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_21)
(Q2_y_Bin_8)-(z_pT_Bin_23), (Q2_y_Bin_8)-(z_pT_Bin_26), (Q2_y_Bin_8)-(z_pT_Bin_28)
(Q2_y_Bin_8)-(z_pT_Bin_29), (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_9)-(z_pT_Bin_10)
(Q2_y_Bin_9)-(z_pT_Bin_11), (Q2_y_Bin_9)-(z_pT_Bin_15), (Q2_y_Bin_9)-(z_pT_Bin_16)
(Q2_y_Bin_9)-(z_pT_Bin_2), (Q2_y_Bin_9)-(z_pT_Bin_22), (Q2_y_Bin_9)-(z_pT_Bin_29)
(Q2_y_Bin_9)-(z_pT_Bin_3), (Q2_y_Bin_9)-(z_pT_Bin_4), (Q2_y_Bin_9)-(z_pT_Bin_5)
(Q2_y_Bin_9)-(z_pT_Bin_6), (Q2_y_Bin_9)-(z_pT_Bin_8), (Q2_y_Bin_9)-(z_pT_Bin_9)

#### 120°

The rule fails every assessable manual exclusion (28).

Manually excluded but passes:

None.

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_15), (Q2_y_Bin_1)-(z_pT_Bin_16)
(Q2_y_Bin_1)-(z_pT_Bin_22), (Q2_y_Bin_1)-(z_pT_Bin_3), (Q2_y_Bin_1)-(z_pT_Bin_30)
(Q2_y_Bin_1)-(z_pT_Bin_4), (Q2_y_Bin_1)-(z_pT_Bin_5), (Q2_y_Bin_1)-(z_pT_Bin_6)
(Q2_y_Bin_1)-(z_pT_Bin_7), (Q2_y_Bin_1)-(z_pT_Bin_9), (Q2_y_Bin_10)-(z_pT_Bin_1)
(Q2_y_Bin_10)-(z_pT_Bin_2), (Q2_y_Bin_10)-(z_pT_Bin_3), (Q2_y_Bin_10)-(z_pT_Bin_32)
(Q2_y_Bin_10)-(z_pT_Bin_4), (Q2_y_Bin_10)-(z_pT_Bin_5), (Q2_y_Bin_10)-(z_pT_Bin_6)
(Q2_y_Bin_10)-(z_pT_Bin_7), (Q2_y_Bin_11)-(z_pT_Bin_1), (Q2_y_Bin_11)-(z_pT_Bin_2)
(Q2_y_Bin_11)-(z_pT_Bin_20), (Q2_y_Bin_11)-(z_pT_Bin_21), (Q2_y_Bin_11)-(z_pT_Bin_22)
(Q2_y_Bin_11)-(z_pT_Bin_23), (Q2_y_Bin_11)-(z_pT_Bin_24), (Q2_y_Bin_11)-(z_pT_Bin_3)
(Q2_y_Bin_11)-(z_pT_Bin_6), (Q2_y_Bin_12)-(z_pT_Bin_11), (Q2_y_Bin_12)-(z_pT_Bin_22)
(Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_6), (Q2_y_Bin_12)-(z_pT_Bin_7)
(Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_13)-(z_pT_Bin_1), (Q2_y_Bin_13)-(z_pT_Bin_2)
(Q2_y_Bin_13)-(z_pT_Bin_4), (Q2_y_Bin_14)-(z_pT_Bin_2), (Q2_y_Bin_14)-(z_pT_Bin_5)
(Q2_y_Bin_15)-(z_pT_Bin_1), (Q2_y_Bin_15)-(z_pT_Bin_15), (Q2_y_Bin_15)-(z_pT_Bin_2)
(Q2_y_Bin_15)-(z_pT_Bin_23), (Q2_y_Bin_15)-(z_pT_Bin_24), (Q2_y_Bin_16)-(z_pT_Bin_6)
(Q2_y_Bin_2)-(z_pT_Bin_1), (Q2_y_Bin_2)-(z_pT_Bin_10), (Q2_y_Bin_2)-(z_pT_Bin_11)
(Q2_y_Bin_2)-(z_pT_Bin_13), (Q2_y_Bin_2)-(z_pT_Bin_14), (Q2_y_Bin_2)-(z_pT_Bin_15)
(Q2_y_Bin_2)-(z_pT_Bin_16), (Q2_y_Bin_2)-(z_pT_Bin_19), (Q2_y_Bin_2)-(z_pT_Bin_2)
(Q2_y_Bin_2)-(z_pT_Bin_20), (Q2_y_Bin_2)-(z_pT_Bin_25), (Q2_y_Bin_2)-(z_pT_Bin_26)
(Q2_y_Bin_2)-(z_pT_Bin_3), (Q2_y_Bin_2)-(z_pT_Bin_32), (Q2_y_Bin_2)-(z_pT_Bin_33)
(Q2_y_Bin_2)-(z_pT_Bin_34), (Q2_y_Bin_2)-(z_pT_Bin_4), (Q2_y_Bin_2)-(z_pT_Bin_5)
(Q2_y_Bin_2)-(z_pT_Bin_6), (Q2_y_Bin_2)-(z_pT_Bin_7), (Q2_y_Bin_2)-(z_pT_Bin_8)
(Q2_y_Bin_2)-(z_pT_Bin_9), (Q2_y_Bin_3)-(z_pT_Bin_1), (Q2_y_Bin_3)-(z_pT_Bin_10)
(Q2_y_Bin_3)-(z_pT_Bin_11), (Q2_y_Bin_3)-(z_pT_Bin_12), (Q2_y_Bin_3)-(z_pT_Bin_13)
(Q2_y_Bin_3)-(z_pT_Bin_14), (Q2_y_Bin_3)-(z_pT_Bin_15), (Q2_y_Bin_3)-(z_pT_Bin_16)
(Q2_y_Bin_3)-(z_pT_Bin_17), (Q2_y_Bin_3)-(z_pT_Bin_18), (Q2_y_Bin_3)-(z_pT_Bin_19)
(Q2_y_Bin_3)-(z_pT_Bin_20), (Q2_y_Bin_3)-(z_pT_Bin_21), (Q2_y_Bin_3)-(z_pT_Bin_22)
(Q2_y_Bin_3)-(z_pT_Bin_23), (Q2_y_Bin_3)-(z_pT_Bin_24), (Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_7), (Q2_y_Bin_3)-(z_pT_Bin_8), (Q2_y_Bin_3)-(z_pT_Bin_9)
(Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_13), (Q2_y_Bin_4)-(z_pT_Bin_14)
(Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_19)
(Q2_y_Bin_4)-(z_pT_Bin_21), (Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_25)
(Q2_y_Bin_4)-(z_pT_Bin_26), (Q2_y_Bin_4)-(z_pT_Bin_27), (Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission], (Q2_y_Bin_5)-(z_pT_Bin_10), (Q2_y_Bin_5)-(z_pT_Bin_13)
(Q2_y_Bin_5)-(z_pT_Bin_14), (Q2_y_Bin_5)-(z_pT_Bin_15), (Q2_y_Bin_5)-(z_pT_Bin_19)
(Q2_y_Bin_5)-(z_pT_Bin_20), (Q2_y_Bin_5)-(z_pT_Bin_3), (Q2_y_Bin_5)-(z_pT_Bin_31)
(Q2_y_Bin_5)-(z_pT_Bin_32), (Q2_y_Bin_5)-(z_pT_Bin_4), (Q2_y_Bin_5)-(z_pT_Bin_5)
(Q2_y_Bin_5)-(z_pT_Bin_6), (Q2_y_Bin_5)-(z_pT_Bin_8), (Q2_y_Bin_5)-(z_pT_Bin_9)
(Q2_y_Bin_6)-(z_pT_Bin_1), (Q2_y_Bin_6)-(z_pT_Bin_2), (Q2_y_Bin_6)-(z_pT_Bin_20)
(Q2_y_Bin_6)-(z_pT_Bin_25), (Q2_y_Bin_6)-(z_pT_Bin_26), (Q2_y_Bin_6)-(z_pT_Bin_27)
(Q2_y_Bin_6)-(z_pT_Bin_28), (Q2_y_Bin_6)-(z_pT_Bin_3), (Q2_y_Bin_6)-(z_pT_Bin_4)
(Q2_y_Bin_6)-(z_pT_Bin_5), (Q2_y_Bin_6)-(z_pT_Bin_6), (Q2_y_Bin_6)-(z_pT_Bin_7)
(Q2_y_Bin_6)-(z_pT_Bin_8), (Q2_y_Bin_6)-(z_pT_Bin_9), (Q2_y_Bin_7)-(z_pT_Bin_1)
(Q2_y_Bin_7)-(z_pT_Bin_10), (Q2_y_Bin_7)-(z_pT_Bin_11), (Q2_y_Bin_7)-(z_pT_Bin_12)
(Q2_y_Bin_7)-(z_pT_Bin_13), (Q2_y_Bin_7)-(z_pT_Bin_16), (Q2_y_Bin_7)-(z_pT_Bin_17)
(Q2_y_Bin_7)-(z_pT_Bin_2), (Q2_y_Bin_7)-(z_pT_Bin_21), (Q2_y_Bin_7)-(z_pT_Bin_24)
(Q2_y_Bin_7)-(z_pT_Bin_27), (Q2_y_Bin_7)-(z_pT_Bin_29), (Q2_y_Bin_7)-(z_pT_Bin_31)
(Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_7)-(z_pT_Bin_7), (Q2_y_Bin_7)-(z_pT_Bin_9)
(Q2_y_Bin_8)-(z_pT_Bin_11), (Q2_y_Bin_8)-(z_pT_Bin_12), (Q2_y_Bin_8)-(z_pT_Bin_13)
(Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16), (Q2_y_Bin_8)-(z_pT_Bin_18)
(Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_21), (Q2_y_Bin_8)-(z_pT_Bin_23)
(Q2_y_Bin_8)-(z_pT_Bin_28), (Q2_y_Bin_8)-(z_pT_Bin_29), (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_9)-(z_pT_Bin_10), (Q2_y_Bin_9)-(z_pT_Bin_2), (Q2_y_Bin_9)-(z_pT_Bin_29)
(Q2_y_Bin_9)-(z_pT_Bin_3), (Q2_y_Bin_9)-(z_pT_Bin_4), (Q2_y_Bin_9)-(z_pT_Bin_5)
(Q2_y_Bin_9)-(z_pT_Bin_6), (Q2_y_Bin_9)-(z_pT_Bin_9)

#### 135°

The rule fails every assessable manual exclusion (28).

Manually excluded but passes:

None.

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_15), (Q2_y_Bin_1)-(z_pT_Bin_16)
(Q2_y_Bin_1)-(z_pT_Bin_22), (Q2_y_Bin_1)-(z_pT_Bin_3), (Q2_y_Bin_1)-(z_pT_Bin_30)
(Q2_y_Bin_1)-(z_pT_Bin_4), (Q2_y_Bin_1)-(z_pT_Bin_5), (Q2_y_Bin_1)-(z_pT_Bin_6)
(Q2_y_Bin_1)-(z_pT_Bin_7), (Q2_y_Bin_1)-(z_pT_Bin_9), (Q2_y_Bin_10)-(z_pT_Bin_1)
(Q2_y_Bin_10)-(z_pT_Bin_2), (Q2_y_Bin_10)-(z_pT_Bin_3), (Q2_y_Bin_10)-(z_pT_Bin_4)
(Q2_y_Bin_10)-(z_pT_Bin_5), (Q2_y_Bin_10)-(z_pT_Bin_6), (Q2_y_Bin_10)-(z_pT_Bin_7)
(Q2_y_Bin_11)-(z_pT_Bin_1), (Q2_y_Bin_11)-(z_pT_Bin_2), (Q2_y_Bin_11)-(z_pT_Bin_21)
(Q2_y_Bin_11)-(z_pT_Bin_22), (Q2_y_Bin_11)-(z_pT_Bin_23), (Q2_y_Bin_11)-(z_pT_Bin_24)
(Q2_y_Bin_11)-(z_pT_Bin_3), (Q2_y_Bin_11)-(z_pT_Bin_6), (Q2_y_Bin_12)-(z_pT_Bin_11)
(Q2_y_Bin_12)-(z_pT_Bin_22), (Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_6)
(Q2_y_Bin_12)-(z_pT_Bin_7), (Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_13)-(z_pT_Bin_1)
(Q2_y_Bin_13)-(z_pT_Bin_2), (Q2_y_Bin_14)-(z_pT_Bin_2), (Q2_y_Bin_14)-(z_pT_Bin_5)
(Q2_y_Bin_15)-(z_pT_Bin_1), (Q2_y_Bin_15)-(z_pT_Bin_15), (Q2_y_Bin_15)-(z_pT_Bin_2)
(Q2_y_Bin_15)-(z_pT_Bin_23), (Q2_y_Bin_15)-(z_pT_Bin_24), (Q2_y_Bin_16)-(z_pT_Bin_6)
(Q2_y_Bin_2)-(z_pT_Bin_1), (Q2_y_Bin_2)-(z_pT_Bin_10), (Q2_y_Bin_2)-(z_pT_Bin_13)
(Q2_y_Bin_2)-(z_pT_Bin_14), (Q2_y_Bin_2)-(z_pT_Bin_15), (Q2_y_Bin_2)-(z_pT_Bin_19)
(Q2_y_Bin_2)-(z_pT_Bin_2), (Q2_y_Bin_2)-(z_pT_Bin_20), (Q2_y_Bin_2)-(z_pT_Bin_25)
(Q2_y_Bin_2)-(z_pT_Bin_3), (Q2_y_Bin_2)-(z_pT_Bin_32), (Q2_y_Bin_2)-(z_pT_Bin_34)
(Q2_y_Bin_2)-(z_pT_Bin_4), (Q2_y_Bin_2)-(z_pT_Bin_5), (Q2_y_Bin_2)-(z_pT_Bin_6)
(Q2_y_Bin_2)-(z_pT_Bin_7), (Q2_y_Bin_2)-(z_pT_Bin_8), (Q2_y_Bin_2)-(z_pT_Bin_9)
(Q2_y_Bin_3)-(z_pT_Bin_1), (Q2_y_Bin_3)-(z_pT_Bin_10), (Q2_y_Bin_3)-(z_pT_Bin_11)
(Q2_y_Bin_3)-(z_pT_Bin_12), (Q2_y_Bin_3)-(z_pT_Bin_13), (Q2_y_Bin_3)-(z_pT_Bin_14)
(Q2_y_Bin_3)-(z_pT_Bin_15), (Q2_y_Bin_3)-(z_pT_Bin_16), (Q2_y_Bin_3)-(z_pT_Bin_17)
(Q2_y_Bin_3)-(z_pT_Bin_18), (Q2_y_Bin_3)-(z_pT_Bin_20), (Q2_y_Bin_3)-(z_pT_Bin_21)
(Q2_y_Bin_3)-(z_pT_Bin_23), (Q2_y_Bin_3)-(z_pT_Bin_24), (Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_7), (Q2_y_Bin_3)-(z_pT_Bin_8), (Q2_y_Bin_3)-(z_pT_Bin_9)
(Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_13), (Q2_y_Bin_4)-(z_pT_Bin_14)
(Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_19)
(Q2_y_Bin_4)-(z_pT_Bin_21), (Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_25)
(Q2_y_Bin_4)-(z_pT_Bin_26), (Q2_y_Bin_4)-(z_pT_Bin_27), (Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission], (Q2_y_Bin_5)-(z_pT_Bin_10), (Q2_y_Bin_5)-(z_pT_Bin_13)
(Q2_y_Bin_5)-(z_pT_Bin_14), (Q2_y_Bin_5)-(z_pT_Bin_19), (Q2_y_Bin_5)-(z_pT_Bin_3)
(Q2_y_Bin_5)-(z_pT_Bin_31), (Q2_y_Bin_5)-(z_pT_Bin_4), (Q2_y_Bin_5)-(z_pT_Bin_5)
(Q2_y_Bin_5)-(z_pT_Bin_6), (Q2_y_Bin_5)-(z_pT_Bin_8), (Q2_y_Bin_5)-(z_pT_Bin_9)
(Q2_y_Bin_6)-(z_pT_Bin_1), (Q2_y_Bin_6)-(z_pT_Bin_2), (Q2_y_Bin_6)-(z_pT_Bin_20)
(Q2_y_Bin_6)-(z_pT_Bin_25), (Q2_y_Bin_6)-(z_pT_Bin_26), (Q2_y_Bin_6)-(z_pT_Bin_27)
(Q2_y_Bin_6)-(z_pT_Bin_3), (Q2_y_Bin_6)-(z_pT_Bin_4), (Q2_y_Bin_6)-(z_pT_Bin_5)
(Q2_y_Bin_6)-(z_pT_Bin_6), (Q2_y_Bin_6)-(z_pT_Bin_7), (Q2_y_Bin_6)-(z_pT_Bin_8)
(Q2_y_Bin_6)-(z_pT_Bin_9), (Q2_y_Bin_7)-(z_pT_Bin_1), (Q2_y_Bin_7)-(z_pT_Bin_10)
(Q2_y_Bin_7)-(z_pT_Bin_11), (Q2_y_Bin_7)-(z_pT_Bin_12), (Q2_y_Bin_7)-(z_pT_Bin_13)
(Q2_y_Bin_7)-(z_pT_Bin_2), (Q2_y_Bin_7)-(z_pT_Bin_21), (Q2_y_Bin_7)-(z_pT_Bin_24)
(Q2_y_Bin_7)-(z_pT_Bin_27), (Q2_y_Bin_7)-(z_pT_Bin_29), (Q2_y_Bin_7)-(z_pT_Bin_31)
(Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_7)-(z_pT_Bin_7), (Q2_y_Bin_8)-(z_pT_Bin_11)
(Q2_y_Bin_8)-(z_pT_Bin_13), (Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16)
(Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_28), (Q2_y_Bin_8)-(z_pT_Bin_29)
(Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_9)-(z_pT_Bin_2), (Q2_y_Bin_9)-(z_pT_Bin_3)
(Q2_y_Bin_9)-(z_pT_Bin_4)

#### 150°

The rule fails every assessable manual exclusion (28).

Manually excluded but passes:

None.

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_15), (Q2_y_Bin_1)-(z_pT_Bin_16)
(Q2_y_Bin_1)-(z_pT_Bin_22), (Q2_y_Bin_1)-(z_pT_Bin_3), (Q2_y_Bin_1)-(z_pT_Bin_30)
(Q2_y_Bin_1)-(z_pT_Bin_4), (Q2_y_Bin_1)-(z_pT_Bin_5), (Q2_y_Bin_1)-(z_pT_Bin_6)
(Q2_y_Bin_1)-(z_pT_Bin_9), (Q2_y_Bin_10)-(z_pT_Bin_2), (Q2_y_Bin_10)-(z_pT_Bin_4)
(Q2_y_Bin_10)-(z_pT_Bin_5), (Q2_y_Bin_10)-(z_pT_Bin_6), (Q2_y_Bin_11)-(z_pT_Bin_1)
(Q2_y_Bin_11)-(z_pT_Bin_2), (Q2_y_Bin_11)-(z_pT_Bin_22), (Q2_y_Bin_11)-(z_pT_Bin_23)
(Q2_y_Bin_11)-(z_pT_Bin_24), (Q2_y_Bin_11)-(z_pT_Bin_3), (Q2_y_Bin_12)-(z_pT_Bin_11)
(Q2_y_Bin_12)-(z_pT_Bin_22), (Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_6)
(Q2_y_Bin_12)-(z_pT_Bin_7), (Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_13)-(z_pT_Bin_1)
(Q2_y_Bin_14)-(z_pT_Bin_5), (Q2_y_Bin_15)-(z_pT_Bin_1), (Q2_y_Bin_15)-(z_pT_Bin_15)
(Q2_y_Bin_15)-(z_pT_Bin_2), (Q2_y_Bin_15)-(z_pT_Bin_24), (Q2_y_Bin_2)-(z_pT_Bin_1)
(Q2_y_Bin_2)-(z_pT_Bin_10), (Q2_y_Bin_2)-(z_pT_Bin_13), (Q2_y_Bin_2)-(z_pT_Bin_14)
(Q2_y_Bin_2)-(z_pT_Bin_15), (Q2_y_Bin_2)-(z_pT_Bin_19), (Q2_y_Bin_2)-(z_pT_Bin_2)
(Q2_y_Bin_2)-(z_pT_Bin_20), (Q2_y_Bin_2)-(z_pT_Bin_25), (Q2_y_Bin_2)-(z_pT_Bin_3)
(Q2_y_Bin_2)-(z_pT_Bin_32), (Q2_y_Bin_2)-(z_pT_Bin_4), (Q2_y_Bin_2)-(z_pT_Bin_5)
(Q2_y_Bin_2)-(z_pT_Bin_6), (Q2_y_Bin_2)-(z_pT_Bin_7), (Q2_y_Bin_2)-(z_pT_Bin_8)
(Q2_y_Bin_2)-(z_pT_Bin_9), (Q2_y_Bin_3)-(z_pT_Bin_1), (Q2_y_Bin_3)-(z_pT_Bin_10)
(Q2_y_Bin_3)-(z_pT_Bin_11), (Q2_y_Bin_3)-(z_pT_Bin_12), (Q2_y_Bin_3)-(z_pT_Bin_13)
(Q2_y_Bin_3)-(z_pT_Bin_15), (Q2_y_Bin_3)-(z_pT_Bin_16), (Q2_y_Bin_3)-(z_pT_Bin_18)
(Q2_y_Bin_3)-(z_pT_Bin_20), (Q2_y_Bin_3)-(z_pT_Bin_21), (Q2_y_Bin_3)-(z_pT_Bin_24)
(Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_7), (Q2_y_Bin_3)-(z_pT_Bin_8)
(Q2_y_Bin_3)-(z_pT_Bin_9), (Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_13)
(Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_19)
(Q2_y_Bin_4)-(z_pT_Bin_21), (Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_25)
(Q2_y_Bin_4)-(z_pT_Bin_27), (Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission]
(Q2_y_Bin_5)-(z_pT_Bin_13), (Q2_y_Bin_5)-(z_pT_Bin_19), (Q2_y_Bin_5)-(z_pT_Bin_3)
(Q2_y_Bin_5)-(z_pT_Bin_31), (Q2_y_Bin_5)-(z_pT_Bin_4), (Q2_y_Bin_5)-(z_pT_Bin_5)
(Q2_y_Bin_5)-(z_pT_Bin_6), (Q2_y_Bin_5)-(z_pT_Bin_8), (Q2_y_Bin_5)-(z_pT_Bin_9)
(Q2_y_Bin_6)-(z_pT_Bin_1), (Q2_y_Bin_6)-(z_pT_Bin_2), (Q2_y_Bin_6)-(z_pT_Bin_25)
(Q2_y_Bin_6)-(z_pT_Bin_26), (Q2_y_Bin_6)-(z_pT_Bin_27), (Q2_y_Bin_6)-(z_pT_Bin_3)
(Q2_y_Bin_6)-(z_pT_Bin_4), (Q2_y_Bin_6)-(z_pT_Bin_5), (Q2_y_Bin_6)-(z_pT_Bin_9)
(Q2_y_Bin_7)-(z_pT_Bin_1), (Q2_y_Bin_7)-(z_pT_Bin_11), (Q2_y_Bin_7)-(z_pT_Bin_12)
(Q2_y_Bin_7)-(z_pT_Bin_13), (Q2_y_Bin_7)-(z_pT_Bin_2), (Q2_y_Bin_7)-(z_pT_Bin_21)
(Q2_y_Bin_7)-(z_pT_Bin_24), (Q2_y_Bin_7)-(z_pT_Bin_31), (Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_11), (Q2_y_Bin_8)-(z_pT_Bin_13), (Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_16), (Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_28)
(Q2_y_Bin_8)-(z_pT_Bin_29), (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_9)-(z_pT_Bin_2)
(Q2_y_Bin_9)-(z_pT_Bin_3)

#### 180°

The rule fails every assessable manual exclusion (28).

Manually excluded but passes:

None.

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_15), (Q2_y_Bin_1)-(z_pT_Bin_3), (Q2_y_Bin_1)-(z_pT_Bin_30)
(Q2_y_Bin_1)-(z_pT_Bin_4), (Q2_y_Bin_1)-(z_pT_Bin_9), (Q2_y_Bin_10)-(z_pT_Bin_6)
(Q2_y_Bin_11)-(z_pT_Bin_22), (Q2_y_Bin_11)-(z_pT_Bin_24), (Q2_y_Bin_11)-(z_pT_Bin_3)
(Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_6), (Q2_y_Bin_12)-(z_pT_Bin_7)
(Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_15)-(z_pT_Bin_24), (Q2_y_Bin_2)-(z_pT_Bin_1)
(Q2_y_Bin_2)-(z_pT_Bin_2), (Q2_y_Bin_2)-(z_pT_Bin_3), (Q2_y_Bin_2)-(z_pT_Bin_4)
(Q2_y_Bin_2)-(z_pT_Bin_5), (Q2_y_Bin_2)-(z_pT_Bin_6), (Q2_y_Bin_2)-(z_pT_Bin_7)
(Q2_y_Bin_3)-(z_pT_Bin_1), (Q2_y_Bin_3)-(z_pT_Bin_10), (Q2_y_Bin_3)-(z_pT_Bin_13)
(Q2_y_Bin_3)-(z_pT_Bin_24), (Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_7)
(Q2_y_Bin_3)-(z_pT_Bin_9), (Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_13)
(Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_19)
(Q2_y_Bin_4)-(z_pT_Bin_21), (Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_25)
(Q2_y_Bin_4)-(z_pT_Bin_27), (Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission]
(Q2_y_Bin_5)-(z_pT_Bin_3), (Q2_y_Bin_5)-(z_pT_Bin_4), (Q2_y_Bin_6)-(z_pT_Bin_25)
(Q2_y_Bin_6)-(z_pT_Bin_26), (Q2_y_Bin_7)-(z_pT_Bin_12), (Q2_y_Bin_7)-(z_pT_Bin_2)
(Q2_y_Bin_7)-(z_pT_Bin_31), (Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_11)
(Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16), (Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_29), (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission]

### pipS2o

Manual list entries: 29. Fit-quality omissions relative to the nominal acceptance bins: 37. Comparisons the budget still keeps: 392.

#### 90°

The rule fails every assessable manual exclusion (29).

Manually excluded but passes:

None.

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_11), (Q2_y_Bin_1)-(z_pT_Bin_15)
(Q2_y_Bin_1)-(z_pT_Bin_16), (Q2_y_Bin_1)-(z_pT_Bin_17), (Q2_y_Bin_1)-(z_pT_Bin_22)
(Q2_y_Bin_1)-(z_pT_Bin_23), (Q2_y_Bin_1)-(z_pT_Bin_3), (Q2_y_Bin_1)-(z_pT_Bin_30)
(Q2_y_Bin_1)-(z_pT_Bin_31), (Q2_y_Bin_1)-(z_pT_Bin_32), (Q2_y_Bin_1)-(z_pT_Bin_4)
(Q2_y_Bin_1)-(z_pT_Bin_5), (Q2_y_Bin_1)-(z_pT_Bin_6), (Q2_y_Bin_1)-(z_pT_Bin_7)
(Q2_y_Bin_1)-(z_pT_Bin_8), (Q2_y_Bin_1)-(z_pT_Bin_9), (Q2_y_Bin_10)-(z_pT_Bin_1)
(Q2_y_Bin_10)-(z_pT_Bin_10), (Q2_y_Bin_10)-(z_pT_Bin_13), (Q2_y_Bin_10)-(z_pT_Bin_15)
(Q2_y_Bin_10)-(z_pT_Bin_2), (Q2_y_Bin_10)-(z_pT_Bin_20), (Q2_y_Bin_10)-(z_pT_Bin_26)
(Q2_y_Bin_10)-(z_pT_Bin_3), (Q2_y_Bin_10)-(z_pT_Bin_31), (Q2_y_Bin_10)-(z_pT_Bin_32)
(Q2_y_Bin_10)-(z_pT_Bin_4), (Q2_y_Bin_10)-(z_pT_Bin_5), (Q2_y_Bin_10)-(z_pT_Bin_6)
(Q2_y_Bin_10)-(z_pT_Bin_7), (Q2_y_Bin_10)-(z_pT_Bin_8), (Q2_y_Bin_10)-(z_pT_Bin_9)
(Q2_y_Bin_11)-(z_pT_Bin_1), (Q2_y_Bin_11)-(z_pT_Bin_10), (Q2_y_Bin_11)-(z_pT_Bin_11)
(Q2_y_Bin_11)-(z_pT_Bin_13), (Q2_y_Bin_11)-(z_pT_Bin_15), (Q2_y_Bin_11)-(z_pT_Bin_18)
(Q2_y_Bin_11)-(z_pT_Bin_2), (Q2_y_Bin_11)-(z_pT_Bin_20), (Q2_y_Bin_11)-(z_pT_Bin_21)
(Q2_y_Bin_11)-(z_pT_Bin_22), (Q2_y_Bin_11)-(z_pT_Bin_23), (Q2_y_Bin_11)-(z_pT_Bin_3)
(Q2_y_Bin_11)-(z_pT_Bin_4), (Q2_y_Bin_11)-(z_pT_Bin_6), (Q2_y_Bin_11)-(z_pT_Bin_8)
(Q2_y_Bin_11)-(z_pT_Bin_9), (Q2_y_Bin_12)-(z_pT_Bin_11), (Q2_y_Bin_12)-(z_pT_Bin_12)
(Q2_y_Bin_12)-(z_pT_Bin_13), (Q2_y_Bin_12)-(z_pT_Bin_16), (Q2_y_Bin_12)-(z_pT_Bin_18)
(Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_6), (Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_13)-(z_pT_Bin_1), (Q2_y_Bin_13)-(z_pT_Bin_12), (Q2_y_Bin_13)-(z_pT_Bin_13)
(Q2_y_Bin_13)-(z_pT_Bin_17), (Q2_y_Bin_13)-(z_pT_Bin_2), (Q2_y_Bin_13)-(z_pT_Bin_26)
(Q2_y_Bin_13)-(z_pT_Bin_3), (Q2_y_Bin_13)-(z_pT_Bin_4), (Q2_y_Bin_13)-(z_pT_Bin_5)
(Q2_y_Bin_13)-(z_pT_Bin_7), (Q2_y_Bin_13)-(z_pT_Bin_8), (Q2_y_Bin_13)-(z_pT_Bin_9)
(Q2_y_Bin_14)-(z_pT_Bin_1), (Q2_y_Bin_14)-(z_pT_Bin_10), (Q2_y_Bin_14)-(z_pT_Bin_2)
(Q2_y_Bin_14)-(z_pT_Bin_26), (Q2_y_Bin_14)-(z_pT_Bin_3), (Q2_y_Bin_14)-(z_pT_Bin_32)
(Q2_y_Bin_14)-(z_pT_Bin_4), (Q2_y_Bin_14)-(z_pT_Bin_5), (Q2_y_Bin_15)-(z_pT_Bin_1)
(Q2_y_Bin_15)-(z_pT_Bin_15), (Q2_y_Bin_15)-(z_pT_Bin_19), (Q2_y_Bin_15)-(z_pT_Bin_2)
(Q2_y_Bin_15)-(z_pT_Bin_21), (Q2_y_Bin_15)-(z_pT_Bin_22), (Q2_y_Bin_15)-(z_pT_Bin_23)
(Q2_y_Bin_15)-(z_pT_Bin_9), (Q2_y_Bin_16)-(z_pT_Bin_1), (Q2_y_Bin_16)-(z_pT_Bin_14)
(Q2_y_Bin_16)-(z_pT_Bin_3), (Q2_y_Bin_16)-(z_pT_Bin_4), (Q2_y_Bin_16)-(z_pT_Bin_5)
(Q2_y_Bin_16)-(z_pT_Bin_6), (Q2_y_Bin_16)-(z_pT_Bin_9), (Q2_y_Bin_17)-(z_pT_Bin_4)
(Q2_y_Bin_2)-(z_pT_Bin_1), (Q2_y_Bin_2)-(z_pT_Bin_10), (Q2_y_Bin_2)-(z_pT_Bin_11)
(Q2_y_Bin_2)-(z_pT_Bin_12), (Q2_y_Bin_2)-(z_pT_Bin_13), (Q2_y_Bin_2)-(z_pT_Bin_14)
(Q2_y_Bin_2)-(z_pT_Bin_15), (Q2_y_Bin_2)-(z_pT_Bin_16), (Q2_y_Bin_2)-(z_pT_Bin_17)
(Q2_y_Bin_2)-(z_pT_Bin_18), (Q2_y_Bin_2)-(z_pT_Bin_19), (Q2_y_Bin_2)-(z_pT_Bin_20)
(Q2_y_Bin_2)-(z_pT_Bin_21), (Q2_y_Bin_2)-(z_pT_Bin_22), (Q2_y_Bin_2)-(z_pT_Bin_23)
(Q2_y_Bin_2)-(z_pT_Bin_25), (Q2_y_Bin_2)-(z_pT_Bin_26), (Q2_y_Bin_2)-(z_pT_Bin_27)
(Q2_y_Bin_2)-(z_pT_Bin_28), (Q2_y_Bin_2)-(z_pT_Bin_3), (Q2_y_Bin_2)-(z_pT_Bin_32)
(Q2_y_Bin_2)-(z_pT_Bin_33), (Q2_y_Bin_2)-(z_pT_Bin_34), (Q2_y_Bin_2)-(z_pT_Bin_4)
(Q2_y_Bin_2)-(z_pT_Bin_5), (Q2_y_Bin_2)-(z_pT_Bin_6), (Q2_y_Bin_2)-(z_pT_Bin_7)
(Q2_y_Bin_2)-(z_pT_Bin_8), (Q2_y_Bin_2)-(z_pT_Bin_9), (Q2_y_Bin_3)-(z_pT_Bin_1)
(Q2_y_Bin_3)-(z_pT_Bin_10), (Q2_y_Bin_3)-(z_pT_Bin_11), (Q2_y_Bin_3)-(z_pT_Bin_12)
(Q2_y_Bin_3)-(z_pT_Bin_13), (Q2_y_Bin_3)-(z_pT_Bin_14), (Q2_y_Bin_3)-(z_pT_Bin_15)
(Q2_y_Bin_3)-(z_pT_Bin_16), (Q2_y_Bin_3)-(z_pT_Bin_17), (Q2_y_Bin_3)-(z_pT_Bin_18)
(Q2_y_Bin_3)-(z_pT_Bin_19), (Q2_y_Bin_3)-(z_pT_Bin_2), (Q2_y_Bin_3)-(z_pT_Bin_20)
(Q2_y_Bin_3)-(z_pT_Bin_21), (Q2_y_Bin_3)-(z_pT_Bin_22), (Q2_y_Bin_3)-(z_pT_Bin_23)
(Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_7), (Q2_y_Bin_3)-(z_pT_Bin_8)
(Q2_y_Bin_3)-(z_pT_Bin_9), (Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_13)
(Q2_y_Bin_4)-(z_pT_Bin_14), (Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_19), (Q2_y_Bin_4)-(z_pT_Bin_20), (Q2_y_Bin_4)-(z_pT_Bin_21)
(Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_25), (Q2_y_Bin_4)-(z_pT_Bin_26)
(Q2_y_Bin_4)-(z_pT_Bin_27), (Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission]
(Q2_y_Bin_5)-(z_pT_Bin_1), (Q2_y_Bin_5)-(z_pT_Bin_10), (Q2_y_Bin_5)-(z_pT_Bin_11)
(Q2_y_Bin_5)-(z_pT_Bin_13), (Q2_y_Bin_5)-(z_pT_Bin_14), (Q2_y_Bin_5)-(z_pT_Bin_15)
(Q2_y_Bin_5)-(z_pT_Bin_16), (Q2_y_Bin_5)-(z_pT_Bin_19), (Q2_y_Bin_5)-(z_pT_Bin_2)
(Q2_y_Bin_5)-(z_pT_Bin_20), (Q2_y_Bin_5)-(z_pT_Bin_25), (Q2_y_Bin_5)-(z_pT_Bin_26)
(Q2_y_Bin_5)-(z_pT_Bin_3), (Q2_y_Bin_5)-(z_pT_Bin_32), (Q2_y_Bin_5)-(z_pT_Bin_4)
(Q2_y_Bin_5)-(z_pT_Bin_5), (Q2_y_Bin_5)-(z_pT_Bin_6), (Q2_y_Bin_5)-(z_pT_Bin_8)
(Q2_y_Bin_5)-(z_pT_Bin_9), (Q2_y_Bin_6)-(z_pT_Bin_1), (Q2_y_Bin_6)-(z_pT_Bin_10)
(Q2_y_Bin_6)-(z_pT_Bin_11), (Q2_y_Bin_6)-(z_pT_Bin_13), (Q2_y_Bin_6)-(z_pT_Bin_14)
(Q2_y_Bin_6)-(z_pT_Bin_15), (Q2_y_Bin_6)-(z_pT_Bin_16), (Q2_y_Bin_6)-(z_pT_Bin_19)
(Q2_y_Bin_6)-(z_pT_Bin_2), (Q2_y_Bin_6)-(z_pT_Bin_20), (Q2_y_Bin_6)-(z_pT_Bin_27)
(Q2_y_Bin_6)-(z_pT_Bin_28), (Q2_y_Bin_6)-(z_pT_Bin_3), (Q2_y_Bin_6)-(z_pT_Bin_4)
(Q2_y_Bin_6)-(z_pT_Bin_5), (Q2_y_Bin_6)-(z_pT_Bin_6), (Q2_y_Bin_6)-(z_pT_Bin_7)
(Q2_y_Bin_6)-(z_pT_Bin_8), (Q2_y_Bin_6)-(z_pT_Bin_9), (Q2_y_Bin_7)-(z_pT_Bin_1)
(Q2_y_Bin_7)-(z_pT_Bin_10), (Q2_y_Bin_7)-(z_pT_Bin_11), (Q2_y_Bin_7)-(z_pT_Bin_12)
(Q2_y_Bin_7)-(z_pT_Bin_13), (Q2_y_Bin_7)-(z_pT_Bin_15), (Q2_y_Bin_7)-(z_pT_Bin_16)
(Q2_y_Bin_7)-(z_pT_Bin_17), (Q2_y_Bin_7)-(z_pT_Bin_18), (Q2_y_Bin_7)-(z_pT_Bin_19)
(Q2_y_Bin_7)-(z_pT_Bin_2), (Q2_y_Bin_7)-(z_pT_Bin_20), (Q2_y_Bin_7)-(z_pT_Bin_21)
(Q2_y_Bin_7)-(z_pT_Bin_22), (Q2_y_Bin_7)-(z_pT_Bin_23), (Q2_y_Bin_7)-(z_pT_Bin_24)
(Q2_y_Bin_7)-(z_pT_Bin_25), (Q2_y_Bin_7)-(z_pT_Bin_26), (Q2_y_Bin_7)-(z_pT_Bin_27)
(Q2_y_Bin_7)-(z_pT_Bin_28), (Q2_y_Bin_7)-(z_pT_Bin_29), (Q2_y_Bin_7)-(z_pT_Bin_31)
(Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_7)-(z_pT_Bin_7), (Q2_y_Bin_7)-(z_pT_Bin_8)
(Q2_y_Bin_7)-(z_pT_Bin_9), (Q2_y_Bin_8)-(z_pT_Bin_11), (Q2_y_Bin_8)-(z_pT_Bin_12)
(Q2_y_Bin_8)-(z_pT_Bin_13), (Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16)
(Q2_y_Bin_8)-(z_pT_Bin_18), (Q2_y_Bin_8)-(z_pT_Bin_19), (Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_21), (Q2_y_Bin_8)-(z_pT_Bin_23), (Q2_y_Bin_8)-(z_pT_Bin_24)
(Q2_y_Bin_8)-(z_pT_Bin_26), (Q2_y_Bin_8)-(z_pT_Bin_28), (Q2_y_Bin_8)-(z_pT_Bin_29)
(Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_9)-(z_pT_Bin_1), (Q2_y_Bin_9)-(z_pT_Bin_10)
(Q2_y_Bin_9)-(z_pT_Bin_11), (Q2_y_Bin_9)-(z_pT_Bin_15), (Q2_y_Bin_9)-(z_pT_Bin_16)
(Q2_y_Bin_9)-(z_pT_Bin_2), (Q2_y_Bin_9)-(z_pT_Bin_22), (Q2_y_Bin_9)-(z_pT_Bin_23)
(Q2_y_Bin_9)-(z_pT_Bin_29), (Q2_y_Bin_9)-(z_pT_Bin_3), (Q2_y_Bin_9)-(z_pT_Bin_30)
(Q2_y_Bin_9)-(z_pT_Bin_4), (Q2_y_Bin_9)-(z_pT_Bin_5), (Q2_y_Bin_9)-(z_pT_Bin_6)
(Q2_y_Bin_9)-(z_pT_Bin_8), (Q2_y_Bin_9)-(z_pT_Bin_9)

#### 120°

The rule fails every assessable manual exclusion (29).

Manually excluded but passes:

None.

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_15), (Q2_y_Bin_1)-(z_pT_Bin_16)
(Q2_y_Bin_1)-(z_pT_Bin_17), (Q2_y_Bin_1)-(z_pT_Bin_22), (Q2_y_Bin_1)-(z_pT_Bin_23)
(Q2_y_Bin_1)-(z_pT_Bin_3), (Q2_y_Bin_1)-(z_pT_Bin_30), (Q2_y_Bin_1)-(z_pT_Bin_31)
(Q2_y_Bin_1)-(z_pT_Bin_32), (Q2_y_Bin_1)-(z_pT_Bin_4), (Q2_y_Bin_1)-(z_pT_Bin_5)
(Q2_y_Bin_1)-(z_pT_Bin_6), (Q2_y_Bin_1)-(z_pT_Bin_7), (Q2_y_Bin_1)-(z_pT_Bin_8)
(Q2_y_Bin_1)-(z_pT_Bin_9), (Q2_y_Bin_10)-(z_pT_Bin_1), (Q2_y_Bin_10)-(z_pT_Bin_15)
(Q2_y_Bin_10)-(z_pT_Bin_2), (Q2_y_Bin_10)-(z_pT_Bin_26), (Q2_y_Bin_10)-(z_pT_Bin_3)
(Q2_y_Bin_10)-(z_pT_Bin_32), (Q2_y_Bin_10)-(z_pT_Bin_4), (Q2_y_Bin_10)-(z_pT_Bin_5)
(Q2_y_Bin_10)-(z_pT_Bin_6), (Q2_y_Bin_10)-(z_pT_Bin_7), (Q2_y_Bin_11)-(z_pT_Bin_1)
(Q2_y_Bin_11)-(z_pT_Bin_10), (Q2_y_Bin_11)-(z_pT_Bin_2), (Q2_y_Bin_11)-(z_pT_Bin_20)
(Q2_y_Bin_11)-(z_pT_Bin_21), (Q2_y_Bin_11)-(z_pT_Bin_22), (Q2_y_Bin_11)-(z_pT_Bin_23)
(Q2_y_Bin_11)-(z_pT_Bin_3), (Q2_y_Bin_11)-(z_pT_Bin_4), (Q2_y_Bin_11)-(z_pT_Bin_6)
(Q2_y_Bin_11)-(z_pT_Bin_9), (Q2_y_Bin_12)-(z_pT_Bin_11), (Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission]
(Q2_y_Bin_12)-(z_pT_Bin_6), (Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_13)-(z_pT_Bin_1)
(Q2_y_Bin_13)-(z_pT_Bin_2), (Q2_y_Bin_13)-(z_pT_Bin_3), (Q2_y_Bin_13)-(z_pT_Bin_4)
(Q2_y_Bin_13)-(z_pT_Bin_5), (Q2_y_Bin_14)-(z_pT_Bin_2), (Q2_y_Bin_14)-(z_pT_Bin_32)
(Q2_y_Bin_14)-(z_pT_Bin_4), (Q2_y_Bin_14)-(z_pT_Bin_5), (Q2_y_Bin_15)-(z_pT_Bin_1)
(Q2_y_Bin_15)-(z_pT_Bin_15), (Q2_y_Bin_15)-(z_pT_Bin_2), (Q2_y_Bin_15)-(z_pT_Bin_22)
(Q2_y_Bin_15)-(z_pT_Bin_23), (Q2_y_Bin_16)-(z_pT_Bin_5), (Q2_y_Bin_16)-(z_pT_Bin_6)
(Q2_y_Bin_2)-(z_pT_Bin_1), (Q2_y_Bin_2)-(z_pT_Bin_10), (Q2_y_Bin_2)-(z_pT_Bin_11)
(Q2_y_Bin_2)-(z_pT_Bin_13), (Q2_y_Bin_2)-(z_pT_Bin_14), (Q2_y_Bin_2)-(z_pT_Bin_15)
(Q2_y_Bin_2)-(z_pT_Bin_16), (Q2_y_Bin_2)-(z_pT_Bin_19), (Q2_y_Bin_2)-(z_pT_Bin_20)
(Q2_y_Bin_2)-(z_pT_Bin_21), (Q2_y_Bin_2)-(z_pT_Bin_25), (Q2_y_Bin_2)-(z_pT_Bin_26)
(Q2_y_Bin_2)-(z_pT_Bin_27), (Q2_y_Bin_2)-(z_pT_Bin_3), (Q2_y_Bin_2)-(z_pT_Bin_32)
(Q2_y_Bin_2)-(z_pT_Bin_33), (Q2_y_Bin_2)-(z_pT_Bin_34), (Q2_y_Bin_2)-(z_pT_Bin_4)
(Q2_y_Bin_2)-(z_pT_Bin_5), (Q2_y_Bin_2)-(z_pT_Bin_6), (Q2_y_Bin_2)-(z_pT_Bin_7)
(Q2_y_Bin_2)-(z_pT_Bin_8), (Q2_y_Bin_2)-(z_pT_Bin_9), (Q2_y_Bin_3)-(z_pT_Bin_1)
(Q2_y_Bin_3)-(z_pT_Bin_10), (Q2_y_Bin_3)-(z_pT_Bin_11), (Q2_y_Bin_3)-(z_pT_Bin_12)
(Q2_y_Bin_3)-(z_pT_Bin_13), (Q2_y_Bin_3)-(z_pT_Bin_14), (Q2_y_Bin_3)-(z_pT_Bin_15)
(Q2_y_Bin_3)-(z_pT_Bin_16), (Q2_y_Bin_3)-(z_pT_Bin_17), (Q2_y_Bin_3)-(z_pT_Bin_18)
(Q2_y_Bin_3)-(z_pT_Bin_19), (Q2_y_Bin_3)-(z_pT_Bin_2), (Q2_y_Bin_3)-(z_pT_Bin_20)
(Q2_y_Bin_3)-(z_pT_Bin_21), (Q2_y_Bin_3)-(z_pT_Bin_22), (Q2_y_Bin_3)-(z_pT_Bin_23)
(Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_7), (Q2_y_Bin_3)-(z_pT_Bin_8)
(Q2_y_Bin_3)-(z_pT_Bin_9), (Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_13)
(Q2_y_Bin_4)-(z_pT_Bin_14), (Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_19), (Q2_y_Bin_4)-(z_pT_Bin_20), (Q2_y_Bin_4)-(z_pT_Bin_21)
(Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_25), (Q2_y_Bin_4)-(z_pT_Bin_26)
(Q2_y_Bin_4)-(z_pT_Bin_27), (Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission]
(Q2_y_Bin_5)-(z_pT_Bin_1), (Q2_y_Bin_5)-(z_pT_Bin_10), (Q2_y_Bin_5)-(z_pT_Bin_13)
(Q2_y_Bin_5)-(z_pT_Bin_14), (Q2_y_Bin_5)-(z_pT_Bin_15), (Q2_y_Bin_5)-(z_pT_Bin_19)
(Q2_y_Bin_5)-(z_pT_Bin_2), (Q2_y_Bin_5)-(z_pT_Bin_20), (Q2_y_Bin_5)-(z_pT_Bin_25)
(Q2_y_Bin_5)-(z_pT_Bin_3), (Q2_y_Bin_5)-(z_pT_Bin_32), (Q2_y_Bin_5)-(z_pT_Bin_4)
(Q2_y_Bin_5)-(z_pT_Bin_5), (Q2_y_Bin_5)-(z_pT_Bin_6), (Q2_y_Bin_5)-(z_pT_Bin_8)
(Q2_y_Bin_5)-(z_pT_Bin_9), (Q2_y_Bin_6)-(z_pT_Bin_1), (Q2_y_Bin_6)-(z_pT_Bin_10)
(Q2_y_Bin_6)-(z_pT_Bin_14), (Q2_y_Bin_6)-(z_pT_Bin_19), (Q2_y_Bin_6)-(z_pT_Bin_2)
(Q2_y_Bin_6)-(z_pT_Bin_20), (Q2_y_Bin_6)-(z_pT_Bin_27), (Q2_y_Bin_6)-(z_pT_Bin_28)
(Q2_y_Bin_6)-(z_pT_Bin_3), (Q2_y_Bin_6)-(z_pT_Bin_4), (Q2_y_Bin_6)-(z_pT_Bin_5)
(Q2_y_Bin_6)-(z_pT_Bin_6), (Q2_y_Bin_6)-(z_pT_Bin_7), (Q2_y_Bin_6)-(z_pT_Bin_8)
(Q2_y_Bin_6)-(z_pT_Bin_9), (Q2_y_Bin_7)-(z_pT_Bin_1), (Q2_y_Bin_7)-(z_pT_Bin_10)
(Q2_y_Bin_7)-(z_pT_Bin_11), (Q2_y_Bin_7)-(z_pT_Bin_12), (Q2_y_Bin_7)-(z_pT_Bin_13)
(Q2_y_Bin_7)-(z_pT_Bin_15), (Q2_y_Bin_7)-(z_pT_Bin_16), (Q2_y_Bin_7)-(z_pT_Bin_17)
(Q2_y_Bin_7)-(z_pT_Bin_18), (Q2_y_Bin_7)-(z_pT_Bin_2), (Q2_y_Bin_7)-(z_pT_Bin_21)
(Q2_y_Bin_7)-(z_pT_Bin_24), (Q2_y_Bin_7)-(z_pT_Bin_26), (Q2_y_Bin_7)-(z_pT_Bin_27)
(Q2_y_Bin_7)-(z_pT_Bin_29), (Q2_y_Bin_7)-(z_pT_Bin_31), (Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission]
(Q2_y_Bin_7)-(z_pT_Bin_7), (Q2_y_Bin_7)-(z_pT_Bin_8), (Q2_y_Bin_7)-(z_pT_Bin_9)
(Q2_y_Bin_8)-(z_pT_Bin_11), (Q2_y_Bin_8)-(z_pT_Bin_12), (Q2_y_Bin_8)-(z_pT_Bin_13)
(Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16), (Q2_y_Bin_8)-(z_pT_Bin_18)
(Q2_y_Bin_8)-(z_pT_Bin_19), (Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_21)
(Q2_y_Bin_8)-(z_pT_Bin_23), (Q2_y_Bin_8)-(z_pT_Bin_24), (Q2_y_Bin_8)-(z_pT_Bin_26)
(Q2_y_Bin_8)-(z_pT_Bin_28), (Q2_y_Bin_8)-(z_pT_Bin_29), (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_9)-(z_pT_Bin_1), (Q2_y_Bin_9)-(z_pT_Bin_10), (Q2_y_Bin_9)-(z_pT_Bin_16)
(Q2_y_Bin_9)-(z_pT_Bin_2), (Q2_y_Bin_9)-(z_pT_Bin_29), (Q2_y_Bin_9)-(z_pT_Bin_3)
(Q2_y_Bin_9)-(z_pT_Bin_4), (Q2_y_Bin_9)-(z_pT_Bin_5), (Q2_y_Bin_9)-(z_pT_Bin_6)
(Q2_y_Bin_9)-(z_pT_Bin_8), (Q2_y_Bin_9)-(z_pT_Bin_9)

#### 135°

The rule fails every assessable manual exclusion (29).

Manually excluded but passes:

None.

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_15), (Q2_y_Bin_1)-(z_pT_Bin_16)
(Q2_y_Bin_1)-(z_pT_Bin_22), (Q2_y_Bin_1)-(z_pT_Bin_3), (Q2_y_Bin_1)-(z_pT_Bin_30)
(Q2_y_Bin_1)-(z_pT_Bin_31), (Q2_y_Bin_1)-(z_pT_Bin_32), (Q2_y_Bin_1)-(z_pT_Bin_4)
(Q2_y_Bin_1)-(z_pT_Bin_5), (Q2_y_Bin_1)-(z_pT_Bin_6), (Q2_y_Bin_1)-(z_pT_Bin_7)
(Q2_y_Bin_1)-(z_pT_Bin_8), (Q2_y_Bin_1)-(z_pT_Bin_9), (Q2_y_Bin_10)-(z_pT_Bin_1)
(Q2_y_Bin_10)-(z_pT_Bin_2), (Q2_y_Bin_10)-(z_pT_Bin_3), (Q2_y_Bin_10)-(z_pT_Bin_32)
(Q2_y_Bin_10)-(z_pT_Bin_4), (Q2_y_Bin_10)-(z_pT_Bin_5), (Q2_y_Bin_10)-(z_pT_Bin_6)
(Q2_y_Bin_10)-(z_pT_Bin_7), (Q2_y_Bin_11)-(z_pT_Bin_1), (Q2_y_Bin_11)-(z_pT_Bin_10)
(Q2_y_Bin_11)-(z_pT_Bin_2), (Q2_y_Bin_11)-(z_pT_Bin_20), (Q2_y_Bin_11)-(z_pT_Bin_21)
(Q2_y_Bin_11)-(z_pT_Bin_22), (Q2_y_Bin_11)-(z_pT_Bin_23), (Q2_y_Bin_11)-(z_pT_Bin_3)
(Q2_y_Bin_11)-(z_pT_Bin_4), (Q2_y_Bin_11)-(z_pT_Bin_6), (Q2_y_Bin_12)-(z_pT_Bin_11)
(Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_6), (Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_13)-(z_pT_Bin_1), (Q2_y_Bin_13)-(z_pT_Bin_2), (Q2_y_Bin_13)-(z_pT_Bin_4)
(Q2_y_Bin_14)-(z_pT_Bin_2), (Q2_y_Bin_14)-(z_pT_Bin_32), (Q2_y_Bin_14)-(z_pT_Bin_5)
(Q2_y_Bin_15)-(z_pT_Bin_1), (Q2_y_Bin_15)-(z_pT_Bin_15), (Q2_y_Bin_15)-(z_pT_Bin_2)
(Q2_y_Bin_15)-(z_pT_Bin_22), (Q2_y_Bin_15)-(z_pT_Bin_23), (Q2_y_Bin_16)-(z_pT_Bin_5)
(Q2_y_Bin_16)-(z_pT_Bin_6), (Q2_y_Bin_2)-(z_pT_Bin_1), (Q2_y_Bin_2)-(z_pT_Bin_10)
(Q2_y_Bin_2)-(z_pT_Bin_11), (Q2_y_Bin_2)-(z_pT_Bin_13), (Q2_y_Bin_2)-(z_pT_Bin_14)
(Q2_y_Bin_2)-(z_pT_Bin_15), (Q2_y_Bin_2)-(z_pT_Bin_16), (Q2_y_Bin_2)-(z_pT_Bin_19)
(Q2_y_Bin_2)-(z_pT_Bin_20), (Q2_y_Bin_2)-(z_pT_Bin_25), (Q2_y_Bin_2)-(z_pT_Bin_3)
(Q2_y_Bin_2)-(z_pT_Bin_32), (Q2_y_Bin_2)-(z_pT_Bin_33), (Q2_y_Bin_2)-(z_pT_Bin_34)
(Q2_y_Bin_2)-(z_pT_Bin_4), (Q2_y_Bin_2)-(z_pT_Bin_5), (Q2_y_Bin_2)-(z_pT_Bin_6)
(Q2_y_Bin_2)-(z_pT_Bin_7), (Q2_y_Bin_2)-(z_pT_Bin_8), (Q2_y_Bin_2)-(z_pT_Bin_9)
(Q2_y_Bin_3)-(z_pT_Bin_1), (Q2_y_Bin_3)-(z_pT_Bin_10), (Q2_y_Bin_3)-(z_pT_Bin_11)
(Q2_y_Bin_3)-(z_pT_Bin_12), (Q2_y_Bin_3)-(z_pT_Bin_13), (Q2_y_Bin_3)-(z_pT_Bin_14)
(Q2_y_Bin_3)-(z_pT_Bin_15), (Q2_y_Bin_3)-(z_pT_Bin_16), (Q2_y_Bin_3)-(z_pT_Bin_17)
(Q2_y_Bin_3)-(z_pT_Bin_18), (Q2_y_Bin_3)-(z_pT_Bin_19), (Q2_y_Bin_3)-(z_pT_Bin_2)
(Q2_y_Bin_3)-(z_pT_Bin_20), (Q2_y_Bin_3)-(z_pT_Bin_21), (Q2_y_Bin_3)-(z_pT_Bin_22)
(Q2_y_Bin_3)-(z_pT_Bin_23), (Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_7)
(Q2_y_Bin_3)-(z_pT_Bin_8), (Q2_y_Bin_3)-(z_pT_Bin_9), (Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_13), (Q2_y_Bin_4)-(z_pT_Bin_14), (Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_19), (Q2_y_Bin_4)-(z_pT_Bin_20)
(Q2_y_Bin_4)-(z_pT_Bin_21), (Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_25)
(Q2_y_Bin_4)-(z_pT_Bin_26), (Q2_y_Bin_4)-(z_pT_Bin_27), (Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission], (Q2_y_Bin_5)-(z_pT_Bin_1), (Q2_y_Bin_5)-(z_pT_Bin_10)
(Q2_y_Bin_5)-(z_pT_Bin_13), (Q2_y_Bin_5)-(z_pT_Bin_14), (Q2_y_Bin_5)-(z_pT_Bin_15)
(Q2_y_Bin_5)-(z_pT_Bin_19), (Q2_y_Bin_5)-(z_pT_Bin_2), (Q2_y_Bin_5)-(z_pT_Bin_20)
(Q2_y_Bin_5)-(z_pT_Bin_25), (Q2_y_Bin_5)-(z_pT_Bin_3), (Q2_y_Bin_5)-(z_pT_Bin_32)
(Q2_y_Bin_5)-(z_pT_Bin_4), (Q2_y_Bin_5)-(z_pT_Bin_5), (Q2_y_Bin_5)-(z_pT_Bin_6)
(Q2_y_Bin_5)-(z_pT_Bin_8), (Q2_y_Bin_5)-(z_pT_Bin_9), (Q2_y_Bin_6)-(z_pT_Bin_1)
(Q2_y_Bin_6)-(z_pT_Bin_10), (Q2_y_Bin_6)-(z_pT_Bin_14), (Q2_y_Bin_6)-(z_pT_Bin_2)
(Q2_y_Bin_6)-(z_pT_Bin_20), (Q2_y_Bin_6)-(z_pT_Bin_27), (Q2_y_Bin_6)-(z_pT_Bin_28)
(Q2_y_Bin_6)-(z_pT_Bin_3), (Q2_y_Bin_6)-(z_pT_Bin_4), (Q2_y_Bin_6)-(z_pT_Bin_5)
(Q2_y_Bin_6)-(z_pT_Bin_6), (Q2_y_Bin_6)-(z_pT_Bin_7), (Q2_y_Bin_6)-(z_pT_Bin_8)
(Q2_y_Bin_6)-(z_pT_Bin_9), (Q2_y_Bin_7)-(z_pT_Bin_1), (Q2_y_Bin_7)-(z_pT_Bin_10)
(Q2_y_Bin_7)-(z_pT_Bin_11), (Q2_y_Bin_7)-(z_pT_Bin_12), (Q2_y_Bin_7)-(z_pT_Bin_13)
(Q2_y_Bin_7)-(z_pT_Bin_18), (Q2_y_Bin_7)-(z_pT_Bin_2), (Q2_y_Bin_7)-(z_pT_Bin_21)
(Q2_y_Bin_7)-(z_pT_Bin_24), (Q2_y_Bin_7)-(z_pT_Bin_27), (Q2_y_Bin_7)-(z_pT_Bin_29)
(Q2_y_Bin_7)-(z_pT_Bin_31), (Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_7)-(z_pT_Bin_7)
(Q2_y_Bin_7)-(z_pT_Bin_9), (Q2_y_Bin_8)-(z_pT_Bin_11), (Q2_y_Bin_8)-(z_pT_Bin_13)
(Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16), (Q2_y_Bin_8)-(z_pT_Bin_18)
(Q2_y_Bin_8)-(z_pT_Bin_19), (Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_21)
(Q2_y_Bin_8)-(z_pT_Bin_23), (Q2_y_Bin_8)-(z_pT_Bin_24), (Q2_y_Bin_8)-(z_pT_Bin_28)
(Q2_y_Bin_8)-(z_pT_Bin_29), (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_9)-(z_pT_Bin_1)
(Q2_y_Bin_9)-(z_pT_Bin_10), (Q2_y_Bin_9)-(z_pT_Bin_16), (Q2_y_Bin_9)-(z_pT_Bin_2)
(Q2_y_Bin_9)-(z_pT_Bin_29), (Q2_y_Bin_9)-(z_pT_Bin_3), (Q2_y_Bin_9)-(z_pT_Bin_4)
(Q2_y_Bin_9)-(z_pT_Bin_8)

#### 150°

The rule fails every assessable manual exclusion (29).

Manually excluded but passes:

None.

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_15), (Q2_y_Bin_1)-(z_pT_Bin_16)
(Q2_y_Bin_1)-(z_pT_Bin_22), (Q2_y_Bin_1)-(z_pT_Bin_3), (Q2_y_Bin_1)-(z_pT_Bin_30)
(Q2_y_Bin_1)-(z_pT_Bin_4), (Q2_y_Bin_1)-(z_pT_Bin_5), (Q2_y_Bin_1)-(z_pT_Bin_6)
(Q2_y_Bin_1)-(z_pT_Bin_7), (Q2_y_Bin_1)-(z_pT_Bin_8), (Q2_y_Bin_1)-(z_pT_Bin_9)
(Q2_y_Bin_10)-(z_pT_Bin_2), (Q2_y_Bin_10)-(z_pT_Bin_3), (Q2_y_Bin_10)-(z_pT_Bin_32)
(Q2_y_Bin_10)-(z_pT_Bin_4), (Q2_y_Bin_10)-(z_pT_Bin_5), (Q2_y_Bin_10)-(z_pT_Bin_6)
(Q2_y_Bin_10)-(z_pT_Bin_7), (Q2_y_Bin_11)-(z_pT_Bin_1), (Q2_y_Bin_11)-(z_pT_Bin_2)
(Q2_y_Bin_11)-(z_pT_Bin_20), (Q2_y_Bin_11)-(z_pT_Bin_21), (Q2_y_Bin_11)-(z_pT_Bin_22)
(Q2_y_Bin_11)-(z_pT_Bin_23), (Q2_y_Bin_11)-(z_pT_Bin_3), (Q2_y_Bin_11)-(z_pT_Bin_4)
(Q2_y_Bin_12)-(z_pT_Bin_11), (Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_6)
(Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_13)-(z_pT_Bin_1), (Q2_y_Bin_13)-(z_pT_Bin_2)
(Q2_y_Bin_14)-(z_pT_Bin_2), (Q2_y_Bin_14)-(z_pT_Bin_5), (Q2_y_Bin_15)-(z_pT_Bin_1)
(Q2_y_Bin_15)-(z_pT_Bin_15), (Q2_y_Bin_15)-(z_pT_Bin_2), (Q2_y_Bin_15)-(z_pT_Bin_23)
(Q2_y_Bin_2)-(z_pT_Bin_1), (Q2_y_Bin_2)-(z_pT_Bin_10), (Q2_y_Bin_2)-(z_pT_Bin_13)
(Q2_y_Bin_2)-(z_pT_Bin_14), (Q2_y_Bin_2)-(z_pT_Bin_15), (Q2_y_Bin_2)-(z_pT_Bin_19)
(Q2_y_Bin_2)-(z_pT_Bin_20), (Q2_y_Bin_2)-(z_pT_Bin_25), (Q2_y_Bin_2)-(z_pT_Bin_3)
(Q2_y_Bin_2)-(z_pT_Bin_32), (Q2_y_Bin_2)-(z_pT_Bin_4), (Q2_y_Bin_2)-(z_pT_Bin_5)
(Q2_y_Bin_2)-(z_pT_Bin_6), (Q2_y_Bin_2)-(z_pT_Bin_7), (Q2_y_Bin_2)-(z_pT_Bin_8)
(Q2_y_Bin_2)-(z_pT_Bin_9), (Q2_y_Bin_3)-(z_pT_Bin_1), (Q2_y_Bin_3)-(z_pT_Bin_10)
(Q2_y_Bin_3)-(z_pT_Bin_11), (Q2_y_Bin_3)-(z_pT_Bin_12), (Q2_y_Bin_3)-(z_pT_Bin_13)
(Q2_y_Bin_3)-(z_pT_Bin_15), (Q2_y_Bin_3)-(z_pT_Bin_16), (Q2_y_Bin_3)-(z_pT_Bin_18)
(Q2_y_Bin_3)-(z_pT_Bin_2), (Q2_y_Bin_3)-(z_pT_Bin_20), (Q2_y_Bin_3)-(z_pT_Bin_21)
(Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_7), (Q2_y_Bin_3)-(z_pT_Bin_8)
(Q2_y_Bin_3)-(z_pT_Bin_9), (Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_13)
(Q2_y_Bin_4)-(z_pT_Bin_14), (Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_19), (Q2_y_Bin_4)-(z_pT_Bin_21), (Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_25), (Q2_y_Bin_4)-(z_pT_Bin_27), (Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission], (Q2_y_Bin_5)-(z_pT_Bin_1), (Q2_y_Bin_5)-(z_pT_Bin_10)
(Q2_y_Bin_5)-(z_pT_Bin_13), (Q2_y_Bin_5)-(z_pT_Bin_14), (Q2_y_Bin_5)-(z_pT_Bin_19)
(Q2_y_Bin_5)-(z_pT_Bin_2), (Q2_y_Bin_5)-(z_pT_Bin_25), (Q2_y_Bin_5)-(z_pT_Bin_3)
(Q2_y_Bin_5)-(z_pT_Bin_32), (Q2_y_Bin_5)-(z_pT_Bin_4), (Q2_y_Bin_5)-(z_pT_Bin_5)
(Q2_y_Bin_5)-(z_pT_Bin_6), (Q2_y_Bin_5)-(z_pT_Bin_8), (Q2_y_Bin_5)-(z_pT_Bin_9)
(Q2_y_Bin_6)-(z_pT_Bin_1), (Q2_y_Bin_6)-(z_pT_Bin_14), (Q2_y_Bin_6)-(z_pT_Bin_2)
(Q2_y_Bin_6)-(z_pT_Bin_20), (Q2_y_Bin_6)-(z_pT_Bin_27), (Q2_y_Bin_6)-(z_pT_Bin_3)
(Q2_y_Bin_6)-(z_pT_Bin_4), (Q2_y_Bin_6)-(z_pT_Bin_5), (Q2_y_Bin_6)-(z_pT_Bin_6)
(Q2_y_Bin_6)-(z_pT_Bin_7), (Q2_y_Bin_6)-(z_pT_Bin_9), (Q2_y_Bin_7)-(z_pT_Bin_1)
(Q2_y_Bin_7)-(z_pT_Bin_11), (Q2_y_Bin_7)-(z_pT_Bin_12), (Q2_y_Bin_7)-(z_pT_Bin_13)
(Q2_y_Bin_7)-(z_pT_Bin_2), (Q2_y_Bin_7)-(z_pT_Bin_21), (Q2_y_Bin_7)-(z_pT_Bin_24)
(Q2_y_Bin_7)-(z_pT_Bin_29), (Q2_y_Bin_7)-(z_pT_Bin_31), (Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission]
(Q2_y_Bin_7)-(z_pT_Bin_7), (Q2_y_Bin_8)-(z_pT_Bin_11), (Q2_y_Bin_8)-(z_pT_Bin_13)
(Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16), (Q2_y_Bin_8)-(z_pT_Bin_19)
(Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_21), (Q2_y_Bin_8)-(z_pT_Bin_24)
(Q2_y_Bin_8)-(z_pT_Bin_28), (Q2_y_Bin_8)-(z_pT_Bin_29), (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_9)-(z_pT_Bin_1), (Q2_y_Bin_9)-(z_pT_Bin_2), (Q2_y_Bin_9)-(z_pT_Bin_29)
(Q2_y_Bin_9)-(z_pT_Bin_3), (Q2_y_Bin_9)-(z_pT_Bin_4), (Q2_y_Bin_9)-(z_pT_Bin_8)

#### 180°

The rule fails every assessable manual exclusion (29).

Manually excluded but passes:

None.

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_15), (Q2_y_Bin_1)-(z_pT_Bin_3)
(Q2_y_Bin_1)-(z_pT_Bin_30), (Q2_y_Bin_1)-(z_pT_Bin_4), (Q2_y_Bin_1)-(z_pT_Bin_5)
(Q2_y_Bin_1)-(z_pT_Bin_8), (Q2_y_Bin_1)-(z_pT_Bin_9), (Q2_y_Bin_10)-(z_pT_Bin_2)
(Q2_y_Bin_10)-(z_pT_Bin_6), (Q2_y_Bin_11)-(z_pT_Bin_22), (Q2_y_Bin_11)-(z_pT_Bin_23)
(Q2_y_Bin_11)-(z_pT_Bin_3), (Q2_y_Bin_11)-(z_pT_Bin_4), (Q2_y_Bin_12)-(z_pT_Bin_11)
(Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_6), (Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_13)-(z_pT_Bin_1), (Q2_y_Bin_15)-(z_pT_Bin_15), (Q2_y_Bin_15)-(z_pT_Bin_2)
(Q2_y_Bin_2)-(z_pT_Bin_1), (Q2_y_Bin_2)-(z_pT_Bin_19), (Q2_y_Bin_2)-(z_pT_Bin_20)
(Q2_y_Bin_2)-(z_pT_Bin_3), (Q2_y_Bin_2)-(z_pT_Bin_32), (Q2_y_Bin_2)-(z_pT_Bin_4)
(Q2_y_Bin_2)-(z_pT_Bin_5), (Q2_y_Bin_2)-(z_pT_Bin_6), (Q2_y_Bin_2)-(z_pT_Bin_7)
(Q2_y_Bin_2)-(z_pT_Bin_9), (Q2_y_Bin_3)-(z_pT_Bin_1), (Q2_y_Bin_3)-(z_pT_Bin_10)
(Q2_y_Bin_3)-(z_pT_Bin_13), (Q2_y_Bin_3)-(z_pT_Bin_2), (Q2_y_Bin_3)-(z_pT_Bin_20)
(Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_7), (Q2_y_Bin_3)-(z_pT_Bin_9)
(Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_13), (Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_19), (Q2_y_Bin_4)-(z_pT_Bin_21)
(Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_25), (Q2_y_Bin_4)-(z_pT_Bin_27)
(Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission], (Q2_y_Bin_5)-(z_pT_Bin_1)
(Q2_y_Bin_5)-(z_pT_Bin_13), (Q2_y_Bin_5)-(z_pT_Bin_2), (Q2_y_Bin_5)-(z_pT_Bin_3)
(Q2_y_Bin_5)-(z_pT_Bin_4), (Q2_y_Bin_5)-(z_pT_Bin_5), (Q2_y_Bin_6)-(z_pT_Bin_2)
(Q2_y_Bin_6)-(z_pT_Bin_7), (Q2_y_Bin_7)-(z_pT_Bin_1), (Q2_y_Bin_7)-(z_pT_Bin_12)
(Q2_y_Bin_7)-(z_pT_Bin_13), (Q2_y_Bin_7)-(z_pT_Bin_2), (Q2_y_Bin_7)-(z_pT_Bin_24)
(Q2_y_Bin_7)-(z_pT_Bin_31), (Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_11)
(Q2_y_Bin_8)-(z_pT_Bin_13), (Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16)
(Q2_y_Bin_8)-(z_pT_Bin_19), (Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_24)
(Q2_y_Bin_8)-(z_pT_Bin_29), (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_9)-(z_pT_Bin_1)
(Q2_y_Bin_9)-(z_pT_Bin_2), (Q2_y_Bin_9)-(z_pT_Bin_29), (Q2_y_Bin_9)-(z_pT_Bin_4)

### pipS3o

Manual list entries: 40. Fit-quality omissions relative to the nominal acceptance bins: 37. Comparisons the budget still keeps: 381.

#### 90°

The rule fails every assessable manual exclusion (40).

Manually excluded but passes:

None.

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_11), (Q2_y_Bin_1)-(z_pT_Bin_16)
(Q2_y_Bin_1)-(z_pT_Bin_17), (Q2_y_Bin_1)-(z_pT_Bin_23), (Q2_y_Bin_1)-(z_pT_Bin_30)
(Q2_y_Bin_1)-(z_pT_Bin_31), (Q2_y_Bin_1)-(z_pT_Bin_32), (Q2_y_Bin_1)-(z_pT_Bin_5)
(Q2_y_Bin_1)-(z_pT_Bin_6), (Q2_y_Bin_1)-(z_pT_Bin_7), (Q2_y_Bin_1)-(z_pT_Bin_9)
(Q2_y_Bin_10)-(z_pT_Bin_1), (Q2_y_Bin_10)-(z_pT_Bin_10), (Q2_y_Bin_10)-(z_pT_Bin_11)
(Q2_y_Bin_10)-(z_pT_Bin_12), (Q2_y_Bin_10)-(z_pT_Bin_13), (Q2_y_Bin_10)-(z_pT_Bin_15)
(Q2_y_Bin_10)-(z_pT_Bin_2), (Q2_y_Bin_10)-(z_pT_Bin_20), (Q2_y_Bin_10)-(z_pT_Bin_21)
(Q2_y_Bin_10)-(z_pT_Bin_26), (Q2_y_Bin_10)-(z_pT_Bin_3), (Q2_y_Bin_10)-(z_pT_Bin_31)
(Q2_y_Bin_10)-(z_pT_Bin_34), (Q2_y_Bin_10)-(z_pT_Bin_4), (Q2_y_Bin_10)-(z_pT_Bin_5)
(Q2_y_Bin_10)-(z_pT_Bin_6), (Q2_y_Bin_10)-(z_pT_Bin_7), (Q2_y_Bin_10)-(z_pT_Bin_8)
(Q2_y_Bin_10)-(z_pT_Bin_9), (Q2_y_Bin_11)-(z_pT_Bin_1), (Q2_y_Bin_11)-(z_pT_Bin_10)
(Q2_y_Bin_11)-(z_pT_Bin_11), (Q2_y_Bin_11)-(z_pT_Bin_13), (Q2_y_Bin_11)-(z_pT_Bin_14)
(Q2_y_Bin_11)-(z_pT_Bin_15), (Q2_y_Bin_11)-(z_pT_Bin_18), (Q2_y_Bin_11)-(z_pT_Bin_19)
(Q2_y_Bin_11)-(z_pT_Bin_2), (Q2_y_Bin_11)-(z_pT_Bin_21), (Q2_y_Bin_11)-(z_pT_Bin_23)
(Q2_y_Bin_11)-(z_pT_Bin_3), (Q2_y_Bin_11)-(z_pT_Bin_6), (Q2_y_Bin_11)-(z_pT_Bin_8)
(Q2_y_Bin_11)-(z_pT_Bin_9), (Q2_y_Bin_12)-(z_pT_Bin_11), (Q2_y_Bin_12)-(z_pT_Bin_12)
(Q2_y_Bin_12)-(z_pT_Bin_13), (Q2_y_Bin_12)-(z_pT_Bin_16), (Q2_y_Bin_12)-(z_pT_Bin_18)
(Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_13)-(z_pT_Bin_1)
(Q2_y_Bin_13)-(z_pT_Bin_12), (Q2_y_Bin_13)-(z_pT_Bin_2), (Q2_y_Bin_13)-(z_pT_Bin_26)
(Q2_y_Bin_13)-(z_pT_Bin_3), (Q2_y_Bin_13)-(z_pT_Bin_4), (Q2_y_Bin_13)-(z_pT_Bin_5)
(Q2_y_Bin_13)-(z_pT_Bin_7), (Q2_y_Bin_13)-(z_pT_Bin_8), (Q2_y_Bin_13)-(z_pT_Bin_9)
(Q2_y_Bin_14)-(z_pT_Bin_1), (Q2_y_Bin_14)-(z_pT_Bin_2), (Q2_y_Bin_14)-(z_pT_Bin_3)
(Q2_y_Bin_14)-(z_pT_Bin_32), (Q2_y_Bin_14)-(z_pT_Bin_4), (Q2_y_Bin_14)-(z_pT_Bin_5)
(Q2_y_Bin_15)-(z_pT_Bin_1), (Q2_y_Bin_15)-(z_pT_Bin_14), (Q2_y_Bin_15)-(z_pT_Bin_2)
(Q2_y_Bin_15)-(z_pT_Bin_21), (Q2_y_Bin_15)-(z_pT_Bin_22), (Q2_y_Bin_15)-(z_pT_Bin_23)
(Q2_y_Bin_15)-(z_pT_Bin_6), (Q2_y_Bin_15)-(z_pT_Bin_9), (Q2_y_Bin_16)-(z_pT_Bin_1)
(Q2_y_Bin_16)-(z_pT_Bin_3), (Q2_y_Bin_16)-(z_pT_Bin_4), (Q2_y_Bin_16)-(z_pT_Bin_5)
(Q2_y_Bin_16)-(z_pT_Bin_6), (Q2_y_Bin_16)-(z_pT_Bin_9), (Q2_y_Bin_17)-(z_pT_Bin_1)
(Q2_y_Bin_17)-(z_pT_Bin_2), (Q2_y_Bin_17)-(z_pT_Bin_3), (Q2_y_Bin_17)-(z_pT_Bin_4)
(Q2_y_Bin_2)-(z_pT_Bin_1), (Q2_y_Bin_2)-(z_pT_Bin_10), (Q2_y_Bin_2)-(z_pT_Bin_11)
(Q2_y_Bin_2)-(z_pT_Bin_12), (Q2_y_Bin_2)-(z_pT_Bin_13), (Q2_y_Bin_2)-(z_pT_Bin_14)
(Q2_y_Bin_2)-(z_pT_Bin_15), (Q2_y_Bin_2)-(z_pT_Bin_16), (Q2_y_Bin_2)-(z_pT_Bin_17)
(Q2_y_Bin_2)-(z_pT_Bin_18), (Q2_y_Bin_2)-(z_pT_Bin_19), (Q2_y_Bin_2)-(z_pT_Bin_2)
(Q2_y_Bin_2)-(z_pT_Bin_20), (Q2_y_Bin_2)-(z_pT_Bin_21), (Q2_y_Bin_2)-(z_pT_Bin_23)
(Q2_y_Bin_2)-(z_pT_Bin_25), (Q2_y_Bin_2)-(z_pT_Bin_26), (Q2_y_Bin_2)-(z_pT_Bin_27)
(Q2_y_Bin_2)-(z_pT_Bin_28), (Q2_y_Bin_2)-(z_pT_Bin_3), (Q2_y_Bin_2)-(z_pT_Bin_32)
(Q2_y_Bin_2)-(z_pT_Bin_33), (Q2_y_Bin_2)-(z_pT_Bin_34), (Q2_y_Bin_2)-(z_pT_Bin_4)
(Q2_y_Bin_2)-(z_pT_Bin_5), (Q2_y_Bin_2)-(z_pT_Bin_6), (Q2_y_Bin_2)-(z_pT_Bin_7)
(Q2_y_Bin_2)-(z_pT_Bin_8), (Q2_y_Bin_2)-(z_pT_Bin_9), (Q2_y_Bin_3)-(z_pT_Bin_1)
(Q2_y_Bin_3)-(z_pT_Bin_10), (Q2_y_Bin_3)-(z_pT_Bin_11), (Q2_y_Bin_3)-(z_pT_Bin_12)
(Q2_y_Bin_3)-(z_pT_Bin_13), (Q2_y_Bin_3)-(z_pT_Bin_14), (Q2_y_Bin_3)-(z_pT_Bin_16)
(Q2_y_Bin_3)-(z_pT_Bin_17), (Q2_y_Bin_3)-(z_pT_Bin_18), (Q2_y_Bin_3)-(z_pT_Bin_19)
(Q2_y_Bin_3)-(z_pT_Bin_2), (Q2_y_Bin_3)-(z_pT_Bin_20), (Q2_y_Bin_3)-(z_pT_Bin_21)
(Q2_y_Bin_3)-(z_pT_Bin_22), (Q2_y_Bin_3)-(z_pT_Bin_23), (Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_7), (Q2_y_Bin_3)-(z_pT_Bin_8), (Q2_y_Bin_3)-(z_pT_Bin_9)
(Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_13), (Q2_y_Bin_4)-(z_pT_Bin_14)
(Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_19)
(Q2_y_Bin_4)-(z_pT_Bin_20), (Q2_y_Bin_4)-(z_pT_Bin_21), (Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_25), (Q2_y_Bin_4)-(z_pT_Bin_26), (Q2_y_Bin_4)-(z_pT_Bin_27)
(Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission], (Q2_y_Bin_5)-(z_pT_Bin_1)
(Q2_y_Bin_5)-(z_pT_Bin_10), (Q2_y_Bin_5)-(z_pT_Bin_11), (Q2_y_Bin_5)-(z_pT_Bin_13)
(Q2_y_Bin_5)-(z_pT_Bin_14), (Q2_y_Bin_5)-(z_pT_Bin_15), (Q2_y_Bin_5)-(z_pT_Bin_19)
(Q2_y_Bin_5)-(z_pT_Bin_2), (Q2_y_Bin_5)-(z_pT_Bin_20), (Q2_y_Bin_5)-(z_pT_Bin_21)
(Q2_y_Bin_5)-(z_pT_Bin_25), (Q2_y_Bin_5)-(z_pT_Bin_26), (Q2_y_Bin_5)-(z_pT_Bin_3)
(Q2_y_Bin_5)-(z_pT_Bin_31), (Q2_y_Bin_5)-(z_pT_Bin_32), (Q2_y_Bin_5)-(z_pT_Bin_4)
(Q2_y_Bin_5)-(z_pT_Bin_5), (Q2_y_Bin_5)-(z_pT_Bin_6), (Q2_y_Bin_5)-(z_pT_Bin_7)
(Q2_y_Bin_5)-(z_pT_Bin_8), (Q2_y_Bin_5)-(z_pT_Bin_9), (Q2_y_Bin_6)-(z_pT_Bin_1)
(Q2_y_Bin_6)-(z_pT_Bin_10), (Q2_y_Bin_6)-(z_pT_Bin_11), (Q2_y_Bin_6)-(z_pT_Bin_13)
(Q2_y_Bin_6)-(z_pT_Bin_14), (Q2_y_Bin_6)-(z_pT_Bin_15), (Q2_y_Bin_6)-(z_pT_Bin_16)
(Q2_y_Bin_6)-(z_pT_Bin_19), (Q2_y_Bin_6)-(z_pT_Bin_2), (Q2_y_Bin_6)-(z_pT_Bin_20)
(Q2_y_Bin_6)-(z_pT_Bin_21), (Q2_y_Bin_6)-(z_pT_Bin_27), (Q2_y_Bin_6)-(z_pT_Bin_28)
(Q2_y_Bin_6)-(z_pT_Bin_3), (Q2_y_Bin_6)-(z_pT_Bin_4), (Q2_y_Bin_6)-(z_pT_Bin_5)
(Q2_y_Bin_6)-(z_pT_Bin_6), (Q2_y_Bin_6)-(z_pT_Bin_7), (Q2_y_Bin_6)-(z_pT_Bin_8)
(Q2_y_Bin_6)-(z_pT_Bin_9), (Q2_y_Bin_7)-(z_pT_Bin_1), (Q2_y_Bin_7)-(z_pT_Bin_10)
(Q2_y_Bin_7)-(z_pT_Bin_11), (Q2_y_Bin_7)-(z_pT_Bin_12), (Q2_y_Bin_7)-(z_pT_Bin_13)
(Q2_y_Bin_7)-(z_pT_Bin_14), (Q2_y_Bin_7)-(z_pT_Bin_15), (Q2_y_Bin_7)-(z_pT_Bin_16)
(Q2_y_Bin_7)-(z_pT_Bin_17), (Q2_y_Bin_7)-(z_pT_Bin_18), (Q2_y_Bin_7)-(z_pT_Bin_19)
(Q2_y_Bin_7)-(z_pT_Bin_2), (Q2_y_Bin_7)-(z_pT_Bin_20), (Q2_y_Bin_7)-(z_pT_Bin_21)
(Q2_y_Bin_7)-(z_pT_Bin_22), (Q2_y_Bin_7)-(z_pT_Bin_23), (Q2_y_Bin_7)-(z_pT_Bin_24)
(Q2_y_Bin_7)-(z_pT_Bin_25), (Q2_y_Bin_7)-(z_pT_Bin_26), (Q2_y_Bin_7)-(z_pT_Bin_27)
(Q2_y_Bin_7)-(z_pT_Bin_28), (Q2_y_Bin_7)-(z_pT_Bin_29), (Q2_y_Bin_7)-(z_pT_Bin_34)
(Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_7)-(z_pT_Bin_7), (Q2_y_Bin_7)-(z_pT_Bin_8)
(Q2_y_Bin_7)-(z_pT_Bin_9), (Q2_y_Bin_8)-(z_pT_Bin_11), (Q2_y_Bin_8)-(z_pT_Bin_12)
(Q2_y_Bin_8)-(z_pT_Bin_13), (Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16)
(Q2_y_Bin_8)-(z_pT_Bin_17), (Q2_y_Bin_8)-(z_pT_Bin_18), (Q2_y_Bin_8)-(z_pT_Bin_19)
(Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_21), (Q2_y_Bin_8)-(z_pT_Bin_23)
(Q2_y_Bin_8)-(z_pT_Bin_24), (Q2_y_Bin_8)-(z_pT_Bin_26), (Q2_y_Bin_8)-(z_pT_Bin_28)
(Q2_y_Bin_8)-(z_pT_Bin_29), (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_9)-(z_pT_Bin_1)
(Q2_y_Bin_9)-(z_pT_Bin_10), (Q2_y_Bin_9)-(z_pT_Bin_11), (Q2_y_Bin_9)-(z_pT_Bin_15)
(Q2_y_Bin_9)-(z_pT_Bin_16), (Q2_y_Bin_9)-(z_pT_Bin_22), (Q2_y_Bin_9)-(z_pT_Bin_3)
(Q2_y_Bin_9)-(z_pT_Bin_30), (Q2_y_Bin_9)-(z_pT_Bin_4), (Q2_y_Bin_9)-(z_pT_Bin_5)
(Q2_y_Bin_9)-(z_pT_Bin_6), (Q2_y_Bin_9)-(z_pT_Bin_7), (Q2_y_Bin_9)-(z_pT_Bin_8)
(Q2_y_Bin_9)-(z_pT_Bin_9)

#### 120°

The rule fails every assessable manual exclusion (40).

Manually excluded but passes:

None.

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_16), (Q2_y_Bin_1)-(z_pT_Bin_23)
(Q2_y_Bin_1)-(z_pT_Bin_30), (Q2_y_Bin_1)-(z_pT_Bin_31), (Q2_y_Bin_1)-(z_pT_Bin_32)
(Q2_y_Bin_1)-(z_pT_Bin_5), (Q2_y_Bin_1)-(z_pT_Bin_6), (Q2_y_Bin_1)-(z_pT_Bin_7)
(Q2_y_Bin_1)-(z_pT_Bin_9), (Q2_y_Bin_10)-(z_pT_Bin_1), (Q2_y_Bin_10)-(z_pT_Bin_10)
(Q2_y_Bin_10)-(z_pT_Bin_15), (Q2_y_Bin_10)-(z_pT_Bin_2), (Q2_y_Bin_10)-(z_pT_Bin_26)
(Q2_y_Bin_10)-(z_pT_Bin_3), (Q2_y_Bin_10)-(z_pT_Bin_31), (Q2_y_Bin_10)-(z_pT_Bin_4)
(Q2_y_Bin_10)-(z_pT_Bin_5), (Q2_y_Bin_10)-(z_pT_Bin_6), (Q2_y_Bin_10)-(z_pT_Bin_7)
(Q2_y_Bin_11)-(z_pT_Bin_1), (Q2_y_Bin_11)-(z_pT_Bin_10), (Q2_y_Bin_11)-(z_pT_Bin_15)
(Q2_y_Bin_11)-(z_pT_Bin_18), (Q2_y_Bin_11)-(z_pT_Bin_19), (Q2_y_Bin_11)-(z_pT_Bin_2)
(Q2_y_Bin_11)-(z_pT_Bin_21), (Q2_y_Bin_11)-(z_pT_Bin_23), (Q2_y_Bin_11)-(z_pT_Bin_3)
(Q2_y_Bin_11)-(z_pT_Bin_6), (Q2_y_Bin_11)-(z_pT_Bin_9), (Q2_y_Bin_12)-(z_pT_Bin_11)
(Q2_y_Bin_12)-(z_pT_Bin_13), (Q2_y_Bin_12)-(z_pT_Bin_16), (Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission]
(Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_13)-(z_pT_Bin_1), (Q2_y_Bin_13)-(z_pT_Bin_2)
(Q2_y_Bin_13)-(z_pT_Bin_3), (Q2_y_Bin_13)-(z_pT_Bin_4), (Q2_y_Bin_14)-(z_pT_Bin_2)
(Q2_y_Bin_14)-(z_pT_Bin_3), (Q2_y_Bin_14)-(z_pT_Bin_32), (Q2_y_Bin_14)-(z_pT_Bin_4)
(Q2_y_Bin_14)-(z_pT_Bin_5), (Q2_y_Bin_15)-(z_pT_Bin_1), (Q2_y_Bin_15)-(z_pT_Bin_2)
(Q2_y_Bin_15)-(z_pT_Bin_22), (Q2_y_Bin_15)-(z_pT_Bin_23), (Q2_y_Bin_15)-(z_pT_Bin_9)
(Q2_y_Bin_16)-(z_pT_Bin_5), (Q2_y_Bin_16)-(z_pT_Bin_6), (Q2_y_Bin_17)-(z_pT_Bin_1)
(Q2_y_Bin_17)-(z_pT_Bin_2), (Q2_y_Bin_17)-(z_pT_Bin_4), (Q2_y_Bin_2)-(z_pT_Bin_1)
(Q2_y_Bin_2)-(z_pT_Bin_10), (Q2_y_Bin_2)-(z_pT_Bin_11), (Q2_y_Bin_2)-(z_pT_Bin_13)
(Q2_y_Bin_2)-(z_pT_Bin_14), (Q2_y_Bin_2)-(z_pT_Bin_15), (Q2_y_Bin_2)-(z_pT_Bin_16)
(Q2_y_Bin_2)-(z_pT_Bin_19), (Q2_y_Bin_2)-(z_pT_Bin_2), (Q2_y_Bin_2)-(z_pT_Bin_20)
(Q2_y_Bin_2)-(z_pT_Bin_21), (Q2_y_Bin_2)-(z_pT_Bin_25), (Q2_y_Bin_2)-(z_pT_Bin_26)
(Q2_y_Bin_2)-(z_pT_Bin_27), (Q2_y_Bin_2)-(z_pT_Bin_3), (Q2_y_Bin_2)-(z_pT_Bin_32)
(Q2_y_Bin_2)-(z_pT_Bin_33), (Q2_y_Bin_2)-(z_pT_Bin_34), (Q2_y_Bin_2)-(z_pT_Bin_4)
(Q2_y_Bin_2)-(z_pT_Bin_5), (Q2_y_Bin_2)-(z_pT_Bin_6), (Q2_y_Bin_2)-(z_pT_Bin_7)
(Q2_y_Bin_2)-(z_pT_Bin_8), (Q2_y_Bin_2)-(z_pT_Bin_9), (Q2_y_Bin_3)-(z_pT_Bin_1)
(Q2_y_Bin_3)-(z_pT_Bin_10), (Q2_y_Bin_3)-(z_pT_Bin_11), (Q2_y_Bin_3)-(z_pT_Bin_12)
(Q2_y_Bin_3)-(z_pT_Bin_13), (Q2_y_Bin_3)-(z_pT_Bin_14), (Q2_y_Bin_3)-(z_pT_Bin_16)
(Q2_y_Bin_3)-(z_pT_Bin_17), (Q2_y_Bin_3)-(z_pT_Bin_18), (Q2_y_Bin_3)-(z_pT_Bin_19)
(Q2_y_Bin_3)-(z_pT_Bin_2), (Q2_y_Bin_3)-(z_pT_Bin_20), (Q2_y_Bin_3)-(z_pT_Bin_21)
(Q2_y_Bin_3)-(z_pT_Bin_22), (Q2_y_Bin_3)-(z_pT_Bin_23), (Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_7), (Q2_y_Bin_3)-(z_pT_Bin_8), (Q2_y_Bin_3)-(z_pT_Bin_9)
(Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_13), (Q2_y_Bin_4)-(z_pT_Bin_14)
(Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_19)
(Q2_y_Bin_4)-(z_pT_Bin_20), (Q2_y_Bin_4)-(z_pT_Bin_21), (Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_25), (Q2_y_Bin_4)-(z_pT_Bin_26), (Q2_y_Bin_4)-(z_pT_Bin_27)
(Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission], (Q2_y_Bin_5)-(z_pT_Bin_1)
(Q2_y_Bin_5)-(z_pT_Bin_10), (Q2_y_Bin_5)-(z_pT_Bin_13), (Q2_y_Bin_5)-(z_pT_Bin_14)
(Q2_y_Bin_5)-(z_pT_Bin_15), (Q2_y_Bin_5)-(z_pT_Bin_19), (Q2_y_Bin_5)-(z_pT_Bin_2)
(Q2_y_Bin_5)-(z_pT_Bin_20), (Q2_y_Bin_5)-(z_pT_Bin_25), (Q2_y_Bin_5)-(z_pT_Bin_3)
(Q2_y_Bin_5)-(z_pT_Bin_31), (Q2_y_Bin_5)-(z_pT_Bin_32), (Q2_y_Bin_5)-(z_pT_Bin_4)
(Q2_y_Bin_5)-(z_pT_Bin_5), (Q2_y_Bin_5)-(z_pT_Bin_6), (Q2_y_Bin_5)-(z_pT_Bin_7)
(Q2_y_Bin_5)-(z_pT_Bin_8), (Q2_y_Bin_5)-(z_pT_Bin_9), (Q2_y_Bin_6)-(z_pT_Bin_1)
(Q2_y_Bin_6)-(z_pT_Bin_10), (Q2_y_Bin_6)-(z_pT_Bin_14), (Q2_y_Bin_6)-(z_pT_Bin_15)
(Q2_y_Bin_6)-(z_pT_Bin_19), (Q2_y_Bin_6)-(z_pT_Bin_2), (Q2_y_Bin_6)-(z_pT_Bin_20)
(Q2_y_Bin_6)-(z_pT_Bin_27), (Q2_y_Bin_6)-(z_pT_Bin_28), (Q2_y_Bin_6)-(z_pT_Bin_3)
(Q2_y_Bin_6)-(z_pT_Bin_4), (Q2_y_Bin_6)-(z_pT_Bin_5), (Q2_y_Bin_6)-(z_pT_Bin_6)
(Q2_y_Bin_6)-(z_pT_Bin_7), (Q2_y_Bin_6)-(z_pT_Bin_8), (Q2_y_Bin_6)-(z_pT_Bin_9)
(Q2_y_Bin_7)-(z_pT_Bin_1), (Q2_y_Bin_7)-(z_pT_Bin_10), (Q2_y_Bin_7)-(z_pT_Bin_11)
(Q2_y_Bin_7)-(z_pT_Bin_12), (Q2_y_Bin_7)-(z_pT_Bin_13), (Q2_y_Bin_7)-(z_pT_Bin_15)
(Q2_y_Bin_7)-(z_pT_Bin_16), (Q2_y_Bin_7)-(z_pT_Bin_17), (Q2_y_Bin_7)-(z_pT_Bin_18)
(Q2_y_Bin_7)-(z_pT_Bin_2), (Q2_y_Bin_7)-(z_pT_Bin_21), (Q2_y_Bin_7)-(z_pT_Bin_22)
(Q2_y_Bin_7)-(z_pT_Bin_23), (Q2_y_Bin_7)-(z_pT_Bin_24), (Q2_y_Bin_7)-(z_pT_Bin_26)
(Q2_y_Bin_7)-(z_pT_Bin_27), (Q2_y_Bin_7)-(z_pT_Bin_28), (Q2_y_Bin_7)-(z_pT_Bin_29)
(Q2_y_Bin_7)-(z_pT_Bin_34), (Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_7)-(z_pT_Bin_7)
(Q2_y_Bin_7)-(z_pT_Bin_9), (Q2_y_Bin_8)-(z_pT_Bin_11), (Q2_y_Bin_8)-(z_pT_Bin_12)
(Q2_y_Bin_8)-(z_pT_Bin_13), (Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16)
(Q2_y_Bin_8)-(z_pT_Bin_18), (Q2_y_Bin_8)-(z_pT_Bin_19), (Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_21), (Q2_y_Bin_8)-(z_pT_Bin_23), (Q2_y_Bin_8)-(z_pT_Bin_24)
(Q2_y_Bin_8)-(z_pT_Bin_26), (Q2_y_Bin_8)-(z_pT_Bin_28), (Q2_y_Bin_8)-(z_pT_Bin_29)
(Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_9)-(z_pT_Bin_1), (Q2_y_Bin_9)-(z_pT_Bin_10)
(Q2_y_Bin_9)-(z_pT_Bin_16), (Q2_y_Bin_9)-(z_pT_Bin_3), (Q2_y_Bin_9)-(z_pT_Bin_4)
(Q2_y_Bin_9)-(z_pT_Bin_5), (Q2_y_Bin_9)-(z_pT_Bin_6), (Q2_y_Bin_9)-(z_pT_Bin_8)

#### 135°

The rule fails every assessable manual exclusion (40).

Manually excluded but passes:

None.

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_16), (Q2_y_Bin_1)-(z_pT_Bin_23)
(Q2_y_Bin_1)-(z_pT_Bin_30), (Q2_y_Bin_1)-(z_pT_Bin_31), (Q2_y_Bin_1)-(z_pT_Bin_32)
(Q2_y_Bin_1)-(z_pT_Bin_5), (Q2_y_Bin_1)-(z_pT_Bin_6), (Q2_y_Bin_1)-(z_pT_Bin_7)
(Q2_y_Bin_1)-(z_pT_Bin_9), (Q2_y_Bin_10)-(z_pT_Bin_1), (Q2_y_Bin_10)-(z_pT_Bin_2)
(Q2_y_Bin_10)-(z_pT_Bin_3), (Q2_y_Bin_10)-(z_pT_Bin_31), (Q2_y_Bin_10)-(z_pT_Bin_4)
(Q2_y_Bin_10)-(z_pT_Bin_5), (Q2_y_Bin_10)-(z_pT_Bin_6), (Q2_y_Bin_10)-(z_pT_Bin_7)
(Q2_y_Bin_11)-(z_pT_Bin_1), (Q2_y_Bin_11)-(z_pT_Bin_10), (Q2_y_Bin_11)-(z_pT_Bin_2)
(Q2_y_Bin_11)-(z_pT_Bin_21), (Q2_y_Bin_11)-(z_pT_Bin_23), (Q2_y_Bin_11)-(z_pT_Bin_3)
(Q2_y_Bin_11)-(z_pT_Bin_6), (Q2_y_Bin_12)-(z_pT_Bin_11), (Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission]
(Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_13)-(z_pT_Bin_1), (Q2_y_Bin_13)-(z_pT_Bin_2)
(Q2_y_Bin_13)-(z_pT_Bin_3), (Q2_y_Bin_14)-(z_pT_Bin_2), (Q2_y_Bin_14)-(z_pT_Bin_32)
(Q2_y_Bin_14)-(z_pT_Bin_4), (Q2_y_Bin_14)-(z_pT_Bin_5), (Q2_y_Bin_15)-(z_pT_Bin_1)
(Q2_y_Bin_15)-(z_pT_Bin_2), (Q2_y_Bin_15)-(z_pT_Bin_22), (Q2_y_Bin_15)-(z_pT_Bin_23)
(Q2_y_Bin_15)-(z_pT_Bin_9), (Q2_y_Bin_16)-(z_pT_Bin_6), (Q2_y_Bin_17)-(z_pT_Bin_2)
(Q2_y_Bin_17)-(z_pT_Bin_4), (Q2_y_Bin_2)-(z_pT_Bin_1), (Q2_y_Bin_2)-(z_pT_Bin_10)
(Q2_y_Bin_2)-(z_pT_Bin_11), (Q2_y_Bin_2)-(z_pT_Bin_13), (Q2_y_Bin_2)-(z_pT_Bin_14)
(Q2_y_Bin_2)-(z_pT_Bin_15), (Q2_y_Bin_2)-(z_pT_Bin_16), (Q2_y_Bin_2)-(z_pT_Bin_19)
(Q2_y_Bin_2)-(z_pT_Bin_2), (Q2_y_Bin_2)-(z_pT_Bin_20), (Q2_y_Bin_2)-(z_pT_Bin_21)
(Q2_y_Bin_2)-(z_pT_Bin_25), (Q2_y_Bin_2)-(z_pT_Bin_26), (Q2_y_Bin_2)-(z_pT_Bin_3)
(Q2_y_Bin_2)-(z_pT_Bin_32), (Q2_y_Bin_2)-(z_pT_Bin_33), (Q2_y_Bin_2)-(z_pT_Bin_34)
(Q2_y_Bin_2)-(z_pT_Bin_4), (Q2_y_Bin_2)-(z_pT_Bin_5), (Q2_y_Bin_2)-(z_pT_Bin_6)
(Q2_y_Bin_2)-(z_pT_Bin_7), (Q2_y_Bin_2)-(z_pT_Bin_8), (Q2_y_Bin_2)-(z_pT_Bin_9)
(Q2_y_Bin_3)-(z_pT_Bin_1), (Q2_y_Bin_3)-(z_pT_Bin_10), (Q2_y_Bin_3)-(z_pT_Bin_11)
(Q2_y_Bin_3)-(z_pT_Bin_12), (Q2_y_Bin_3)-(z_pT_Bin_13), (Q2_y_Bin_3)-(z_pT_Bin_14)
(Q2_y_Bin_3)-(z_pT_Bin_16), (Q2_y_Bin_3)-(z_pT_Bin_17), (Q2_y_Bin_3)-(z_pT_Bin_18)
(Q2_y_Bin_3)-(z_pT_Bin_19), (Q2_y_Bin_3)-(z_pT_Bin_2), (Q2_y_Bin_3)-(z_pT_Bin_20)
(Q2_y_Bin_3)-(z_pT_Bin_21), (Q2_y_Bin_3)-(z_pT_Bin_22), (Q2_y_Bin_3)-(z_pT_Bin_23)
(Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_7), (Q2_y_Bin_3)-(z_pT_Bin_8)
(Q2_y_Bin_3)-(z_pT_Bin_9), (Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_13)
(Q2_y_Bin_4)-(z_pT_Bin_14), (Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_19), (Q2_y_Bin_4)-(z_pT_Bin_20), (Q2_y_Bin_4)-(z_pT_Bin_21)
(Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_25), (Q2_y_Bin_4)-(z_pT_Bin_26)
(Q2_y_Bin_4)-(z_pT_Bin_27), (Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission]
(Q2_y_Bin_5)-(z_pT_Bin_1), (Q2_y_Bin_5)-(z_pT_Bin_10), (Q2_y_Bin_5)-(z_pT_Bin_13)
(Q2_y_Bin_5)-(z_pT_Bin_14), (Q2_y_Bin_5)-(z_pT_Bin_15), (Q2_y_Bin_5)-(z_pT_Bin_19)
(Q2_y_Bin_5)-(z_pT_Bin_2), (Q2_y_Bin_5)-(z_pT_Bin_20), (Q2_y_Bin_5)-(z_pT_Bin_25)
(Q2_y_Bin_5)-(z_pT_Bin_3), (Q2_y_Bin_5)-(z_pT_Bin_31), (Q2_y_Bin_5)-(z_pT_Bin_32)
(Q2_y_Bin_5)-(z_pT_Bin_4), (Q2_y_Bin_5)-(z_pT_Bin_5), (Q2_y_Bin_5)-(z_pT_Bin_6)
(Q2_y_Bin_5)-(z_pT_Bin_7), (Q2_y_Bin_5)-(z_pT_Bin_8), (Q2_y_Bin_5)-(z_pT_Bin_9)
(Q2_y_Bin_6)-(z_pT_Bin_1), (Q2_y_Bin_6)-(z_pT_Bin_10), (Q2_y_Bin_6)-(z_pT_Bin_14)
(Q2_y_Bin_6)-(z_pT_Bin_15), (Q2_y_Bin_6)-(z_pT_Bin_2), (Q2_y_Bin_6)-(z_pT_Bin_20)
(Q2_y_Bin_6)-(z_pT_Bin_27), (Q2_y_Bin_6)-(z_pT_Bin_28), (Q2_y_Bin_6)-(z_pT_Bin_3)
(Q2_y_Bin_6)-(z_pT_Bin_4), (Q2_y_Bin_6)-(z_pT_Bin_5), (Q2_y_Bin_6)-(z_pT_Bin_6)
(Q2_y_Bin_6)-(z_pT_Bin_7), (Q2_y_Bin_6)-(z_pT_Bin_8), (Q2_y_Bin_6)-(z_pT_Bin_9)
(Q2_y_Bin_7)-(z_pT_Bin_1), (Q2_y_Bin_7)-(z_pT_Bin_10), (Q2_y_Bin_7)-(z_pT_Bin_11)
(Q2_y_Bin_7)-(z_pT_Bin_12), (Q2_y_Bin_7)-(z_pT_Bin_13), (Q2_y_Bin_7)-(z_pT_Bin_15)
(Q2_y_Bin_7)-(z_pT_Bin_16), (Q2_y_Bin_7)-(z_pT_Bin_17), (Q2_y_Bin_7)-(z_pT_Bin_18)
(Q2_y_Bin_7)-(z_pT_Bin_2), (Q2_y_Bin_7)-(z_pT_Bin_21), (Q2_y_Bin_7)-(z_pT_Bin_22)
(Q2_y_Bin_7)-(z_pT_Bin_24), (Q2_y_Bin_7)-(z_pT_Bin_26), (Q2_y_Bin_7)-(z_pT_Bin_27)
(Q2_y_Bin_7)-(z_pT_Bin_28), (Q2_y_Bin_7)-(z_pT_Bin_34), (Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission]
(Q2_y_Bin_7)-(z_pT_Bin_7), (Q2_y_Bin_7)-(z_pT_Bin_9), (Q2_y_Bin_8)-(z_pT_Bin_11)
(Q2_y_Bin_8)-(z_pT_Bin_12), (Q2_y_Bin_8)-(z_pT_Bin_13), (Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_16), (Q2_y_Bin_8)-(z_pT_Bin_18), (Q2_y_Bin_8)-(z_pT_Bin_19)
(Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_21), (Q2_y_Bin_8)-(z_pT_Bin_23)
(Q2_y_Bin_8)-(z_pT_Bin_24), (Q2_y_Bin_8)-(z_pT_Bin_26), (Q2_y_Bin_8)-(z_pT_Bin_28)
(Q2_y_Bin_8)-(z_pT_Bin_29), (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_9)-(z_pT_Bin_1)
(Q2_y_Bin_9)-(z_pT_Bin_3), (Q2_y_Bin_9)-(z_pT_Bin_4), (Q2_y_Bin_9)-(z_pT_Bin_5)

#### 150°

The rule fails every assessable manual exclusion (40).

Manually excluded but passes:

None.

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_16), (Q2_y_Bin_1)-(z_pT_Bin_23)
(Q2_y_Bin_1)-(z_pT_Bin_30), (Q2_y_Bin_1)-(z_pT_Bin_32), (Q2_y_Bin_1)-(z_pT_Bin_5)
(Q2_y_Bin_1)-(z_pT_Bin_6), (Q2_y_Bin_1)-(z_pT_Bin_9), (Q2_y_Bin_10)-(z_pT_Bin_2)
(Q2_y_Bin_10)-(z_pT_Bin_3), (Q2_y_Bin_10)-(z_pT_Bin_4), (Q2_y_Bin_10)-(z_pT_Bin_5)
(Q2_y_Bin_10)-(z_pT_Bin_6), (Q2_y_Bin_11)-(z_pT_Bin_1), (Q2_y_Bin_11)-(z_pT_Bin_2)
(Q2_y_Bin_11)-(z_pT_Bin_21), (Q2_y_Bin_11)-(z_pT_Bin_23), (Q2_y_Bin_11)-(z_pT_Bin_3)
(Q2_y_Bin_11)-(z_pT_Bin_6), (Q2_y_Bin_12)-(z_pT_Bin_11), (Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission]
(Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_13)-(z_pT_Bin_1), (Q2_y_Bin_13)-(z_pT_Bin_2)
(Q2_y_Bin_14)-(z_pT_Bin_4), (Q2_y_Bin_14)-(z_pT_Bin_5), (Q2_y_Bin_15)-(z_pT_Bin_1)
(Q2_y_Bin_15)-(z_pT_Bin_2), (Q2_y_Bin_15)-(z_pT_Bin_22), (Q2_y_Bin_15)-(z_pT_Bin_23)
(Q2_y_Bin_16)-(z_pT_Bin_6), (Q2_y_Bin_17)-(z_pT_Bin_2), (Q2_y_Bin_17)-(z_pT_Bin_4)
(Q2_y_Bin_2)-(z_pT_Bin_1), (Q2_y_Bin_2)-(z_pT_Bin_10), (Q2_y_Bin_2)-(z_pT_Bin_13)
(Q2_y_Bin_2)-(z_pT_Bin_14), (Q2_y_Bin_2)-(z_pT_Bin_15), (Q2_y_Bin_2)-(z_pT_Bin_16)
(Q2_y_Bin_2)-(z_pT_Bin_19), (Q2_y_Bin_2)-(z_pT_Bin_2), (Q2_y_Bin_2)-(z_pT_Bin_20)
(Q2_y_Bin_2)-(z_pT_Bin_25), (Q2_y_Bin_2)-(z_pT_Bin_3), (Q2_y_Bin_2)-(z_pT_Bin_32)
(Q2_y_Bin_2)-(z_pT_Bin_33), (Q2_y_Bin_2)-(z_pT_Bin_34), (Q2_y_Bin_2)-(z_pT_Bin_4)
(Q2_y_Bin_2)-(z_pT_Bin_5), (Q2_y_Bin_2)-(z_pT_Bin_6), (Q2_y_Bin_2)-(z_pT_Bin_7)
(Q2_y_Bin_2)-(z_pT_Bin_8), (Q2_y_Bin_2)-(z_pT_Bin_9), (Q2_y_Bin_3)-(z_pT_Bin_1)
(Q2_y_Bin_3)-(z_pT_Bin_10), (Q2_y_Bin_3)-(z_pT_Bin_11), (Q2_y_Bin_3)-(z_pT_Bin_12)
(Q2_y_Bin_3)-(z_pT_Bin_13), (Q2_y_Bin_3)-(z_pT_Bin_16), (Q2_y_Bin_3)-(z_pT_Bin_17)
(Q2_y_Bin_3)-(z_pT_Bin_18), (Q2_y_Bin_3)-(z_pT_Bin_2), (Q2_y_Bin_3)-(z_pT_Bin_20)
(Q2_y_Bin_3)-(z_pT_Bin_21), (Q2_y_Bin_3)-(z_pT_Bin_22), (Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_7), (Q2_y_Bin_3)-(z_pT_Bin_8), (Q2_y_Bin_3)-(z_pT_Bin_9)
(Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_13), (Q2_y_Bin_4)-(z_pT_Bin_14)
(Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_19)
(Q2_y_Bin_4)-(z_pT_Bin_21), (Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_25)
(Q2_y_Bin_4)-(z_pT_Bin_26), (Q2_y_Bin_4)-(z_pT_Bin_27), (Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission], (Q2_y_Bin_5)-(z_pT_Bin_1), (Q2_y_Bin_5)-(z_pT_Bin_10)
(Q2_y_Bin_5)-(z_pT_Bin_13), (Q2_y_Bin_5)-(z_pT_Bin_14), (Q2_y_Bin_5)-(z_pT_Bin_19)
(Q2_y_Bin_5)-(z_pT_Bin_2), (Q2_y_Bin_5)-(z_pT_Bin_25), (Q2_y_Bin_5)-(z_pT_Bin_3)
(Q2_y_Bin_5)-(z_pT_Bin_31), (Q2_y_Bin_5)-(z_pT_Bin_32), (Q2_y_Bin_5)-(z_pT_Bin_4)
(Q2_y_Bin_5)-(z_pT_Bin_5), (Q2_y_Bin_5)-(z_pT_Bin_6), (Q2_y_Bin_5)-(z_pT_Bin_7)
(Q2_y_Bin_5)-(z_pT_Bin_8), (Q2_y_Bin_5)-(z_pT_Bin_9), (Q2_y_Bin_6)-(z_pT_Bin_1)
(Q2_y_Bin_6)-(z_pT_Bin_14), (Q2_y_Bin_6)-(z_pT_Bin_15), (Q2_y_Bin_6)-(z_pT_Bin_2)
(Q2_y_Bin_6)-(z_pT_Bin_20), (Q2_y_Bin_6)-(z_pT_Bin_27), (Q2_y_Bin_6)-(z_pT_Bin_28)
(Q2_y_Bin_6)-(z_pT_Bin_3), (Q2_y_Bin_6)-(z_pT_Bin_4), (Q2_y_Bin_6)-(z_pT_Bin_5)
(Q2_y_Bin_6)-(z_pT_Bin_6), (Q2_y_Bin_6)-(z_pT_Bin_7), (Q2_y_Bin_6)-(z_pT_Bin_9)
(Q2_y_Bin_7)-(z_pT_Bin_1), (Q2_y_Bin_7)-(z_pT_Bin_11), (Q2_y_Bin_7)-(z_pT_Bin_12)
(Q2_y_Bin_7)-(z_pT_Bin_13), (Q2_y_Bin_7)-(z_pT_Bin_2), (Q2_y_Bin_7)-(z_pT_Bin_21)
(Q2_y_Bin_7)-(z_pT_Bin_24), (Q2_y_Bin_7)-(z_pT_Bin_26), (Q2_y_Bin_7)-(z_pT_Bin_34)
(Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_7)-(z_pT_Bin_7), (Q2_y_Bin_8)-(z_pT_Bin_11)
(Q2_y_Bin_8)-(z_pT_Bin_13), (Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16)
(Q2_y_Bin_8)-(z_pT_Bin_19), (Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_21)
(Q2_y_Bin_8)-(z_pT_Bin_24), (Q2_y_Bin_8)-(z_pT_Bin_28), (Q2_y_Bin_8)-(z_pT_Bin_29)
(Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_9)-(z_pT_Bin_1), (Q2_y_Bin_9)-(z_pT_Bin_3)
(Q2_y_Bin_9)-(z_pT_Bin_4), (Q2_y_Bin_9)-(z_pT_Bin_5)

#### 180°

The rule does not fail every assessable manual exclusion: 4 of 40 pass.

Manually excluded but passes:

(Q2_y_Bin_1)-(z_pT_Bin_22), (Q2_y_Bin_11)-(z_pT_Bin_20), (Q2_y_Bin_9)-(z_pT_Bin_2)
(Q2_y_Bin_9)-(z_pT_Bin_29)

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_30), (Q2_y_Bin_1)-(z_pT_Bin_5)
(Q2_y_Bin_1)-(z_pT_Bin_9), (Q2_y_Bin_10)-(z_pT_Bin_6), (Q2_y_Bin_11)-(z_pT_Bin_23)
(Q2_y_Bin_11)-(z_pT_Bin_3), (Q2_y_Bin_12)-(z_pT_Bin_11), (Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission]
(Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_14)-(z_pT_Bin_5), (Q2_y_Bin_15)-(z_pT_Bin_2)
(Q2_y_Bin_15)-(z_pT_Bin_23), (Q2_y_Bin_2)-(z_pT_Bin_1), (Q2_y_Bin_2)-(z_pT_Bin_10)
(Q2_y_Bin_2)-(z_pT_Bin_19), (Q2_y_Bin_2)-(z_pT_Bin_2), (Q2_y_Bin_2)-(z_pT_Bin_20)
(Q2_y_Bin_2)-(z_pT_Bin_3), (Q2_y_Bin_2)-(z_pT_Bin_32), (Q2_y_Bin_2)-(z_pT_Bin_4)
(Q2_y_Bin_2)-(z_pT_Bin_5), (Q2_y_Bin_2)-(z_pT_Bin_6), (Q2_y_Bin_2)-(z_pT_Bin_7)
(Q2_y_Bin_2)-(z_pT_Bin_9), (Q2_y_Bin_3)-(z_pT_Bin_1), (Q2_y_Bin_3)-(z_pT_Bin_10)
(Q2_y_Bin_3)-(z_pT_Bin_12), (Q2_y_Bin_3)-(z_pT_Bin_13), (Q2_y_Bin_3)-(z_pT_Bin_2)
(Q2_y_Bin_3)-(z_pT_Bin_20), (Q2_y_Bin_3)-(z_pT_Bin_21), (Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_7), (Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_13)
(Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_19)
(Q2_y_Bin_4)-(z_pT_Bin_21), (Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_25)
(Q2_y_Bin_4)-(z_pT_Bin_27), (Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission]
(Q2_y_Bin_5)-(z_pT_Bin_1), (Q2_y_Bin_5)-(z_pT_Bin_2), (Q2_y_Bin_5)-(z_pT_Bin_3)
(Q2_y_Bin_5)-(z_pT_Bin_31), (Q2_y_Bin_5)-(z_pT_Bin_4), (Q2_y_Bin_5)-(z_pT_Bin_5)
(Q2_y_Bin_5)-(z_pT_Bin_7), (Q2_y_Bin_6)-(z_pT_Bin_2), (Q2_y_Bin_6)-(z_pT_Bin_28)
(Q2_y_Bin_7)-(z_pT_Bin_12), (Q2_y_Bin_7)-(z_pT_Bin_2), (Q2_y_Bin_7)-(z_pT_Bin_24)
(Q2_y_Bin_7)-(z_pT_Bin_34), (Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_11)
(Q2_y_Bin_8)-(z_pT_Bin_13), (Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16)
(Q2_y_Bin_8)-(z_pT_Bin_19), (Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_24)
(Q2_y_Bin_8)-(z_pT_Bin_29), (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_9)-(z_pT_Bin_1)

### pipS4o

Manual list entries: 48. Fit-quality omissions relative to the nominal acceptance bins: 42. Comparisons the budget still keeps: 371.

#### 90°

The rule fails every assessable manual exclusion (48).

Manually excluded but passes:

None.

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_11), (Q2_y_Bin_1)-(z_pT_Bin_16)
(Q2_y_Bin_1)-(z_pT_Bin_17), (Q2_y_Bin_1)-(z_pT_Bin_23), (Q2_y_Bin_1)-(z_pT_Bin_30)
(Q2_y_Bin_1)-(z_pT_Bin_31), (Q2_y_Bin_1)-(z_pT_Bin_32), (Q2_y_Bin_1)-(z_pT_Bin_4)
(Q2_y_Bin_1)-(z_pT_Bin_5), (Q2_y_Bin_1)-(z_pT_Bin_6), (Q2_y_Bin_1)-(z_pT_Bin_7)
(Q2_y_Bin_1)-(z_pT_Bin_8), (Q2_y_Bin_1)-(z_pT_Bin_9), (Q2_y_Bin_10)-(z_pT_Bin_1)
(Q2_y_Bin_10)-(z_pT_Bin_10), (Q2_y_Bin_10)-(z_pT_Bin_13), (Q2_y_Bin_10)-(z_pT_Bin_15)
(Q2_y_Bin_10)-(z_pT_Bin_2), (Q2_y_Bin_10)-(z_pT_Bin_20), (Q2_y_Bin_10)-(z_pT_Bin_26)
(Q2_y_Bin_10)-(z_pT_Bin_3), (Q2_y_Bin_10)-(z_pT_Bin_31), (Q2_y_Bin_10)-(z_pT_Bin_32)
(Q2_y_Bin_10)-(z_pT_Bin_4), (Q2_y_Bin_10)-(z_pT_Bin_5), (Q2_y_Bin_10)-(z_pT_Bin_6)
(Q2_y_Bin_10)-(z_pT_Bin_7), (Q2_y_Bin_10)-(z_pT_Bin_9), (Q2_y_Bin_11)-(z_pT_Bin_1)
(Q2_y_Bin_11)-(z_pT_Bin_10), (Q2_y_Bin_11)-(z_pT_Bin_11), (Q2_y_Bin_11)-(z_pT_Bin_13)
(Q2_y_Bin_11)-(z_pT_Bin_14), (Q2_y_Bin_11)-(z_pT_Bin_15), (Q2_y_Bin_11)-(z_pT_Bin_18)
(Q2_y_Bin_11)-(z_pT_Bin_19), (Q2_y_Bin_11)-(z_pT_Bin_2), (Q2_y_Bin_11)-(z_pT_Bin_23)
(Q2_y_Bin_11)-(z_pT_Bin_6), (Q2_y_Bin_11)-(z_pT_Bin_8), (Q2_y_Bin_11)-(z_pT_Bin_9)
(Q2_y_Bin_12)-(z_pT_Bin_11), (Q2_y_Bin_12)-(z_pT_Bin_12), (Q2_y_Bin_12)-(z_pT_Bin_13)
(Q2_y_Bin_12)-(z_pT_Bin_16), (Q2_y_Bin_12)-(z_pT_Bin_18), (Q2_y_Bin_12)-(z_pT_Bin_21) [fit-quality omission]
(Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_6), (Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_13)-(z_pT_Bin_1), (Q2_y_Bin_13)-(z_pT_Bin_12), (Q2_y_Bin_13)-(z_pT_Bin_2)
(Q2_y_Bin_13)-(z_pT_Bin_26), (Q2_y_Bin_13)-(z_pT_Bin_3), (Q2_y_Bin_13)-(z_pT_Bin_4)
(Q2_y_Bin_13)-(z_pT_Bin_5), (Q2_y_Bin_13)-(z_pT_Bin_7), (Q2_y_Bin_13)-(z_pT_Bin_8)
(Q2_y_Bin_14)-(z_pT_Bin_1), (Q2_y_Bin_14)-(z_pT_Bin_2), (Q2_y_Bin_14)-(z_pT_Bin_3)
(Q2_y_Bin_14)-(z_pT_Bin_32), (Q2_y_Bin_14)-(z_pT_Bin_4), (Q2_y_Bin_14)-(z_pT_Bin_5)
(Q2_y_Bin_15)-(z_pT_Bin_1), (Q2_y_Bin_15)-(z_pT_Bin_19), (Q2_y_Bin_15)-(z_pT_Bin_2)
(Q2_y_Bin_15)-(z_pT_Bin_23), (Q2_y_Bin_15)-(z_pT_Bin_9), (Q2_y_Bin_16)-(z_pT_Bin_1)
(Q2_y_Bin_16)-(z_pT_Bin_3), (Q2_y_Bin_16)-(z_pT_Bin_4), (Q2_y_Bin_16)-(z_pT_Bin_5)
(Q2_y_Bin_16)-(z_pT_Bin_6), (Q2_y_Bin_17)-(z_pT_Bin_4), (Q2_y_Bin_2)-(z_pT_Bin_1)
(Q2_y_Bin_2)-(z_pT_Bin_10), (Q2_y_Bin_2)-(z_pT_Bin_11), (Q2_y_Bin_2)-(z_pT_Bin_12)
(Q2_y_Bin_2)-(z_pT_Bin_13), (Q2_y_Bin_2)-(z_pT_Bin_14), (Q2_y_Bin_2)-(z_pT_Bin_15)
(Q2_y_Bin_2)-(z_pT_Bin_16), (Q2_y_Bin_2)-(z_pT_Bin_18), (Q2_y_Bin_2)-(z_pT_Bin_19)
(Q2_y_Bin_2)-(z_pT_Bin_2), (Q2_y_Bin_2)-(z_pT_Bin_20), (Q2_y_Bin_2)-(z_pT_Bin_21)
(Q2_y_Bin_2)-(z_pT_Bin_25), (Q2_y_Bin_2)-(z_pT_Bin_26), (Q2_y_Bin_2)-(z_pT_Bin_27)
(Q2_y_Bin_2)-(z_pT_Bin_28), (Q2_y_Bin_2)-(z_pT_Bin_29), (Q2_y_Bin_2)-(z_pT_Bin_3)
(Q2_y_Bin_2)-(z_pT_Bin_32), (Q2_y_Bin_2)-(z_pT_Bin_33), (Q2_y_Bin_2)-(z_pT_Bin_34)
(Q2_y_Bin_2)-(z_pT_Bin_5), (Q2_y_Bin_2)-(z_pT_Bin_6), (Q2_y_Bin_2)-(z_pT_Bin_7)
(Q2_y_Bin_2)-(z_pT_Bin_8), (Q2_y_Bin_2)-(z_pT_Bin_9), (Q2_y_Bin_3)-(z_pT_Bin_1)
(Q2_y_Bin_3)-(z_pT_Bin_10), (Q2_y_Bin_3)-(z_pT_Bin_11), (Q2_y_Bin_3)-(z_pT_Bin_12)
(Q2_y_Bin_3)-(z_pT_Bin_13), (Q2_y_Bin_3)-(z_pT_Bin_14), (Q2_y_Bin_3)-(z_pT_Bin_15)
(Q2_y_Bin_3)-(z_pT_Bin_16), (Q2_y_Bin_3)-(z_pT_Bin_17), (Q2_y_Bin_3)-(z_pT_Bin_18)
(Q2_y_Bin_3)-(z_pT_Bin_19), (Q2_y_Bin_3)-(z_pT_Bin_2), (Q2_y_Bin_3)-(z_pT_Bin_20)
(Q2_y_Bin_3)-(z_pT_Bin_21), (Q2_y_Bin_3)-(z_pT_Bin_22), (Q2_y_Bin_3)-(z_pT_Bin_23)
(Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_7), (Q2_y_Bin_3)-(z_pT_Bin_8)
(Q2_y_Bin_3)-(z_pT_Bin_9), (Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_14)
(Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_19)
(Q2_y_Bin_4)-(z_pT_Bin_20), (Q2_y_Bin_4)-(z_pT_Bin_21), (Q2_y_Bin_4)-(z_pT_Bin_22) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_25), (Q2_y_Bin_4)-(z_pT_Bin_26)
(Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission], (Q2_y_Bin_5)-(z_pT_Bin_10)
(Q2_y_Bin_5)-(z_pT_Bin_11), (Q2_y_Bin_5)-(z_pT_Bin_13), (Q2_y_Bin_5)-(z_pT_Bin_14)
(Q2_y_Bin_5)-(z_pT_Bin_15), (Q2_y_Bin_5)-(z_pT_Bin_19), (Q2_y_Bin_5)-(z_pT_Bin_2)
(Q2_y_Bin_5)-(z_pT_Bin_20), (Q2_y_Bin_5)-(z_pT_Bin_25), (Q2_y_Bin_5)-(z_pT_Bin_3)
(Q2_y_Bin_5)-(z_pT_Bin_31), (Q2_y_Bin_5)-(z_pT_Bin_32), (Q2_y_Bin_5)-(z_pT_Bin_4)
(Q2_y_Bin_5)-(z_pT_Bin_5), (Q2_y_Bin_5)-(z_pT_Bin_6), (Q2_y_Bin_5)-(z_pT_Bin_7)
(Q2_y_Bin_5)-(z_pT_Bin_8), (Q2_y_Bin_5)-(z_pT_Bin_9), (Q2_y_Bin_6)-(z_pT_Bin_1)
(Q2_y_Bin_6)-(z_pT_Bin_10), (Q2_y_Bin_6)-(z_pT_Bin_11), (Q2_y_Bin_6)-(z_pT_Bin_13)
(Q2_y_Bin_6)-(z_pT_Bin_14), (Q2_y_Bin_6)-(z_pT_Bin_15), (Q2_y_Bin_6)-(z_pT_Bin_19)
(Q2_y_Bin_6)-(z_pT_Bin_2), (Q2_y_Bin_6)-(z_pT_Bin_20), (Q2_y_Bin_6)-(z_pT_Bin_27)
(Q2_y_Bin_6)-(z_pT_Bin_28), (Q2_y_Bin_6)-(z_pT_Bin_3), (Q2_y_Bin_6)-(z_pT_Bin_4)
(Q2_y_Bin_6)-(z_pT_Bin_5), (Q2_y_Bin_6)-(z_pT_Bin_6), (Q2_y_Bin_6)-(z_pT_Bin_7)
(Q2_y_Bin_6)-(z_pT_Bin_8), (Q2_y_Bin_7)-(z_pT_Bin_1), (Q2_y_Bin_7)-(z_pT_Bin_10)
(Q2_y_Bin_7)-(z_pT_Bin_11), (Q2_y_Bin_7)-(z_pT_Bin_12), (Q2_y_Bin_7)-(z_pT_Bin_13)
(Q2_y_Bin_7)-(z_pT_Bin_15), (Q2_y_Bin_7)-(z_pT_Bin_16), (Q2_y_Bin_7)-(z_pT_Bin_17)
(Q2_y_Bin_7)-(z_pT_Bin_18), (Q2_y_Bin_7)-(z_pT_Bin_19), (Q2_y_Bin_7)-(z_pT_Bin_2)
(Q2_y_Bin_7)-(z_pT_Bin_20), (Q2_y_Bin_7)-(z_pT_Bin_21), (Q2_y_Bin_7)-(z_pT_Bin_22)
(Q2_y_Bin_7)-(z_pT_Bin_23), (Q2_y_Bin_7)-(z_pT_Bin_25), (Q2_y_Bin_7)-(z_pT_Bin_26)
(Q2_y_Bin_7)-(z_pT_Bin_27), (Q2_y_Bin_7)-(z_pT_Bin_28), (Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission]
(Q2_y_Bin_7)-(z_pT_Bin_7), (Q2_y_Bin_7)-(z_pT_Bin_8), (Q2_y_Bin_7)-(z_pT_Bin_9)
(Q2_y_Bin_8)-(z_pT_Bin_11), (Q2_y_Bin_8)-(z_pT_Bin_12), (Q2_y_Bin_8)-(z_pT_Bin_13)
(Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16), (Q2_y_Bin_8)-(z_pT_Bin_18)
(Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_21), (Q2_y_Bin_8)-(z_pT_Bin_23)
(Q2_y_Bin_8)-(z_pT_Bin_26), (Q2_y_Bin_8)-(z_pT_Bin_28), (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_9)-(z_pT_Bin_10), (Q2_y_Bin_9)-(z_pT_Bin_15), (Q2_y_Bin_9)-(z_pT_Bin_16)
(Q2_y_Bin_9)-(z_pT_Bin_2), (Q2_y_Bin_9)-(z_pT_Bin_22), (Q2_y_Bin_9)-(z_pT_Bin_3)
(Q2_y_Bin_9)-(z_pT_Bin_30), (Q2_y_Bin_9)-(z_pT_Bin_4), (Q2_y_Bin_9)-(z_pT_Bin_5)
(Q2_y_Bin_9)-(z_pT_Bin_6), (Q2_y_Bin_9)-(z_pT_Bin_8), (Q2_y_Bin_9)-(z_pT_Bin_9)

#### 120°

The rule fails every assessable manual exclusion (48).

Manually excluded but passes:

None.

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_16), (Q2_y_Bin_1)-(z_pT_Bin_30)
(Q2_y_Bin_1)-(z_pT_Bin_31), (Q2_y_Bin_1)-(z_pT_Bin_4), (Q2_y_Bin_1)-(z_pT_Bin_5)
(Q2_y_Bin_1)-(z_pT_Bin_6), (Q2_y_Bin_1)-(z_pT_Bin_7), (Q2_y_Bin_1)-(z_pT_Bin_8)
(Q2_y_Bin_1)-(z_pT_Bin_9), (Q2_y_Bin_10)-(z_pT_Bin_1), (Q2_y_Bin_10)-(z_pT_Bin_2)
(Q2_y_Bin_10)-(z_pT_Bin_3), (Q2_y_Bin_10)-(z_pT_Bin_31), (Q2_y_Bin_10)-(z_pT_Bin_4)
(Q2_y_Bin_10)-(z_pT_Bin_5), (Q2_y_Bin_10)-(z_pT_Bin_6), (Q2_y_Bin_10)-(z_pT_Bin_7)
(Q2_y_Bin_11)-(z_pT_Bin_1), (Q2_y_Bin_11)-(z_pT_Bin_10), (Q2_y_Bin_11)-(z_pT_Bin_15)
(Q2_y_Bin_11)-(z_pT_Bin_2), (Q2_y_Bin_11)-(z_pT_Bin_23), (Q2_y_Bin_11)-(z_pT_Bin_6)
(Q2_y_Bin_11)-(z_pT_Bin_9), (Q2_y_Bin_12)-(z_pT_Bin_11), (Q2_y_Bin_12)-(z_pT_Bin_21) [fit-quality omission]
(Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_6), (Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_13)-(z_pT_Bin_1), (Q2_y_Bin_13)-(z_pT_Bin_3), (Q2_y_Bin_13)-(z_pT_Bin_4)
(Q2_y_Bin_13)-(z_pT_Bin_5), (Q2_y_Bin_14)-(z_pT_Bin_1), (Q2_y_Bin_14)-(z_pT_Bin_2)
(Q2_y_Bin_14)-(z_pT_Bin_4), (Q2_y_Bin_14)-(z_pT_Bin_5), (Q2_y_Bin_15)-(z_pT_Bin_1)
(Q2_y_Bin_15)-(z_pT_Bin_19), (Q2_y_Bin_15)-(z_pT_Bin_2), (Q2_y_Bin_15)-(z_pT_Bin_23)
(Q2_y_Bin_15)-(z_pT_Bin_9), (Q2_y_Bin_16)-(z_pT_Bin_5), (Q2_y_Bin_16)-(z_pT_Bin_6)
(Q2_y_Bin_17)-(z_pT_Bin_4), (Q2_y_Bin_2)-(z_pT_Bin_1), (Q2_y_Bin_2)-(z_pT_Bin_10)
(Q2_y_Bin_2)-(z_pT_Bin_11), (Q2_y_Bin_2)-(z_pT_Bin_13), (Q2_y_Bin_2)-(z_pT_Bin_14)
(Q2_y_Bin_2)-(z_pT_Bin_15), (Q2_y_Bin_2)-(z_pT_Bin_16), (Q2_y_Bin_2)-(z_pT_Bin_19)
(Q2_y_Bin_2)-(z_pT_Bin_2), (Q2_y_Bin_2)-(z_pT_Bin_20), (Q2_y_Bin_2)-(z_pT_Bin_25)
(Q2_y_Bin_2)-(z_pT_Bin_26), (Q2_y_Bin_2)-(z_pT_Bin_3), (Q2_y_Bin_2)-(z_pT_Bin_32)
(Q2_y_Bin_2)-(z_pT_Bin_33), (Q2_y_Bin_2)-(z_pT_Bin_34), (Q2_y_Bin_2)-(z_pT_Bin_5)
(Q2_y_Bin_2)-(z_pT_Bin_6), (Q2_y_Bin_2)-(z_pT_Bin_7), (Q2_y_Bin_2)-(z_pT_Bin_8)
(Q2_y_Bin_2)-(z_pT_Bin_9), (Q2_y_Bin_3)-(z_pT_Bin_1), (Q2_y_Bin_3)-(z_pT_Bin_10)
(Q2_y_Bin_3)-(z_pT_Bin_11), (Q2_y_Bin_3)-(z_pT_Bin_12), (Q2_y_Bin_3)-(z_pT_Bin_13)
(Q2_y_Bin_3)-(z_pT_Bin_14), (Q2_y_Bin_3)-(z_pT_Bin_15), (Q2_y_Bin_3)-(z_pT_Bin_16)
(Q2_y_Bin_3)-(z_pT_Bin_17), (Q2_y_Bin_3)-(z_pT_Bin_18), (Q2_y_Bin_3)-(z_pT_Bin_2)
(Q2_y_Bin_3)-(z_pT_Bin_20), (Q2_y_Bin_3)-(z_pT_Bin_21), (Q2_y_Bin_3)-(z_pT_Bin_22)
(Q2_y_Bin_3)-(z_pT_Bin_23), (Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_7)
(Q2_y_Bin_3)-(z_pT_Bin_8), (Q2_y_Bin_3)-(z_pT_Bin_9), (Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_14), (Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_19), (Q2_y_Bin_4)-(z_pT_Bin_21), (Q2_y_Bin_4)-(z_pT_Bin_22) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_25), (Q2_y_Bin_4)-(z_pT_Bin_26)
(Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission], (Q2_y_Bin_5)-(z_pT_Bin_10)
(Q2_y_Bin_5)-(z_pT_Bin_13), (Q2_y_Bin_5)-(z_pT_Bin_14), (Q2_y_Bin_5)-(z_pT_Bin_15)
(Q2_y_Bin_5)-(z_pT_Bin_19), (Q2_y_Bin_5)-(z_pT_Bin_2), (Q2_y_Bin_5)-(z_pT_Bin_20)
(Q2_y_Bin_5)-(z_pT_Bin_25), (Q2_y_Bin_5)-(z_pT_Bin_3), (Q2_y_Bin_5)-(z_pT_Bin_31)
(Q2_y_Bin_5)-(z_pT_Bin_32), (Q2_y_Bin_5)-(z_pT_Bin_4), (Q2_y_Bin_5)-(z_pT_Bin_5)
(Q2_y_Bin_5)-(z_pT_Bin_6), (Q2_y_Bin_5)-(z_pT_Bin_7), (Q2_y_Bin_5)-(z_pT_Bin_8)
(Q2_y_Bin_5)-(z_pT_Bin_9), (Q2_y_Bin_6)-(z_pT_Bin_1), (Q2_y_Bin_6)-(z_pT_Bin_10)
(Q2_y_Bin_6)-(z_pT_Bin_14), (Q2_y_Bin_6)-(z_pT_Bin_19), (Q2_y_Bin_6)-(z_pT_Bin_2)
(Q2_y_Bin_6)-(z_pT_Bin_20), (Q2_y_Bin_6)-(z_pT_Bin_27), (Q2_y_Bin_6)-(z_pT_Bin_28)
(Q2_y_Bin_6)-(z_pT_Bin_3), (Q2_y_Bin_6)-(z_pT_Bin_4), (Q2_y_Bin_6)-(z_pT_Bin_5)
(Q2_y_Bin_6)-(z_pT_Bin_6), (Q2_y_Bin_6)-(z_pT_Bin_7), (Q2_y_Bin_6)-(z_pT_Bin_8)
(Q2_y_Bin_7)-(z_pT_Bin_1), (Q2_y_Bin_7)-(z_pT_Bin_10), (Q2_y_Bin_7)-(z_pT_Bin_11)
(Q2_y_Bin_7)-(z_pT_Bin_12), (Q2_y_Bin_7)-(z_pT_Bin_13), (Q2_y_Bin_7)-(z_pT_Bin_15)
(Q2_y_Bin_7)-(z_pT_Bin_16), (Q2_y_Bin_7)-(z_pT_Bin_17), (Q2_y_Bin_7)-(z_pT_Bin_18)
(Q2_y_Bin_7)-(z_pT_Bin_2), (Q2_y_Bin_7)-(z_pT_Bin_21), (Q2_y_Bin_7)-(z_pT_Bin_22)
(Q2_y_Bin_7)-(z_pT_Bin_23), (Q2_y_Bin_7)-(z_pT_Bin_26), (Q2_y_Bin_7)-(z_pT_Bin_27)
(Q2_y_Bin_7)-(z_pT_Bin_28), (Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_7)-(z_pT_Bin_7)
(Q2_y_Bin_7)-(z_pT_Bin_9), (Q2_y_Bin_8)-(z_pT_Bin_11), (Q2_y_Bin_8)-(z_pT_Bin_12)
(Q2_y_Bin_8)-(z_pT_Bin_13), (Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16)
(Q2_y_Bin_8)-(z_pT_Bin_18), (Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_21)
(Q2_y_Bin_8)-(z_pT_Bin_23), (Q2_y_Bin_8)-(z_pT_Bin_28), (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_9)-(z_pT_Bin_10), (Q2_y_Bin_9)-(z_pT_Bin_16), (Q2_y_Bin_9)-(z_pT_Bin_2)
(Q2_y_Bin_9)-(z_pT_Bin_3), (Q2_y_Bin_9)-(z_pT_Bin_4), (Q2_y_Bin_9)-(z_pT_Bin_5)
(Q2_y_Bin_9)-(z_pT_Bin_6), (Q2_y_Bin_9)-(z_pT_Bin_9)

#### 135°

The rule does not fail every assessable manual exclusion: 1 of 48 pass.

Manually excluded but passes:

(Q2_y_Bin_15)-(z_pT_Bin_21)

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_16), (Q2_y_Bin_1)-(z_pT_Bin_30)
(Q2_y_Bin_1)-(z_pT_Bin_31), (Q2_y_Bin_1)-(z_pT_Bin_4), (Q2_y_Bin_1)-(z_pT_Bin_5)
(Q2_y_Bin_1)-(z_pT_Bin_6), (Q2_y_Bin_1)-(z_pT_Bin_7), (Q2_y_Bin_1)-(z_pT_Bin_8)
(Q2_y_Bin_1)-(z_pT_Bin_9), (Q2_y_Bin_10)-(z_pT_Bin_1), (Q2_y_Bin_10)-(z_pT_Bin_2)
(Q2_y_Bin_10)-(z_pT_Bin_3), (Q2_y_Bin_10)-(z_pT_Bin_4), (Q2_y_Bin_10)-(z_pT_Bin_5)
(Q2_y_Bin_10)-(z_pT_Bin_6), (Q2_y_Bin_10)-(z_pT_Bin_7), (Q2_y_Bin_11)-(z_pT_Bin_1)
(Q2_y_Bin_11)-(z_pT_Bin_10), (Q2_y_Bin_11)-(z_pT_Bin_15), (Q2_y_Bin_11)-(z_pT_Bin_2)
(Q2_y_Bin_11)-(z_pT_Bin_23), (Q2_y_Bin_11)-(z_pT_Bin_6), (Q2_y_Bin_11)-(z_pT_Bin_9)
(Q2_y_Bin_12)-(z_pT_Bin_11), (Q2_y_Bin_12)-(z_pT_Bin_21) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission]
(Q2_y_Bin_12)-(z_pT_Bin_6), (Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_13)-(z_pT_Bin_1)
(Q2_y_Bin_13)-(z_pT_Bin_4), (Q2_y_Bin_13)-(z_pT_Bin_5), (Q2_y_Bin_14)-(z_pT_Bin_2)
(Q2_y_Bin_14)-(z_pT_Bin_4), (Q2_y_Bin_14)-(z_pT_Bin_5), (Q2_y_Bin_15)-(z_pT_Bin_1)
(Q2_y_Bin_15)-(z_pT_Bin_2), (Q2_y_Bin_15)-(z_pT_Bin_23), (Q2_y_Bin_15)-(z_pT_Bin_9)
(Q2_y_Bin_16)-(z_pT_Bin_5), (Q2_y_Bin_16)-(z_pT_Bin_6), (Q2_y_Bin_17)-(z_pT_Bin_4)
(Q2_y_Bin_2)-(z_pT_Bin_1), (Q2_y_Bin_2)-(z_pT_Bin_10), (Q2_y_Bin_2)-(z_pT_Bin_13)
(Q2_y_Bin_2)-(z_pT_Bin_14), (Q2_y_Bin_2)-(z_pT_Bin_15), (Q2_y_Bin_2)-(z_pT_Bin_16)
(Q2_y_Bin_2)-(z_pT_Bin_19), (Q2_y_Bin_2)-(z_pT_Bin_2), (Q2_y_Bin_2)-(z_pT_Bin_20)
(Q2_y_Bin_2)-(z_pT_Bin_25), (Q2_y_Bin_2)-(z_pT_Bin_3), (Q2_y_Bin_2)-(z_pT_Bin_32)
(Q2_y_Bin_2)-(z_pT_Bin_33), (Q2_y_Bin_2)-(z_pT_Bin_34), (Q2_y_Bin_2)-(z_pT_Bin_5)
(Q2_y_Bin_2)-(z_pT_Bin_6), (Q2_y_Bin_2)-(z_pT_Bin_7), (Q2_y_Bin_2)-(z_pT_Bin_8)
(Q2_y_Bin_2)-(z_pT_Bin_9), (Q2_y_Bin_3)-(z_pT_Bin_1), (Q2_y_Bin_3)-(z_pT_Bin_10)
(Q2_y_Bin_3)-(z_pT_Bin_11), (Q2_y_Bin_3)-(z_pT_Bin_12), (Q2_y_Bin_3)-(z_pT_Bin_13)
(Q2_y_Bin_3)-(z_pT_Bin_14), (Q2_y_Bin_3)-(z_pT_Bin_15), (Q2_y_Bin_3)-(z_pT_Bin_16)
(Q2_y_Bin_3)-(z_pT_Bin_17), (Q2_y_Bin_3)-(z_pT_Bin_18), (Q2_y_Bin_3)-(z_pT_Bin_2)
(Q2_y_Bin_3)-(z_pT_Bin_20), (Q2_y_Bin_3)-(z_pT_Bin_21), (Q2_y_Bin_3)-(z_pT_Bin_22)
(Q2_y_Bin_3)-(z_pT_Bin_23), (Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_7)
(Q2_y_Bin_3)-(z_pT_Bin_8), (Q2_y_Bin_3)-(z_pT_Bin_9), (Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_14), (Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_19), (Q2_y_Bin_4)-(z_pT_Bin_21), (Q2_y_Bin_4)-(z_pT_Bin_22) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_25), (Q2_y_Bin_4)-(z_pT_Bin_26)
(Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission], (Q2_y_Bin_5)-(z_pT_Bin_10)
(Q2_y_Bin_5)-(z_pT_Bin_13), (Q2_y_Bin_5)-(z_pT_Bin_14), (Q2_y_Bin_5)-(z_pT_Bin_15)
(Q2_y_Bin_5)-(z_pT_Bin_19), (Q2_y_Bin_5)-(z_pT_Bin_2), (Q2_y_Bin_5)-(z_pT_Bin_25)
(Q2_y_Bin_5)-(z_pT_Bin_3), (Q2_y_Bin_5)-(z_pT_Bin_31), (Q2_y_Bin_5)-(z_pT_Bin_32)
(Q2_y_Bin_5)-(z_pT_Bin_4), (Q2_y_Bin_5)-(z_pT_Bin_5), (Q2_y_Bin_5)-(z_pT_Bin_6)
(Q2_y_Bin_5)-(z_pT_Bin_7), (Q2_y_Bin_5)-(z_pT_Bin_8), (Q2_y_Bin_5)-(z_pT_Bin_9)
(Q2_y_Bin_6)-(z_pT_Bin_1), (Q2_y_Bin_6)-(z_pT_Bin_14), (Q2_y_Bin_6)-(z_pT_Bin_2)
(Q2_y_Bin_6)-(z_pT_Bin_20), (Q2_y_Bin_6)-(z_pT_Bin_27), (Q2_y_Bin_6)-(z_pT_Bin_28)
(Q2_y_Bin_6)-(z_pT_Bin_3), (Q2_y_Bin_6)-(z_pT_Bin_4), (Q2_y_Bin_6)-(z_pT_Bin_5)
(Q2_y_Bin_6)-(z_pT_Bin_6), (Q2_y_Bin_6)-(z_pT_Bin_7), (Q2_y_Bin_6)-(z_pT_Bin_8)
(Q2_y_Bin_7)-(z_pT_Bin_1), (Q2_y_Bin_7)-(z_pT_Bin_10), (Q2_y_Bin_7)-(z_pT_Bin_11)
(Q2_y_Bin_7)-(z_pT_Bin_12), (Q2_y_Bin_7)-(z_pT_Bin_13), (Q2_y_Bin_7)-(z_pT_Bin_15)
(Q2_y_Bin_7)-(z_pT_Bin_17), (Q2_y_Bin_7)-(z_pT_Bin_2), (Q2_y_Bin_7)-(z_pT_Bin_21)
(Q2_y_Bin_7)-(z_pT_Bin_27), (Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_7)-(z_pT_Bin_7)
(Q2_y_Bin_7)-(z_pT_Bin_9), (Q2_y_Bin_8)-(z_pT_Bin_11), (Q2_y_Bin_8)-(z_pT_Bin_13)
(Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16), (Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_21), (Q2_y_Bin_8)-(z_pT_Bin_23), (Q2_y_Bin_8)-(z_pT_Bin_28)
(Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_9)-(z_pT_Bin_2), (Q2_y_Bin_9)-(z_pT_Bin_3)
(Q2_y_Bin_9)-(z_pT_Bin_4), (Q2_y_Bin_9)-(z_pT_Bin_5)

#### 150°

The rule does not fail every assessable manual exclusion: 3 of 48 pass.

Manually excluded but passes:

(Q2_y_Bin_11)-(z_pT_Bin_20), (Q2_y_Bin_15)-(z_pT_Bin_21), (Q2_y_Bin_7)-(z_pT_Bin_29)

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_16), (Q2_y_Bin_1)-(z_pT_Bin_30)
(Q2_y_Bin_1)-(z_pT_Bin_4), (Q2_y_Bin_1)-(z_pT_Bin_5), (Q2_y_Bin_1)-(z_pT_Bin_6)
(Q2_y_Bin_1)-(z_pT_Bin_8), (Q2_y_Bin_1)-(z_pT_Bin_9), (Q2_y_Bin_10)-(z_pT_Bin_1)
(Q2_y_Bin_10)-(z_pT_Bin_2), (Q2_y_Bin_10)-(z_pT_Bin_3), (Q2_y_Bin_10)-(z_pT_Bin_4)
(Q2_y_Bin_10)-(z_pT_Bin_5), (Q2_y_Bin_10)-(z_pT_Bin_6), (Q2_y_Bin_10)-(z_pT_Bin_7)
(Q2_y_Bin_11)-(z_pT_Bin_1), (Q2_y_Bin_11)-(z_pT_Bin_2), (Q2_y_Bin_11)-(z_pT_Bin_23)
(Q2_y_Bin_11)-(z_pT_Bin_6), (Q2_y_Bin_12)-(z_pT_Bin_11), (Q2_y_Bin_12)-(z_pT_Bin_21) [fit-quality omission]
(Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_6), (Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_13)-(z_pT_Bin_1), (Q2_y_Bin_14)-(z_pT_Bin_4), (Q2_y_Bin_14)-(z_pT_Bin_5)
(Q2_y_Bin_15)-(z_pT_Bin_1), (Q2_y_Bin_15)-(z_pT_Bin_2), (Q2_y_Bin_15)-(z_pT_Bin_23)
(Q2_y_Bin_15)-(z_pT_Bin_9), (Q2_y_Bin_16)-(z_pT_Bin_6), (Q2_y_Bin_17)-(z_pT_Bin_4)
(Q2_y_Bin_2)-(z_pT_Bin_1), (Q2_y_Bin_2)-(z_pT_Bin_10), (Q2_y_Bin_2)-(z_pT_Bin_13)
(Q2_y_Bin_2)-(z_pT_Bin_14), (Q2_y_Bin_2)-(z_pT_Bin_2), (Q2_y_Bin_2)-(z_pT_Bin_20)
(Q2_y_Bin_2)-(z_pT_Bin_25), (Q2_y_Bin_2)-(z_pT_Bin_3), (Q2_y_Bin_2)-(z_pT_Bin_32)
(Q2_y_Bin_2)-(z_pT_Bin_34), (Q2_y_Bin_2)-(z_pT_Bin_5), (Q2_y_Bin_2)-(z_pT_Bin_6)
(Q2_y_Bin_2)-(z_pT_Bin_7), (Q2_y_Bin_2)-(z_pT_Bin_8), (Q2_y_Bin_2)-(z_pT_Bin_9)
(Q2_y_Bin_3)-(z_pT_Bin_1), (Q2_y_Bin_3)-(z_pT_Bin_10), (Q2_y_Bin_3)-(z_pT_Bin_11)
(Q2_y_Bin_3)-(z_pT_Bin_12), (Q2_y_Bin_3)-(z_pT_Bin_13), (Q2_y_Bin_3)-(z_pT_Bin_15)
(Q2_y_Bin_3)-(z_pT_Bin_18), (Q2_y_Bin_3)-(z_pT_Bin_2), (Q2_y_Bin_3)-(z_pT_Bin_20)
(Q2_y_Bin_3)-(z_pT_Bin_21), (Q2_y_Bin_3)-(z_pT_Bin_23), (Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_7), (Q2_y_Bin_3)-(z_pT_Bin_9), (Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_14), (Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_19), (Q2_y_Bin_4)-(z_pT_Bin_21), (Q2_y_Bin_4)-(z_pT_Bin_22) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_25), (Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission], (Q2_y_Bin_5)-(z_pT_Bin_10), (Q2_y_Bin_5)-(z_pT_Bin_13)
(Q2_y_Bin_5)-(z_pT_Bin_14), (Q2_y_Bin_5)-(z_pT_Bin_19), (Q2_y_Bin_5)-(z_pT_Bin_2)
(Q2_y_Bin_5)-(z_pT_Bin_25), (Q2_y_Bin_5)-(z_pT_Bin_3), (Q2_y_Bin_5)-(z_pT_Bin_31)
(Q2_y_Bin_5)-(z_pT_Bin_4), (Q2_y_Bin_5)-(z_pT_Bin_5), (Q2_y_Bin_5)-(z_pT_Bin_6)
(Q2_y_Bin_5)-(z_pT_Bin_7), (Q2_y_Bin_5)-(z_pT_Bin_8), (Q2_y_Bin_5)-(z_pT_Bin_9)
(Q2_y_Bin_6)-(z_pT_Bin_1), (Q2_y_Bin_6)-(z_pT_Bin_2), (Q2_y_Bin_6)-(z_pT_Bin_20)
(Q2_y_Bin_6)-(z_pT_Bin_27), (Q2_y_Bin_6)-(z_pT_Bin_28), (Q2_y_Bin_6)-(z_pT_Bin_3)
(Q2_y_Bin_6)-(z_pT_Bin_4), (Q2_y_Bin_6)-(z_pT_Bin_5), (Q2_y_Bin_6)-(z_pT_Bin_6)
(Q2_y_Bin_6)-(z_pT_Bin_7), (Q2_y_Bin_6)-(z_pT_Bin_8), (Q2_y_Bin_7)-(z_pT_Bin_1)
(Q2_y_Bin_7)-(z_pT_Bin_11), (Q2_y_Bin_7)-(z_pT_Bin_12), (Q2_y_Bin_7)-(z_pT_Bin_13)
(Q2_y_Bin_7)-(z_pT_Bin_2), (Q2_y_Bin_7)-(z_pT_Bin_21), (Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission]
(Q2_y_Bin_7)-(z_pT_Bin_7), (Q2_y_Bin_8)-(z_pT_Bin_11), (Q2_y_Bin_8)-(z_pT_Bin_13)
(Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16), (Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_28), (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_9)-(z_pT_Bin_2)
(Q2_y_Bin_9)-(z_pT_Bin_3), (Q2_y_Bin_9)-(z_pT_Bin_4)

#### 180°

The rule does not fail every assessable manual exclusion: 7 of 48 pass.

Manually excluded but passes:

(Q2_y_Bin_1)-(z_pT_Bin_22), (Q2_y_Bin_11)-(z_pT_Bin_20), (Q2_y_Bin_15)-(z_pT_Bin_21)
(Q2_y_Bin_15)-(z_pT_Bin_22), (Q2_y_Bin_6)-(z_pT_Bin_9), (Q2_y_Bin_7)-(z_pT_Bin_29)
(Q2_y_Bin_9)-(z_pT_Bin_29)

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_30), (Q2_y_Bin_1)-(z_pT_Bin_4), (Q2_y_Bin_1)-(z_pT_Bin_5)
(Q2_y_Bin_1)-(z_pT_Bin_8), (Q2_y_Bin_1)-(z_pT_Bin_9), (Q2_y_Bin_10)-(z_pT_Bin_5)
(Q2_y_Bin_10)-(z_pT_Bin_6), (Q2_y_Bin_11)-(z_pT_Bin_2), (Q2_y_Bin_11)-(z_pT_Bin_23)
(Q2_y_Bin_12)-(z_pT_Bin_11), (Q2_y_Bin_12)-(z_pT_Bin_21) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission]
(Q2_y_Bin_12)-(z_pT_Bin_6), (Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_13)-(z_pT_Bin_1)
(Q2_y_Bin_14)-(z_pT_Bin_5), (Q2_y_Bin_15)-(z_pT_Bin_1), (Q2_y_Bin_15)-(z_pT_Bin_2)
(Q2_y_Bin_2)-(z_pT_Bin_1), (Q2_y_Bin_2)-(z_pT_Bin_2), (Q2_y_Bin_2)-(z_pT_Bin_3)
(Q2_y_Bin_2)-(z_pT_Bin_5), (Q2_y_Bin_2)-(z_pT_Bin_6), (Q2_y_Bin_2)-(z_pT_Bin_7)
(Q2_y_Bin_2)-(z_pT_Bin_9), (Q2_y_Bin_3)-(z_pT_Bin_1), (Q2_y_Bin_3)-(z_pT_Bin_10)
(Q2_y_Bin_3)-(z_pT_Bin_15), (Q2_y_Bin_3)-(z_pT_Bin_2), (Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_7), (Q2_y_Bin_3)-(z_pT_Bin_9), (Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_19)
(Q2_y_Bin_4)-(z_pT_Bin_21), (Q2_y_Bin_4)-(z_pT_Bin_22) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_25), (Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission]
(Q2_y_Bin_5)-(z_pT_Bin_2), (Q2_y_Bin_5)-(z_pT_Bin_3), (Q2_y_Bin_5)-(z_pT_Bin_31)
(Q2_y_Bin_5)-(z_pT_Bin_4), (Q2_y_Bin_5)-(z_pT_Bin_5), (Q2_y_Bin_5)-(z_pT_Bin_6)
(Q2_y_Bin_5)-(z_pT_Bin_7), (Q2_y_Bin_5)-(z_pT_Bin_8), (Q2_y_Bin_5)-(z_pT_Bin_9)
(Q2_y_Bin_6)-(z_pT_Bin_1), (Q2_y_Bin_7)-(z_pT_Bin_12), (Q2_y_Bin_7)-(z_pT_Bin_2)
(Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_11), (Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_16), (Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission]

### pipS5o

Manual list entries: 40. Fit-quality omissions relative to the nominal acceptance bins: 37. Comparisons the budget still keeps: 380.

#### 90°

The rule fails every assessable manual exclusion (40).

Manually excluded but passes:

None.

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_11), (Q2_y_Bin_1)-(z_pT_Bin_15)
(Q2_y_Bin_1)-(z_pT_Bin_16), (Q2_y_Bin_1)-(z_pT_Bin_17), (Q2_y_Bin_1)-(z_pT_Bin_2)
(Q2_y_Bin_1)-(z_pT_Bin_22), (Q2_y_Bin_1)-(z_pT_Bin_23), (Q2_y_Bin_1)-(z_pT_Bin_30)
(Q2_y_Bin_1)-(z_pT_Bin_31), (Q2_y_Bin_1)-(z_pT_Bin_32), (Q2_y_Bin_1)-(z_pT_Bin_4)
(Q2_y_Bin_1)-(z_pT_Bin_5), (Q2_y_Bin_1)-(z_pT_Bin_6), (Q2_y_Bin_1)-(z_pT_Bin_7)
(Q2_y_Bin_1)-(z_pT_Bin_8), (Q2_y_Bin_1)-(z_pT_Bin_9), (Q2_y_Bin_10)-(z_pT_Bin_1)
(Q2_y_Bin_10)-(z_pT_Bin_10), (Q2_y_Bin_10)-(z_pT_Bin_11), (Q2_y_Bin_10)-(z_pT_Bin_15)
(Q2_y_Bin_10)-(z_pT_Bin_2), (Q2_y_Bin_10)-(z_pT_Bin_20), (Q2_y_Bin_10)-(z_pT_Bin_3)
(Q2_y_Bin_10)-(z_pT_Bin_31), (Q2_y_Bin_10)-(z_pT_Bin_32), (Q2_y_Bin_10)-(z_pT_Bin_33)
(Q2_y_Bin_10)-(z_pT_Bin_4), (Q2_y_Bin_10)-(z_pT_Bin_5), (Q2_y_Bin_10)-(z_pT_Bin_6)
(Q2_y_Bin_10)-(z_pT_Bin_7), (Q2_y_Bin_10)-(z_pT_Bin_9), (Q2_y_Bin_11)-(z_pT_Bin_1)
(Q2_y_Bin_11)-(z_pT_Bin_10), (Q2_y_Bin_11)-(z_pT_Bin_13), (Q2_y_Bin_11)-(z_pT_Bin_14)
(Q2_y_Bin_11)-(z_pT_Bin_15), (Q2_y_Bin_11)-(z_pT_Bin_18), (Q2_y_Bin_11)-(z_pT_Bin_2)
(Q2_y_Bin_11)-(z_pT_Bin_20), (Q2_y_Bin_11)-(z_pT_Bin_21), (Q2_y_Bin_11)-(z_pT_Bin_23)
(Q2_y_Bin_11)-(z_pT_Bin_24), (Q2_y_Bin_11)-(z_pT_Bin_3), (Q2_y_Bin_11)-(z_pT_Bin_6)
(Q2_y_Bin_11)-(z_pT_Bin_8), (Q2_y_Bin_11)-(z_pT_Bin_9), (Q2_y_Bin_12)-(z_pT_Bin_12)
(Q2_y_Bin_12)-(z_pT_Bin_13), (Q2_y_Bin_12)-(z_pT_Bin_16), (Q2_y_Bin_12)-(z_pT_Bin_18)
(Q2_y_Bin_12)-(z_pT_Bin_21) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_13)-(z_pT_Bin_1), (Q2_y_Bin_13)-(z_pT_Bin_12), (Q2_y_Bin_13)-(z_pT_Bin_2)
(Q2_y_Bin_13)-(z_pT_Bin_26), (Q2_y_Bin_13)-(z_pT_Bin_3), (Q2_y_Bin_13)-(z_pT_Bin_4)
(Q2_y_Bin_13)-(z_pT_Bin_5), (Q2_y_Bin_13)-(z_pT_Bin_7), (Q2_y_Bin_13)-(z_pT_Bin_8)
(Q2_y_Bin_14)-(z_pT_Bin_1), (Q2_y_Bin_14)-(z_pT_Bin_2), (Q2_y_Bin_14)-(z_pT_Bin_3)
(Q2_y_Bin_14)-(z_pT_Bin_32), (Q2_y_Bin_14)-(z_pT_Bin_4), (Q2_y_Bin_14)-(z_pT_Bin_5)
(Q2_y_Bin_15)-(z_pT_Bin_1), (Q2_y_Bin_15)-(z_pT_Bin_13), (Q2_y_Bin_15)-(z_pT_Bin_14)
(Q2_y_Bin_15)-(z_pT_Bin_15), (Q2_y_Bin_15)-(z_pT_Bin_2), (Q2_y_Bin_15)-(z_pT_Bin_21)
(Q2_y_Bin_15)-(z_pT_Bin_23), (Q2_y_Bin_15)-(z_pT_Bin_24), (Q2_y_Bin_15)-(z_pT_Bin_9)
(Q2_y_Bin_16)-(z_pT_Bin_4), (Q2_y_Bin_16)-(z_pT_Bin_6), (Q2_y_Bin_17)-(z_pT_Bin_2)
(Q2_y_Bin_17)-(z_pT_Bin_3), (Q2_y_Bin_17)-(z_pT_Bin_4), (Q2_y_Bin_2)-(z_pT_Bin_1)
(Q2_y_Bin_2)-(z_pT_Bin_10), (Q2_y_Bin_2)-(z_pT_Bin_11), (Q2_y_Bin_2)-(z_pT_Bin_12)
(Q2_y_Bin_2)-(z_pT_Bin_13), (Q2_y_Bin_2)-(z_pT_Bin_15), (Q2_y_Bin_2)-(z_pT_Bin_16)
(Q2_y_Bin_2)-(z_pT_Bin_17), (Q2_y_Bin_2)-(z_pT_Bin_19), (Q2_y_Bin_2)-(z_pT_Bin_2)
(Q2_y_Bin_2)-(z_pT_Bin_20), (Q2_y_Bin_2)-(z_pT_Bin_21), (Q2_y_Bin_2)-(z_pT_Bin_22)
(Q2_y_Bin_2)-(z_pT_Bin_23), (Q2_y_Bin_2)-(z_pT_Bin_25), (Q2_y_Bin_2)-(z_pT_Bin_26)
(Q2_y_Bin_2)-(z_pT_Bin_27), (Q2_y_Bin_2)-(z_pT_Bin_28), (Q2_y_Bin_2)-(z_pT_Bin_3)
(Q2_y_Bin_2)-(z_pT_Bin_32), (Q2_y_Bin_2)-(z_pT_Bin_33), (Q2_y_Bin_2)-(z_pT_Bin_34)
(Q2_y_Bin_2)-(z_pT_Bin_4), (Q2_y_Bin_2)-(z_pT_Bin_5), (Q2_y_Bin_2)-(z_pT_Bin_6)
(Q2_y_Bin_2)-(z_pT_Bin_7), (Q2_y_Bin_2)-(z_pT_Bin_9), (Q2_y_Bin_3)-(z_pT_Bin_1)
(Q2_y_Bin_3)-(z_pT_Bin_10), (Q2_y_Bin_3)-(z_pT_Bin_11), (Q2_y_Bin_3)-(z_pT_Bin_12)
(Q2_y_Bin_3)-(z_pT_Bin_13), (Q2_y_Bin_3)-(z_pT_Bin_14), (Q2_y_Bin_3)-(z_pT_Bin_15)
(Q2_y_Bin_3)-(z_pT_Bin_16), (Q2_y_Bin_3)-(z_pT_Bin_17), (Q2_y_Bin_3)-(z_pT_Bin_18)
(Q2_y_Bin_3)-(z_pT_Bin_19), (Q2_y_Bin_3)-(z_pT_Bin_2), (Q2_y_Bin_3)-(z_pT_Bin_20)
(Q2_y_Bin_3)-(z_pT_Bin_21), (Q2_y_Bin_3)-(z_pT_Bin_22), (Q2_y_Bin_3)-(z_pT_Bin_23)
(Q2_y_Bin_3)-(z_pT_Bin_24), (Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_7)
(Q2_y_Bin_3)-(z_pT_Bin_8), (Q2_y_Bin_3)-(z_pT_Bin_9), (Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_14), (Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_20), (Q2_y_Bin_4)-(z_pT_Bin_21), (Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_26), (Q2_y_Bin_4)-(z_pT_Bin_27), (Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission], (Q2_y_Bin_5)-(z_pT_Bin_1), (Q2_y_Bin_5)-(z_pT_Bin_10)
(Q2_y_Bin_5)-(z_pT_Bin_11), (Q2_y_Bin_5)-(z_pT_Bin_13), (Q2_y_Bin_5)-(z_pT_Bin_14)
(Q2_y_Bin_5)-(z_pT_Bin_15), (Q2_y_Bin_5)-(z_pT_Bin_16), (Q2_y_Bin_5)-(z_pT_Bin_19)
(Q2_y_Bin_5)-(z_pT_Bin_2), (Q2_y_Bin_5)-(z_pT_Bin_20), (Q2_y_Bin_5)-(z_pT_Bin_25)
(Q2_y_Bin_5)-(z_pT_Bin_26), (Q2_y_Bin_5)-(z_pT_Bin_3), (Q2_y_Bin_5)-(z_pT_Bin_32)
(Q2_y_Bin_5)-(z_pT_Bin_5), (Q2_y_Bin_5)-(z_pT_Bin_6), (Q2_y_Bin_5)-(z_pT_Bin_7)
(Q2_y_Bin_5)-(z_pT_Bin_8), (Q2_y_Bin_5)-(z_pT_Bin_9), (Q2_y_Bin_6)-(z_pT_Bin_1)
(Q2_y_Bin_6)-(z_pT_Bin_10), (Q2_y_Bin_6)-(z_pT_Bin_11), (Q2_y_Bin_6)-(z_pT_Bin_13)
(Q2_y_Bin_6)-(z_pT_Bin_14), (Q2_y_Bin_6)-(z_pT_Bin_15), (Q2_y_Bin_6)-(z_pT_Bin_16)
(Q2_y_Bin_6)-(z_pT_Bin_19), (Q2_y_Bin_6)-(z_pT_Bin_2), (Q2_y_Bin_6)-(z_pT_Bin_20)
(Q2_y_Bin_6)-(z_pT_Bin_27), (Q2_y_Bin_6)-(z_pT_Bin_28), (Q2_y_Bin_6)-(z_pT_Bin_3)
(Q2_y_Bin_6)-(z_pT_Bin_4), (Q2_y_Bin_6)-(z_pT_Bin_5), (Q2_y_Bin_6)-(z_pT_Bin_6)
(Q2_y_Bin_6)-(z_pT_Bin_7), (Q2_y_Bin_6)-(z_pT_Bin_8), (Q2_y_Bin_6)-(z_pT_Bin_9)
(Q2_y_Bin_7)-(z_pT_Bin_1), (Q2_y_Bin_7)-(z_pT_Bin_10), (Q2_y_Bin_7)-(z_pT_Bin_11)
(Q2_y_Bin_7)-(z_pT_Bin_12), (Q2_y_Bin_7)-(z_pT_Bin_13), (Q2_y_Bin_7)-(z_pT_Bin_15)
(Q2_y_Bin_7)-(z_pT_Bin_16), (Q2_y_Bin_7)-(z_pT_Bin_17), (Q2_y_Bin_7)-(z_pT_Bin_18)
(Q2_y_Bin_7)-(z_pT_Bin_19), (Q2_y_Bin_7)-(z_pT_Bin_2), (Q2_y_Bin_7)-(z_pT_Bin_20)
(Q2_y_Bin_7)-(z_pT_Bin_21), (Q2_y_Bin_7)-(z_pT_Bin_22), (Q2_y_Bin_7)-(z_pT_Bin_23)
(Q2_y_Bin_7)-(z_pT_Bin_24), (Q2_y_Bin_7)-(z_pT_Bin_25), (Q2_y_Bin_7)-(z_pT_Bin_26)
(Q2_y_Bin_7)-(z_pT_Bin_27), (Q2_y_Bin_7)-(z_pT_Bin_28), (Q2_y_Bin_7)-(z_pT_Bin_29)
(Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_7)-(z_pT_Bin_7), (Q2_y_Bin_7)-(z_pT_Bin_8)
(Q2_y_Bin_7)-(z_pT_Bin_9), (Q2_y_Bin_8)-(z_pT_Bin_11), (Q2_y_Bin_8)-(z_pT_Bin_12)
(Q2_y_Bin_8)-(z_pT_Bin_13), (Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16)
(Q2_y_Bin_8)-(z_pT_Bin_18), (Q2_y_Bin_8)-(z_pT_Bin_19), (Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_21), (Q2_y_Bin_8)-(z_pT_Bin_23), (Q2_y_Bin_8)-(z_pT_Bin_26)
(Q2_y_Bin_8)-(z_pT_Bin_28), (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_9)-(z_pT_Bin_1)
(Q2_y_Bin_9)-(z_pT_Bin_10), (Q2_y_Bin_9)-(z_pT_Bin_15), (Q2_y_Bin_9)-(z_pT_Bin_2)
(Q2_y_Bin_9)-(z_pT_Bin_22), (Q2_y_Bin_9)-(z_pT_Bin_23), (Q2_y_Bin_9)-(z_pT_Bin_29)
(Q2_y_Bin_9)-(z_pT_Bin_3), (Q2_y_Bin_9)-(z_pT_Bin_4), (Q2_y_Bin_9)-(z_pT_Bin_5)
(Q2_y_Bin_9)-(z_pT_Bin_6), (Q2_y_Bin_9)-(z_pT_Bin_7), (Q2_y_Bin_9)-(z_pT_Bin_8)

#### 120°

The rule fails every assessable manual exclusion (40).

Manually excluded but passes:

None.

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_15), (Q2_y_Bin_1)-(z_pT_Bin_16)
(Q2_y_Bin_1)-(z_pT_Bin_17), (Q2_y_Bin_1)-(z_pT_Bin_2), (Q2_y_Bin_1)-(z_pT_Bin_22)
(Q2_y_Bin_1)-(z_pT_Bin_23), (Q2_y_Bin_1)-(z_pT_Bin_30), (Q2_y_Bin_1)-(z_pT_Bin_31)
(Q2_y_Bin_1)-(z_pT_Bin_32), (Q2_y_Bin_1)-(z_pT_Bin_4), (Q2_y_Bin_1)-(z_pT_Bin_5)
(Q2_y_Bin_1)-(z_pT_Bin_6), (Q2_y_Bin_1)-(z_pT_Bin_8), (Q2_y_Bin_1)-(z_pT_Bin_9)
(Q2_y_Bin_10)-(z_pT_Bin_1), (Q2_y_Bin_10)-(z_pT_Bin_15), (Q2_y_Bin_10)-(z_pT_Bin_2)
(Q2_y_Bin_10)-(z_pT_Bin_3), (Q2_y_Bin_10)-(z_pT_Bin_31), (Q2_y_Bin_10)-(z_pT_Bin_32)
(Q2_y_Bin_10)-(z_pT_Bin_4), (Q2_y_Bin_10)-(z_pT_Bin_5), (Q2_y_Bin_10)-(z_pT_Bin_6)
(Q2_y_Bin_10)-(z_pT_Bin_7), (Q2_y_Bin_11)-(z_pT_Bin_1), (Q2_y_Bin_11)-(z_pT_Bin_10)
(Q2_y_Bin_11)-(z_pT_Bin_2), (Q2_y_Bin_11)-(z_pT_Bin_20), (Q2_y_Bin_11)-(z_pT_Bin_21)
(Q2_y_Bin_11)-(z_pT_Bin_23), (Q2_y_Bin_11)-(z_pT_Bin_24), (Q2_y_Bin_11)-(z_pT_Bin_3)
(Q2_y_Bin_11)-(z_pT_Bin_6), (Q2_y_Bin_11)-(z_pT_Bin_9), (Q2_y_Bin_12)-(z_pT_Bin_21) [fit-quality omission]
(Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_13)-(z_pT_Bin_1)
(Q2_y_Bin_14)-(z_pT_Bin_2), (Q2_y_Bin_14)-(z_pT_Bin_32), (Q2_y_Bin_14)-(z_pT_Bin_4)
(Q2_y_Bin_14)-(z_pT_Bin_5), (Q2_y_Bin_15)-(z_pT_Bin_1), (Q2_y_Bin_15)-(z_pT_Bin_15)
(Q2_y_Bin_15)-(z_pT_Bin_2), (Q2_y_Bin_15)-(z_pT_Bin_21), (Q2_y_Bin_15)-(z_pT_Bin_23)
(Q2_y_Bin_15)-(z_pT_Bin_24), (Q2_y_Bin_15)-(z_pT_Bin_9), (Q2_y_Bin_16)-(z_pT_Bin_6)
(Q2_y_Bin_17)-(z_pT_Bin_4), (Q2_y_Bin_2)-(z_pT_Bin_1), (Q2_y_Bin_2)-(z_pT_Bin_10)
(Q2_y_Bin_2)-(z_pT_Bin_11), (Q2_y_Bin_2)-(z_pT_Bin_13), (Q2_y_Bin_2)-(z_pT_Bin_15)
(Q2_y_Bin_2)-(z_pT_Bin_16), (Q2_y_Bin_2)-(z_pT_Bin_19), (Q2_y_Bin_2)-(z_pT_Bin_2)
(Q2_y_Bin_2)-(z_pT_Bin_20), (Q2_y_Bin_2)-(z_pT_Bin_21), (Q2_y_Bin_2)-(z_pT_Bin_25)
(Q2_y_Bin_2)-(z_pT_Bin_26), (Q2_y_Bin_2)-(z_pT_Bin_27), (Q2_y_Bin_2)-(z_pT_Bin_3)
(Q2_y_Bin_2)-(z_pT_Bin_32), (Q2_y_Bin_2)-(z_pT_Bin_33), (Q2_y_Bin_2)-(z_pT_Bin_34)
(Q2_y_Bin_2)-(z_pT_Bin_4), (Q2_y_Bin_2)-(z_pT_Bin_5), (Q2_y_Bin_2)-(z_pT_Bin_6)
(Q2_y_Bin_2)-(z_pT_Bin_7), (Q2_y_Bin_2)-(z_pT_Bin_9), (Q2_y_Bin_3)-(z_pT_Bin_1)
(Q2_y_Bin_3)-(z_pT_Bin_10), (Q2_y_Bin_3)-(z_pT_Bin_11), (Q2_y_Bin_3)-(z_pT_Bin_12)
(Q2_y_Bin_3)-(z_pT_Bin_13), (Q2_y_Bin_3)-(z_pT_Bin_14), (Q2_y_Bin_3)-(z_pT_Bin_15)
(Q2_y_Bin_3)-(z_pT_Bin_16), (Q2_y_Bin_3)-(z_pT_Bin_17), (Q2_y_Bin_3)-(z_pT_Bin_18)
(Q2_y_Bin_3)-(z_pT_Bin_2), (Q2_y_Bin_3)-(z_pT_Bin_20), (Q2_y_Bin_3)-(z_pT_Bin_21)
(Q2_y_Bin_3)-(z_pT_Bin_22), (Q2_y_Bin_3)-(z_pT_Bin_23), (Q2_y_Bin_3)-(z_pT_Bin_24)
(Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_7), (Q2_y_Bin_3)-(z_pT_Bin_8)
(Q2_y_Bin_3)-(z_pT_Bin_9), (Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_14)
(Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_21)
(Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_26), (Q2_y_Bin_4)-(z_pT_Bin_27)
(Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission], (Q2_y_Bin_5)-(z_pT_Bin_1)
(Q2_y_Bin_5)-(z_pT_Bin_10), (Q2_y_Bin_5)-(z_pT_Bin_13), (Q2_y_Bin_5)-(z_pT_Bin_14)
(Q2_y_Bin_5)-(z_pT_Bin_15), (Q2_y_Bin_5)-(z_pT_Bin_19), (Q2_y_Bin_5)-(z_pT_Bin_2)
(Q2_y_Bin_5)-(z_pT_Bin_20), (Q2_y_Bin_5)-(z_pT_Bin_25), (Q2_y_Bin_5)-(z_pT_Bin_3)
(Q2_y_Bin_5)-(z_pT_Bin_32), (Q2_y_Bin_5)-(z_pT_Bin_5), (Q2_y_Bin_5)-(z_pT_Bin_6)
(Q2_y_Bin_5)-(z_pT_Bin_7), (Q2_y_Bin_5)-(z_pT_Bin_8), (Q2_y_Bin_5)-(z_pT_Bin_9)
(Q2_y_Bin_6)-(z_pT_Bin_1), (Q2_y_Bin_6)-(z_pT_Bin_10), (Q2_y_Bin_6)-(z_pT_Bin_14)
(Q2_y_Bin_6)-(z_pT_Bin_19), (Q2_y_Bin_6)-(z_pT_Bin_2), (Q2_y_Bin_6)-(z_pT_Bin_20)
(Q2_y_Bin_6)-(z_pT_Bin_27), (Q2_y_Bin_6)-(z_pT_Bin_28), (Q2_y_Bin_6)-(z_pT_Bin_3)
(Q2_y_Bin_6)-(z_pT_Bin_4), (Q2_y_Bin_6)-(z_pT_Bin_5), (Q2_y_Bin_6)-(z_pT_Bin_6)
(Q2_y_Bin_6)-(z_pT_Bin_7), (Q2_y_Bin_6)-(z_pT_Bin_8), (Q2_y_Bin_6)-(z_pT_Bin_9)
(Q2_y_Bin_7)-(z_pT_Bin_1), (Q2_y_Bin_7)-(z_pT_Bin_10), (Q2_y_Bin_7)-(z_pT_Bin_11)
(Q2_y_Bin_7)-(z_pT_Bin_12), (Q2_y_Bin_7)-(z_pT_Bin_13), (Q2_y_Bin_7)-(z_pT_Bin_15)
(Q2_y_Bin_7)-(z_pT_Bin_16), (Q2_y_Bin_7)-(z_pT_Bin_17), (Q2_y_Bin_7)-(z_pT_Bin_18)
(Q2_y_Bin_7)-(z_pT_Bin_2), (Q2_y_Bin_7)-(z_pT_Bin_21), (Q2_y_Bin_7)-(z_pT_Bin_23)
(Q2_y_Bin_7)-(z_pT_Bin_24), (Q2_y_Bin_7)-(z_pT_Bin_26), (Q2_y_Bin_7)-(z_pT_Bin_27)
(Q2_y_Bin_7)-(z_pT_Bin_29), (Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_7)-(z_pT_Bin_7)
(Q2_y_Bin_7)-(z_pT_Bin_9), (Q2_y_Bin_8)-(z_pT_Bin_11), (Q2_y_Bin_8)-(z_pT_Bin_12)
(Q2_y_Bin_8)-(z_pT_Bin_13), (Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16)
(Q2_y_Bin_8)-(z_pT_Bin_18), (Q2_y_Bin_8)-(z_pT_Bin_19), (Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_21), (Q2_y_Bin_8)-(z_pT_Bin_23), (Q2_y_Bin_8)-(z_pT_Bin_28)
(Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_9)-(z_pT_Bin_1), (Q2_y_Bin_9)-(z_pT_Bin_10)
(Q2_y_Bin_9)-(z_pT_Bin_2), (Q2_y_Bin_9)-(z_pT_Bin_29), (Q2_y_Bin_9)-(z_pT_Bin_3)
(Q2_y_Bin_9)-(z_pT_Bin_4), (Q2_y_Bin_9)-(z_pT_Bin_5), (Q2_y_Bin_9)-(z_pT_Bin_6)

#### 135°

The rule does not fail every assessable manual exclusion: 1 of 40 pass.

Manually excluded but passes:

(Q2_y_Bin_9)-(z_pT_Bin_9)

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_15), (Q2_y_Bin_1)-(z_pT_Bin_16)
(Q2_y_Bin_1)-(z_pT_Bin_2), (Q2_y_Bin_1)-(z_pT_Bin_22), (Q2_y_Bin_1)-(z_pT_Bin_23)
(Q2_y_Bin_1)-(z_pT_Bin_30), (Q2_y_Bin_1)-(z_pT_Bin_4), (Q2_y_Bin_1)-(z_pT_Bin_5)
(Q2_y_Bin_1)-(z_pT_Bin_6), (Q2_y_Bin_1)-(z_pT_Bin_8), (Q2_y_Bin_1)-(z_pT_Bin_9)
(Q2_y_Bin_10)-(z_pT_Bin_1), (Q2_y_Bin_10)-(z_pT_Bin_15), (Q2_y_Bin_10)-(z_pT_Bin_2)
(Q2_y_Bin_10)-(z_pT_Bin_3), (Q2_y_Bin_10)-(z_pT_Bin_31), (Q2_y_Bin_10)-(z_pT_Bin_32)
(Q2_y_Bin_10)-(z_pT_Bin_4), (Q2_y_Bin_10)-(z_pT_Bin_5), (Q2_y_Bin_10)-(z_pT_Bin_6)
(Q2_y_Bin_10)-(z_pT_Bin_7), (Q2_y_Bin_11)-(z_pT_Bin_1), (Q2_y_Bin_11)-(z_pT_Bin_10)
(Q2_y_Bin_11)-(z_pT_Bin_2), (Q2_y_Bin_11)-(z_pT_Bin_20), (Q2_y_Bin_11)-(z_pT_Bin_21)
(Q2_y_Bin_11)-(z_pT_Bin_23), (Q2_y_Bin_11)-(z_pT_Bin_24), (Q2_y_Bin_11)-(z_pT_Bin_3)
(Q2_y_Bin_11)-(z_pT_Bin_6), (Q2_y_Bin_12)-(z_pT_Bin_21) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission]
(Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_13)-(z_pT_Bin_1), (Q2_y_Bin_14)-(z_pT_Bin_2)
(Q2_y_Bin_14)-(z_pT_Bin_32), (Q2_y_Bin_14)-(z_pT_Bin_4), (Q2_y_Bin_14)-(z_pT_Bin_5)
(Q2_y_Bin_15)-(z_pT_Bin_1), (Q2_y_Bin_15)-(z_pT_Bin_15), (Q2_y_Bin_15)-(z_pT_Bin_2)
(Q2_y_Bin_15)-(z_pT_Bin_23), (Q2_y_Bin_15)-(z_pT_Bin_24), (Q2_y_Bin_15)-(z_pT_Bin_9)
(Q2_y_Bin_16)-(z_pT_Bin_6), (Q2_y_Bin_17)-(z_pT_Bin_4), (Q2_y_Bin_2)-(z_pT_Bin_1)
(Q2_y_Bin_2)-(z_pT_Bin_10), (Q2_y_Bin_2)-(z_pT_Bin_11), (Q2_y_Bin_2)-(z_pT_Bin_13)
(Q2_y_Bin_2)-(z_pT_Bin_15), (Q2_y_Bin_2)-(z_pT_Bin_16), (Q2_y_Bin_2)-(z_pT_Bin_19)
(Q2_y_Bin_2)-(z_pT_Bin_2), (Q2_y_Bin_2)-(z_pT_Bin_20), (Q2_y_Bin_2)-(z_pT_Bin_25)
(Q2_y_Bin_2)-(z_pT_Bin_3), (Q2_y_Bin_2)-(z_pT_Bin_32), (Q2_y_Bin_2)-(z_pT_Bin_33)
(Q2_y_Bin_2)-(z_pT_Bin_34), (Q2_y_Bin_2)-(z_pT_Bin_4), (Q2_y_Bin_2)-(z_pT_Bin_5)
(Q2_y_Bin_2)-(z_pT_Bin_6), (Q2_y_Bin_2)-(z_pT_Bin_7), (Q2_y_Bin_2)-(z_pT_Bin_9)
(Q2_y_Bin_3)-(z_pT_Bin_1), (Q2_y_Bin_3)-(z_pT_Bin_10), (Q2_y_Bin_3)-(z_pT_Bin_11)
(Q2_y_Bin_3)-(z_pT_Bin_12), (Q2_y_Bin_3)-(z_pT_Bin_13), (Q2_y_Bin_3)-(z_pT_Bin_14)
(Q2_y_Bin_3)-(z_pT_Bin_15), (Q2_y_Bin_3)-(z_pT_Bin_16), (Q2_y_Bin_3)-(z_pT_Bin_17)
(Q2_y_Bin_3)-(z_pT_Bin_18), (Q2_y_Bin_3)-(z_pT_Bin_2), (Q2_y_Bin_3)-(z_pT_Bin_20)
(Q2_y_Bin_3)-(z_pT_Bin_21), (Q2_y_Bin_3)-(z_pT_Bin_24), (Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_7), (Q2_y_Bin_3)-(z_pT_Bin_8), (Q2_y_Bin_3)-(z_pT_Bin_9)
(Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_14), (Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_21), (Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_26), (Q2_y_Bin_4)-(z_pT_Bin_27), (Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission], (Q2_y_Bin_5)-(z_pT_Bin_1), (Q2_y_Bin_5)-(z_pT_Bin_10)
(Q2_y_Bin_5)-(z_pT_Bin_13), (Q2_y_Bin_5)-(z_pT_Bin_14), (Q2_y_Bin_5)-(z_pT_Bin_15)
(Q2_y_Bin_5)-(z_pT_Bin_19), (Q2_y_Bin_5)-(z_pT_Bin_2), (Q2_y_Bin_5)-(z_pT_Bin_20)
(Q2_y_Bin_5)-(z_pT_Bin_25), (Q2_y_Bin_5)-(z_pT_Bin_3), (Q2_y_Bin_5)-(z_pT_Bin_32)
(Q2_y_Bin_5)-(z_pT_Bin_5), (Q2_y_Bin_5)-(z_pT_Bin_6), (Q2_y_Bin_5)-(z_pT_Bin_7)
(Q2_y_Bin_5)-(z_pT_Bin_8), (Q2_y_Bin_5)-(z_pT_Bin_9), (Q2_y_Bin_6)-(z_pT_Bin_1)
(Q2_y_Bin_6)-(z_pT_Bin_10), (Q2_y_Bin_6)-(z_pT_Bin_14), (Q2_y_Bin_6)-(z_pT_Bin_2)
(Q2_y_Bin_6)-(z_pT_Bin_20), (Q2_y_Bin_6)-(z_pT_Bin_27), (Q2_y_Bin_6)-(z_pT_Bin_28)
(Q2_y_Bin_6)-(z_pT_Bin_3), (Q2_y_Bin_6)-(z_pT_Bin_4), (Q2_y_Bin_6)-(z_pT_Bin_5)
(Q2_y_Bin_6)-(z_pT_Bin_6), (Q2_y_Bin_6)-(z_pT_Bin_8), (Q2_y_Bin_6)-(z_pT_Bin_9)
(Q2_y_Bin_7)-(z_pT_Bin_1), (Q2_y_Bin_7)-(z_pT_Bin_10), (Q2_y_Bin_7)-(z_pT_Bin_11)
(Q2_y_Bin_7)-(z_pT_Bin_12), (Q2_y_Bin_7)-(z_pT_Bin_13), (Q2_y_Bin_7)-(z_pT_Bin_15)
(Q2_y_Bin_7)-(z_pT_Bin_16), (Q2_y_Bin_7)-(z_pT_Bin_17), (Q2_y_Bin_7)-(z_pT_Bin_2)
(Q2_y_Bin_7)-(z_pT_Bin_21), (Q2_y_Bin_7)-(z_pT_Bin_24), (Q2_y_Bin_7)-(z_pT_Bin_26)
(Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_7)-(z_pT_Bin_7), (Q2_y_Bin_8)-(z_pT_Bin_11)
(Q2_y_Bin_8)-(z_pT_Bin_13), (Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16)
(Q2_y_Bin_8)-(z_pT_Bin_19), (Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_21)
(Q2_y_Bin_8)-(z_pT_Bin_23), (Q2_y_Bin_8)-(z_pT_Bin_28), (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_9)-(z_pT_Bin_1), (Q2_y_Bin_9)-(z_pT_Bin_2), (Q2_y_Bin_9)-(z_pT_Bin_29)
(Q2_y_Bin_9)-(z_pT_Bin_3), (Q2_y_Bin_9)-(z_pT_Bin_4)

#### 150°

The rule does not fail every assessable manual exclusion: 3 of 40 pass.

Manually excluded but passes:

(Q2_y_Bin_10)-(z_pT_Bin_26), (Q2_y_Bin_9)-(z_pT_Bin_16), (Q2_y_Bin_9)-(z_pT_Bin_9)

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_15), (Q2_y_Bin_1)-(z_pT_Bin_16)
(Q2_y_Bin_1)-(z_pT_Bin_2), (Q2_y_Bin_1)-(z_pT_Bin_22), (Q2_y_Bin_1)-(z_pT_Bin_30)
(Q2_y_Bin_1)-(z_pT_Bin_4), (Q2_y_Bin_1)-(z_pT_Bin_5), (Q2_y_Bin_1)-(z_pT_Bin_6)
(Q2_y_Bin_1)-(z_pT_Bin_8), (Q2_y_Bin_1)-(z_pT_Bin_9), (Q2_y_Bin_10)-(z_pT_Bin_3)
(Q2_y_Bin_10)-(z_pT_Bin_31), (Q2_y_Bin_10)-(z_pT_Bin_32), (Q2_y_Bin_10)-(z_pT_Bin_4)
(Q2_y_Bin_10)-(z_pT_Bin_5), (Q2_y_Bin_10)-(z_pT_Bin_6), (Q2_y_Bin_11)-(z_pT_Bin_1)
(Q2_y_Bin_11)-(z_pT_Bin_2), (Q2_y_Bin_11)-(z_pT_Bin_21), (Q2_y_Bin_11)-(z_pT_Bin_23)
(Q2_y_Bin_11)-(z_pT_Bin_24), (Q2_y_Bin_11)-(z_pT_Bin_3), (Q2_y_Bin_11)-(z_pT_Bin_6)
(Q2_y_Bin_12)-(z_pT_Bin_21) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_13)-(z_pT_Bin_1), (Q2_y_Bin_14)-(z_pT_Bin_5), (Q2_y_Bin_15)-(z_pT_Bin_1)
(Q2_y_Bin_15)-(z_pT_Bin_15), (Q2_y_Bin_15)-(z_pT_Bin_2), (Q2_y_Bin_15)-(z_pT_Bin_23)
(Q2_y_Bin_15)-(z_pT_Bin_24), (Q2_y_Bin_15)-(z_pT_Bin_9), (Q2_y_Bin_17)-(z_pT_Bin_4)
(Q2_y_Bin_2)-(z_pT_Bin_1), (Q2_y_Bin_2)-(z_pT_Bin_10), (Q2_y_Bin_2)-(z_pT_Bin_19)
(Q2_y_Bin_2)-(z_pT_Bin_2), (Q2_y_Bin_2)-(z_pT_Bin_20), (Q2_y_Bin_2)-(z_pT_Bin_25)
(Q2_y_Bin_2)-(z_pT_Bin_3), (Q2_y_Bin_2)-(z_pT_Bin_32), (Q2_y_Bin_2)-(z_pT_Bin_33)
(Q2_y_Bin_2)-(z_pT_Bin_4), (Q2_y_Bin_2)-(z_pT_Bin_5), (Q2_y_Bin_2)-(z_pT_Bin_6)
(Q2_y_Bin_2)-(z_pT_Bin_7), (Q2_y_Bin_2)-(z_pT_Bin_9), (Q2_y_Bin_3)-(z_pT_Bin_1)
(Q2_y_Bin_3)-(z_pT_Bin_10), (Q2_y_Bin_3)-(z_pT_Bin_11), (Q2_y_Bin_3)-(z_pT_Bin_12)
(Q2_y_Bin_3)-(z_pT_Bin_13), (Q2_y_Bin_3)-(z_pT_Bin_15), (Q2_y_Bin_3)-(z_pT_Bin_2)
(Q2_y_Bin_3)-(z_pT_Bin_20), (Q2_y_Bin_3)-(z_pT_Bin_21), (Q2_y_Bin_3)-(z_pT_Bin_24)
(Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_7), (Q2_y_Bin_3)-(z_pT_Bin_9)
(Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_21), (Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_27)
(Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission], (Q2_y_Bin_5)-(z_pT_Bin_1)
(Q2_y_Bin_5)-(z_pT_Bin_13), (Q2_y_Bin_5)-(z_pT_Bin_14), (Q2_y_Bin_5)-(z_pT_Bin_2)
(Q2_y_Bin_5)-(z_pT_Bin_20), (Q2_y_Bin_5)-(z_pT_Bin_25), (Q2_y_Bin_5)-(z_pT_Bin_3)
(Q2_y_Bin_5)-(z_pT_Bin_32), (Q2_y_Bin_5)-(z_pT_Bin_5), (Q2_y_Bin_5)-(z_pT_Bin_6)
(Q2_y_Bin_5)-(z_pT_Bin_7), (Q2_y_Bin_5)-(z_pT_Bin_8), (Q2_y_Bin_5)-(z_pT_Bin_9)
(Q2_y_Bin_6)-(z_pT_Bin_1), (Q2_y_Bin_6)-(z_pT_Bin_14), (Q2_y_Bin_6)-(z_pT_Bin_20)
(Q2_y_Bin_6)-(z_pT_Bin_27), (Q2_y_Bin_6)-(z_pT_Bin_3), (Q2_y_Bin_6)-(z_pT_Bin_4)
(Q2_y_Bin_6)-(z_pT_Bin_5), (Q2_y_Bin_6)-(z_pT_Bin_9), (Q2_y_Bin_7)-(z_pT_Bin_1)
(Q2_y_Bin_7)-(z_pT_Bin_11), (Q2_y_Bin_7)-(z_pT_Bin_12), (Q2_y_Bin_7)-(z_pT_Bin_13)
(Q2_y_Bin_7)-(z_pT_Bin_2), (Q2_y_Bin_7)-(z_pT_Bin_21), (Q2_y_Bin_7)-(z_pT_Bin_24)
(Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_7)-(z_pT_Bin_7), (Q2_y_Bin_8)-(z_pT_Bin_11)
(Q2_y_Bin_8)-(z_pT_Bin_13), (Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16)
(Q2_y_Bin_8)-(z_pT_Bin_19), (Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_28)
(Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_9)-(z_pT_Bin_1), (Q2_y_Bin_9)-(z_pT_Bin_2)
(Q2_y_Bin_9)-(z_pT_Bin_29), (Q2_y_Bin_9)-(z_pT_Bin_3), (Q2_y_Bin_9)-(z_pT_Bin_4)

#### 180°

The rule does not fail every assessable manual exclusion: 5 of 40 pass.

Manually excluded but passes:

(Q2_y_Bin_10)-(z_pT_Bin_26), (Q2_y_Bin_2)-(z_pT_Bin_14), (Q2_y_Bin_2)-(z_pT_Bin_8)
(Q2_y_Bin_9)-(z_pT_Bin_16), (Q2_y_Bin_9)-(z_pT_Bin_9)

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_15), (Q2_y_Bin_1)-(z_pT_Bin_2), (Q2_y_Bin_1)-(z_pT_Bin_30)
(Q2_y_Bin_1)-(z_pT_Bin_4), (Q2_y_Bin_1)-(z_pT_Bin_5), (Q2_y_Bin_1)-(z_pT_Bin_8)
(Q2_y_Bin_1)-(z_pT_Bin_9), (Q2_y_Bin_10)-(z_pT_Bin_6), (Q2_y_Bin_11)-(z_pT_Bin_23)
(Q2_y_Bin_11)-(z_pT_Bin_24), (Q2_y_Bin_11)-(z_pT_Bin_3), (Q2_y_Bin_12)-(z_pT_Bin_21) [fit-quality omission]
(Q2_y_Bin_12)-(z_pT_Bin_24) [fit-quality omission], (Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_14)-(z_pT_Bin_5)
(Q2_y_Bin_15)-(z_pT_Bin_15), (Q2_y_Bin_15)-(z_pT_Bin_2), (Q2_y_Bin_15)-(z_pT_Bin_23)
(Q2_y_Bin_15)-(z_pT_Bin_24), (Q2_y_Bin_2)-(z_pT_Bin_1), (Q2_y_Bin_2)-(z_pT_Bin_2)
(Q2_y_Bin_2)-(z_pT_Bin_3), (Q2_y_Bin_2)-(z_pT_Bin_4), (Q2_y_Bin_2)-(z_pT_Bin_5)
(Q2_y_Bin_2)-(z_pT_Bin_6), (Q2_y_Bin_2)-(z_pT_Bin_7), (Q2_y_Bin_2)-(z_pT_Bin_9)
(Q2_y_Bin_3)-(z_pT_Bin_1), (Q2_y_Bin_3)-(z_pT_Bin_10), (Q2_y_Bin_3)-(z_pT_Bin_2)
(Q2_y_Bin_3)-(z_pT_Bin_24), (Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_29) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_7)
(Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_21), (Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_27)
(Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission], (Q2_y_Bin_5)-(z_pT_Bin_1)
(Q2_y_Bin_5)-(z_pT_Bin_2), (Q2_y_Bin_5)-(z_pT_Bin_3), (Q2_y_Bin_5)-(z_pT_Bin_5)
(Q2_y_Bin_5)-(z_pT_Bin_7), (Q2_y_Bin_5)-(z_pT_Bin_9), (Q2_y_Bin_6)-(z_pT_Bin_27)
(Q2_y_Bin_7)-(z_pT_Bin_12), (Q2_y_Bin_7)-(z_pT_Bin_13), (Q2_y_Bin_7)-(z_pT_Bin_2)
(Q2_y_Bin_7)-(z_pT_Bin_24), (Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_11)
(Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16), (Q2_y_Bin_8)-(z_pT_Bin_19)
(Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_9)-(z_pT_Bin_1)
(Q2_y_Bin_9)-(z_pT_Bin_29)

### pipS6o

Manual list entries: 52. Fit-quality omissions relative to the nominal acceptance bins: 35. Comparisons the budget still keeps: 371.

#### 90°

The rule fails every assessable manual exclusion (52).

Manually excluded but passes:

None.

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_11), (Q2_y_Bin_1)-(z_pT_Bin_16)
(Q2_y_Bin_1)-(z_pT_Bin_17), (Q2_y_Bin_1)-(z_pT_Bin_23), (Q2_y_Bin_1)-(z_pT_Bin_30)
(Q2_y_Bin_1)-(z_pT_Bin_31), (Q2_y_Bin_1)-(z_pT_Bin_32), (Q2_y_Bin_1)-(z_pT_Bin_4)
(Q2_y_Bin_1)-(z_pT_Bin_5), (Q2_y_Bin_1)-(z_pT_Bin_6), (Q2_y_Bin_1)-(z_pT_Bin_7)
(Q2_y_Bin_10)-(z_pT_Bin_1), (Q2_y_Bin_10)-(z_pT_Bin_10), (Q2_y_Bin_10)-(z_pT_Bin_13)
(Q2_y_Bin_10)-(z_pT_Bin_15), (Q2_y_Bin_10)-(z_pT_Bin_2), (Q2_y_Bin_10)-(z_pT_Bin_20)
(Q2_y_Bin_10)-(z_pT_Bin_26), (Q2_y_Bin_10)-(z_pT_Bin_3), (Q2_y_Bin_10)-(z_pT_Bin_31)
(Q2_y_Bin_10)-(z_pT_Bin_32), (Q2_y_Bin_10)-(z_pT_Bin_4), (Q2_y_Bin_10)-(z_pT_Bin_5)
(Q2_y_Bin_10)-(z_pT_Bin_6), (Q2_y_Bin_10)-(z_pT_Bin_7), (Q2_y_Bin_10)-(z_pT_Bin_8)
(Q2_y_Bin_10)-(z_pT_Bin_9), (Q2_y_Bin_11)-(z_pT_Bin_1), (Q2_y_Bin_11)-(z_pT_Bin_10)
(Q2_y_Bin_11)-(z_pT_Bin_13), (Q2_y_Bin_11)-(z_pT_Bin_15), (Q2_y_Bin_11)-(z_pT_Bin_18)
(Q2_y_Bin_11)-(z_pT_Bin_2), (Q2_y_Bin_11)-(z_pT_Bin_20), (Q2_y_Bin_11)-(z_pT_Bin_21)
(Q2_y_Bin_11)-(z_pT_Bin_22), (Q2_y_Bin_11)-(z_pT_Bin_23), (Q2_y_Bin_11)-(z_pT_Bin_24)
(Q2_y_Bin_11)-(z_pT_Bin_3), (Q2_y_Bin_11)-(z_pT_Bin_6), (Q2_y_Bin_11)-(z_pT_Bin_9)
(Q2_y_Bin_12)-(z_pT_Bin_13), (Q2_y_Bin_12)-(z_pT_Bin_16), (Q2_y_Bin_12)-(z_pT_Bin_18)
(Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_13)-(z_pT_Bin_1), (Q2_y_Bin_13)-(z_pT_Bin_12)
(Q2_y_Bin_13)-(z_pT_Bin_2), (Q2_y_Bin_13)-(z_pT_Bin_26), (Q2_y_Bin_13)-(z_pT_Bin_3)
(Q2_y_Bin_13)-(z_pT_Bin_4), (Q2_y_Bin_13)-(z_pT_Bin_5), (Q2_y_Bin_13)-(z_pT_Bin_7)
(Q2_y_Bin_13)-(z_pT_Bin_8), (Q2_y_Bin_14)-(z_pT_Bin_1), (Q2_y_Bin_14)-(z_pT_Bin_2)
(Q2_y_Bin_14)-(z_pT_Bin_32), (Q2_y_Bin_14)-(z_pT_Bin_4), (Q2_y_Bin_14)-(z_pT_Bin_5)
(Q2_y_Bin_15)-(z_pT_Bin_15), (Q2_y_Bin_15)-(z_pT_Bin_19), (Q2_y_Bin_15)-(z_pT_Bin_21)
(Q2_y_Bin_15)-(z_pT_Bin_22), (Q2_y_Bin_15)-(z_pT_Bin_23), (Q2_y_Bin_15)-(z_pT_Bin_24)
(Q2_y_Bin_15)-(z_pT_Bin_6), (Q2_y_Bin_15)-(z_pT_Bin_9), (Q2_y_Bin_16)-(z_pT_Bin_3)
(Q2_y_Bin_16)-(z_pT_Bin_4), (Q2_y_Bin_16)-(z_pT_Bin_6), (Q2_y_Bin_17)-(z_pT_Bin_4)
(Q2_y_Bin_2)-(z_pT_Bin_1), (Q2_y_Bin_2)-(z_pT_Bin_10), (Q2_y_Bin_2)-(z_pT_Bin_11)
(Q2_y_Bin_2)-(z_pT_Bin_12), (Q2_y_Bin_2)-(z_pT_Bin_13), (Q2_y_Bin_2)-(z_pT_Bin_15)
(Q2_y_Bin_2)-(z_pT_Bin_16), (Q2_y_Bin_2)-(z_pT_Bin_19), (Q2_y_Bin_2)-(z_pT_Bin_2)
(Q2_y_Bin_2)-(z_pT_Bin_20), (Q2_y_Bin_2)-(z_pT_Bin_21), (Q2_y_Bin_2)-(z_pT_Bin_25)
(Q2_y_Bin_2)-(z_pT_Bin_26), (Q2_y_Bin_2)-(z_pT_Bin_27), (Q2_y_Bin_2)-(z_pT_Bin_28)
(Q2_y_Bin_2)-(z_pT_Bin_3), (Q2_y_Bin_2)-(z_pT_Bin_32), (Q2_y_Bin_2)-(z_pT_Bin_33)
(Q2_y_Bin_2)-(z_pT_Bin_34), (Q2_y_Bin_2)-(z_pT_Bin_4), (Q2_y_Bin_2)-(z_pT_Bin_5)
(Q2_y_Bin_2)-(z_pT_Bin_6), (Q2_y_Bin_2)-(z_pT_Bin_7), (Q2_y_Bin_2)-(z_pT_Bin_8)
(Q2_y_Bin_2)-(z_pT_Bin_9), (Q2_y_Bin_3)-(z_pT_Bin_1), (Q2_y_Bin_3)-(z_pT_Bin_11)
(Q2_y_Bin_3)-(z_pT_Bin_12), (Q2_y_Bin_3)-(z_pT_Bin_13), (Q2_y_Bin_3)-(z_pT_Bin_14)
(Q2_y_Bin_3)-(z_pT_Bin_16), (Q2_y_Bin_3)-(z_pT_Bin_17), (Q2_y_Bin_3)-(z_pT_Bin_18)
(Q2_y_Bin_3)-(z_pT_Bin_19), (Q2_y_Bin_3)-(z_pT_Bin_2), (Q2_y_Bin_3)-(z_pT_Bin_20)
(Q2_y_Bin_3)-(z_pT_Bin_21), (Q2_y_Bin_3)-(z_pT_Bin_22), (Q2_y_Bin_3)-(z_pT_Bin_23)
(Q2_y_Bin_3)-(z_pT_Bin_24), (Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_7), (Q2_y_Bin_3)-(z_pT_Bin_8)
(Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_14), (Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_20), (Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_26), (Q2_y_Bin_4)-(z_pT_Bin_27), (Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission], (Q2_y_Bin_5)-(z_pT_Bin_10), (Q2_y_Bin_5)-(z_pT_Bin_13)
(Q2_y_Bin_5)-(z_pT_Bin_15), (Q2_y_Bin_5)-(z_pT_Bin_19), (Q2_y_Bin_5)-(z_pT_Bin_20)
(Q2_y_Bin_5)-(z_pT_Bin_26), (Q2_y_Bin_5)-(z_pT_Bin_3), (Q2_y_Bin_5)-(z_pT_Bin_31)
(Q2_y_Bin_5)-(z_pT_Bin_32), (Q2_y_Bin_5)-(z_pT_Bin_4), (Q2_y_Bin_5)-(z_pT_Bin_5)
(Q2_y_Bin_5)-(z_pT_Bin_6), (Q2_y_Bin_6)-(z_pT_Bin_1), (Q2_y_Bin_6)-(z_pT_Bin_10)
(Q2_y_Bin_6)-(z_pT_Bin_11), (Q2_y_Bin_6)-(z_pT_Bin_13), (Q2_y_Bin_6)-(z_pT_Bin_14)
(Q2_y_Bin_6)-(z_pT_Bin_15), (Q2_y_Bin_6)-(z_pT_Bin_16), (Q2_y_Bin_6)-(z_pT_Bin_19)
(Q2_y_Bin_6)-(z_pT_Bin_2), (Q2_y_Bin_6)-(z_pT_Bin_20), (Q2_y_Bin_6)-(z_pT_Bin_26)
(Q2_y_Bin_6)-(z_pT_Bin_27), (Q2_y_Bin_6)-(z_pT_Bin_3), (Q2_y_Bin_6)-(z_pT_Bin_4)
(Q2_y_Bin_6)-(z_pT_Bin_5), (Q2_y_Bin_6)-(z_pT_Bin_6), (Q2_y_Bin_6)-(z_pT_Bin_7)
(Q2_y_Bin_6)-(z_pT_Bin_8), (Q2_y_Bin_6)-(z_pT_Bin_9), (Q2_y_Bin_7)-(z_pT_Bin_1)
(Q2_y_Bin_7)-(z_pT_Bin_10), (Q2_y_Bin_7)-(z_pT_Bin_11), (Q2_y_Bin_7)-(z_pT_Bin_12)
(Q2_y_Bin_7)-(z_pT_Bin_13), (Q2_y_Bin_7)-(z_pT_Bin_15), (Q2_y_Bin_7)-(z_pT_Bin_16)
(Q2_y_Bin_7)-(z_pT_Bin_17), (Q2_y_Bin_7)-(z_pT_Bin_18), (Q2_y_Bin_7)-(z_pT_Bin_19)
(Q2_y_Bin_7)-(z_pT_Bin_2), (Q2_y_Bin_7)-(z_pT_Bin_20), (Q2_y_Bin_7)-(z_pT_Bin_21)
(Q2_y_Bin_7)-(z_pT_Bin_22), (Q2_y_Bin_7)-(z_pT_Bin_23), (Q2_y_Bin_7)-(z_pT_Bin_24)
(Q2_y_Bin_7)-(z_pT_Bin_25), (Q2_y_Bin_7)-(z_pT_Bin_26), (Q2_y_Bin_7)-(z_pT_Bin_27)
(Q2_y_Bin_7)-(z_pT_Bin_28), (Q2_y_Bin_7)-(z_pT_Bin_29), (Q2_y_Bin_7)-(z_pT_Bin_31)
(Q2_y_Bin_7)-(z_pT_Bin_34), (Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_7)-(z_pT_Bin_7)
(Q2_y_Bin_7)-(z_pT_Bin_8), (Q2_y_Bin_7)-(z_pT_Bin_9), (Q2_y_Bin_8)-(z_pT_Bin_11)
(Q2_y_Bin_8)-(z_pT_Bin_12), (Q2_y_Bin_8)-(z_pT_Bin_13), (Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_16), (Q2_y_Bin_8)-(z_pT_Bin_18), (Q2_y_Bin_8)-(z_pT_Bin_19)
(Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_21), (Q2_y_Bin_8)-(z_pT_Bin_23)
(Q2_y_Bin_8)-(z_pT_Bin_26), (Q2_y_Bin_8)-(z_pT_Bin_28), (Q2_y_Bin_8)-(z_pT_Bin_29)
(Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_9)-(z_pT_Bin_10), (Q2_y_Bin_9)-(z_pT_Bin_11)
(Q2_y_Bin_9)-(z_pT_Bin_15), (Q2_y_Bin_9)-(z_pT_Bin_16), (Q2_y_Bin_9)-(z_pT_Bin_2)
(Q2_y_Bin_9)-(z_pT_Bin_22), (Q2_y_Bin_9)-(z_pT_Bin_3), (Q2_y_Bin_9)-(z_pT_Bin_30)
(Q2_y_Bin_9)-(z_pT_Bin_4), (Q2_y_Bin_9)-(z_pT_Bin_5), (Q2_y_Bin_9)-(z_pT_Bin_6)
(Q2_y_Bin_9)-(z_pT_Bin_8), (Q2_y_Bin_9)-(z_pT_Bin_9)

#### 120°

The rule fails every assessable manual exclusion (52).

Manually excluded but passes:

None.

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_16), (Q2_y_Bin_1)-(z_pT_Bin_23)
(Q2_y_Bin_1)-(z_pT_Bin_30), (Q2_y_Bin_1)-(z_pT_Bin_31), (Q2_y_Bin_1)-(z_pT_Bin_32)
(Q2_y_Bin_1)-(z_pT_Bin_4), (Q2_y_Bin_1)-(z_pT_Bin_5), (Q2_y_Bin_1)-(z_pT_Bin_6)
(Q2_y_Bin_1)-(z_pT_Bin_7), (Q2_y_Bin_10)-(z_pT_Bin_1), (Q2_y_Bin_10)-(z_pT_Bin_2)
(Q2_y_Bin_10)-(z_pT_Bin_26), (Q2_y_Bin_10)-(z_pT_Bin_3), (Q2_y_Bin_10)-(z_pT_Bin_31)
(Q2_y_Bin_10)-(z_pT_Bin_32), (Q2_y_Bin_10)-(z_pT_Bin_4), (Q2_y_Bin_10)-(z_pT_Bin_5)
(Q2_y_Bin_10)-(z_pT_Bin_6), (Q2_y_Bin_10)-(z_pT_Bin_7), (Q2_y_Bin_11)-(z_pT_Bin_1)
(Q2_y_Bin_11)-(z_pT_Bin_10), (Q2_y_Bin_11)-(z_pT_Bin_2), (Q2_y_Bin_11)-(z_pT_Bin_21)
(Q2_y_Bin_11)-(z_pT_Bin_22), (Q2_y_Bin_11)-(z_pT_Bin_23), (Q2_y_Bin_11)-(z_pT_Bin_24)
(Q2_y_Bin_11)-(z_pT_Bin_3), (Q2_y_Bin_11)-(z_pT_Bin_6), (Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_13)-(z_pT_Bin_1), (Q2_y_Bin_13)-(z_pT_Bin_4), (Q2_y_Bin_14)-(z_pT_Bin_2)
(Q2_y_Bin_14)-(z_pT_Bin_32), (Q2_y_Bin_14)-(z_pT_Bin_4), (Q2_y_Bin_14)-(z_pT_Bin_5)
(Q2_y_Bin_15)-(z_pT_Bin_15), (Q2_y_Bin_15)-(z_pT_Bin_22), (Q2_y_Bin_15)-(z_pT_Bin_23)
(Q2_y_Bin_15)-(z_pT_Bin_24), (Q2_y_Bin_15)-(z_pT_Bin_9), (Q2_y_Bin_16)-(z_pT_Bin_6)
(Q2_y_Bin_2)-(z_pT_Bin_1), (Q2_y_Bin_2)-(z_pT_Bin_10), (Q2_y_Bin_2)-(z_pT_Bin_11)
(Q2_y_Bin_2)-(z_pT_Bin_13), (Q2_y_Bin_2)-(z_pT_Bin_15), (Q2_y_Bin_2)-(z_pT_Bin_16)
(Q2_y_Bin_2)-(z_pT_Bin_19), (Q2_y_Bin_2)-(z_pT_Bin_2), (Q2_y_Bin_2)-(z_pT_Bin_20)
(Q2_y_Bin_2)-(z_pT_Bin_21), (Q2_y_Bin_2)-(z_pT_Bin_25), (Q2_y_Bin_2)-(z_pT_Bin_26)
(Q2_y_Bin_2)-(z_pT_Bin_3), (Q2_y_Bin_2)-(z_pT_Bin_32), (Q2_y_Bin_2)-(z_pT_Bin_33)
(Q2_y_Bin_2)-(z_pT_Bin_34), (Q2_y_Bin_2)-(z_pT_Bin_4), (Q2_y_Bin_2)-(z_pT_Bin_5)
(Q2_y_Bin_2)-(z_pT_Bin_6), (Q2_y_Bin_2)-(z_pT_Bin_7), (Q2_y_Bin_2)-(z_pT_Bin_8)
(Q2_y_Bin_2)-(z_pT_Bin_9), (Q2_y_Bin_3)-(z_pT_Bin_1), (Q2_y_Bin_3)-(z_pT_Bin_11)
(Q2_y_Bin_3)-(z_pT_Bin_12), (Q2_y_Bin_3)-(z_pT_Bin_13), (Q2_y_Bin_3)-(z_pT_Bin_14)
(Q2_y_Bin_3)-(z_pT_Bin_16), (Q2_y_Bin_3)-(z_pT_Bin_17), (Q2_y_Bin_3)-(z_pT_Bin_18)
(Q2_y_Bin_3)-(z_pT_Bin_19), (Q2_y_Bin_3)-(z_pT_Bin_2), (Q2_y_Bin_3)-(z_pT_Bin_20)
(Q2_y_Bin_3)-(z_pT_Bin_21), (Q2_y_Bin_3)-(z_pT_Bin_22), (Q2_y_Bin_3)-(z_pT_Bin_23)
(Q2_y_Bin_3)-(z_pT_Bin_24), (Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_7), (Q2_y_Bin_3)-(z_pT_Bin_8)
(Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_14), (Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_20), (Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_26), (Q2_y_Bin_4)-(z_pT_Bin_27), (Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission], (Q2_y_Bin_5)-(z_pT_Bin_10), (Q2_y_Bin_5)-(z_pT_Bin_13)
(Q2_y_Bin_5)-(z_pT_Bin_15), (Q2_y_Bin_5)-(z_pT_Bin_19), (Q2_y_Bin_5)-(z_pT_Bin_20)
(Q2_y_Bin_5)-(z_pT_Bin_3), (Q2_y_Bin_5)-(z_pT_Bin_31), (Q2_y_Bin_5)-(z_pT_Bin_32)
(Q2_y_Bin_5)-(z_pT_Bin_4), (Q2_y_Bin_5)-(z_pT_Bin_5), (Q2_y_Bin_5)-(z_pT_Bin_6)
(Q2_y_Bin_6)-(z_pT_Bin_1), (Q2_y_Bin_6)-(z_pT_Bin_10), (Q2_y_Bin_6)-(z_pT_Bin_14)
(Q2_y_Bin_6)-(z_pT_Bin_2), (Q2_y_Bin_6)-(z_pT_Bin_20), (Q2_y_Bin_6)-(z_pT_Bin_26)
(Q2_y_Bin_6)-(z_pT_Bin_27), (Q2_y_Bin_6)-(z_pT_Bin_3), (Q2_y_Bin_6)-(z_pT_Bin_4)
(Q2_y_Bin_6)-(z_pT_Bin_5), (Q2_y_Bin_6)-(z_pT_Bin_6), (Q2_y_Bin_6)-(z_pT_Bin_7)
(Q2_y_Bin_6)-(z_pT_Bin_8), (Q2_y_Bin_6)-(z_pT_Bin_9), (Q2_y_Bin_7)-(z_pT_Bin_1)
(Q2_y_Bin_7)-(z_pT_Bin_10), (Q2_y_Bin_7)-(z_pT_Bin_11), (Q2_y_Bin_7)-(z_pT_Bin_12)
(Q2_y_Bin_7)-(z_pT_Bin_13), (Q2_y_Bin_7)-(z_pT_Bin_15), (Q2_y_Bin_7)-(z_pT_Bin_16)
(Q2_y_Bin_7)-(z_pT_Bin_17), (Q2_y_Bin_7)-(z_pT_Bin_2), (Q2_y_Bin_7)-(z_pT_Bin_21)
(Q2_y_Bin_7)-(z_pT_Bin_24), (Q2_y_Bin_7)-(z_pT_Bin_26), (Q2_y_Bin_7)-(z_pT_Bin_27)
(Q2_y_Bin_7)-(z_pT_Bin_29), (Q2_y_Bin_7)-(z_pT_Bin_31), (Q2_y_Bin_7)-(z_pT_Bin_34)
(Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_7)-(z_pT_Bin_7), (Q2_y_Bin_7)-(z_pT_Bin_9)
(Q2_y_Bin_8)-(z_pT_Bin_11), (Q2_y_Bin_8)-(z_pT_Bin_12), (Q2_y_Bin_8)-(z_pT_Bin_13)
(Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16), (Q2_y_Bin_8)-(z_pT_Bin_18)
(Q2_y_Bin_8)-(z_pT_Bin_19), (Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_21)
(Q2_y_Bin_8)-(z_pT_Bin_23), (Q2_y_Bin_8)-(z_pT_Bin_26), (Q2_y_Bin_8)-(z_pT_Bin_28)
(Q2_y_Bin_8)-(z_pT_Bin_29), (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_9)-(z_pT_Bin_10)
(Q2_y_Bin_9)-(z_pT_Bin_15), (Q2_y_Bin_9)-(z_pT_Bin_2), (Q2_y_Bin_9)-(z_pT_Bin_3)
(Q2_y_Bin_9)-(z_pT_Bin_4), (Q2_y_Bin_9)-(z_pT_Bin_5), (Q2_y_Bin_9)-(z_pT_Bin_8)

#### 135°

The rule fails every assessable manual exclusion (52).

Manually excluded but passes:

None.

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_16), (Q2_y_Bin_1)-(z_pT_Bin_30)
(Q2_y_Bin_1)-(z_pT_Bin_31), (Q2_y_Bin_1)-(z_pT_Bin_4), (Q2_y_Bin_1)-(z_pT_Bin_5)
(Q2_y_Bin_1)-(z_pT_Bin_6), (Q2_y_Bin_1)-(z_pT_Bin_7), (Q2_y_Bin_10)-(z_pT_Bin_1)
(Q2_y_Bin_10)-(z_pT_Bin_2), (Q2_y_Bin_10)-(z_pT_Bin_3), (Q2_y_Bin_10)-(z_pT_Bin_32)
(Q2_y_Bin_10)-(z_pT_Bin_4), (Q2_y_Bin_10)-(z_pT_Bin_5), (Q2_y_Bin_10)-(z_pT_Bin_6)
(Q2_y_Bin_10)-(z_pT_Bin_7), (Q2_y_Bin_11)-(z_pT_Bin_1), (Q2_y_Bin_11)-(z_pT_Bin_2)
(Q2_y_Bin_11)-(z_pT_Bin_22), (Q2_y_Bin_11)-(z_pT_Bin_23), (Q2_y_Bin_11)-(z_pT_Bin_24)
(Q2_y_Bin_11)-(z_pT_Bin_3), (Q2_y_Bin_11)-(z_pT_Bin_6), (Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_13)-(z_pT_Bin_1), (Q2_y_Bin_14)-(z_pT_Bin_32), (Q2_y_Bin_14)-(z_pT_Bin_5)
(Q2_y_Bin_15)-(z_pT_Bin_15), (Q2_y_Bin_15)-(z_pT_Bin_22), (Q2_y_Bin_15)-(z_pT_Bin_23)
(Q2_y_Bin_15)-(z_pT_Bin_24), (Q2_y_Bin_15)-(z_pT_Bin_9), (Q2_y_Bin_16)-(z_pT_Bin_6)
(Q2_y_Bin_2)-(z_pT_Bin_1), (Q2_y_Bin_2)-(z_pT_Bin_10), (Q2_y_Bin_2)-(z_pT_Bin_13)
(Q2_y_Bin_2)-(z_pT_Bin_15), (Q2_y_Bin_2)-(z_pT_Bin_16), (Q2_y_Bin_2)-(z_pT_Bin_19)
(Q2_y_Bin_2)-(z_pT_Bin_2), (Q2_y_Bin_2)-(z_pT_Bin_20), (Q2_y_Bin_2)-(z_pT_Bin_25)
(Q2_y_Bin_2)-(z_pT_Bin_3), (Q2_y_Bin_2)-(z_pT_Bin_32), (Q2_y_Bin_2)-(z_pT_Bin_33)
(Q2_y_Bin_2)-(z_pT_Bin_34), (Q2_y_Bin_2)-(z_pT_Bin_4), (Q2_y_Bin_2)-(z_pT_Bin_5)
(Q2_y_Bin_2)-(z_pT_Bin_6), (Q2_y_Bin_2)-(z_pT_Bin_7), (Q2_y_Bin_2)-(z_pT_Bin_8)
(Q2_y_Bin_2)-(z_pT_Bin_9), (Q2_y_Bin_3)-(z_pT_Bin_1), (Q2_y_Bin_3)-(z_pT_Bin_11)
(Q2_y_Bin_3)-(z_pT_Bin_12), (Q2_y_Bin_3)-(z_pT_Bin_13), (Q2_y_Bin_3)-(z_pT_Bin_14)
(Q2_y_Bin_3)-(z_pT_Bin_16), (Q2_y_Bin_3)-(z_pT_Bin_17), (Q2_y_Bin_3)-(z_pT_Bin_18)
(Q2_y_Bin_3)-(z_pT_Bin_19), (Q2_y_Bin_3)-(z_pT_Bin_2), (Q2_y_Bin_3)-(z_pT_Bin_20)
(Q2_y_Bin_3)-(z_pT_Bin_21), (Q2_y_Bin_3)-(z_pT_Bin_22), (Q2_y_Bin_3)-(z_pT_Bin_24)
(Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_7), (Q2_y_Bin_3)-(z_pT_Bin_8), (Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_14), (Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_20), (Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_26)
(Q2_y_Bin_4)-(z_pT_Bin_27), (Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission]
(Q2_y_Bin_5)-(z_pT_Bin_10), (Q2_y_Bin_5)-(z_pT_Bin_13), (Q2_y_Bin_5)-(z_pT_Bin_15)
(Q2_y_Bin_5)-(z_pT_Bin_19), (Q2_y_Bin_5)-(z_pT_Bin_3), (Q2_y_Bin_5)-(z_pT_Bin_31)
(Q2_y_Bin_5)-(z_pT_Bin_32), (Q2_y_Bin_5)-(z_pT_Bin_4), (Q2_y_Bin_5)-(z_pT_Bin_5)
(Q2_y_Bin_5)-(z_pT_Bin_6), (Q2_y_Bin_6)-(z_pT_Bin_1), (Q2_y_Bin_6)-(z_pT_Bin_14)
(Q2_y_Bin_6)-(z_pT_Bin_2), (Q2_y_Bin_6)-(z_pT_Bin_20), (Q2_y_Bin_6)-(z_pT_Bin_26)
(Q2_y_Bin_6)-(z_pT_Bin_27), (Q2_y_Bin_6)-(z_pT_Bin_3), (Q2_y_Bin_6)-(z_pT_Bin_4)
(Q2_y_Bin_6)-(z_pT_Bin_5), (Q2_y_Bin_6)-(z_pT_Bin_6), (Q2_y_Bin_6)-(z_pT_Bin_7)
(Q2_y_Bin_6)-(z_pT_Bin_8), (Q2_y_Bin_6)-(z_pT_Bin_9), (Q2_y_Bin_7)-(z_pT_Bin_1)
(Q2_y_Bin_7)-(z_pT_Bin_10), (Q2_y_Bin_7)-(z_pT_Bin_11), (Q2_y_Bin_7)-(z_pT_Bin_12)
(Q2_y_Bin_7)-(z_pT_Bin_13), (Q2_y_Bin_7)-(z_pT_Bin_2), (Q2_y_Bin_7)-(z_pT_Bin_21)
(Q2_y_Bin_7)-(z_pT_Bin_24), (Q2_y_Bin_7)-(z_pT_Bin_27), (Q2_y_Bin_7)-(z_pT_Bin_31)
(Q2_y_Bin_7)-(z_pT_Bin_34), (Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_7)-(z_pT_Bin_7)
(Q2_y_Bin_7)-(z_pT_Bin_9), (Q2_y_Bin_8)-(z_pT_Bin_11), (Q2_y_Bin_8)-(z_pT_Bin_13)
(Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16), (Q2_y_Bin_8)-(z_pT_Bin_19)
(Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_21), (Q2_y_Bin_8)-(z_pT_Bin_28)
(Q2_y_Bin_8)-(z_pT_Bin_29), (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_9)-(z_pT_Bin_2)
(Q2_y_Bin_9)-(z_pT_Bin_3), (Q2_y_Bin_9)-(z_pT_Bin_4), (Q2_y_Bin_9)-(z_pT_Bin_8)

#### 150°

The rule does not fail every assessable manual exclusion: 1 of 52 pass.

Manually excluded but passes:

(Q2_y_Bin_6)-(z_pT_Bin_28)

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_10), (Q2_y_Bin_1)-(z_pT_Bin_16), (Q2_y_Bin_1)-(z_pT_Bin_30)
(Q2_y_Bin_1)-(z_pT_Bin_4), (Q2_y_Bin_1)-(z_pT_Bin_5), (Q2_y_Bin_1)-(z_pT_Bin_6)
(Q2_y_Bin_10)-(z_pT_Bin_2), (Q2_y_Bin_10)-(z_pT_Bin_3), (Q2_y_Bin_10)-(z_pT_Bin_32)
(Q2_y_Bin_10)-(z_pT_Bin_4), (Q2_y_Bin_10)-(z_pT_Bin_5), (Q2_y_Bin_10)-(z_pT_Bin_6)
(Q2_y_Bin_11)-(z_pT_Bin_2), (Q2_y_Bin_11)-(z_pT_Bin_22), (Q2_y_Bin_11)-(z_pT_Bin_23)
(Q2_y_Bin_11)-(z_pT_Bin_24), (Q2_y_Bin_11)-(z_pT_Bin_3), (Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_13)-(z_pT_Bin_1), (Q2_y_Bin_14)-(z_pT_Bin_5), (Q2_y_Bin_15)-(z_pT_Bin_15)
(Q2_y_Bin_15)-(z_pT_Bin_22), (Q2_y_Bin_15)-(z_pT_Bin_23), (Q2_y_Bin_15)-(z_pT_Bin_24)
(Q2_y_Bin_2)-(z_pT_Bin_1), (Q2_y_Bin_2)-(z_pT_Bin_10), (Q2_y_Bin_2)-(z_pT_Bin_13)
(Q2_y_Bin_2)-(z_pT_Bin_15), (Q2_y_Bin_2)-(z_pT_Bin_19), (Q2_y_Bin_2)-(z_pT_Bin_2)
(Q2_y_Bin_2)-(z_pT_Bin_20), (Q2_y_Bin_2)-(z_pT_Bin_25), (Q2_y_Bin_2)-(z_pT_Bin_3)
(Q2_y_Bin_2)-(z_pT_Bin_32), (Q2_y_Bin_2)-(z_pT_Bin_34), (Q2_y_Bin_2)-(z_pT_Bin_4)
(Q2_y_Bin_2)-(z_pT_Bin_5), (Q2_y_Bin_2)-(z_pT_Bin_6), (Q2_y_Bin_2)-(z_pT_Bin_7)
(Q2_y_Bin_2)-(z_pT_Bin_8), (Q2_y_Bin_2)-(z_pT_Bin_9), (Q2_y_Bin_3)-(z_pT_Bin_1)
(Q2_y_Bin_3)-(z_pT_Bin_11), (Q2_y_Bin_3)-(z_pT_Bin_12), (Q2_y_Bin_3)-(z_pT_Bin_13)
(Q2_y_Bin_3)-(z_pT_Bin_16), (Q2_y_Bin_3)-(z_pT_Bin_2), (Q2_y_Bin_3)-(z_pT_Bin_20)
(Q2_y_Bin_3)-(z_pT_Bin_21), (Q2_y_Bin_3)-(z_pT_Bin_24), (Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_7)
(Q2_y_Bin_3)-(z_pT_Bin_8), (Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_14)
(Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_26), (Q2_y_Bin_4)-(z_pT_Bin_27), (Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission], (Q2_y_Bin_5)-(z_pT_Bin_13), (Q2_y_Bin_5)-(z_pT_Bin_3)
(Q2_y_Bin_5)-(z_pT_Bin_31), (Q2_y_Bin_5)-(z_pT_Bin_32), (Q2_y_Bin_5)-(z_pT_Bin_4)
(Q2_y_Bin_5)-(z_pT_Bin_5), (Q2_y_Bin_5)-(z_pT_Bin_6), (Q2_y_Bin_6)-(z_pT_Bin_1)
(Q2_y_Bin_6)-(z_pT_Bin_14), (Q2_y_Bin_6)-(z_pT_Bin_2), (Q2_y_Bin_6)-(z_pT_Bin_26)
(Q2_y_Bin_6)-(z_pT_Bin_27), (Q2_y_Bin_6)-(z_pT_Bin_3), (Q2_y_Bin_6)-(z_pT_Bin_4)
(Q2_y_Bin_6)-(z_pT_Bin_5), (Q2_y_Bin_6)-(z_pT_Bin_7), (Q2_y_Bin_6)-(z_pT_Bin_9)
(Q2_y_Bin_7)-(z_pT_Bin_1), (Q2_y_Bin_7)-(z_pT_Bin_11), (Q2_y_Bin_7)-(z_pT_Bin_12)
(Q2_y_Bin_7)-(z_pT_Bin_13), (Q2_y_Bin_7)-(z_pT_Bin_2), (Q2_y_Bin_7)-(z_pT_Bin_21)
(Q2_y_Bin_7)-(z_pT_Bin_24), (Q2_y_Bin_7)-(z_pT_Bin_31), (Q2_y_Bin_7)-(z_pT_Bin_34)
(Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_11), (Q2_y_Bin_8)-(z_pT_Bin_13)
(Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16), (Q2_y_Bin_8)-(z_pT_Bin_19)
(Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_21), (Q2_y_Bin_8)-(z_pT_Bin_28)
(Q2_y_Bin_8)-(z_pT_Bin_29), (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_9)-(z_pT_Bin_2)
(Q2_y_Bin_9)-(z_pT_Bin_3), (Q2_y_Bin_9)-(z_pT_Bin_4)

#### 180°

The rule does not fail every assessable manual exclusion: 12 of 52 pass.

Manually excluded but passes:

(Q2_y_Bin_1)-(z_pT_Bin_22), (Q2_y_Bin_15)-(z_pT_Bin_1), (Q2_y_Bin_15)-(z_pT_Bin_2)
(Q2_y_Bin_2)-(z_pT_Bin_14), (Q2_y_Bin_3)-(z_pT_Bin_15), (Q2_y_Bin_3)-(z_pT_Bin_9)
(Q2_y_Bin_5)-(z_pT_Bin_14), (Q2_y_Bin_5)-(z_pT_Bin_25), (Q2_y_Bin_5)-(z_pT_Bin_8)
(Q2_y_Bin_5)-(z_pT_Bin_9), (Q2_y_Bin_6)-(z_pT_Bin_28), (Q2_y_Bin_9)-(z_pT_Bin_29)

Not manually excluded but fails:

(Q2_y_Bin_1)-(z_pT_Bin_30), (Q2_y_Bin_1)-(z_pT_Bin_4), (Q2_y_Bin_10)-(z_pT_Bin_6)
(Q2_y_Bin_11)-(z_pT_Bin_22), (Q2_y_Bin_11)-(z_pT_Bin_23), (Q2_y_Bin_11)-(z_pT_Bin_24)
(Q2_y_Bin_11)-(z_pT_Bin_3), (Q2_y_Bin_12)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_14)-(z_pT_Bin_5)
(Q2_y_Bin_15)-(z_pT_Bin_15), (Q2_y_Bin_15)-(z_pT_Bin_24), (Q2_y_Bin_2)-(z_pT_Bin_1)
(Q2_y_Bin_2)-(z_pT_Bin_2), (Q2_y_Bin_2)-(z_pT_Bin_20), (Q2_y_Bin_2)-(z_pT_Bin_3)
(Q2_y_Bin_2)-(z_pT_Bin_4), (Q2_y_Bin_2)-(z_pT_Bin_5), (Q2_y_Bin_2)-(z_pT_Bin_6)
(Q2_y_Bin_2)-(z_pT_Bin_7), (Q2_y_Bin_3)-(z_pT_Bin_1), (Q2_y_Bin_3)-(z_pT_Bin_13)
(Q2_y_Bin_3)-(z_pT_Bin_2), (Q2_y_Bin_3)-(z_pT_Bin_20), (Q2_y_Bin_3)-(z_pT_Bin_24)
(Q2_y_Bin_3)-(z_pT_Bin_25) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_26) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_27) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_28) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_3)-(z_pT_Bin_5) [fit-quality omission]
(Q2_y_Bin_3)-(z_pT_Bin_7), (Q2_y_Bin_4)-(z_pT_Bin_10) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_16) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_17) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_23) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_27)
(Q2_y_Bin_4)-(z_pT_Bin_29) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_31) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_32) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_34) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_7) [fit-quality omission]
(Q2_y_Bin_4)-(z_pT_Bin_8) [fit-quality omission], (Q2_y_Bin_4)-(z_pT_Bin_9) [fit-quality omission], (Q2_y_Bin_5)-(z_pT_Bin_3)
(Q2_y_Bin_5)-(z_pT_Bin_31), (Q2_y_Bin_5)-(z_pT_Bin_4), (Q2_y_Bin_5)-(z_pT_Bin_5)
(Q2_y_Bin_6)-(z_pT_Bin_26), (Q2_y_Bin_7)-(z_pT_Bin_12), (Q2_y_Bin_7)-(z_pT_Bin_31)
(Q2_y_Bin_7)-(z_pT_Bin_34), (Q2_y_Bin_7)-(z_pT_Bin_4) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_11)
(Q2_y_Bin_8)-(z_pT_Bin_14) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_16), (Q2_y_Bin_8)-(z_pT_Bin_19)
(Q2_y_Bin_8)-(z_pT_Bin_20) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_29), (Q2_y_Bin_8)-(z_pT_Bin_31) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_32) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_33) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_34) [fit-quality omission]
(Q2_y_Bin_8)-(z_pT_Bin_6) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_7) [fit-quality omission], (Q2_y_Bin_8)-(z_pT_Bin_8) [fit-quality omission]
(Q2_y_Bin_9)-(z_pT_Bin_2), (Q2_y_Bin_9)-(z_pT_Bin_3)

## Monotonicity

For every nominal input and every variation, the failure count does not increase as the allowed missing coverage increases from 90° to 180°.
