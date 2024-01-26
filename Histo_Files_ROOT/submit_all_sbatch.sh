#!/bin/bash

DIR_WITH_SCRIPTS="/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/Histo_Files_ROOT"
echo "Submitting jobs for running makeROOT_epip_SIDIS_histos_new.py"
echo ""
echo "Currently Running Jobs:"
squeue -u richcap
echo "Total:"
squeue -u richcap | wc -l
echo ""

# Submit Normally:
echo "Submitting for mdf file in:"
cd "${DIR_WITH_SCRIPTS}/Matching_REC_MC/"
pwd
# cat ${DIR_WITH_SCRIPTS}/Matching_REC_MC/sbatch_SIDIS_python_matching_MC.sh
sbatch ${DIR_WITH_SCRIPTS}/Matching_REC_MC/sbatch_SIDIS_python_matching_MC.sh

# echo "Skipping gdf files..."
echo "Submitting for gdf file in:"
cd "${DIR_WITH_SCRIPTS}/GEN_MC/"
pwd
# cat ${DIR_WITH_SCRIPTS}/GEN_MC/sbatch_SIDIS_python_gen_MC.sh
sbatch ${DIR_WITH_SCRIPTS}/GEN_MC/sbatch_SIDIS_python_gen_MC.sh

echo "Submitting for rdf file in:"
cd "${DIR_WITH_SCRIPTS}/REAL_Data/"
pwd
# cat ${DIR_WITH_SCRIPTS}/REAL_Data/sbatch_SIDIS_python_real_data.sh
sbatch ${DIR_WITH_SCRIPTS}/REAL_Data/sbatch_SIDIS_python_real_data.sh


# # # Submit with dependencies:
# echo "Submitting for mdf file in:"
# cd "${DIR_WITH_SCRIPTS}/Matching_REC_MC/"
# pwd
# JOB_ID=$(sbatch ${DIR_WITH_SCRIPTS}/Matching_REC_MC/sbatch_SIDIS_python_matching_MC.sh | awk '{print $4}')
# echo "Submitting for gdf file in:"
# cd "${DIR_WITH_SCRIPTS}/GEN_MC/"
# pwd
# JOB_ID=$(sbatch --dependency=afterany:$JOB_ID ${DIR_WITH_SCRIPTS}/GEN_MC/sbatch_SIDIS_python_gen_MC.sh | awk '{print $4}')
# echo "Submitting for rdf file in:"
# cd "${DIR_WITH_SCRIPTS}/REAL_Data/"
# pwd
# JOB_ID=$(sbatch --dependency=afterany:$JOB_ID ${DIR_WITH_SCRIPTS}/REAL_Data/sbatch_SIDIS_python_real_data.sh | awk '{print $4}')



echo ""
echo "Done submitting all jobs"
echo "Currently Running Jobs:"
squeue -u richcap
echo "Total:"
squeue -u richcap | wc -l



