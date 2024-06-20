#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=P2_mdf_Mom_6_14_2024_Run2_Pass_2_New_Smear_V13_Mom
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu 
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=3500
#SBATCH --time=4:00:00
#SBATCH --array=0-53
#SBATCH --constraint=el7

# FILES=(/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/With_BeamCharge/Pass2/MC_Matching_sidis_epip_richcap.inb.qa.inb-clasdis_*)
## Above is for (mdf) #SBATCH --array=0-53

FILES=(/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/With_BeamCharge/Pass2/More_Cut_Info/MC_Matching_sidis_epip_richcap.inb.qa.new2.inb-clasdis_*)
# Above is for (mdf_NewP2) #SBATCH --array=0-53
# Normally requested time: --time=14:00:00


srun python3 /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/makeROOT_epip_SIDIS_histos_new.py mdf_mom_NewP2 ${FILES[$SLURM_ARRAY_TASK_ID]}
