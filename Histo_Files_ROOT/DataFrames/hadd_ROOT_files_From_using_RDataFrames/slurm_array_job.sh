#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=ZerothOrder_11_24_2025_running_batch_jobs
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=3GB
#SBATCH --time=20:00:00
#SBATCH --array=1-5,7-10,12-57


BATCH_ID=${SLURM_ARRAY_TASK_ID}
NAME_BASE="ZerothOrder"
EMAIL_MSG="Zeroth Order Acceptance Weight batched run. No Injected Physics.
This is the second (reran) version of these files. Reran due to timing-out in the first attempt."
NAME_FOR_BATCH="${NAME_BASE}_Batch${BATCH_ID}"


srun python3 /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/using_RDataFrames_python.py -bID ${BATCH_ID} -NoEvGen -f -MR -n "${NAME_FOR_BATCH}" -t "Zeroth Order Acceptance Weights" -em "${EMAIL_MSG}" -hpp /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/generated_acceptance_weights_ZeroOrder.hpp