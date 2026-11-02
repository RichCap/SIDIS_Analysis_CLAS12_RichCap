# Agent record
- run_id: 20261101T184840
- stage: variations
- campaign: both
- source_or_shard: shard-0
- label: variation

Variation shard 0 is 42 jobs, 21 unweighted and 21 spline. Families actually in the files are 3D Bayesian, one unweighted 5D Bayesian, and unweighted 3D Bin. RC_Bayesian and BC_RC_Bayesian are absent and were not created. Publication is off. Start mode is manual: each variation uses nominal B and C starts with the existing limit windows, via --fit_init_file. The universal spline was not used. Errors are histogram errors.

The shard command was python3 Systematic_Studies/sidis_physics_cli.py run_shard -p variation -s 0 -w Systematic_Studies/physics_campaign/work_plan.json. No pass cap and no chi-squared stop. Nothing was unfolded and no farm job was submitted. Fits whose inputs were unchanged were reused by that command, but none had a complete record_refinement note, so those return codes are initial fits. Previously failed sector jobs and the new Acc015, BayesMinus1, NoRho0, Acc025, BayesPlus1, and Phi12 jobs were fit by that command and returned 0. Empty sector histograms are skipped. Bin-by-bin stayed on --unfolding_3D --Unfold_Methods (Bin), not --unfolding_1D.

Overlays of unweighted dcfid_el loose (3,16), (10,11), (14,5), and (15,15) showed the stored curve too flat where an unconstrained cosine follows the points. The same trap, from the second pass staying near a start outside the histogram minimum, repeats across the shard. Only those keys were widened in a per-job refine_init.py. nominal_init.py and the shared manual initializer were not edited. Remakes were the affected Q2-y bins only. 506 edited bins improved. Unedited cells in those Q2-y bins did not move. Full-coverage JSON files still have 452 cells. The largest drops were spline no_pip_testdc (10,11) 33.46 to 2.15, unweighted dcv_el loose (10,11) 28.82 to 1.78, and spline (13,4) about 18 to about 2.6. Spline eS2o (8,30) was tried and reverted because chi2/NDF went from 313 to 499.

Twelve sector fits are completed_partial. Empty histograms are N/A (359 across those files, about 26 to 32 each) and were not filled from the nominal. Sparse sector bins that still diverge, including repeated (3,29), (4,15), (8,25), and (8,30), stay unresolved. Full-coverage files have no hard failures. Bins left because the histogram disagrees with a neighbor are the ones whose own cosine already matches the stored curve. AccSpline and Phi12 still have a high chi2/NDF tail from the histogram shape.

record_refinement notes for all 42 jobs are completed.
