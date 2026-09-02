#!/usr/bin/env bash
# cg_cov_l2 — approach 2: make.bash the vendored tree into /persist/gosrc,
# then build a coverage-instrumented cmd/compile with THAT toolchain.
set -u
OUT=/out/cg_cov_l2.txt
exec > >(tee "$OUT") 2>&1
say(){ echo "=== $* ==="; }

export GOTOOLCHAIN=local GOPROXY=off GOFLAGS=-mod=mod GOCACHE=/persist/gocache
mkdir -p /persist/gocache
SRC=/persist/gosrc

say "pre-state"
go version; ls -a "$SRC" | tr '\n' ' '; echo

# cmd/dist wants a VERSION file or a VCS; the copy has neither -> supply one.
if [ ! -f "$SRC/VERSION" ]; then
  printf 'go1.28-devel-pseudocoup\ntime 2026-07-15T22:11:42Z\n' > "$SRC/VERSION"
fi
rm -rf "$SRC/.git" "$SRC/.jj"
cat "$SRC/VERSION"

say make.bash
export GOROOT_BOOTSTRAP="$(go env GOROOT)"
cd "$SRC/src" || exit 91
bash make.bash 2>&1 | tail -30
M=${PIPESTATUS[0]}
echo "make_bash_exit=$M"
[ "$M" -ne 0 ] && { df -h /work /persist|sed -n 1,4p; exit 92; }

export GOROOT="$SRC"; export PATH="$SRC/bin:$PATH"
say "built toolchain"
"$SRC/bin/go" version
"$SRC/bin/go" env GOROOT

say "go build -cover cmd/compile"
cd "$SRC/src/cmd" || exit 93
set -x
"$SRC/bin/go" build -cover -o /persist/compile_cov cmd/compile
A=$?
set +x
echo "build_cover_exit=$A"
[ "$A" -ne 0 ] && exit 94
ls -l /persist/compile_cov
echo "USED_TOOLCHAIN=$SRC/bin/go" > /persist/cov_toolchain.env

say disk
du -sh /persist/gosrc /persist/gocache /persist/compile_cov
df -h /work /persist | sed -n 1,4p
echo DONE_OK
