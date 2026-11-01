#!/bin/bash
# Two-shard SIDIS fit campaign. Does not unfold, start EvGen, or submit farm jobs.
set -u
ROOT="/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap"
PY="/Users/richardcapobianco/opt/miniforge3/envs/updated_python/bin/python"
PLAN="$ROOT/Systematic_Studies/physics_campaign/work_plan.json"
LOG="$ROOT/Systematic_Studies/physics_campaign/logs/campaign.log"
mkdir -p "$ROOT/Systematic_Studies/physics_campaign/logs"
cd "$ROOT"
echo "nominal start $(date)" >> "$LOG"
"$PY" Systematic_Studies/sidis_physics_cli.py run_shard -w "$PLAN" -p nominal -s 0 >> "$LOG" 2>&1 &
p0=$!
"$PY" Systematic_Studies/sidis_physics_cli.py run_shard -w "$PLAN" -p nominal -s 1 >> "$LOG" 2>&1 &
p1=$!
wait $p0
c0=$?
wait $p1
c1=$?
if [ "$c0" -ne 0 ] || [ "$c1" -ne 0 ]; then
  echo "FAILED: nominal shards rc=$c0,$c1" >> "$LOG"
  echo "FAILED: nominal shards rc=$c0,$c1"
  exit 1
fi
echo "variation start $(date)" >> "$LOG"
"$PY" Systematic_Studies/sidis_physics_cli.py run_shard -w "$PLAN" -p variation -s 0 >> "$LOG" 2>&1 &
v0=$!
"$PY" Systematic_Studies/sidis_physics_cli.py run_shard -w "$PLAN" -p variation -s 1 >> "$LOG" 2>&1 &
v1=$!
wait $v0
d0=$?
wait $v1
d1=$?
if [ "$d0" -ne 0 ] || [ "$d1" -ne 0 ]; then
  echo "FAILED: variation shards rc=$d0,$d1" >> "$LOG"
  echo "FAILED: variation shards rc=$d0,$d1"
  exit 1
fi
echo "DONE: fits $(date)" >> "$LOG"
echo "DONE: fits"
