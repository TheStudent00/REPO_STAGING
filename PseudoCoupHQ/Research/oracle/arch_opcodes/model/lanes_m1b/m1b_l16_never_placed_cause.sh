#!/usr/bin/env bash
# m1b_l16_never_placed_cause.sh -- task m1b: the eight mnemonics the
# coverage table records as never placed, measured one level deeper
# than the table's own cause, so each is a fact rather than an
# absence. Per mnemonic, over the whole corpus:
#   body lines      -- lines of a canon40 unit's own body that spell it
#   linked lines    -- of those, how many the relink ties to a ledger
#                      row at all
#   attributed to   -- when a line IS tied to a row, what the row's
#                      produced_by says, which is how a line can be in
#                      the body and still name no cell of its own
# MEMORY BOUND: 16 GB resident inside the m1b instance's 20g, named
# abort ABORT_MEMORY_M1B, checked after every shard; one shard held
# and dropped. Peak RSS printed.
set -euo pipefail
echo "[1/2] task m1b: the never-placed eight, measured over 332 shards"
cd /projects/PseudoCoupHQ/Research/op_pipeline
python3 - <<'PY'
import collections
import json
import resource
import sys
import time

sys.path.insert(0, "/projects/PseudoCoupHQ/Research/op_pipeline")
sys.path.insert(0, "/projects/PseudoCoupHQ/Research/op_pipeline/lean")
sys.path.insert(0, "/projects/PseudoCoupHQ/Research/oracle/arch_opcodes")
import term as T
import canonical_form as CF
import term66_run as TR
import single_opcode_units as SOU

ABORT_MEMORY_M1B_KB = 16 * 1024 * 1024


def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


document = json.load(open("/projects/PseudoCoupHQ/Research/oracle/"
                          "arch_opcodes/model/model_table.json"))
wanted = []
for record in document["counts"]["coverage"]:
    if record["category"] == "never placed":
        wanted.append(record["mnem"])
print("   the eight: %s" % " ".join(wanted))
wanted = set(wanted)

readings = CF.runtime_answer_readings()
routines = CF.runtime_routine_names(readings)
body_lines = collections.Counter()
linked_lines = collections.Counter()
attributed = collections.Counter()
example = {}
shard_paths = TR.shards()
started = time.time()
for number, path in enumerate(shard_paths):
    shard = json.load(open(path))
    for unit_id, record in shard["units"].items():
        body = record.get("body_verbatim") or []
        here = set()
        for line in body:
            pieces = line.split(None, 1)
            if not pieces:
                continue
            mnem = pieces[0]
            if mnem not in wanted:
                continue
            body_lines[mnem] += 1
            here.add(line)
            if mnem not in example:
                example[mnem] = (unit_id, line)
        if not here:
            continue
        toolchain = CF.TOOLCHAIN_OF_LANGUAGE.get(record.get("lang"))
        try:
            _rows, line_of_row, _occ = T.relink(
                record, runtime_routines=routines,
                runtime_answers=readings, toolchain=toolchain)
        except Exception:
            continue
        by_line = {}
        for row_name in line_of_row:
            by_line.setdefault(line_of_row[row_name], []).append(row_name)
        rows_by_name = {}
        for row in record.get("ledger") or []:
            rows_by_name[row["row"]] = row
        for line in here:
            names = by_line.get(line)
            if not names:
                continue
            mnem = line.split(None, 1)[0]
            linked_lines[mnem] += 1
            for row_name in names:
                row = rows_by_name.get(row_name)
                if row is None:
                    continue
                producer = row.get("produced_by") or {}
                attributed[(mnem, str(producer.get("kind")),
                            str(producer.get("mnem")))] += 1
    del shard
    if peak_kb() > ABORT_MEMORY_M1B_KB:
        raise SystemExit("ABORT_MEMORY_M1B: %d kB" % peak_kb())
    if (number + 1) % 100 == 0 or number + 1 == len(shard_paths):
        print("   [%d/%d] shards, %.1f s"
              % (number + 1, len(shard_paths), time.time() - started))

print("")
print("   | mnem | body lines | lines the relink ties to a row |")
for mnem in sorted(wanted):
    print("   | %-8s | %6d | %6d |"
          % (mnem, body_lines[mnem], linked_lines[mnem]))
print("")
print("   where a linked line's row is attributed:")
for key in sorted(attributed, key=lambda k: (-attributed[k], str(k))):
    print("      %-8s -> kind %-18s mnem %-12s %d"
          % (key[0], key[1], key[2], attributed[key]))
print("")
print("   o2's own narrow chaff rule, LITERAL:")
print("      NARROW_BARE      = %s" % sorted(SOU.NARROW_BARE))
print("      NARROW_PURE_MOVE = %s" % sorted(SOU.NARROW_PURE_MOVE))
print("")
print("   one example body line each: %s" % dict(example))
print("")
print("peak RSS: %d kB" % peak_kb())
PY
echo "[2/2] done"
