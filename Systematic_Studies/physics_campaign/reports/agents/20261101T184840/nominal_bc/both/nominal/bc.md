# Agent record
- run_id: 20261101T184840
- stage: nominal_bc
- campaign: both
- source_or_shard: nominal
- label: bc

Stage C wrote nominal BC_RC_Bayesian histograms from the Stage B RC files, then refined those fits. The input for each campaign was corrected/<campaign>/rc/corrected.root, not the acceptance file and not another BC variation. apply_nominal_corrections.py --stage bc applied the nominal 2026-10-26 BC JSON once. correction_report.json records 452 histograms and 0 problems for each campaign. A sampled spline ratio of RC content to BC content matches BC_Factor on 47 nonzero bins. The fits did not pass --Apply_BC or --Apply_RC.

Alternative BC factors, including the 15 subdivision settings, were not applied. Those alternatives use that same RC file. Their fitted observable shifts are still missing, so they did not block this nominal fit. The subdivision source stays one pooled RMS of 15 observable shifts, N=15, for Unweighted only. It is not five quadrature terms, not a factor-difference substitute, not zero, and not copied into Spline.

Resolved scope is 3D only. Each corrected/<campaign>/bc/corrected.root has 452 (MultiDim_3D_Histo)_(BC_RC_Bayesian)_ histograms and no Bayesian, RC_Bayesian, Bin, or 5D histograms.

Start mode is spline. The keys that actually apply to BC_RC histograms have median B width 0.17, and only 47 unweighted and 54 spline RC B or C values fall outside them. That is not the tight 3D RC window (median B width 0.013) that pinned Stage B, so the first remake passed --use_spline_init. Error source is histogram. Publication is off. The shared spline initializer and the manual initializer were not edited.

The first remake returned 0 for both campaigns. That return code was the initial fit, not a finished refinement. Overlays showed stored curves that were too flat, or the wrong cos 2phi sign, where an unconstrained cosine follows the points. Unweighted edits were (3,16), (3,24), (3,29), (10,2), (10,11), (10,17), (11,3), (11,20), (14,15), and (15,15), remade for Q2-y 3, 10, 11, 14, and 15. Spline edits were (13,4), (3,16), (3,24), (3,29), (4,33), (10,2), (10,11), (11,20), and (15,15), remade for Q2-y 3, 4, 10, 11, 13, and 15. (15,15) and (3,29) had C pinned by the guide in both campaigns. Every edited bin improved and now lies on that cosine. The largest drops were spline (13,4) 5.88 to 1.29 and unweighted (3,29) 3.73 to 2.45. Sibling cells and the Q2-y bins that were not remade did not move. Each JSON still has 452 Fit_Pars_from_3D_BC_RC_Bayesian cells. No hard failures and no empty histograms.

Left because the histogram is flat while a neighbor is not: unweighted (5,19), (10,13), (9,15), (6,13), and (1,15); spline (5,19), (10,13), (9,15), and (6,13). Spline (13,10) keeps the modulation the points support. Smaller shifts were not applied where both curves already follow the points, including unweighted (2,29) and spline (1,22) and (5,7). Unresolved high chi2/NDF remains where the cosine already matches the histogram, including (1,32) and (12,24) in both campaigns and (1,7).

record_refinement for unweighted|nominal|BC_RC_Bayesian and spline|nominal|BC_RC_Bayesian is completed. Notes are corrected/unweighted/bc/refinement_note.json and corrected/spline/bc/refinement_note.json.
