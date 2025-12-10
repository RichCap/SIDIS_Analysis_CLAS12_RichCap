#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=FirstOrder_12_08_2025_hadd_batches
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=1GB
#SBATCH --time=04:00:00


$ROOTSYS/bin/hadd -f /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_All_File_Types_from_RDataFrames_FirstOrder_Fixed.root /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_All_File_Types_from_RDataFrames_FirstOrder_Fixed_Batch[1-9]*.root