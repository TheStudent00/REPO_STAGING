#!/usr/bin/env bash
# ap5_l4_build_the_cells_file.sh -- task ap5: `autopoly5_cells.json`,
# which is task ap4's cells file with the SYMBOLIC-IMMEDIATE rows added
# and nothing else touched.
#
# WHAT IT ADDS AND WHERE.  For every cell of the outer set whose shape
# begins `imm`, the row the driver already chooses is spelled a second
# time with a register of the operand's own width in the immediate's
# slot -- the spelling `model_translate.shapes_for` now lists as
# `imm_symbolic_*` -- and the reference is asked for it.  Where it
# answers, the new row goes into that cell's own `rows` list marked
# `imm_symbolic`; where it refuses, the reference's own words go on the
# cell as `imm_symbolic_refusal` and the cell keeps the row task ap4
# ran.  NO EXISTING ROW IS TOUCHED: the lane proves that by comparing
# the two files row for row on every field.
#
#  [1] the read, and the outer set re-counted.
#  [2] the symbolic rows built, one line each.
#  [3] the write, and the two files compared row for row.
#  [4] the driver asked which row it now chooses at each imm_* cell.
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_AP5.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
python3 - <<'PY'
import copy
import json
import os
import resource
import sys

HERE = "PseudoCoupHQ/Research/oracle/cross_construction/emulation"
sys.path.insert(0, os.path.join(HERE, "handful"))
sys.path.insert(0, os.path.join(HERE, "autopoly"))
sys.path.insert(0, HERE)
import handful as H
import model_table as MTAB
import model_translate as MT
import autopoly5 as A

ABORT_KB = 6 * 1024 * 1024


def guard(where):
    got = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if got > ABORT_KB:
        raise SystemExit("ABORT_MEMORY_AP5: %d kB at %s" % (got, where))
    print("   peak resident at %s: %d kB" % (where, got))


A.use_task_ap5()
MTAB._install_gpr_widths()
AP4 = os.path.join(A.HERE, "autopoly4_cells.json")
print("[1/4] the read")
before = A.read_json(AP4)
print("   %s: %d cells" % (AP4, len(before["asked"])))
total = sum(r["attested_ledger_rows"] for r in before["asked"])
print("   attested ledger rows over the outer set: %d" % total)
after = copy.deepcopy(before)
guard("the read")

# THE SPELLING, and it is `model_translate.shapes_for`'s own.  A shape
# whose first operand is an immediate is spelled a second time with
# GPR_C at the operand's own width; the shape's NAME is the one
# `shapes_for` lists for it, so the row says what it is.
SYMBOLIC_NAME = {
    "imm_gpr": "imm_symbolic_gpr",
    "imm_gpr_gpr": "imm_symbolic_gpr_gpr",
    "imm_xmm_gpr": "imm_symbolic_xmm_gpr",
    "imm_gpr_xmm": "imm_symbolic_gpr_xmm",
}

print("")
print("[2/4] the symbolic rows")
built = 0
refused = 0
for record in after["asked"]:
    asked = record["asked"]
    if not (asked.get("shape") or "").startswith("imm"):
        continue
    held = {}
    row = H.chosen_row(after, (asked["mnem"], asked["shape"],
                               asked["key_width"]), held)
    if row is None:
        record["imm_symbolic_refusal"] = "no TRANSLATED row at this cell"
        refused = refused + 1
        print("   `%-8s %-12s %-4s  no TRANSLATED row at this cell"
              % (asked["mnem"] + "`", asked["shape"], asked["key_width"]))
        continue
    operands = list(row.get("operands") or [])
    width = row.get("width")
    name = SYMBOLIC_NAME.get(asked["shape"])
    if not operands or not operands[0].startswith("$") or name is None \
            or width not in MT.GPR_C:
        record["imm_symbolic_refusal"] = (
            "this cell's chosen row has no immediate in its first "
            "operand slot, or its shape is not one `shapes_for` "
            "spells a symbolic immediate for")
        refused = refused + 1
        print("   `%-8s %-12s %-4s  %s"
              % (asked["mnem"] + "`", asked["shape"], asked["key_width"],
                 record["imm_symbolic_refusal"]))
        continue
    operands[0] = MT.GPR_C[width]
    attempt = {"mnem": row["mnem"], "operands": operands,
               "preseeded": row.get("preseeded", False),
               "flags_in_setter": (row.get("flags_in") or {}).get("mnem"),
               "width": width}
    written, flags = MTAB.places_of_attempt(attempt)
    if written is None:
        record["imm_symbolic_refusal"] = "%s" % flags
        refused = refused + 1
        print("   `%-8s %-12s %-4s  REFUSED %s"
              % (asked["mnem"] + "`", asked["shape"], asked["key_width"],
                 flags))
        continue
    new = copy.deepcopy(row)
    new["operands"] = operands
    new["shape"] = name
    new["text"] = "%s %s" % (row["mnem"], ",".join(operands))
    new["row_id"] = "%s_imm_symbolic" % row["row_id"]
    new["imm_symbolic"] = True
    record["rows"].append(new)
    built = built + 1
    print("   `%-8s %-12s %-4s  `%s` -> `%s`   places %s"
          % (asked["mnem"] + "`", asked["shape"], asked["key_width"],
             row.get("text"), new["text"],
             sorted(written) + (["flags"] if flags is not None else [])))
print("")
print("   symbolic rows built: %d" % built)
print("   imm_* cells with no symbolic row: %d" % refused)
guard("section 2")

print("")
print("[3/4] the write, and the two files compared row for row")
A.write_json(A.CELLS, after)
print("   wrote %s" % A.CELLS)
written_back = A.read_json(A.CELLS)
print("   cells on the new file: %d" % len(written_back["asked"]))
print("   attested ledger rows on the new file: %d"
      % sum(r["attested_ledger_rows"] for r in written_back["asked"]))
moved = []
added = 0
old_index = {}
for record in before["asked"]:
    key = (record["asked"]["mnem"], record["asked"]["shape"],
           record["asked"]["key_width"])
    old_index[key] = record
for record in written_back["asked"]:
    key = (record["asked"]["mnem"], record["asked"]["shape"],
           record["asked"]["key_width"])
    was = old_index.get(key)
    if was is None:
        moved.append("%s is on the new file and not the old" % (key,))
        continue
    old_rows = {r["row_id"]: r for r in was["rows"]}
    for row in record["rows"]:
        if row.get("imm_symbolic"):
            added = added + 1
            continue
        twin = old_rows.get(row["row_id"])
        if twin is None:
            moved.append("%s row %s is new and not symbolic"
                         % (key, row["row_id"]))
            continue
        if json.dumps(twin, sort_keys=True) != json.dumps(
                row, sort_keys=True):
            moved.append("%s row %s differs" % (key, row["row_id"]))
print("   rows added, all of them symbolic: %d" % added)
print("   existing rows that differ in ANY field: %d" % len(moved))
for line in moved[:20]:
    print("      %s" % line)
print("   cells on the old file that are not on the new: %d"
      % len([k for k in old_index
             if k not in [(r["asked"]["mnem"], r["asked"]["shape"],
                           r["asked"]["key_width"])
                          for r in written_back["asked"]]]))
guard("section 3")

print("")
print("[4/4] the row the driver now chooses at each imm_* cell")
for record in written_back["asked"]:
    asked = record["asked"]
    if not (asked.get("shape") or "").startswith("imm"):
        continue
    held = {}
    row = H.chosen_row(written_back, (asked["mnem"], asked["shape"],
                                      asked["key_width"]), held)
    print("   `%-8s %-12s %-4s  row %-24s line %-22r  %s"
          % (asked["mnem"] + "`", asked["shape"], asked["key_width"],
             (row or {}).get("row_id"), (row or {}).get("text"),
             held.get("chosen_by")))
guard("section 4")
print("done")
PY
