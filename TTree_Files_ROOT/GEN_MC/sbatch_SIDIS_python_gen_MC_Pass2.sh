#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=gdf_TTree_SIDIS_9_21_2024_Run2_New_TTree_V1_SIDIS
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu 
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=2000
#SBATCH --time=5:00:00
#SBATCH --array=0-223


FILES=(/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/Pass2/MC_Gen_sidis_epip_richcap.inb.qa.new5.inb-clasdis*)
# Above is for (gdf_NewP2 - As of 9/21/2024) #SBATCH --array=0-223
# Normally requested time: --time=12:00:00

srun python3 /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/TTree_create_ROOT_epip_SIDIS.py gdf_sidis ${FILES[$SLURM_ARRAY_TASK_ID]}
