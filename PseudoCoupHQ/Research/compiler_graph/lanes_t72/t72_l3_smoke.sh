#!/usr/bin/env bash
# t72 lane 3 — smoke ONE probe through the widened diary compiler, with
# $WORK expanded. Measures diary size per compile before 590 are run.
set -euo pipefail
REPO=/projects/PseudoCoupHQ/Research/compiler_graph
rm -rf /work/probe && mkdir -p /work/probe /work/out
cd /work/probe
printf 'module probe\n\ngo 1.28\n' > go.mod
cat > probe.go <<'GO'
package main

//go:noinline
func op_smoke(a int32) int32 {
	return +a
}

var ga int32
var sink interface{}

func main() {
	sink = op_smoke(ga)
	_ = sink
}
GO
python3 - <<'PY'
import os, shlex, subprocess, sys, time
line = open('/persist/probecfg/toolline.raw').read().strip()
parts = shlex.split(line)
parts[0] = '/persist/compile_diary_all'
for i, p in enumerate(parts):
    if p == '-o':
        parts[i + 1] = '/work/out/_pkg_.a'
    if p.startswith('$WORK') or '$WORK' in p:
        if p.endswith('importcfg'):
            parts[i] = '/persist/probecfg/importcfg'
        else:
            parts[i] = p.replace('$WORK', '/work/w')
print('ARGV:', ' '.join(parts))
open('/persist/probecfg/toolline.parts', 'w').write('\n'.join(parts))
env = dict(os.environ, COMPILER_DIARY='/work/smoke.diary')
t = time.time()
r = subprocess.run(parts, env=env, cwd='/work/probe',
                   capture_output=True, text=True)
print('exit', r.returncode, 'seconds %.2f' % (time.time() - t))
if r.returncode != 0:
    print(r.stdout[-2000:]); print(r.stderr[-2000:]); sys.exit(4)
PY
echo "diary bytes : $(stat -c %s /work/smoke.diary)"
echo "diary lines : $(wc -l < /work/smoke.diary)"
echo "distinct ids: $(cut -f3 /work/smoke.diary | sort -u | wc -l)"
echo "gzip bytes  : $(gzip -c /work/smoke.diary | wc -c)"
echo "--- first 15 lines, LITERAL ---"
head -15 /work/smoke.diary
echo "--- subject spread ---"
cut -f2 /work/smoke.diary | sort | uniq -c | sort -rn | head
cp /work/smoke.diary "$REPO/t72/smoke.diary"
echo "DONE t72_l3"
