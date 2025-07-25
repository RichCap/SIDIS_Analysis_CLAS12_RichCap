#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=Just_RooUnfold_Sector_Tests_V1_R3_EvGen_7_22_2025
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu 
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=15000
#SBATCH --time=1:40:00
#SBATCH --array=1-17


# source /group/clas12/packages/setup.csh
# source /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/New_RooUnfold/RooUnfold/build/setup.sh
# Main array: SBATCH --array=0-17
# Normal request: #SBATCH --mem-per-cpu=13000
# no_txt request: #SBATCH --mem-per-cpu=9000

srun /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/./Just_RooUnfold_SIDIS_richcap.py -title "Made with EvGen" -r 'Unfolded_EvGen_Histos_From_Just_RooUnfold_SIDIS_richcap.root' -smear $SLURM_ARRAY_TASK_ID
