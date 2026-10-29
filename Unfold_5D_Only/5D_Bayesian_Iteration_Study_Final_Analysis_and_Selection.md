# 5D Bayesian Iteration Study: Final Analysis and Selection

Date: 2026-10-28.

This note uses the finished 5D iteration-study file. The study was not rerun, and no nominal 5D unfolding was launched. `iteration_study_errors.root` and the two execution logs were opened read-only.

Three kinds of statement are kept separate below. **Observed** means a value read from the ROOT file or a log. **Conclusion** means a result of the existing stability scorer applied to those values. **Not done** means work that was left for a later decision.

## A. Execution Summary

### Observed run

The orchestrator log records this command, started 2026-10-24 18:10:04:

```text
python3 run_Dedicated_5D_Unfold.py -droot work_b \
  -sfin .../SIDIS_epip_Response_Matrices_from_RDataFrames_Only_5D_SIDIS_Workflow_Bank_Response_Matrices_Final_Thesis_Files_All.root \
  -r .../Unfold_5D_Only/iteration_study_errors.root \
  --iteration_study --study_only --error_mode errors \
  --parm_min 1 --parm_max 10 --parm_step 1 \
  --background_source lundvpk \
  --Min_Allowed_Acceptance_Cut 0.020 --phi_bins 24 --email
```

The input named in `Unfold_5D_Only/summary.txt` is that same 5D response file.

The C++ scan is the clone-free loop in `Dedicated_5D_Unfold.cxx`. Each integer `k` builds a new `RooUnfoldBayes` on the same response and calls `Hunfold` with the requested error treatment. `RooUnfoldParms` is not used. The loop writes one bin centered on each integer `k`. For `parm_min = 1`, `parm_max = 10`, and `parm_step = 1`, the axis is `[0.5, 10.5]` with 10 bins.

Logged configuration:

- Error treatment: `errors` (`RooUnfold::kErrors`). Toy count stayed at the unused default of 10.
- Background subtraction for this study: `lundvpk`.
- Acceptance cut: 0.020.
- `phi_bins`: 24.
- Auto-detected 5D bookkeeping: increment 434, `num_bins` 10850, `num_slices` 25.
- Reconstructed-bin reduction printed twice: original 10850, reduced 9851.
- Generated axis used for the residuals: all 10850 generated bins. The mean-residual profile has 10850 entries in every `k` bin.
- `--study_only` was set. The log ends with `study_only: scan finished. Nominal Hunfold was not run.`

The email dump at the end of the log also records `--bayes_iterations --> 6`. That was the launcher default when this job was submitted. It is not the scan. The scan is `parm_min` through `parm_max`. Because `study_only` skipped the nominal `Hunfold`, iteration 6 was not applied as a saved unfolded result.

### Stages and runtime

| Marker | Time |
| --- | --- |
| Process start | 2026-10-24 18:10:04 |
| `k=1` start | 2026-10-24 18:10:24 |
| `k=8` finished, `k=9` start | 2026-10-26 19:09:18 |
| `k=10` finished, profiles ready, study_only stop | 2026-10-28 02:44:55 |
| Script's own elapsed line at that stop | 3 days, 8 hours, 34 minutes, 41 seconds |
| `Done Saving` | 2026-10-28 08:55:26 |

The save after the profiles were ready took about six hours. The process then printed the usual finished-unfolding email block.

### Warnings and the log gap

Observed warning: `Multiple 5D matrix configurations found; using increment=434, num_bins=10850, num_slices=25`. The job continued with that choice.

The iteration log contains this handwritten line just after the `k=9` RooUnfold iteration-4 message:

```text
... (Lost logs during run? Manually copying end of the run for below)
```

After that note, the file has a copied tail: RooUnfold iterations 0 through 9, `Chi^2 of change` falling from `3.67864e+06` to `23.7805`, then `Calculating covariances due to number of measured events`, then `Iteration-study k=10 finished`. There is no separate `Iteration-study k=9 finished` line and no separate `Iteration-study k=10` start line. Those lines sit in the gap described by the note.

That RooUnfold `Chi^2 of change` is the internal iteration monitor. It is not `Iteration_Study_Chi2`.

The four saved profiles each have bins at `k = 1` through `k = 10`, and every mean-residual bin has 10850 entries. The missing log lines are a logging gap. They are not missing iterations in the ROOT file.

No crash, null `Hunfold`, or failed-save message is present after the profiles are declared ready.

### What this run is, and what the new defaults are

Observed: this file is the `lundvpk`, acceptance 0.020, `error_mode=errors` scan. Future nominal subtraction and MC-weight defaults are `rho0_new`. Those defaults do not rewrite this file, and this note does not treat the file as a `rho0_new` study.

## B. Diagnostic Results

### Definitions in the C++ loop

For each `k`, the unfolded histogram is compared with `MC_GEN` on the generated axis (`nt = 10850`):

- `Iteration_Study_Chi2` (`TProfile`): one fill per `k` of `sum (residual^2 / error^2)` over generated bins whose unfolded error is positive. The scored value is the bin content.
- `Iteration_Study_MeanResiduals` (`TProfile`): one fill per generated bin of `unfolded - MC_GEN`. The bin content is the signed mean residual. Scoring uses the absolute value. `GetBinError` is the error on that mean. That error is the residual-mean error used by the scorer.
- `Iteration_Study_RMSResiduals` (`TH1D`): `sqrt(mean of residual^2)`. It is aligned with `k`, and it is not a selection input. Its content is about `1.38e8`, far from the profile error on the mean.
- `Iteration_Study_RMSError` (`TProfile`): one fill per `k` of the average unfolded bin error, `sum(GetBinError) / nt`. The name is historical. The plotted quantity is the mean bin error. It is a cost diagnostic, not a selection input.

The signed mean residual is negative at every `k` (about `-1.4665e6` to `-1.4691e6`). The absolute-value convention is required. Using the profile content directly would flip the residual curve.

### Values and normalized steps

`d_M(k) = |M(k+1) - M(k)| / (max M - min M)` on the scanned values of that metric. A blank `d` means `k` has no following iteration. `step_stable` is 1 only when all three selection metrics have `d <= 0.03`. `C_E = (mean bin error) / (minimum mean bin error) - 1`. The minimum mean bin error is at `k = 1`.

The same rows are in `Unfold_5D_Only/5D_iteration_stability_scores.tsv`. `rms_residual_not_used` in that file is the unused RMS histogram.

| k | χ² | \|μ\| | σ_μ | Mean bin error | d_χ² | d_\|μ\| | d_σ | Stable step | In run | C_E |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 6.079078339e9 | 1.466467477e6 | 1.322043853e6 | 301.771 | 0.6934 | 0.7125 | 0.7088 | no | no | 0 |
| 2 | 3.108919674e9 | 1.468328826e6 | 1.323888863e6 | 435.214 | 0.1647 | 0.1778 | 0.1796 | no | no | 0.442 |
| 3 | 2.403411370e9 | 1.468793378e6 | 1.324356480e6 | 507.918 | 0.06585 | 0.05759 | 0.05847 | no | no | 0.683 |
| 4 | 2.121351859e9 | 1.468943831e6 | 1.324508675e6 | 550.111 | 0.03261 | 0.02408 | 0.02452 | no | no | 0.823 |
| 5 | 1.981690125e9 | 1.469006743e6 | 1.324572495e6 | 575.837 | 0.01814 | 0.01213 | 0.01238 | yes | yes | 0.908 |
| 6 | 1.904003263e9 | 1.469038441e6 | 1.324604725e6 | 592.157 | 0.01086 | 0.00691 | 0.00706 | yes | yes | 0.962 |
| 7 | 1.857487102e9 | 1.469056482e6 | 1.324623098e6 | 602.858 | 0.00685 | 0.00426 | 0.00435 | yes | yes | 0.998 |
| 8 | 1.828155558e9 | 1.469067606e6 | 1.324634434e6 | 610.077 | 0.00449 | 0.00278 | 0.00284 | yes | yes | 1.022 |
| 9 | 1.808920564e9 | 1.469074862e6 | 1.324641827e6 | 615.070 | 0.00304 | 0.00189 | 0.00193 | yes | yes | 1.038 |
| 10 | 1.795904873e9 | 1.469079801e6 | 1.324646857e6 | 618.602 |  |  |  | edge | yes | 1.050 |

### How the curves move

χ² falls by about a factor of 3.4 from `k = 1` to `k = 10` (`6.08e9` to `1.80e9`). The drop is steep through `k = 3` and then slows. It is still falling at `k = 10`. The absolute χ² is not read as a p-value. With 10850 generated bins and a residual that stays near `1.47e6`, a large χ² is expected. The scorer uses only the normalized step.

\|μ\| and σ_μ rise by a few parts in `10^3` across the whole scan and are almost flat after `k = 4`. The full \|μ\| span is about 2600 on an offset of about `1.469e6`. A small normalized step means the iteration dependence has flattened. It does not mean the residual itself is small.

Mean bin error rises at every step, from 302 at `k = 1` to 576 at `k = 5` and 619 at `k = 10`. Extra iterations buy a smaller χ² step and cost a larger average bin error. From `k = 5` to `k = 10` the mean bin error grows by about 7 percent, while `C_E` goes from 0.91 to 1.05.

The near-constant test (`span <= 10^{-4} |M(k=1)|`) does not fire. All four curves move by more than that fraction of their `k = 1` value, so every step is judged by the 0.03 threshold.

The three selection curves agree on the stable interval. The only disagreement at the boundary is the `k = 4` step: `d_|μ|` and `d_σ` are already under 0.03, and `d_χ² = 0.03261` is just over it. That one metric keeps `k = 4` out of the stable run.

## C. Iteration Selection

### Rule

The scorer is `score_curve` / `recommend` in `score_data_iteration_stability.py`, with `STEP_MAX = 0.03`, `RUN_LEN = 3`, and `STABLE_REL = 1e-4`.

A step `k → k+1` is stable when χ², \|μ\|, and the residual-mean error each change by at most 3 percent of that curve's full scanned range. The first time three such steps are consecutive, the supported iterations are the first step's `k` through one iteration past the last stable step. Later adjacent stable steps extend that run. The selected iteration is the smallest supported `k`. Status `ok` requires the supported set to be one contiguous block.

`plot_iteration_study.select_5d_iteration` (the older median-of-three rule) was not used.

### Conclusion

`recommend` returned `status = ok`, `k_selected = 5`, supported iterations `5,6,7,8,9,10`.

`k = 5` is the earliest iteration that starts a run of at least three stable steps (`5→6`, `6→7`, `7→8`). The run continues through `9→10`, so `k = 10` is inside the supported set as the iteration after the last stable step. `k = 4` is excluded because `d_χ²` on the `4→5` step is 0.03261. A later choice such as 6 or 7 is also inside the stable window, and the mean bin error is higher there. The rule keeps the earliest supported iteration.

The scan is long enough for this rule. A three-step window that ends at `k = 10` can select as late as `k = 7`. The selected point, `k = 5`, is inside the scan, with five stable steps after it rather than the minimum of three.

### What this does not show

This is stability of the diagnostic curves against `MC_GEN` on the generated axis. It is not a closure test, and it is not a demonstration that the unfolded cross section is unbiased. No closure sample was unfolded for this decision.

## D. Figures

### File

`Unfold_5D_Only/Iteration_Tests_5D_Diagnostics_for_Experimental_Data_020_AccCut_lundvpk.pdf`

One page, 468 by 458 pt (6.50 by 6.36 in), from `gStyle.SetPaperSize(16.5, 16.5)` and a 1200 by 1200 canvas. Four panels in a 2×2 grid. No `TLegend` and no legend pad. Curves are the original diagnostic values, with the absolute value for the mean residual. Both ROOT grids are on. Line width is 2. A red vertical line is drawn at `k = 5`. Axis limits are `k` from 0.5 to 10.5 and each y-axis is the data range plus an 8 percent pad.

Titles are χ², Absolute Mean Residual, Residual-Mean Error, and Mean Bin Error. Mathematical y labels are `|#mu|` and `#sigma_{#mu}`. The subtitle is `Based on Unfolding Tests with 2% Acceptance Cuts`.

Regenerate with:

```text
/Users/richardcapobianco/opt/miniforge3/envs/updated_python/bin/python -u Unfold_5D_Only/plot_5d_diagnostics.py
```

The script rereads the ROOT file, runs the same scorer, and exits without drawing if the status is not `ok` or the selected iteration is not 5.

### Inspection

The PDF was rendered and read at that page size. The four panels are separate and fill the page. Tick labels run from 1 to 10. The subtitle text contains `2%` and does not contain `2%%`. Extracted text includes `Absolute Mean Residual`, `Residual-Mean Error`, `Mean Bin Error`, `|#mu|` as `|µ|`, and the residual-mean-error label as `σ` with `µ`. χ² is drawn with the ROOT `#chi^{2}` glyph. The χ² y-axis is scaled by `10^6` (about 1500 to 6000). The two residual panels are scaled by `10^3`. The mean-bin-error panel is unscaled, about 300 to 620. The red line sits on iteration 5 in each panel. No clipped title or axis label was visible at this size.

## E. Code and Configuration Updates

Nominal 5D unfolding now defaults to 5 iterations. An explicit `--bayes_iterations` on `run_Dedicated_5D_Unfold.py`, `Dedicated_5D_Unfold.py`, or the C++ binary still replaces that default. Scan bounds stay `--parm_min 1` and `--parm_max 10`. The 3D per-bin lookup is unchanged, including the ±1 systematic neighborhood around those 3D values. No 5D lookup row was written.

`rho0_new` stays the default for `--background_source` and is now also the default for `--rho0_source`. `lundvpk`, `lundrho`, and `None` remain explicit background choices. `lundvpk` and `lundrho` remain explicit weight choices. Weight formulas were not changed. Acceptance 0.020 was not changed.

### Files

| File | Previous nominal value | Now |
| --- | --- | --- |
| `Cpp_Dedicated_5D_Unfold/Dedicated_5D_Unfold.cxx` | 5D branch `bayes_iterations = 4` | `5`. `args.bayes_iterations` still overrides it. |
| `run_Dedicated_5D_Unfold.py` | `--bayes_iterations` default 6 | default 5. The launcher always forwards the flag. |
| `Dedicated_5D_Unfold.py` | argparse default 6, and the 5D branch set 4 | both are 5. `if(args.bayes_iterations)` still overrides the branch. |
| `Campaign/run_sidis_campaign.py` `k_for` | 5D read the lookup | `k_for("5D", ...)` returns `(5, provenance)` before the lookup. 3D still reads the lookup. |
| `Campaign/run_sidis_campaign.py` `iteration_study_command` | 5D background was fixed in the command | the command takes the campaign `-bg` value. Parm limits stay 1 to `k_max`. |
| `Campaign/local_orchestrator.py` `run_unfold` | 5D background was fixed | 5D argv uses `k_for("5D")` and `args.background_source`. |
| `Campaign/local_orchestrator.py` `run_iteration` | 5D background was fixed | 5D study argv appends `args.background_source`. |
| `Campaign/local_orchestrator.py` `five_d_study_argv`, `five_d_nominal_argv` | background fixed | both take a background argument. Callers pass `args.background_source`. Study argv is still `error_mode errors`, parm 1–10. Nominal argv is still `error_mode covariance`. |
| `Campaign/local_orchestrator.py` `run_unfold_5d_only` | called `select_5d_iteration` | sets `k_value = 5` and logs `nominal 5D k 5`. This function was not executed. |
| `Campaign/local_orchestrator.py` `acceptance_commands` | `--rho0_source lundvpk` | `--rho0_source rho0_new`. |
| `Histo_Files_ROOT/DataFrames/Acceptance_Weights_Creations_using_RDataFrames.py` | `--rho0_source` default `lundvpk` | default `rho0_new`. |
| `Histo_Files_ROOT/DataFrames/Submit_Full_Histogram_Creation_Pipeline.py` | `--rho0_source` default `lundvpk` | default `rho0_new`. |

`Campaign/early_chain.py` `iteration_5d` was already a fixed command string with `--background_source rho0_new`. It has no background switch, and it was left as it is.

New files, both under `Unfold_5D_Only/`:

- `plot_5d_diagnostics.py`
- `Iteration_Tests_5D_Diagnostics_for_Experimental_Data_020_AccCut_lundvpk.pdf`
- `5D_iteration_stability_scores.tsv`
- this report

### Overrides that exist, and overrides that do not

Checked without starting a job:

- `run_Dedicated_5D_Unfold.py` with no extra flags builds a C++ command with `--bayes_iterations 5` and `--background_source rho0_new`. Adding `--bayes_iterations 9 --background_source lundvpk` puts 9 and `lundvpk` on that command.
- `Dedicated_5D_Unfold.py` parses the same way: default 5 and `rho0_new`; the same two flags parse as 9 and `lundvpk`.
- `k_for("5D", "0.020", None, "current_binning")` returns `(5, "current_binning")`.
- `k_for("3D", "0.020", 1, "current_binning")` returns `(6, "current_binning")`.
- `five_d_nominal_argv(..., 5)` contains `--bayes_iterations 5` and `--background_source rho0_new`. The same call with background `lundvpk` contains `lundvpk`.
- `five_d_study_argv` keeps `--parm_min 1 --parm_max 10 --parm_step 1` and `--error_mode errors`, and it carries the background argument it is given.
- `run_unfold` for 5D, dry-run only, prints `--bayes_iterations 5` with `--background_source rho0_new`, and prints `lundvpk` when `-bg` is `lundvpk`. Neither call launched a process.
- `acceptance_commands("work")` contains `--rho0_source rho0_new` and does not contain `lundvpk`.

The campaign CLI has `-bg` / `--background_source` (default `rho0_new`). Where a 5D command builder already had `args` in scope, that value is now passed through. The campaign flag `-k` / `--iteration_action` is only `use_lookup` or `refresh`. It is not an iteration count. There is no campaign flag for a 5D iteration count, and none was added. A campaign 5D unfold passes 5. A different count has to be given to the launcher with `--bayes_iterations`.

There is no campaign `--rho0_source` flag, and none was added. Another MC-weight source has to be requested on `Acceptance_Weights_Creations_using_RDataFrames.py` or `Submit_Full_Histogram_Creation_Pipeline.py` with `--rho0_source`.

### Binary not rebuilt

`Cpp_Dedicated_5D_Unfold/Dedicated_5D_Unfold` is dated 2026-10-26. `Dedicated_5D_Unfold.cxx` is dated 2026-10-28. The binary was not rebuilt. Every nominal path found above goes through `run_Dedicated_5D_Unfold.py`, which always puts `--bayes_iterations` on the command, so those paths pass 5 even with the older binary. A direct run of the binary that omits `--bayes_iterations` still uses whatever default was compiled on 2026-10-26. Rebuilding was not done here.

### Not done

- The 5D iteration study was not rerun.
- Nominal 5D unfolding was not started.
- No closure test was run. Diagnostic stability is not closure.
- The 3D iteration choice, the 3D lookup, and the existing 3D thesis figures were not changed.
- `iteration_study_errors.root` and the two logs were not modified.
