#!/bin/tcsh
# Environment probe. Run it only through swif_job.csh so swif_env.csh has already been sourced.
set failed = 0

which module >& /dev/null
if ($status != 0) then
  echo "missing command: module"
  set failed = 1
else
  echo "found command: module"
endif

which run-groovy >& /dev/null
if ($status != 0) then
  echo "missing command: run-groovy"
  set failed = 1
else
  echo "found command: run-groovy"
endif

if (! $?JYPATH) then
  echo "missing variable: JYPATH"
  set failed = 1
else
  echo "JYPATH is set"
endif

if (! $?QADB) then
  echo "missing variable: QADB"
  set failed = 1
else
  echo "QADB is set"
endif

module list |& grep -q clas12
if ($status != 0) then
  echo "missing CLAS12 module"
  set failed = 1
else
  echo "CLAS12 module is loaded"
endif

if ($failed != 0) then
  echo "swif_env_check failed"
  exit 1
endif
echo "swif_env_check ok"
exit 0
