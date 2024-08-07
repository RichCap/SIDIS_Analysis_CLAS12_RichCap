#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=NS_Bayes_Test_5D_Unfold_Test_V7_5_31_2024_Run1
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu 
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=20050
#SBATCH --time=48:00:00
#SBATCH --array=1-17
#SBATCH --constraint=el7


# source /group/clas12/packages/setup.csh
# source /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/New_RooUnfold/RooUnfold/build/setup.sh
# Main array: SBATCH --array=0-17
# Normal request: #SBATCH --mem-per-cpu=15000

srun python3 /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Bayes_RooUnfold_SIDIS_Iteration_Test.py no_smear $SLURM_ARRAY_TASK_ID
