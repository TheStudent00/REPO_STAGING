#!/usr/bin/env bash
# ap2_l2_table_and_check_L2.sh -- task ap2: the two guards lane
# ap2_l1 did not reach, and the reason it did not.
#
# WHY THIS LANE EXISTS.  Lane ap2_l1 ran `model_translate.py check` as
# the regression guard the brief names on fix 5, and it stopped on
# `KeyError: 'mnemonic'` in `load_rows`.  That is NOT this task's
# change: it is the defect task m1b already recorded as the first of
# the four items in log_237 section 14 -- `model_translate.load_rows`
# still reads task o2's artifact by the field name task mn1 renamed to
# `mnem`.  So `check_L2` cannot be re-derived by anyone today, and this
# lane guards it the only way that is honest: it reads the STORED
# `check_L2.json`, prints its tally, and then measures whether either
# of this task's two reference changes could reach a row of it -- by
# asking the population `check_L2` is built over whether it spells
# `cmovg` or `movswq` at all, and whether any of its bodies carries a
# lea form with an empty base slot.
#
# The rest of the lane is steps 3 and 4 of ap2_l1: fix 4, the
# `key_width` case, over the whole 71,778-row table.
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_AP2.
set -euo pipefail

echo "[1/3] check_L2: the stored tally, and whether this task can reach it"
python3 - <<'PY'
import json
import os
import re
import resource
import sys
sys.path.insert(0, "/projects/PseudoCoupHQ/Research/op_pipeline")
import reference as R

ABORT_KB = 6 * 1024 * 1024
LEAN = "/projects/PseudoCoupHQ/Research/op_pipeline/lean/check_L2.json"
UNITS = ("/projects/PseudoCoupHQ/Research/oracle/arch_opcodes/"
         "single_opcode_units.json")


def check(where):
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if peak > ABORT_KB:
        raise SystemExit("ABORT_MEMORY_AP2: %d kB at %s" % (peak, where))
    return peak


document = json.load(open(LEAN))
rows = document["rows"]
tally = {}
for row in rows:
    tally[row.get("outcome")] = tally.get(row.get("outcome"), 0) + 1
print("   check_L2.json rows: %d" % len(rows))
for outcome in sorted(tally):
    print("      %-10s %d" % (outcome, tally[outcome]))

# THE POPULATION `check_L2` IS BUILT OVER, read the same way
# `model_translate.load_rows` reads it -- by task mn1's field name,
# which is the one the artifact now carries.
units = json.load(open(UNITS))
spelled = {}
lea_forms = set()
bodies = 0
for language in ("c", "cpp", "go", "rust", "swift"):
    group = units["single_opcode_groups"][language]["narrow"]
    for row in group:
        bodies = bodies + 1
        name = row.get("mnem", row.get("mnemonic"))
        spelled[name] = spelled.get(name, 0) + 1
        for line in (row.get("body_text") or "").split(";"):
            stripped = line.strip()
            if not stripped.startswith("lea"):
                continue
            for piece in stripped.split():
                if "(" in piece:
                    lea_forms.add(piece)
print("   rows of the population check_L2 is built over: %d" % bodies)
print("   distinct mnemonics it spells: %d" % len(spelled))
for name in R.EMULATION_MNEMONICS:
    print("      does it spell %-8s ? %s" % (name, name in spelled))
print("   lea operand forms in that population: %d" % len(lea_forms))
empty_base = []
for form in sorted(lea_forms):
    hit = R.LEA_RE.match(form)
    if hit is not None and hit.group(2) is None:
        empty_base.append(form)
print("      of them with an EMPTY BASE SLOT, the form this task's "
      "change reaches: %s" % empty_base)
print("   peak resident: %d kB" % check("after check_L2"))
PY

echo "[2/3] model_table.key_width: the rule, on the mnemonics it moves"
python3 - <<'PY'
import sys
sys.path.insert(0, "/projects/PseudoCoupHQ/Research/op_pipeline")
sys.path.insert(0, "/projects/PseudoCoupHQ/Research/oracle/arch_opcodes/model")
import reference as R
import model_table as MTAB

print("   WIDENING_MOVE_WIDTH, read from the reference's own tables:")
for mnem in sorted(MTAB.WIDENING_MOVE_WIDTH):
    print("      %-8s -> %d" % (mnem, MTAB.WIDENING_MOVE_WIDTH[mnem]))
print("")
print("   the mnemonics with a pair of None, left to the general rule: "
      "%s" % sorted(name for table in (R.SIGN_EXTEND, R.ZERO_EXTEND)
                    for name in table if table[name] is None))
print("")
print("   key_width(mnem, width) on every widening mnemonic:")
print("   | mnem | width null | 8 | 16 | 32 | 64 |")
print("   |---|---|---|---|---|---|")
for mnem in sorted(MTAB.WIDENING_MOVE_WIDTH):
    row = []
    for width in (None, 8, 16, 32, 64):
        row.append(str(MTAB.key_width(mnem, width)))
    print("   | %-8s | %s |" % (mnem, " | ".join(row)))
PY

echo "[3/3] the whole table: which rows' key_width moves, before and after"
python3 - <<'PY'
import json
import resource
import sys
sys.path.insert(0, "/projects/PseudoCoupHQ/Research/op_pipeline")
sys.path.insert(0, "/projects/PseudoCoupHQ/Research/oracle/arch_opcodes/model")
import model_table as MTAB

ABORT_KB = 6 * 1024 * 1024
MODEL = ("/projects/PseudoCoupHQ/Research/oracle/arch_opcodes/model/"
         "model_table.json")


def check(where):
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if peak > ABORT_KB:
        raise SystemExit("ABORT_MEMORY_AP2: %d kB at %s" % (peak, where))
    return peak


document = json.load(open(MODEL))
print("   peak after the parse: %d kB" % check("after the parse"))
rows = document["rows"]
print("   rows in the table: %d" % len(rows))
print("   the table's own counts: %s"
      % json.dumps(document["counts"], sort_keys=True))

# THE ROW'S OWN STORED `key_width` IS THE BEFORE; `key_width(mnem,
# width)` called now is the AFTER.  Nothing is re-swept: the same
# function over the same two fields of the same rows.
moved = {}
same = 0
for row in rows:
    before = row.get("key_width")
    after = MTAB.key_width(row["mnem"], row.get("width"))
    if before == after:
        same = same + 1
        continue
    key = (row["mnem"], row.get("shape"), str(before), str(after))
    moved[key] = moved.get(key, 0) + 1
print("   rows whose key_width is unchanged: %d" % same)
print("   rows whose key_width moves: %d"
      % sum(moved[key] for key in moved))
print("")
print("   | mnem | shape | before | after | rows |")
print("   |---|---|---|---|---|")
for key in sorted(moved):
    print("   | %s | %s | %s | %s | %d |"
          % (key[0], key[1], key[2], key[3], moved[key]))

print("")
print("   ATTESTED CELLS (a TRANSLATED row with ledger_rows > 0) whose "
      "stored key_width is null:")
by_key = {}
for row in rows:
    if row.get("outcome") != "TRANSLATED":
        continue
    held = (row.get("attestation") or {}).get("ledger_rows") or 0
    if held <= 0:
        continue
    key = (row["mnem"], row.get("shape"), row.get("key_width"))
    if key[2] is not None:
        continue
    by_key.setdefault(key, [0, set()])
    by_key[key][0] = max(by_key[key][0], held)
    by_key[key][1].add(row.get("width"))
for key in sorted(by_key, key=lambda k: (-by_key[k][0], k)):
    print("      %-8s %-14s ledger_rows %-6d stored widths %s -> "
          "key_width now %s"
          % (key[0], key[1], by_key[key][0],
             sorted(str(w) for w in by_key[key][1]),
             MTAB.key_width(key[0], None)))
print("   attested cells carrying a null key_width: %d" % len(by_key))

print("")
print("   THE OUTER SET, counted the way lane ap1_l1_cells.sh counts "
       "it, with the key_width rule as it now stands:")
outer = {}
for row in rows:
    if row.get("outcome") != "TRANSLATED":
        continue
    held = (row.get("attestation") or {}).get("ledger_rows") or 0
    if held <= 0:
        continue
    key = (row["mnem"], row.get("shape"),
           MTAB.key_width(row["mnem"], row.get("width")))
    outer[key] = max(outer.get(key, 0), held)
print("      cells: %d" % len(outer))
print("      attested ledger rows over them: %d"
      % sum(outer[key] for key in outer))
print("      cells whose key_width is still null: %d"
      % len([key for key in outer if key[2] is None]))
print("   peak resident: %d kB" % check("at the end"))
PY
echo "done"
