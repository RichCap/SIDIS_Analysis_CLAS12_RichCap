# SIDIS 3D systematic campaign

Launcher:

`Campaign/run_sidis_systematics_campaign.py`

The command prepares 34 Phase 1 response-matrix configurations and 7 nominal-only unfolding branches. It does not start work unless `--dry_run` is omitted. A production run still has to be authorized separately.

## Flags

| Flag | Default | Meaning |
|---|---|---|
| `-c` / `--campaign` | `systematics_3d` | Run name used in the work directory, log, and output names |
| `-droot` / `--data_root` | `work_b` | Analysis data root |
| `-wm` / `--weight_mode` | `unweighted` | Phase 2 response for the 33 non-nominal configurations: `unweighted`, `weighted` (spline), or `both` |
| `-rnh` / `--regenerate_nominal_spline_hpp` | off | Write a new nominal spline HPP file. Do not overwrite the existing HPP products |
| `-mlw` / `--max_local_workers` | `41` | Local histogram plus unfold workers. Values above 41 are rejected. A lower value staggers local work only |
| `-n` / `--dry_run` | off | Print commands and write the manifest. No `sbatch` and no histogram or unfold process |
| `-rs` / `--resume` | off | Continue a campaign directory. Completed outputs stay. Recorded HPP paths are reused |
| `-e` / `--email` | off | Configuration-level start, success, and failure mail. No per-bin mail |
| `-ht` / `--hpp_tag` | `Final_Thesis` | Tag for the existing `noSpline` and `withSpline` HPP files |
| `-em` / `--email_message` | empty | Extra text printed at startup |

Nominal Phase 2 always reads the `AccSpline` histograms. `--weight_mode` does not change that. `AcceptanceWeightVariation` reads `Spline` from the same nominal file.

## What is scheduled

Phase 1 is one hybrid Only_3D run per stored cut, all with Bank matching. The strict π⁺ χ² configuration is `cut_Complete_SIDIS_chi2_strict_pip`. Smearing-off uses `cut_Complete_SIDIS_noSmear` and `--unsmeared`. Each configuration keeps the four MC histogram variants: unweighted, `Acc`, `Spline`, and `AccSpline`.

Phase 2 branches, from the nominal response only: `BayesMinus1`, `BayesPlus1`, `Acc015`, `Acc025`, `Phi12`, `NoRho0`, `AcceptanceWeightVariation`. Six-bin φₕ merging is not available in the current unfolder, so it is not scheduled.

## HPP regeneration

Leave `-rnh` off unless the spline weights have changed. When it is on:

- Only the nominal spline-weighted HPP product is created.
- The new file is `generated_acceptance_weights_<tag>_withSpline_sysregen_<campaign>_<stamp>.hpp`.
- The existing noSpline and withSpline files are not modified.
- The other 33 configurations start immediately on the existing pair.
- The nominal histogram job waits for the new file and then uses it as the withSpline input.
- The manifest stores both paths for every configuration. Resume passes those paths through and does not look the tag up again.

## Commands

Dry run:

```bash
python Campaign/run_sidis_systematics_campaign.py -n -c systematics_3d -droot work_b
```

Both weighting modes, still a dry run:

```bash
python Campaign/run_sidis_systematics_campaign.py -n -wm both -c systematics_3d -droot work_b
```

Resume:

```bash
python Campaign/run_sidis_systematics_campaign.py -rs -c systematics_3d -droot work_b
```

Optional nominal spline HPP, dry run:

```bash
python Campaign/run_sidis_systematics_campaign.py -n -rnh -c systematics_3d -droot work_b
```

## Outputs

The campaign directory is `<data_root>/SIDIS_Campaign/systematics/<campaign>/` when that data root is mounted, otherwise `/tmp/SIDIS_systematics_campaign/<data_root>/<campaign>/`.

- `manifest.json` records status, HPP paths, SLURM ids, and output paths.
- `campaign.log` is the shared log.
- Phase 1 merged files stay on the existing hadd path. The name contains `Sys3D_<id>_Bank` and the cut when the cut is not nominal.
- Phase 2 writes one file per Q²–y bin under `unfold_parts/`, then one merged file under `unfolded/`.
- `final/` receives only complete merged unfolded files.

`--weight_mode unweighted` or `weighted`: 41 SLURM arrays, 697 tasks, 41 final unfolded files.

`--weight_mode both`: 74 SLURM arrays, 1258 tasks, 74 final unfolded files. The two local unfolds for one configuration run one after the other. The local-worker cap stays 41.

## Local workers

The cap counts one local histogram batch or one local unfold process. Controllers are not counted. Phase 1 still uses its existing hybrid scheduler with `--jobs_3D 1`. Phase 2 waits 60 seconds after the array submission, takes over only a task whose SLURM state is `PD`, and cancels that task only after a local slot is free and a second check still shows `PD`.

## Strict χ² definition

`cut_Complete_SIDIS_chi2_strict_pip` is used as stored. `CHI2PID_CUT_strict_pip` in `ExtraAnalysisCodeValues.py` (lines 2744–2751) uses coefficient 0.88 and compares `PID_chi2pip` with a three-piece function of electron momentum `el`. That note does not change the cut.

## Fixed-list histogram recovery

`Campaign/recovery_batches_systematics_3d_both_rnh_20261027.json` is the execution list: 33 non-nominal configurations and 1,580 batch tasks. `13660240_156`, `_157`, and `_158` are absent. `13660242_108`, `13660241_112`, and `13660241_111` are absent because those tasks finished. Nominal is not in this list.

`-rb` / `--recovery_batches` reads that file and does not discover more indices. It rejects `-rnh`. Phase 1 is one Only_3D `slurm` submission per listed configuration, with `--batch_ids`, `--hybrid_date 10_27_2026`, `--slurm_time 24:00:00`, and `--only3d_slurm_mem 4500M`. `-rlb` removes only that array task’s own batch file and skips the outside-batch ROOT gate. Unlisted batches are not submitted. After the listed array finishes, the existing pipeline hadd still requires all 171 batch files. A failed merge does not unfold that configuration. A successful merge continues into Phase 2 with `--weight_mode both`.

`-o3m` / `--only3d_slurm_mem` changes only the Only_3D memory request. Leave it unset and that request stays 4GB.

Submissions are appended to `<campaign>/submission_history.jsonl`. Earlier lines are not rewritten. A configuration failure mail names the campaign, the configuration, the recorded SLURM ids, and the recovery batch list.

The second campaign name is `systematics_3d_both_recovery_20261028`. Its manifest, log, and JSONL are separate. Histogram batches and the merged response file stay on the original `Sys3D_<id>` paths.

Every original non-nominal job has finished. Only the nominal spline HPP generation is still active. Do not interrupt that run, and do not resume the original campaign onto these batch files. This launcher does not look for processes and does not cancel them.

On iFarm, `sinfo -p production -o "%P %l"` must show a maximum of at least 24 hours. If it does not, stop and report that. Do not shorten the request in the command.

A later file, `Campaign/recovery_batches_20261029.json`, is a separate campaign. Empty `batches` skips histogram submission and the merge, then checks the merged response and unfolds. `defer_merge` submits only the listed batches and does not hadd. Phase 2 stdout and stderr go to `/farm_out/richcap/`. Nominal stays out.

## Complete 3D campaign

`Campaign/recovery_batches_complete_20261029.json` with `-incn` / `--include_nominal` is one submission. The campaign id is `systematics_3d_complete_20261029`. The three ids already used are refused for a live run. `-rnh` stays rejected. The October 29 recovery file is unchanged.

Nominal histograms use `Sys3D_nominal_complete_20261029`, the existing Final_Thesis HPP pair, and the acc020 spline-weight file. They do not regenerate HPP files. After that merge passes the 17-bin plain and `_(Spline)` object check, Phase 2 submits the original AccSpline Bayesian branch, the seven variation branches, Bayesian Unweighted, and bin-by-bin Spline and Unweighted. Spline Bayesian is `AcceptanceWeightVariation` only. Bin-by-bin calls `Simple_RooUnfold_SelfContained.py -u3D -bbo` and returns the measured/acceptance correction before RooUnfold. The local-worker ceiling for `-incn` is 43. Without `-incn` the ceiling stays 41.

`dvz_loose_pip` has an empty batch list and `external_merge`. The coordinator does not hadd it. A pause in file growth stays pending. Phase 2 starts after two object-check passes at the same size. `ecband_tight_el` and `ecthr_tight_el` still submit only their listed batches with `-dfm`. The same coordinator hadds them after all 171 batch files are valid on two successive reads, then starts Phase 2. No resume command is required. `pipS6o` stays on its selective non-deferred route.

5D unfolding and the spline Only_5D histogram job are not part of this command.

## Spline and noSmear Phase 2 recovery

`-suo` / `--shared_unfold_output` writes part files and finals into `systematics_3d_complete_20261029`, even when `-c` is a new id. A recovery entry may set `phase2_weights` to `spline`, `unweighted`, or `both`. That choice overrides `-wm`.

Before a Spline array is submitted, each `q2yNN_WSpline.root` part is opened. It is reused only when it has a `_(Bayesian)_` histogram for that Q²–y bin, `error_mode=covariance`, and the configuration's merged response in `Latest_List_of_File_Names`. Nonempty size is not enough. Only bins that fail those checks are submitted. If every bin passes, the existing parts are hadded and a final that already passes is left as it is.

`noSmear` Phase 2 passes `--no_smear`. A kept `noSmear` histogram must not contain `SMEAR=Smear`.

`Campaign/recovery_batches_phase2_spline_nosmear.json` is Spline-only for the 30 finished Unweighted configurations and both weights for `noSmear`. `dvz_tight_pip` and `pipS6o` are not in it.

Prepared command for the 28 October list, not launched by this repository change. Run it from the iFarm checkout:

```bash
python3 Campaign/run_sidis_systematics_campaign.py -c systematics_3d_both_recovery_20261028 -droot work_b -wm both -rb Campaign/recovery_batches_systematics_3d_both_rnh_20261027.json -e
```
