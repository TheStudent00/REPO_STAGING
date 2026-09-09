#!/usr/bin/env bash
# m1_l3_classifier.sh -- task m1: the operand-form classifier re-checked
# over three whole shards after two corrections (a `%cl` written LAST is
# a destination register, not the count; a row with no line is named as
# the OUT block's answer row where that is what it is). MEMORY BOUND:
# 16g, named abort ABORT_MEMORY_M1; one shard held at a time.
set -euo pipefail
echo "[1/1] task m1: classify_line over three shards"
cd PseudoCoupHQ/Research/oracle/arch_opcodes/model
python3 - <<'PY'
import json
import sys

sys.path.insert(0, "PseudoCoupHQ/Research/oracle/arch_opcodes/model")
import model_table as M

M._install_gpr_widths()
readings = M.CF.runtime_answer_readings()
routines = M.CF.runtime_routine_names(readings)
every = M.TR.shards()
chosen = [every[0], every[1], every[5]]
placed = 0
missed = {}
example = {}
shapes = {}
for path in chosen:
    document = json.load(open(path))
    print("shard %s: %d units" % (path.split("/")[-1],
                                  len(document["units"])))
    for unit_id, record in document["units"].items():
        line_of_row = M.lines_of_unit(record, routines, readings)
        if line_of_row is None:
            cause = "the unit's body could not be relinked"
            missed.setdefault(cause, 0)
            missed[cause] += len(M.arch_opcode_rows(record))
            continue
        for row in M.arch_opcode_rows(record):
            line = line_of_row.get(row["row"])
            if line is None:
                cause = M.no_line_cause(row)
                missed.setdefault(cause, 0)
                missed[cause] += 1
                continue
            shape, width, cause = M.classify_line(
                row["produced_by"]["mnem"], line, row.get("size"))
            if cause is not None:
                missed.setdefault(cause, 0)
                missed[cause] += 1
                if cause not in example:
                    example[cause] = line
                continue
            placed = placed + 1
            key = "%s|%s" % (shape, width)
            shapes.setdefault(key, 0)
            shapes[key] += 1
    del document
print("")
print("placed %d rows into %d (shape, width) cells" % (placed,
                                                       len(shapes)))
print("")
print("missed, by cause:")
for cause in sorted(missed, key=lambda c: -missed[c]):
    print("  %6d  %s" % (missed[cause], cause))
    if cause in example:
        print("          example line: %r" % example[cause])
print("")
print("the ten most common cells:")
for key in sorted(shapes, key=lambda k: -shapes[k])[:10]:
    print("  %6d  %s" % (shapes[key], key))
print("")
print("peak RSS: %d kB" % M.peak_kb())
PY
echo "[1/1] done"
