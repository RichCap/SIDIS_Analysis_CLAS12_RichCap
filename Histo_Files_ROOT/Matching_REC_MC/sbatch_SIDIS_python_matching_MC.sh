#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=mdf_SIDIS_5_24_2024_Run1_5D_Unfold_Test_V7_SIDIS
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu 
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=4000
#SBATCH --time=16:00:00
#SBATCH --array=0-219
#SBATCH --constraint=el7


FILES=(/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/MC_Matching_sidis_epip_richcap.inb.qa.45nA_job_*)
# Above is for (mdf) #SBATCH --array=0-219
# Normally requested time: --time=16:00:00

srun python3 /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/makeROOT_epip_SIDIS_histos_new.py mdf_sidis ${FILES[$SLURM_ARRAY_TASK_ID]}
