#!/usr/bin/env bash
# rv1 lane 20 -- the law's count over every file this task added, at the end,
# so the log's flag 6 states the final numbers and not an earlier pass's.
set -u
RV=PseudoCoupHQ/Research/oracle/riscv
total=1
echo "[1/$total] the count, every file, nonzero rows named"
for f in $RV/*.py $RV/*.json $RV/*.md $RV/lanes_rv1/*.sh; do
  n=$(grep -c exempt "$f")
  if [ "$n" != "0" ]; then printf 'NONZERO %s  %s\n' "$n" "$(basename "$f")"; fi
done
echo "--- totals"
python3 - <<'PY'
import glob, os
root = "PseudoCoupHQ/Research/oracle/riscv"
deliverable = 0
lanes = 0
for path in sorted(glob.glob(root + "/*.py") + glob.glob(root + "/*.json")
                   + glob.glob(root + "/*.md")):
    if "exempt" in open(path).read():
        deliverable = deliverable + 1
for path in sorted(glob.glob(root + "/lanes_rv1/*.sh")):
    if "exempt" in open(path).read():
        lanes = lanes + 1
print("deliverable files containing the word: %d" % deliverable)
print("lane scripts containing the word: %d" % lanes)
import resource
print('peak RSS: %.1f MB'
      % (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0))
PY
echo "--- lane finished"
