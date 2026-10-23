#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=RMatrix_2D_Presentation_SIDIS_Workflow_Bank_Q2_Y_Bins_Final_Thesis_Files_10_22_2026
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=3GB
#SBATCH --time=12:00:00
#SBATCH --array=1-171

BATCH_ID=${SLURM_ARRAY_TASK_ID}
BATCH_PAD=$(printf "%03d" "${BATCH_ID}")
cd /lustre24/expphy/volatile/clas12/richcap/RDataFrames_to_Delete_from_work/2D_Presentation_SIDIS_Workflow_Bank_Q2_Y_Bins_Final_Thesis_Files_10_22_2026
/w/ceph24/hallb/clas12/users/richcap/SIDIS_Analysis_CLAS12_RichCap/Histo_Files_ROOT/DataFrames/Response_Matrix_Creation_using_RDataFrames.py --batch_id ${BATCH_ID} --data_root work_b -cnR cut_Complete_SIDIS -cnM cut_Complete_SIDIS --z_axis_2D Q2_Y_Bin --make_root --make_2D --unfold_5D --fast --use_hpp --spline_weights --spline_file /w/ceph24/hallb/clas12/users/richcap/SIDIS_Analysis_CLAS12_RichCap/Prepare_Next_Iteration/rho0_Subtracted_5D_V2_4D_xB_Fit_Pars_from_5D_BC_RC_Bayesian_Compute_SplineWeight.txt --hpp_input_file /w/ceph24/hallb/clas12/users/richcap/SIDIS_Analysis_CLAS12_RichCap/Histo_Files_ROOT/DataFrames/HPP_Files_Output/generated_acceptance_weights_Final_Thesis_noSpline.hpp --hpp_input_file_spline /w/ceph24/hallb/clas12/users/richcap/SIDIS_Analysis_CLAS12_RichCap/Histo_Files_ROOT/DataFrames/HPP_Files_Output/generated_acceptance_weights_Final_Thesis_withSpline.hpp --run_rho_weight --matching_criteria Bank -n 2D_Presentation_SIDIS_Workflow_Bank_Q2_Y_Bins_Final_Thesis_Files_Batch${BATCH_PAD} -r /lustre24/expphy/volatile/clas12/richcap/RDataFrames_to_Delete_from_work/2D_Presentation_SIDIS_Workflow_Bank_Q2_Y_Bins_Final_Thesis_Files_10_22_2026/SIDIS_epip_Response_Matrices_from_RDataFrames.root --make_2D_rho_normalization_only --run_rho_weight
