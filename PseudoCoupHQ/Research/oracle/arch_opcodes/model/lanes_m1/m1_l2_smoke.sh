#!/usr/bin/env bash
# m1_l2_smoke.sh -- task m1: model_table.py's own pieces, exercised on a
# handful of objects before the whole-table run. MEMORY BOUND: 16g,
# named abort ABORT_MEMORY_M1 (model_table.check_memory); this lane
# holds one shard at most. Peak RSS printed at the end.
set -euo pipefail
echo "[1/1] task m1: model_table.py pieces on a handful of objects"
cd /projects/PseudoCoupHQ/Research/oracle/arch_opcodes/model
python3 - <<'PY'
import json
import sys

sys.path.insert(0, "/projects/PseudoCoupHQ/Research/oracle/arch_opcodes/model")
import model_table as M

print("the partial region, per builder, for the five the brief names")
table = M.R.REFERENCE.opcode_table
for mnem in ["add", "lea", "imul", "sar", "idiv", "shl", "mul", "div",
             "movzbl", "call"]:
    entry = table.entries[mnem]
    print("  %-8s builder=%-24s %s"
          % (mnem, M.builder_name(entry), M.partial_region(entry)[:220]))

print("")
print("one row of each of the five example triples")
holder = M.T.Term()
model = M.MT.Model()
wanted = [("add", "gpr_gpr", 32), ("imul", "gpr_one", 32),
          ("imul", "gpr_gpr", 32), ("sar", "cl_gpr", 32),
          ("idiv", "gpr_one", 32)]
index = 0
for mnem, shape_wanted, width_wanted in wanted:
    for shape_name, width, texts in M.MT.attempts_for(mnem):
        if shape_name != shape_wanted:
            continue
        if width != width_wanted:
            continue
        attempt = M.MT.one_attempt(model, mnem, shape_name, width, texts)
        row = M.row_of_attempt(holder, table, index, attempt)
        index = index + 1
        print(json.dumps(row, indent=1, sort_keys=True))
        print("")

print("the operand-form classifier, on real body lines")
M._install_gpr_widths()
lines = ["add %esi,%edi", "imul %esi,%edi", "imul %edi",
         "sar %cl,%eax", "idivl (%rsi)", "idiv %esi",
         "lea (%rsi,%rcx,1),%rdi", "lea 0x1(%rdi),%eax",
         "mov -0x8(%rbp),%eax", "movzbl %sil,%eax",
         "shl $0x3,%rax", "test %edi,%edi", "cvtsi2sd %edi,%xmm0",
         "xor %eax,%eax", "movss %xmm1,%xmm0", "cltq", "ret",
         "addsd (%rax),%xmm0", "shld %cl,%rsi,%rdi"]
for line in lines:
    mnem = line.split()[0]
    shape, width, cause = M.classify_line(mnem, line, 8)
    print("  %-28s -> shape=%-14s width=%-5s %s"
          % (line, shape, width, cause or ""))

print("")
print("one shard: the classifier over its real ledger rows")
readings = M.CF.runtime_answer_readings()
routines = M.CF.runtime_routine_names(readings)
path = M.TR.shards()[0]
document = json.load(open(path))
placed = 0
missed = {}
for unit_id, record in list(document["units"].items())[:200]:
    line_of_row = M.lines_of_unit(record, routines, readings)
    if line_of_row is None:
        missed.setdefault("relink refused", 0)
        missed["relink refused"] += 1
        continue
    for row in M.arch_opcode_rows(record):
        line = line_of_row.get(row["row"])
        if line is None:
            missed.setdefault("no line", 0)
            missed["no line"] += 1
            continue
        shape, width, cause = M.classify_line(
            row["produced_by"]["mnem"], line, row.get("size"))
        if cause is not None:
            missed.setdefault(cause, 0)
            missed[cause] += 1
            continue
        placed = placed + 1
print("  placed %d rows; missed: %s" % (placed, json.dumps(missed)))
print("")
print("peak RSS: %d kB" % M.peak_kb())
PY
echo "[1/1] done"
