# Agent record
- run_id: 20261101T184840
- stage: kt2
- campaign: both
- source_or_shard: nominal
- label: kt2

uncertainty_campaign was empty, so Unweighted and Spline were extracted separately and were not merged. Each campaign had one invocation with --uncertainty_source systematic. There was no statistical fit in the same invocation and no variation refit.

normalized_bc.json was absent, so write_normalized_results.py wrote it from corrected/<campaign>/bc/fit.json and the provisional acceptance budget. The older corrected/<campaign>/normalized.json was not the input and was not replaced. Both new files have normalization_status applied, systematic_scope provisional_acceptance_level, 452 Fit_Pars_from_3D_BC_RC_Bayesian cells, Fit_Par_A_SYS on every cell, provisional_systematic true, and unassigned_factor_uncertainty true. The source-fit fingerprint matches the BC fit. Bin 1-1 A0 equals that BC Fit_Par_A divided by bin area times luminosity times Gamma_gamma. B and C were not rescaled. --already_normalized was set, so Fit_Par_A was not divided again. The fit weights are Fit_Par_A_SYS. That uncertainty is not a cross-bin systematic covariance. It is the provisional acceptance-level budget, not the complete final systematic.

physics_campaign/kt2/<campaign>/kt2_results.tsv was already present, so each run wrote a timestamped subdirectory and left the parent tables in place. Those parent tables are the 2026-11-01 extraction from normalized.json. Ninety of 91 slopes differ from that parent table.

Unweighted wrote physics_campaign/kt2/unweighted/run_20261102_152727. rows=91, points=452, used=452, excluded=0. Status strings: ok;log_uncertainty_large = 13 and ok;log_uncertainty_large;slope_consistent_with_zero = 78. The log line is rows=91 ok=91 poor=0 failed=0 near_zero=0 consistent_with_zero=78 positive_slope=0 large_ln_err=91. Log: physics_campaign/logs/kt2_unweighted_normalized_bc_systematic.log.

Spline wrote physics_campaign/kt2/spline/run_20261102_152727. rows=91, points=452, used=452, excluded=0. Status strings: ok;log_uncertainty_large = 11 and ok;log_uncertainty_large;slope_consistent_with_zero = 80. The log line is rows=91 ok=91 poor=0 failed=0 near_zero=0 consistent_with_zero=80 positive_slope=0 large_ln_err=91. Log: physics_campaign/logs/kt2_spline_normalized_bc_systematic.log.

Every z row has log_uncertainty_large because at least one used point has sigma_A/A greater than 0.5. Those points stayed in the fit. No kt2 value is blank. There is no positive slope and no near-zero slope. Most slopes are consistent with zero because the provisional systematic weights are large.

Each new directory has 17 fit PDFs, 51 summary PDFs, kt2_results.tsv, kt2_points.tsv, SCHEMA.txt, and uncertainty_source.txt. Each PDF starts with a PDF header. No kt2_review.pptx was requested. --validate_bin5 was not used. No phi_h refit, unfold, or farm job was started.
