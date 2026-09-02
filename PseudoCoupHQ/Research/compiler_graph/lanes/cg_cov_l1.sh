#!/usr/bin/env bash
# cg_cov_l1 — build a coverage-instrumented Go compiler (cmd/compile).
# Approach 1: go build -cover with the installed toolchain against the
# vendored tree. Fallback: make.bash the whole tree, then approach 1
# with that toolchain.
set -u
OUT=/out/cg_cov_l1.txt
exec > >(tee "$OUT") 2>&1
say(){ echo "=== $* ==="; }

say recon
date -u +%Y-%m-%dT%H:%M:%SZ
go version
which go; echo "GOROOT=$(go env GOROOT)"
echo "--- tree marker files"
ls /sources/golang_src/VERSION 2>&1 || echo "NO VERSION FILE in tree"
tail -3 /sources/golang_src/src/internal/goversion/goversion.go
df -h /work /persist | sed -n '1,5p'

export GOTOOLCHAIN=local
export GOPROXY=off
export GOFLAGS=-mod=mod
export GOCACHE=/persist/gocache
mkdir -p /persist/gocache

SRC=/persist/gosrc
if [ ! -d "$SRC/src/cmd/compile" ]; then
  say "copying tree to $SRC"
  rm -rf "$SRC"; mkdir -p "$SRC"
  cp -a /sources/golang_src/. "$SRC"/
  rm -rf "$SRC/.git"
fi
du -sh "$SRC"

say "approach 1: go build -cover cmd/compile from $SRC/src/cmd"
cd "$SRC/src/cmd" || exit 90
set -x
go build -cover -o /persist/compile_cov ./compile
A1=$?
set +x
echo "approach1_exit=$A1"

if [ $A1 -ne 0 ]; then
  say "approach 1 FAILED -> approach 2: make.bash"
  export GOROOT_BOOTSTRAP="$(go env GOROOT)"
  echo "GOROOT_BOOTSTRAP=$GOROOT_BOOTSTRAP"
  cd "$SRC/src" || exit 91
  # keep it lean: no tests, no race
  env GOROOT_BOOTSTRAP="$GOROOT_BOOTSTRAP" GOCACHE=/persist/gocache \
      bash make.bash 2>&1 | tail -40
  M=${PIPESTATUS[0]}
  echo "make_bash_exit=$M"
  [ $M -ne 0 ] && { echo FATAL_MAKE_BASH; df -h /work /persist; exit 92; }
  export GOROOT="$SRC"
  export PATH="$SRC/bin:$PATH"
  say "built toolchain version"
  "$SRC/bin/go" version
  cd "$SRC/src/cmd" || exit 93
  set -x
  "$SRC/bin/go" build -cover -o /persist/compile_cov ./compile
  A2=$?
  set +x
  echo "approach2_build_cover_exit=$A2"
  [ $A2 -ne 0 ] && exit 94
  echo "USED_TOOLCHAIN=$SRC/bin/go" > /persist/cov_toolchain.env
else
  echo "USED_TOOLCHAIN=$(command -v go)" > /persist/cov_toolchain.env
fi

say result
ls -l /persist/compile_cov
cat /persist/cov_toolchain.env
say disk
du -sh /persist/* 2>/dev/null
df -h /work /persist | sed -n '1,5p'
echo DONE_OK
