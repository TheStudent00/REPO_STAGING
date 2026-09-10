#!/usr/bin/env bash
# ap5_l22_the_one_regression.sh -- task ap5: the ONE run task ap4
# proved that this task does not, read off the two stores rather than
# described.  Nothing is re-run and nothing is written: this lane
# prints task ap4's line and task ap5's line for the single pair
# `sbb` imm_gpr 8 -> swift, field by field, LITERAL, so the cause is
# read from the record.
#
# The brief's STOP condition is "zero regressions or STOP"; the
# resumer's instruction is to stop and REPORT rather than run further,
# and this is the reading the report is built on.
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_AP5.  Both
# stores are read one line at a time and only the two matching lines
# are kept.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
python3 - <<'PY'
import json
import resource

ABORT_KB = 6 * 1024 * 1024
HERE = ("PseudoCoupHQ/Research/oracle/cross_construction/"
        "emulation/autopoly/")
WANT = ("sbb", "imm_gpr", 8, "swift")


def guard(where):
    got = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if got > ABORT_KB:
        raise SystemExit("ABORT_MEMORY_AP5: %d kB at %s" % (got, where))
    print("   peak resident at %s: %d kB" % (where, got))


def pick(name):
    handle = open(HERE + name)
    for line in handle:
        line = line.strip()
        if not line:
            continue
        run = json.loads(line)
        key = (run.get("mnem"), run.get("shape"), run.get("key_width"),
               run.get("lang"))
        if key == WANT:
            handle.close()
            return run
    handle.close()
    return None


def show(label, run):
    print("")
    print("== %s" % label)
    if run is None:
        print("   no line on this store for %s" % (WANT,))
        return
    for name in sorted(run):
        if name == "places":
            continue
        value = run[name]
        text = json.dumps(value)
        if len(text) > 400:
            text = text[:400] + " ...[%d chars]" % len(json.dumps(value))
        print("   %-28s %s" % (name, text))
    for place in run.get("places") or []:
        print("   -- place %s" % place.get("writes"))
        for name in sorted(place):
            if name in ("source", "term_text", "body_text"):
                print("      %-24s [%d chars, not printed here]"
                      % (name, len(str(place[name] or ""))))
                continue
            value = place[name]
            text = json.dumps(value)
            if len(text) > 400:
                text = text[:400] + " ...[%d chars]" % len(json.dumps(value))
            print("      %-24s %s" % (name, text))


print("[1/2] task ap4's store")
theirs = pick("autopoly4_runs.jsonl")
show("task ap4: `sbb` imm_gpr 8 -> swift", theirs)
guard("task ap4's line")

print("")
print("[2/2] task ap5's store")
mine = pick("autopoly5_runs.jsonl")
show("task ap5: `sbb` imm_gpr 8 -> swift", mine)
guard("task ap5's line")
print("done")
PY
