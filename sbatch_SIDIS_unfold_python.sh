#!/bin/bash
#SBATCH --ntasks=2
#SBATCH --job-name=RooUnfold_python_SIDIS_Multi_Dimension_Unfold_V3_Simulated_Test_2_histo_3_14_2023
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu 
#SBATCH --output=/farm_out/%u/%x-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=16000
#SBATCH --time=24:00:00
#SBATCH --array=0-8

source /group/clas12/packages/setup.csh
source /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/New_RooUnfold/RooUnfold/build/setup.sh

srun python3 /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/RooUnfold_SIDIS_richcap.py save_sim $SLURM_ARRAY_TASK_ID
