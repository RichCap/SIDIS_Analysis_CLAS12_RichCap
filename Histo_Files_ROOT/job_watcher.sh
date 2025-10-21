#!/usr/bin/env bash
#
# job_watcher.sh — simple PID watcher with optional follow-up actions
# Usage:
#   ./job_watcher.sh <PID> [command1] [command2] [...]
#
# Example:
#   ./job_watcher.sh 1301556 "python3 post_process.py" "mv results/*.root archive/"
#
# Notes:
#   - Uses `mail` to send notification to EMAIL (must be configured).
#   - Checks the process every CHECK_INTERVAL seconds.

# ==============================
# Configuration
# ==============================
EMAIL="richard.capobianco@uconn.edu"   # where to send completion notice
CHECK_INTERVAL=600                     # seconds between checks (currently set to check every 10 minutes)

# ==============================
# Parse inputs
# ==============================
if(( $# < 1 )); then
    echo "Usage: $0 <PID> [follow-up commands...]"
    exit 1
fi

PID="$1"
shift  # remaining args are optional follow-up commands

# ==============================
# Wait for the job to finish
# ==============================
start_time="$(date)"
echo "[$(date '+%H:%M:%S')] Monitoring process ${PID} ..."

while ps -p "$PID" > /dev/null 2>&1; do
    echo "Checking Job at: $(date '+%H:%M:%S')"
    sleep "$CHECK_INTERVAL"
done

end_time="$(date)"
echo "[$(date '+%H:%M:%S')] Process ${PID} has finished."

# # ==============================
# # Email notification
# # ==============================
# subject="Job ${PID} complete on $(hostname -s)"
# body="Your monitored job (PID ${PID}) has finished.

# Host: $(hostname -f)
# Start time: ${start_time}
# End time:   ${end_time}

# This message was sent automatically by job_watcher.sh."

# echo "$body" | mail -s "$subject" "$EMAIL"
# echo "[$(date '+%H:%M:%S')] Notification sent to ${EMAIL}."

# ==============================
# Follow-up actions
# ==============================

echo "[$(date '+%H:%M:%S')] Beginning follow-up actions..."

# 1) Check if squeue_wc <= 4, and conditionally hold jobs
RUN_HOLD=0
SQUEUE_COUNT=$(squeue_wc 2>/dev/null)

if(( $? == 0 )); then
    echo "[$(date '+%H:%M:%S')] squeue_wc returned: ${SQUEUE_COUNT}"
    if(( SQUEUE_COUNT <= 4 )); then
        echo "[$(date '+%H:%M:%S')] Running: scontrol hold 56056065 56056383"
        scontrol hold 56056065 56056383
        RUN_HOLD=1
    else
        echo "[$(date '+%H:%M:%S')] Skipping hold command (squeue_wc = ${SQUEUE_COUNT} > 4)."
    fi
else
    echo "[$(date '+%H:%M:%S')] Warning: squeue_wc command not found or failed."
fi

# 2) Run Pass_2_sbatch_submit_scripts.sh
echo "[$(date '+%H:%M:%S')] Running: ./Pass_2_sbatch_submit_scripts.sh --skip-rdf"
./Pass_2_sbatch_submit_scripts.sh --skip-rdf
SUBMIT_EXIT=$?
if(( SUBMIT_EXIT == 0 )); then
    echo "[$(date '+%H:%M:%S')] Pass_2_sbatch_submit_scripts.sh completed successfully."
else
    echo "[$(date '+%H:%M:%S')] Warning: Pass_2_sbatch_submit_scripts.sh exited with code ${SUBMIT_EXIT}."
fi

# 3) Prepare and send final email summary
EMAIL_SUBJECT="Job ${PID} finished — Follow-up complete on $(hostname -s)"

# Header
EMAIL_BODY="Your monitored job (PID ${PID}) has finished and follow-up actions were performed.

Host: $(hostname -f)
Time: $(date)
------------------------------------------------------------
"

# Script execution summary
if(( SUBMIT_EXIT == 0 )); then
    EMAIL_BODY+="✔ Pass_2_sbatch_submit_scripts.sh --skip-rdf was run successfully.\n"
else
    EMAIL_BODY+="⚠ Pass_2_sbatch_submit_scripts.sh encountered an error (exit code ${SUBMIT_EXIT}).\n"
fi

if(( RUN_HOLD == 1 )); then
    EMAIL_BODY+="✔ scontrol hold 56056065 56056383 was executed because squeue_wc <= 4.\n"
    EMAIL_BODY+="Release these held jobs with this command when the new jobs are done:\n"
    EMAIL_BODY+="    scontrol release 56056065 56056383\n"
else
    EMAIL_BODY+="ℹ scontrol hold was not run (either squeue_wc > 4 or squeue_wc failed).\n"
fi

EMAIL_BODY+="------------------------------------------------------------
Current SQueue (formatted):
$(SQueue_format 2>&1)
------------------------------------------------------------"

echo -e "$EMAIL_BODY" | mail -s "$EMAIL_SUBJECT" "$EMAIL"

echo "[$(date '+%H:%M:%S')] Follow-up email sent to ${EMAIL}."
echo "[$(date '+%H:%M:%S')] Follow-up actions complete."


echo "[$(date '+%H:%M:%S')] job_watcher.sh finished."
