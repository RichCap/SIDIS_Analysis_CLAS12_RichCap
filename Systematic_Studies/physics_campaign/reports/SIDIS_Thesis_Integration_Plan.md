# SIDIS thesis integration plan

This file is a specification for a later editing pass. It does not modify the thesis.

The thesis source was read on 2026-11-02. No thesis file was edited, no figure was copied into the thesis, and the thesis was not compiled.

Thesis root: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Actual_Thesis_LaTeX_Projects/LaTeX_GitHub/Richard_Capobianco_PhD_Thesis`.

Chapter order in `main.tex` is Introduction, The Experiment, Data Processing and Event Selection, Monte Carlo, Analysis Procedure, Results and Systematic Uncertainties, and Conclusions and Outlook. Appendix A is Additional Figures. `Timeline.tex` is commented out of `main.tex`.

Chapter 6 keeps its current section order: Cosine Moment Extractions, Closure Tests, then Systematic Uncertainties. Unweighted and Spline stay separate. Neither is the quoted result. Unavailable numbers stay blocked or provisional. A blocked row is not a measurement and is not entered as zero.

## Chapter 5 — Radiative Corrections

- Source: `Analysis_Procedures/Analysis_Procedures_SubSections/Radiative_Corrections.tex`
- Location: equation RadiativeCorrection and RC_Factor_Application
- Action: retain
- Status: verified
- Artifact: ``
- Citation key: `BYER2023108702`
- Draft text: Keep the nominal factor as the radiated-to-Born event ratio and the application as division of the acceptance-corrected yield. Do not restore the commented bin-center fit as the nominal correction.
- Justification: The live equations match apply_nominal_corrections.py, which writes RC_Bayesian by dividing by the event-ratio factors. The fixed-point cross section is a separate alternative.

## Chapter 5 — Radiative Corrections

- Source: `Analysis_Procedures/Analysis_Procedures_SubSections/Radiative_Corrections.tex`
- Location: after RC_Factor_Application; the commented eq:RCPhiFit stays commented
- Action: revise
- Status: provisional
- Artifact: `Systematic_Studies/physics_campaign/fixed_point/rc_grid_status.json`
- Citation key: `BYER2023108702`
- Draft text: Add that a fixed-point sigma_tot/sigma_B evaluation is an alternative used only for model dependence. It is not the nominal factor. Its cubature uncertainty is not an experimental systematic. SF 0 is Prokudin. SF 2 is the electroproduction A_ep spline, and that spline omits the virtual-photon flux. The RC cache finished with 10848 succeeded cells for each of SF 0 and SF 2. No moment-shift table was formed from that cache, so neither alternative enters the quadrature and no shift is quoted.
- Justification: rc_grid_status.json records complete grids. budgets.json still excludes radiative SF 0, SF 2, and their difference, and stores no radiative number. The number is not zero.
- Dependency: reviewed radiative shift tables; do not quote the cache as a systematic

## Chapter 5 — Bin-Centering Corrections

- Source: `Analysis_Procedures/Analysis_Procedures.tex`
- Location: equation eq:BC_Factor_Definition and eq:BC_Factor_Application
- Action: retain
- Status: verified
- Artifact: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/BC_Corrections/Sub_Bin_Contents_for_BC_Correction_with_Binned_sbatch_from_10_26_2026.json`
- Draft text: Keep BC as the unweighted sub-bin mean divided by the center sub-bin, zeros included, on the 3x3x3x3x5 grid. The nominal application divides the RC-corrected yield by that factor.
- Justification: The live equations match the nominal JSON field BC_Factor and the nominal Stage C application.

## Chapter 5 — Bin-Centering Corrections

- Source: `Analysis_Procedures/Analysis_Procedures.tex`
- Location: equation eq:BCIterationWeight and the paragraph that says the fully corrected results include this BC factor
- Action: revise
- Status: verified
- Artifact: `/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Prepare_Next_Iteration/acc020_3D_BC_RC_rawA_4D_xB_Fit_Pars_from_3D_BC_RC_Bayesian_Compute_SplineWeight.txt`
- Draft text: State that the campaign nominal factor is the event-style unweighted JSON, not the one-update weight in eq:BCIterationWeight and not a spline. The histogram-weight spline is the raw-amplitude file. It is not the electroproduction A_ep spline. A_ep divides Fit_Par_A by the bin area and luminosity and does not divide by Gamma. Histogram normalization may still divide by Gamma. B and C stay dimensionless in both conventions. The spline BC alternative and the iteration stay out of the quoted systematic.
- Justification: bin_centering.json keeps the iteration and the spline-transfer method not combined, with a null systematic. The injection path is the raw-amplitude file named by the workflow.

## Chapter 5 — Procedure Overview

- Source: `Analysis_Procedures/Analysis_Procedures_SubSections/Procedural_Overview.tex`
- Location: equation eq:NormalizedA, after eq:DeltaPT2
- Action: revise
- Status: provisional
- Artifact: `Systematic_Studies/physics_campaign/corrected/unweighted/normalized_bc.json`
- Citation key: `klimenko2024`
- Draft text: Keep the luminosity, beam-blocker, and tracking factors, and keep Gamma in the reported histogram amplitude. State that normalized_bc.json divides the stored Fit_Par_A by bin area times luminosity times Gamma after the fit, with Delta(p_T^2) in that area, and does not rescale B or C. eq:BinVolume itself uses Delta(p_T). A later figure must say which width it used. Do not interchange that file with the A_ep spline, which omits Gamma.
- Justification: write_normalized_results.py sets pT2 true and builds A0 from area, luminosity, and flux. The electroproduction note keeps Gamma out of A_ep. The two files are not the same amplitude.
- Dependency: the quoted figure must name Delta(p_T) or Delta(p_T^2) before the normalized file is inserted

## Chapter 5 — Acceptance Corrections

- Source: `Analysis_Procedures/Analysis_Procedures_SubSections/Acceptance_Corrections.tex`
- Location: tab:UnfoldingSummary and the paragraph on the 5D matrix
- Action: retain
- Status: verified
- Artifact: ``
- Citation key: `DAgostini:1994fjx`
- Draft text: Keep the 3D Bayesian result as the result shown in the thesis. Keep the 5D matrix as a systematic test, not as the source of the quoted moments. Do not change the stated acceptance threshold 0.020 or the iteration choice k=6 in Q2-y bins 1 and 5 and k=5 otherwise.
- Justification: Those choices are the live thesis text and the nominal campaign definition. The Spline 5D file is absent and contributes no number.

## Chapter 6 — Cosine Moment Extractions

- Source: `Results/Results_SubSections/Cosine_Moment_Extractions.tex`
- Location: the averaged percent-difference paragraph and the commented 455-bin note
- Action: revise
- Status: blocked
- Artifact: `Systematic_Studies/physics_campaign/corrected/unweighted/normalized_bc.json`
- Draft text: Do not keep or recompute those percentages for this plan. They describe an older acc025 chain, and the comment quotes 455 bins. Each normalized_bc.json has 452 Fit_Pars_from_3D_BC_RC_Bayesian cells. Leave the paragraph unchanged until a new average is calculated from the campaign fits. Do not invent a replacement percentage.
- Justification: The live images are named 3D_rho0_acc025 and 3D_WITHOUT_rho0_acc025. The campaign files are the 0.020 nominal chain. The counts and the filenames are not the same result.
- Dependency: a new stage-to-stage average from the campaign fits, calculated separately for Unweighted and Spline

## Chapter 6 — Cosine Moment Extractions

- Source: `Results/Results_SubSections/Cosine_Moment_Extractions.tex`
- Location: fig:Moments_Bayesian_noRho_z through fig:Moments_BCRC_pT
- Action: revise
- Status: blocked
- Artifact: `Systematic_Studies/physics_campaign/mosaics`
- Suggested caption or title: Acceptance, radiative, and bin-centering corrected A0, B, and C. The band is the provisional acceptance-level budget, not the final systematic. Unweighted and Spline are separate.
- Draft text: Do not replace the four existing correction-stage figures until the mosaics are redrawn from normalized_bc.json. The redraw does not pass the A0 scale a second time and keeps the two campaigns apart. The existing acc025 figures stay until that redraw exists. Do not call the band final, and do not choose a quoted campaign in the caption. The current mosaic PDFs are older than normalized_bc.json.
- Justification: normalized_bc.json is labeled provisional_acceptance_level. Neither campaign is the quoted result. The mosaic directory is older than both normalized files.
- Dependency: redraw z, P_T, and P_T^2 mosaics from normalized_bc.json, without a second A0 scale, before any figure is inserted

## Chapter 6 — Cosine Moment Extractions

- Source: `Results/Results_SubSections/Cosine_Moment_Extractions.tex`
- Location: end of the section, after the P_T moment figures and before Closure Tests
- Action: add
- Status: provisional
- Artifact: `Systematic_Studies/physics_campaign/kt2/unweighted/run_20261102_152727/kt2_results.tsv`
- Suggested caption or title: Gaussian P_T^2 slope of normalized A0. The error is the provisional acceptance-level uncertainty. This is not a measured intrinsic width.
- Draft text: Add the kT2 figure only from run_20261102_152727, not from the older top-level kt2_results.tsv. Unweighted has 91 rows: all 91 have a large log uncertainty, 78 are also consistent with zero slope, and 13 are not. Spline has 91 rows: all 91 have a large log uncertainty, 80 are also consistent with zero slope, and 11 are not. Do not quote one width, and do not interpret the slope as a model conclusion. Keep the two campaigns separate. The spline companion table is the same run directory under kt2/spline.
- Justification: That run used the normalized BC file and the systematic error field. The top-level TSV is an older, different file. A slope consistent with zero is not a kT2 measurement.
- Dependency: the same quoted-campaign choice as the moment figures; do not promote the top-level TSV

## Chapter 6 — Closure Tests

- Source: `Results/Results_SubSections/Closure_Tests.tex`
- Location: sec:Unfold_MC and sec:phi_h_edge_cuts
- Action: retain
- Status: blocked
- Artifact: ``
- Draft text: Leave the three placeholder paragraphs as they are. Do not add a closure number, a passed or failed statement, or an edge-cut tolerance.
- Justification: The section states the tests and does not report a result. No closure artifact was produced for this plan.
- Dependency: a stored closure result; none is available

## Chapter 6 — Systematic Uncertainties

- Source: `Results/Results_SubSections/Systematic_Uncertainties.tex`
- Location: tab:SystematicUncertainties; keep the following input order unchanged
- Action: revise
- Status: blocked
- Artifact: `Systematic_Studies/physics_campaign/budgets.json`
- Suggested caption or title: Source list in the present order. Blank cells are not zero. The total band is provisional and acceptance-level.
- Draft text: Keep every subsection in its current order, from the sampling fraction through acceptance reweighting. Do not fill the three moment columns from the raw budget RMS. Those A shifts are not in the normalized A0 units. The normalized total is Fit_Par_A_SYS, Fit_Par_B_SYS, and Fit_Par_C_SYS, and it is provisional. Per-source cells stay blank until a scaled per-source table exists. Sectors, radiative alternatives, the spline BC alternative, the BC iteration, and the fifteen-subdivision RMS stay out of the sum. A missing source is named and is not entered as zero.
- Justification: budgets.json is provisional for both campaigns. electron_sector and pion_sector are not combined. The radiative and bin-centering alternatives are listed under excluded and have no number. Subdivision shifts were not fitted, so they are not in the sum. The fifteen-file RMS, once it exists, is one Unweighted term, not five terms, and it is not copied into Spline.
- Dependency: a per-source table scaled like normalized_bc.json, plus the missing radiative and bin-centering shifts

## Chapter 6 — Sector dependence

- Source: `Results/Results_SubSections/Uncertainties_SubSections/Sys_Sector_Dependence.tex`
- Location: after the last paragraph of sys-sector
- Action: add
- Status: provisional
- Artifact: `Systematic_Studies/physics_campaign/phi_figures`
- Suggested caption or title: Partial sector phi_h canvases. Empty pads are N/A and are not zero. Sectors are not in the final quadrature.
- Draft text: The twelve electron-sector and twelve pion-sector canvases may be shown as diagnostics. Keep both sector families out of the final quadrature until that inclusion is authorized. Do not replace an empty pad by zero.
- Justification: Twenty-four sector PDFs are present under phi_figures. budgets.json marks both sector sources not combined. Empty bins stay out of the RMS.
- Dependency: authorization to show sector diagnostics; they still do not enter the sum

## Chapter 6 — Radiative-Correction Model Dependence

- Source: `Results/Results_SubSections/Uncertainties_SubSections/Sys_Radiative_Model.tex`
- Location: sys-rc-model, after the description of the alternative
- Action: revise
- Status: provisional
- Artifact: `Systematic_Studies/physics_campaign/fixed_point/rc_grid_status.json`
- Citation key: `BYER2023108702`
- Draft text: Keep the nominal description. Add that the fixed-point SF 0 and SF 2 caches finished and that their moment shifts were not extracted or reviewed. Do not write a systematic value. The cubature uncertainty on sigma_tot/sigma_B is not that value.
- Justification: The subsection defines the comparison. The cache does not by itself supply the shift of A0, B, or C. The budget excludes it.
- Dependency: reviewed radiative shift tables

## Chapter 6 — BC Corrections

- Source: `Results/Results_SubSections/Uncertainties_SubSections/Sys_Iterative_Bin_Centering.tex`
- Location: sys-bc-iter and sys-bc-kin
- Action: revise
- Status: provisional
- Artifact: `Systematic_Studies/physics_campaign/reports/bin_centering.json`
- Draft text: Keep the definitions. State that the one-update azimuthal weight and the spline alternative are not combined. The fifteen subdivision files are on disk, but the fitted A, B, and C shifts from a full refinement are not. Those shifts become one pooled RMS for Unweighted only, not five quadrature terms, and they are not copied into Spline. Until those shifts exist, the cells stay blank.
- Justification: bin_centering.json records the subdivision files and awaiting_observable_shifts. The iteration and method systematics are null.
- Dependency: fifteen refined subdivision shifts before any BC sampling number is entered

## Chapter 7 — Comparisons to World Data

- Source: `Conclusions/Conclusions_SubSections/Comparisons_to_World_Data.tex`
- Location: section body; it is one placeholder sentence
- Action: replace
- Status: blocked
- Artifact: `Systematic_Studies/physics_campaign/reports/world_comparisons.md`
- Suggested caption or title: B and C at matched kinematics. Hall C moments, if shown, are a refit from published multiplicities.
- Citation key: `HallCSIDIS:2025plr`
- Draft text: Do not replace the placeholder with the readiness note. Fill the section only from comparison figures that do not yet exist. Use the current normalized moments, not the October 30 CLAS12 values and not their chi-squared. hallc_2510.03562_cos_moments_refit_all.csv is a refit, not the Hall C published moment table; HallCSIDIS:2025plr is the multiplicity paper. HarrisonThesis and Osipenko:2008rv are the other CLAS samples already in the bibliography. HERMES cosine moments are absent from the table directory and are not invented. A no-rho0 curve uses the NoRho0 fits, not a rescaling. Do not claim a first multidimensional or first same-energy measurement.
- Justification: The tex file is one sentence. world_comparisons.md lists external tables and does not contain an overlay, a residual plot, or an agreement table.
- Dependency: no world-data overlay, residual plot, or agreement table has been written

## Chapter 7 — Comparisons to Theory Models

- Source: `Conclusions/Conclusions_SubSections/Comparisons_to_Theory_Models.tex`
- Location: section body; it is one placeholder sentence
- Action: add
- Status: blocked
- Artifact: `Systematic_Studies/physics_campaign/reports/theory_comparisons.md`
- Citation key: `Cahn:1978se`
- Draft text: Do not add a numerical curve. Cahn:1978se may be named as the kinematic effect already used in the thesis, not as a new plotted prediction. Barone et al. 2015, Bastami et al. 2019, and Balitsky and Prokudin 2026 stay interpretation-only: no checked formula is stored, and those papers were not given citation keys in this plan. Do not present a partial Boer-Mulders term as the Barone et al. 2015 model. An A0 comparison, once a checked curve exists, prefers shape and P_T width unless the absolute normalization has been shown to match.
- Justification: theory_comparisons.md states that no numerical curve is written. The bibliography was searched for those three model papers and no matching key was used here.
- Dependency: no checked theory curve has been written

## Chapter 7 — Final Conclusions

- Source: `Conclusions/Conclusions_SubSections/Final_Conclusions.tex`
- Location: the placeholder sentence
- Action: revise
- Status: blocked
- Artifact: ``
- Draft text: Leave the placeholder in place. A later closing paragraph may state only the measured moments and the kinematic coverage that were actually shown. It must separate those statements from an interpretation of the P_T width or of a model comparison. It must not claim a first multidimensional or first same-energy measurement.
- Justification: The section is one sentence. The world and theory sections have no validated comparison, and no campaign has been chosen as the quoted result.
- Dependency: validated moment figures and validated world and theory comparisons

## Chapter A — Additional Figures

- Source: `Appendix_Sections/Additional_Phi_h_Figures.tex`
- Location: A:Phi_h_Unfolded_AC, A:Phi_h_Unfolded_RC, and A:Phi_h_Unfolded_BC
- Action: retain
- Status: provisional
- Artifact: `Systematic_Studies/physics_campaign/phi_figures`
- Draft text: Keep the families already drawn. The main text already collects all 17 Q2-y bins for the replaced acceptance and bin-centering canvases, and the appendix still has the radiative bins 2-17 plus the without-rho0 sets. Do not add a second copy of a family that the main text already shows. A sector canvas or a missing correction stage may be added only when that family is absent from the main text. The three nominal stages must use their own acceptance, RC, and BC files. One stage is not a substitute for another. No file is copied in this plan.
- Justification: The appendix states that the consolidated main-text figures collect every Q2-y bin for the families that were replaced. Campaign nominal canvases exist for all three stages, and the without-rho0 directory has only the acceptance canvas.
- Dependency: a later editing pass may insert a missing family; this plan does not copy figures

## Chapter A — Additional Tables

- Source: `Appendix_Sections/Appendix.tex`
- Location: chapter Additional Tables, after the fiducial-cut table
- Action: add
- Status: blocked
- Artifact: `Systematic_Studies/physics_campaign/corrected/spline/normalized_bc.json`
- Suggested caption or title: Normalized A0, B, and C after acceptance, radiative, and bin-centering corrections. One campaign per table.
- Draft text: Do not add the numerical table yet. When it is added, use normalized_bc.json, one table for each campaign, with the provisional acceptance-level uncertainty labeled as provisional. Do not merge the campaigns and do not use the older normalized.json.
- Justification: The additional-tables chapter currently contains the DC fiducial vertices and no moment table. Both normalized files exist, but neither campaign is the quoted result.
- Dependency: a quoted campaign and the bin-width statement required for eq:NormalizedA
