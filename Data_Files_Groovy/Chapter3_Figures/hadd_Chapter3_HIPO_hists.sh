#!/bin/bash
# Combine per-job Chapter 3 HIPO TTree ROOT files with ROOT hadd.
# Per-job ROOT files are kept (this script does not delete them).
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
CHECK_LIST="$("${PYTHON}" - "${KEEP[@]}" <<'PY'
from __future__ import print_function
import os
import sys

try:
    import ROOT
except Exception as exc:
    sys.stderr.write("ERROR: cannot import ROOT to validate files: %s\n" % exc)
    sys.exit(2)

ROOT.gROOT.SetBatch(True)
for path in sys.argv[1:]:
    kind = None
    reason = None
    tfile = None
    if((not os.path.isfile(path)) or (os.path.getsize(path) <= 0)):
        kind = "corrupt"
        reason = "missing or empty"
    else:
        tfile = ROOT.TFile.Open(path, "READ")
        if((tfile is None) or (not tfile) or tfile.IsZombie()):
            kind = "corrupt"
            reason = "ROOT file is unreadable or a zombie"
        else:
            tree = tfile.Get("h22")
            if((tree is None) or (not tree)):
                kind = "corrupt"
                reason = "missing h22 TTree"
            else:
                try:
                    nent = int(tree.GetEntries())
                except Exception:
                    kind = "corrupt"
                    reason = "h22 TTree is unreadable"
                else:
                    if(nent <= 0):
                        kind = "zero"
                        reason = "h22 has GetEntries() == 0"
        if(tfile):
            tfile.Close()
    if(kind is not None):
        print("%s\t%s\t%s" % (kind, path, reason))
PY
)"
PY_RC=$?
set -e
if [[ ${PY_RC} -ne 0 ]]; then
  echo "ERROR: ROOT-file validation failed to run (python/ROOT rc=${PY_RC})."
  exit 1
fi

CORRUPT_LIST=""
ZERO_LIST=""
if [[ -n "${CHECK_LIST}" ]]; then
  while IFS=$'\t' read -r kind path reason; do
    if [[ -z "${kind}" ]]; then
      continue
    fi
    line="${path}	${reason}"
    if [[ "${kind}" == "corrupt" ]]; then
      if [[ -n "${CORRUPT_LIST}" ]]; then
        CORRUPT_LIST="${CORRUPT_LIST}"$'\n'"${line}"
      else
        CORRUPT_LIST="${line}"
      fi
    elif [[ "${kind}" == "zero" ]]; then
      if [[ -n "${ZERO_LIST}" ]]; then
        ZERO_LIST="${ZERO_LIST}"$'\n'"${line}"
      else
        ZERO_LIST="${line}"
      fi
    fi
  done <<< "${CHECK_LIST}"
fi

print_path_reason_list() {
  local title="$1"
  local list="$2"
  echo "${title}"
  if [[ -z "${list}" ]]; then
    echo "  (none)"
    return
  fi
  while IFS=$'\t' read -r path reason; do
    if [[ -z "${path}" ]]; then
      continue
    fi
    echo "  ${path}  (${reason})"
  done <<< "${list}"
}

if [[ -n "${ZERO_LIST}" ]]; then
  echo
  print_path_reason_list "Zero-entry input files (readable h22, GetEntries() == 0; not blocking hadd):" "${ZERO_LIST}"
fi

if [[ -n "${CORRUPT_LIST}" ]]; then
  echo "ERROR: corrupted or unreadable Chapter 3 ROOT files were found. hadd was not run."
  echo
  print_path_reason_list "Corrupted/unreadable input files:" "${CORRUPT_LIST}"
  echo
  : > "${RERUN_LIST}"
  while IFS=$'\t' read -r path reason; do
    if [[ -z "${path}" ]]; then
      continue
    fi
    base="$(basename "${path}")"
    hipo="${base#Chapter3_HIPO_hists_}"
    hipo="${hipo%.root}"
    echo "${HIPO_PREFIX}/${hipo}" >> "${RERUN_LIST}"
  done <<< "${CORRUPT_LIST}"
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
  echo
  print_path_reason_list "Zero-entry input files:" "${ZERO_LIST}"
  echo
  print_path_reason_list "Corrupted/unreadable input files:" "${CORRUPT_LIST}"
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
try:
    nent = int(tree.GetEntries())
except Exception:
    print("combined h22 TTree is unreadable")
    tfile.Close()
    sys.exit(1)
tfile.Close()
print("ok %d" % nent)
PY
)"
COMBINED_RC=$?
set -e
if [[ ${COMBINED_RC} -ne 0 ]]; then
  echo "ERROR: combined file failed validation: ${COMBINED_CHECK}"
  echo
  print_path_reason_list "Zero-entry input files:" "${ZERO_LIST}"
  echo
  print_path_reason_list "Corrupted/unreadable input files:" "${CORRUPT_LIST}"
  exit 1
fi

COMBINED_NENT="${COMBINED_CHECK#ok }"
echo "Combined h22 entries: ${COMBINED_NENT}"
echo
print_path_reason_list "Zero-entry input files:" "${ZERO_LIST}"
echo
print_path_reason_list "Corrupted/unreadable input files:" "${CORRUPT_LIST}"
echo "Kept per-job ROOT files in ${OUTDIR}"
echo "Kept combined file: ${COMBINED}"
