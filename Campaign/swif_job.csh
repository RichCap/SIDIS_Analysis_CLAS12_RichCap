#!/bin/tcsh
# /bin/tcsh -f swif_job.csh <checkout> <command> [args...]
# -f is required. Without it, ~/.cshrc hits `if (! $?prompt) exit` before this file runs.
if ($#argv < 2) then
  echo "swif_job usage: swif_job.csh <checkout> <command> [args...]"
  exit 1
endif
set checkout = "$argv[1]"
shift
set envfile = "$0:h/swif_env.csh"
source "$envfile"
if ($status != 0) then
  echo "swif_job failed: source $envfile"
  exit 1
endif
cd "$checkout"
if ($status != 0) then
  echo "swif_job failed: cd $checkout"
  exit 1
endif
exec $argv:q
echo "swif_job failed: exec $argv[1]"
exit 127
