#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=mdf_TTree_SIDIS_9_10_2024_Run1_New_TTree_V1_SIDIS
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu 
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=5000
#SBATCH --time=14:00:00
#SBATCH --array=0-123


FILES=(/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/With_BeamCharge/Pass2/More_Cut_Info/MC_Matching_sidis_epip_richcap.inb.qa.new5.inb-clasdis*)
# Above is for (mdf_NewP2 - As of 9/9/2024) #SBATCH --array=0-123
# Normally requested time: --time=14:00:00

srun python3 /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/TTree_create_ROOT_epip_SIDIS.py mdf_sidis ${FILES[$SLURM_ARRAY_TASK_ID]}
