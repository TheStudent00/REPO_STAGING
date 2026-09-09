#!/usr/bin/env bash
# trickle_down.sh -- stop the CPU-capped copy.
#
# WHAT IT REMOVES
#   the container `trickle-runner` and the network `trickle-internal`.
#
# WHAT IT LEAVES ON DISK, DELIBERATELY
#   ~/Programming/AirlockTrickle/agent/{drop,out,logs,status} -- the lane
#   scripts and their raw products; and everything the trickle banked in
#   Research/op_pipeline (trickle_state.json, trickle_store/, trickle_raw/,
#   trickle_lanes/). The resume state is the point: a stopped trickle
#   picks up at the first chunk not marked done.
#
#   NOTHING owned by Airlock or SandboxDesign is touched. The shared image
#   and the shared `sandbox-persist` volume are left exactly as they were;
#   this copy only ever mounted the volume read-only.
#
# usage:  bash trickle_down.sh          stop and remove
#         bash trickle_down.sh --pause  stop only, keep the container
set -euo pipefail

CONTAINER="trickle-runner"
NETWORK="trickle-internal"

if [ "${1:-}" = "--pause" ]; then
    podman stop "$CONTAINER" >/dev/null 2>&1 || true
    echo "  $CONTAINER stopped (kept; 'bash trickle_up.sh' starts it again)"
    exit 0
fi

podman rm -f "$CONTAINER" >/dev/null 2>&1 || true
echo "  $CONTAINER removed"
podman network rm "$NETWORK" >/dev/null 2>&1 || true
echo "  $NETWORK removed"
echo
echo "  left on disk (resume state):"
echo "    ~/Programming/AirlockTrickle/agent"
echo "    Research/op_pipeline/trickle_state.json"
echo "    Research/op_pipeline/trickle_store/  trickle_raw/  trickle_lanes/"
echo
echo "  Airlock's own containers, untouched:"
podman ps -a --filter "name=sandbox-" --format '    {{.Names}}  {{.Status}}'
