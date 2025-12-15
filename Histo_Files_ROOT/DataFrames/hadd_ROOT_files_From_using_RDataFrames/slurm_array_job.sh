#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=V_AngleOnlyZerothOrder_12_13_2025_running_batch_jobs
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=3GB
#SBATCH --time=20:00:00
#SBATCH --array=1-57


BATCH_ID=${SLURM_ARRAY_TASK_ID}
NAME_BASE="AngleOnlyZerothOrder_Valerii"
EMAIL_MSG="Zeroth Order Acceptance Weight batched run. Only used the acceptance weights for the lab angles. No Momemntum weights OR Injected Physics.
Ran with Valerii's Binning. Ran with improved weight normalization and with sequential mode running simultaneously."
NAME_FOR_BATCH="${NAME_BASE}_Batch${BATCH_ID}"


srun python3 /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/using_RDataFrames_python.py -bID ${BATCH_ID} -NoEvGen -f -MR --valerii_bins -n "${NAME_FOR_BATCH}" -t "Zeroth Order Acceptance Weights (Angles Only)" -em "${EMAIL_MSG}" -hpp /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/generated_acceptance_weights_ZeroOrder.hpp --angles_only_hpp