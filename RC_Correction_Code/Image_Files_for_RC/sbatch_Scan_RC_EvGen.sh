#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=RC_EvGen_Scan_2_10_2026_Run1
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu 
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=1000
#SBATCH --time=24:00:00
#SBATCH --array=1-515


echo "Starting at"; date; echo ""
/w/hallb-scshelf2102/clas12/richcap/Radiative_MC/SIDIS_RC_EvGen_richcap/Running_EvGen_richcap/./Make_RC_Factor_Plots_with_Kinematic_Bins.py -p "RC" -mm 0 -n "EvGen_Mods" -t "Default EvGen Modulations" -s -sn 3 -q -s -f -uj -json "/w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/RC_Correction_Code/Scanned_Fit_Parameters_for_RC.json" -4d $SLURM_ARRAY_TASK_ID
echo ""; echo "Stopped running at:"; date

