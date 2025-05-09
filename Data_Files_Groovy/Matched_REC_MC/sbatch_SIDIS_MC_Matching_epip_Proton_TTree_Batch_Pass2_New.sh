#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=P_MC_REC_SIDIS_epip_Proton_TTree_7_25_2024_Pass2_New_V5
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu 
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=5500
#SBATCH --time=24:00:00
#SBATCH --array=0-53


FILES=(/lustre19/expphy/volatile/clas12/sdiehl/osg_out/clasdis/inb-clasdis_*)
# Above is for #SBATCH --array=0-53

# FILES=(/lustre19/expphy/volatile/clas12/sdiehl/osg_out/claspyth/inb-claspyth_*)
# # Above is for #SBATCH --array=0-26

srun /w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/MC_Matched_TTree_epip_Proton_Batch.groovy ${FILES[$SLURM_ARRAY_TASK_ID]}
