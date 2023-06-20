#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=RooUnfold_python_SIDIS_Gen_Cuts_V1_smear_histo_6_16_2023
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu 
#SBATCH --output=/farm_out/%u/%x-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=6000
#SBATCH --time=4:00:00
#SBATCH --array=0-17


source /group/clas12/packages/setup.csh
source /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/New_RooUnfold/RooUnfold/build/setup.sh

srun python3 /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/RooUnfold_SIDIS_richcap.py save $SLURM_ARRAY_TASK_ID
