# Theory-figure invocation, 9 November 2026

These commands were recovered from the session log `call-5401a6a4-5d71-4497-b026-feb21e43332e-83.log`. They wrote the theory PDFs now in the two version trees. An earlier call in `call-3f28da44-eeca-445b-95e9-2c33d1bcbbb7-71.log` omitted `--skip_measured_regression` and stopped on the measured-median check. This note is not part of either thesis.

Working directory: `SIDIS_Analysis_CLAS12_RichCap`

Interpreter: `/Users/richardcapobianco/opt/miniforge3/envs/updated_python/bin/python`

Script: `Systematic_Studies/physics_campaign/redraw_theory_figures_stepped.py`

Version A:

```text
python Systematic_Studies/physics_campaign/redraw_theory_figures_stepped.py \
  --json_file Systematic_Studies/physics_campaign/corrected/spline/normalized_bc_no_chi2_pid.json \
  --image_dir Actual_Thesis_LaTeX_Projects/LaTeX_GitHub/Richard_Capobianco_PhD_Thesis_VersionA_no_chi2_pid/Conclusions/Comparison_Images \
  --skip_measured_regression
```

Version B:

```text
python Systematic_Studies/physics_campaign/redraw_theory_figures_stepped.py \
  --json_file Systematic_Studies/physics_campaign/corrected/spline/normalized_bc_no_chi2_pid_no_reweight.json \
  --image_dir Actual_Thesis_LaTeX_Projects/LaTeX_GitHub/Richard_Capobianco_PhD_Thesis_VersionB_no_chi2_pid_no_reweight/Conclusions/Comparison_Images \
  --skip_measured_regression
```

`--skip_measured_regression` bypasses the script's stored measured-median targets, median B = −0.081220013228 and median C = −0.004871686379, and the three residual-RMS targets. The live normalized file and both version files share the current central values. Their medians are B = −0.0817730079869 and C = −0.00496882503369. The theory-curve checks remained active and passed, including the published widths 0.25 and 0.20 GeV². All 452 central values and statistical uncertainties in each version JSON matched the live normalized file.
