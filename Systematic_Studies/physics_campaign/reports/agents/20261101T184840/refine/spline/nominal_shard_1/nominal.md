# Agent record
- run_id: 20261101T184840
- stage: refine
- campaign: spline
- source_or_shard: nominal_shard_1
- label: nominal

Nominal shard 1 is the spline 3D Bayesian acceptance fit only. RC_Bayesian, BC_RC_Bayesian, and Bin are not in the file and were not created. There is no 5D family. Bin-by-bin was not selected and was not run with --unfolding_1D.

The shard command was python3 Systematic_Studies/sidis_physics_cli.py run_shard -p nominal -s 1 -w Systematic_Studies/physics_campaign/work_plan.json. It reused the existing fit and returned 0. That return code is the initial fit, not a finished refinement. No pass cap and no chi-squared stop were added. Nothing was unfolded and no farm job was submitted.

Start mode is manual. The universal spline B windows are tight (median width 0.019, 467 of 655 narrower than 0.05), so --use_spline_init was not used. Errors are histogram errors. Publication was not requested.

Overlays of the initial fit showed twenty-nine bins whose first-pass moment start was too small, or whose limits excluded the histogram cosine. The second pass only moves a parameter halfway from that start, so A(1 + B cos phi + C cos 2phi) missed the modulation. Those starts were moved onto the cosine and the excluding limits were opened in refine_init.py. The shared manual initializer and the universal spline file were not edited. The guide remake was 3D Bayesian for Q2-y 1, 2, 6, 7, 13, 15, and 16, with --fit_error_source histogram and --fit_init_file.

All twenty-nine bins improved, and the nine bins refit in this pass moved onto the cosine: (13,10) 6.49 to 5.46, (6,2) 4.20 to 3.83, (1,4) 3.87 to 3.37, (1,8) 3.35 to 3.02, (15,24) 2.64 to 2.26, (16,12) 2.25 to 1.54, (2,29) 2.25 to 1.61, (7,11) 2.38 to 1.94, and (1,22) 1.79 to 1.24. The other cells in those Q2-y bins did not move. Q2-y 3, 4, 5, 8, 9, 10, 11, 12, 14, and 17 are unchanged. The JSON still has 452 cells. No bin fails the A, B, C, error, or chi-squared rules.

(13,10) was left at B -0.305 and C 0.102 rather than a flatter neighbor. (5,7) was not retuned: the free cosine is C 0.018 and 1.97, against the stored 2.03. There is no 5D family in this file. The best three-parameter curve still misses points at (1,14), (1,7), (1,32), (6,12), (6,6), (2,6), (1,2), (2,5), (2,4), (2,2), (5,12), (9,14), (12,24), and (10,12), plus leftover points in (13,10), (6,2), (15,24), and (1,22).

record_refinement for spline|nominal|nominal matched the saved fit and was recorded as verified.
