#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=MC_GEN_2_27_2024_Run1_Pass_2_New_Q2_Y_Bins_V2_SIDIS
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu 
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=1500
#SBATCH --time=24:00:00
#SBATCH --array=0-53


FILES=(/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/Pass2/MC_Gen_sidis_epip_richcap.inb.qa.inb-clasdis_*)
# Above is for (gdf) #SBATCH --array=0-53

srun python3 /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/makeROOT_epip_SIDIS_histos_new.py gdf_sidis_P2 ${FILES[$SLURM_ARRAY_TASK_ID]}
