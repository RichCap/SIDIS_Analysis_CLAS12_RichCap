#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=REAL_Data_2_22_2024_Run2_New_Q2_Y_Bins_V1_SIDIS
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu 
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=2500
#SBATCH --time=6:00:00
#SBATCH --array=0,2,6,7,14,16,18,21,23,26,29,30,32,34-36,38,39,50,51,55-57,59,62,63,65,67-69,72-75,77,79,82,83,85,87,88,95,98,105,112,118,121,122,126,128,130-132,136,137,141-145,148-151,155,167


FILES=(/w/hallb-scshelf2102/clas12/richcap/SIDIS/REAL_Data/Data_sidis_epip_richcap.inb.qa.skim4_00*)
# Above is for (rdf) #SBATCH --array=0-173

srun python3 /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/makeROOT_epip_SIDIS_histos_new.py rdf_sidis ${FILES[$SLURM_ARRAY_TASK_ID]}
