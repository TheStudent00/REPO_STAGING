#!/usr/bin/env bash
# t72 lane 0 — the PATH CHECK. Read-only. Proves which side of the
# container wall this runs on, and whether /persist/gosrc still exists on
# the DEFAULT instance's sandbox-persist volume.
set -u
echo "=== which side of the wall ==="
echo "hostname: $(cat /etc/hostname 2>/dev/null)"
echo "uname:    $(uname -a)"
echo "-- a host-only path must NOT exist in here:"
# a glob, so no user name is ever written into a tracked artifact
ls -d /home/*/Programming 2>&1 || echo "  ABSENT (as expected inside the container)"
echo "-- container-only paths that must exist:"
for p in /persist /sources PseudoCoupHQ /work /out ; do
  printf '  %-28s ' "$p"; ls -d "$p" >/dev/null 2>&1 && echo present || echo ABSENT
done
echo
echo "=== /persist/gosrc ==="
ls -d /persist/gosrc 2>&1 && echo "PRESENT" || echo "ABSENT"
echo "-- VERSION file:"; cat /persist/gosrc/VERSION 2>&1
echo "-- go binary version, QUOTED from the toolchain:"
/persist/gosrc/bin/go version 2>&1
echo "-- instrumented binaries left by the August lap:"
ls -la /persist/compile_diary /persist/compile_diary2 /persist/compile_cov 2>&1
echo "-- goversion.go:"; grep -n 'Version =' /persist/gosrc/src/internal/goversion/goversion.go 2>&1
echo "-- du:"; du -sh /persist/gosrc /persist/gocache 2>&1
echo
echo "=== the read-only source tree the rebuild would come from ==="
ls -d /sources/golang_src 2>&1
grep -n 'Version =' /sources/golang_src/src/internal/goversion/goversion.go 2>&1
echo "DONE t72_l0"
