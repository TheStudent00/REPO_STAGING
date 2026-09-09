#!/usr/bin/env bash
# t81 lane 4 — THE SAMPLE, before any full pass. 20 c probes and 20 cpp
# probes through the instrumented clang, so the per-probe cost, the
# diary size and the peak resident size of the replay driver are
# MEASURED and not estimated. The memory gate of round 15 (log_183,
# "ADDED THIS ROUND") requires exactly this before the 1,380-probe pass.
#
# It also settles a fact the go lap did not have to face: clang's driver
# forks a `-cc1` process, so the hook writes `<COMPILER_DIARY>.<pid>`.
# This lane prints how many pid files each compile produced.
set -u
say() { echo; echo "======== $* ========"; }
REPO=PseudoCoupHQ/Research/compiler_graph
CLANG=/persist/llvmbuild/bin/clang
CLANGXX=/persist/llvmbuild/bin/clang++
mkdir -p /work/probe /work/sample

say "[1/3] the binary under test"
"$CLANG" --version 2>&1 | head -2
echo "   the SHIP tool line, from op_pipeline/trickle_lanes/regen_c_c0023.sh:"
echo "     CLANG   -std=c17   -O1 -c unit.c   -o unit_ship.o"
echo "     CLANGXX -std=c++20 -O1 -c unit.cpp -o unit_ship.o"

say "[2/3] 20 c and 20 cpp probes, timed"
python3 - <<'PY'
import json, os, resource, subprocess, time, glob

REPO = 'PseudoCoupHQ/Research/compiler_graph'
CLANG = '/persist/llvmbuild/bin/clang'
CLANGXX = '/persist/llvmbuild/bin/clang++'
probes = json.load(open(os.path.join(REPO, 't81', 'probes_cpp.json')))['probes']

by_language = {'c': [], 'cpp': []}
for unit in sorted(probes):
    by_language[unit.split('/', 1)[0]].append(unit)
print('   corpus: c %d, cpp %d, total %d'
      % (len(by_language['c']), len(by_language['cpp']), len(probes)))

rows = []
for language in ('c', 'cpp'):
    units = by_language[language][:20]
    for index, unit in enumerate(units, 1):
        stem = unit.split('/', 1)[1]
        suffix = 'c' if language == 'c' else 'cpp'
        source_path = '/work/probe/unit.%s' % suffix
        open(source_path, 'w').write(probes[unit]['source'])
        target = '/work/sample/%s__%s.txt' % (language, stem)
        for stale in glob.glob(target + '.*'):
            os.remove(stale)
        tool = CLANG if language == 'c' else CLANGXX
        standard = '-std=c17' if language == 'c' else '-std=c++20'
        command = [tool, standard, '-O1', '-c', source_path,
                   '-o', '/work/probe/unit_ship.o']
        started = time.time()
        result = subprocess.run(command,
                                env=dict(os.environ, COMPILER_DIARY=target),
                                capture_output=True, text=True)
        seconds = time.time() - started
        pid_files = sorted(glob.glob(target + '.*'))
        lines = 0
        size = 0
        for name in pid_files:
            size = size + os.path.getsize(name)
            with open(name, errors='replace') as handle:
                for lines, _ in enumerate(handle, lines + 1):
                    pass
        rows.append({
            'unit': unit, 'seconds': seconds, 'exit': result.returncode,
            'pid_files': len(pid_files), 'lines': lines, 'bytes': size,
            'stderr': (result.stderr or '')[-200:],
        })
        print('   [%d/40] %-10s exit=%d %5.2f s  pid files=%d  '
              'lines=%d  bytes=%d'
              % (len(rows), unit, result.returncode, seconds,
                 len(pid_files), lines, size))

failed = [row for row in rows if row['exit'] != 0]
print('   probes compiled : %d of 40' % (len(rows) - len(failed)))
print('   probes failed   : %d of 40' % len(failed))
for row in failed[:5]:
    print('      %s -> %s' % (row['unit'], row['stderr']))
empty = [row for row in rows if row['lines'] == 0]
print('   probes with an EMPTY diary : %d of 40' % len(empty))
for row in empty[:5]:
    print('      %s' % row['unit'])
counts = sorted({row['pid_files'] for row in rows})
print('   distinct pid-file counts seen : %s' % counts)
seconds = [row['seconds'] for row in rows]
lines = [row['lines'] for row in rows]
size = [row['bytes'] for row in rows]
print('   seconds per probe : min %.2f  max %.2f  mean %.2f'
      % (min(seconds), max(seconds), sum(seconds) / len(seconds)))
print('   diary lines       : min %d  max %d  mean %.0f'
      % (min(lines), max(lines), sum(lines) / len(lines)))
print('   diary bytes       : min %d  max %d  mean %.0f  total %d'
      % (min(size), max(size), sum(size) / len(size), sum(size)))
print('   PROJECTION for 1,380 probes: %.0f s wall, %.1f GB of diaries'
      % (sum(seconds) / len(seconds) * 1380,
         sum(size) / len(size) * 1380 / 1e9))
peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
child = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / 1024.0
print('   PEAK RESIDENT, replay driver : %.1f MB' % peak)
print('   PEAK RESIDENT, largest child (the compiler) : %.1f MB' % child)
json.dump(rows, open(os.path.join(REPO, 't81', 'sample_probe_cost.json'), 'w'),
          indent=1)
PY

say "[3/3] LITERAL, the head and the tail of one sampled diary"
LARGEST=$(ls -S /work/sample/*.txt.* 2>/dev/null | head -1)
echo "   file: $(basename "$LARGEST")"
head -3 "$LARGEST"
echo "   ..."
tail -2 "$LARGEST"
echo "   lines whose field count is not three:"
awk -F'\t' 'NF!=3' "$LARGEST" | wc -l
echo "   distinct subjects in the second column:"
cut -f2 "$LARGEST" | sort -u | head -10
echo "   subject_enter markers:"
grep -c 'subject_enter' "$LARGEST" || true
cp -f "$LARGEST" "$REPO/t81/sample_one.diary"
df -h PseudoCoupHQ | tail -1
echo "DONE t81_l4"
