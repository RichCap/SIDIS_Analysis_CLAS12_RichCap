#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=RMatrix_Only_2D_rho0_Normalization_Creation_Final_Thesis_Bank_Final_Thesis_Files_09_05_2026
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=4GB
#SBATCH --time=12:00:00
#SBATCH --array=1-171

BATCH_ID=${SLURM_ARRAY_TASK_ID}
BATCH_PAD=$(printf "%03d" "${BATCH_ID}")
cd /lustre24/expphy/volatile/clas12/richcap/RDataFrames_to_Delete_from_work/Only_2D_rho0_Normalization_Creation_Final_Thesis_Bank_Final_Thesis_Files_09_05_2026
/w/ceph24/hallb/clas12/users/richcap/SIDIS_Analysis_CLAS12_RichCap/Histo_Files_ROOT/DataFrames/Response_Matrix_Creation_using_RDataFrames.py --batch_id ${BATCH_ID} --data_root work_b -cnR cut_Complete_SIDIS -cnM cut_Complete_SIDIS --z_axis_2D z_Bins --make_root --make_2D --fast --run_rho_weight --matching_criteria Bank -n Only_2D_rho0_Normalization_Creation_Final_Thesis_Bank_Final_Thesis_Files_Batch${BATCH_PAD} -r /lustre24/expphy/volatile/clas12/richcap/RDataFrames_to_Delete_from_work/Only_2D_rho0_Normalization_Creation_Final_Thesis_Bank_Final_Thesis_Files_09_05_2026/SIDIS_epip_Response_Matrices_from_RDataFrames.root --make_2D_rho_normalization_only --run_rho_weight
