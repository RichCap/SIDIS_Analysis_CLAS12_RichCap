#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=Mod_MC_GEN_Gen_Cuts_V8_SIDIS_histo_9_1_2023_Modulated
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu 
#SBATCH --output=/farm_out/%u/%x-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=2500
#SBATCH --time=6:00:00
#SBATCH --array=0-219


FILES=(/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/MC_Gen_sidis_epip_richcap.inb.qa.45nA_job_*)
# Above is for (gdf) #SBATCH --array=0-219

srun python3 /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/makeROOT_epip_SIDIS_histos_new.py gdf_sidis_mod ${FILES[$SLURM_ARRAY_TASK_ID]}
