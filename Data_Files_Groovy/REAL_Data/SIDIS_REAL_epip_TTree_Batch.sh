#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=sidis_REAL_richcap_epip_TTree_9_7_2022_All
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu 
#SBATCH --output=/farm_out/%u/%x-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=5500
#SBATCH --time=24:00:00
#SBATCH --array=0-172


FILES=(/cache/clas12/rg-a/production/recon/fall2018/torus-1/pass1/v0/dst/train/skim4/*)
# Above is for #SBATCH --array=0-173

srun Data_TTree_epip_Batch.groovy ${FILES[$SLURM_ARRAY_TASK_ID]}
