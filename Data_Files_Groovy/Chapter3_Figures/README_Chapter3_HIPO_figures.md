# Chapter 3 HIPO TTree workflow

These scripts read the **REAL experimental** `nSidis` HIPO files and write compact ROOT TTrees for Chapter 3 PID/fiducial plots. They do **not** write the usual analysis ntuples.

Do not run the Groovy job on a laptop that does not contain the HIPO inputs.

Optional cut combinations are applied later in `plot_Chapter3_HIPO_hists.py`. Changing a cut threshold does not require rerunning HIPO, as long as the stored variables are unchanged.

## Inputs

File discovery is the same as the existing Groovy ntuple submitter:

- manifest: `Data_Files_Groovy/Paths_to_REAL_Data_files_all.txt`
- glob: `/lustre24/expphy/cache/clas12/rg-a/production/recon/fall2018/torus-1/pass2/main/train/nSidis/nSidis_*`

Override the list with `-ptxt` if a restricted SIDIS subset is required (`TEMP_Paths_to_REAL_Data_files_SIDIS.txt`).

## Trees in each ROOT file

Particle 0 must pass `ElectronCandidate.iselectron(PID)` before any `elepip` or `had` row is written.

| Tree | Rows | Used for |
|---|---|---|
| `ele` | one PID trigger electron | HTCC, PCAL \(E\), SF tot, rotated electron DC when the cut index has **no** pion bits |
| `elepip` | one e–\(\pi^+\) pair (`ipart≥1`, EventBuilder \(\pi^+\) PID; FORWARD is optional) | the same electron plots when the cut index includes a pion bit |
| `had` | one `charge>0` reconstructed particle, in a PID-electron event | inclusive \(\beta\) vs \(p\) (not pion-only) |

## Optional-cut index (plot-time)

Defined in `plot_Chapter3_HIPO_hists.py`. Groovy does not store cut indices.

| Bit | Value | Filter |
|---|---|---|
| 0 | 1 | pion/hadron FD status \(2000\le\mathrm{status}<4000\) |
| 1 | 2 | \(\lvert\chi^2_{\mathrm{PID}}\rvert<3\) (simple diagnostic, not the nominal momentum-dependent cut) |
| 2 | 4 | electron DC edges R1,R2 \(>5.0\) cm and R3 \(>10.0\) cm |
| 3 | 8 | pion/hadron DC edges R1,R2 \(>2.5\) cm and R3 \(>9.0\) cm |
| 4 | 16 | electron \(-8<v_z<2\) cm |
| 5 | 32 | PCAL \(E>0.06\) GeV |

Examples: `0` none; `4` electron DC only; `8` pion DC only; `12` both DC; `63` all six.

## Submit jobs (from `cd_Groovy`)

Reuse `run_groovy_scripts_with_emails.py`. `-wd` must point at `Chapter3_Figures/job_outputs`.

SLURM array:

```bash
cd /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy && ./run_groovy_scripts_with_emails.py -src data -evt epipX -sp Chapter3_Figures/Chapter3_HIPO_Histograms.groovy -m slurm -st 6:00:00 -sn Chapter3Hists -wd /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/Chapter3_Figures/job_outputs -em "Creating thesis Chapter 3 figure images."
```

Local parallel, cancelling matching pending SLURM tasks:

```bash
./run_groovy_scripts_with_emails.py -src data -evt epipX -sp Chapter3_Figures/Chapter3_HIPO_Histograms.groovy -m parallel --parallel_jobs 4 -wd /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/Chapter3_Figures/job_outputs -saj <SLURM_ARRAY_JOBID>
```

Each job writes:

- `Chapter3_Figures/job_outputs/Chapter3_HIPO_hists_<hipo_basename>.root`

Override the output directory with `CHAPTER3_HIPO_OUTDIR`.

## Merge

From inside `Chapter3_Figures`:

```bash
cd /Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Data_Files_Groovy/Chapter3_Figures
./hadd_Chapter3_HIPO_hists.sh
```

On the farm the same command works after `cd` to that directory. This runs ROOT `hadd` on the per-job ROOT files, writes `Chapter3_HIPO_hists_combined.root` next to the script, and then deletes the per-job ROOT files.

## Plot

From `Chapter3_Figures`:

```bash
python plot_Chapter3_HIPO_hists.py -r Chapter3_HIPO_hists_combined.root -o Plot_Images
python plot_Chapter3_HIPO_hists.py -r Chapter3_HIPO_hists_combined.root -o Plot_Images -ci 0,4,8,12,63
```

PDFs are written under `Plot_Images/cut_index_NN/` using the thesis file names:

| File | Figure |
|---|---|
| `HTCC_Nphe.pdf` | `fig:HTCC_Nphe` |
| `PCAL_Emin.pdf` | `fig:PCAL_Emin` |
| `SFtot_band.pdf` | `fig:SFtot_band_cut` |
| `Beta_PID.pdf` | `fig:Beta_PID` |
| `electron_DC_rotated.pdf` | `fig:electron_DC_rotated` |
