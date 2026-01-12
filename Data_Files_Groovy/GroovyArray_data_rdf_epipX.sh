#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=Data_epipX_data_1_12_2026
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=3500M
#SBATCH --time=20:00:00
#SBATCH --array=0-29

TASK_ID="${SLURM_ARRAY_TASK_ID}"
MANIFEST="TEMP_Paths_to_REAL_Data_files_SIDIS.txt"
GROOVY_SCRIPT="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/REAL_Data/Data_TTree_epip_Batch_Pass2.groovy"
WORK_DIR="/w/hallb-scshelf2102/clas12/richcap/SIDIS/REAL_Data/Pass2/More_Cut_Info/"

cd "${WORK_DIR}" || { echo "ERROR: Failed to cd into WORK_DIR=${WORK_DIR}"; exit 1; }

mapfile -t PATTERNS < <(grep -v '^[[:space:]]*#' "${MANIFEST}" | sed '/^[[:space:]]*$/d')
if [[ ${#PATTERNS[@]} -eq 0 ]]; then echo "ERROR: No usable entries in manifest: ${MANIFEST}"; exit 1; fi

# Expand patterns into file list (sorted per-pattern for stability)
FILES=()
for pat in "${PATTERNS[@]}"; do
  while IFS= read -r fp; do FILES+=("$fp"); done < <(compgen -G "$pat" | sort)
done

# Dedupe while keeping order
declare -A SEEN
DEDUPED=()
for fp in "${FILES[@]}"; do
  if [[ -z "${SEEN[$fp]+x}" ]]; then SEEN["$fp"]=1; DEDUPED+=("$fp"); fi
done

NFILES=${#DEDUPED[@]}
if [[ $NFILES -eq 0 ]]; then echo "ERROR: Expansion produced zero files from manifest: ${MANIFEST}"; exit 1; fi

# TASK_ID is 0-based here (matches your default array spec 0-(N-1))
if [[ ${TASK_ID} -lt 0 || ${TASK_ID} -ge ${NFILES} ]]; then
  echo "ERROR: TASK_ID=${TASK_ID} out of range for NFILES=${NFILES}"; exit 1;
fi
INPUT_FILE="${DEDUPED[$TASK_ID]}"

echo "Running TASK_ID=${TASK_ID} on host $(hostname) at $(date)"
echo "Work dir: ${WORK_DIR}"
echo "Input file: ${INPUT_FILE}"

srun "${GROOVY_SCRIPT}" "${INPUT_FILE}"
echo "Finished TASK_ID=${TASK_ID} at $(date)"
