# Agent record
- run_id: 20261101T184840
- stage: phi_figures
- campaign: both
- source_or_shard: all
- label: phi-figures

Drew only unfolded_ac, unfolded_rc, and unfolded_bc with plot_consolidated_phi_h_figures.py. Output is under physics_campaign/phi_figures/<campaign>/<source>/<variation>/. Each PDF is one page. No Dedicated_5D_Unfold.py, no tectonic, and no thesis edit.

Nominals, both campaigns. unfolded_ac uses fits/<campaign>/nominal/nominal/fit.json and Fit_Pars_from_3D_Bayesian. unfolded_rc uses corrected/<campaign>/rc/fit.json and Fit_Pars_from_3D_RC_Bayesian. unfolded_bc uses corrected/<campaign>/bc/fit.json and Fit_Pars_from_3D_BC_RC_Bayesian. Each of those six files has 452 retained bins and the matching fit_corrections stage. The histogram file for all three families is the campaign acceptance unfold (inherited_Unweighted.root or inherited_Spline.root). The plotter reads Bayesian histograms and, for unfolded_rc and unfolded_bc, divides by RC_Factors_ifarm_rc.root and then the 2026-10-26 BC JSON. corrected/<campaign>/{rc,bc}/corrected.root was not passed: those files contain only RC_Bayesian or BC_RC_Bayesian names, which this plotter does not draw. That is the same acceptance file plus the stage fit, not a replacement of a missing stage. parent corrected/<campaign>/fit.json was not used.

All six nominal PDFs are thesis_ready=yes: Unfolded_AC_All_Q2y.pdf, Unfolded_RC_All_Q2y.pdf, and Unfolded_BC_All_Q2y.pdf in phi_figures/unweighted/nominal/nominal and phi_figures/spline/nominal/nominal. Legends are Acceptance Corrected Only, AC + RC, and AC + RC + BC.

Systematics are unfolded_ac only. Enabled manifest variations with Fit_Pars_from_3D_Bayesian on all 452 retained bins were drawn for both campaigns (28 each, 56 PDFs): acceptance_reweighting (Acc, AccSpline), acceptance_threshold (Acc015, Acc025), bayes_iteration (BayesMinus1, BayesPlus1), chi2_strict_pip, dcfid_el loose/tight, dcfid_pip loose/tight, dcfidref_el loose/tight, dcv_el loose/tight, dvz_pip loose/tight, ecband_el loose/tight, ecthr_el loose/tight, noSmear, no_pip_testdc, no_sector_pcal, no_valerii_knockout, pcalvol loose/tight, phi_bins Phi12, and rho0_subtraction NoRho0. NoRho0 uses the same-weight NoRho0 unfold and unfolded_ac, not unfolded_ac_norho. Every one returned thesis_ready=yes. Sizes are 1.3-1.6 MB.

Not written, and not replaced by another family or another fit key:
- 24 electron and pion sector variations (eS1o-eS6o, pipS1o-pipS6o, both campaigns). The plotter reached the draw and returned thesis_ready=no because the stored fit misses retained bins (422-426 of 452 for Unweighted, 418-423 of 452 for Spline). The first missing bins in the status line are Q2-y 3 and 4. No PDF was saved.
- BinByBin, both campaigns. fit.json has Fit_Pars_from_3D_Bin, not Fit_Pars_from_3D_Bayesian. thesis_ready=no, no PDF.
- Unweighted dimension 5D. fit.json has Fit_Pars_from_5D_Bayesian and unfolding_3D is false. thesis_ready=no, no PDF. The Spline 5D file is absent and was not drawn or replaced by the 3D nominal.
- Six AccSpline-only method files (Acc015, Acc025, BayesMinus1, BayesPlus1, NoRho0, Phi12) are eligible false and blocked. They were not drawn.

62 PDFs, all one page, all return code 0. Logs are physics_campaign/logs/phi_figures/, with summary.tsv.
