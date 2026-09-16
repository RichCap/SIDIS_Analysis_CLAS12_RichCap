#!/bin/tcsh
# Cancel one SLURM array task. Split tasks use JOBID_N; compact pending arrays need JOBID_[N].
# Quotes keep [N] from being treated as a glob.

if ($# != 2) then
    echo "Usage: $0 ARRAY_JOBID TASK_INDEX"
    exit 2
endif

set jobid = "$1"
set task  = "$2"
set split = "${jobid}_${task}"
set bracket = "${jobid}_[${task}]"

scancel "${split}"
if ($status == 0) then
    echo "Cancelled ${split}"
    exit 0
endif

scancel "${bracket}"
if ($status == 0) then
    echo "Cancelled ${bracket}"
    exit 0
endif

echo "scancel failed for ${split} and ${bracket}"
exit 1
