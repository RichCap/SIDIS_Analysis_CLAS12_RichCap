#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name=EvGen_REC_SIDIS_epip_TTree_7_16_2025_Pass2_New_V5_R1
#SBATCH --mail-type=ALL
#SBATCH --mail-user=richard.capobianco@uconn.edu 
#SBATCH --output=/farm_out/%u/%x-%A_%a-%j-%N.out
#SBATCH --error=/farm_out/%u/%x-%A_%a-%j-%N.err
#SBATCH --partition=production
#SBATCH --account=clas12
#SBATCH --mem-per-cpu=5500
#SBATCH --time=24:00:00
#SBATCH --array=0-9


# FILES=(/w/hallb-scshelf2102/clas12/richcap/SIDIS/New_MC_hipo/BeamEnergy_1060/inb-clasdis-7975*)
# # Above is for #SBATCH --array=0-9

# FILES=(/lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/inb-clasdis-8183_*)
# # Above is for #SBATCH --array=0-9

# FILES=(/lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/inb-clasdis-8213_*
#     /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/inb-clasdis-8214_*
#     /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/inb-clasdis-8219_*
#     /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/inb-clasdis-8220_*
#     /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/inb-clasdis-8221_*)
# # Above is for #SBATCH --array=0-49

# FILES=(/lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/inb-clasdis-8*)
# # Above is for #SBATCH --array=0-139

# FILES=(/lustre24/expphy/volatile/clas12/akripko/inb-clasdis-osg_merged/inb-clasdis-*)
# # Above is for #SBATCH --array=0-8

# FILES=(/lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/inb-clasdis-8989_*
#        /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/inb-clasdis-9040_*
#        /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/inb-clasdis-8976_*
#        /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/inb-clasdis-9030_*
#        /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/inb-clasdis-9034_*
#        /lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/inb-clasdis-9047_*)
# # Above is for #SBATCH --array=0-59

FILES=(/lustre24/expphy/volatile/clas12/richcap/New_MC_SIDIS_Files_Volatile/inb-EvGen-LUND_EvGen_richcap_GEMC_Test-9427_*)
# Above is for #SBATCH --array=0-9

srun /w/hallb-scshelf2102/clas12/richcap/SIDIS/Matched_REC_MC/MC_Matched_TTree_epip_Batch.groovy ${FILES[$SLURM_ARRAY_TASK_ID]}
