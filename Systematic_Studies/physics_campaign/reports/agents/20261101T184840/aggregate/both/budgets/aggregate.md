# Agent record
- run_id: 20261101T184840
- stage: aggregate
- campaign: both
- source_or_shard: budgets
- label: aggregate

Both budgets are provisional. The radiative study is enabled and pending, so radiative SF 0, radiative SF 2, and their comparison contribute no number and are not stored as zero. The spline BC alternative stays not_combined and is not stored as zero. Unweighted and Spline totals were not added. Fit_Par_*_ERR is only the denominator of R_source and R_total. No completed row had a missing, zero, or non-finite fit error, so every ratio was written, and no ratio dropped a source. The sum is reduce_source(..., "rms") from Campaign/aggregate_systematics.py, with N inside the square root, then combine_sources(..., "quadrature") of independent sources only. A one-variation source is the absolute difference. An independent recomputation of every source RMS and every campaign quadrature from comparisons.csv matched the tables. Adding a nonzero fit error in quadrature moves the total, and the stored totals do not include it.

A nonempty refinement note, a fit JSON file, or a process return code was not treated as completion. Each nominal and each variation entered only after classify_refinement_dir matched the stated after-quality to the saved fit. Failed or unverified variations: 0. Library tests in Systematic_Studies/test_sidis_physics.py passed before the table was written.

The bin-centering subdivision source has no 15 refined observable shifts (study_state awaiting_observable_shifts, count 0). It was not entered in the Unweighted quadrature, was not copied into Spline, and was not replaced by zero. The bin-centering method and iteration comparisons stay blocked and contribute no number. Bayesian 1D is disabled and contributes no number. Spline 5D is absent and is not zero. Q2-y bins 1 and 5 on the Unweighted 5D comparison are flagged iteration_mismatch (183 completed rows, 61 bins) and remain in that source RMS. Electron and pion sector sources are not_combined. Empty bins are 711 missing comparison rows, not zeroes. The largest unweighted electron-sector B RMS stays out of the total: (Q2_y_Bin_12)-(z_pT_Bin_14) is about 6.31e6 while that bin's quadrature B is about 0.178.

Unweighted versus Spline nominal differences are campaign cross, source unweighted_versus_spline, combine not_combined, and are outside both totals. Reference is the Unweighted nominal and the variation is the Spline nominal.

Comparison rows: 112482. Source rows: 59334. Total rows: 2712. Per-bin source RMS is in sources.csv. The numbers below are the median, minimum, and maximum of that per-bin RMS, not a second reduction. n_shifts is the number of variations inside the RMS. Quadrature totals have no shift count.

Unweighted provisional True. Bins 452.
Reasons: radiative systematic pending; bin-centering method blocked; bin-centering iteration blocked; bin-centering subdivision awaiting observable shifts.
Independent: acceptance_reweighting, acceptance_threshold, bayes_iteration, chi2_strict_pip, correction_method, dcfid_el, dcfid_pip, dcfidref_el, dcv_el, dimension, dvz_pip, ecband_el, ecthr_el, noSmear, no_pip_testdc, no_sector_pcal, no_valerii_knockout, pcalvol, phi_bins, rho0_subtraction.
Not combined: electron_sector, pion_sector.
Quadrature A bins=452 median=16955.938 min=4038.4328 max=59185.266. B bins=452 median=0.10769039 min=0.019905938 max=0.33496817. C bins=452 median=0.03421975 min=0.0059946813 max=0.22956275.
acceptance_reweighting independent A bins=452 median=224.35214 min=0.34293327 max=2665.9585 n_shifts=1-1. B bins=452 median=0.096892177 min=4.2818988e-10 max=0.26427978 n_shifts=1-1. C bins=452 median=0.025892613 min=2.3944462e-06 max=0.11876727 n_shifts=1-1.
acceptance_threshold independent A bins=452 median=2.1875597 min=0.0064596319 max=771.58315 n_shifts=2-2. B bins=452 median=0.00024150405 min=1.125781e-09 max=0.042124103 n_shifts=2-2. C bins=452 median=0.00017886831 min=3.6146066e-12 max=0.04273193 n_shifts=2-2.
bayes_iteration independent A bins=452 median=6.1653435 min=0.092771461 max=766.71254 n_shifts=2-2. B bins=452 median=0.00053275443 min=1.27814e-08 max=0.042236984 n_shifts=2-2. C bins=452 median=0.0004317339 min=3.4940088e-12 max=0.042731933 n_shifts=2-2.
chi2_strict_pip independent A bins=452 median=817.8264 min=0.85085568 max=4886.145 n_shifts=1-1. B bins=452 median=0.010533525 min=6.3632985e-10 max=0.093960932 n_shifts=1-1. C bins=452 median=0.0035367708 min=3.2407112e-12 max=0.054834175 n_shifts=1-1.
correction_method independent A bins=452 median=363.93983 min=0.31349915 max=4776.7348 n_shifts=1-1. B bins=452 median=0.011588136 min=5.7122499e-06 max=0.095236888 n_shifts=1-1. C bins=452 median=0.0048738833 min=1.3359697e-11 max=0.052574973 n_shifts=1-1.
dcfid_el independent A bins=452 median=0.0091711916 min=9.7152224e-09 max=848.46819 n_shifts=2-2. B bins=452 median=8.2076653e-07 min=3.3843928e-11 max=0.054392679 n_shifts=2-2. C bins=452 median=8.2655814e-07 min=3.1757868e-12 max=0.043027946 n_shifts=2-2.
dcfid_pip independent A bins=452 median=12.234534 min=0.15881164 max=835.07262 n_shifts=2-2. B bins=452 median=0.0012486554 min=1.2447635e-10 max=0.045186394 n_shifts=2-2. C bins=452 median=0.0010570758 min=2.2772027e-12 max=0.04273193 n_shifts=2-2.
dcfidref_el independent A bins=452 median=18.112839 min=0.54761026 max=872.75487 n_shifts=2-2. B bins=452 median=0.0015394508 min=8.9291795e-10 max=0.043858403 n_shifts=2-2. C bins=452 median=0.0014088374 min=4.024621e-12 max=0.04273193 n_shifts=2-2.
dcv_el independent A bins=452 median=117.97511 min=5.7954078 max=794.09357 n_shifts=2-2. B bins=452 median=0.0013338099 min=6.0128939e-10 max=0.040868187 n_shifts=2-2. C bins=452 median=0.0012310251 min=3.5429394e-12 max=0.042731932 n_shifts=2-2.
dimension independent A bins=452 median=187.06688 min=0.18465184 max=3458.8148 n_shifts=1-1. B bins=452 median=0.0049544377 min=2.4460832e-09 max=0.077337225 n_shifts=1-1. C bins=452 median=0.003098654 min=1.2973318e-10 max=0.046465257 n_shifts=1-1.
dvz_pip independent A bins=452 median=16.605571 min=0.97256839 max=794.14346 n_shifts=2-2. B bins=452 median=0.00083829341 min=9.7851578e-10 max=0.042381668 n_shifts=2-2. C bins=452 median=0.00057619532 min=3.1335819e-12 max=0.042731931 n_shifts=2-2.
ecband_el independent A bins=452 median=11.163915 min=0.51016154 max=772.05143 n_shifts=2-2. B bins=452 median=0.00036430595 min=4.9078083e-10 max=0.041767719 n_shifts=2-2. C bins=452 median=0.00036463938 min=3.5279814e-12 max=0.042731931 n_shifts=2-2.
ecthr_el independent A bins=452 median=21.824251 min=1.517136 max=747.33349 n_shifts=2-2. B bins=452 median=0.0004709968 min=3.734466e-10 max=0.041620562 n_shifts=2-2. C bins=452 median=0.00043886961 min=3.5030763e-12 max=0.042731931 n_shifts=2-2.
electron_sector not_combined A bins=426 median=617.43187 min=20.511437 max=21093.912 n_shifts=1-6. B bins=426 median=0.038407527 min=0.0082710697 max=6312646.7 n_shifts=1-6. C bins=426 median=0.032134962 min=3.1326105e-09 max=4131144.3 n_shifts=1-6.
noSmear independent A bins=452 median=17.916801 min=0.16691013 max=879.06717 n_shifts=1-1. B bins=452 median=0.0014831596 min=6.3257414e-10 max=0.045645395 n_shifts=1-1. C bins=452 median=0.0010562298 min=2.0321809e-12 max=0.043027944 n_shifts=1-1.
no_pip_testdc independent A bins=452 median=91.96901 min=0.2797142 max=4041.4303 n_shifts=1-1. B bins=452 median=0.0046361854 min=1.6837197e-09 max=0.18504144 n_shifts=1-1. C bins=452 median=0.0049722717 min=2.0808877e-12 max=0.1335991 n_shifts=1-1.
no_sector_pcal independent A bins=452 median=155.90224 min=3.6596288e-05 max=1349.7051 n_shifts=1-1. B bins=452 median=0.00038125206 min=2.3282491e-10 max=0.054392785 n_shifts=1-1. C bins=452 median=0.00044916659 min=3.5526161e-12 max=0.043027947 n_shifts=1-1.
no_valerii_knockout independent A bins=452 median=76.898454 min=3.6596288e-05 max=711.78611 n_shifts=1-1. B bins=452 median=0.00052010864 min=2.7729943e-10 max=0.041943102 n_shifts=1-1. C bins=452 median=0.00047267045 min=3.5157823e-12 max=0.042731931 n_shifts=1-1.
pcalvol independent A bins=452 median=48.12035 min=0.0001170189 max=4369.7162 n_shifts=2-2. B bins=452 median=0.00020480549 min=1.492401e-10 max=0.041096873 n_shifts=2-2. C bins=452 median=0.0001823704 min=3.31231e-12 max=0.042731931 n_shifts=2-2.
phi_bins independent A bins=452 median=16847.69 min=4029.8119 max=58433.409 n_shifts=1-1. B bins=452 median=0.0028047009 min=1.1192157e-10 max=0.073964953 n_shifts=1-1. C bins=452 median=0.0029807133 min=2.5626432e-11 max=0.06230344 n_shifts=1-1.
pion_sector not_combined A bins=426 median=599.12445 min=89.826306 max=21082.472 n_shifts=1-6. B bins=426 median=0.046434189 min=0.0078827589 max=4163585.6 n_shifts=1-6. C bins=426 median=0.035279278 min=1.9542661e-09 max=2716336.6 n_shifts=1-6.
rho0_subtraction independent A bins=452 median=378.68827 min=1.8452244 max=1893.5961 n_shifts=1-1. B bins=452 median=0.0068495223 min=4.5312586e-10 max=0.042216107 n_shifts=1-1. C bins=452 median=0.0020390359 min=3.4711255e-12 max=0.054225059 n_shifts=1-1.
Flags: {"source:fit_larger": 20449, "source:systematic_larger": 9227, "total:fit_larger": 6, "total:systematic_larger": 1350}.

Spline provisional True. Bins 452.
Reasons: radiative systematic pending; bin-centering method blocked; bin-centering iteration blocked; spline 5D blocked.
Independent: acceptance_reweighting, acceptance_threshold, bayes_iteration, chi2_strict_pip, correction_method, dcfid_el, dcfid_pip, dcfidref_el, dcv_el, dvz_pip, ecband_el, ecthr_el, noSmear, no_pip_testdc, no_sector_pcal, no_valerii_knockout, pcalvol, phi_bins, rho0_subtraction.
Not combined: electron_sector, pion_sector.
Quadrature A bins=452 median=17174.923 min=3507.686 max=59283.328. B bins=452 median=0.094835454 min=0.028973468 max=0.37626307. C bins=452 median=0.032355769 min=6.5750017e-08 max=0.21177835.
acceptance_reweighting independent A bins=452 median=208.94972 min=0.59213221 max=1680.8485 n_shifts=1-1. B bins=452 median=0.086023192 min=0.00046927972 max=0.31287815 n_shifts=1-1. C bins=452 median=0.025426192 min=5.3473586e-10 max=0.084213398 n_shifts=1-1.
acceptance_threshold independent A bins=452 median=2.3981593 min=0.009210642 max=1069.6467 n_shifts=2-2. B bins=452 median=0.00021754458 min=2.2414573e-07 max=0.080183886 n_shifts=2-2. C bins=452 median=0.00017528695 min=4.047693e-11 max=0.048010145 n_shifts=2-2.
bayes_iteration independent A bins=452 median=12.295178 min=0.10672753 max=1148.7644 n_shifts=2-2. B bins=452 median=0.00066528082 min=2.2219197e-07 max=0.080183887 n_shifts=2-2. C bins=452 median=0.00039688608 min=6.2467755e-11 max=0.048076627 n_shifts=2-2.
chi2_strict_pip independent A bins=452 median=830.20378 min=10.082226 max=6454.3599 n_shifts=1-1. B bins=452 median=0.010925041 min=0.00010430887 max=0.12652731 n_shifts=1-1. C bins=452 median=0.0033621055 min=4.8716724e-13 max=0.057465254 n_shifts=1-1.
correction_method independent A bins=452 median=291.67786 min=0.42542484 max=6621.6826 n_shifts=1-1. B bins=452 median=0.0078896686 min=2.2416085e-07 max=0.094471157 n_shifts=1-1. C bins=452 median=0.0039015278 min=4.309748e-11 max=0.060420714 n_shifts=1-1.
dcfid_el independent A bins=452 median=0.010350632 min=8.8584784e-10 max=1065.1319 n_shifts=2-2. B bins=452 median=8.8380255e-07 min=8.7041485e-14 max=0.080183885 n_shifts=2-2. C bins=452 median=9.7207394e-07 min=2.133016e-13 max=0.047890875 n_shifts=2-2.
dcfid_pip independent A bins=452 median=11.309015 min=0.21933033 max=1055.91 n_shifts=2-2. B bins=452 median=0.001264148 min=2.2413489e-07 max=0.080183887 n_shifts=2-2. C bins=452 median=0.0009982623 min=6.0720249e-11 max=0.049084027 n_shifts=2-2.
dcfidref_el independent A bins=452 median=17.703532 min=0.19236091 max=1034.9369 n_shifts=2-2. B bins=452 median=0.0015262056 min=2.2414116e-07 max=0.080183886 n_shifts=2-2. C bins=452 median=0.0014355582 min=7.7327464e-11 max=0.047977634 n_shifts=2-2.
dcv_el independent A bins=452 median=120.31938 min=6.3129537 max=1073.3663 n_shifts=2-2. B bins=452 median=0.0013053012 min=2.2414317e-07 max=0.080183889 n_shifts=2-2. C bins=452 median=0.0012144818 min=3.3440133e-10 max=0.048635643 n_shifts=2-2.
dvz_pip independent A bins=452 median=15.906485 min=1.2629524 max=1064.0559 n_shifts=2-2. B bins=452 median=0.00085464421 min=2.2415932e-07 max=0.080183889 n_shifts=2-2. C bins=452 median=0.00052304617 min=6.2043636e-11 max=0.047951026 n_shifts=2-2.
ecband_el independent A bins=452 median=10.586053 min=0.23931344 max=1067.2884 n_shifts=2-2. B bins=452 median=0.00036564687 min=2.2397967e-07 max=0.080183888 n_shifts=2-2. C bins=452 median=0.00035337402 min=2.2801739e-11 max=0.047502469 n_shifts=2-2.
ecthr_el independent A bins=452 median=21.978125 min=2.1466018 max=1070.9756 n_shifts=2-2. B bins=452 median=0.00048983099 min=2.2396361e-07 max=0.080183885 n_shifts=2-2. C bins=452 median=0.00043302587 min=4.6643991e-12 max=0.047981332 n_shifts=2-2.
electron_sector not_combined A bins=423 median=638.53505 min=24.936238 max=25614.619 n_shifts=1-6. B bins=423 median=0.038190439 min=0.0083974287 max=642922.19 n_shifts=1-6. C bins=423 median=0.032929828 min=3.7960959e-08 max=633245 n_shifts=1-6.
noSmear independent A bins=452 median=21.328568 min=0.10516867 max=1115.525 n_shifts=1-1. B bins=452 median=0.0015802766 min=6.8541565e-06 max=0.080183885 n_shifts=1-1. C bins=452 median=0.00095943152 min=8.9934581e-11 max=0.048861734 n_shifts=1-1.
no_pip_testdc independent A bins=452 median=93.477075 min=0.69469874 max=4384.0292 n_shifts=1-1. B bins=452 median=0.0047579631 min=1.168216e-06 max=0.19208636 n_shifts=1-1. C bins=452 median=0.0047039108 min=4.8157901e-12 max=0.13106813 n_shifts=1-1.
no_sector_pcal independent A bins=452 median=154.15428 min=1.8285959e-05 max=1048.4088 n_shifts=1-1. B bins=452 median=0.00038896816 min=6.8741447e-10 max=0.080183892 n_shifts=1-1. C bins=452 median=0.00038877978 min=2.1904602e-10 max=0.045176285 n_shifts=1-1.
no_valerii_knockout independent A bins=452 median=81.758283 min=1.0335225e-05 max=1120.9339 n_shifts=1-1. B bins=452 median=0.0005302371 min=2.0728255e-10 max=0.080183887 n_shifts=1-1. C bins=452 median=0.00045913912 min=1.6376171e-12 max=0.049494252 n_shifts=1-1.
pcalvol independent A bins=452 median=50.941402 min=7.3055094e-05 max=4450.0684 n_shifts=2-2. B bins=452 median=0.00016880594 min=1.113537e-10 max=0.080183886 n_shifts=2-2. C bins=452 median=0.0001517602 min=2.1184745e-10 max=0.047404085 n_shifts=2-2.
phi_bins independent A bins=452 median=17072.767 min=3499.6007 max=58784.984 n_shifts=1-1. B bins=452 median=0.0028636833 min=2.2405666e-07 max=0.085192285 n_shifts=1-1. C bins=452 median=0.0031522998 min=5.0964172e-11 max=0.049828924 n_shifts=1-1.
pion_sector not_combined A bins=423 median=599.14076 min=100.20856 max=25596.12 n_shifts=1-6. B bins=423 median=0.046551523 min=0.0078465397 max=652628.31 n_shifts=1-6. C bins=423 median=0.035591506 min=0.0018619048 max=642745.39 n_shifts=1-6.
rho0_subtraction independent A bins=452 median=385.76242 min=4.4847868 max=1878.0222 n_shifts=1-1. B bins=452 median=0.0068887504 min=4.5475281e-06 max=0.080183884 n_shifts=1-1. C bins=452 median=0.0020094423 min=3.151338e-10 max=0.050967379 n_shifts=1-1.
Flags: {"source:fit_larger": 19740, "source:systematic_larger": 8562, "total:fit_larger": 8, "total:systematic_larger": 1348}.

Cross unweighted_versus_spline not_combined. A bins=452 median=330.52342 min=0.81128817 max=5395.5176 n_shifts=1-1. B bins=452 median=0.0089513054 min=4.9803308e-05 max=0.14636477 n_shifts=1-1. C bins=452 median=0.006316472 min=1.532079e-09 max=0.046697601 n_shifts=1-1.

Outputs:
- Systematic_Studies/physics_campaign/comparisons.csv
- Systematic_Studies/physics_campaign/sources.csv
- Systematic_Studies/physics_campaign/totals.csv
- Systematic_Studies/physics_campaign/budgets.json

Normalized copies, mosaics, and kT2 were not regenerated from this budget.
