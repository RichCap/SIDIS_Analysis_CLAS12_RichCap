#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=GEN_claspyth_sidis_epip_TTree_10_10_2024_P2_WithPionCount_R1
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu 
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=5500
#SBATCH --time=4:00:00
#SBATCH --array=0-26


FILES=(/lustre24/expphy/volatile/clas12/sdiehl/osg_out/claspyth/inb-claspyth_*)
# Above is for #SBATCH --array=0-26

srun /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/GEN_MC/MC_Gen_TTree_epip_Batch_Pass2_UpToDate.groovy ${FILES[$SLURM_ARRAY_TASK_ID]}
