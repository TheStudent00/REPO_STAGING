#!/usr/bin/env bash
# trickle_doctor.sh -- what state the CPU-capped copy is in, each finding
# with its remedy. Reads; changes nothing.
#
# usage:  bash trickle_doctor.sh
set -uo pipefail

ROOT="${TRICKLE_ROOT:-$HOME/Programming/AirlockTrickle}"
AGENT="$ROOT/agent"
CONTAINER="trickle-runner"
NETWORK="trickle-internal"

echo "== which side of the container wall this is running on"
if [ -d /work ]; then
    echo "  /work exists -- this is INSIDE a runner container"
else
    echo "  /work absent, hostname $(hostname) -- this is the HOST"
fi

echo
echo "== name collisions (Airlock and SandboxDesign share sandbox-* names)"
for n in sandbox-runner sandbox-proxy va-runner va-proxy; do
    if podman container exists "$n" 2>/dev/null; then
        echo "  $n exists -- and is NOT this copy's name, so no collision"
    fi
done
echo "  this copy uses: $CONTAINER, $NETWORK"

echo
echo "== the container"
if podman container exists "$CONTAINER"; then
    podman ps -a --filter "name=$CONTAINER" \
        --format '  {{.Names}}  {{.Status}}  {{.Image}}'
    cpus=$(podman inspect "$CONTAINER" --format '{{.HostConfig.NanoCpus}}')
    echo "  cpu cap: $((cpus / 1000000000)) of $(nproc) cores"
    podman inspect "$CONTAINER" \
        --format '{{range .Mounts}}  mount {{.Destination}} <- {{.Source}} rw={{.RW}}{{"\n"}}{{end}}'
else
    echo "  ABSENT. remedy:  bash trickle_up.sh"
fi

echo
echo "== toolchains, asked rather than assumed"
if podman ps --filter "name=$CONTAINER" --format '{{.Names}}' | grep -q .; then
    podman exec "$CONTAINER" bash -lc '
      /usr/bin/clang --version | head -1
      rustc --version
      go version
      objdump --version | head -1
      if [ -f /usr/lib/x86_64-linux-gnu/libncursesw.so.6.6 ]; then
        ln -sf /usr/lib/x86_64-linux-gnu/libncursesw.so.6.6 \
           /usr/lib/x86_64-linux-gnu/libncurses.so.6 2>/dev/null
        ldconfig 2>/dev/null
      fi
      /persist/swift/usr/bin/swiftc --version | head -1
    ' 2>&1 | sed 's/^/  /'
else
    echo "  container not running; remedy:  bash trickle_up.sh"
fi

echo
echo "== the trickle's own state"
STATE="$(dirname "$0")/trickle_state.json"
if [ -f "$STATE" ]; then
    /tmp/reconnect_venv/bin/python3 "$(dirname "$0")/trickle.py" --status \
        2>&1 | sed 's/^/  /'
else
    echo "  no plan yet. remedy:  trickle.py --plan"
fi

echo
echo "== disk"
df -Pm "$AGENT" | awk 'NR==2{print "  agent tree free: " $4 " MB"}'
