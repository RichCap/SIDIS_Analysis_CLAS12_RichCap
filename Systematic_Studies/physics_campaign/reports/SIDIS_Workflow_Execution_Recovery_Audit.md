# SIDIS physics-results execution and recovery audit

Inspection only. Evidence is from `.grok/workflows/sidis-physics-results.rhai`, skill front matter, `~/.grok/docs/user-guide/08-skills.md`, `~/.grok/bundled/skills/create-workflow/SKILL.md`, `plot_consolidated_phi_h_figures.py`, `sidis_physics_reports.py`, `sidis_physics_lib.py`, the `sidis-physics-results-2` journal, the fit registry, fit JSON, coverage files, φ_h logs, and file timestamps. Agent prose is a claim unless an artifact confirms it.

Run `sidis-physics-results-2` started 2026-11-02 00:29 UTC and completed 01:47 UTC. Fifteen agents ran. Stage success does not mean the final A₀ figures and ⟨k_T²⟩ use the latest corrected fits.

## 1. Executive summary

Confirmed:

- Acceptance-level fit JSON exists for both nominals, the cut variations, the new same-weight method branches, Unweighted `Acc`, Spline `AccSpline`, bin-by-bin, and the Unweighted 5D comparison.
- All 24 sector configurations have `Fit_Pars_from_3D_Bayesian`, `fit_coverage.json`, and `refinement_note.json`. Latest registry status is `completed_partial`. Unweighted `eS1o` has 422 fitted cells. The 24 partial records sum to 10,137 fitted cells and 711 `N/A` empty histograms. Those bins are `empty_histogram`, not zeroes.
- Nominal `RC_Bayesian` and `BC_RC_Bayesian` fits exist, 452 bins each, under `physics_campaign/corrected/<campaign>/{rc,bc}/`. Unweighted bin `(Q2_y_Bin_1)-(z_pT_Bin_1)` A in the new BC JSON is 23929.4, still on the yield scale. Those files have no `Fit_Par_*_SYS` and no `normalization_status`.
- `budgets.json` at 20:17 is a provisional acceptance-level budget. Sectors are `not_combined`. Radiative, bin-centering method, iteration, subdivision, and Spline 5D contribute no number. That budget is not the complete final systematic until the required correction-stage contributions exist.
- 62 φ_h PDFs were saved. The 24 sector commands ran and returned `thesis_ready=no`, so no sector PDF was written.
- Mosaics and ⟨k_T²⟩ were written from `corrected/<campaign>/normalized.json` (mtime 01:55), not from the 20:32 BC fits.

The 10,137 sector fits are reusable. They do not need to be repeated to draw sector figures. The 89 refinement notes are not automatically invalid. They are also not proof that `/refine-phi-fits` ran. Only 18 overlay files exist. The least expensive check is a sample of notes against `refine_init.py` and the fit JSON, not a campaign rerun.

The 15 bin-centering subdivision variations are different. Their A, B, and C shifts do not exist. When they are computed, each of the 15 must finish the full `refine-phi-fits` procedure before the shifts enter the Unweighted systematic. A single fit pass may be kept as an intermediate file. It is not a completed refinement and it is not an RMS input.

## 2. Skill and command invocation

### Supported mechanism

`~/.grok/docs/user-guide/08-skills.md` states that `disable-model-invocation: true` means only the user's slash command runs the skill. The model cannot invoke it automatically. Every physics skill used here sets `user-invocable: true` and `disable-model-invocation: true`. `refine-phi-fits` says it runs when the user runs `/refine-phi-fits`, and that the text after that token is the argument string. It also requires reading `references/repo-fit-interface.md` before a fit.

`~/.grok/bundled/skills/create-workflow/SKILL.md` documents `agent(prompt, opts)`. The options are `label`, `phase`, `capability_mode`, `output_schema`, `agent_type`, `model`, `isolation_worktree`, and `resume_from`. There is no skill argument. `fork_context` is rejected for project scripts, so a child does not inherit the parent conversation. The same file says a cold subagent only does what the prompt commands, and that a scoping rule must be a Rhai check on the agent's output, not prompt text alone.

A slash token typed inside an `agent()` string is not a documented skill load. The user slash menu is a session action that injects `SKILL.md`. The workflow host does not provide an equivalent call.

### What this workflow does

`sidis-physics-results.rhai` calls `agent(prompt)` and `parallel(...)`. The prompts say `Follow refine-phi-fits` and the other names. They do not include the skill body, the reference file, or a schema the script checks. `record_refinement` (`refinement_note_ok` in `sidis_physics_lib.py`) accepts any note with six non-empty strings. A return code of 0, a nonempty JSON, or that note can all be true while the skill's overlay judgment never ran.

### Repair

The supported repair is a self-contained prompt plus a host-side check:

1. The Rhai prompt must tell the subagent to `read_file` the exact `SKILL.md` and its `references/` file, then carry out those steps. Naming the skill is not enough.
2. The prompt must paste the operative requirements the script will check, because the child may not receive the skill.
3. `agent(..., #{ output_schema: ... })` must require the substantive evidence for that skill. The script rejects the stage if those fields are missing. A note that merely has the six keys fails the check.
4. Do not treat a literal `/skill-name` inside the prompt as execution.

For `refine-phi-fits`, the schema should require: resolved root and family, start mode, error source, whether overlay plotting ran or failed, the bins whose guides changed, the Q²–y list that was remade, a before/after quality number for each edited bin, bins left because the histogram disagreed, and unresolved bins. The script checks that the named `refine_init.py` exists and that the fit JSON still contains the unedited bins.

The same pattern applies to the other stages:

| Stage | Skill or command the prompt must load | Evidence the script must require |
| --- | --- | --- |
| Nominal, variations, RC, BC, subdivision | `refine-phi-fits` plus `references/repo-fit-interface.md` | Fields above. Family token matches `Bayesian`, `RC_Bayesian`, `BC_RC_Bayesian`, or 3D `(Bin)` |
| Radiative | `evaluate-radiative-systematics` | Pending flag, null systematic, and the manifest's verified event-ratio path left unchanged. The scan ROOT is not a systematic |
| Bin centering | `evaluate-bin-centering-systematics` | Five variable RMS values, one pooled RMS of 15 refined shifts, or an explicit not-in-sum state. No factor-only substitute |
| Mosaic | `plot-sidis-mosaic` and the printed plotter command | Input path, `normalization_status`, error suffix, and PDF paths. Refuse the 01:55 file once a newer normalized file exists |
| φ_h | `consolidate-thesis-phi-figures` limited to `unfolded_ac`, `unfolded_rc`, `unfolded_bc` | Log line with `pdf=` set, or a recorded `N/A` pad list if the save rule is changed. No thesis edit |
| ⟨k_T²⟩ | `extract-sidis-kt2` | JSON path, `--already_normalized`, uncertainty source, and row counts |
| Reports | Report builder after the inputs above | Figure inventory paths that exist on disk |

### Existing 89 notes

Do not delete them and do not refit all of them. What is on disk: 89 `refinement_note.json` files and 89 `refine_init.py` files. The unweighted nominal note names 22 bins, a Q²–y remake list, and a χ² drop from 16.22 to 1.44 at `(3,16)`. The unweighted `eS1o` note names 10 improved bins and 30 empty bins left as `N/A`. What is not on disk: a skill-load record, and a per-bin overlay set (18 overlay files under four directories).

Least expensive verification: sample notes against the matching `refine_init.py` keys and the fit JSON. If a sample's edited bins are absent from the guide file or the JSON, recover only those files. If the sample matches, keep the 89 fits and record them as `complete_but_unverified` until a later visual spot check. That is not a reason to repeat the 10,137 sector cells.

## 3. Classifications

| Product | Class | Evidence |
| --- | --- | --- |
| Acceptance nominals, cuts, new method branches, Acc, AccSpline | `complete_but_unverified` | JSON and notes exist. Overlay archive does not cover every bin. Not auto-invalidated |
| Bin-by-bin and Unweighted 5D | `verified_complete` for the defined comparison | 452-bin JSON. Q²–y 1 and 5 of the 5D comparison stay `iteration_mismatch`. Spline 5D is absent |
| 24 sector fits | `partial_recoverable` | JSON, coverage, and notes exist. PDFs do not. Do not refit to draw them |
| Nominal RC and BC fits | `partial_recoverable` | Right family, 452 bins, yield-scale A, no `_SYS` |
| `normalized.json`, mosaics, ⟨k_T²⟩, reports | `stale_downstream` | Normalized file is 01:55. New BC A for bin 1-1 is 23929 (Unweighted) and 21714 (Spline). Old A₀ is 0.091 and 0.083 |
| `budgets.json` | Provisional acceptance budget, not the final systematic | Written 20:17, before the BC fits. Correction-stage terms are not in it |
| 15 subdivision shifts | `requires_refit` | Correction files exist. Fitted shifts do not. Full refinement is required before they enter the sum |
| BC method and iteration | `blocked` | Transfer is `user_decision`. No post-refit spline is named |
| Radiative alternatives and Spline 5D | `missing_required_input` | Binary absent. 5D Spline path absent. Nominal RC file still exists |

## 4. Sector figures

Fits are on disk for all 24 names. Unweighted `eS1o` has 422 `Fit_Pars_from_3D_Bayesian` cells. Coverage lists `(Q2_y_Bin_3)-(z_pT_Bin_4)` as `N/A` / `empty_histogram`. Each sector directory has a refinement note. Latest registry status is `completed_partial` for all 24. Older `failed` rows remain only because `artifacts.jsonl` is append-only.

The plot command ran. `physics_campaign/logs/phi_figures/spline_pion_sector_pipS5o_unfolded_ac.log` calls `plot_consolidated_phi_h_figures.py -f unfolded_ac` with that sector ROOT and fit JSON. Status: `thesis_ready=no`, `pdf=` empty, reason `missing fit 3-4; missing fit 3-5; ...`. The same gate appears in `unweighted_electron_sector_eS4o_unfolded_ac.log`. No PDF exists under the sector figure directories.

`draw_family` appends every retained bin with no histogram or no fit dict to `missing`. `thesis_ready = (len(missing) == 0)`. `save_one_page` runs only when that flag is true. One absent bin drops the canvas. Aggregation already stores missing sector comparisons as `status=missing` and keeps sectors `not_combined`. Do not insert zeroes.

Recovery is a save-rule change plus a rerun of the 24 logged commands. No refit. Valid fitted histograms stay eligible. `N/A` pads stay empty.

## 5. Stale downstream chain

Current: acceptance fits, the 20:17 provisional acceptance budget, and `corrected/<campaign>/{rc,bc}/fit.json`.

Stale: `corrected/<campaign>/normalized.json` (01:55), parent `corrected/<campaign>/fit.json`, mosaics, both ⟨k_T²⟩ extractions, and the reports. The mosaic and kT2 agent records name the 01:55 file. New ⟨k_T²⟩ counts match the old ones (Unweighted 78 ok / 13 poor, Spline 84 ok / 7 poor, 91 rows).

`mosaic_command` requires `normalization_status: applied`. `write_normalized_results.py` reads `corrected/<campaign>/fit.json`, not `bc/fit.json`. Nothing compares the BC fit mtime with the normalized file. The budget is also older than the BC fits, so it was never attached to those central values.

The acceptance-level budget may be attached to the new BC central values as a provisional systematic, with that provenance written on the file. It must not be labeled the complete final systematic while subdivision, radiative alternatives, and the blocked bin-centering comparisons are still outside the sum.

## 6. Reporting gap

`markdown_report` lists nominals, budget source names, sector coverage, and kT2 status counts. It does not read `bc/fit.json`, print A/B/C tables, or walk figure directories. `write_pptx` builds a short text deck. That is why the figure-rich run still produced an 11.5 KB note and a 32 KB presentation.

A later report, after Tier 1 and any completed Tier 2 term, should keep Unweighted and Spline in separate sections, tabulate A₀, B, and C with both uncertainties, state that A was divided once and B and C were not, list per-source RMS and every study that contributes no number, and link every PDF. The PowerPoint shows representative figures with those paths. Every figure is in the Markdown inventory. The provisional acceptance systematic is labeled provisional. Do not edit the thesis.

## 7. Recovery tiers

Do not repeat the 10,137 sector cells or the nominal RC and BC JSON files to fix plots and normalization. Do not bulk-repeat the 89 notes. Sample them. Repeat a file only if that sample shows the note does not match the guide or the JSON.

### Tier 1 — existing artifacts, no physics refit

1. Let the φ_h plotter save a canvas when some fits are missing, mark those pads `N/A`, and write no zero. Rerun the 24 logged sector commands.
2. Normalize `corrected/<campaign>/bc/fit.json` with the 20:17 budget. Write a new file. Do not replace the 01:55 file until the new A₀ is checked. Record provenance: provisional acceptance-level systematic, not the final systematic. Scale A and that uncertainty once. Leave B and C unscaled.
3. Rerun mosaics for both campaigns, z, P_T, and P_T², statistical and systematic, on that new file.
4. Rerun ⟨k_T²⟩ once per campaign, `--uncertainty_source systematic`, `--already_normalized`.
5. Rebuild the Markdown as a figure inventory and numerical record, and the PowerPoint from those figures.
6. Repair skill invocation as in section 2 before any later workflow run. Tier 1 plot and normalize commands can run from the existing CLIs without that repair. The repair is required before the next agent-driven refinement stage.

Check: bin 1-1 A₀ equals the new BC A divided by the existing cross-section factor, `_SYS` is present and labeled provisional, mosaics and ⟨k_T²⟩ cite the new file, and each sector directory has a PDF.

The previous 36 mosaics and two ⟨k_T²⟩ jobs took minutes. Twenty-four φ_h canvases are the slow piece, on the order of an hour.

### Tier 2 — 15 subdivision refinements

For each of the 15 Unweighted subdivision JSON files, apply BC to `corrected/unweighted/rc/corrected.root` and run the full `refine-phi-fits` procedure on that `BC_RC_Bayesian` copy. The reference is the existing nominal BC fit. Do not refit that reference. A one-pass JSON may be kept only as an intermediate. It does not enter the RMS.

Then form five diagnostic RMS values and one pooled RMS of the 15 refined shifts. That pooled value is the RMS of all 15 shifts, not the quadrature of the five variable RMS values. Re-aggregate, re-normalize, and refresh plots and reports. Until those refined shifts exist, the subdivision term stays out of the sum and is not zero. Spline does not receive it.

This is 15 full refinements, not an 85-file campaign, and not an optional extra pass.

### Tier 3 — blocked outside this recovery

- Radiative systematic until the `cross_section` binary and an approved alternative exist.
- Spline 5D until `Unfolded_5D_inherited_Spline.root` exists.
- Event-versus-spline BC transfer until a numerical rule is chosen.
- Spline-iteration BC until a post-refit spline file is named.
- A lower-acceptance unfold. Empty fractions are about 6% to 7.5%. This audit does not request that unfold.

## 8. Decisions before any recovery run

1. Approve copying this audit to the reports path and stopping, or also authorize Tier 1.
2. Keep the 01:55 `normalized.json` until the new file is checked.
3. Tier 2 is mandatory before the subdivision term is quoted. Each of the 15 must complete `refine-phi-fits`. A single pass is not sufficient.
4. The acceptance-level budget attached in Tier 1 is provisional. It is not the complete final systematic while Tier 2 and the Tier 3 studies are outstanding.
5. Sample the 89 notes before any decision to repeat one of those fits. Do not repeat them as a block, and do not repeat the 10,137 sector fits in order to draw their figures.
