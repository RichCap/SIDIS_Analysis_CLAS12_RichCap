# Agent record
- run_id: 20261101T184840
- stage: refine
- campaign: both
- source_or_shard: variation_shard_1
- label: shard

Variation shard 1 is 41 3D phi_h fits. The histograms that exist are Bayesian, except spline correction_method/BinByBin, which is (MultiDim_3D_Histo)_(Bin)_. RC_Bayesian, BC_RC_Bayesian, and 5D are absent and were not created. Publication was not requested.

The shard command was python3 Systematic_Studies/sidis_physics_cli.py run_shard -p variation -s 1 -w Systematic_Studies/physics_campaign/work_plan.json. It was run with updated_python so the coverage scan can import ROOT. Completed initial fits with unchanged inputs were reused and were not treated as finished, because none had a complete record_refinement note. No pass cap and no chi-squared stop were added. Nothing was unfolded and no farm job was submitted. Bin histograms stayed on --unfolding_3D.

Start mode is manual. Universal spline B windows are tight (median width 0.020, 945 of 1390 narrower than 0.05), so --use_spline_init was not used. The shared manual file and the universal spline file were not edited.

Overlays of the initial fits showed A(1 + B cos phi + C cos 2phi) too flat where a free cosine follows the points. The nominal-init start sat inside a small first-pass moment window, and the second pass only moves each parameter halfway. Those starts were moved onto the histogram cosine and the excluding limits were widened in each job's refine_init.py. Remakes used only the affected Q2-y bins. 613 edited bins improved, none got worse, and the other cells did not move. An after overlay of unweighted chi2_strict_pip (1,19) follows the histogram (reduced chi-squared 12.84 to 2.35).

Sector files also contain 52 pre-existing failed-rule bins, mostly |B| or |C| beyond 1 or a divergent moment on a sparse histogram. The guide edit did not create them, and they were not counted among the 613 improved bins. They stay out of any RMS. Empty sector histograms are N/A and were not given a nominal value. Electron sectors have 28 to 34 empty histograms; pion sectors have 27 to 32. Filled bins in those files were refined. The same recurring misses that a guide cannot remove are (1,32), (1,7), (1,14), (6,12), (6,6), (2,6), and (12,24), where the best cosine already matches and a few points or a phi hole remain. Unweighted dcv_el/tight (1,9) still has parameter errors of 0. Sector bins whose free cosine diverges, including unweighted eS2o (8,30) and (3,29), were left unresolved.

Histogram shapes that disagree with a neighbor were kept. There is no 5D family in these files. record_refinement is completed for every job. Per-job notes are refinement_note.json.

unweighted chi2_strict_pip/chi2_strict_pip cells=452 changed=14 na=0
unweighted dcfid_pip/loose cells=452 changed=14 na=0
unweighted dcfid_pip/tight cells=452 changed=15 na=0
unweighted dcfidref_el/tight cells=452 changed=15 na=0
unweighted dcv_el/tight cells=452 changed=15 na=0
unweighted dvz_pip/tight cells=452 changed=13 na=0
unweighted electron_sector/eS2o cells=424 changed=10 na=28
unweighted electron_sector/eS4o cells=424 changed=15 na=28
unweighted electron_sector/eS6o cells=424 changed=13 na=28
unweighted ecband_el/tight cells=452 changed=15 na=0
unweighted ecthr_el/tight cells=452 changed=14 na=0
unweighted no_pip_testdc/no_pip_testdc cells=452 changed=14 na=0
unweighted no_valerii_knockout/no_valerii_knockout cells=452 changed=13 na=0
unweighted pcalvol/loose cells=452 changed=14 na=0
unweighted pion_sector/pipS1o cells=425 changed=17 na=27
unweighted pion_sector/pipS3o cells=425 changed=8 na=27
unweighted pion_sector/pipS5o cells=425 changed=19 na=27
unweighted acceptance_reweighting/Acc cells=452 changed=30 na=0
unweighted acceptance_threshold/Acc025 cells=452 changed=14 na=0
unweighted bayes_iteration/BayesPlus1 cells=452 changed=14 na=0
unweighted phi_bins/Phi12 cells=452 changed=17 na=0
spline dcfid_el/loose cells=452 changed=16 na=0
spline dcfid_el/tight cells=452 changed=16 na=0
spline dcfidref_el/loose cells=452 changed=13 na=0
spline dcv_el/loose cells=452 changed=18 na=0
spline dvz_pip/loose cells=452 changed=15 na=0
spline electron_sector/eS1o cells=418 changed=10 na=34
spline electron_sector/eS3o cells=422 changed=11 na=30
spline electron_sector/eS5o cells=421 changed=10 na=31
spline ecband_el/loose cells=452 changed=17 na=0
spline ecthr_el/loose cells=452 changed=17 na=0
spline noSmear/noSmear cells=452 changed=20 na=0
spline no_sector_pcal/no_sector_pcal cells=452 changed=16 na=0
spline correction_method/BinByBin cells=452 changed=12 na=0
spline pcalvol/tight cells=452 changed=20 na=0
spline pion_sector/pipS2o cells=421 changed=13 na=31
spline pion_sector/pipS4o cells=420 changed=15 na=32
spline pion_sector/pipS6o cells=423 changed=14 na=29
spline acceptance_threshold/Acc015 cells=452 changed=17 na=0
spline bayes_iteration/BayesMinus1 cells=452 changed=16 na=0
spline rho0_subtraction/NoRho0 cells=452 changed=14 na=0
