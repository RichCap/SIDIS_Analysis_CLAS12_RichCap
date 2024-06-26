#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=P2_Correction_Compare_V6_5_8_2024_Run1
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu 
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=5000
#SBATCH --time=0:40:00
#SBATCH --array=1-17


# source /group/clas12/packages/setup.csh
# source /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/New_RooUnfold/RooUnfold/build/setup.sh
# Main array: SBATCH --array=0-17

srun python3 /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Correction_Compare_RooUnfold_SIDIS_richcap.py save $SLURM_ARRAY_TASK_ID
