# Noninteractive CLAS12/Groovy setup for SWIF2 jobs.
# Sourced by swif_job.csh. This is not ~/.login: no syslogin, stty, or prompt setup.
# ~/.cshrc exits when $?prompt is unset, so a batch tcsh must not rely on it.

source /site/env/syscshrc
if ($status != 0) then
  echo "swif_env failed: source /site/env/syscshrc"
  exit 1
endif

source /site/env/sysapps
if ($status != 0) then
  echo "swif_env failed: source /site/env/sysapps"
  exit 1
endif

source /u/group/clas12/packages/setup.csh
if ($status != 0) then
  echo "swif_env failed: source /u/group/clas12/packages/setup.csh"
  exit 1
endif

module load clas12/pro
if ($status != 0) then
  echo "swif_env failed: module load clas12/pro"
  exit 1
endif

source /w/hallb-scshelf2102/clas12/richcap/SIDIS_Analysis/New_RooUnfold/RooUnfold/build/setup.sh
if ($status != 0) then
  echo "swif_env failed: source RooUnfold setup.sh"
  exit 1
endif

source /w/hallb-scshelf2102/clas12/kenjo/groovy/env.csh
if ($status != 0) then
  echo "swif_env failed: source groovy env.csh"
  exit 1
endif

source /w/hallb-scshelf2102/clas12/kenjo/groovy/env.csh
if ($status != 0) then
  echo "swif_env failed: source groovy env.csh (second time)"
  exit 1
endif

if (! $?JYPATH) then
  echo "swif_env failed: JYPATH is unset"
  exit 1
endif
if (! $?QADB) then
  echo "swif_env failed: QADB is unset"
  exit 1
endif
setenv JYPATH "${JYPATH}:${QADB}/src"

source /work/clas12/klest/RadCorrPythia/setup_radcorr.csh
if ($status != 0) then
  echo "swif_env failed: source setup_radcorr.csh"
  exit 1
endif
