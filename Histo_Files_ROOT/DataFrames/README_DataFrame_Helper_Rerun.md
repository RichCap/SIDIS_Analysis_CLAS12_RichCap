# Rerun failed `run_dataframe_makeROOT_helper.py` jobs

Use this after a **hybrid** (or SLURM) DataFrame conversion where some array tasks **timed out** or otherwise failed. Shell on JLab: **`tcsh`**.

The helper does **not** skip files that already converted successfully. Re-running the original glob would redo every file. Use `--input_list` / `-il` with only the failed source ROOT paths.

Hybrid completion emails **undercount** SLURM timeouts: the local half skips a task once SLURM owns it, so a 1-hour `TIME LIMIT` never shows up as a local `FAIL`.

---

## What a helper run writes

`--variant` picks data type, `job_base`, and output subdirectory. `--data_root work` vs `work_b` picks which analysis tree holds the DataFrames (Groovy inputs stay under hallb `SIDIS/`).

| `--variant` | Output subdirectory | Filelist name |
|-------------|---------------------|---------------|
| `real_data_pass2` | `REAL_Data` | `{job_base}_filelist.txt` |
| `matching_mc_pass2` | `Matching_REC_MC` | `{job_base}_filelist.txt` |
| `gen_mc_pass2` | `GEN_MC` | `{job_base}_filelist.txt` |

`job_base` is the preset (for example `mdf_DF_9_2_2026_R1_Final_Thesis_Files`) unless you passed `--job_base`.

Other artifacts:

- SLURM stdout: `/farm_out/$USER/{job_base}-{array}_{task}-{job}-{node}.out`
- `{task}` is **1-based** and is the line number in that variant’s `*_filelist.txt`
- `{job}` is the individual SLURM job ID (the number in `CANCELLED AT ... DUE TO TIME LIMIT`)
- Local helper logs: `/scratch/$USER/dataframe_makeROOT_logs/{REAL_Data,Matching_REC_MC,GEN_MC}/`
- Converter success line: `Saved File:`
- Snapshot on timeout can leave a **truncated** DataFrame ROOT. File existence is not enough.

Worked example (Final Thesis on `work_b`):

```
WB=/w/ceph24/hallb/clas12/users/richcap/SIDIS_Analysis_CLAS12_RichCap/Histo_Files_ROOT/DataFrames
job_base rdf: rdf_DF_9_2_2026_R1_Final_Thesis_Files
job_base mdf: mdf_DF_9_2_2026_R1_Final_Thesis_Files
job_base gdf: gdf_DF_9_2_2026_R1_Final_Thesis_Files
```

---

## `tcsh` pitfalls (read before pasting)

- **`noclobber`**: `cat /dev/null > file` fails with `File exists.` Use `>!` to overwrite.
- Do **not** paste a one-line `foreach` that uses backticks. Chat/markdown strips `$`, backticks, and turns `-` into Unicode `−`. Use the `python3 << PY` blocks below.
- If the prompt is `foreach?`, the loop never started. Type `end` until you get `ifarm...>` back. Do not keep pasting.

Confirm `--input_list` exists:

```
cd /w/ceph24/hallb/clas12/users/richcap/SIDIS_Analysis_CLAS12_RichCap/Histo_Files_ROOT/DataFrames ; ./run_dataframe_makeROOT_helper.py -h | grep input_list
```

(Use the `work` DataFrames directory instead if that is the copy you launched from.)

---

## 1. Collect timed-out job IDs

From farm_out (replace `JOB_BASE` with `rdf_...` / `mdf_...` / `gdf_...`):

```
grep -l "TIME LIMIT" /farm_out/$USER/JOB_BASE-*.out
```

Or from the cancellation line, the number after `JOB` is `{job}`:

```
slurmstepd: error: *** JOB 10229126 ON sciml2402 CANCELLED AT ... DUE TO TIME LIMIT ***
```

Optional sacct:

```
sacct -j 10229126 -n -P --format=JobID,JobName,ArrayTaskID,Elapsed,State
```

Memory (if you are not sure it was only time): also search for `MEMORY LIMIT`, `Exceeded job memory limit`, and sacct state `OUT_OF_MEMORY`. `OOM`/`oom` alone can miss SLURM memory kills.

Put the individual job IDs in a space-separated list. You will paste that list into the Python blocks below.

---

## 2. Set paths

Replace `WB`, the three `job_base` strings, and the rerun filenames if this is not the Final Thesis `work_b` example.

```
setenv WB /w/ceph24/hallb/clas12/users/richcap/SIDIS_Analysis_CLAS12_RichCap/Histo_Files_ROOT/DataFrames ; setenv RDF_LIST $WB/REAL_Data/rdf_DF_9_2_2026_R1_Final_Thesis_Files_filelist.txt ; setenv MDF_LIST $WB/Matching_REC_MC/mdf_DF_9_2_2026_R1_Final_Thesis_Files_filelist.txt ; setenv GDF_LIST $WB/GEN_MC/gdf_DF_9_2_2026_R1_Final_Thesis_Files_filelist.txt ; setenv RDF_RERUN $WB/REAL_Data/rdf_DF_9_2_2026_R1_Final_Thesis_Files_rerun.txt ; setenv MDF_RERUN $WB/Matching_REC_MC/mdf_DF_9_2_2026_R1_Final_Thesis_Files_rerun.txt ; setenv GDF_RERUN $WB/GEN_MC/gdf_DF_9_2_2026_R1_Final_Thesis_Files_rerun.txt ; ls -l $RDF_LIST $MDF_LIST $GDF_LIST
```

If a filelist is missing, that variant never wrote one; stop and inspect that output directory.

---

## 3. Truncate rerun lists

```
cat /dev/null >! $RDF_RERUN ; cat /dev/null >! $MDF_RERUN ; cat /dev/null >! $GDF_RERUN ; echo ready
```

---

## 4. Map job IDs → source ROOT paths

Paste this whole block. It ends on a line that is only `PY`. Replace the `jobs = "..."` string with your job IDs. Replace the three `job_base` keys if your presets used different names.

```
python3 << PY
import glob, os
jobs = "10228790 10228823 10228834 10228855 10228856 10228921 10228952 10228953 10228954 10229126 10229246 10229578 10229604 10229605 10229718 10229729 10229730 10229731".split()
lists = {
    "rdf_DF_9_2_2026_R1_Final_Thesis_Files": os.environ["RDF_LIST"],
    "mdf_DF_9_2_2026_R1_Final_Thesis_Files": os.environ["MDF_LIST"],
    "gdf_DF_9_2_2026_R1_Final_Thesis_Files": os.environ["GDF_LIST"],
}
reruns = {
    "rdf_DF_9_2_2026_R1_Final_Thesis_Files": os.environ["RDF_RERUN"],
    "mdf_DF_9_2_2026_R1_Final_Thesis_Files": os.environ["MDF_RERUN"],
    "gdf_DF_9_2_2026_R1_Final_Thesis_Files": os.environ["GDF_RERUN"],
}
found = {k: [] for k in lists}
farm = "/farm_out/%s" % os.environ["USER"]
for j in jobs:
    hits = sorted(glob.glob("%s/*-%s-*.out" % (farm, j)))
    if not hits:
        print("MISSING farm_out for JOB", j)
        continue
    f = hits[0]
    parts = os.path.basename(f)[:-4].split("-")
    jb = parts[0]
    task = parts[1].split("_")[-1]
    if jb not in lists:
        print("UNKNOWN job_base", jb, "for JOB", j, "file", f)
        continue
    lines = open(lists[jb]).read().splitlines()
    idx = int(task) - 1
    src = lines[idx] if 0 <= idx < len(lines) else ""
    print("JOB", j, jb, "task=" + task, "SRC=" + src)
    if src:
        found[jb].append(src)
    else:
        print("NO filelist line", task, "in", lists[jb])
for jb, paths in found.items():
    uniq = []
    for p in paths:
        if p not in uniq:
            uniq.append(p)
    open(reruns[jb], "w").write(("\n".join(uniq) + "\n") if uniq else "")
    print("WROTE", reruns[jb], len(uniq))
PY
```

---

## 5. Inspect the lists

```
echo "=== RDF ===" ; wc -l $RDF_RERUN ; cat $RDF_RERUN ; echo "=== MDF ===" ; wc -l $MDF_RERUN ; cat $MDF_RERUN ; echo "=== GDF ===" ; wc -l $GDF_RERUN ; cat $GDF_RERUN
```

The three counts should add to the number of timed-out jobs (minus any `MISSING` / `UNKNOWN` lines). Deduplicate if needed:

```
sort -u $RDF_RERUN -o $RDF_RERUN ; sort -u $MDF_RERUN -o $MDF_RERUN ; sort -u $GDF_RERUN -o $GDF_RERUN
```

---

## 6. Truncated DataFrame ROOT files

```
python3 << PY
import glob, os, sys
jobs = "10228790 10228823 10228834 10228855 10228856 10228921 10228952 10228953 10228954 10229126 10229246 10229578 10229604 10229605 10229718 10229729 10229730 10229731".split()
farm = "/farm_out/%s" % os.environ["USER"]
for j in jobs:
    hits = sorted(glob.glob("%s/*-%s-*.out" % (farm, j)))
    print("====", j, hits[0] if hits else "MISSING", "====")
    if not hits:
        continue
    for line in open(hits[0], errors="replace"):
        if ("Saved File:" in line) or ("File being made is:" in line):
            sys.stdout.write(line)
PY
```

If a log has `File being made is: SomeName.root` and **no** `Saved File:`, delete **only** that file from the matching DataFrames subdirectory. Do not mass-delete the directory.

---

## 7. Dry-run, then rerun

Skip a variant if its rerun file is empty (`wc -l` is 0).

Work from the **same repository copy** you will launch (scripts from execution root; DataFrames from `--data_root`).

Typical SLURM time for a timeout rerun: **double** the original (1 hour → `-st 02:00:00`). Keep `--slurm_mem 4GB` unless logs showed a memory kill.

From `$WB` (example: `work_b`, Final Thesis):

RDF dry-run:

```
./run_dataframe_makeROOT_helper.py --dry_run --variant real_data_pass2 --max_jobs 10 --common_name Final_Thesis_Files_ --mode hybrid --data_root work_b -st 02:00:00 --input_list /w/ceph24/hallb/clas12/users/richcap/SIDIS_Analysis_CLAS12_RichCap/Histo_Files_ROOT/DataFrames/REAL_Data/rdf_DF_9_2_2026_R1_Final_Thesis_Files_rerun.txt
```

MDF dry-run:

```
./run_dataframe_makeROOT_helper.py --dry_run --variant matching_mc_pass2 --max_jobs 10 --common_name Final_Thesis_Files_ --mode hybrid --data_root work_b -st 02:00:00 --input_list /w/ceph24/hallb/clas12/users/richcap/SIDIS_Analysis_CLAS12_RichCap/Histo_Files_ROOT/DataFrames/Matching_REC_MC/mdf_DF_9_2_2026_R1_Final_Thesis_Files_rerun.txt
```

GDF dry-run:

```
./run_dataframe_makeROOT_helper.py --dry_run --variant gen_mc_pass2 --max_jobs 10 --common_name Final_Thesis_Files_ --mode hybrid --data_root work_b -st 02:00:00 --input_list /w/ceph24/hallb/clas12/users/richcap/SIDIS_Analysis_CLAS12_RichCap/Histo_Files_ROOT/DataFrames/GEN_MC/gdf_DF_9_2_2026_R1_Final_Thesis_Files_rerun.txt
```

Dry-run **Files Found** must match that list’s line count. The converter path must be this repository copy. Output dirs must match `--data_root`. `--file` paths must be the Groovy/source lines from the rerun lists.

Real run: drop `--dry_run`, add `-e` and a new `--email_message`. Example MDF:

```
./run_dataframe_makeROOT_helper.py -e --email_message 'Timeout rerun of failed Final_Thesis_Files mdf DataFrames on work_b. SLURM time 2 hours. Hybrid.' --variant matching_mc_pass2 --max_jobs 10 --common_name Final_Thesis_Files_ --mode hybrid --data_root work_b -st 02:00:00 --input_list /w/ceph24/hallb/clas12/users/richcap/SIDIS_Analysis_CLAS12_RichCap/Histo_Files_ROOT/DataFrames/Matching_REC_MC/mdf_DF_9_2_2026_R1_Final_Thesis_Files_rerun.txt
```

Same pattern for `--variant real_data_pass2` with `$RDF_RERUN` and `--variant gen_mc_pass2` with `$GDF_RERUN`.

If one file still hits the new time limit, rerun **that leftover only** with a larger `-st`.

---

## Do not

- Re-run the original three commands without `--input_list` (that converts every file again).
- Use `>` instead of `>!` to empty an existing `*_rerun.txt` under `noclobber`.
- Paste a `tcsh` `foreach` with backticks from chat.
- Delete an entire `REAL_Data` / `Matching_REC_MC` / `GEN_MC` directory to clear truncated ROOT files.
- Treat “the ROOT file exists” as success after a timeout.
