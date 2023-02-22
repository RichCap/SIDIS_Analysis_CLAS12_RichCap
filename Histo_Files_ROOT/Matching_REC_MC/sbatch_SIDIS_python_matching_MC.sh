#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=MC_Matching_Analysis_Note_Update_V4_SIDIS_histo_2_20_2023
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu 
#SBATCH --output=/farm_out/%u/%x-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=28000
#SBATCH --time=24:00:00
#SBATCH --array=0-219


FILES=(/w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/MC_Matching_sidis_epip_richcap.inb.qa.45nA_job_*)
# Above is for (mdf/pdf) #SBATCH --array=0-219

# FILES=(/lustre19/expphy/volatile/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/Matched_REC_MC/MC_Matching_sidis_epip_richcap.inb.qa.45nA_job_*)
# # Above is for (mdf/pdf) #SBATCH --array=0-219


# srun python /lustre19/expphy/volatile/clas12/richcap/SIDIS_Analysis/makeROOT_epip_SIDIS_histos.py mdf ${FILES[$SLURM_ARRAY_TASK_ID]}
srun python /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/makeROOT_epip_SIDIS_histos_new.py mdf ${FILES[$SLURM_ARRAY_TASK_ID]}
