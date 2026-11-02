# Agent record
- run_id: 20261101T184840
- stage: mosaic
- campaign: both
- source_or_shard: nominal
- label: mosaic

uncertainty_campaign was empty, so Unweighted and Spline were written as separate mosaics and were not merged. corrected/spline/fit.json has no normalization_status and was refused (mosaic requires normalization_status applied). Both corrected/<campaign>/normalized.json files have normalization_status applied, 452 Fit_Pars_from_3D_BC_RC_Bayesian bins, provisional_systematic true, and unassigned_factor_uncertainty true. Every plotted bin has Fit_Par_A/B/C_ERR and Fit_Par_A/B/C_SYS, so the systematic figures were not refused. A copy with one Fit_Par_A_SYS removed raises "systematic mosaic is missing _SYS entries" and is not drawn.

Printed and ran six commands per campaign, statistical and systematic for z, pt, and pt2. Statistical uses --err_suffix _ERR. Systematic uses --err_suffix _SYS. None of the commands pass --apply_A_corr, -cs, or --sys_err_suffix. All pass --draw_with_log_A, --pad_label_mode bin_Q2y, and --draw_legends. pt2 uses --x_mode pt --pT2. No preliminary watermark. The A0 scale was not applied again.

spline_overlay is yes. The plotter loads {prefix}_4D_xB_Fit_Pars_from_3D_BC_RC_Bayesian_Fit_Par_{A,B,C}.pkl, so the prefix is Prepare_Next_Iteration/acc020_3D_BC_RC_rawA. That resolves to the acc020 rawA 4D_xB pickles. The library SPLINE_PREFIX already includes the dimension and fit-set name and would miss those files. No log reported a missing spline. Curves are the 200-point evaluated spline, line width 2, not a polyline through the points. The global title stays centered (align 23, title_x 0.50, title_size 0.032).

Each command returned 0 and wrote three PDFs (A, B, and C). The 36 files are in physics_campaign/mosaics, named sidis_mosaic_<campaign>_<z|pt|pt2>_<statistical|systematic>_3D_BayesianUnfold_BC_*.pdf. Logs are physics_campaign/logs/mosaic_<campaign>_<x>_<uncertainty>.log. No fit, unfold, or farm job was started.
