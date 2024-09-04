#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=P2_gdf_SIDIS_9_4_2024_Run1_New_Fiducial_Cut_Test_V10_SIDIS
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu 
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=2000
#SBATCH --time=5:00:00
#SBATCH --array=0-113

# FILES=(/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/Pass2/MC_Gen_sidis_epip_richcap.inb.qa.inb-clasdis_*)
# # Above is for (gdf) #SBATCH --array=0-53
# # Normally requested time: --time=12:00:00

FILES=(/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/Pass2/MC_Gen_sidis_epip_richcap.inb.qa.new5.inb-clasdis*)
# Above is for (mdf_NewP2 - As of 8/22/2024) #SBATCH --array=0-113
# Normally requested time: --time=12:00:00


srun python3 /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/makeROOT_epip_SIDIS_histos_new.py gdf_sidis_NewP2 ${FILES[$SLURM_ARRAY_TASK_ID]}
