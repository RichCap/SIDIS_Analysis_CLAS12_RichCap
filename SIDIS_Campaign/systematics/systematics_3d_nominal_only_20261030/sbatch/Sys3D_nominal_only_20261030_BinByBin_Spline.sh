#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --job-name=Sys3D_nominal_only_20261030_BinByBin_Spline
#SBATCH --output=/farm_out/richcap/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/richcap/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=15000
#SBATCH --time=1:40:00
#SBATCH --array=1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17
set -euo pipefail
BIN="${SLURM_ARRAY_TASK_ID}"
PAD=$(printf "%02d" "$BIN")
ROOT="/w/ceph24/hallb/clas12/users/richcap/SIDIS_Analysis_CLAS12_RichCap/SIDIS_Campaign/systematics/systematics_3d_complete_20261029/unfold_parts/Sys3D_nominal_only_20261030_BinByBin_Spline_q2y${PAD}.root"
ROO=""
for cand in "$PWD/New_RooUnfold/RooUnfold/build-arm64" "$PWD/New_RooUnfold/RooUnfold/build" "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/New_RooUnfold/RooUnfold/build" "/w/ceph24/hallb/clas12/users/richcap/SIDIS_Analysis_CLAS12_RichCap/New_RooUnfold/RooUnfold/build"; do
  if [ -d "$cand" ]; then ROO="$cand"; break; fi
done
if [ -n "$ROO" ]; then
  export PYTHONPATH="$ROO${PYTHONPATH:+:$PYTHONPATH}"
  export LD_LIBRARY_PATH="$ROO${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
  export DYLD_LIBRARY_PATH="$ROO${DYLD_LIBRARY_PATH:+:$DYLD_LIBRARY_PATH}"
fi
'/cvmfs/jlab.opensciencegrid.org/hallb/clas12/sw/almalinux9-gcc11/local/python/3.13.7/bin/python3' '/w/ceph24/hallb/clas12/users/richcap/SIDIS_Analysis_CLAS12_RichCap/Simple_RooUnfold_SelfContained.py' '-droot' 'work_b' '-u3D' '-bbo' '-ac' '0.02' '-bgs' 'rho0_new' '-sfin' '/w/ceph24/hallb/clas12/users/richcap/SIDIS_Analysis_CLAS12_RichCap/Histo_Files_ROOT/DataFrames/hadd_ROOT_files_From_using_RDataFrames/SIDIS_epip_Response_Matrices_from_RDataFrames_Only_3D_Sys3D_nominal_only_20261030_Bank_Response_Matrices_Final_Thesis_Files_All.root' '-r' "$ROOT" '-wt' 'Spline' "$BIN"
