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

if ! command -v hadd >/dev/null 2>&1; then
  echo "ERROR: ROOT hadd is not on PATH."
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

mkdir -p "$(dirname "${COMBINED}")"
echo "hadd of ${#KEEP[@]} files -> ${COMBINED}"
hadd -f "${COMBINED}" "${KEEP[@]}"

if [[ ! -s "${COMBINED}" ]]; then
  echo "ERROR: combined file missing or empty: ${COMBINED}"
  exit 1
fi

echo "Removing ${#KEEP[@]} per-job ROOT files"
rm -f "${KEEP[@]}"
echo "Kept combined file: ${COMBINED}"
