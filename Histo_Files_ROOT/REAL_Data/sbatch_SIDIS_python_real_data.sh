#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=REAL_Data_Unfolding_Tests_V1_SIDIS_histo_11_3_2022
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu 
#SBATCH --output=/farm_out/%u/%x-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=7000
#SBATCH --time=24:00:00
#SBATCH --array=0-173


FILES=(/w/hallb-scshelf2102/clas12/richcap/SIDIS/REAL_Data/Data_sidis_epip_richcap.inb.qa.skim4_00*)
# Above is for (rdf) #SBATCH --array=0-173

# FILES=(/lustre19/expphy/volatile/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/REAL_Data/Data_sidis_epip_richcap.inb.qa.skim4_00*)
# # Above is for (rdf) #SBATCH --array=0-173


srun python /lustre19/expphy/volatile/clas12/richcap/SIDIS_Analysis/makeROOT_epip_SIDIS_histos.py rdf ${FILES[$SLURM_ARRAY_TASK_ID]}
