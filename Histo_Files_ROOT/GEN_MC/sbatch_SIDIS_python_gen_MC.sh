#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=MC_GEN_Unfolding_Tests_V1_SIDIS_histo_11_3_2022
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu 
#SBATCH --output=/farm_out/%u/%x-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=7000
#SBATCH --time=24:00:00
#SBATCH --array=0-219


FILES=(/w/hallb-scshelf2102/clas12/richcap/SIDIS/GEN_MC/MC_Gen_sidis_epip_richcap.inb.qa.45nA_job_*)
# Above is for (gdf) #SBATCH --array=0-219

# FILES=(/lustre19/expphy/volatile/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/GEN_MC/MC_Gen_sidis_epip_richcap.inb.qa.45nA_job_*)
# # Above is for (gdf) #SBATCH --array=0-219


srun python /lustre19/expphy/volatile/clas12/richcap/SIDIS_Analysis/makeROOT_epip_SIDIS_histos.py gdf ${FILES[$SLURM_ARRAY_TASK_ID]}
