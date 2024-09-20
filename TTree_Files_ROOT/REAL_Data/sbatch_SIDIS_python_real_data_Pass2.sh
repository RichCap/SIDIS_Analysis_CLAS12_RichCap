#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=rdf_TTree_SIDIS_9_13_2024_Run1_New_TTree_V1_SIDIS
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu 
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=3500
#SBATCH --time=9:00:00
#SBATCH --array=0-170


FILES=(/w/hallb-scshelf2102/clas12/richcap/SIDIS/REAL_Data/Pass2/More_Cut_Info/Data_sidis_epip_richcap.inb.qa.new5.nSidis_005*)
# Above is for (rdf_NewP2 - As of 7/29/2024) #SBATCH --array=0-170
# Normally requested time: --time=8:00:00

srun python3 /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/TTree_create_ROOT_epip_SIDIS.py rdf_sidis ${FILES[$SLURM_ARRAY_TASK_ID]}
