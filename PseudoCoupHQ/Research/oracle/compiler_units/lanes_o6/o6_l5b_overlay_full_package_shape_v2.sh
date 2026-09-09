#!/usr/bin/env bash
# task o6 lane 5b (resume, second build): the same full pass in shape=package (a fresh
# FileSet + importer per package check, GC + FreeOSMemory after each), so
# the peak RSS is one package's closure and the wall clock is the price of
# re-importing every closure. Sites go to /work (scratch); the cost record
# (meta + per-package rows, no sites) is kept in the artifact folder as
# go_types_package_shape_cost.json; the site sets of both shapes are
# compared here, line by line, never as whole documents.
set -uo pipefail
export GOTOOLCHAIN=local GOPROXY=off GOFLAGS=-mod=mod GO111MODULE=on
export GOCACHE=/work/o6/gocache GOPATH=/work/o6/gopath HOME=/work/o6/home
mkdir -p /work/o6/mod /work/o6/gocache /work/o6/gopath /work/o6/home /work/o6/scratch
OVERLAY=/sources/golang_src/src/internal/buildcfg/zbootstrap.go=/usr/lib/go-1.26/src/internal/buildcfg/zbootstrap.go
TREE=/projects/PseudoCoupHQ/Research/oracle/compiler_units/go_types_sites.json.gz
PKG=/work/o6/sites_package_shape.json.gz
COST=/projects/PseudoCoupHQ/Research/oracle/compiler_units/go_types_package_shape_cost.json
echo "[1/3] full pass, shape=package, overlay on, GOROOT = source tree (binary from lane 4b)"
ls -l /work/o6/oracle
GO111MODULE=off /work/o6/oracle -shape package -root /sources/golang_src/src/cmd/compile -goroot /sources/golang_src \
  -overlay "$OVERLAY" -scratch /work/o6/scratch -out "$PKG" ; echo "oracle exit: $?"
echo "[2/3] cost record to the artifact folder (meta + packages, no sites)"
python3 - "$PKG" "$COST" <<'PY'
import gzip, json, sys
src, dst = sys.argv[1], sys.argv[2]
meta = None; packages = []
with gzip.open(src, 'rt') as f:
    section = None
    for line in f:
        line = line.rstrip('\n')
        if line.startswith('"meta": '):
            meta = json.loads(line[len('"meta": '):].rstrip(','))
        elif line == '"packages": [':
            section = 'packages'
        elif line in ('],', '"files": [', '"sites": ['):
            if section == 'packages': break
        elif section == 'packages':
            packages.append(json.loads(line.rstrip(',')))
json.dump({'meta': meta, 'packages': packages}, open(dst, 'w'), indent=1)
print('wrote', dst, 'packages', len(packages), 'peak_rss_mb %.1f elapsed_s %s' % (meta['peak_rss_mb'], meta['elapsed_s']))
print('slowest 5 package checks (wall s, maxrss MB after):')
for p in sorted(packages, key=lambda p: -p['wall_s'])[:5]:
    print('  %s %s wall=%.1f maxrss_after=%.0f sites=%d errors=%d' % (p['import_path'], p['bin'], p['wall_s'], p['maxrss_mb_after'], p['sites'], p['errors']))
PY
echo "[3/3] do both shapes type the same sites? (streamed: one hash per site line, position+kind+label+operand spellings+result)"
python3 - "$TREE" "$PKG" <<'PY'
import gzip, json, sys, hashlib
def sites(path):
    out = {}
    with gzip.open(path, 'rt') as f:
        insites = False
        for line in f:
            line = line.rstrip('\n')
            if line == '"sites": [':
                insites = True; continue
            if not insites: continue
            if line in (']', '}'): break
            s = json.loads(line.rstrip(','))
            k = (s['file'], s['line'], s['col'], s['end_line'], s['end_col'], s['kind'], s['operator'], tuple(o['spelling'] for o in s['operands']), s['result'], s['func'], s['package'], s['file_bin'])
            h = hashlib.sha1(repr(k).encode()).hexdigest()
            out[h] = out.get(h, 0) + 1
    return out
a = sites(sys.argv[1]); b = sites(sys.argv[2])
na = sum(a.values()); nb = sum(b.values())
only_a = sum(n for h, n in a.items() if h not in b); only_b = sum(n for h, n in b.items() if h not in a)
diff = sum(abs(a.get(h, 0) - b.get(h, 0)) for h in set(a) | set(b))
print('tree sites=%d package sites=%d | in tree only=%d | in package only=%d | multiset difference=%d | identical=%s' % (na, nb, only_a, only_b, diff, diff == 0))
PY
echo "[3/3] done"
