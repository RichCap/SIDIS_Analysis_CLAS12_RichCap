#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=rdf_SIDIS_5_24_2024_Run1_5D_Unfold_Test_V7_SIDIS
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu 
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=2500
#SBATCH --time=6:00:00
#SBATCH --array=0-173
#SBATCH --constraint=el7


FILES=(/w/hallb-scshelf2102/clas12/richcap/SIDIS/REAL_Data/Data_sidis_epip_richcap.inb.qa.skim4_00*)
# Above is for (rdf) #SBATCH --array=0-173

srun python3 /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/makeROOT_epip_SIDIS_histos_new.py rdf_sidis ${FILES[$SLURM_ARRAY_TASK_ID]}
