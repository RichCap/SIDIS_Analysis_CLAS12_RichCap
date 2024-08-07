#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=My_GEN_sidis_epip_TTree_8_7_2024_P2_WithPionCount_R1
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu 
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=5500
#SBATCH --time=4:00:00
#SBATCH --array=0-9


FILES=(/w/hallb-scshelf2102/clas12/richcap/SIDIS/New_MC_hipo/BeamEnergy_1060/inb-clasdis-7975*)
# Above is for #SBATCH --array=0-9

srun /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Data_Files_Groovy/GEN_MC/MC_Gen_TTree_epip_Batch_Pass2_UpToDate.groovy ${FILES[$SLURM_ARRAY_TASK_ID]}
