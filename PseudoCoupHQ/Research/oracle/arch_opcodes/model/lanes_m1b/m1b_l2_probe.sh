#!/usr/bin/env bash
# m1b_l2_probe.sh -- task m1b, the second survey lane: the four
# populations the closer has to key, measured over the WHOLE corpus
# (332 canon40 shards) before any code is written.
#   1. the reference handed the three x87 shapes on a PRESEEDED state
#      (the sweep's own second pass), and on a fresh one
#   2. what the three new shapes do to a NON-x87 mnemonic
#   3. every flag_pair row of the corpus: consumer, block, setter,
#      and whether the relink gives it a line
#   4. every x87 line of the corpus: the operand texts, per mnemonic
#   5. the control transfers: every ledger row that carries one
# MEMORY BOUND: 16 GB resident inside the m1b instance's 20g, named
# abort ABORT_MEMORY_M1B (resource.getrusage), checked after every
# shard; one shard is held at a time and dropped. Peak RSS printed.
set -euo pipefail
echo "[1/5] task m1b: the reference, handed the three x87 shapes"
cd PseudoCoupHQ/Research/op_pipeline
python3 - <<'PY'
import collections
import json
import os
import resource
import sys
import time

sys.path.insert(0, "PseudoCoupHQ/Research/op_pipeline")
sys.path.insert(0, "PseudoCoupHQ/Research/op_pipeline/lean")
import reference as R
import ledger48 as L48
import term as T
import canonical_form as CF
import term66_run as TR
import model_translate as MT

ABORT_MEMORY_M1B_KB = 16 * 1024 * 1024


def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def check_memory(where):
    now = peak_kb()
    if now > ABORT_MEMORY_M1B_KB:
        raise SystemExit("ABORT_MEMORY_M1B: %d kB at %s" % (now, where))


NEW_SHAPES = [
    ("st_st", ["%st", "%st(1)"]),
    ("st_one", ["%st(1)"]),
    ("st_none", []),
]

table = R.REFERENCE.opcode_table
x87_mnems = []
for mnem in sorted(table.entries):
    if L48.x87_base(mnem) is not None:
        x87_mnems.append(mnem)

model = MT.Model()
for preseeded in (False, True):
    outcomes = collections.Counter()
    example = {}
    for mnem in x87_mnems:
        for shape_name, texts in NEW_SHAPES:
            row = MT.one_attempt(model, mnem, shape_name, 64,
                                 list(texts), None, preseeded)
            outcomes[(shape_name, row["outcome"])] += 1
            key = (shape_name, row["outcome"])
            if key not in example:
                places = []
                for one in row.get("defs") or []:
                    places.append(one["writes"])
                example[key] = (mnem, row.get("line"), places,
                                (row.get("cause") or "")[:90])
    print("   preseeded=%s, over the %d x87 mnemonics"
          % (preseeded, len(x87_mnems)))
    for key in sorted(outcomes, key=str):
        print("      %-8s %-32s %d" % (key[0], key[1], outcomes[key]))
    for key in sorted(example, key=str):
        print("      e.g. %-8s %-30s %s" % (key[0], key[1], example[key]))

print("")
print("[2/5] the three new shapes over the mnemonics that are NOT x87")
other = []
for mnem in sorted(table.entries):
    if L48.x87_base(mnem) is None:
        other.append(mnem)
outcomes = collections.Counter()
translated = []
for preseeded in (False, True):
    for mnem in other:
        entry = table.entries[mnem]
        if entry.build is None:
            continue
        for shape_name, texts in NEW_SHAPES:
            row = MT.one_attempt(model, mnem, shape_name, 64,
                                 list(texts), None, preseeded)
            outcomes[(preseeded, shape_name, row["outcome"])] += 1
            if row["outcome"] == "TRANSLATED":
                translated.append((preseeded, mnem, shape_name,
                                   row.get("line")))
for key in sorted(outcomes, key=str):
    print("   preseeded=%-5s %-8s %-32s %d"
          % (key[0], key[1], key[2], outcomes[key]))
print("   the TRANSLATED ones (%d): %s"
      % (len(translated), translated[:40]))
check_memory("after the shape probe")

print("")
print("[3/5] how many attempts the three new shapes add")
before = len(MT.attempts_for("add"))
print("   attempts_for('add') today: %d" % before)
print("   the three new shapes would add 3 per width x %d widths = %d"
      % (len(MT.SWEEP_WIDTHS), 3 * len(MT.SWEEP_WIDTHS)))
print("   table mnemonics: %d, so the sweep grows by about %d attempts"
      % (len(table.entries), 3 * len(MT.SWEEP_WIDTHS)
         * len(table.entries)))

print("")
print("[4/5] the whole corpus: flag_pair rows, x87 lines, transfers")
readings = CF.runtime_answer_readings()
routines = CF.runtime_routine_names(readings)
shard_paths = TR.shards()
pair_by_consumer = collections.Counter()
pair_by_block = collections.Counter()
pair_line = collections.Counter()
pair_setters = collections.Counter()
pair_shape_texts = collections.Counter()
pair_example = {}
x87_operand_texts = collections.Counter()
x87_example = {}
transfer_arch_rows = collections.Counter()
kinds = collections.Counter()
units_seen = 0
started = time.time()
for number, path in enumerate(shard_paths):
    document = json.load(open(path))
    for unit_id, record in document["units"].items():
        units_seen = units_seen + 1
        toolchain = CF.TOOLCHAIN_OF_LANGUAGE.get(record.get("lang"))
        try:
            _rows, line_of_row, _occ = T.relink(
                record, runtime_routines=routines,
                runtime_answers=readings, toolchain=toolchain)
        except Exception:
            line_of_row = None
        for row in record.get("ledger") or []:
            produced_by = row.get("produced_by") or {}
            kind = produced_by.get("kind")
            mnem = produced_by.get("mnem")
            kinds[kind] += 1
            line = None
            if line_of_row is not None:
                line = line_of_row.get(row["row"])
            if kind == "flag_pair" and isinstance(mnem, list) \
                    and len(mnem) == 2:
                consumer = mnem[1]
                pair_by_consumer[consumer] += 1
                pair_by_block[(row.get("block"), line is not None)] += 1
                pair_setters[mnem[0]] += 1
                if line is None:
                    pair_line[(row.get("block"),
                               "no line from the relink")] += 1
                    continue
                pair_line[(row.get("block"), "a line")] += 1
                pieces = line.split(None, 1)
                rest = ""
                if len(pieces) > 1:
                    rest = pieces[1].strip()
                entry = table.entries.get(consumer)
                writes = "(not in the table)"
                if entry is not None:
                    writes = " ".join(sorted(entry.writes))
                pair_shape_texts[(consumer, rest, writes,
                                  row.get("size"))] += 1
                if consumer not in pair_example:
                    pair_example[consumer] = (line, mnem[0], writes)
                continue
            if not isinstance(mnem, str):
                continue
            if L48.x87_base(mnem) is not None and line is not None:
                pieces = line.split(None, 1)
                rest = "(no operand)"
                if len(pieces) > 1:
                    rest = pieces[1].strip()
                x87_operand_texts[(mnem, rest, row.get("size"))] += 1
                if mnem not in x87_example:
                    x87_example[mnem] = line
            entry = table.entries.get(mnem)
            if entry is None:
                continue
            if R.THE_BRANCH_CONDITION in entry.writes or \
                    mnem in ("jmp", "call", "ret", "ud2"):
                transfer_arch_rows[mnem] += 1
    del document
    check_memory("shard %d" % number)
    if (number + 1) % 100 == 0 or number + 1 == len(shard_paths):
        print("   [%d/%d] shards, %d units, %.1f s"
              % (number + 1, len(shard_paths), units_seen,
                 time.time() - started))

print("")
print("row kinds over the whole corpus: %s" % dict(kinds))
print("flag_pair rows: %d over %d distinct consumers"
      % (sum(pair_by_consumer.values()), len(pair_by_consumer)))
print("  block x has-a-line: %s" % dict(pair_line))
print("  setters: %s" % dict(pair_setters))
print("  per consumer (rows, and the write set the reference gives it):")
for consumer in sorted(pair_by_consumer,
                       key=lambda c: -pair_by_consumer[c]):
    writes = "(not in the table)"
    entry = table.entries.get(consumer)
    if entry is not None:
        writes = " ".join(sorted(entry.writes))
    print("     %-10s %6d   writes: %s" % (consumer,
                                           pair_by_consumer[consumer],
                                           writes))
print("  the operand texts of a flag_pair row's line, top 40:")
for key in sorted(pair_shape_texts,
                  key=lambda k: (-pair_shape_texts[k], str(k)))[:40]:
    print("     %-10s %-22s size=%-4s %-24s %d"
          % (key[0], key[1], key[3], key[2], pair_shape_texts[key]))

print("")
print("x87 lines, by mnemonic and operand text:")
for key in sorted(x87_operand_texts,
                  key=lambda k: (-x87_operand_texts[k], str(k))):
    print("   %-10s %-24s size=%-4s %d"
          % (key[0], key[1], key[2], x87_operand_texts[key]))

print("")
print("[5/5] ledger rows produced by a control transfer: %s"
      % dict(transfer_arch_rows))
print("")
print("peak RSS: %d kB" % peak_kb())
PY
echo "[5/5] done"
