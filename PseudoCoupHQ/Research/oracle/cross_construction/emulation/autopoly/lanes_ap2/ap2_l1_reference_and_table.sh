#!/usr/bin/env bash
# ap2_l1_reference_and_table.sh -- task ap2, fixes 4 and 5, MEASURED ON
# THE CELLS THEY TARGET before anything long runs.
#
# FIX 5, `reference.py`, three additive registrations:
#   * `cmovg`   -- already built by the `for suffix in CT.SUFFIX_TO_COND`
#                  loop with `build_move_condition`, then removed by
#                  `_prune`; now kept by `KEPT_MNEMONICS`.
#   * `movswq`  -- already built by the `for mnemonic in SIGN_EXTEND`
#                  loop with `build_extension`, then removed by
#                  `_prune`; now kept the same way.
#   * `lea 0x0(,%rdi,8)` -- the same (displacement, base, index, scale)
#                  shape with the base slot EMPTY, which is a base of
#                  zero.  `LEA_RE` makes the base optional and
#                  `build_lea` reads an absent base as zero.
#   GUARD: `check_L2`'s tally unchanged -- 259 rows, 172 STATED, 87
#   REFUSED (node_0_3_2 PROGRESS, task m1b's own reading, read three
#   times) -- and `check_L2.json` byte-identical after the re-run.
#
# FIX 4, `model_table.key_width`, one more case: a widening move's key
# width is its DESTINATION width, read from `reference.SIGN_EXTEND` and
# `reference.ZERO_EXTEND`.
#   GUARD: over the whole 71,778-row table, the only rows whose
#   `key_width` moves are rows of those mnemonics, and the eight cells
#   that carried null now carry a width.  Printed before and after.
#
# MEMORY BOUND: 6 GB resident on this one process, named abort
# ABORT_MEMORY_AP2.  The heavy read is the 73 MB `model_table.json`
# (task ap1 measured its parse at 290,040 kB).
set -euo pipefail
cd PseudoCoupHQ/Research/op_pipeline

echo "[1/4] the reference: the two mnemonics and the lea form"
python3 - <<'PY'
import os
import resource
import sys
sys.path.insert(0, "PseudoCoupHQ/Research/op_pipeline")
import reference as R

ABORT_KB = 6 * 1024 * 1024


def check(where):
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if peak > ABORT_KB:
        raise SystemExit("ABORT_MEMORY_AP2: %d kB at %s" % (peak, where))
    return peak


print("   EMULATION_MNEMONICS: %s" % R.EMULATION_MNEMONICS)
print("   len(CORPUS_MNEMONICS), the corpus's own census: %d"
      % len(R.CORPUS_MNEMONICS))
print("   len(KEPT_MNEMONICS): %d" % len(R.KEPT_MNEMONICS))

table = R.REFERENCE.opcode_table
for mnemonic in ("cmovg", "cmovl", "movswq", "movslq"):
    entry = table.entry_for(mnemonic)
    if entry is None:
        print("   %-8s NO ENTRY" % mnemonic)
        continue
    print("   %-8s reads=%s writes=%s builder=%s"
          % (mnemonic, entry.reads, entry.writes,
             getattr(entry.build, "__name__", entry.build)))

print("")
print("   the lea forms, through LEA_RE and build_lea:")
FORMS = ["0x0(,%rdi,8)", "(%rax)", "0x8(%rax)", "0x0(%rax,%rdx,4)",
         "-0x4(%rbp)", "0x2e57(%rip)", "(,%rdi,8)", "()"]
for text in FORMS:
    hit = R.LEA_RE.match(text)
    if hit is None:
        print("      %-20s LEA_RE: no match" % text)
    else:
        print("      %-20s LEA_RE: displacement=%r base=%r index=%r "
              "scale=%r" % ((text,) + hit.groups()))
print("   peak resident: %d kB" % check("after the reference"))
PY

echo "[2/4] check_L2, the regression guard on the reference"
cd PseudoCoupHQ/Research/op_pipeline/lean
sha256sum check_L2.json
python3 model_translate.py check
sha256sum check_L2.json

echo "[3/4] model_table.key_width: the rule, on the mnemonics it moves"
python3 - <<'PY'
import resource
import sys
sys.path.insert(0, "PseudoCoupHQ/Research/op_pipeline")
sys.path.insert(0, "PseudoCoupHQ/Research/oracle/arch_opcodes/model")
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
print("   key_width(mnem, width) on every widening mnemonic, at every "
      "width the sweep walks and at null:")
print("   | mnem | width null | 8 | 16 | 32 | 64 |")
for mnem in sorted(MTAB.WIDENING_MOVE_WIDTH):
    row = []
    for width in (None, 8, 16, 32, 64):
        row.append(str(MTAB.key_width(mnem, width)))
    print("   | %-8s | %s |" % (mnem, " | ".join(row)))
PY

echo "[4/4] the whole table: which rows' key_width moves, before and after"
python3 - <<'PY'
import json
import resource
import sys
sys.path.insert(0, "PseudoCoupHQ/Research/op_pipeline")
sys.path.insert(0, "PseudoCoupHQ/Research/oracle/arch_opcodes/model")
import model_table as MTAB

ABORT_KB = 6 * 1024 * 1024
MODEL = ("PseudoCoupHQ/Research/oracle/arch_opcodes/model/"
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

# THE ROW'S OWN `key_width` IS WHAT THE TABLE WAS WRITTEN WITH -- the
# BEFORE.  `key_width(mnem, width)` called now is the AFTER.  Nothing
# is re-swept here: the same function on the same two fields.
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

# THE ATTESTED CELLS whose key_width was null -- task ap1's six.
print("")
print("   attested cells (a TRANSLATED row with ledger_rows > 0) whose "
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
    after = MTAB.key_width(key[0], None)
    print("      %-8s %-14s ledger_rows %-6d stored widths %s -> "
          "key_width now %s"
          % (key[0], key[1], by_key[key][0],
             sorted(str(w) for w in by_key[key][1]), after))
print("   attested cells carrying a null key_width: %d" % len(by_key))
print("   peak resident: %d kB" % check("at the end"))
PY
echo "done"
