#!/bin/bash
# Combine per-job Chapter 3 HIPO histogram ROOT files with ROOT hadd,
# then delete the per-job ROOT files after a successful merge.
#
# Usage (from Data_Files_Groovy, after all jobs finish):
#   bash Chapter3_Figures/hadd_Chapter3_HIPO_hists.sh
#
# Optional:
#   CHAPTER3_HIPO_OUTDIR=/path/to/job_outputs bash Chapter3_Figures/hadd_Chapter3_HIPO_hists.sh

set -euo pipefail

OUTDIR="${CHAPTER3_HIPO_OUTDIR:-Chapter3_Figures/job_outputs}"
COMBINED="${CHAPTER3_HIPO_COMBINED:-Chapter3_Figures/Chapter3_HIPO_hists_combined.root}"

if ! command -v hadd >/dev/null 2>&1; then
  echo "ERROR: ROOT hadd is not on PATH."
  exit 1
fi

shopt -s nullglob
FILES=( "${OUTDIR}"/Chapter3_HIPO_hists_*.root )
if [[ ${#FILES[@]} -eq 0 ]]; then
  echo "ERROR: no per-job ROOT files in ${OUTDIR}"
  exit 1
fi

mkdir -p "$(dirname "${COMBINED}")"
echo "hadd of ${#FILES[@]} files -> ${COMBINED}"
hadd -f "${COMBINED}" "${FILES[@]}"

if [[ ! -s "${COMBINED}" ]]; then
  echo "ERROR: combined file missing or empty: ${COMBINED}"
  exit 1
fi

echo "Removing ${#FILES[@]} per-job ROOT files"
rm -f "${FILES[@]}"
echo "Kept combined file: ${COMBINED}"
