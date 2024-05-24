#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=Mod_P2_mdf_SIDIS_5_23_2024_Run1_Pass_2_5D_Unfold_Test_V6_SIDIS
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu 
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=5000
#SBATCH --time=14:00:00
#SBATCH --array=0-53


FILES=(/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/With_BeamCharge/Pass2/MC_Matching_sidis_epip_richcap.inb.qa.inb-clasdis_*)
# Above is for (mdf) #SBATCH --array=0-53
# Normally requested time: --time=14:00:00

srun python3 /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/makeROOT_epip_SIDIS_histos_new.py mdf_sidis_P2_NS_mod ${FILES[$SLURM_ARRAY_TASK_ID]}
