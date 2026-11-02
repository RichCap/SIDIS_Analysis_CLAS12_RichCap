# Agent record
- run_id: 20261101T184840
- stage: aggregate
- campaign: both
- source_or_shard: budgets
- label: aggregate

Both budgets are provisional. The radiative study is enabled and pending, so it contributes no systematic number and is not entered as zero. Unweighted and Spline totals were not added. Fit_Par_*_ERR is only the denominator of R_source and R_total. No fit error was zero, missing, or non-finite in this table, so no ratio was skipped, and no ratio dropped a source. The sum is reduce_source(..., "rms") with N inside the square root, then combine_sources(..., "quadrature") of independent sources only. A one-variation source is the absolute difference. The quadrature check matched that sum for every bin.

The bin-centering subdivision source has no 15 observable shifts (study_state awaiting_observable_shifts, count 0). It was not entered in the Unweighted quadrature, was not copied into Spline, and was not replaced by zero. The bin-centering method and iteration comparisons stay blocked and contribute no number. Bayesian 1D is disabled and contributes no number. Spline 5D is absent and is not zero. Q2-y bins 1 and 5 on the Unweighted 5D comparison are flagged iteration_mismatch and remain in that source RMS.

Electron and pion sector sources are not_combined. Empty bins are missing rows (711 missing comparison rows), not zeroes. Their largest B and C RMS values are outside the totals: unweighted electron_sector B and C at (Q2_y_Bin_12)-(z_pT_Bin_14), and spline pion_sector B and C at (Q2_y_Bin_4)-(z_pT_Bin_15).

Unweighted versus Spline nominal differences are campaign cross, source unweighted_versus_spline, combine not_combined, and are outside both totals. Reference is the Unweighted nominal and the variation is the Spline nominal.

Library tests in Systematic_Studies/test_sidis_physics.py passed before this table was written (sidis physics tests ok). Failed or missing fit jobs: 0. Comparison rows: 112482. Source rows: 59334. Total rows: 2712.

Per-bin source RMS is in sources.csv. The numbers below are the median and the maximum of that per-bin RMS, not a second reduction. n_shifts is the number of variations inside the RMS.

Unweighted provisional True. Bins 452.
Independent: acceptance_reweighting, acceptance_threshold, bayes_iteration, chi2_strict_pip, correction_method, dcfid_el, dcfid_pip, dcfidref_el, dcv_el, dimension, dvz_pip, ecband_el, ecthr_el, noSmear, no_pip_testdc, no_sector_pcal, no_valerii_knockout, pcalvol, phi_bins, rho0_subtraction.
Not combined: electron_sector, pion_sector.
Quadrature A median 16957.587 max 59185.266. B median 0.10701702 max 0.34631291. C median 0.034214252 max 0.22956275.
acceptance_reweighting A median 221.83607 max 2665.9585 (n=1). B median 0.096182076 max 0.29967056. C median 0.025812776 max 0.11876727.
acceptance_threshold A median 2.1875597 max 848.17399 (n=2). B median 0.00023876305 max 0.066432584. C median 0.00017858662 max 0.043027944.
bayes_iteration A median 6.1653435 max 847.39321 (n=2). B median 0.00053275443 max 0.06418556. C median 0.0004317339 max 0.043027945.
chi2_strict_pip A median 826.73757 max 4886.145 (n=1). B median 0.010405627 max 0.10814171. C median 0.0034981137 max 0.054834175.
correction_method A median 358.67256 max 4776.7348 (n=1). B median 0.011658148 max 0.11667354. C median 0.0047266965 max 0.052574973.
dcfid_el A median 0.0091711916 max 848.46819 (n=2). B median 8.1921596e-07 max 0.094162135. C median 8.2655814e-07 max 0.043027946.
dcfid_pip A median 12.234534 max 877.69569 (n=2). B median 0.0012457177 max 0.044163029. C median 0.001053375 max 0.043027947.
dcfidref_el A median 18.319189 max 872.75487 (n=2). B median 0.0015465636 max 0.062452117. C median 0.0014088374 max 0.043027945.
dcv_el A median 118.24277 max 794.09357 (n=2). B median 0.0013346724 max 0.063304795. C median 0.0012310251 max 0.043027947.
dimension A median 192.45631 max 3458.8148 (n=1). B median 0.0049355786 max 0.094867875. C median 0.0030788915 max 0.046465257.
dvz_pip A median 16.696536 max 734.33362 (n=2). B median 0.000865789 max 0.067476195. C median 0.00057619532 max 0.043027945.
ecband_el A median 11.145239 max 842.99009 (n=2). B median 0.00036430595 max 0.066629674. C median 0.00036463938 max 0.043027946.
ecthr_el A median 22.107627 max 855.163 (n=2). B median 0.00048622928 max 0.068522195. C median 0.00043923721 max 0.043027946.
noSmear A median 17.916801 max 879.06717 (n=1). B median 0.0015004106 max 0.094756847. C median 0.0010562298 max 0.043027944.
no_pip_testdc A median 91.96901 max 4041.4303 (n=1). B median 0.0046384139 max 0.18504144. C median 0.0049326919 max 0.1335991.
no_sector_pcal A median 154.51915 max 1349.7051 (n=1). B median 0.00040170203 max 0.093191147. C median 0.00043152211 max 0.043027947.
no_valerii_knockout A median 75.536418 max 561.99914 (n=1). B median 0.00052010864 max 0.054392679. C median 0.00047118987 max 0.04302795.
pcalvol A median 54.072155 max 4369.7162 (n=2). B median 0.00023836551 max 0.051043218. C median 0.0001823704 max 0.043027946.
phi_bins A median 16847.69 max 58433.409 (n=1). B median 0.0028048625 max 0.073964953. C median 0.0029688189 max 0.06230344.
rho0_subtraction A median 378.68827 max 1893.5961 (n=1). B median 0.0068202403 max 0.1131763. C median 0.0020198356 max 0.054225059.
electron_sector not_combined A median 617.15139 max 21093.912 (n=1-6, 426 bins). B median 0.038611749 max 6312646.7. C median 0.031955615 max 4131144.3.
pion_sector not_combined A median 601.83703 max 21082.472 (n=1-6, 426 bins). B median 0.046649239 max 4163585.6. C median 0.03512277 max 2716336.6.
Flags: source fit_larger 20467, source systematic_larger 9209, total fit_larger 8, total systematic_larger 1348.

Spline provisional True. Bins 452. Subdivision was not copied here.
Independent: acceptance_reweighting, acceptance_threshold, bayes_iteration, chi2_strict_pip, correction_method, dcfid_el, dcfid_pip, dcfidref_el, dcv_el, dvz_pip, ecband_el, ecthr_el, noSmear, no_pip_testdc, no_sector_pcal, no_valerii_knockout, pcalvol, phi_bins, rho0_subtraction.
Not combined: electron_sector, pion_sector.
Quadrature A median 17174.923 max 59283.328. B median 0.096063142 max 0.31369964. C median 0.032319298 max 0.16298583.
acceptance_reweighting A median 208.94972 max 1680.8485 (n=1). B median 0.08595496 max 0.31287815. C median 0.025103236 max 0.084213398.
acceptance_threshold A median 2.3981593 max 636.82771 (n=2). B median 0.00021754458 max 0.048972537. C median 0.00017330333 max 0.033486626.
bayes_iteration A median 12.029205 max 892.86827 (n=2). B median 0.00065592637 max 0.050880169. C median 0.00037993423 max 0.041240081.
chi2_strict_pip A median 831.65717 max 6454.3599 (n=1). B median 0.011024653 max 0.12652731. C median 0.0032926901 max 0.057465254.
correction_method A median 291.67786 max 5735.38 (n=1). B median 0.008020669 max 0.067606391. C median 0.0038229157 max 0.060420714.
dcfid_el A median 0.01022034 max 900.3751 (n=2). B median 7.8194909e-07 max 0.04544812. C median 9.2469246e-07 max 0.041240081.
dcfid_pip A median 11.439644 max 712.34893 (n=2). B median 0.001264148 max 0.069340392. C median 0.0009969636 max 0.047287921.
dcfidref_el A median 17.759927 max 870.37784 (n=2). B median 0.0015358101 max 0.051261802. C median 0.0014321209 max 0.03343977.
dcv_el A median 119.98461 max 871.58358 (n=2). B median 0.0013065492 max 0.045385084. C median 0.0012151633 max 0.041240082.
dvz_pip A median 15.888803 max 931.95481 (n=2). B median 0.0008550067 max 0.049616662. C median 0.00051560364 max 0.041240081.
ecband_el A median 10.565377 max 640.75343 (n=2). B median 0.00036253649 max 0.051419352. C median 0.00035038497 max 0.033437704.
ecthr_el A median 21.978125 max 684.9486 (n=2). B median 0.00049347392 max 0.051585734. C median 0.00043330172 max 0.033437611.
noSmear A median 21.24012 max 866.81743 (n=1). B median 0.0015802766 max 0.049097046. C median 0.00093770144 max 0.041240081.
no_pip_testdc A median 92.380904 max 4384.0292 (n=1). B median 0.0047897518 max 0.19208636. C median 0.0046562272 max 0.13106813.
no_sector_pcal A median 152.01609 max 1380.3887 (n=1). B median 0.00039197449 max 0.044987378. C median 0.00037391329 max 0.041240081.
no_valerii_knockout A median 79.211214 max 998.38441 (n=1). B median 0.00053039946 max 0.071846644. C median 0.00045913912 max 0.047287921.
pcalvol A median 43.054208 max 4450.0684 (n=2). B median 0.00016880594 max 0.055041927. C median 0.0001477493 max 0.033664253.
phi_bins A median 17072.767 max 58784.984 (n=1). B median 0.0028832979 max 0.085192285. C median 0.0029610595 max 0.049828924.
rho0_subtraction A median 386.7155 max 1878.0222 (n=1). B median 0.0068213571 max 0.040791877. C median 0.0019521526 max 0.050967379.
electron_sector not_combined A median 638.53505 max 25614.619 (n=1-6, 423 bins). B median 0.03931209 max 642922.19. C median 0.032189365 max 633245.
pion_sector not_combined A median 599.14076 max 25596.12 (n=1-6, 423 bins). B median 0.04673287 max 652628.31. C median 0.034738278 max 642745.39.
Flags: source fit_larger 19825, source systematic_larger 8477, total fit_larger 10, total systematic_larger 1346.

Cross unweighted_versus_spline not_combined. A median 330.52342 max 4509.215 (n=1, 452 bins). B median 0.0089016552 max 0.10661096. C median 0.0062500908 max 0.046697601.

Outputs:
- Systematic_Studies/physics_campaign/comparisons.csv
- Systematic_Studies/physics_campaign/sources.csv
- Systematic_Studies/physics_campaign/totals.csv
- Systematic_Studies/physics_campaign/budgets.json

Normalized copies, mosaics, and kT2 were not regenerated from this budget.
