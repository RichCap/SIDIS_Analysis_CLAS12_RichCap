#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=sidis_Matching_richcap_epip_TTree_9_12_2022_All
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu 
#SBATCH --output=/farm_out/%u/%x-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=5500
#SBATCH --time=24:00:00
#SBATCH --array=0-219


FILES=(/cache/clas12/rg-a/production/montecarlo/clasdis/fall2018/torus-1/v1/bkg45nA_10604MeV/45nA_job_*)
# Above is for #SBATCH --array=0-219

srun MC_Matched_TTree_epip_Batch.groovy ${FILES[$SLURM_ARRAY_TASK_ID]}
