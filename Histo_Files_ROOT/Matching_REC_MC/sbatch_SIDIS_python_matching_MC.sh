#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=MC_Match_2_6_2024_Run1_New_Smearing_V4_Mom
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu 
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=2000
#SBATCH --time=14:00:00
#SBATCH --array=0-219


FILES=(/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/MC_Matching_sidis_epip_richcap.inb.qa.45nA_job_*)
# Above is for (mdf) #SBATCH --array=0-219

srun python3 /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/makeROOT_epip_SIDIS_histos_new.py mdf_mom ${FILES[$SLURM_ARRAY_TASK_ID]}
