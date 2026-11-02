# Agent record
- run_id: 20261101T184840
- stage: nominal_bc
- campaign: both
- source_or_shard: nominal
- label: bc

Stage C wrote nominal BC_RC_Bayesian histograms from the Stage B RC files, then refined those fits. The previous BC notes were not reused: corrected/<campaign>/rc/corrected.root was rewritten on 2026-11-02 after those notes. The input for each campaign was that RC file, not the acceptance file and not another BC variation. apply_nominal_corrections.py --stage bc applied the nominal 2026-10-26 event BC JSON once. That JSON was not replaced by a spline-BC table; its size, mtime, and sha256 are unchanged. correction_report.json records 452 histograms and 0 problems for each campaign. A check of 40 histograms in each campaign matched RC content divided by BC_Factor with no residual. The fits did not pass --Apply_BC or --Apply_RC.

Alternative BC factors, including the 15 subdivision settings, were not applied. Those alternatives use that same RC file. Their fitted observable shifts are still missing, so they did not block this nominal fit. The subdivision source stays one pooled RMS of 15 observable shifts, N=15, for Unweighted only. It is not five quadrature terms, not a factor-difference substitute, not zero, and not copied into Spline.

Resolved scope is 3D only. Each corrected/<campaign>/bc/corrected.root has 452 (MultiDim_3D_Histo)_(BC_RC_Bayesian)_ histograms and no Bayesian, RC_Bayesian, Bin, or 5D histograms.

Start mode is spline. The keys that apply to BC_RC histograms have median B width 0.17. That is not the tight 3D RC window, so the first remake passed --use_spline_init. Error source is histogram. Publication is off. The shared spline initializer and the manual initializer were not edited.

The first remake returned 0 for both campaigns. That return code was the initial fit, not a finished refinement. Overlays showed stored curves that were too flat, or the wrong cos 2phi sign, where an unconstrained cosine follows the points. (3,29), (15,15), and (11,20) had C trapped by the guide in both campaigns. Unweighted (1,9) had C pinned at zero. Unweighted edits were (10,17) 3.520 to 1.526, (14,15) 2.388 to 0.748, (3,29) 3.732 to 2.454, (15,15) 2.133 to 0.896, (10,2) 2.340 to 1.147, (10,11) 1.930 to 0.826, (11,3) 1.991 to 1.099, (3,24) 2.752 to 2.002, (3,16) 1.816 to 1.123, (11,20) 2.135 to 1.481, (1,9) 1.109 to 0.515, and (2,29) 1.480 to 1.039, remade for Q2-y 1, 2, 3, 10, 11, 14, and 15. Spline edits were (13,4) 5.878 to 1.291, (3,29) 5.290 to 2.777, (10,2) 3.447 to 1.949, (4,33) 2.036 to 0.778, (10,11) 1.991 to 0.817, (15,15) 2.013 to 0.988, (3,24) 3.366 to 2.373, (11,20) 2.431 to 1.850, and (3,16) 1.588 to 1.140, remade for Q2-y 3, 4, 10, 11, 13, and 15. Every edited bin improved, and the after overlays follow the histograms. Sibling cells and the Q2-y bins that were not remade did not move. Each JSON still has 452 Fit_Pars_from_3D_BC_RC_Bayesian cells. No hard failures and no empty histograms.

Left because the histogram is flat while a neighbor is not: unweighted (1,15), (5,19), (5,31), (6,13), (10,13), and (9,15); spline (5,19), (6,13), (10,13), and (9,15). Spline (13,10) keeps the modulation the points support. Smaller shifts were not applied where both curves already follow the points, including spline (4,34), (1,22), and (5,7). Unresolved high chi2/NDF remains where the cosine already matches the histogram, including (1,32) and (12,24) in both campaigns and (1,7).

record_refinement for unweighted|nominal|BC_RC_Bayesian and spline|nominal|BC_RC_Bayesian is verified. Notes are corrected/unweighted/bc/refinement_note.json and corrected/spline/bc/refinement_note.json.
