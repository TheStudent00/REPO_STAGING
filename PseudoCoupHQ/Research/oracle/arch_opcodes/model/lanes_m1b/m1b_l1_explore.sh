#!/usr/bin/env bash
# m1b_l1_explore.sh -- task m1b, the survey lane: the five things the
# closer's shape depends on, measured before anything is written.
#   1. the flag_pair ledger rows the m1 classifier never read
#   2. the control transfers, and which ledger rows carry them
#   3. the x87 operand texts the corpus actually spells
#   4. what the reference does when it is handed the three x87 operand
#      shapes the brief authorises
#   5. the mnemonics of the 162 with no attested cell in m1's artifact
# MEMORY BOUND: 16 GB resident inside the m1b instance's 20g, named
# abort ABORT_MEMORY_M1B (resource.getrusage), checked after every
# shard. This lane reads FOUR shards, one at a time, and drops each.
# Peak RSS is printed at the end.
set -euo pipefail
echo "[1/5] task m1b: the flag_pair rows, over four canon40 shards"
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
sys.path.insert(0, "PseudoCoupHQ/Research/oracle/arch_opcodes/model")
import reference as R
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


readings = CF.runtime_answer_readings()
routines = CF.runtime_routine_names(readings)
shard_paths = TR.shards()
print("shards on this machine: %d" % len(shard_paths))
sample = shard_paths[:4]

pair_consumers = collections.Counter()
pair_setters = collections.Counter()
pair_blocks = collections.Counter()
pair_line_hit = collections.Counter()
pair_examples = {}
transfer_rows = collections.Counter()
transfer_blocks = collections.Counter()
transfer_examples = {}
x87_operands = collections.Counter()
x87_lines = {}
kinds = collections.Counter()

TRANSFERS = set(["jmp", "call", "ret", "ud2"])


def is_transfer(mnem):
    if mnem in TRANSFERS:
        return True
    if mnem.startswith("j"):
        return True
    return False


for number, path in enumerate(sample):
    document = json.load(open(path))
    for unit_id, record in document["units"].items():
        toolchain = CF.TOOLCHAIN_OF_LANGUAGE.get(record.get("lang"))
        line_of_row = None
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
            if kind == "flag_pair" and isinstance(mnem, list) \
                    and len(mnem) == 2:
                pair_setters[mnem[0]] += 1
                pair_consumers[mnem[1]] += 1
                pair_blocks[(row.get("block"), mnem[1])] += 1
                line = None
                if line_of_row is not None:
                    line = line_of_row.get(row["row"])
                if line is None:
                    pair_line_hit["no line from the relink"] += 1
                else:
                    pair_line_hit["a line from the relink"] += 1
                    if mnem[1] not in pair_examples:
                        pair_examples[mnem[1]] = (row.get("block"),
                                                  mnem[0], line)
            if isinstance(mnem, str) and is_transfer(mnem):
                transfer_rows[mnem] += 1
                transfer_blocks[(row.get("block"), mnem)] += 1
                if mnem not in transfer_examples:
                    line = None
                    if line_of_row is not None:
                        line = line_of_row.get(row["row"])
                    transfer_examples[mnem] = (row.get("block"), line,
                                               row.get("type"))
            if isinstance(mnem, str) and mnem.startswith("f"):
                if line_of_row is None:
                    continue
                line = line_of_row.get(row["row"])
                if line is None:
                    continue
                pieces = line.split(None, 1)
                if len(pieces) < 2:
                    x87_operands[(mnem, "(no operand)")] += 1
                    continue
                x87_operands[(mnem, pieces[1].strip())] += 1
                if mnem not in x87_lines:
                    x87_lines[mnem] = line
    del document
    check_memory("shard %d" % number)
    print("   [%d/%d] %s read" % (number + 1, len(sample),
                                  os.path.basename(path)))

print("")
print("ledger row kinds over the four shards: %s"
      % dict(kinds))
print("flag_pair rows: %d" % sum(pair_consumers.values()))
print("  by block and consumer:")
for key in sorted(pair_blocks, key=str):
    print("     %-6s %-10s %d" % (key[0], key[1], pair_blocks[key]))
print("  the relink's line for a flag_pair row: %s"
      % dict(pair_line_hit))
print("  one example per consumer (block, setter, line):")
for consumer in sorted(pair_examples):
    print("     %-10s %s" % (consumer, pair_examples[consumer]))
print("  setters seen: %s" % dict(pair_setters))

print("")
print("[2/5] the control transfers in the ledger")
print("rows whose produced_by.mnem is a control transfer: %s"
      % dict(transfer_rows))
for key in sorted(transfer_blocks, key=str):
    print("   %-6s %-8s %d" % (key[0], key[1], transfer_blocks[key]))
print("one example each (block, line, type): %s"
      % dict(transfer_examples))

print("")
print("[3/5] the x87 operand texts the corpus spells")
for key in sorted(x87_operands, key=lambda k: (-x87_operands[k], str(k))):
    print("   %-10s %-24s %d" % (key[0], key[1], x87_operands[key]))

print("")
print("[4/5] the reference, handed the three x87 operand shapes")
NEW_SHAPES = [
    ("st_st", ["%st", "%st(1)"]),
    ("st_one", ["%st(1)"]),
    ("st_none", []),
]
table = R.REFERENCE.opcode_table
x87_mnems = []
for mnem in sorted(table.entries):
    import ledger48 as L48
    if L48.x87_base(mnem) is not None:
        x87_mnems.append(mnem)
print("x87 mnemonics in the table: %d -- %s"
      % (len(x87_mnems), " ".join(x87_mnems)))
model = MT.Model()
outcomes = collections.Counter()
first = {}
for mnem in x87_mnems:
    for shape_name, texts in NEW_SHAPES:
        row = MT.one_attempt(model, mnem, shape_name, 64, list(texts))
        outcomes[(shape_name, row["outcome"])] += 1
        key = (shape_name, row["outcome"])
        if key not in first:
            first[key] = (mnem, row.get("cause"),
                          [d["writes"] for d in row.get("defs") or []])
for key in sorted(outcomes, key=str):
    print("   %-8s %-32s %d" % (key[0], key[1], outcomes[key]))
print("   one example each:")
for key in sorted(first, key=str):
    print("     %-8s %-30s %s" % (key[0], key[1], first[key]))

print("")
print("[5/5] the 162, against m1's attestation artifact")
corpus = json.load(open("PseudoCoupHQ/Research/oracle/"
                        "arch_opcodes/unique_opcodes.json"))
corpus_mnems = sorted(r["mnem"] for r in corpus["cross_language_rows"])
attest = json.load(open("PseudoCoupHQ/Research/oracle/"
                        "arch_opcodes/model/model_table_attest.json"))
attested = set(c["mnem"] for c in attest["cells"])
missing = [m for m in corpus_mnems if m not in attested]
print("corpus mnemonics: %d; with at least one attested cell: %d; "
      "with none: %d" % (len(corpus_mnems),
                         len(corpus_mnems) - len(missing), len(missing)))
groups = collections.Counter()
for mnem in missing:
    if is_transfer(mnem):
        groups["a control transfer"] += 1
    elif mnem.startswith("set") or mnem.startswith("cmov"):
        groups["a flag consumer"] += 1
    elif mnem.startswith("f"):
        groups["x87"] += 1
    else:
        groups["other"] += 1
print("   %s" % dict(groups))
print("   the 'other' ones: %s"
      % " ".join(m for m in missing
                 if not is_transfer(m)
                 and not m.startswith("set")
                 and not m.startswith("cmov")
                 and not m.startswith("f")))
print("")
print("peak RSS: %d kB" % peak_kb())
PY
echo "[5/5] done"
