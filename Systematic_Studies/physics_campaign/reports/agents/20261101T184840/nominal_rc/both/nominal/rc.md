# Agent record
- run_id: 20261101T184840
- stage: nominal_rc
- campaign: both
- source_or_shard: nominal
- label: rc

Stage B wrote nominal RC_Bayesian histograms from the acceptance-corrected nominals, then refined those fits. The radiative study stays pending. That alternative was not fabricated, EvGen was not started, and RC_Cross_Section_Scan_Outputs_Final.root was not used. The event-ratio file RC_Factors_ifarm_rc.root is verified, so the pending study did not block this nominal file. BC was not applied. The fits did not pass --Apply_RC or --Apply_BC.

Resolved scope is 3D only. Each corrected/<campaign>/rc/corrected.root has 452 (MultiDim_3D_Histo)_(RC_Bayesian)_ histograms and no Bayesian, BC_RC_Bayesian, Bin, or 5D histograms. Both inputs were the acceptance files, Sys3D_nominal_only_20261030_inherited_Unweighted.root and Sys3D_nominal_only_20261030_inherited_Spline.root, not a BC file. correction_report.json records 452 histograms and 0 problems for each campaign.

Start mode is manual. Error source is histogram. Publication is off. The universal 3D RC spline windows have median B width 0.013, and 447 of 452 acceptance B or C values fall outside them, so --use_spline_init was not used. The shared manual initializer was not edited.

The first remake returned 0 for both campaigns. That return code was the initial fit, not a finished refinement. Overlays showed stored curves that were too flat, or the wrong cos 2phi sign, where an unconstrained cosine follows the points. Unweighted edits were (3,16), (15,15), (3,29), and (11,20), remade for Q2-y 3, 11, and 15. Spline edits were (13,4), (3,16), (3,29), (4,33), (15,15), (14,5), and (10,11), remade for Q2-y 3, 4, 10, 11, 13, 14, and 15. Every edited bin improved and now lies on that cosine. The largest drops were spline (13,4) 11.61 to 2.58 and unweighted (3,16) 5.49 to 1.44. Sibling cells and the Q2-y bins that were not remade did not move. Each JSON still has 452 Fit_Pars_from_3D_RC_Bayesian cells. No hard failures and no empty histograms.

Left because the histogram is flat while a neighbor is not: unweighted (5,19), (10,13), (9,15), (6,13), and (1,15); spline (5,19), (10,13), (9,15), and (6,13). Spline (13,10) keeps the modulation the points support. Unresolved high chi2/NDF remains where the cosine already matches the histogram, including (1,32) and (1,7) in both campaigns and spline (13,10).

record_refinement for unweighted|nominal|RC_Bayesian and spline|nominal|RC_Bayesian is completed. Notes are corrected/unweighted/rc/refinement_note.json and corrected/spline/rc/refinement_note.json.
