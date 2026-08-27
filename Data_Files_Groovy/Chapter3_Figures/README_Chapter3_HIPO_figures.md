# Chapter 3 HIPO histogram workflow

These scripts fill Chapter 3 PID/fiducial histograms from the **REAL experimental** `nSidis` HIPO files and do **not** write the usual analysis ntuples.

Do not run them on a laptop that does not contain the HIPO inputs.

## Inputs

File discovery is the same as the existing Groovy ntuple submitter:

- manifest: `Data_Files_Groovy/Paths_to_REAL_Data_files_all.txt`
- glob: `/lustre24/expphy/cache/clas12/rg-a/production/recon/fall2018/torus-1/pass2/main/train/nSidis/nSidis_*`

Override the list with `-ptxt` if a restricted SIDIS subset is required (`TEMP_Paths_to_REAL_Data_files_SIDIS.txt`).

## Submit jobs (from `cd_Groovy`)

Reuse `run_groovy_scripts_with_emails.py` (sequential, local parallel, SLURM array, and SLURM/local skip-or-cancel coordination).

SLURM array:

```bash
cd /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy
./run_groovy_scripts_with_emails.py \
  -src data -evt epipX \
  -sp Chapter3_Figures/Chapter3_HIPO_Histograms.groovy \
  -m slurm \
  -st 6:00:00 \
  -sn Chapter3Hists
```

Local parallel, cancelling the matching pending SLURM tasks:

```bash
./run_groovy_scripts_with_emails.py \
  -src data -evt epipX \
  -sp Chapter3_Figures/Chapter3_HIPO_Histograms.groovy \
  -m parallel --parallel_jobs 4 \
  -saj <SLURM_ARRAY_JOBID>
```

Each job writes:

- `Chapter3_Figures/job_outputs/Chapter3_HIPO_hists_<hipo_basename>.json`
- `Chapter3_Figures/job_outputs/Chapter3_HIPO_hists_<hipo_basename>.root`

Override the output directory with `CHAPTER3_HIPO_OUTDIR`.

## Merge

After every job has finished:

```bash
bash Chapter3_Figures/hadd_Chapter3_HIPO_hists.sh
```

This runs ROOT `hadd` on the per-job ROOT files, writes

`Chapter3_Figures/Chapter3_HIPO_hists_combined.root`,

and then deletes the per-job ROOT files.

## Plot

```bash
python Chapter3_Figures/plot_Chapter3_HIPO_hists.py \
  --root Chapter3_Figures/Chapter3_HIPO_hists_combined.root \
  --out  /path/to/thesis/Experiment/Data_Collection_Images/Analysis_Cut_Images
```

Produced PDFs (thesis include names):

| File | Figure |
|---|---|
| `HTCC_Nphe.pdf` | `fig:HTCC_Nphe` |
| `PCAL_Emin.pdf` | `fig:PCAL_Emin` |
| `SFtot_band.pdf` | `fig:SFtot_band_cut` |
| `Beta_PID.pdf` | `fig:Beta_PID` |
| `electron_DC_rotated.pdf` | `fig:electron_DC_rotated` |
