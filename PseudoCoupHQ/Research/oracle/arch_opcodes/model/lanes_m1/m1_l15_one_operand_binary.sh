#!/usr/bin/env bash
# m1_l15_one_operand_binary.sh -- task m1: the one finding this table
# surfaces about the REFERENCE itself, measured rather than asserted.
# `reference.build_binary` opens with `if len(ops.texts) == 1:
# build_wide_multiply(ops); return`, so every mnemonic of the BINARY
# family -- not only `imul` -- gets the accumulator-pair widening
# multiply on a one-operand form. This lane counts the rows that reach
# the table that way and says whether the corpus attests any of them.
# Nothing is changed: `reference.py` is a shared file this brief did not
# name, so this is a flag for the coordinator.
set -euo pipefail
echo "[1/1] task m1: the one-operand BINARY rows"
cd PseudoCoupHQ/Research/oracle/arch_opcodes/model
python3 - <<'PY'
import json
import sys

sys.path.insert(0, "PseudoCoupHQ/Research/oracle/arch_opcodes/model")
import model_table as M

table = M.R.REFERENCE.opcode_table
family = []
for mnem in sorted(table.entries):
    entry = table.entries[mnem]
    if entry.build is None:
        continue
    if entry.build.__name__ != "build_binary":
        continue
    family.append(mnem)
print("the BINARY family, as the table registers it: %s"
      % " ".join(family))
print("")
print("the branch, quoted from reference.py's build_binary:")
import inspect
source = inspect.getsource(M.R.build_binary).split("\n")
for line in source[1:4]:
    print("    %s" % line)
print("")

document = json.load(open("model_table.json"))
one_operand = []
for row in document["rows"]:
    if row["outcome"] != "TRANSLATED":
        continue
    if row.get("builder") != "build_binary":
        continue
    if len(row.get("operands") or []) != 1:
        continue
    one_operand.append(row)
print("TRANSLATED rows whose builder is build_binary and whose line "
      "has ONE operand: %d" % len(one_operand))
by_mnem = {}
for row in one_operand:
    by_mnem.setdefault(row["mnem"], []).append(row)
print("")
print("| mnem | rows | ledger rows the corpus attests for those "
      "triples |")
print("|---|---|---|")
for mnem in sorted(by_mnem):
    attested = 0
    for row in by_mnem[mnem]:
        attested = attested + row["attestation"]["ledger_rows"]
    print("| %s | %d | %d |" % (mnem, len(by_mnem[mnem]), attested))
print("")
print("one such row in full, LITERAL:")
for row in one_operand:
    if row["mnem"] != "add":
        continue
    if row["shape"] != "gpr_one":
        continue
    if row["width"] != 32:
        continue
    print(json.dumps(row, indent=1, sort_keys=True))
    break
print("")
print("peak RSS: %d kB" % M.peak_kb())
PY
echo "[1/1] done"
