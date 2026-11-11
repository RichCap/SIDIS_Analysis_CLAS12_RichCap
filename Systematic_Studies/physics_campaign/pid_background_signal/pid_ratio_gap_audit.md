# PID ratio gap audit

Authoritative bin count is `Get_Num_of_z_pT_Bins_w_Migrations`: index 0 is the number of defined z-P_T bins, index 1 is the last defined index, and index 2 is the migration list excluded by `skip_condition_z_pT_bins` when the method contains `Y_bin`.

`retained_bins` walks every pad index from 1 through rows times columns and drops an index when `skip_condition_z_pT_bins` is true. `fill_ratio_grid` calls `grid.cd(zpt)` only for those retained indices. A retained bin is drawn only when all four histograms exist; otherwise the pad is marked N/A. Histogram presence alone does not draw a skipped pad.

A phi_h point with zero signal is omitted from the ratio curve inside a drawn panel. That is not an omitted z-P_T panel.

## Counts by Q2-y group

| Q2-y | Grid | Defined | Undefined slots | Skipped defined | Retained | In summary (drawn) |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 35 | 35 | 0 | 6 | 29 | 29 |
| 2 | 36 | 36 | 0 | 4 | 32 | 32 |
| 3 | 30 | 30 | 0 | 2 | 28 | 28 |
| 4 | 36 | 36 | 0 | 13 | 23 | 23 |
| 5 | 36 | 36 | 0 | 4 | 32 | 32 |
| 6 | 30 | 30 | 0 | 4 | 26 | 26 |
| 7 | 36 | 36 | 0 | 4 | 32 | 32 |
| 8 | 35 | 35 | 0 | 9 | 26 | 26 |
| 9 | 35 | 35 | 0 | 6 | 29 | 29 |
| 10 | 36 | 36 | 0 | 4 | 32 | 32 |
| 11 | 25 | 25 | 0 | 2 | 23 | 23 |
| 12 | 25 | 25 | 0 | 10 | 15 | 15 |
| 13 | 30 | 30 | 0 | 4 | 26 | 26 |
| 14 | 36 | 36 | 0 | 5 | 31 | 31 |
| 15 | 25 | 25 | 0 | 6 | 19 | 19 |
| 16 | 30 | 30 | 0 | 6 | 24 | 24 |
| 17 | 30 | 30 | 0 | 5 | 25 | 25 |
| Total | 546 | 546 | 0 | 94 | 452 | 452 |

Expected retained panels: 452. Retained by the skip rule: 452. Panels recorded as drawn in the summary: 452.
The retained list, the summary, and the four-histogram requirement agree. No retained bin failed to appear.

## Omitted defined bins and other discrepancies

| Q2-y | z-P_T | Class | Reason |
|---:|---:|---|---|
| 1 | 21 | defined bin excluded | migration list |
| 1 | 27 | defined bin excluded | migration list |
| 1 | 28 | defined bin excluded | migration list |
| 1 | 33 | defined bin excluded | migration list |
| 1 | 34 | defined bin excluded | migration list |
| 1 | 35 | defined bin excluded | migration list |
| 2 | 24 | defined bin excluded | migration list |
| 2 | 30 | defined bin excluded | migration list |
| 2 | 35 | defined bin excluded | migration list |
| 2 | 36 | defined bin excluded | migration list |
| 3 | 6 | defined bin excluded | additional Y_bin exclusion in skip_condition_z_pT_bins |
| 3 | 30 | defined bin excluded | migration list |
| 4 | 1 | defined bin excluded | additional Y_bin exclusion in skip_condition_z_pT_bins |
| 4 | 2 | defined bin excluded | additional Y_bin exclusion in skip_condition_z_pT_bins |
| 4 | 3 | defined bin excluded | additional Y_bin exclusion in skip_condition_z_pT_bins |
| 4 | 4 | defined bin excluded | additional Y_bin exclusion in skip_condition_z_pT_bins |
| 4 | 5 | defined bin excluded | additional Y_bin exclusion in skip_condition_z_pT_bins |
| 4 | 6 | defined bin excluded | migration list |
| 4 | 11 | defined bin excluded | additional Y_bin exclusion in skip_condition_z_pT_bins |
| 4 | 12 | defined bin excluded | additional Y_bin exclusion in skip_condition_z_pT_bins |
| 4 | 18 | defined bin excluded | additional Y_bin exclusion in skip_condition_z_pT_bins |
| 4 | 24 | defined bin excluded | additional Y_bin exclusion in skip_condition_z_pT_bins |
| 4 | 30 | defined bin excluded | additional Y_bin exclusion in skip_condition_z_pT_bins |
| 4 | 35 | defined bin excluded | migration list |
| 4 | 36 | defined bin excluded | migration list |
| 5 | 24 | defined bin excluded | migration list |
| 5 | 30 | defined bin excluded | migration list |
| 5 | 35 | defined bin excluded | migration list |
| 5 | 36 | defined bin excluded | migration list |
| 6 | 18 | defined bin excluded | migration list |
| 6 | 24 | defined bin excluded | migration list |
| 6 | 29 | defined bin excluded | migration list |
| 6 | 30 | defined bin excluded | migration list |
| 7 | 5 | defined bin excluded | additional Y_bin exclusion in skip_condition_z_pT_bins |
| 7 | 6 | defined bin excluded | migration list |
| 7 | 30 | defined bin excluded | migration list |
| 7 | 36 | defined bin excluded | migration list |
| 8 | 1 | defined bin excluded | additional Y_bin exclusion in skip_condition_z_pT_bins |
| 8 | 2 | defined bin excluded | additional Y_bin exclusion in skip_condition_z_pT_bins |
| 8 | 3 | defined bin excluded | additional Y_bin exclusion in skip_condition_z_pT_bins |
| 8 | 4 | defined bin excluded | additional Y_bin exclusion in skip_condition_z_pT_bins |
| 8 | 5 | defined bin excluded | additional Y_bin exclusion in skip_condition_z_pT_bins |
| 8 | 9 | defined bin excluded | additional Y_bin exclusion in skip_condition_z_pT_bins |
| 8 | 10 | defined bin excluded | additional Y_bin exclusion in skip_condition_z_pT_bins |
| 8 | 15 | defined bin excluded | additional Y_bin exclusion in skip_condition_z_pT_bins |
| 8 | 35 | defined bin excluded | migration list |
| 9 | 21 | defined bin excluded | migration list |
| 9 | 27 | defined bin excluded | migration list |
| 9 | 28 | defined bin excluded | migration list |
| 9 | 33 | defined bin excluded | migration list |
| 9 | 34 | defined bin excluded | migration list |
| 9 | 35 | defined bin excluded | migration list |
| 10 | 24 | defined bin excluded | migration list |
| 10 | 30 | defined bin excluded | migration list |
| 10 | 35 | defined bin excluded | migration list |
| 10 | 36 | defined bin excluded | migration list |
| 11 | 5 | defined bin excluded | additional Y_bin exclusion in skip_condition_z_pT_bins |
| 11 | 25 | defined bin excluded | migration list |
| 12 | 1 | defined bin excluded | additional Y_bin exclusion in skip_condition_z_pT_bins |
| 12 | 2 | defined bin excluded | additional Y_bin exclusion in skip_condition_z_pT_bins |
| 12 | 3 | defined bin excluded | additional Y_bin exclusion in skip_condition_z_pT_bins |
| 12 | 4 | defined bin excluded | additional Y_bin exclusion in skip_condition_z_pT_bins |
| 12 | 5 | defined bin excluded | migration list |
| 12 | 9 | defined bin excluded | additional Y_bin exclusion in skip_condition_z_pT_bins |
| 12 | 10 | defined bin excluded | additional Y_bin exclusion in skip_condition_z_pT_bins |
| 12 | 15 | defined bin excluded | additional Y_bin exclusion in skip_condition_z_pT_bins |
| 12 | 20 | defined bin excluded | additional Y_bin exclusion in skip_condition_z_pT_bins |
| 12 | 25 | defined bin excluded | migration list |
| 13 | 20 | defined bin excluded | migration list |
| 13 | 25 | defined bin excluded | migration list |
| 13 | 29 | defined bin excluded | migration list |
| 13 | 30 | defined bin excluded | migration list |
| 14 | 6 | defined bin excluded | additional Y_bin exclusion in skip_condition_z_pT_bins |
| 14 | 24 | defined bin excluded | migration list |
| 14 | 30 | defined bin excluded | migration list |
| 14 | 35 | defined bin excluded | migration list |
| 14 | 36 | defined bin excluded | migration list |
| 15 | 3 | defined bin excluded | additional Y_bin exclusion in skip_condition_z_pT_bins |
| 15 | 4 | defined bin excluded | additional Y_bin exclusion in skip_condition_z_pT_bins |
| 15 | 5 | defined bin excluded | migration list |
| 15 | 10 | defined bin excluded | additional Y_bin exclusion in skip_condition_z_pT_bins |
| 15 | 20 | defined bin excluded | migration list |
| 15 | 25 | defined bin excluded | migration list |
| 16 | 18 | defined bin excluded | migration list |
| 16 | 23 | defined bin excluded | migration list |
| 16 | 24 | defined bin excluded | migration list |
| 16 | 28 | defined bin excluded | migration list |
| 16 | 29 | defined bin excluded | migration list |
| 16 | 30 | defined bin excluded | migration list |
| 17 | 5 | defined bin excluded | additional Y_bin exclusion in skip_condition_z_pT_bins |
| 17 | 6 | defined bin excluded | additional Y_bin exclusion in skip_condition_z_pT_bins |
| 17 | 24 | defined bin excluded | migration list |
| 17 | 29 | defined bin excluded | migration list |
| 17 | 30 | defined bin excluded | migration list |

Blank pads inside a Q2-y group are the undefined slots plus the skipped defined bins. `fill_ratio_grid` never calls those pad indices, so they stay empty. It does not delete a histogram.
