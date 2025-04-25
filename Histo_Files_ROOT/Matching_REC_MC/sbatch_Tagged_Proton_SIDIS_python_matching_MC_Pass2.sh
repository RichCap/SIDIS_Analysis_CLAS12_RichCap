#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=FC14_TP_mdf_SIDIS_4_24_2025_Run2_Plots_for_Maria_V3_SIDIS
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu 
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=5000
#SBATCH --time=14:00:00
#SBATCH --array=0-253


# FILES=(/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/With_BeamCharge/Pass2/More_Cut_Info/MC_Matching_sidis_epip_richcap.inb.qa.wProton.new5.inb-clasdis*)
# # Above is for (mdf_NewP2_Pro - As of 8/22/2024) #SBATCH --array=0-113
# # Normally requested time: --time=14:00:00

FILES=(/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/With_BeamCharge/Pass2/More_Cut_Info/MC_Matching_sidis_epip_richcap.inb.qa.wProton.new5*.inb-clasdis*)
# Above is for (mdf_NewP2_Pro - As of 4/23/2025) #SBATCH --array=0-253
# Normally requested time: --time=14:00:00

# srun python3 /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/makeROOT_epip_SIDIS_histos_new.py mdf_sidis_NewP2_Pro_NS_FC_14 ${FILES[$SLURM_ARRAY_TASK_ID]}
srun python3 /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/makeROOT_epip_SIDIS_histos_new.py mdf_sidis_NewP2_Pro_FC_14 ${FILES[$SLURM_ARRAY_TASK_ID]}
