#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=REAL_Data_New_Binning_Schemes_V6_SIDIS_histo_6_2_2023
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu 
#SBATCH --output=/farm_out/%u/%x-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=4000
#SBATCH --time=24:00:00
#SBATCH --array=0-173


FILES=(/w/hallb-scshelf2102/clas12/richcap/SIDIS/REAL_Data/Data_sidis_epip_richcap.inb.qa.skim4_00*)
# Above is for (rdf) #SBATCH --array=0-173

srun python3 /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/makeROOT_epip_SIDIS_histos_new.py rdf ${FILES[$SLURM_ARRAY_TASK_ID]}

