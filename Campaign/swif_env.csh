# Noninteractive CLAS12 setup for AlmaLinux 9 SWIF2 jobs.
# Sourced by swif_job.csh under /bin/tcsh -f. Do not read ~/.cshrc or ~/.login.
# source /site/env/syscshrc
# source /site/env/sysapps
# source /u/group/clas12/packages/setup.csh
# module load clas12/pro
# source /w/hallb-scshelf2102/clas12/kenjo/groovy/env.csh
# source /work/clas12/klest/RadCorrPythia/setup_radcorr.csh

if ( -e /etc/profile.d/modules.csh ) then
  source /etc/profile.d/modules.csh
else if ( -e /usr/share/Modules/init/tcsh ) then
  source /usr/share/Modules/init/tcsh
else
  echo "swif_env failed: the module command is not available to noninteractive tcsh"
  exit 1
endif
if ( ! $?MODULEPATH ) then
  echo "swif_env failed: MODULEPATH is unset after module initialization"
  exit 1
endif

module use /scigroup/cvmfs/hallb/clas12/sw/modulefiles
if ( $status != 0 ) then
  echo "swif_env failed: module use /scigroup/cvmfs/hallb/clas12/sw/modulefiles"
  exit 1
endif

module use /cvmfs/oasis.opensciencegrid.org/jlab/hallb/clas12/sw/modulefiles
if ( $status != 0 ) then
  echo "swif_env failed: module use oasis clas12 modulefiles"
  exit 1
endif

module load clas12
if ( $status != 0 ) then
  echo "swif_env failed: module load clas12"
  exit 1
endif

# Same RooUnfold setup.sh the working AlmaLinux 9 jobs source.
source /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/New_RooUnfold/RooUnfold/build/setup.sh
if ( $status != 0 ) then
  echo "swif_env failed: source RooUnfold setup.sh"
  exit 1
endif

if ( $?LD_LIBRARY_PATH ) then
  setenv LD_LIBRARY_PATH ${LD_LIBRARY_PATH}:/work/clas12/kenjo/j2root/alma9/build/
else
  setenv LD_LIBRARY_PATH /work/clas12/kenjo/j2root/alma9/build/
endif

# Groovy jars from the working AlmaLinux 9 line, then QADB if the clas12 module set it.
setenv JYPATH "/work/clas12/kenjo/groovy/lib/*"
if ( ! $?QADB ) then
  echo "swif_env failed: QADB is unset"
  exit 1
endif
setenv JYPATH "${JYPATH}:${QADB}/src"
