# Systematic-only width extraction

Input: corrected/spline/normalized_bc.json, normalization_status applied, Fit_Par_A_SYS.
That field matches budgets/rerun_refinement_20261108_coverage135/budget.json per_bin_sys A in all 452 cells, with maximum absolute difference 0.
No systematic value is zero, negative, or non-finite.
The quadrature of Fit_Par_A_ERR and Fit_Par_A_SYS differs from Fit_Par_A_SYS in all 452 bins.

Fit: ln A0 = b - P_T^2 / kappa, ROOT option SQN.
kt2_err is GetParError of kappa. It is not scaled by sqrt(chi2/ndf) and no slope uncertainty is added.
On ln A0 the point uncertainty is Fit_Par_A_SYS / A0.

Counts: 91 rows, 90 ok, 1 poor, 0 unsuccessful, 0 unreliable covariance, 1 large relative uncertainty, 0 negative widths, 0 linear disagreements, 0 excluded points.
All 452 points were used. Saved point errors agree with Fit_Par_A_SYS to 4.7e-10, which is the %.10g table precision. No saved point error matches the statistical field or the quadrature when those differ from the systematic field.

Linear check: |kappa + 1/a| <= max(1e-6 GeV^2, 1e-5 * max(|kappa|, |1/a|)).
The largest difference divided by that limit is 2.7e-4. No row needs a separate investigation.

Special rows:
- Q2-y 1, z 0.175: poor, chi2 4.180, ndf 2, covariance status 3, kappa 0.192 ± 0.025. Printed as an ordinary measurement.
- Q2-y 15, z 0.555: ok and large_relative_uncertainty, ndf 0, covariance status 3, kappa 0.217 ± 0.190. The uncertainty is at least half the width. The fit status is 0 and the covariance is accurate. It is marked and is not treated as a failed fit.

Central values run from 0.161 to 0.304 GeV^2 at three decimal places.

The JSON, the coverage135 budget, the nominal acceptance fit, and run_20261108_stat_only/kt2_results.tsv kept the hashes recorded before this run.
run_20261108_stat_only remains the earlier statistical-only extraction and was not used here.
