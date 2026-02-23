#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=RMatrix_ZerothOrderAcc_02_20_2026_running_batch_jobs
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=2GB
#SBATCH --time=00:45:00
#SBATCH --array=1-108


BATCH_ID=${SLURM_ARRAY_TASK_ID}
NAME_BASE="ZerothOrderAcc"
EMAIL_MSG="Zeroth Order Acceptance Weight batched run. No Injected Physics."


srun python3 /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/Response_Matrix_Creation_using_RDataFrames.py -bID ${BATCH_ID} -f -MR -n "${NAME_BASE}" -t "Zeroth Order Acceptance Weights" -em "${EMAIL_MSG}" -hpp_in /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/New_Pass_2_Cut_generated_acceptance_weights_Zeroth_Order.hpp --use_hpp

