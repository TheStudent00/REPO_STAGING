#!/usr/bin/env bash
# t72 lane 1 — build the go toolchain into THIS instance's own /persist,
# from the read-only /sources/golang_src, by coverage_meta.md's recipe.
set -euo pipefail
T0=$(date +%s)
echo "[1/5] path check"
echo "hostname: $(cat /etc/hostname)"; ls -d /persist /sources || true
df -h /persist | tail -1

SRC=/persist/gosrc
if [ -x "$SRC/bin/go" ]; then
  echo "[2/5] toolchain already built in this instance:"
  "$SRC/bin/go" version
  echo "SKIP build"
else
  echo "[2/5] copy /sources/golang_src -> $SRC"
  mkdir -p "$SRC"
  cp -a /sources/golang_src/. "$SRC"/
  rm -rf "$SRC/.git"
  printf 'go1.28-devel-pseudocoup\ntime 2026-07-15T22:11:42Z\n' > "$SRC/VERSION"
  echo "  copied in $(( $(date +%s) - T0 ))s"
  echo "[3/5] make.bash"
  T1=$(date +%s)
  export GOTOOLCHAIN=local GOPROXY=off GOFLAGS=-mod=mod
  export GOCACHE=/persist/gocache
  cd "$SRC/src"
  GOROOT_BOOTSTRAP=/usr/lib/go-1.26 bash make.bash > /persist/make_t72.log 2>&1 || {
      echo "MAKE FAILED — tail:"; tail -40 /persist/make_t72.log; exit 3; }
  echo "  make.bash: $(( $(date +%s) - T1 ))s"
fi

echo "[4/5] the pin, QUOTED from the toolchain"
export GOROOT="$SRC" PATH="$SRC/bin:$PATH"
"$SRC/bin/go" version
echo "[5/5] disk"
du -sh /persist/gosrc /persist/gocache 2>/dev/null
df -h /persist | tail -1
echo "TOTAL_SECONDS=$(( $(date +%s) - T0 ))"
echo "DONE t72_l1"
