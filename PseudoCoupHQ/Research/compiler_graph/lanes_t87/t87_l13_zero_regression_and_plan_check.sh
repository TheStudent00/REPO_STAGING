#!/usr/bin/env bash
# t87 lane 13 — ZERO REGRESSIONS, PROVED rather than asserted, and the
# planning tree checked.
#
# `graph.py` is a shared file: task 71 built it, task 75 folded
# coverage.py into it, task 81 edited it, and task 87 added the third
# connection kind to it. So the two methods that were already there are
# run from the PRE-TASK-87 version out of git and from the current one,
# over the same sample, and the outputs are diffed byte for byte.
# Baseline commit e2cba0db (2026-09-04 15:16), task 81's version.
#
# THE SPELLING BAN, ABSOLUTE (the owner, 2026-08-25). Nothing here groups or
# pairs anything; it diffs two runs of the same program.
set -u
say() { echo; echo "======== $* ========"; }
REPO=PseudoCoupHQ/Research/compiler_graph
PIPE=PseudoCoupHQ/Research/op_pipeline
cd "$REPO"

say "[1/4] the baseline version, taken out of git"
cd PseudoCoupHQ
git log --format='%h %ad %s' --date=format:'%Y-%m-%d %H:%M' -1 e2cba0db
mkdir -p /work/baseline
git show e2cba0db:Research/compiler_graph/graph.py > /work/baseline/graph.py
wc -l /work/baseline/graph.py Research/compiler_graph/graph.py
grep -c "variant_connections" /work/baseline/graph.py || echo "   baseline has 0 mentions of variant_connections (as expected)"
cd "$REPO"

say "[2/4] Graph.coverage -- the same join, both versions, diffed"
rm -rf /work/reg_sample && mkdir -p /work/reg_sample
python3 - <<'PY'
import os
src = 'PseudoCoupHQ/Research/compiler_graph/diaries/go'
for n in sorted(x for x in os.listdir(src) if x.endswith('.txt'))[:30]:
    os.symlink(os.path.join(src, n), os.path.join('/work/reg_sample', n))
print("   sampled 30 go diaries")
PY
python3 /work/baseline/graph.py join --graph graph_go.json \
    --diaries /work/reg_sample --out /work/join_before.json 2>&1 | tail -4
python3 graph.py join --graph graph_go.json \
    --diaries /work/reg_sample --out /work/join_after.json 2>&1 | tail -4
if diff -q /work/join_before.json /work/join_after.json >/dev/null; then
  echo "   coverage: IDENTICAL"
else
  echo "   coverage: DIFFERS -- a regression"; diff /work/join_before.json /work/join_after.json | head -20
fi

say "[3/4] Graph.super_ops -- the same mine, both versions, diffed"
python3 /work/baseline/graph.py super-ops --graph graph_go.json \
    --diaries /work/reg_sample --min-length 3 --min-support 2 \
    --max-length 12 --max-runs-per-level 2000000 --memory-ceiling-mb 6144 \
    --subject probe_own --language go --cache /work/reg_before.i32 \
    --out /work/ops_before.json 2>&1 | tail -3
python3 graph.py super-ops --graph graph_go.json \
    --diaries /work/reg_sample --min-length 3 --min-support 2 \
    --max-length 12 --max-runs-per-level 2000000 --memory-ceiling-mb 6144 \
    --subject probe_own --language go --cache /work/reg_after.i32 \
    --out /work/ops_after.json 2>&1 | tail -3
python3 - <<'PY'
import json
a = json.load(open('/work/ops_before.json'))
b = json.load(open('/work/ops_after.json'))
for key in ("parameters", "populations", "candidates"):
    same = json.dumps(a[key], sort_keys=True) == json.dumps(b[key], sort_keys=True)
    print("   super_ops %-12s identical: %s" % (key, same))
print("   (the `cost` block carries wall time and a cache path and is "
      "expected to differ)")
PY

say "[4/4] the planning tree checked"
python3 PlanPlan/framework/check_plans.py \
    PseudoCoupHQ/Planning 2>&1 | tail -30
echo "   check_plans exit=$?"
echo "DONE t87_l13"
