#!/usr/bin/env bash
# task o6 lane 2: (a) which generated z*.go files the image's GOROOT has
# that the checked-in source tree lacks (the cause lane 1 measured), and
# what internal/buildcfg/cfg.go references; (b) the FULL pass with GOROOT
# at the source tree and NO overlay -- the brief's own first measurement,
# so the obstacle is on record with numbers. Output to /work (scratch).
set -uo pipefail
export GOTOOLCHAIN=local GOPROXY=off GOFLAGS=-mod=mod GO111MODULE=on
export GOCACHE=/work/o6/gocache GOPATH=/work/o6/gopath HOME=/work/o6/home
mkdir -p /work/o6/mod /work/o6/gocache /work/o6/gopath /work/o6/home
echo "[1/4] generated files: in image GOROOT but not in the source tree (z*.go under src/, excluding testdata)"
cd /usr/lib/go-1.26/src
find . -name 'z*.go' -not -path '*/testdata/*' | sort | while read -r f; do
  if [ ! -e "/sources/golang_src/src/$f" ]; then echo "  missing in source tree: $f"; fi
done
echo "  --- identifiers cfg.go:24 uses ---"
sed -n 20,30p /sources/golang_src/src/internal/buildcfg/cfg.go
echo "  --- image's zbootstrap.go ---"
cat /usr/lib/go-1.26/src/internal/buildcfg/zbootstrap.go
echo "[2/4] gofmt the artifact in place, then build"
gofmt -w PseudoCoupHQ/Research/oracle/compiler_units/go_types_oracle.go
cp PseudoCoupHQ/Research/oracle/compiler_units/go_types_oracle.go /work/o6/mod/main.go
cd /work/o6/mod
printf 'module o6\n\ngo 1.26\n' > go.mod
go build -o /work/o6/oracle . ; echo "build exit: $?"
echo "[3/4] full pass, GOROOT = source tree, NO overlay (scratch output)"
GO111MODULE=off /work/o6/oracle -root /sources/golang_src/src/cmd/compile -goroot /sources/golang_src \
  -out /work/o6/sites_no_overlay.json ; echo "oracle exit: $?"
echo "[4/4] summary of the no-overlay pass, by error cause and by bin"
python3 - <<'PY'
import json, collections
d = json.load(open('/work/o6/sites_no_overlay.json'))
m = d['meta']
print('meta: packages=%d files=%d sites=%d sites_all_operands_typed=%d elapsed_s=%s peak_rss_mb=%.1f' % (m['packages'], m['files'], m['sites'], m['sites_all_operands_typed'], m['elapsed_s'], m['peak_rss_mb']))
causes = collections.Counter(); bins = collections.Counter(); binpk = collections.Counter(); failing = 0
for p in d['packages']:
    for c, n in p['error_causes'].items(): causes[c] += n
    bins[p['bin']] += p['sites']; binpk[p['bin']] += 1
    if p['errors']: failing += 1
print('packages with errors: %d of %d' % (failing, len(d['packages'])))
for c, n in causes.most_common(): print('  cause: %s: %d' % (c, n))
for b, n in binpk.most_common(): print('  bin: %s: packages=%d sites=%d' % (b, n, bins[b]))
buildcfg = sum(1 for p in d['packages'] if any('defaultGOARCH' in s for s in p['error_samples']))
print('packages whose first messages name defaultGOARCH (the missing generated file): %d' % buildcfg)
PY
echo "[4/4] done"
