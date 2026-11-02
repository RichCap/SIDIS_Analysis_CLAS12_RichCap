# Agent record
- run_id: 20261101T184840
- stage: bin_centering
- campaign: both
- source_or_shard: status
- label: bin_centering

bc_spline_alternative was yes, so one read-only spline-BC call was made. A kinematic scan was not run. EvGen was not run.

correct.py -m BC -q 1 -z 1 -p 1 returned one object. Its fields were checked, not its exit status: ok is true, mode is BC, n_sub is 405, center_subbin is 203, and bc is 0.962648406941639 at Q2-y 1, z-pT 1, phi_h 1. That value is the unweighted mean of raw-amplitude sub-bin midpoint weights divided by the center sub-bin weight. It is not the nominal event-based BC factor and was not compared to it. It is not a systematic and was not copied into either quadrature sum. Provenance from that object: normalization_reference /Users/richardcapobianco/.grok/skills/sidis-bin-corrections/references/electroproduction-normalization.md; physics_configuration first-iteration raw-amplitude spline; normalization_convention raw_fit_amplitude; normalization_gamma not_applied. spline_file is the raw-amplitude text. Its header on disk is Dimension mode 4D_xB, Fit set Fit_Pars_from_3D_BC_RC_Bayesian, generated 10-26-2026 21:19:44, matching the object.

The event-versus-spline comparison stays not_combined. The method row is estimated_transfer, reference event_unweighted, alternative initial_spline, transfer_prescription user_decision, study_state blocked, systematic null. No scale factor was applied. No initial-spline correction file is configured, so the one-bin factor was not promoted to that comparison.

The event reference is the 2026-10-26 JSON. Its meta was read: num_sub_bins_q2, y, z, and pt are 3 and phi is 5. The written report has event_counts_match true.

Iteration comparison stays not_combined and blocked. systematic is null. The original injection spline, acc020_3D_BC_RC_rawA_4D_xB_Fit_Pars_from_3D_BC_RC_Bayesian_Compute_SplineWeight.txt, is the file named by jlab_work_paths.REL_SPLINE_DEFAULT and is verified on disk. Manifest later_spline path is null and path_status is needs_configuration. No configuration names a post-refit spline, so updated_spline stays needs_configuration and blocked. A missing later file was not treated as a zero shift.

The 15 subdivision files are five variables, q2, y, z, pt, and phi, with three settings each: 3, 5, and 7 for q2, y, z, and pt, and 5, 7, and 9 for phi. Each file's meta was read. The named count matches and every other count is 1. The written report has 15 verified rows. Their quoted source is one RMS of 15 observable shifts, N = 15, for Unweighted only, and only after each variation completes refine-phi-fits. No subdivision fit directory exists under physics_campaign/fits. budgets.json records shift_count 0, state awaiting_observable_shifts, entered_unweighted_quadrature false, substituted_zero false, and copied_into_spline false. The Spline source list does not contain bin_centering_subdivision. systematic stays null. A missing shift was not entered as zero. Factor differences were not used in its place. The five variable RMS values stay diagnostic and are not five quadrature terms. spline_transfer stays user_decision.

Direct evaluation at the same points stays deferred. Sub-bin contents were not reconstructed, generator weights were not removed, aggregated bins were not reweighted, Monte Carlo was not regenerated, and unfolding was not rerun.

Report: Systematic_Studies/physics_campaign/reports/bin_centering.json
