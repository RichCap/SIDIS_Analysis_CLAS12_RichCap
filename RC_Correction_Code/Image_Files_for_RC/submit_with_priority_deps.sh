#!/usr/bin/env bash
set -euo pipefail

# --- Define groups ---
HIGH=(
  sbatch_Scan_RC_M_Mods.sh
  sbatch_Scan_Born_M_Mods.sh
)

MEDIUM=(
  sbatch_Scan_RC_EvGen.sh
  sbatch_Scan_RC_No_Mods.sh
)

LOW=(
  sbatch_Scan_Born_EvGen.sh
  sbatch_Scan_Born_No_Mods.sh
)

LOWEST=(
  sbatch_Scan_TCS_M_Mods.sh
  sbatch_Scan_TCS_EvGen.sh
  sbatch_Scan_TCS_No_Mods.sh
)

# --- Helpers ---
join_by_colon() {
  local IFS=":"
  echo "$*"
}

submit_group() {
  local dep="$1"; shift
  local -a scripts=("$@")
  local -a ids=()

  for s in "${scripts[@]}"; do
    local jid
    if [[ -n "$dep" ]]; then
      jid=$(sbatch --parsable --dependency="$dep" "$s")
      echo "Submitted $s -> $jid (dep: $dep)" >&2
    else
      jid=$(sbatch --parsable "$s")
      echo "Submitted $s -> $jid" >&2
    fi
    ids+=("$jid")
  done

  # IMPORTANT: stdout is ONLY the numeric IDs
  echo "${ids[@]}"
}

# --- Submit HIGH (no dependencies) ---
read -r -a HIGH_IDS <<< "$(submit_group "" "${HIGH[@]}")"

# MEDIUM: after HIGH has STARTED
HIGH_AFTER="after:$(join_by_colon "${HIGH_IDS[@]}")"
read -r -a MEDIUM_IDS <<< "$(submit_group "$HIGH_AFTER" "${MEDIUM[@]}")"

# LOW: after HIGH has FINISHED (any exit) AND after MEDIUM has STARTED
HIGH_DONE="afterany:$(join_by_colon "${HIGH_IDS[@]}")"
MEDIUM_AFTER="after:$(join_by_colon "${MEDIUM_IDS[@]}")"
LOW_DEP="${HIGH_DONE},${MEDIUM_AFTER}"
read -r -a LOW_IDS <<< "$(submit_group "$LOW_DEP" "${LOW[@]}")"

# LOWEST: after HIGH+MEDIUM have FINISHED (any exit) AND after LOW has STARTED
HIGH_MEDIUM_DONE="afterany:$(join_by_colon "${HIGH_IDS[@]}" "${MEDIUM_IDS[@]}")"
LOW_AFTER="after:$(join_by_colon "${LOW_IDS[@]}")"
LOWEST_DEP="${HIGH_MEDIUM_DONE},${LOW_AFTER}"
read -r -a LOWEST_IDS <<< "$(submit_group "$LOWEST_DEP" "${LOWEST[@]}")"

# --- Summary (to stderr so it won't pollute stdout if you ever capture it) ---
{
  echo
  echo "Summary:"
  echo "  HIGH:    ${HIGH_IDS[*]}"
  echo "  MEDIUM:  ${MEDIUM_IDS[*]}"
  echo "  LOW:     ${LOW_IDS[*]}"
  echo "  LOWEST:  ${LOWEST_IDS[*]}"
} >&2
