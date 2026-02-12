#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=RMatrix_ZerothOrder_02_11_2026_running_batch_jobs
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=3GB
#SBATCH --time=20:00:00
#SBATCH --array=1-108


BATCH_ID=${SLURM_ARRAY_TASK_ID}
NAME_BASE="ZerothOrder"
EMAIL_MSG="Zeroth Order batched run. No Injected Physics/Weights."


srun python3 /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/Response_Matrix_Creation_using_RDataFrames.py -bID ${BATCH_ID} -f -MR -n "${NAME_BASE}" -t "Zeroth Order (No Weights)" -em "${EMAIL_MSG}" -hpp_in /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/generated_acceptance_weights_ZeroOrder.hpp

