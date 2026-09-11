# Chapter 3 HIPO TTree workflow

These scripts read the **REAL experimental** `nSidis` HIPO files and write a compact ROOT `h22` TTree for Chapter 3 PID/fiducial plots. They do **not** write the usual analysis ntuples.

Do not run the Groovy job on a laptop that does not contain the HIPO inputs.

Optional cut combinations are applied later in `plot_Chapter3_HIPO_hists.py`. Changing a cut threshold does not require rerunning HIPO, as long as the stored variables are unchanged.

## Inputs

File discovery is the same as the existing Groovy ntuple submitter:

- manifest: `Data_Files_Groovy/Paths_to_REAL_Data_files_all.txt`
- glob: `/lustre24/expphy/cache/clas12/rg-a/production/recon/fall2018/torus-1/pass2/main/train/nSidis/nSidis_*`

Override the list with `-ptxt` if a restricted SIDIS subset is required (`TEMP_Paths_to_REAL_Data_files_SIDIS.txt`).

## `h22` row kinds

Particle 0 must pass `ElectronCandidate.iselectron(PID)` before pair or hadron rows are written.

| `kind` | Rows | Used for |
|---|---|---|
| 0 | one PID trigger electron | HTCC, PCAL \(E\), SF tot, rotated electron DC when the configuration has **no** pion cuts |
| 1 | one e–\(\pi^+\) pair (`ipart≥1`, EventBuilder \(\pi^+\) PID; FORWARD is optional) | the same electron plots when the configuration includes a pion cut |
| 2 | one `charge>0` reconstructed particle, in a PID-electron event | inclusive \(\beta\) vs \(p\) (not pion-only) |

Each job writes one tree named `h22` (same `ROOTFile` / `makeTree('h22', ...)` / `tt.write()` / `ff.close()` pattern as the ntuple Groovy scripts).

## Optional cuts (plot-time)

Defined in `plot_Chapter3_HIPO_hists.py`. Groovy does not store cut indices.

| Name | Filter |
|---|---|
| `pip_fd` | pion/hadron FD status \(2000\le\mathrm{status}<4000\) |
| `chi2pid` | \(\lvert\chi^2_{\mathrm{PID}}\rvert<3\) (simple diagnostic, not the nominal momentum-dependent cut) |
| `el_dc` | electron DC edges R1,R2 \(>5.0\) cm and R3 \(>10.0\) cm |
| `pip_dc` | pion/hadron DC edges R1,R2 \(>2.5\) cm and R3 \(>9.0\) cm |
| `el_vz` | electron \(-8<v_z<2\) cm |
| `pcal_emin` | PCAL \(E>0.06\) GeV |
| `all_electron` | stored `all_electron==1` (production `Full_default_el`: PID, CC \(N_{phe}\), EC sampling, PCAL V/W, DC-edge, \(v_z\); not Sangbaek/Valerii rotated DC) |
| `all_cuts` | former `all`: pip_fd + chi2pid + el_dc + pip_dc + el_vz + pcal_emin |
| `all_electron_FD` | `all_electron` + `pip_fd` |
| `all` | meta-option: every named config except itself |

Default: `none` and `all_electron`.

```bash
python plot_Chapter3_HIPO_hists.py -r Chapter3_HIPO_hists_combined.root -o Plot_Images
python plot_Chapter3_HIPO_hists.py -r Chapter3_HIPO_hists_combined.root -o Plot_Images -c all_electron all_electron_FD
python plot_Chapter3_HIPO_hists.py -r Chapter3_HIPO_hists_combined.root -o Plot_Images -c all
```

Selectable `-c` names: `none`, `el_dc`, `pip_dc`, `el_pip_dc`, `pip_fd`, `chi2pid`, `el_vz`, `pcal_emin`, `all_cuts`, `all_electron`, `all_electron_FD`, `all`.

## Submit jobs (from `Data_Files_Groovy`)

Reuse `run_groovy_scripts_with_emails.py`. `-wd` must point at `Chapter3_Figures/job_outputs`.

Run from the `Data_Files_Groovy` of the launched repository (`work` `/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis` or `work_b` `/w/ceph24/hallb/clas12/users/richcap/SIDIS_Analysis_CLAS12_RichCap`). The hadd rerun command uses that same tree.

```bash
cd /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy && ./run_groovy_scripts_with_emails.py -src data -evt epipX -sp Chapter3_Figures/Chapter3_HIPO_Histograms.groovy -m slurm -st 6:00:00 -sn Chapter3Hists -wd /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/Chapter3_Figures/job_outputs -em "Creating thesis Chapter 3 figure images."
```

Each job writes:

- `Chapter3_Figures/job_outputs/Chapter3_HIPO_hists_<hipo_basename>.root`

Override the output directory with `CHAPTER3_HIPO_OUTDIR`.

## Merge

From inside `Chapter3_Figures`:

```bash
cd Chapter3_Figures
./hadd_Chapter3_HIPO_hists.sh
```

Each per-job file must contain a readable `h22` tree with `GetEntries() > 0`. If any file fails, hadd stops, nothing is deleted, and a one-line rerun command is printed.

## Plot

From `Chapter3_Figures`:

```bash
python plot_Chapter3_HIPO_hists.py -r Chapter3_HIPO_hists_combined.root -o Plot_Images
```

PDFs are written under `Plot_Images/<config>/` using the thesis file names:

| File | Figure |
|---|---|
| `HTCC_Nphe.pdf` | `fig:HTCC_Nphe` |
| `PCAL_Emin.pdf` | `fig:PCAL_Emin` |
| `SFtot_band.pdf` | `fig:SFtot_band_cut` |
| `Beta_PID.pdf` | `fig:Beta_PID` |
| `electron_DC_rotated.pdf` | `fig:electron_DC_rotated` (weighted by `el_chi2pid`) |
| `electron_vz.pdf` | electron \(v_z\) |
| `electron_DC_edge.pdf` | electron DC-edge R1–R3 |
| `pip_chi2pid.pdf` | pion \(\chi^2_{\mathrm{PID}}\) vs \(p\) (\(C=0.88\), no \(p>4.6\) piece) |
| `delta_vz.pdf` | electron–pion \(\Delta v_z\) |
| `pion_DC_edge.pdf` | pion DC-edge R1–R3 |
| `PCAL_inefficient.pdf` | PCAL \(H_x\)–\(H_y\) occupancy |
| `PCAL_VW.pdf` | PCAL \(V\)–\(W\) fiducial |
