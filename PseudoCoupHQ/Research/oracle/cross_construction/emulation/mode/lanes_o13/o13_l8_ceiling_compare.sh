#!/bin/bash
# task o13, lane 8: the standing rule on time/memory limits -- a limit
# is a flag, so report whether the answer changed between the 3,000 ms
# ceiling (the verdict of record) and the 30,000 ms re-run, per entry,
# using the report's own outcome_word() so nothing is re-defined here.
set -u
M=/projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/mode
export PATH=/opt/cargo/bin:$PATH
cd "$M" && python3 - <<'PY'
import json, sys
sys.path.insert(0, ".")
import mode

def load(path):
    return {r["entry_id"]: r for r in mode.read_json(path)["results"]}

print("[1/1] outcome at 3,000 ms vs 30,000 ms, per target")
for target, base_path, raised_path in (
    ("c", "mode_run_c.json", "mode_run_c_30000_ms.json"),
    ("rust", "mode_run_rust.json", "mode_run_rust_30000_ms.json"),
):
    base = load(base_path)
    raised = load(raised_path)
    changed = []
    same = 0
    for entry_id, rec in base.items():
        other = raised.get(entry_id)
        if other is None:
            continue
        w0, _ = mode.outcome_word(rec)
        w1, _ = mode.outcome_word(other)
        if w0 == w1:
            same += 1
        else:
            changed.append((entry_id, rec["x_unit"], w0, w1))
    print("  %s: %d entries compared, %d unchanged, %d changed"
          % (target, len(base), same, len(changed)))
    for row in changed:
        print("    CHANGED %s (%s): %s -> %s" % row)
print("lane o13_l8 done")
PY
