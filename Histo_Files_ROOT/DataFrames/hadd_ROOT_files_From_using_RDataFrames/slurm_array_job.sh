#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=FirstOrder_12_08_2025_running_batch_jobs
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
NAME_BASE="FirstOrder_Fixed"
EMAIL_MSG="First Order Injected Physics Modulation Weight batched run. No Acceptance Weights.
This is the second (fixed) version of these files. Ran with improved weight normalization and (hopefully) with sequential mode running simultaneously."
NAME_FOR_BATCH="${NAME_BASE}_Batch${BATCH_ID}"


srun python3 /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/using_RDataFrames_python.py -bID ${BATCH_ID} -NoEvGen -f -MR -n "${NAME_FOR_BATCH}" -t "First Order Modulation Weights" -em "${EMAIL_MSG}" -hpp /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/generated_acceptance_weights_FirstOrder.hpp --json_weights --json_file /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Fit_Pars_from_3D_Bayesian_with_Toys.json --do_not_use_hpp