#!/usr/bin/env bash
# ap5_l1_probe_the_two_remainders.sh -- task ap5: the FIRST probe, and
# nothing is written against it until it has landed.  It asks the two
# populations this task is about, off task ap4's own store and off the
# cells file, and it asks the objects rather than the log:
#
#  [1] THE x87 POPULATION as task ap4 left it: every run whose cause is
#      `answer home or arrival on the x87 stack`, by target and by
#      cell, with its attested ledger rows; and, separately, every cell
#      whose `key_width` is 80 with its four outcomes, so "the 30 x87 c
#      cells" can be counted rather than quoted.
#  [2] THE TWO SHARED READINGS the brief authorises: what
#      `reference.answer_of` does with an x87 answer home today, and
#      what `pool100_entry_equivalence.align_by_row` does with an x87
#      arrival today, each asked directly and its raising quoted.
#  [3] THE imm_* POPULATION: every cell of the outer set whose shape
#      begins `imm`, with the row's own line, the attested ledger rows,
#      and task ap4's four verdicts; then the term of every written
#      place for the most attested of them.
#  [4] THE IMMEDIATE AS THE REFERENCE READS IT: `Operands.read_text`'s
#      immediate branch LITERAL, and every builder in the table that
#      branches on `is_immediate`, so what a SYMBOLIC immediate would
#      have to be is read off the reference and not invented.
#
# MEMORY BOUND: 6 GB resident on this one process, named abort
# ABORT_MEMORY_AP5, checked after each section.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
python3 - <<'PY'
import inspect
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
import pool100_entry_equivalence as P100
import model_table as MTAB
import model_translate as MT
import autopoly4 as A

ABORT_KB = 6 * 1024 * 1024


def peak():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def guard(where):
    got = peak()
    if got > ABORT_KB:
        raise SystemExit("ABORT_MEMORY_AP5: %d kB at %s" % (got, where))
    print("   peak resident at %s: %d kB" % (where, got))


A.use_task_ap4()
MTAB._install_gpr_widths()
cells = A.read_json(A.CELLS)
runs = A.read_runs(A.RUNS)
print("cells on the outer set: %d" % len(cells["asked"]))
print("runs on task ap4's store: %d" % len(runs))
guard("the two reads")

print("")
print("[1/4] THE x87 POPULATION, off task ap4's own store")
by_target = {}
by_cell = {}
rows_of = {}
total = 0
for run in runs:
    if A.cause_of(run) != E.CAUSE_X87:
        continue
    total = total + 1
    by_target[run["lang"]] = by_target.get(run["lang"], 0) + 1
    key = (run["mnem"], run["shape"], run["key_width"])
    by_cell[key] = by_cell.get(key, 0) + 1
    rows_of[key] = run.get("attested_ledger_rows") or 0
print("   runs carrying the x87 cause: %d" % total)
print("   distinct cells: %d" % len(by_cell))
print("   their attested ledger rows, counted ONCE per cell: %d"
      % sum(rows_of.values()))
print("   the same rows counted once per run: %d"
      % sum(rows_of[(r["mnem"], r["shape"], r["key_width"])]
            for r in runs if A.cause_of(r) == E.CAUSE_X87))
for lang in sorted(by_target):
    print("      %-6s %d" % (lang, by_target[lang]))

print("")
print("   EVERY CELL WHOSE key_width IS 80, with its four outcomes")
x87_cells = [c for c in cells["asked"]
             if c["asked"].get("key_width") == 80]
print("   cells at key_width 80: %d" % len(x87_cells))
outcome = {}
for run in runs:
    if run.get("key_width") != 80:
        continue
    outcome[(run["mnem"], run["shape"], run["lang"])] = A.outcome_of(run)
tally = {}
for key in outcome:
    tally[(key[2], outcome[key])] = tally.get((key[2], outcome[key]), 0) + 1
for key in sorted(tally):
    print("      %-6s %-30s %d" % (key[0], key[1], tally[key]))
proved_c = [k for k in outcome if k[2] == "c" and outcome[k] == "proved"]
print("   x87 cells PROVED on c: %d" % len(proved_c))
notproved_c = sorted(k for k in outcome if k[2] == "c"
                     and outcome[k] != "proved")
print("   x87 cells NOT proved on c: %d" % len(notproved_c))
for key in notproved_c:
    print("      `%s` %s 80  ->  %s" % (key[0], key[1], outcome[key]))
guard("section 1")

print("")
print("[2/4] THE TWO SHARED READINGS, asked directly")
print("   reference.Reference.answer_of, LITERAL:")
print(inspect.getsource(R.Reference.answer_of))
state = R.MachineState()
state.x87_push(z3.FP("seed_X87_1", R.X87_SORT))
state.x87_push(z3.FP("seed_X87_0", R.X87_SORT))
try:
    got = R.REFERENCE.answer_of(state, (E.X87_ANSWER_FAMILY, E.X87_BITS))
    print("   answer_of((X87_0, 79)) gave: %s" % got)
except Exception as problem:
    print("   answer_of((X87_0, 79)) raised %s: %s"
          % (type(problem).__name__, problem))
print("")
print("   pool100_entry_equivalence.align_by_row, LITERAL:")
print(inspect.getsource(P100.align_by_row))
print("   pool100_entry_equivalence.input_rows, LITERAL:")
print(inspect.getsource(P100.input_rows))
print("   pool100_entry_equivalence.family_bits, LITERAL:")
print(inspect.getsource(P100.family_bits))
term = z3.fpToIEEEBV(z3.FP("seed_X87_0", R.X87_SORT)
                     * z3.FP("seed_X87_1", R.X87_SORT))
rows = P100.input_rows(["X87_0", "X87_1"])
print("   input_rows(['X87_0','X87_1']) = %s" % json.dumps(rows))
print("   the term, LITERAL: %s" % term)
try:
    got = P100.align_by_row(term, rows)
    print("   align_by_row over an x87 term gave: %s" % got)
    print("   ...and its free symbols: %s"
          % [s.decl().name() for s in z3.z3util.get_vars(got)])
except Exception as problem:
    print("   align_by_row over an x87 term raised %s: %s"
          % (type(problem).__name__, problem))
guard("section 2")

print("")
print("[3/4] THE imm_* POPULATION of the outer set")
imm_cells = [c for c in cells["asked"]
             if (c["asked"].get("shape") or "").startswith("imm")]
print("   cells whose shape begins `imm`: %d" % len(imm_cells))
shapes = {}
for cell in imm_cells:
    name = cell["asked"]["shape"]
    shapes[name] = shapes.get(name, 0) + 1
for shape in sorted(shapes):
    print("      %-14s %d cells" % (shape, shapes[shape]))
print("")
verdict = {}
for run in runs:
    verdict[(run["mnem"], run["shape"], run["key_width"],
             run["lang"])] = A.outcome_of(run)
imm_keys = []
print("| mnem | shape | key_width | ledger rows | c | rust | go | swift |")
print("|---|---|---|---|---|---|---|---|")
for cell in sorted(imm_cells,
                   key=lambda c: -c["attested_ledger_rows"]):
    key = (cell["asked"]["mnem"], cell["asked"]["shape"],
           cell["asked"]["key_width"])
    imm_keys.append(key)
    print("| `%s` | %s | %s | %d | %s | %s | %s | %s |"
          % (key[0], key[1], key[2], cell["attested_ledger_rows"],
             verdict.get(key + ("c",), "--"),
             verdict.get(key + ("rust",), "--"),
             verdict.get(key + ("go",), "--"),
             verdict.get(key + ("swift",), "--")))
guard("section 3a")

print("")
print("   THE TERM OF EVERY WRITTEN PLACE, for the six most attested")
for key in imm_keys[:6]:
    held = H.cell_input(cells, key)
    print("   == `%s` %s %s   line %r"
          % (key[0], key[1], key[2], held.get("line")))
    if held.get("refusal_cause") is not None:
        print("      refused: %s" % held.get("refusal_cause"))
        continue
    for place in held.get("places") or []:
        print("      place %-14s bits %-5s families %s"
              % (place.get("writes"), place.get("bits"),
                 place.get("families")))
        print("         term, LITERAL: %s" % place.get("term"))
guard("section 3b")

print("")
print("   THE ATTESTATION of those six cells, as the cells file holds it")
for key in imm_keys[:6]:
    for cell in imm_cells:
        if (cell["asked"]["mnem"], cell["asked"]["shape"],
                cell["asked"]["key_width"]) != key:
            continue
        for row in cell["rows"]:
            if row.get("outcome") != "TRANSLATED":
                continue
            attest = row.get("attestation") or {}
            print("   == `%s` %s %s  row %s  operands %s"
                  % (key[0], key[1], key[2], row.get("row_id"),
                     row.get("operands")))
            print("      attestation keys: %s" % sorted(attest))
            for name in sorted(attest):
                value = attest[name]
                if isinstance(value, list):
                    print("         %-20s %s" % (name, value[:6]))
                else:
                    print("         %-20s %s" % (name, value))
            break
        break
guard("section 3c")

print("")
print("[4/4] THE IMMEDIATE AS THE REFERENCE READS IT")
print("   reference.Operands.read_text, LITERAL:")
print(inspect.getsource(R.Operands.read_text))
print("   reference.IMMEDIATE_RE, LITERAL: %s" % R.IMMEDIATE_RE.pattern)
print("")
print("   every builder in the reference that branches on is_immediate:")
source = inspect.getsource(R)
for match in re.finditer(r"\ndef (build_[a-z_0-9]+)\(", source):
    name = match.group(1)
    body = inspect.getsource(getattr(R, name))
    if "is_immediate" in body:
        print("      %s" % name)
print("")
print("   the sweep's own imm_* spellings, `model_translate.shapes_for`:")
for shape, texts in MT.shapes_for(32):
    if shape.startswith("imm"):
        print("      %-14s %s" % (shape, texts))
print("")
print("   THE SAME LINE, immediate against register, term for term")
for pair in [("mov", ["$0x3", "%edi"], ["%r8d", "%edi"]),
             ("add", ["$0x3", "%edi"], ["%r8d", "%edi"]),
             ("sar", ["$0x3", "%edi"], ["%cl", "%edi"]),
             ("shl", ["$0x3", "%edi"], ["%r8d", "%edi"])]:
    mnem, imm_texts, sym_texts = pair
    for texts in (imm_texts, sym_texts):
        try:
            written, flags, _state, line = MT.run_line(mnem, texts)
            said = []
            for place in sorted(written):
                said.append("%s = %s" % (place, written[place]))
            print("      %-28s -> %s" % (line, "; ".join(said) or "--"))
        except Exception as problem:
            print("      %-28s -> raised %s: %s"
                  % ("%s %s" % (mnem, ",".join(texts)),
                     type(problem).__name__, problem))
guard("section 4")
print("done")
PY
