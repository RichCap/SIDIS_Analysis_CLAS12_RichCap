#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=FC14_mdf_EvGen_7_22_2025_Run1_Sector_Tests_V2
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu 
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=7500
#SBATCH --time=24:00:00
#SBATCH --array=0-9


FILES=(/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/With_BeamCharge/Pass2/More_Cut_Info/MC_Matching_sidis_epip_richcap.inb.qa.new5.45nA.inb-EvGen-LUND_EvGen_richcap_GEMC_Test-*)
# Normally requested time: --time=14:00:00

srun python3 /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/makeROOT_epip_SIDIS_histos_new.py mdf_sidis_NewP2_FC_14 ${FILES[$SLURM_ARRAY_TASK_ID]}
