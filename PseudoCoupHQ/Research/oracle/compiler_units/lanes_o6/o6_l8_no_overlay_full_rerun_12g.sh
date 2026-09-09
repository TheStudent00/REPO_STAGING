#!/usr/bin/env bash
# task o6 lane 8 (resume): the FLAG RE-RUN. The first run's full pass with
# GOROOT at the source tree and NO overlay aborted by name
# (ABORT_MEMORY_O6: peak RSS 6114.7 MB > 3072 MB bound, lane
# o6_l2_generated_files_and_no_overlay_full.sh, 1722 s). Standing rule: a
# limit hit is a flag -- re-run with more room (bound now 12 GB, container
# 14g) and report whether the answer changed. Same command as before,
# shape=tree, output to /work (scratch). If it completes, its site lines
# are compared to the deliverable's; if it aborts again, that is the
# answer.
set -uo pipefail
mkdir -p /work/o6/scratch
echo "[1/2] full pass, GOROOT = source tree, NO overlay, shape=tree, bound 12 GB"
ls -l /work/o6/oracle
GO111MODULE=off /work/o6/oracle -shape tree -root /sources/golang_src/src/cmd/compile -goroot /sources/golang_src \
  -scratch /work/o6/scratch -out /work/o6/sites_no_overlay.json.gz ; echo "oracle exit: $?"
echo "[2/2] if it completed: summary by cause and bin, and the site-line comparison to the deliverable"
if [ -s /work/o6/sites_no_overlay.json.gz ]; then
python3 - <<'PY'
import gzip, json, collections, hashlib
def stream(path):
    section = None
    with gzip.open(path, 'rt') as f:
        for line in f:
            line = line.rstrip('\n')
            if line.startswith('"meta": '): yield 'meta', json.loads(line[8:].rstrip(','))
            elif line in ('"packages": [', '"files": [', '"sites": ['): section = line[1:line.index('"', 1)]
            elif line in ('],', ']', '{', '}'): continue
            elif section: yield section, json.loads(line.rstrip(','))
causes = collections.Counter(); bins = collections.Counter(); binpk = collections.Counter(); failing = 0; buildcfg = 0
sites = {}
for sec, r in stream('/work/o6/sites_no_overlay.json.gz'):
    if sec == 'meta':
        print('meta: packages=%d files=%d sites=%d sites_all_operands_typed=%d elapsed_s=%s peak_rss_mb=%.1f' % (r['packages'], r['files'], r['sites'], r['sites_all_operands_typed'], r['elapsed_s'], r['peak_rss_mb']))
    elif sec == 'packages':
        for c, n in r['error_causes'].items(): causes[c] += n
        bins[r['bin']] += r['sites']; binpk[r['bin']] += 1
        if r['errors']: failing += 1
        if any('defaultGOARCH' in s for s in (r['error_samples'] or [])): buildcfg += 1
    elif sec == 'sites':
        k = (r['file'], r['line'], r['col'], r['end_line'], r['end_col'], r['kind'], r['operator'], tuple(o['spelling'] for o in r['operands']), r['result'])
        h = hashlib.sha1(repr(k).encode()).hexdigest(); sites[h] = sites.get(h, 0) + 1
print('packages with errors: %d' % failing)
for c, n in causes.most_common(): print('  cause: %s: %d' % (c, n))
for b, n in binpk.most_common(): print('  bin: %s: packages=%d sites=%d' % (b, n, bins[b]))
print('packages whose first messages name defaultGOARCH (the missing generated file): %d' % buildcfg)
ref = {}
for sec, r in stream('/projects/PseudoCoupHQ/Research/oracle/compiler_units/go_types_sites.json.gz'):
    if sec == 'sites':
        k = (r['file'], r['line'], r['col'], r['end_line'], r['end_col'], r['kind'], r['operator'], tuple(o['spelling'] for o in r['operands']), r['result'])
        h = hashlib.sha1(repr(k).encode()).hexdigest(); ref[h] = ref.get(h, 0) + 1
same = sum(min(sites.get(h, 0), ref.get(h, 0)) for h in ref)
print('site lines identical to the deliverable (position+kind+label+operand spellings+result): %d of %d no-overlay sites; deliverable has %d' % (same, sum(sites.values()), sum(ref.values())))
PY
else
  echo "no output: the pass did not complete (see the oracle exit and any ABORT line above)"
fi
echo "[2/2] done"
