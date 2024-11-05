#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=P2_mdf_Mom_11_4_2024_Run1_Update_Cors_and_Cuts_V1_Mom
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu 
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=3500
#SBATCH --time=4:00:00
#SBATCH --array=0-273

# FILES=(/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/With_BeamCharge/Pass2/MC_Matching_sidis_epip_richcap.inb.qa.inb-clasdis_*)
## Above is for (mdf) #SBATCH --array=0-53

FILES=(/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/With_BeamCharge/Pass2/More_Cut_Info/MC_Matching_sidis_epip_richcap.inb.qa.new5.inb-clasdis*)
# Above is for (mdf_NewP2 - As of 9/26/2024) #SBATCH --array=0-273
# Normally requested time: --time=14:00:00


srun python3 /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/makeROOT_epip_SIDIS_histos_new.py mdf_mom_NewP2_FC_14 ${FILES[$SLURM_ARRAY_TASK_ID]}
