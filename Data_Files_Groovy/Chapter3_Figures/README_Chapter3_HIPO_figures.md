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

Default plotting writes every established configuration into its own directory:

`none`, `el_dc`, `pip_dc`, `el_pip_dc`, `pip_fd`, `chi2pid`, `el_vz`, `pcal_emin`, `all`

## Submit jobs (from `Data_Files_Groovy`)

Reuse `run_groovy_scripts_with_emails.py`. `-wd` must point at `Chapter3_Figures/job_outputs`.

```bash
cd /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy && ./run_groovy_scripts_with_emails.py -src data -evt epipX -sp Chapter3_Figures/Chapter3_HIPO_Histograms.groovy -m slurm -st 6:00:00 -sn Chapter3Hists -wd /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/Chapter3_Figures/job_outputs -em "Creating thesis Chapter 3 figure images."
```

Each job writes:

- `Chapter3_Figures/job_outputs/Chapter3_HIPO_hists_<hipo_basename>.root`

Override the output directory with `CHAPTER3_HIPO_OUTDIR`.

## Merge

From inside `Chapter3_Figures`:

```bash
cd /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/Chapter3_Figures
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
| `electron_DC_rotated.pdf` | `fig:electron_DC_rotated` |
