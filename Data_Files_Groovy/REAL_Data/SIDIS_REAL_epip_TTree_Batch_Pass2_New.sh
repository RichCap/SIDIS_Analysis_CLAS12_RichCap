#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=REAL_SIDIS_epip_TTree_7_26_2024_Pass2_New_V5_R2
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu 
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=5500
#SBATCH --time=2:00:00
#SBATCH --array=158-165

FILES=(/lustre19/expphy/cache/clas12/rg-a/production/recon/fall2018/torus-1/pass2/main/train/nSidis/nSidis_*)
# Above is for #SBATCH --array=0-170

srun /w/hallb-scshelf2102/clas12/richcap/SIDIS/REAL_Data/Pass2/Data_TTree_epip_Batch_Pass2.groovy ${FILES[$SLURM_ARRAY_TASK_ID]}
