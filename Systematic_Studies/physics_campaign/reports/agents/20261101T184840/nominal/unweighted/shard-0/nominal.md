# Agent record
- run_id: 20261101T184840
- stage: nominal
- campaign: unweighted
- source_or_shard: shard-0
- label: nominal

Nominal shard 0 is the unweighted 3D Bayesian file only. Resolved scope: 452 (MultiDim_3D_Histo)_(Bayesian)_ histograms, Q2-y 1-17. RC_Bayesian, BC_RC_Bayesian, Bin, and 5D are absent and were not created. Start mode manual. Error source histogram. Publication off.

The existing run_shard return code 0 was an initial fit, not a finished refinement. Spline windows are tight enough that the universal spline was not used, and the manual initializer was not overwritten.

Overlays plus an unconstrained cosine showed 22 bins whose |B| or C was trapped. Those keys were widened in fits/unweighted/nominal/nominal/refine_init.py and remade for Q2-y 1, 2, 3, 5, 7, 9, 10, 11, 12, 13, 14, 15, and 16. No pass cap and no chi-squared stop. Every edited bin improved, other bins did not move, and the JSON still has 452 entries.

Left because the histogram disagrees with its neighbor: (5,19), (10,13), (9,15), (6,13), and (1,15) stay near zero. Unresolved because a better guide does not help: (1,32), (1,7), (12,24) phi hole, and (13,10) one high bin. record_refinement note is fits/unweighted/nominal/nominal/refinement_note.json.
