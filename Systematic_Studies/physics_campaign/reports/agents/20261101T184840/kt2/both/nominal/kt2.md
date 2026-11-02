# Agent record
- run_id: 20261101T184840
- stage: kt2
- campaign: both
- source_or_shard: nominal
- label: kt2

uncertainty_campaign was empty, so Unweighted and Spline were extracted separately and were not merged. Each campaign had one invocation with --uncertainty_source systematic. There was no statistical fit in the same invocation and no variation refit. The input is the nominal normalized A0 only: corrected/<campaign>/normalized.json, collection Fit_Pars_from_3D_BC_RC_Bayesian. Both files have normalization_status applied, 452 cells, Fit_Par_A_SYS on every cell, provisional_systematic true, and unassigned_factor_uncertainty true. --already_normalized was set, so Fit_Par_A was not divided by the cross-section scale again. The fit weights are Fit_Par_A_SYS. That uncertainty is not a cross-bin systematic covariance.

physics_campaign/kt2/<campaign>/kt2_results.tsv was already present, so each run wrote a timestamped subdirectory and left the parent tables in place. The new kt2_results.tsv and kt2_points.tsv files are identical to those parent tables.

Unweighted returned 0. rows=91 ok=78 poor=13 failed=0 near_zero=0 consistent_with_zero=0 positive_slope=0 large_ln_err=0. Output: physics_campaign/kt2/unweighted/run_20261101_204000. Log: physics_campaign/logs/kt2_unweighted_systematic.log.

Spline returned 0. rows=91 ok=84 poor=7 failed=0 near_zero=0 consistent_with_zero=0 positive_slope=0 large_ln_err=0. Output: physics_campaign/kt2/spline/run_20261101_204001. Log: physics_campaign/logs/kt2_spline_systematic.log.

Each new directory has 17 fit PDFs, 51 summary PDFs, kt2_results.tsv, kt2_points.tsv, SCHEMA.txt, and uncertainty_source.txt. No kt2_review.pptx was requested. --validate_bin5 was not used. No phi_h refit, unfold, or farm job was started.
