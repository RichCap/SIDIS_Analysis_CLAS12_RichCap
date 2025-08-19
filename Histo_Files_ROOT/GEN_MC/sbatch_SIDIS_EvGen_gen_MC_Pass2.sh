#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=gdf_EvGen_8_19_2025_R1_Acceptance_Tests_V1
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu 
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=6500
#SBATCH --time=24:00:00
#SBATCH --array=0-9

FILES=(/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/Pass2/MC_Gen_sidis_epip_richcap.inb.qa.new5.45nA.inb-EvGen-LUND_EvGen_richcap_GEMC_Test-*)
# Normally requested time: --time=24:00:00

srun python3 /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/makeROOT_epip_SIDIS_histos_new.py gdf_sidis_NewP2 ${FILES[$SLURM_ARRAY_TASK_ID]}
