#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=TP_gdf_TTree_11_8_2024_Run1_New_TTree_V2_SIDIS
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu 
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=5000
#SBATCH --time=14:00:00
#SBATCH --array=0-113


FILES=(/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/Pass2/MC_Gen_sidis_epip_richcap.inb.qa.wProton.new5.inb-clasdis*)
# Above is for (gdf_NewP2_Pro - As of 8/22/2024) #SBATCH --array=0-113
# Normally requested time: --time=14:00:00

srun python3 /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/TTree_create_ROOT_epip_SIDIS.py gdf_sidis_Pro ${FILES[$SLURM_ARRAY_TASK_ID]}
