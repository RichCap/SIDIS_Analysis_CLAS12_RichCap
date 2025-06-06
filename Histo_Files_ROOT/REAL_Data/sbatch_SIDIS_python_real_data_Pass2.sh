#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=FC14_rdf_SIDIS_5_9_2025_Run1_Sector_Tests_V1
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu 
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=3500
#SBATCH --time=12:00:00
#SBATCH --array=0-170


# FILES=(/w/hallb-scshelf2102/clas12/richcap/SIDIS/REAL_Data/Pass2/Data_sidis_epip_richcap.inb.qa.nSidis_005*)
# # Above is for (rdf) #SBATCH --array=0-170
# # Normally requested time: --time=8:00:00

FILES=(/w/hallb-scshelf2102/clas12/richcap/SIDIS/REAL_Data/Pass2/More_Cut_Info/Data_sidis_epip_richcap.inb.qa.new5.nSidis_005*)
# Above is for (rdf_NewP2 - As of 7/29/2024) #SBATCH --array=0-170
# Normally requested time: --time=8:00:00

srun python3 /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/makeROOT_epip_SIDIS_histos_new.py rdf_sidis_NewP2_FC_14 ${FILES[$SLURM_ARRAY_TASK_ID]}
