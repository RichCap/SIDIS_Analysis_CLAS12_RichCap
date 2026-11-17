# Q2-y = 1 unweighted-fake validation

## Implementation checked

- C++ and Python select the untagged `Background_Response_Matrix_1D` key from the same signal-MC file.
- Known signal weight tags (`Spline`, `JSON`, acceptance combinations, and legacy `Weighed`) are removed only from the fake-background key. Production base weights embedded in the untagged histogram are retained.
- The experimental rho0 subtraction path is unchanged.
- RooUnfoldBayes fake handling is unchanged.
- The signal generated-column correction is unchanged.
- C++ slice histograms now allocate `Sumw2` before filling, preventing ROOT's implicit `sqrt(content)` error from being added to the copied dense-bin uncertainty.

## Python/C++ bin-by-bin parity

Correction off, identical inputs and no acceptance mask:

- Dense 1D: 698/698 contents and 698/698 errors match exactly.
- 29 Q2-y=1 z-pT slices: 696/696 contents and 696/696 errors match exactly.
- The prior first-phi-bin error discrepancy was the C++ slice `Sumw2` issue described above.

Column-corrected case:

- An independent Python reference repeated edge alignment, fake addition, acceptance division, data division, and the preserved mask using the saved column-corrected reconstructed/generated histograms.
- Dense 1D: 698/698 contents and errors match C++ exactly.
- 29 slices: 696/696 contents and errors match C++ exactly.
- The production Python `DivUnw` mode remains a different legacy correction (histogram-wise division), not the generated-column correction: 669/698 active dense bins differ. It was not rewritten in this narrow fake-background change.

## Repaired versus saved faulty corrected bin-by-bin

- Saved faulty integral: 7,100.3977.
- Repaired integral: 12,934,534.0397.
- Completed nominal Bayesian integral: 14,965,175.8963.
- Repaired/Bayesian integral ratio: 0.86431; faulty/Bayesian: 0.00047446.
- Median content difference from nominal Bayesian improves from 99.945% (faulty) to 8.914% (repaired).
- Median error difference improves from 99.833% to 27.472%.
- Median fitted-parameter differences from Bayesian improve as follows:
  - A: 99.956% to 9.653%.
  - B: 71.549% to 13.423%.
  - C: 111.182% to 29.164%.

Per-slice A/B/C values and fit errors are in `fits/q2y1_fit_parameters.json`.

## Bayesian before/after fake-background selection

- Old mask: 86 excluded reconstructed bins.
- New unweighted-fake mask: 88 excluded bins.
- New exclusions: bins 18 and 22; no bins were restored.
- With the old mask held fixed, old and new dense Bayesian contents and errors are exactly identical in all 698 bins. This confirms that the fake histogram is not otherwise consumed by RooUnfoldBayes.
- With the new mask, the two newly excluded bins dominate the visible change. Excluding those membership changes, the median content shift is 3.25e-7 and the maximum is 1.142%; the median error shift is 7.15e-8 and the maximum is 2.730%.
- The rho0-subtracted data histogram is exactly identical before/after in all 698 contents and errors.

## Artifacts

- Full machine-readable comparison: `q2y1_comparison_report.json`
- Per-slice fit results: `fits/q2y1_fit_parameters.json`
- Correction-off and corrected parity: `plots/python_cpp_binbybin_parity_q2y1.pdf`
- Repaired/faulty/Bayesian comparison: `plots/binbybin_repaired_vs_faulty_and_bayes_q2y1.pdf`
- Bayesian fixed-mask isolation: `plots/bayesian_unweighted_fake_mask_isolation_q2y1.pdf`
- Independent corrected Python reference: `python_reference_corrected_binbybin.root`
