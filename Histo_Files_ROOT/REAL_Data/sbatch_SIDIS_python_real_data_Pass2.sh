#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=REAL_Data_2_20_2024_Run2_Pass_2_CrossCheck_V2_SIDIS
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu 
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=1500
#SBATCH --time=6:00:00
#SBATCH --array=17,25,30,31,36,39,42,43,49-51,59,70,72,73,78,80


FILES=(/w/hallb-scshelf2102/clas12/richcap/SIDIS/REAL_Data/Pass2/Data_sidis_epip_richcap.inb.qa.nSidis_005*)
# Above is for (rdf) #SBATCH --array=0-170

srun python3 /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/makeROOT_epip_SIDIS_histos_new.py rdf_sidis_P2 ${FILES[$SLURM_ARRAY_TASK_ID]}