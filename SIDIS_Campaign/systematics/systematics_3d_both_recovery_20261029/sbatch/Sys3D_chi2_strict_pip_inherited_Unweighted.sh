#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --job-name=Sys3D_chi2_strict_pip_inherited_Unweighted
#SBATCH --output=/farm_out/richcap/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/richcap/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=15000
#SBATCH --time=1:40:00
#SBATCH --array=1-17
set -euo pipefail
BIN="${SLURM_ARRAY_TASK_ID}"
PAD=$(printf "%02d" "$BIN")
ROOT="/w/ceph24/hallb/clas12/users/richcap/SIDIS_Analysis_CLAS12_RichCap/SIDIS_Campaign/systematics/systematics_3d_both_recovery_20261029/unfold_parts/Sys3D_chi2_strict_pip_inherited_Unweighted_q2y${PAD}.root"
'/cvmfs/jlab.opensciencegrid.org/hallb/clas12/sw/almalinux9-gcc11/local/python/3.13.7/bin/python3' '/w/ceph24/hallb/clas12/users/richcap/SIDIS_Analysis_CLAS12_RichCap/run_Simple_Unfold.py' '-droot' 'work_b' '-u3D' '-err' 'covariance' '-ac' '0.02' '-bgs' 'rho0_new' '-ph' '24' '-b' "$BIN" '-sfin' '/w/ceph24/hallb/clas12/users/richcap/SIDIS_Analysis_CLAS12_RichCap/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_3D_Sys3D_chi2_strict_pip_Bank_cut_Complete_SIDIS_chi2_strict_pip_Response_Matrices_Final_Thesis_Files_All.root' '-r' "$ROOT" '--skip_compile'
