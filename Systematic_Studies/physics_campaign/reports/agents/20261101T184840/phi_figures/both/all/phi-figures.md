# Agent record
- run_id: 20261101T184840
- stage: phi_figures
- campaign: both
- source_or_shard: all
- label: phi-figures

Drew only unfolded_ac, unfolded_rc, and unfolded_bc with plot_consolidated_phi_h_figures.py. Output is under physics_campaign/phi_figures/<campaign>/<source>/<variation>/. Each PDF was checked on disk: one page, and the inflated content streams contain one N/A label per missing pad. No Dedicated_5D_Unfold.py, no tectonic, and no thesis edit.

Nominals, both campaigns. unfolded_ac uses fits/<campaign>/nominal/nominal/fit.json and Fit_Pars_from_3D_Bayesian. unfolded_rc uses corrected/<campaign>/rc/fit.json and Fit_Pars_from_3D_RC_Bayesian. unfolded_bc uses corrected/<campaign>/bc/fit.json and Fit_Pars_from_3D_BC_RC_Bayesian. Each of those six files has 452 bins and the matching fit_corrections stage. The histogram file for all three families is the campaign acceptance unfold (inherited_Unweighted.root or inherited_Spline.root). The plotter reads Bayesian histograms and, for unfolded_rc and unfolded_bc, divides by RC_Factors_ifarm_rc.root and then the 2026-10-26 BC JSON. corrected/<campaign>/{rc,bc}/corrected.root was not passed: those files contain only RC_Bayesian or BC_RC_Bayesian names, which this plotter does not draw. That is the acceptance file plus the stage fit, not a replacement of a missing stage. parent corrected/<campaign>/fit.json was not used.

All six nominal PDFs have na=0, drawn=452, and thesis_ready=yes: Unfolded_AC_All_Q2y.pdf, Unfolded_RC_All_Q2y.pdf, and Unfolded_BC_All_Q2y.pdf in phi_figures/unweighted/nominal/nominal and phi_figures/spline/nominal/nominal. Legends are Acceptance Corrected Only, AC + RC, and AC + RC + BC. Page count is 1.

Systematics are unfolded_ac only. Enabled 3D Bayesian variations with Fit_Pars_from_3D_Bayesian were drawn for both campaigns. Fifty-six of those canvases have 452 drawn pads, na=0, and thesis_ready=yes: acceptance_reweighting (Acc, AccSpline), acceptance_threshold (Acc015, Acc025), bayes_iteration (BayesMinus1, BayesPlus1), chi2_strict_pip, dcfid_el loose/tight, dcfid_pip loose/tight, dcfidref_el loose/tight, dcv_el loose/tight, dvz_pip loose/tight, ecband_el loose/tight, ecthr_el loose/tight, noSmear, no_pip_testdc, no_sector_pcal, no_valerii_knockout, pcalvol loose/tight, phi_bins Phi12, and rho0_subtraction NoRho0. NoRho0 uses the same-weight NoRho0 unfold and unfolded_ac, not unfolded_ac_norho.

The 24 electron and pion sector canvases were saved with N/A pads. thesis_ready=no. Missing bins are labeled N/A and were not stored as zero. Drawn pads match the saved Fit_Pars_from_3D_Bayesian count, and drawn+na is 452 on every canvas. N/A counts: spline eS1o 34, eS2o 32, eS3o 30, eS4o 31, eS5o 31, eS6o 31, pipS1o 31, pipS2o 31, pipS3o 31, pipS4o 32, pipS5o 32, pipS6o 29; unweighted eS1o 30, eS2o 28, eS3o 26, eS4o 28, eS5o 28, eS6o 28, pipS1o 27, pipS2o 29, pipS3o 27, pipS4o 31, pipS5o 27, pipS6o 27. That is 711 N/A labels. Sectors stay not_combined.

Not drawn, and not replaced by another family or another fit key:
- BinByBin, both campaigns. The fit key is Fit_Pars_from_3D_Bin, not Fit_Pars_from_3D_Bayesian. No PDF.
- Unweighted 5D. The fit key is Fit_Pars_from_5D_Bayesian and unfolding_3D is false. No PDF. The Spline 5D file is absent and was not replaced by the 3D nominal.
- Six AccSpline-only method files (Acc015, Acc025, BayesMinus1, BayesPlus1, NoRho0, Phi12) are eligible false. They were not drawn.

86 PDFs, all one page. Sizes are 1.37-1.67 MB. Logs are physics_campaign/logs/phi_figures/, with summary.tsv. The PDF page count and the N/A label count were read from the files, not taken from the plotter return code.
