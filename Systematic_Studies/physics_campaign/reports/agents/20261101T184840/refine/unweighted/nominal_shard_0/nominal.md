# Agent record
- run_id: 20261101T184840
- stage: refine
- campaign: unweighted
- source_or_shard: nominal_shard_0
- label: nominal

Nominal shard 0 is the unweighted 3D Bayesian acceptance fit only. The file has 452 (MultiDim_3D_Histo)_(Bayesian)_ phi_h histograms, Q2-y 1-17. RC_Bayesian, BC_RC_Bayesian, Bin, and 5D are absent and were not created.

The shard command was python3 Systematic_Studies/sidis_physics_cli.py run_shard -p nominal -s 0 -w Systematic_Studies/physics_campaign/work_plan.json. It reused the existing fit and returned 0. That return code is the initial fit, not a finished refinement. No pass cap and no chi-squared stop were added. Nothing was unfolded and no farm job was submitted.

Start mode is manual. Of 486 untagged spline bins, 320 have no B window and the median width of the rest is 0.17, so --use_spline_init was not used. Errors are histogram errors. Publication was not requested.

Overlays showed five bins whose guide still missed the histogram. (1,4) had C pinned at -0.01. (1,22) was forced negative on a flat distribution. (2,34), (7,10), and (7,11) stopped short of the modulation the points support. Those keys were widened in refine_init.py. The shared manual initializer and the universal spline file were not edited. The remake was 3D Bayesian for Q2-y 1, 2, and 7.

All five bins improved: (1,4) 3.389 to 2.961, (1,22) 1.426 to 1.025, (2,34) 1.924 to 1.547, (7,10) 2.346 to 2.132, and (7,11) 2.095 to 1.711. The other cells did not move. The JSON still has 452 cells. No bin fails the A, B, C, error, or chi-squared rules. (3,16) remains 1.435 after its earlier release from 16.22.

(5,19) and (1,15) stay near zero because those histograms are flat. (6,12) keeps B about -0.44 because the points support it. (4,29) was not given a larger |B| because that curve overshoots the peak. Unresolved histogram misses remain at (1,32), (1,7), (12,24), and (13,10). There is no 5D family in this file.

record_refinement for unweighted|nominal|nominal is verified and completed.
