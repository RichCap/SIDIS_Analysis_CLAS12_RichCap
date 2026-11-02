# Agent record
- run_id: 20261101T184840
- stage: refine
- campaign: both
- source_or_shard: variation_shard_1
- label: shard

Variation shard 1 is 41 3D phi_h fits. The histograms that exist are Bayesian, except spline correction_method/BinByBin, which is (MultiDim_3D_Histo)_(Bin)_. RC_Bayesian, BC_RC_Bayesian, and 5D are absent and were not created. Publication was not requested.

The shard command was python3 Systematic_Studies/sidis_physics_cli.py run_shard -p variation -s 1 -w Systematic_Studies/physics_campaign/work_plan.json. It reused all 41 fits because the input size and mtime were unchanged, and returned 0. That return code is not the refinement. No pass cap and no chi-squared stop were added. Nothing was unfolded and no farm job was submitted. Bin histograms stayed on --unfolding_3D --Unfold_Methods (Bin).

Start mode is manual. Universal spline B windows are tight (median width 0.020, 945 of 1390 narrower than 0.05), so --use_spline_init was not used. The shared manual file and the universal spline file were not edited.

Each stored curve was compared with a free weighted cosine on the same positive-error phi bins. Overlays of the misses showed the fit too flat where the histogram has a cosine: chi2_strict_pip (16,12) had C stuck at 0.060, which is 1.5 times the 0.04 limit, while the peak wants C 0.107; spline dcfid_el/loose (6,1), dcfid_pip/tight (10,17), dvz_pip/tight (3,2), and eS3o (13,4) had the same first-pass limit, and the second pass only moves a parameter halfway. dcfid_pip/loose (5,31) was noisy but its limits excluded the positive side the points allow. Those starts were moved onto the histogram cosine and only the excluding limits were widened in refine_init.py. Remakes used only the affected Q2-y bins. 132 edited bins improved, none got worse, and cells whose guides were not edited did not move. Unselected Q2-y bins are unchanged. JSON cell counts are unchanged. After overlays follow the histograms: (16,12) reduced chi-squared 2.20 to 1.54, (6,1) 2.15 to 1.20, (10,17) 3.02 to 1.86, (3,2) 1.54 to 0.80. The dip near 300 deg in (6,1) stays inside large errors and was not cut out of the fit.

Phi12 and unweighted eS6o had no trapped bin. Phi12 (1,7) was drawn: the stored curve and the free cosine are the same (B -0.403, C 0.084), reduced chi-squared 10.49, with two points off a 12-bin histogram. Acc (1,32) reduced chi-squared 7.73 follows the other points and leaves one high phi bin. A further guide change does not fix those. 86 failed-rule bins, mostly sparse sector histograms with |B| or |C| beyond 1 or NDF 0, were not given a nominal value. Empty sector histograms stay N/A.

Histogram shapes that disagree with a neighbor were kept, including (16,12) B near -0.38 beside (16,13) near 0. There is no 5D family in these files. record_refinement is verified for every job. Per-job notes are refinement_note.json.

unweighted chi2_strict_pip/chi2_strict_pip cells=452 changed=2 na=0
unweighted dcfid_pip/loose cells=452 changed=4 na=0
unweighted dcfid_pip/tight cells=452 changed=4 na=0
unweighted dcfidref_el/tight cells=452 changed=4 na=0
unweighted dcv_el/tight cells=452 changed=2 na=0
unweighted dvz_pip/tight cells=452 changed=4 na=0
unweighted electron_sector/eS2o cells=424 changed=1 na=28
unweighted electron_sector/eS4o cells=424 changed=1 na=28
unweighted electron_sector/eS6o cells=424 changed=0 na=28
unweighted ecband_el/tight cells=452 changed=3 na=0
unweighted ecthr_el/tight cells=452 changed=6 na=0
unweighted no_pip_testdc/no_pip_testdc cells=452 changed=2 na=0
unweighted no_valerii_knockout/no_valerii_knockout cells=452 changed=5 na=0
unweighted pcalvol/loose cells=452 changed=4 na=0
unweighted pion_sector/pipS1o cells=425 changed=1 na=27
unweighted pion_sector/pipS3o cells=425 changed=1 na=27
unweighted pion_sector/pipS5o cells=425 changed=3 na=27
unweighted acceptance_reweighting/Acc cells=452 changed=2 na=0
unweighted acceptance_threshold/Acc025 cells=452 changed=5 na=0
unweighted bayes_iteration/BayesPlus1 cells=452 changed=3 na=0
unweighted phi_bins/Phi12 cells=452 changed=0 na=0
spline dcfid_el/loose cells=452 changed=5 na=0
spline dcfid_el/tight cells=452 changed=5 na=0
spline dcfidref_el/loose cells=452 changed=2 na=0
spline dcv_el/loose cells=452 changed=5 na=0
spline dvz_pip/loose cells=452 changed=6 na=0
spline electron_sector/eS1o cells=418 changed=3 na=34
spline electron_sector/eS3o cells=422 changed=5 na=30
spline electron_sector/eS5o cells=421 changed=1 na=31
spline ecband_el/loose cells=452 changed=4 na=0
spline ecthr_el/loose cells=452 changed=4 na=0
spline noSmear/noSmear cells=452 changed=5 na=0
spline no_sector_pcal/no_sector_pcal cells=452 changed=4 na=0
spline correction_method/BinByBin cells=452 changed=4 na=0
spline pcalvol/tight cells=452 changed=1 na=0
spline pion_sector/pipS2o cells=421 changed=1 na=31
spline pion_sector/pipS4o cells=420 changed=5 na=32
spline pion_sector/pipS6o cells=423 changed=1 na=29
spline acceptance_threshold/Acc015 cells=452 changed=4 na=0
spline bayes_iteration/BayesMinus1 cells=452 changed=6 na=0
spline rho0_subtraction/NoRho0 cells=452 changed=4 na=0
