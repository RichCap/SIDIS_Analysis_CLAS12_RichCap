#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=P2_rdf_Mom_6_14_2024_Run2_Pass_2_New_Smear_V13_Mom
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu 
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=2500
#SBATCH --time=6:00:00
#SBATCH --array=0-170
#SBATCH --constraint=el7

# FILES=(/w/hallb-scshelf2102/clas12/richcap/SIDIS/REAL_Data/Pass2/Data_sidis_epip_richcap.inb.qa.nSidis_005*)
# # Above is for (rdf) #SBATCH --array=0-170

FILES=(/w/hallb-scshelf2102/clas12/richcap/SIDIS/REAL_Data/Pass2/More_Cut_Info/Data_sidis_epip_richcap.inb.qa.new2.nSidis_005*)
# Above is for (rdf_NewP2) #SBATCH --array=0-170
# Normally requested time: --time=8:00:00


srun python3 /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/makeROOT_epip_SIDIS_histos_new.py rdf_mom_NewP2 ${FILES[$SLURM_ARRAY_TASK_ID]}
