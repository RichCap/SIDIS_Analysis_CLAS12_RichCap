#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=rdf_DF_9_2_2026_R1_Final_Thesis_Files
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=4GB
#SBATCH --time=01:00:00
#SBATCH --array=1-171

FILELIST="/w/ceph24/hallb/clas12/users/richcap/SIDIS_Analysis_CLAS12_RichCap/Histo_Files_ROOT/DataFrames/REAL_Data/rdf_DF_9_2_2026_R1_Final_Thesis_Files_filelist.txt"
INPUT_FILE=$(sed -n "${SLURM_ARRAY_TASK_ID}p" "${FILELIST}")
cd /w/ceph24/hallb/clas12/users/richcap/SIDIS_Analysis_CLAS12_RichCap/Histo_Files_ROOT/DataFrames/REAL_Data
/w/ceph24/hallb/clas12/users/richcap/SIDIS_Analysis_CLAS12_RichCap/dataframe_makeROOT_epip_SIDIS.py rdf --sidis --Common_Name Final_Thesis_Files_ --file "${INPUT_FILE}"
