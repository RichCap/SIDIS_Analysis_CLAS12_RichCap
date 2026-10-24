#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=RMatrix_Diagnostic_1D_SIDIS_Workflow_Bank_Final_Thesis_Files_10_24_2026
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=5GB
#SBATCH --time=12:00:00
#SBATCH --array=1-171

BATCH_ID=${SLURM_ARRAY_TASK_ID}
BATCH_PAD=$(printf "%03d" "${BATCH_ID}")
cd /lustre24/expphy/volatile/clas12/richcap/RDataFrames_to_Delete_from_work/Diagnostic_1D_SIDIS_Workflow_Bank_Final_Thesis_Files_10_24_2026
/w/ceph24/hallb/clas12/users/richcap/SIDIS_Analysis_CLAS12_RichCap/Histo_Files_ROOT/DataFrames/Response_Matrix_Creation_using_RDataFrames.py --batch_id ${BATCH_ID} --data_root work_b -cnR cut_Complete_SIDIS -cnM cut_Complete_SIDIS --make_root --fast --run_rho_weight --matching_criteria Bank -n Diagnostic_1D_SIDIS_Workflow_Bank_Final_Thesis_Files_Batch${BATCH_PAD} -r /lustre24/expphy/volatile/clas12/richcap/RDataFrames_to_Delete_from_work/Diagnostic_1D_SIDIS_Workflow_Bank_Final_Thesis_Files_10_24_2026/SIDIS_epip_Response_Matrices_from_RDataFrames.root --diagnostic_1d
