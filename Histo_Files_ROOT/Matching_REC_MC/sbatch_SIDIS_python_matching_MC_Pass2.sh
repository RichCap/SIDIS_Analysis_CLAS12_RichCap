#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=P2_mdf_SIDIS_4_2_2024_Run2_Pass_2_New_Q2_Y_Bins_V4_SIDIS
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu 
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=4500
#SBATCH --time=12:00:00
#SBATCH --array=0-53


FILES=(/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/With_BeamCharge/Pass2/MC_Matching_sidis_epip_richcap.inb.qa.inb-clasdis_*)
# Above is for (mdf) #SBATCH --array=0-53

srun python3 /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/makeROOT_epip_SIDIS_histos_new.py mdf_sidis_P2 ${FILES[$SLURM_ARRAY_TASK_ID]}
