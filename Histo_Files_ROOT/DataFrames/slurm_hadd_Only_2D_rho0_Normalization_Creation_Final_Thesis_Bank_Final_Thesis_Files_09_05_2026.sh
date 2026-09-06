#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=RMatrix_hadd_Only_2D_rho0_Normalization_Creation_Final_Thesis_Bank_Final_Thesis_Files_09_05_2026
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=2GB
#SBATCH --time=04:00:00

hadd -f /w/ceph24/hallb/clas12/users/richcap/SIDIS_Analysis_CLAS12_RichCap/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_2D_rho0_Normalization_Creation_Final_Thesis_Bank_Final_Thesis_Files_09_05_2026.root /lustre24/expphy/volatile/clas12/richcap/RDataFrames_to_Delete_from_work/Only_2D_rho0_Normalization_Creation_Final_Thesis_Bank_Final_Thesis_Files_09_05_2026/*Batch*.root
