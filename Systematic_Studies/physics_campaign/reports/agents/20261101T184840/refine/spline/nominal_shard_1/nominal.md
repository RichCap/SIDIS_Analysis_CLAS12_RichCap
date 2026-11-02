# Agent record
- run_id: 20261101T184840
- stage: refine
- campaign: spline
- source_or_shard: nominal_shard_1
- label: nominal

Nominal shard 1 is the spline 3D Bayesian acceptance fit only. RC_Bayesian and BC_RC_Bayesian are not in the file and were not created. Bin-by-bin is not this shard.

The shard command was python3 Systematic_Studies/sidis_physics_cli.py run_shard -p nominal -s 1 -w Systematic_Studies/physics_campaign/work_plan.json. It reused the existing fit and returned 0. That return code is the initial fit, not a finished refinement. No pass cap and no chi-squared stop were added. Nothing was unfolded and no farm job was submitted.

Start mode is manual. The universal spline B/C windows are tight (median B width 0.02), so --use_spline_init was not used. Errors are histogram errors. Publication was not requested.

Overlays of the initial fit showed twenty bins whose first-pass moment start was too small. The second pass only moves a parameter halfway from that start, so A(1 + B cos phi + C cos 2phi) missed the modulation. Those starts were moved onto the histogram minimum and limits that excluded it were widened in refine_init.py. The shared manual initializer and the universal spline file were not edited. The remake was 3D Bayesian for Q2-y 1, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, and 15.

All twenty bins improved. The largest were (13,4) 17.80 to 2.59, (3,16) 14.80 to 1.42, and (10,11) 8.70 to 1.56. The JSON still has 452 cells. Q2-y 2, 8, 16, and 17 are unchanged, and so are the other cells in the remade Q2-y bins. No bin fails the A, B, C, error, or chi-squared rules.

(13,10) was left at its histogram shape rather than the flat neighbor. (3,29), (9,7), (11,20), (14,5), and (15,15) keep a B or C that the neighbor does not share because the histogram supports it. There is no 5D family in this file. Unresolved histogram misses remain at (13,10), (1,14), (1,7), (1,32), (6,12), (6,6), (2,6), (1,2), (2,5), (2,4), (2,2), (5,12), plus leftover points in (12,24), (3,29), (9,7), and (15,15). (5,7) was not retuned because an unconstrained fit diverged.

record_refinement for spline|nominal|nominal is completed.
