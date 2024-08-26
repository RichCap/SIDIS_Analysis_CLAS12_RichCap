#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=RooUnfold_New_Fiducial_Cut_Test_FC5_V7_8_26_2024_Run1
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu 
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=13000
#SBATCH --time=1:40:00
#SBATCH --array=0-17


# source /group/clas12/packages/setup.csh
# source /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/New_RooUnfold/RooUnfold/build/setup.sh
# Main array: SBATCH --array=0-17
# Normal request: #SBATCH --mem-per-cpu=13000
# no_txt request: #SBATCH --mem-per-cpu=9000

# srun python3 /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/RooUnfold_SIDIS_richcap.py    smear_no_stat $SLURM_ARRAY_TASK_ID
srun python3 /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/RooUnfold_SIDIS_richcap.py no_smear_no_stat $SLURM_ARRAY_TASK_ID
