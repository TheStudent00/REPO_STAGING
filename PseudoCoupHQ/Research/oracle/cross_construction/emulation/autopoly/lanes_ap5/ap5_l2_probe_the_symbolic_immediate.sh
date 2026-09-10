#!/usr/bin/env bash
# ap5_l2_probe_the_symbolic_immediate.sh -- task ap5: the SECOND probe.
# Nothing of section 2 is written until this lands.  It asks, of the
# objects and never of a reading:
#
#  [1] WHAT A SYMBOLIC IMMEDIATE CAN BE.  `reference.Operands.read_text`
#      reads an immediate operand as a `BitVecVal` of the operand's own
#      width and a REGISTER operand as that register's symbol cut to the
#      same width -- so within the reference's own model the two differ
#      only in whether the value is a literal.  This section spells each
#      imm_* shape a second time with a register in the immediate's slot
#      and asks the reference for the term, mnemonic by mnemonic over
#      the outer set's own 27 imm_* cells.
#  [2] THE PROOF THAT THE TWO SPELLINGS ARE ONE MAPPING: z3 is asked
#      whether the symbolic term with the sweep's own literal
#      substituted for the symbol IS the literal row's term.  A cell
#      where z3 does not say so is printed and is not carried.
#  [3] THE ROUTE each imm_* run took on task ap4's store, per target,
#      so what changing the cell's term would move is known before it
#      is moved.
#  [4] THE CORPUS'S OWN IMMEDIATES: where the rows that attest an imm_*
#      cell are held, and the distinct immediate constants they spell.
#  [5] THE DEFINITIONS: whether a symbolic row's Lean body is one the
#      model already holds, which is what decides whether the
#      `check_L2` guard can move.
#
# MEMORY BOUND: 6 GB resident on this one process, named abort
# ABORT_MEMORY_AP5.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
python3 - <<'PY'
import json
import os
import re
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
runs = A.read_runs(A.RUNS)
imm_cells = [c for c in cells["asked"]
             if (c["asked"].get("shape") or "").startswith("imm")]
imm_cells.sort(key=lambda c: -c["attested_ledger_rows"])
print("imm_* cells on the outer set: %d" % len(imm_cells))
guard("the two reads")

# THE SPARE REGISTER.  `model_translate.GPR_C` is spelled in that file
# and used by no shape it lists, so the symbolic spelling takes it and
# collides with no existing spelling.
print("")
print("[1/5] THE SYMBOLIC SPELLING, and what the reference does with it")
print("   model_translate.GPR_C, LITERAL: %s" % json.dumps(MT.GPR_C))


def symbolic_texts(shape, texts, width):
    """the same operand list with a REGISTER of the operand's own width
    in the immediate's slot -- the immediate slot being the first, which
    is what every imm_* shape `shapes_for` spells has."""
    if not texts:
        return None
    if not texts[0].startswith("$"):
        return None
    out = list(texts)
    out[0] = MT.GPR_C[width]
    return out


def a_row_of(cell):
    for row in cell["rows"]:
        if row.get("outcome") == "TRANSLATED":
            return row
    return None


def operand_width(row):
    """the width the sweep spelled this row's operands at -- the row's
    own `width`, which is the loop label and is what GPR_C must match."""
    return row.get("width")


ok = []
refused = []
print("")
print("| mnem | shape | key_width | the literal line | the symbolic line "
      "| the reference's answer |")
print("|---|---|---|---|---|---|")
for cell in imm_cells:
    asked = cell["asked"]
    row = a_row_of(cell)
    if row is None:
        continue
    width = operand_width(row)
    texts = symbolic_texts(asked["shape"], row.get("operands") or [],
                           width)
    literal_line = "%s %s" % (row["mnem"], ",".join(row["operands"]))
    if texts is None:
        print("| `%s` | %s | %s | `%s` | -- | the first operand is not an "
              "immediate |"
              % (asked["mnem"], asked["shape"], asked["key_width"],
                 literal_line))
        continue
    symbolic_line = "%s %s" % (row["mnem"], ",".join(texts))
    try:
        written, flags, _state, line = MT.run_line(row["mnem"], texts)
        said = "TRANSLATED: %d place(s) %s" % (
            len(written), sorted(written))
        ok.append((cell, row, width, texts))
    except Exception as problem:
        said = "%s: %s" % (type(problem).__name__, problem)
        refused.append((cell, row, width, texts, said))
    print("| `%s` | %s | %s | `%s` | `%s` | %s |"
          % (asked["mnem"], asked["shape"], asked["key_width"],
             literal_line, symbolic_line, said))
print("")
print("   imm_* cells the symbolic spelling reaches: %d" % len(ok))
print("   imm_* cells the reference refuses it for: %d" % len(refused))
for cell, row, width, texts, said in refused:
    print("      `%s` %s %s -- %s"
          % (cell["asked"]["mnem"], cell["asked"]["shape"],
             cell["asked"]["key_width"], said))
guard("section 1")

print("")
print("[2/5] THE PROOF THAT THE TWO SPELLINGS ARE ONE MAPPING")
print("   z3 is asked: the symbolic term, with the sweep's own literal")
print("   substituted for the symbol, IS the literal row's term.")
agreed = 0
disagreed = []
for cell, row, width, texts in ok:
    literal_written, _f, _s, _l = MT.run_line(row["mnem"],
                                              row["operands"])
    symbolic_written, _f, _s, _l = MT.run_line(row["mnem"], texts)
    value = int(R.IMMEDIATE_RE.match(row["operands"][0]).group(1), 0)
    family = R.canon.FAMILY_OF[texts[0][1:]]
    seed = z3.BitVec("seed_%s" % family, 64)
    fixed = z3.BitVecVal(value, 64)
    places = sorted(set(literal_written) | set(symbolic_written))
    verdict = []
    for place in places:
        left = literal_written.get(place)
        right = symbolic_written.get(place)
        if left is None or right is None:
            verdict.append("%s: only one side writes it" % place)
            continue
        put = z3.simplify(z3.substitute(right, (seed, fixed)))
        solver = z3.Solver()
        solver.set("timeout", 10000)
        solver.add(left != put)
        answer = solver.check()
        verdict.append("%s: %s" % (place, answer))
    line = "; ".join(verdict)
    if all(v.endswith(": unsat") for v in verdict) and verdict:
        agreed = agreed + 1
    else:
        disagreed.append((cell, line))
    print("   `%-8s %-12s %-4s  %s"
          % (cell["asked"]["mnem"] + "`", cell["asked"]["shape"],
             cell["asked"]["key_width"], line))
print("")
print("   cells where every written place agrees under the "
      "substitution: %d of %d" % (agreed, len(ok)))
for cell, line in disagreed:
    print("      DISAGREES `%s` %s %s -- %s"
          % (cell["asked"]["mnem"], cell["asked"]["shape"],
             cell["asked"]["key_width"], line))
guard("section 2")

print("")
print("[3/5] THE ROUTE each imm_* run took on task ap4's store")
route = {}
for run in runs:
    if not (run.get("shape") or "").startswith("imm"):
        continue
    route[(run["mnem"], run["shape"], run["key_width"],
           run["lang"])] = (A.route_of(run), A.outcome_of(run))
print("| mnem | shape | key_width | c | rust | go | swift |")
print("|---|---|---|---|---|---|---|")
for cell in imm_cells:
    asked = cell["asked"]
    key = (asked["mnem"], asked["shape"], asked["key_width"])
    said = []
    for lang in ["c", "rust", "go", "swift"]:
        got = route.get(key + (lang,))
        said.append("--" if got is None else "%s / %s" % got)
    print("| `%s` | %s | %s | %s |"
          % (key[0], key[1], key[2], " | ".join(said)))
tally = {}
for key in route:
    tally[route[key][0]] = tally.get(route[key][0], 0) + 1
print("")
print("   the imm_* runs by route: %s" % json.dumps(tally, sort_keys=True))
guard("section 3")

print("")
print("[4/5] THE CORPUS'S OWN IMMEDIATES")
rows_path = ("PseudoCoupHQ/Research/oracle/arch_opcodes/model/"
             "model_table_rows.json")
print("   %s" % rows_path)
table_rows = A.read_json(rows_path)
print("   type: %s" % type(table_rows).__name__)
if isinstance(table_rows, dict):
    print("   keys: %s" % sorted(table_rows)[:10])
    sample = table_rows.get("rows") or table_rows.get("asked")
else:
    sample = table_rows
if isinstance(sample, list) and sample:
    print("   entries: %d" % len(sample))
    print("   one entry's keys: %s" % sorted(sample[0]))
    print("   one entry, LITERAL: %s"
          % json.dumps(sample[0], sort_keys=True)[:900])
guard("section 4a")

print("")
print("   the single-opcode rows that classify to an imm_* cell, per")
print("   language, with their own body text -- this is what the")
print("   primitive route matches and where the baked-in immediate is")
for key in [("mov", "imm_gpr", 32), ("mov", "imm_gpr", 8),
            ("xor", "imm_gpr", 8), ("shl", "imm_gpr", 32)]:
    for lang in ["c", "rust", "go", "swift"]:
        found = H.primitive_lookup({"mnem": key[0], "shape": key[1],
                                    "key_width": key[2]}, lang)
        chosen = found.get("row")
        print("   `%s` %s %s / %-5s  rows %d  chosen %s"
              % (key[0], key[1], key[2], lang,
                 found.get("rows_that_classify_to_this_cell", 0),
                 "--" if chosen is None
                 else repr(chosen.get("body_text"))))
guard("section 4b")

print("")
print("   every DISTINCT immediate the corpus's single-opcode rows")
print("   spell at each imm_* cell, over the four languages")
IMM = re.compile(r"\$(-?(?:0x[0-9a-fA-F]+|\d+))")
for cell in imm_cells:
    asked = cell["asked"]
    seen = {}
    for lang in ["c", "rust", "go", "swift"]:
        found = H.primitive_lookup({"mnem": asked["mnem"],
                                    "shape": asked["shape"],
                                    "key_width": asked["key_width"]},
                                   lang)
        for row in found.get("candidate_rows") or []:
            for hit in IMM.findall(row.get("body_text") or ""):
                seen[hit] = seen.get(hit, 0) + 1
    print("   `%-8s %-12s %-4s  distinct immediates: %s"
          % (asked["mnem"] + "`", asked["shape"], asked["key_width"],
             json.dumps(sorted(seen), sort_keys=True)))
guard("section 4c")

print("")
print("[5/5] THE DEFINITIONS: is a symbolic row's mapping one the model")
print("      already holds?  `add_definition` is asked for the literal")
print("      spelling, the register spelling `shapes_for` already has,")
print("      and the symbolic spelling, in that order, on one Model.")
model = MT.Model()
before = 0
for cell, row, width, texts in ok[:8]:
    names = []
    for label, spelling in [("literal", row["operands"]),
                            ("symbolic", texts)]:
        written, flags, _s, line = MT.run_line(row["mnem"], spelling)
        for place in sorted(written):
            translated = MT.translate_term(written[place])
            if translated["refused"] is not None:
                names.append("%s/%s refused" % (label, place))
                continue
            name = MT.add_definition(model, row["mnem"], translated,
                                     note=line)
            names.append("%s/%s -> %s" % (label, place, name))
    print("   `%-8s %-12s %-4s  %s"
          % (cell["asked"]["mnem"] + "`", cell["asked"]["shape"],
             cell["asked"]["key_width"], "; ".join(names)))
print("   definitions on this scratch model: %d" % len(model.definitions))
guard("section 5")
print("done")
PY
