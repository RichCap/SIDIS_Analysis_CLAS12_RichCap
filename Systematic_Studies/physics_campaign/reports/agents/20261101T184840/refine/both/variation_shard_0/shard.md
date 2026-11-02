# Agent record
- run_id: 20261101T184840
- stage: refine
- campaign: both
- source_or_shard: variation_shard_0
- label: shard

Variation shard 0 is 42 phi_h fits, 21 unweighted and 21 spline. The histograms that exist are 3D Bayesian, one unweighted 5D Bayesian, and unweighted 3D Bin. RC_Bayesian and BC_RC_Bayesian are absent and were not created. Publication was not requested.

The shard command was python3 Systematic_Studies/sidis_physics_cli.py run_shard -p variation -s 0 -w Systematic_Studies/physics_campaign/work_plan.json. It reused all 42 fits because the inputs were unchanged. Existing notes were not treated as a finished review. No pass cap and no chi-squared stop were added. Nothing was unfolded and no farm job was submitted. Bin histograms stayed on --unfolding_3D --Unfold_Methods (Bin).

Start mode is manual. Universal spline B windows are tight (median width 0.020, 945 of 1390 narrower than 0.05), so --use_spline_init was not used. Errors are histogram errors. The shared manual initializer and the universal spline file were not edited.

Overlays showed A(1 + B cos phi + C cos 2phi) too shallow where the points peak. The nominal-init start sat in a narrow first-pass window, and the second pass only moves each parameter halfway, so the fit could not reach the histogram cosine. Those starts were moved onto the cosine and the excluding limits were widened in each job's refine_init.py. Remakes used only the affected Q2-y bins. 136 edited bins improved, none got worse, and the other cells did not move. JSON files still have their original cell counts. An after overlay of unweighted dcfid_el loose (1,19) follows the histogram (reduced chi-squared 9.78 to 1.79). The same check on unweighted dcv_el loose (13,10), bin-by-bin (10,11), and spline no_pip_testdc (6,2) follows the points. The largest drop was unweighted ecthr_el loose (1,19), 10.20 to 1.78.

Spline eS2o (8,30) has four filled phi bins and a divergent stored B. Opening that guide to the free cosine raised chi2/NDF from 313 to 499, so the edit was reverted and the bin stays unresolved. Fourteen other sector bins with |B| or |C| at or above 1 on sparse histograms were left unresolved and were not filled from the nominal. Empty sector histograms are N/A and were not given a nominal value.

Histogram shapes that already match their own cosine were kept, including the high chi2/NDF tail in AccSpline and Phi12. 5D bins were fit to the 5D histograms and were not replaced by the 3D result. record_refinement is verified for every job. Per-job notes are refinement_note.json.

unweighted dimension/5D cells=452 changed=3 na=0
unweighted dcfid_el/loose cells=452 changed=4 na=0
unweighted dcfid_el/tight cells=452 changed=4 na=0
unweighted dcfidref_el/loose cells=452 changed=3 na=0
unweighted dcv_el/loose cells=452 changed=4 na=0
unweighted dvz_pip/loose cells=452 changed=3 na=0
unweighted electron_sector/eS1o cells=422 changed=3 na=30
unweighted electron_sector/eS3o cells=426 changed=1 na=26
unweighted electron_sector/eS5o cells=424 changed=1 na=28
unweighted ecband_el/loose cells=452 changed=4 na=0
unweighted ecthr_el/loose cells=452 changed=5 na=0
unweighted noSmear/noSmear cells=452 changed=5 na=0
unweighted no_sector_pcal/no_sector_pcal cells=452 changed=3 na=0
unweighted correction_method/BinByBin cells=452 changed=5 na=0
unweighted pcalvol/tight cells=452 changed=2 na=0
unweighted pion_sector/pipS2o cells=423 changed=0 na=29
unweighted pion_sector/pipS4o cells=421 changed=2 na=31
unweighted pion_sector/pipS6o cells=425 changed=2 na=27
unweighted acceptance_threshold/Acc015 cells=452 changed=7 na=0
unweighted bayes_iteration/BayesMinus1 cells=452 changed=5 na=0
unweighted rho0_subtraction/NoRho0 cells=452 changed=4 na=0
spline chi2_strict_pip/chi2_strict_pip cells=452 changed=4 na=0
spline dcfid_pip/loose cells=452 changed=4 na=0
spline dcfid_pip/tight cells=452 changed=3 na=0
spline dcfidref_el/tight cells=452 changed=3 na=0
spline dcv_el/tight cells=452 changed=5 na=0
spline dvz_pip/tight cells=452 changed=4 na=0
spline electron_sector/eS2o cells=420 changed=0 na=32
spline electron_sector/eS4o cells=421 changed=1 na=31
spline electron_sector/eS6o cells=421 changed=2 na=31
spline ecband_el/tight cells=452 changed=4 na=0
spline ecthr_el/tight cells=452 changed=5 na=0
spline no_pip_testdc/no_pip_testdc cells=452 changed=7 na=0
spline no_valerii_knockout/no_valerii_knockout cells=452 changed=4 na=0
spline pcalvol/loose cells=452 changed=4 na=0
spline pion_sector/pipS1o cells=421 changed=2 na=31
spline pion_sector/pipS3o cells=421 changed=0 na=31
spline pion_sector/pipS5o cells=420 changed=0 na=32
spline acceptance_reweighting/AccSpline cells=452 changed=7 na=0
spline acceptance_threshold/Acc025 cells=452 changed=4 na=0
spline bayes_iteration/BayesPlus1 cells=452 changed=3 na=0
spline phi_bins/Phi12 cells=452 changed=0 na=0
