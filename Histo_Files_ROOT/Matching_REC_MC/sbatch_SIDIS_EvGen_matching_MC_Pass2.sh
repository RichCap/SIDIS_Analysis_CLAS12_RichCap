#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=EvGen_mdf_9_2_2025_R3_FC14_Acceptance_Tests_V1
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu 
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=7500
#SBATCH --time=24:00:00
#SBATCH --array=0-39



FILES=(/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/With_BeamCharge/Pass2/More_Cut_Info/MC_Matching_sidis_epip_richcap.inb.qa.new5.45nA.inb-EvGen-LUND_EvGen_richcap_GEMC*)
# Above is for EvGen files as of 9/2/2025: #SBATCH --array=0-39

# FILES=(/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/With_BeamCharge/Pass2/More_Cut_Info/MC_Matching_sidis_epip_richcap.inb.qa.new5.45nA.inb-EvGen-LUND_EvGen_richcap_GEMC_Test-*)
# # Above is for EvGen files as of 8/19/2025: #SBATCH --array=0-9

# Normally requested time: --time=14:00:00

srun python3 /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/makeROOT_epip_SIDIS_histos_new.py mdf_sidis_NewP2_FC_14_no_smear ${FILES[$SLURM_ARRAY_TASK_ID]}
