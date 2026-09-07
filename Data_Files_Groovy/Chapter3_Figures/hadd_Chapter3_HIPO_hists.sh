#!/bin/bash
# Combine per-job Chapter 3 HIPO TTree ROOT files with ROOT hadd,
# then delete the per-job ROOT files after a successful merge.
#
# Usage (from Chapter3_Figures, after all jobs finish):
#   ./hadd_Chapter3_HIPO_hists.sh
#
# Optional:
#   CHAPTER3_HIPO_OUTDIR=/path/to/job_outputs ./hadd_Chapter3_HIPO_hists.sh
#   CHAPTER3_HIPO_COMBINED=/path/to/combined.root ./hadd_Chapter3_HIPO_hists.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTDIR="${CHAPTER3_HIPO_OUTDIR:-${SCRIPT_DIR}/job_outputs}"
COMBINED="${CHAPTER3_HIPO_COMBINED:-${SCRIPT_DIR}/Chapter3_HIPO_hists_combined.root}"
RERUN_LIST="${SCRIPT_DIR}/rerun_broken_hipo_files.txt"
HIPO_PREFIX="/cache/clas12/rg-a/production/recon/fall2018/torus-1/pass2/main/train/nSidis"

if [[ -d "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy" ]]; then
  GROOVY_DIR="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy"
else
  GROOVY_DIR="/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Data_Files_Groovy"
fi

if ! command -v hadd >/dev/null 2>&1; then
  echo "ERROR: ROOT hadd is not on PATH."
  exit 1
fi

PYTHON=""
if command -v python3 >/dev/null 2>&1; then
  PYTHON="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON="python"
else
  echo "ERROR: python is required to validate ROOT files before hadd."
  exit 1
fi

shopt -s nullglob
FILES=( "${OUTDIR}"/Chapter3_HIPO_hists_*.root )
KEEP=()
for f in "${FILES[@]}"; do
  base="$(basename "${f}")"
  if [[ "${base}" == "Chapter3_HIPO_hists_combined.root" ]]; then
    continue
  fi
  KEEP+=("${f}")
done

if [[ ${#KEEP[@]} -eq 0 ]]; then
  echo "ERROR: no per-job ROOT files in ${OUTDIR}"
  exit 1
fi

set +e
BAD_LIST="$("${PYTHON}" - "${KEEP[@]}" <<'PY'
from __future__ import print_function
import os
import sys

try:
    import ROOT
except Exception as exc:
    sys.stderr.write("ERROR: cannot import ROOT to validate files: %s\n" % exc)
    sys.exit(2)

ROOT.gROOT.SetBatch(True)
bad = []
for path in sys.argv[1:]:
    reason = None
    if((not os.path.isfile(path)) or (os.path.getsize(path) <= 0)):
        reason = "missing or empty"
    else:
        tfile = ROOT.TFile.Open(path, "READ")
        if((tfile is None) or (not tfile) or tfile.IsZombie()):
            reason = "ROOT file is unreadable or a zombie"
        else:
            tree = tfile.Get("h22")
            if((tree is None) or (not tree)):
                reason = "missing h22 TTree"
            else:
                try:
                    nent = int(tree.GetEntries())
                except Exception:
                    nent = 0
                if(nent <= 0):
                    reason = "h22 has GetEntries() <= 0"
        if(tfile):
            tfile.Close()
    if(reason is not None):
        bad.append("%s\t%s" % (path, reason))
for line in bad:
    print(line)
PY
)"
PY_RC=$?
set -e
if [[ ${PY_RC} -ne 0 ]]; then
  echo "ERROR: ROOT-file validation failed to run (python/ROOT rc=${PY_RC})."
  exit 1
fi

if [[ -n "${BAD_LIST}" ]]; then
  echo "ERROR: corrupted or empty Chapter 3 ROOT files were found. hadd was not run and no files were deleted."
  echo
  echo "Failed files:"
  : > "${RERUN_LIST}"
  while IFS=$'\t' read -r path reason; do
    echo "  ${path}  (${reason})"
    base="$(basename "${path}")"
    hipo="${base#Chapter3_HIPO_hists_}"
    hipo="${hipo%.root}"
    echo "${HIPO_PREFIX}/${hipo}" >> "${RERUN_LIST}"
  done <<< "${BAD_LIST}"
  echo
  echo "Wrote hipo list: ${RERUN_LIST}"
  echo "Rerun only the broken files with this one command:"
  echo "cd ${GROOVY_DIR} && ./run_groovy_scripts_with_emails.py -src data -evt epipX -sp ${GROOVY_DIR}/Chapter3_Figures/Chapter3_HIPO_Histograms.groovy -m slurm -sn Chapter3HistsRerun -wd ${GROOVY_DIR}/Chapter3_Figures/job_outputs -ptxt ${RERUN_LIST}"
  exit 1
fi

mkdir -p "$(dirname "${COMBINED}")"
echo "hadd of ${#KEEP[@]} files -> ${COMBINED}"
hadd -f "${COMBINED}" "${KEEP[@]}"

if [[ ! -s "${COMBINED}" ]]; then
  echo "ERROR: combined file missing or empty: ${COMBINED}"
  exit 1
fi

set +e
COMBINED_CHECK="$("${PYTHON}" - "${COMBINED}" <<'PY'
from __future__ import print_function
import os
import sys
import ROOT
ROOT.gROOT.SetBatch(True)
path = sys.argv[1]
if((not os.path.isfile(path)) or (os.path.getsize(path) <= 0)):
    print("combined file missing or empty")
    sys.exit(1)
tfile = ROOT.TFile.Open(path, "READ")
if((tfile is None) or (not tfile) or tfile.IsZombie()):
    print("combined ROOT file is unreadable or a zombie")
    sys.exit(1)
tree = tfile.Get("h22")
if((tree is None) or (not tree)):
    print("combined file missing h22 TTree")
    tfile.Close()
    sys.exit(1)
nent = int(tree.GetEntries())
tfile.Close()
if(nent <= 0):
    print("combined h22 has GetEntries() <= 0")
    sys.exit(1)
print("ok %d" % nent)
PY
)"
COMBINED_RC=$?
set -e
if [[ ${COMBINED_RC} -ne 0 ]]; then
  echo "ERROR: combined file failed validation: ${COMBINED_CHECK}"
  echo "Per-job ROOT files were NOT deleted."
  exit 1
fi

echo "Removing ${#KEEP[@]} per-job ROOT files"
rm -f "${KEEP[@]}"
echo "Kept combined file: ${COMBINED}"
