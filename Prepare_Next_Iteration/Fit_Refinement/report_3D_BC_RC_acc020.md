# 3D BC+RC acc020 fit review

Date: 26 October 2026. The next Monte Carlo production, response-matrix generation, and unfolding were not run.

## Input and family

ROOT file, updated in place:

`Unfolded_Simple_3D_Final_Thesis_Bank_rho0_new_acc020_Zeroth_Order_Full.root`

JSON:

`Fit_Pars_from_Simple_RooUnfold_SelfContained_using_Unfolded_Simple_3D_Final_Thesis_Bank_rho0_new_acc020_Zeroth_Order_Full.json`

Only `Fit_Pars_from_3D_BC_RC_Bayesian` was refit. The fit is `A (1 + B cos φ_h + C cos 2φ_h)` with histogram uncertainties and spline initialization. Acceptance-only, RC-only, and 5D results were not refit. The file still holds 452 φ_h histograms in each of Bayesian, RC_Bayesian, and BC_RC_Bayesian. Fit objects exist only for BC_RC (452).

## Iterations and fit quality

Two passes.

1. Full remake of all 452 BC+RC bins.
2. Q²-y bin 9 only, after one tagged guide.

The only guide edit is `("9", "32", "3D", "BC")` in `Prepare_Next_Iteration/Phi_h_Fit_Parameters_from_Spline.py`. The manual initializer was not changed. Before that guide, bin (9, 32) had B = −0.046 and χ²/NDF = 7.09. After it, B = −0.137, C = −0.005, χ² = 32.64, NDF = 21, χ²/NDF = 1.554.

Final sample: 452 bins, 0 failed, 0 excluded from the spline.

- Median χ²/NDF = 1.087
- 95th percentile = 2.18
- 5 bins above 3, none above 5

Bins left above 3:

| Q²-y | z-pT | χ²/NDF | B | C |
| --- | --- | --- | --- | --- |
| 1 | 32 | 3.85 | −0.137 | 0.002 |
| 3 | 29 | 3.73 | −0.167 | 0.008 |
| 12 | 24 | 3.72 | −0.103 | −0.007 |
| 10 | 17 | 3.52 | −0.133 | 0.005 |
| 1 | 26 | 3.07 | −0.165 | 0.039 |

(1, 32) and (1, 26) are single high bins at the edge of φ_h. The other three are elevated and still follow the histogram. No further guide was added.

## Corrections and normalization

The stored BC+RC histogram already includes 3D Bayesian unfolding, radiative corrections, and bin-centering corrections. The fit was run on that histogram. `--Apply_RC`, `--Apply_BC`, and `--CrossSection_Norm` were not used. The φ_h figures show this native histogram and its TF1.

Spline A, and only A, is then divided by bin area × luminosity × virtual-photon flux. B and C are not rescaled. A is stored as log(A). Luminosity uses the charge summary with the Klimenko beam-blocker and tracking correction on, and the current target density 0.07151 g/cm³.

Checked against `Cross_Section_Normalization`: for every one of the 452 bins, the stored spline A equals the fit A divided by that product (ratio 1). For Q²-y 9, z-pT 32 the factors are bin area 0.00384, luminosity 4.582×10¹⁰ μb⁻¹ with the beam correction and 4.670×10¹⁰ without it (ratio 0.981), and Γ_γ = 4.00×10⁻⁴.

The July 2026 5D weight file does not divide by Γ_γ. Its A matches fit A / (bin area × luminosity) up to one flat factor, 1.020114, which is 0.07151 / 0.0701, the target-density update of 11 August 2026. That factor does not depend on kinematics.

## Spline products

New files, not overwrites of the 5D products, all under `Prepare_Next_Iteration/`:

- `acc020_3D_BC_RC_4D_xB_Fit_Pars_from_3D_BC_RC_Bayesian_Compute_SplineWeight.txt`
- `acc020_3D_BC_RC_4D_xB_Fit_Pars_from_3D_BC_RC_Bayesian_Fit_Par_A.npz` and `.pkl`
- the same pattern for B and C

Mode `4D_xB`. Signature `ComputeSplineWeight(Q2, xB, y, z, pT, phi_h)`. 452 training points. A uses a thin-plate kernel in log space. B and C use a gaussian kernel. The C++ evaluator is the file the reweighting code calls.

## Figures

`Comparison_Between_GEN_and_Unfold.py` was not used. That script is a generated-versus-unfolded campaign and its correction flags would apply luminosity, flux, and bin volume on top of histograms that already contain unfolding, RC, and BC.

The φ_h figures are the stored histograms with the fitted curves, one PDF per Q²-y bin:

`Prepare_Next_Iteration/Fit_Refinement/plots/3D_BC_RC_acc020_review/phi_h_pdf/`

17 PDFs, 452 pages, written after the (9, 32) refit.

Comparison plots and the matched-bin table:

`Prepare_Next_Iteration/Fit_Refinement/plots/3D_BC_RC_acc020_review/comparison/`

Review deck, new file:

`Prepare_Next_Iteration/Fit_Refinement/plots/3D_BC_RC_acc020_review/3D_BC_RC_acc020_Final_Review.pptx`

## 5D comparison

The nominal file is the one named by the reweighting and response-matrix defaults:

`Prepare_Next_Iteration/rho0_Subtracted_5D_V2_4D_xB_Fit_Pars_from_5D_BC_RC_Bayesian_Compute_SplineWeight.txt`

It was not modified. 5D parameter errors used for scale come from `Fit_Pars_from_Simple_RooUnfold_SelfContained_using_Hybrid_Unfolded_5D_and_3D_Histos_From_Dedicated_5D_Unfold.json`, whose B values match 425 of the 5D training points.

421 bin centers are shared. 31 3D bins and 48 5D bins have no partner and are excluded. The two results are related reductions of the same measurement, so a ratio of their difference to the combined uncertainty is a scale, not a significance.

Fit parameters, 3D minus 5D, on the 421 shared bins:

- B: median difference −0.005, median absolute 0.012, 95th percentile absolute 0.039, maximum 0.088. 3.1% of bins exceed 0.05. None exceed 0.10.
- C: median difference −0.004, median absolute 0.008, 95th percentile absolute 0.033, maximum 0.068. 0.7% exceed 0.05. None exceed 0.10.
- Where |B_5D| > 0.05 (252 bins), the median absolute relative difference is 5.5%.

The smoothed weight functions move less: median |ΔB| = 0.0067 and median |ΔC| = 0.0048. The largest change in `1 + B cos φ + C cos 2φ`, maximized over φ, has median 0.012 and 95th percentile 0.032.

Largest |ΔB| parameters: (2, 6) +0.088 at high z and pT, then (10, 2) +0.075, (3, 24) +0.075, and (8, 20) −0.073. Largest |ΔC|: (3, 24) −0.068, (9, 9) −0.058, (14, 15) +0.051. By Q²-y, the smoothed |ΔB| medians are a little larger in bins 8, 11, 12, and 15 (0.014 to 0.018) and small everywhere else. The change is broad, with a few edge bins on top.

A is not comparable until the photon flux is removed. Median (A_3D / A_5D) × Γ_γ = 0.976 for the evaluated splines (16th percentile 0.937, 84th 1.063, 95th 1.33, maximum 2.10). At φ_h = 0 the raw weight ratio W_3D / W_5D has median 1804 and 95th percentile 7451, because the new A is divided by Γ_γ ≈ 5×10⁻⁴ and the July A is not. After that factor is removed, the median relative weight change at φ_h = 0 is −3.3% (median absolute 4.9%, 95th percentile absolute 31%).

## Downstream defaults

The new spline file has the same function signature, coordinate mode, and A/B/C layout as the July file. It is not weight-compatible. Pointing the defaults at it would multiply event weights by a Q²- and y-dependent factor of order 10³.

These defaults were left on the July 5D file:

- `jlab_work_paths.py` (`REL_SPLINE_DEFAULT`)
- `Histo_Files_ROOT/DataFrames/Acceptance_Weights_Creations_using_RDataFrames.py`
- `Histo_Files_ROOT/DataFrames/Submit_Full_Histogram_Creation_Pipeline.py`
- `Histo_Files_ROOT/DataFrames/Response_Matrix_Creation_using_RDataFrames.py`
- `Histo_Files_ROOT/DataFrames/run_sidis_DataFrame_pipeline.py`
- `Campaign/local_orchestrator.py`
- `evaluate_spline_reference.py`

Historical SLURM scripts were not rewritten. A 3D file can become the nominal weight after it is built with the July A convention (bin area × luminosity, no photon flux), or after the consumer is changed to expect the flux division. The file generated here is the cross-section spline.

## Not run

Monte Carlo generation, response matrices, unfolding, radiative corrections, bin-centering, and the next analysis iteration were not started.
