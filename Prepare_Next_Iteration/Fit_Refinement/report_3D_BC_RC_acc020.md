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

This section records the decision at the end of the fit campaign. The follow-up below replaces the nominal weight file with the raw-A 3D spline.

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

## Follow-up: raw-A spline

The 452 φ_h fits, their ROOT objects, the fit JSON, and the normalized spline family were left in place. No histogram was refit.

A second spline family was built from `Fit_Pars_from_3D_BC_RC_Bayesian` with the same `4D_xB` settings and `--log_A`, and without `--apply_A_corr`. B and C `.npz` files in this family are byte-identical to the existing 3D B and C models. The C++ weight file was rebuilt from that raw A plus those copied B and C models.

Raw-A products, under `Prepare_Next_Iteration/`:

- `acc020_3D_BC_RC_rawA_4D_xB_Fit_Pars_from_3D_BC_RC_Bayesian_Compute_SplineWeight.txt`
- `acc020_3D_BC_RC_rawA_4D_xB_Fit_Pars_from_3D_BC_RC_Bayesian_Fit_Par_A.npz` and `.pkl`
- the B and C `.npz` and `.pkl` copies beside them

The normalized family `acc020_3D_BC_RC_4D_xB_...` and the July 5D file were not overwritten.

At all 452 training centers, the raw-A spline was divided by bin area × luminosity × Γ_γ, with beam-blocker and tracking corrections on, and compared with the spline that was fit to already-normalized A. Every bin was above the relative floor (2% of the median |A|). Median signed difference −0.35%. Median absolute difference 10.5%. The 16th and 84th percentiles are −15% and +17%. The 95th percentile of the absolute difference is 42%, and the maximum is +79% at Q²-y 8, z-pT 24. The raw spline itself tracks the JSON amplitudes (median ratio 0.994). The extra spread is the log-space interpolant of A versus the log-space interpolant of A divided by a bin-dependent scale. Both fits are kept.

Figures:

- `Prepare_Next_Iteration/Fit_Refinement/plots/3D_BC_RC_acc020_review/rawA_comparison/`
- Mosaics in `Prepare_Next_Iteration/Fit_Refinement/plots/3D_BC_RC_acc020_review/mosaic/`: `acc020_normA_3D_BayesianUnfold_BC_RC_z_NormalizedA.pdf`, `acc020_rawA_3D_BayesianUnfold_BC_RC_z_Amplitude.pdf`, `acc020_B_3D_BayesianUnfold_BC_RC_z_CosPhiMoment.pdf`, `acc020_C_3D_BayesianUnfold_BC_RC_z_Cos2PhiMoment.pdf`

Six slides were appended to `3D_BC_RC_acc020_Final_Review.pptx` (now 490 slides). The earlier 484 slides were not rebuilt.

The event weight is `ComputeSplineWeight(Q2, xB, y, z, pT, phi_h)` with `4D_xB` coordinates and log-space A. The raw-A file evaluates to a finite weight and returns the fit amplitude, not the flux-divided amplitude. That is the intended Monte Carlo convention. The July 5D absolute scale is only a historical reference.

These defaults now name the raw-A file. The previous 5D path is the commented line above each one:

- `jlab_work_paths.py`
- `Histo_Files_ROOT/DataFrames/Acceptance_Weights_Creations_using_RDataFrames.py`
- `Histo_Files_ROOT/DataFrames/Submit_Full_Histogram_Creation_Pipeline.py`
- `Histo_Files_ROOT/DataFrames/Response_Matrix_Creation_using_RDataFrames.py`
- `Histo_Files_ROOT/DataFrames/run_sidis_DataFrame_pipeline.py`
- `Campaign/local_orchestrator.py`
- `evaluate_spline_reference.py`

Historical SLURM scripts were not rewritten. The normalized 3D file remains the cross-section spline. Monte Carlo generation, response matrices, and unfolding were not started. The raw-A file still has to be present at the ifarm path named in those defaults before a farm job can read it.
