# Agent record
- run_id: 20261101T184840
- stage: nominal_rc
- campaign: both
- source_or_shard: nominal
- label: rc

Stage B wrote nominal RC_Bayesian histograms from the acceptance-corrected nominals, then refined those fits. The radiative study stays pending. That alternative was not fabricated, EvGen was not started, and RC_Cross_Section_Scan_Outputs_Final.root was not used. RC_Factors_ifarm_rc.root is on disk, so the pending study did not block this nominal file. BC was not applied. The fits did not pass --Apply_RC or --Apply_BC.

Resolved scope is 3D only. Each corrected/<campaign>/rc/corrected.root was rewritten by apply_nominal_corrections.py --stage rc from Sys3D_nominal_only_20261030_inherited_Unweighted.root and Sys3D_nominal_only_20261030_inherited_Spline.root, not from a BC file. correction_report.json records 452 histograms and 0 problems for each campaign. The files contain (MultiDim_3D_Histo)_(RC_Bayesian)_ only. Bayesian, BC_RC_Bayesian, Bin, and 5D are absent and were not created.

Start mode is manual. Error source is histogram. Publication is off. The universal 3D RC spline windows have median B width 0.013, so --use_spline_init was not used. The shared manual initializer was not edited.

The first remake returned 0 for both campaigns. That return code was the initial fit, not a finished refinement. Overlays were compared with an unconstrained cosine. Unweighted edits were (3,16) 5.487 to 1.443, (3,29) 4.173 to 2.965, (10,11) 2.666 to 1.673, (11,20) 2.604 to 1.938, (14,5) 3.643 to 2.499, and (15,15) 2.739 to 1.134, remade for Q2-y 3, 10, 11, 14, and 15. Spline edits were (13,4) 11.607 to 2.580, (3,29) 5.901 to 3.405, (3,16) 4.695 to 1.420, (14,5) 3.437 to 2.252, (11,20) 3.015 to 2.440, (10,11) 2.643 to 1.575, (15,15) 2.552 to 1.241, and (4,33) 2.212 to 0.812, remade for Q2-y 3, 4, 10, 11, 13, 14, and 15. The after overlays follow the histograms. Sibling cells and the Q2-y bins that were not remade did not move. Each JSON still has 452 Fit_Pars_from_3D_RC_Bayesian cells. No hard failures and no empty histograms.

Left because the histogram is flat while a neighbor is not: unweighted (1,15) beside (1,14), and spline (5,19) beside (5,18). Spline (3,24) keeps the smoother curve because two points pull the free cosine off the rest of the histogram. Unweighted (1,5) and (5,31), and spline (1,5), (1,16), (1,22), and (5,31), already follow the points. Spline (13,10) keeps the modulation the points support. Unresolved high chi2/NDF remains where the cosine already matches the histogram, including (1,32) and (1,7) in both campaigns and spline (13,10).

Notes are corrected/unweighted/rc/refinement_note.json and corrected/spline/rc/refinement_note.json.
