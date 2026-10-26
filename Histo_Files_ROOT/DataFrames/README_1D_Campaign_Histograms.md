# Only_1D and Diagnostic_1D histograms

`Response_Matrix_Creation_using_RDataFrames.py` calls `run_campaign_1d` and exits when `--only_1d` or `--diagnostic_1d` is set. The batch ROOT file is `args.root`. The existing hadd merges those batch files. Nothing in this mode is added into the 3D or 5D response matrices.

## What each mode measures

Only_1D is the source-separated kinematic distributions, plus the reconstructed versus matched-generated φ_h response in the nominal 4D analysis cell.

Diagnostic_1D is the momentum-correction and smearing response, and the bank particle-matching categories. Correction quantities are data only. Smearing quantities are smeared reconstructed Monte Carlo only.

## Sources

Files are split with `classify_rho_name` before a dataframe is built.

| Data-Type | Files | Meaning |
|---|---|---|
| `rdf` | `rdf` | Experimental data. Unweighted. |
| `mdf` | `mdf_clasdis` paths that are not dedicated ρ files | Reconstructed clasdis Monte Carlo. `*_gen` columns on this frame are matched generated quantities, not independent `gdf`. |
| `gdf` | `gdf_clasdis` paths that are not dedicated ρ files | Independently generated Monte Carlo. |
| `mdf` or `gdf` with `_(lundvpk)`, `_(lundrho)`, or `_(rho0_new)` | Paths classified as that ρ source | That ρ Monte Carlo alone. |

A missing ρ file is reported. It is not replaced by another sample.

## Weights

The unweighted histogram is always booked. Further weights come from `enabled_weight_specs`:

| Source | Extra tags | Column |
|---|---|---|
| `rdf` | none | |
| `mdf` | `Acc`, `JSON`, `AccJSON`, `Spline`, `AccSpline` | `Event_Weight_Acc`, `Event_Weight_JSON`, `Event_Weight_AccJSON`, `Event_Weight_Spline`, `Event_Weight_AccSpline` |
| `gdf` | `JSON`, `Spline` | `Event_Weight_JSON`, `Event_Weight_Spline` |

Those extra tags are booked only when the same flags that enable them for 3D/5D are on. If the flag is on and the column is absent, the column name is printed and that variant is not filled with unit weight. `exclusive_rho_weight`, when the column exists, is one more tagged weight. It does not mix ρ samples.

## Names

`finalize_histo_name` builds the ROOT name:

`((Histo-Group='Only_1D'), (Data-Type='mdf'), (Data-Cut='cut_Complete_SIDIS'), (Smear-Type='no_smear'), (Binning-Type='Y_bin'), (Var='Q2'))`

A ρ source appends `_(lundrho)`. A weight appends `_(AccSpline)`. Diagnostic histograms use `Histo-Group='Diagnostic_1D'`. Matched generated kinematics use `Smear-Type='matched_gen'` and `Var='Q2_gen'`. Duplicate names are refused.

Titles use `variable_Title_name` when that helper knows the variable. Weighted histograms add `Weighted (Tag)`.

## Only_1D kinematics

TH3. X is the variable below. Y is `Q2_Y_Bin`, 18 bins from −0.5 to 17.5. Z is `z_pT_Bin_Y_bin`, 38 bins from −0.5 to 37.5. The selection is `cut_Complete_SIDIS == 1`.

| Variable | Column | Bins | Range |
|---|---|---|---|
| Q² | `Q2` | 140 | 0–12 |
| xB | `xB` | 100 | 0–1 |
| y | `y` | 100 | 0.05–1.05 |
| z | `z` | 100 | 0–1 |
| P_T | `pT` | 105 | 0–1.05 |
| Missing mass | `MM` | 80 | 0.5–4.5 |
| φ_h | `phi_t` | 24 | 0–360° |
| Electron momentum | `el` | 200 | 0–8 |
| Pion momentum | `pip` | 150 | 0–6 |
| θ | `elth`, `pipth` | 200 | 0–40° |
| φ | `elPhi`, `pipPhi` | 360 | 0–360° |
| xF | `xF` | 200 | −1–1 |

xF is `2 (p_π · q) / (|q| W)` from `dataframe_makeROOT_epip_SIDIS.py`. The axis is the commented −1 to 1, 200-bin entry in `makeROOT_epip_SIDIS_histos_new.py`. `MM` is also filled with `cut_Complete_SIDIS_MM_None` when that column exists. Q2-removed and y-removed histograms are not booked: `cut_Complete_NoKin` is not in these snapshots.

On `mdf`, the same table is filled again from `Q2_gen`, `xB_gen`, and the other `*_gen` columns when they exist. Those histograms stay `Data-Type='mdf'`.

## φ_h response

`Var='phi_response_4d'` is a TH3 for matched `mdf` only: reconstructed `phi_t`, matched generated `phi_t_gen`, and `campaign_dense_4d_cell`. Both φ axes are 24 bins from 0° to 360°. It is not filled for `rdf` or independent `gdf`.

The cell count `n` is `create_dense_5d_bin_mapping()["total_kinematic_slots"]`. The axis has `n + 2` bins from −1.5 to `n + 0.5`. `Campaign_Dense_4D_Cell(q2y, zpt)` reads `kinematic_start_slot[q2y][zpt]` and returns `((start - 1) / 24) + 1`. Bin 0 means the pair is outside the map. Do not hardcode a 452 or 546 count. To recover the analysis bin, find the `(Q2_Y_Bin, z_pT_Bin_Y_bin)` whose start slot maps to that cell, then read φ_h inside the 24 bins of that slot.

## Diagnostic quantities

Correction histograms are `rdf` only.

- `Complete_Correction_Factor_Ele` is `dppC(...) + 1`.
- `Complete_Correction_Factor_Pip` is `dppC(...) + 1`, times `Energy_Loss_Cor_Factor` on Pass 2.
- `Delta_phi_t` is `phi_t` minus φ_h after the pion correction is divided out. Production snapshots leave `Run_Uncorrected_phi_t_Info_Q` false, so the booker recomputes that expression when the pion momenta and the correction factor exist. It is not the smearing angle.

Smearing histograms are smeared `mdf` only.

- `Delta_Smear_El_P` and `Delta_Smear_Pip_P` are `|P_smeared| − |P|`.
- `campaign_smear_dphi` is `phi_t_smeared − phi_t`, wrapped into (−180°, 180°].

| Var | X | Y | Z |
|---|---|---|---|
| `corr_el_vs_pip` | electron factor, 100 bins, 0.9–1.1 | pion factor, 100 bins, 0.9–1.1 | 4D cell |
| `corr_el_vs_dphi`, `corr_pip_vs_dphi` | that factor | Δφ_h from the correction, 125 bins, −10°–10° | 4D cell |
| `smear_el_vs_pip` | electron Δp, 100 bins, −0.5–0.5 | pion Δp, 100 bins, −0.5–0.5 | 4D cell |
| `smear_el_vs_dphi`, `smear_pip_vs_dphi` | that Δp | smearing Δφ_h, 90 bins, −180°–180° | 4D cell |
| `corr_el_index`, `corr_pip_index` | that factor | `Q2_Y_Bin` | `z_pT_Bin_Y_bin` |
| `smear_el_index`, `smear_pip_index` | that Δp | `Q2_Y_Bin` | `z_pT_Bin_Y_bin` |

## Matching categories

Status is 0 when the bank PID is 11 for the electron or 211 for the pion, 2 when the PID is 0, and 1 otherwise. The category is `3 * electron_status + pion_status`. Columns follow `-mac` through `MATCHING_SOURCE_SUFFIX`. Bank uses `PID_el_Bank` and `PID_pip_Bank`.

| Bin | Electron | Pion | Axis label |
|---|---|---|---|
| 0 | Correct | Correct | Correct / Correct |
| 1 | Correct | Wrong PID | Correct / Wrong PID |
| 2 | Correct | Unmatched | Correct / Unmatched |
| 3 | Wrong PID | Correct | Wrong PID / Correct |
| 4 | Wrong PID | Wrong PID | Wrong PID / Wrong PID |
| 5 | Wrong PID | Unmatched | Wrong PID / Unmatched |
| 6 | Unmatched | Correct | Unmatched / Correct |
| 7 | Unmatched | Wrong PID | Unmatched / Wrong PID |
| 8 | Unmatched | Unmatched | Unmatched / Unmatched |

The integrated histogram is `Var='match_category'`, 9 bins from −0.5 to 8.5. Bin labels are set on the X axis. `Var='match_category_dense'` is category versus the 4D cell. `Var='match_category_q2y_zpt'` is category versus `Q2_Y_Bin` and `z_pT_Bin_Y_bin`. `el_status` and `pip_status` use the three status labels. `el_pid` and `pip_pid` are the raw PID spectra. `match_denominator` and `match_denominator_q2y_zpt` count events with weight 1 in the same selection, so a later plot can divide the category counts after hadd. The histogram contents stay numeric. A PDF named `<root stem>_match_category.pdf` draws the integrated category with the text labels.

## How to run

From `Histo_Files_ROOT/DataFrames`, the existing pipeline flags are `--only_1d` and `--diagnostic_1d`. The campaign product keys are `Only_1D` and `Diagnostic_1D`. `-mac Bank` is the nominal matching mode. After hadd, open the merged file and `Get` the `finalize_histo_name` string. Do not look for `MDF_Match_Category`.
