#!/usr/bin/env bash
# ap5_l3_probe_the_symbolic_row_properly.sh -- task ap5: the THIRD
# probe, and it is lane ap5_l2 asked again with two defects of ap5_l2's
# own corrected.  ap5_l2 ran every spelling on a FRESH state and
# compared only the written REGISTER places, so
#   * `sbb` and `adc`, whose rows the sweep marked `preseeded`, refused
#     for want of an arriving flag state -- a defect of the probe, not
#     a fact about the spelling; and
#   * `cmp` and `test`, which write no register place at all, printed
#     an EMPTY verdict and were counted as disagreeing.
# This lane builds both spellings through `model_table.places_of_attempt`
# on the row's OWN state (its `preseeded` flag and its own
# `flags_in` setter), and compares every written place AND the flag
# triple.
#
#  [1] every imm_* cell of the outer set, both spellings, the outcome.
#  [2] z3 asked, per place and for the flag pair: the symbolic term
#      with the sweep's own literal substituted for the symbol IS the
#      literal row's term.
#  [3] the arrival families each spelling gives, so what the alignment
#      will be handed is known before it is handed.
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_AP5.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
python3 - <<'PY'
import json
import os
import resource
import sys

HERE = "PseudoCoupHQ/Research/oracle/cross_construction/emulation"
sys.path.insert(0, os.path.join(HERE, "handful"))
sys.path.insert(0, os.path.join(HERE, "autopoly"))
sys.path.insert(0, HERE)
import z3
import emulate as E
import handful as H
import reference as R
import model_table as MTAB
import model_translate as MT
import autopoly4 as A

ABORT_KB = 6 * 1024 * 1024


def guard(where):
    got = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if got > ABORT_KB:
        raise SystemExit("ABORT_MEMORY_AP5: %d kB at %s" % (got, where))
    print("   peak resident at %s: %d kB" % (where, got))


A.use_task_ap4()
MTAB._install_gpr_widths()
cells = A.read_json(A.CELLS)
imm_cells = [c for c in cells["asked"]
             if (c["asked"].get("shape") or "").startswith("imm")]
imm_cells.sort(key=lambda c: -c["attested_ledger_rows"])
print("imm_* cells on the outer set: %d" % len(imm_cells))


def chosen(cell):
    """the row the driver itself would choose for this cell."""
    held = {}
    return H.chosen_row(cells, (cell["asked"]["mnem"],
                                cell["asked"]["shape"],
                                cell["asked"]["key_width"]), held), held


def symbolic_operands(operands, width):
    if not operands or not operands[0].startswith("$"):
        return None
    out = list(operands)
    out[0] = MT.GPR_C[width]
    return out


def attempt_of(row, operands):
    return {"mnem": row["mnem"], "operands": operands,
            "preseeded": row.get("preseeded", False),
            "flags_in_setter": (row.get("flags_in") or {}).get("mnem"),
            "width": row.get("width")}


def as_pair(flags):
    if flags is None:
        return None
    return z3.Concat(MT.as_bits(flags[1]), MT.as_bits(flags[2]))


print("")
print("[1/3] BOTH SPELLINGS, on the row's own state")
print("| mnem | shape | key_width | the literal line | the symbolic "
      "line | the reference's answer |")
print("|---|---|---|---|---|---|")
reached = []
refused = []
for cell in imm_cells:
    asked = cell["asked"]
    row, _held = chosen(cell)
    if row is None:
        continue
    width = row.get("width")
    operands = symbolic_operands(row.get("operands") or [], width)
    literal_line = "%s %s" % (row["mnem"], ",".join(row["operands"]))
    if operands is None:
        print("| `%s` | %s | %s | `%s` | -- | the first operand is not "
              "an immediate |"
              % (asked["mnem"], asked["shape"], asked["key_width"],
                 literal_line))
        continue
    symbolic_line = "%s %s" % (row["mnem"], ",".join(operands))
    written, flags = MTAB.places_of_attempt(attempt_of(row, operands))
    if written is None:
        said = "%s" % flags
        refused.append((cell, row, said))
    else:
        places = sorted(written) + (["flags"] if flags is not None
                                    else [])
        said = "TRANSLATED: %s" % (places or "no place")
        reached.append((cell, row, operands))
    print("| `%s` | %s | %s | `%s` | `%s` | %s |"
          % (asked["mnem"], asked["shape"], asked["key_width"],
             literal_line, symbolic_line, said))
print("")
print("   imm_* cells the symbolic spelling reaches: %d" % len(reached))
print("   imm_* cells the reference refuses it for: %d" % len(refused))
for cell, row, said in refused:
    print("      `%s` %s %s -- %s"
          % (cell["asked"]["mnem"], cell["asked"]["shape"],
             cell["asked"]["key_width"], said))
guard("section 1")

print("")
print("[2/3] z3: the symbolic term at the sweep's own literal IS the")
print("      literal row's term -- every written place and the flags")
agreed = []
disagreed = []
for cell, row, operands in reached:
    left_written, left_flags = MTAB.places_of_attempt(
        attempt_of(row, row["operands"]))
    right_written, right_flags = MTAB.places_of_attempt(
        attempt_of(row, operands))
    value = int(R.IMMEDIATE_RE.match(row["operands"][0]).group(1), 0)
    family = R.canon.FAMILY_OF[operands[0][1:]]
    seed = z3.BitVec("seed_%s" % family, 64)
    fixed = z3.BitVecVal(value, 64)
    verdict = []
    every = sorted(set(left_written) | set(right_written))
    pairs = [(name, left_written.get(name), right_written.get(name))
             for name in every]
    pairs.append(("flags", as_pair(left_flags), as_pair(right_flags)))
    for name, left, right in pairs:
        if left is None and right is None:
            continue
        if left is None or right is None:
            verdict.append("%s: only one spelling writes it" % name)
            continue
        put = z3.simplify(z3.substitute(right, (seed, fixed)))
        if left.size() != put.size():
            verdict.append("%s: %d bits against %d"
                           % (name, left.size(), put.size()))
            continue
        solver = z3.Solver()
        solver.set("timeout", 20000)
        solver.add(left != put)
        verdict.append("%s: %s" % (name, solver.check()))
    line = "; ".join(verdict)
    if verdict and all(v.endswith(": unsat") for v in verdict):
        agreed.append(cell)
    else:
        disagreed.append((cell, line))
    print("   `%-8s %-12s %-4s  %s"
          % (cell["asked"]["mnem"] + "`", cell["asked"]["shape"],
             cell["asked"]["key_width"], line))
print("")
print("   cells where every place agrees under the substitution: "
      "%d of %d" % (len(agreed), len(reached)))
for cell, line in disagreed:
    print("      DISAGREES `%s` %s %s -- %s"
          % (cell["asked"]["mnem"], cell["asked"]["shape"],
             cell["asked"]["key_width"], line))
guard("section 2")

print("")
print("[3/3] THE ARRIVAL FAMILIES each spelling gives")
for cell, row, operands in reached:
    left_written, left_flags = MTAB.places_of_attempt(
        attempt_of(row, row["operands"]))
    right_written, right_flags = MTAB.places_of_attempt(
        attempt_of(row, operands))
    said = []
    for label, written, flags in [("literal", left_written, left_flags),
                                  ("symbolic", right_written,
                                   right_flags)]:
        names = []
        for name in sorted(written):
            try:
                names.append("%s%s" % (name,
                                       H.families_of(written[name])))
            except Exception as problem:
                names.append("%s<%s>" % (name, type(problem).__name__))
        said.append("%s %s" % (label, "; ".join(names) or "no register "
                               "place"))
    print("   `%-8s %-12s %-4s  %s"
          % (cell["asked"]["mnem"] + "`", cell["asked"]["shape"],
             cell["asked"]["key_width"], "   ||   ".join(said)))
guard("section 3")
print("done")
PY
