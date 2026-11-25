#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=RMatrix_RecW_Creation_RecW_physiter1_hist_recs_spline1_Bank_Response_Matrices_iter1_Final_Thesis_Files_11_25_2026
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=8GB
#SBATCH --time=24:00:00
#SBATCH --array=1-171

BATCH_ID=${SLURM_ARRAY_TASK_ID}
BATCH_PAD=$(printf "%03d" "${BATCH_ID}")
cd /lustre24/expphy/volatile/clas12/richcap/RDataFrames_to_Delete_from_work/RecW_Creation_RecW_physiter1_hist_recs_spline1_Bank_Response_Matrices_iter1_Final_Thesis_Files_11_25_2026
/w/ceph24/hallb/clas12/users/richcap/SIDIS_Analysis_CLAS12_RichCap/Histo_Files_ROOT/DataFrames/Response_Matrix_Creation_using_RDataFrames.py --batch_id ${BATCH_ID} --data_root work_b -cnR cut_Complete_SIDIS -cnM cut_Complete_SIDIS --make_root --unfold_5D --fast --spline_weights --spline_file /w/ceph24/hallb/clas12/users/richcap/SIDIS_Analysis_CLAS12_RichCap/Prepare_Next_Iteration/acc020_3D_BC_RC_normGenA_iter1_4D_xB_Fit_Pars_from_3D_BC_RC_Bayesian_Compute_SplineWeight.txt --run_rho_weight --matching_criteria Bank -n RecW_Creation_RecW_physiter1_hist_recs_spline1_Bank_Response_Matrices_Final_Thesis_Files_Batch${BATCH_PAD} -r /lustre24/expphy/volatile/clas12/richcap/RDataFrames_to_Delete_from_work/RecW_Creation_RecW_physiter1_hist_recs_spline1_Bank_Response_Matrices_iter1_Final_Thesis_Files_11_25_2026/SIDIS_epip_Response_Matrices_from_RDataFrames.root --run_rho_weight --unfold_5D_only --recw_creation --recw_task hist_recs_spline1 --spline_weights --reconstruction_weight recs --cumulative_iteration 1 --recw_header /w/ceph24/hallb/clas12/users/richcap/SIDIS_Analysis_CLAS12_RichCap/Histo_Files_ROOT/DataFrames/RecW_Output/RecW_Tables.hpp
