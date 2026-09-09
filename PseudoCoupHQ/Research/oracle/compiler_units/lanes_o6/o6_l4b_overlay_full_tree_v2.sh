#!/usr/bin/env bash
# task o6 lane 4b (resume, second build; after the first join: BinaryExpr/UnaryExpr nodes go/types records as TYPE expressions -- constraint unions, `~T` -- are skipped and counted, and positions are physical, PositionFor(adjusted=false), so a `//line` directive no longer moves a site): the FULL go/types pass over src/cmd/compile/...,
# GOROOT at the source tree, overlay on for internal/buildcfg/zbootstrap.go
# (lane 3 showed the closure types with it), shape=tree (one shared
# importer cache), 12 GB bound. Writes the deliverable
# go_types_sites.json.gz (gzip: lane 4's 106,063 one-line site records
# were 57.3 MB uncompressed and 2.4 MB gzipped; the artifact folder is
# auto-committed to a GitHub repo, so the compressed form is kept).
set -uo pipefail
export GOTOOLCHAIN=local GOPROXY=off GOFLAGS=-mod=mod GO111MODULE=on
export GOCACHE=/work/o6/gocache GOPATH=/work/o6/gopath HOME=/work/o6/home
mkdir -p /work/o6/mod /work/o6/gocache /work/o6/gopath /work/o6/home /work/o6/scratch
OVERLAY=/sources/golang_src/src/internal/buildcfg/zbootstrap.go=/usr/lib/go-1.26/src/internal/buildcfg/zbootstrap.go
OUT=/projects/PseudoCoupHQ/Research/oracle/compiler_units/go_types_sites.json.gz
echo "[1/3] build (the second source: type-expression skip + physical positions)"
cp /projects/PseudoCoupHQ/Research/oracle/compiler_units/go_types_oracle.go /work/o6/mod/main.go
cd /work/o6/mod
printf 'module o6\n\ngo 1.26\n' > go.mod
go build -o /work/o6/oracle . ; echo "build exit: $?"
echo "[2/3] full pass, shape=tree, overlay on, GOROOT = source tree"
GO111MODULE=off /work/o6/oracle -shape tree -root /sources/golang_src/src/cmd/compile -goroot /sources/golang_src \
  -overlay "$OVERLAY" -scratch /work/o6/scratch -out "$OUT" ; echo "oracle exit: $?"
echo "[3/3] output size, meta, error causes by bin"
ls -l "$OUT"
python3 - <<'PY'
import gzip, json, collections
d = json.load(gzip.open('/projects/PseudoCoupHQ/Research/oracle/compiler_units/go_types_sites.json.gz', 'rt'))
m = d['meta']
print('meta:', json.dumps({k: v for k, v in m.items() if k != 'release_tags'}))
causes = collections.Counter(); bins = collections.Counter(); binpk = collections.Counter(); failing = 0
for p in d['packages']:
    for c, n in p['error_causes'].items(): causes[c] += n
    bins[p['bin']] += p['sites']; binpk[p['bin']] += 1
    if p['errors']: failing += 1
print('packages with errors: %d of %d' % (failing, len(d['packages'])))
for c, n in causes.most_common(): print('  cause: %s: %d' % (c, n))
for b, n in binpk.most_common(): print('  bin: %s: packages=%d sites=%d' % (b, n, bins[b]))
print('slowest 5 package checks (wall s, maxrss MB after):')
for p in sorted(d['packages'], key=lambda p: -p['wall_s'])[:5]:
    print('  %s %s wall=%.1f maxrss_after=%.0f sites=%d errors=%d' % (p['import_path'], p['bin'], p['wall_s'], p['maxrss_mb_after'], p['sites'], p['errors']))
PY
echo "[3/3] done"
