#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=RMatrix_Only_5D_Only_5D_nominal_spline_20261030_Bank_Response_Matrices_Final_Thesis_Files_10_30_2026
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=14GB
#SBATCH --time=12:00:00
#SBATCH --array=1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171

BATCH_ID=${SLURM_ARRAY_TASK_ID}
BATCH_PAD=$(printf "%03d" "${BATCH_ID}")
cd /lustre24/expphy/volatile/clas12/richcap/RDataFrames_to_Delete_from_work/Only_5D_Only_5D_nominal_spline_20261030_Bank_Response_Matrices_Final_Thesis_Files_10_30_2026
rm -f /lustre24/expphy/volatile/clas12/richcap/RDataFrames_to_Delete_from_work/Only_5D_Only_5D_nominal_spline_20261030_Bank_Response_Matrices_Final_Thesis_Files_10_30_2026/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_5D_Only_5D_nominal_spline_20261030_Bank_Response_Matrices_Final_Thesis_Files_Batch${BATCH_PAD}.root
/w/ceph24/hallb/clas12/users/richcap/SIDIS_Analysis_CLAS12_RichCap/Histo_Files_ROOT/DataFrames/Response_Matrix_Creation_using_RDataFrames.py --batch_id ${BATCH_ID} --data_root work_b -cnR cut_Complete_SIDIS -cnM cut_Complete_SIDIS --make_root --unfold_5D --fast --use_hpp --spline_weights --spline_file /w/ceph24/hallb/clas12/users/richcap/SIDIS_Analysis_CLAS12_RichCap/Prepare_Next_Iteration/acc020_3D_BC_RC_rawA_4D_xB_Fit_Pars_from_3D_BC_RC_Bayesian_Compute_SplineWeight.txt --hpp_input_file /w/ceph24/hallb/clas12/users/richcap/SIDIS_Analysis_CLAS12_RichCap/Histo_Files_ROOT/DataFrames/HPP_Files_Output/generated_acceptance_weights_Final_Thesis_noSpline.hpp --hpp_input_file_spline /w/ceph24/hallb/clas12/users/richcap/SIDIS_Analysis_CLAS12_RichCap/Histo_Files_ROOT/DataFrames/HPP_Files_Output/generated_acceptance_weights_Final_Thesis_withSpline.hpp --run_rho_weight --matching_criteria Bank -n Only_5D_Only_5D_nominal_spline_20261030_Bank_Response_Matrices_Final_Thesis_Files_Batch${BATCH_PAD} -r /lustre24/expphy/volatile/clas12/richcap/RDataFrames_to_Delete_from_work/Only_5D_Only_5D_nominal_spline_20261030_Bank_Response_Matrices_Final_Thesis_Files_10_30_2026/SIDIS_epip_Response_Matrices_from_RDataFrames.root --run_rho_weight --unfold_5D_only
