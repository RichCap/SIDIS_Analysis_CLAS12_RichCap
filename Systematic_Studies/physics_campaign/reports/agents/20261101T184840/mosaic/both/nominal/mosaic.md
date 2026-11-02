# Agent record
- run_id: 20261101T184840
- stage: mosaic
- campaign: both
- source_or_shard: nominal
- label: mosaic

uncertainty_campaign was empty, so Unweighted and Spline were written as separate mosaics and were not merged. normalized_bc.json is absent for both campaigns, so the older corrected/<campaign>/normalized.json was used and was not refused. Both files have normalization_status applied, 452 Fit_Pars_from_3D_BC_RC_Bayesian bins, provisional_systematic true, and unassigned_factor_uncertainty true. Their mtime is 2026-11-01 01:55:04. Every plotted bin has Fit_Par_A/B/C_ERR and Fit_Par_A/B/C_SYS, so the systematic figures were not refused. A cell dict missing Fit_Par_A_SYS raises "systematic mosaic is missing _SYS entries" and is not drawn. corrected/<campaign>/fit.json and corrected/<campaign>/bc/fit.json have no normalization_status and no Fit_Par_*_SYS. mosaic_command raises "mosaic requires normalization_status applied" for both, including the 2026-11-02 15:17 BC fits. Those files were not drawn, and the A0 scale was not applied again. normalized_bc.json was not written.

Printed and ran six commands per campaign, statistical and systematic for z, pt, and pt2. Statistical uses --err_suffix _ERR. Systematic uses --err_suffix _SYS. None of the commands pass --apply_A_corr, -cs, or --sys_err_suffix. All pass --draw_with_log_A, --pad_label_mode bin_Q2y, and --draw_legends. pt2 uses --x_mode pt --pT2. No preliminary watermark.

spline_overlay is yes. The plotter loads {prefix}_4D_xB_Fit_Pars_from_3D_BC_RC_Bayesian_Fit_Par_{A,B,C}.pkl. The prefix is Prepare_Next_Iteration/acc020_3D_BC_RC_rawA, which resolves to the acc020 rawA 4D_xB pickles. The library SPLINE_PREFIX already includes the dimension and fit-set name and does not match those files, so it was not passed. No log reported a missing spline. Curves are the 200-point evaluated spline from build_spline_graph, line width 2, not a polyline through the points. The global title stays centered (align 23, title_x 0.50, title_size 0.032).

Each command returned 0 and wrote three PDFs (A, B, and C). The 36 files are in physics_campaign/mosaics, named sidis_mosaic_<campaign>_<z|pt|pt2>_<statistical|systematic>_3D_BayesianUnfold_BC_*.pdf, each with a %PDF header and mtime 2026-11-02 15:23. Logs are physics_campaign/logs/mosaic_<campaign>_<x>_<uncertainty>.log. Each log names the normalized.json path and three created PDFs. No fit, unfold, or farm job was started.
