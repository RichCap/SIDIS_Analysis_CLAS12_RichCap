#!/bin/zsh
# Apply finished factor caches, then fit them one or two at a time.
# Nominal files under corrected/ are read and never replaced.
set -u
PY="/Users/richardcapobianco/opt/miniforge3/envs/updated_python/bin/python"
REPO="/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap"
ALT="$REPO/Systematic_Studies/physics_campaign/alternatives"
CACHE="$REPO/Systematic_Studies/physics_campaign/fixed_point"
APPLY="$REPO/Systematic_Studies/apply_nominal_corrections.py"
FIT="$REPO/Simple_RooUnfold_SelfContained.py"
ROO="$REPO/New_RooUnfold/RooUnfold/build-arm64"
UW="$REPO/SIDIS_Campaign/systematics/systematics_3d_complete_20261029/unfolded/Sys3D_nominal_only_20261030_inherited_Unweighted.root"
SP="$REPO/SIDIS_Campaign/systematics/systematics_3d_complete_20261029/unfolded/Sys3D_nominal_only_20261030_inherited_Spline.root"
RC_UW="$REPO/Systematic_Studies/physics_campaign/corrected/unweighted/rc/corrected.root"
RC_SP="$REPO/Systematic_Studies/physics_campaign/corrected/spline/rc/corrected.root"
BC_DIR="$REPO/BC_Corrections"
LOG="$ALT/queue.log"
mkdir -p "$ALT/logs"
: > "$LOG"

log() { print -r -- "$*" >> "$LOG" }
fail() { log "FAILED: $*"; print -r -- "FAILED: $*"; exit 1 }

free_mb() {
  local pages
  pages=$(vm_stat | awk '/Pages free/ {gsub(/\./, "", $3); print $3}')
  print $(( pages * 16384 / 1048576 ))
}
swapouts() {
  memory_pressure 2>/dev/null | awk '/Swapouts/ {print $2}'
}
BASE_SWAP=$(swapouts)
log "start free_mb=$(free_mb) swapouts=$BASE_SWAP"

export PYTHONPATH="$ROO${PYTHONPATH:+:$PYTHONPATH}"
export LD_LIBRARY_PATH="$ROO${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export DYLD_LIBRARY_PATH="$ROO${DYLD_LIBRARY_PATH:+:$DYLD_LIBRARY_PATH}"

write_hist() {
  local label="$1"
  shift
  local stamp="$ALT/logs/write_${label// /_}.out"
  log "WRITE $label"
  "$PY" "$APPLY" "$@" > "$stamp" 2>&1
  local code=$?
  cat "$stamp" >> "$LOG"
  if (( code != 0 )); then
    fail "write $label exited $code"
  fi
  if ! grep -q "histograms 452 problems 0" "$stamp"; then
    fail "write $label did not report 452 histograms"
  fi
  log "WRITE_OK $label"
}

typeset -a QUEUE PIDS NAMES
QUEUE=(
  "rc|unweighted|sf0|RC_Bayesian"
  "rc|unweighted|sf2|RC_Bayesian"
  "rc|spline|sf0|RC_Bayesian"
  "rc|spline|sf2|RC_Bayesian"
)
for spec in q2_3 q2_5 q2_7 y_3 y_5 y_7 z_3 z_5 z_7 pt_3 pt_5 pt_7 phi_5 phi_7 phi_9; do
  QUEUE+=("sub|unweighted|$spec|BC_RC_Bayesian")
done
QUEUE+=("bcs|unweighted|spline|BC_RC_Bayesian")
QUEUE+=("bcs|spline|spline|BC_RC_Bayesian")
PIDS=()
NAMES=()
NEXT=1
STARTED=0

prepare_job() {
  local kind="$1" camp="$2" tag="$3"
  local dest="$ALT/$camp/${kind}_${tag}/histograms.root"
  local input sf json
  if [[ -f "$dest" ]]; then
    log "KEEP $dest"
    return 0
  fi
  case "$kind" in
    rc)
      sf=${tag#sf}
      if [[ "$camp" == "unweighted" ]]; then input="$UW"; else input="$SP"; fi
      write_hist "$kind $camp $tag" -st fixed_rc -c "$camp" -i "$input" -o "$dest" --cache_dir "$CACHE" -s "$sf"
      ;;
    sub)
      json="$BC_DIR/Sub_Bin_Contents_for_BC_Correction_with_Binned_sbatch_from_10_26_2026_sens_${tag}.json"
      write_hist "$kind $camp $tag" -st subdivision_bc -c "$camp" -i "$RC_UW" -o "$dest" --bc_json "$json"
      ;;
    bcs)
      if [[ "$camp" == "unweighted" ]]; then input="$RC_UW"; else input="$RC_SP"; fi
      write_hist "$kind $camp $tag" -st fixed_bc -c "$camp" -i "$input" -o "$dest" --cache_dir "$CACHE"
      ;;
    *)
      fail "unknown kind $kind"
      ;;
  esac
}

start_fit() {
  local kind="$1" camp="$2" tag="$3" family="$4"
  local dir="$ALT/$camp/${kind}_${tag}"
  local root="$dir/histograms.root"
  local json="$dir/fit.json"
  local flog="$ALT/logs/${camp}_${kind}_${tag}.log"
  if [[ -f "$json" ]]; then
    log "FIT_SKIP $camp $kind $tag"
    return 2
  fi
  log "FIT_START $camp $kind $tag free_mb=$(free_mb)"
  (
    cd "$REPO" || exit 1
    "$PY" "$FIT" \
      --root "$root" \
      --Use_TTree --fit --remake_fit --smear --save_json \
      --json_name "$json" \
      --fit_error_source histogram \
      --unfolding_3D \
      --fit_corrections "$family"
  ) >> "$flog" 2>&1 &
  PIDS+=($!)
  NAMES+=("$camp $kind $tag")
  STARTED=$(( STARTED + 1 ))
  log "FIT_PID $! $camp $kind $tag running=${#PIDS}"
}

reap() {
  local i pid name code
  local -a keep_p keep_n
  keep_p=()
  keep_n=()
  if (( ${#PIDS} == 0 )); then
    return 0
  fi
  for i in {1..${#PIDS}}; do
    pid=$PIDS[$i]
    name=$NAMES[$i]
    if kill -0 "$pid" 2>/dev/null; then
      keep_p+=("$pid")
      keep_n+=("$name")
    else
      wait "$pid"
      code=$?
      log "FIT_EXIT $name code=$code"
      if (( code != 0 )); then
        fail "fit $name exited $code"
      fi
    fi
  done
  PIDS=($keep_p)
  NAMES=($keep_n)
}

memory_allows_another() {
  local now_swap
  now_swap=$(swapouts)
  if (( $(free_mb) < 700 )); then
    return 1
  fi
  if (( now_swap > BASE_SWAP )); then
    return 1
  fi
  return 0
}

while (( NEXT <= ${#QUEUE} || ${#PIDS} > 0 )); do
  reap
  if (( NEXT <= ${#QUEUE} )); then
    if (( ${#PIDS} == 0 )) || { (( ${#PIDS} < 2 )) && memory_allows_another; }; then
      item=$QUEUE[$NEXT]
      NEXT=$(( NEXT + 1 ))
      kind=${item%%|*}
      rest=${item#*|}
      camp=${rest%%|*}
      rest=${rest#*|}
      tag=${rest%%|*}
      family=${rest#*|}
      prepare_job "$kind" "$camp" "$tag"
      start_fit "$kind" "$camp" "$tag" "$family"
    fi
  fi
  if (( ${#PIDS} > 0 )); then
    sleep 20
  fi
done

log "QUEUE_DONE"
print -r -- "QUEUE_DONE"
