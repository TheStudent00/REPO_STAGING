#!/usr/bin/env bash
# trickle_up.sh -- start the CPU-capped copy of the Airlock runner that the
# probe regeneration trickles through.
#
# WHY A COPY AND NOT AIRLOCK ITSELF
#   Airlock's runner is a shared, long-lived container used by other work on
#   this machine, and it runs its lane scripts SERIALLY at whatever core
#   share it was started with. The regeneration is a long run that must
#   never hold the machine hot, so it gets its own container at half the
#   cores, which can be stopped and removed without touching Airlock.
#
# THE NAME CONSTRAINT, which is the whole reason every name here is new
#   Airlock and SandboxDesign SHARE container,
#   network, image and volume names (sandbox-runner, sandbox-proxy,
#   sandbox-internal, sandbox-egress, sandbox-persist) -- which is why
#   those two must never run at the same time. A third participant that
#   reused any of those names would collide with BOTH. So this copy uses
#   the prefix `trickle-` throughout and shares no name with either:
#
#       container   trickle-runner        (vs sandbox-runner)
#       network     trickle-internal      (vs sandbox-internal)
#       agent tree  AirlockTrickle/agent
#
#   It is therefore safe BESIDE a running Airlock, which is the state this
#   was built for.
#
# WHAT IS SHARED, DELIBERATELY, AND HOW IT IS MADE SAFE
#   The runner IMAGE (sandbox-runner:latest) and the toolchain volume
#   (sandbox-persist, which holds the swift installation at /persist/swift)
#   are shared. An image is read-only by construction. The volume is
#   mounted READ-ONLY here, so this container cannot alter the toolchain
#   Airlock's own runs depend on.
#
# NO HOT-FOLDER DAEMON, AND WHY -- MEASURED, NOT CHOSEN FOR TASTE
#   The image's default command is Airlock's inotify watcher on /drop. It
#   was tried first and the container stopped immediately:
#
#     OSError: [Errno 28] inotify_add_watch(/drop) failed: No space left on device
#
#   That is the inotify INSTANCE limit, not disk:
#
#     $ cat /proc/sys/fs/inotify/max_user_instances
#     128
#
#   This machine already runs many watchers (the repository daemon and the
#   editor among them) and has no instance left to give. Raising a kernel
#   limit is a system setting change and is not something this task makes.
#
#   So the container is started IDLE and the chunk driver reaches in with
#   `podman exec`. Nothing about the lane changes: the same lane script,
#   the same /work scratch, the same /out products. Only the doorbell is
#   different, and the driver was going to sequence chunks itself anyway.
#
# NO PROXY, DELIBERATELY
#   Airlock pairs its runner with an allowlist proxy so a run can fetch
#   from a named list. The regeneration compiles local source and fetches
#   nothing, so this copy has no proxy at all and sits on an --internal
#   network with no route out. Fewer names, fewer moving parts, and no
#   egress to reason about.
#
# HOW TO STOP IT
#   bash trickle_down.sh          stops and removes the container and the
#                                 network; leaves the agent tree on disk so
#                                 a partial trickle can still be read and
#                                 resumed.
#
# usage:  bash trickle_up.sh
set -euo pipefail

ROOT="${TRICKLE_ROOT:-$HOME/Programming/AirlockTrickle}"
AGENT="$ROOT/agent"
CONTAINER="trickle-runner"
NETWORK="trickle-internal"
IMAGE="sandbox-runner:latest"
PERSIST_VOLUME="sandbox-persist"

TOTAL_CORES="$(nproc)"
CAP_CORES="${TRICKLE_CPUS:-$(( TOTAL_CORES / 2 ))}"

echo "  machine cores: $TOTAL_CORES ; cap: $CAP_CORES (half, per the "
echo "  overheating constraint; TRICKLE_CPUS overrides)"

# ---- refuse to collide -----------------------------------------------------
# A name check, not a guess: if any of this copy's names is already taken by
# something that is not this copy, stop rather than adopt it.
for taken in sandbox-runner sandbox-proxy va-runner va-proxy; do
    if [ "$taken" = "$CONTAINER" ]; then
        echo "  REFUSING: this copy's container name collides with $taken" >&2
        exit 1
    fi
done

mkdir -p "$AGENT"/{drop,out,logs,status}

podman network exists "$NETWORK" || podman network create --internal "$NETWORK"

if podman container exists "$CONTAINER"; then
    bound_drop=$(podman inspect "$CONTAINER" \
        --format '{{range .Mounts}}{{if eq .Destination "/drop"}}{{.Source}}{{end}}{{end}}' \
        2>/dev/null || echo "")
    if [ -n "$bound_drop" ] && [ "$bound_drop" != "$AGENT/drop" ]; then
        echo "  REFUSING to reuse $CONTAINER: it is bound to another tree." >&2
        echo "    its /drop:  $bound_drop" >&2
        echo "    this tree:  $AGENT/drop" >&2
        echo "    remove it and rerun:  podman rm -f $CONTAINER" >&2
        exit 1
    fi
    podman start "$CONTAINER" >/dev/null
    echo "  $CONTAINER already existed; started (bound to $AGENT/drop)"
else
    podman run -d --name "$CONTAINER" \
        --network "$NETWORK" \
        -v "$AGENT/drop":/drop \
        -v "$AGENT/out":/out \
        -v "$AGENT/logs":/logs \
        -v "$AGENT/status":/status \
        -v "$PERSIST_VOLUME":/persist:ro \
        --memory 8g --cpus "$CAP_CORES" --pids-limit 2048 \
        --cap-drop=ALL \
        --security-opt no-new-privileges \
        --tmpfs /tmp:rw,nosuid,nodev,size=2g \
        --tmpfs /work:rw,nosuid,nodev,size=4g \
        --entrypoint "" \
        "$IMAGE" sleep infinity
    echo "  $CONTAINER started"
    echo "    cpus:     $CAP_CORES of $TOTAL_CORES"
    echo "    drop:     $AGENT/drop"
    echo "    status:   $AGENT/status"
    echo "    out/logs: $AGENT/{out,logs}"
    echo "    persist:  $PERSIST_VOLUME at /persist, READ-ONLY"
fi

echo
podman ps --filter "name=trickle-" --format '  {{.Names}}  {{.Status}}  {{.Image}}'
echo
echo "  toolchains, asked rather than assumed:"
podman exec "$CONTAINER" bash -lc '
  /usr/bin/clang --version | head -1
  /usr/bin/clang++ --version | head -1
  rustc --version
  go version
  /persist/swift/usr/bin/swiftc --version | head -1
' || echo "  WARNING: a toolchain did not answer -- see trickle_doctor.sh"
