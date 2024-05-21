#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=P2_Bayes_Test_5D_Unfold_Test_V6_5_21_2024_Run2
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu 
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=15000
#SBATCH --time=24:00:00
#SBATCH --array=1-17
#SBATCH --constraint=el7


# source /group/clas12/packages/setup.csh
# source /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/New_RooUnfold/RooUnfold/build/setup.sh
# Main array: SBATCH --array=0-17
# Normal request: #SBATCH --mem-per-cpu=15000

srun python3 /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Bayes_RooUnfold_SIDIS_Iteration_Test.py smear $SLURM_ARRAY_TASK_ID
