#!/bin/bash
# run_all_languages.sh -- submit every cartesian probe lane for the
# remaining eight languages, in the one order that is safe, without an
# agent.  Written 2026-08-22, log_062.
#
# WHAT IT DOES NOT DO: it never starts, stops or restarts podman, and it
# never runs a probe itself.  It writes lane files into Airlock's drop
# folder through the validating CLI and then WATCHES status files.  The
# container must already be up -- see RUN_ALL_LANGUAGES.md step 1.
#
# ORDER IS A DEPENDENCY, NOT A PREFERENCE.  A level-2 cell for a
# statically checked language exists only where `op(y, y)` typechecks,
# and `y`'s type is read out of that language's level-1 lane output.  So
# phase 2 cannot even be GENERATED until phase 1 has produced answers.
# That is also why every level-1 lane comes first: a partial run is still
# a whole level.
#
# Vocabulary: the OS-stopped outcome is ABORT.

set -u

KFZ="$HOME/Programming/PRIVATE/PseudoCoupHQ/Research/kind_fuzz_clustering"
AIR="$HOME/Programming/PUBLIC/Airlock"
LANES="$KFZ/lanes"
BATCH="pygo-emitters-log061"

PHASE1="ct_php_l1.sh ct_typescript_l1.sh ct_java_l1.sh ct_kotlin_l1.sh \
ct_cpp_l1.sh ct_swift_l1.sh ct_dart_l1.sh ct_csharp_l1.sh"

# the weight is the lane's own probe count, taken out of the lane's own
# banner line rather than kept in a second place that can drift.
weight_of () {
  grep -m1 -o -- '-- [0-9]* probes ===' "$1" | tr -cd '0-9'
}

submit () {
  local f="$1"
  local w
  w="$(weight_of "$f")"
  if [ -z "$w" ]; then w=1; fi
  echo "submitting $(basename "$f")  weight $w"
  python3 "$AIR/airlock" submit "$f" --batch "$BATCH" --weight "$w" || {
    echo "!! airlock refused $(basename "$f") -- read the refusal above and stop here."
    exit 1
  }
}

status_of () {
  local n="$1"
  if [ -f "$AIR/agent/status/$n.status" ]; then
    cat "$AIR/agent/status/$n.status"
  else
    echo "state=queued"
  fi
}

wait_for () {
  # block until every named lane has a status file saying it finished.
  # A lane the operating system stopped on the wall-clock ceiling reads
  # as done here too -- `airlock status` renders that outcome ABORT and
  # the runbook says what to do about it.
  local names="$*"
  local left n
  while true; do
    left=""
    for n in $names; do
      case "$(status_of "$n")" in
        *state=done*) ;;
        *) left="$left $n" ;;
      esac
    done
    if [ -z "$left" ]; then
      echo "== all lanes of this phase have finished =="
      return 0
    fi
    echo "[waiting] still running or queued:$left"
    python3 "$AIR/airlock" status 2>/dev/null | sed -n '1,12p'
    sleep 30
  done
}

echo "=== PHASE 1 -- every LEVEL 1 lane, eight languages ==="
date -u +%Y-%m-%dT%H:%M:%SZ
for f in $PHASE1; do submit "$LANES/$f"; done
echo
echo "Phase 1 submitted.  Watch it with:"
echo "    python3 $AIR/airlock watch"
echo "    bash $AIR/progress.sh -w"
echo
wait_for $PHASE1

echo
echo "=== PHASE 2 -- generate the LEVEL 2 lanes from phase 1's answers ==="
date -u +%Y-%m-%dT%H:%M:%SZ
cd "$KFZ" || exit 1
python3 "$KFZ/l3_cart_gen.py" --eight l2 --no-drop || {
  echo "!! the level-2 generator failed.  Nothing was submitted."
  exit 1
}

echo
echo "=== PHASE 2 -- submit every LEVEL 2 lane ==="
PHASE2=""
for f in "$LANES"/ct_php_l2*.sh "$LANES"/ct_typescript_l2*.sh \
         "$LANES"/ct_java_l2*.sh "$LANES"/ct_kotlin_l2*.sh \
         "$LANES"/ct_cpp_l2*.sh "$LANES"/ct_swift_l2*.sh \
         "$LANES"/ct_dart_l2*.sh "$LANES"/ct_csharp_l2*.sh; do
  [ -f "$f" ] || continue
  submit "$f"
  PHASE2="$PHASE2 $(basename "$f")"
done
echo
echo "Phase 2 submitted:$PHASE2"
wait_for $PHASE2

echo
echo "=== EVERYTHING SUBMITTED AND FINISHED ==="
date -u +%Y-%m-%dT%H:%M:%SZ
python3 "$AIR/airlock" status
echo
echo "Raw lane output is in $AIR/agent/out/ .  Nothing here folds it --"
echo "the fold is a separate decision and is not part of this run."
