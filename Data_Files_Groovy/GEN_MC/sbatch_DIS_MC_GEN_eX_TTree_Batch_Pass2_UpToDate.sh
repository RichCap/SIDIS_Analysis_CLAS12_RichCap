#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=GEN_DIS_eX_TTree_10_15_2024_P2_R1
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu 
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=5500
#SBATCH --time=4:00:00
#SBATCH --array=0-53


FILES=(/lustre19/expphy/volatile/clas12/sdiehl/osg_out/clasdis/inb-clasdis_*)
# Above is for #SBATCH --array=0-53

srun /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/GEN_MC/MC_Gen_TTree_eX_Batch_Pass2_UpToDate.groovy ${FILES[$SLURM_ARRAY_TASK_ID]}
