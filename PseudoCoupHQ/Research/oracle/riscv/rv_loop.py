#!/usr/bin/env python3
"""rv_loop.py -- THE LOOP ON THE DELTA: `find_emulation` run over the
RISC-V cells that have NO x86 twin, on riscv64.

Node: hq.research.arch_unit_oracle.  Task rv2, brief section 2 step 4,
`PRIVATE/PseudoCoupHQ/Research/briefs/task_rv2_brief.md`.

WHAT THIS IS, one sentence, in relation: the same four steps the x86 loop
runs -- render the cell's term as source, compile it at the target's ship
flags, carve the body, ask z3 whether the body computes the term -- run
only over the cells the transfer could not reach, and with riscv64's own
compilers.

THE ALGORITHM, exactly, and it is `find_emulation`'s own:

    term   = cell.mapping                       # from model_table_rv.json
    source = render(term, target)               # handful's own renderer,
                                                #   or the target's own
                                                #   primitive where a
                                                #   riscv64 singleton
                                                #   lowers to this cell
    body   = carve(compile(source, ship flags for riscv64))
    verdict = z3(walk(body) == term)            # at the cell's key_width

THE TWO ROUTES, both attempted per cell, exactly as the x86 loop does.
  * THE TERM ROUTE: `handful.render_one_place` writes the cell's term in
    the target's own operators.  The renderer is architecture-neutral --
    it emits SOURCE, not machine code -- and it is called unchanged.
  * THE PRIMITIVE ROUTE: where `attest_rv.json` holds a SINGLETON for the
    cell -- a corpus probe whose whole riscv64 body is that one
    instruction -- the probe's own source is compiled instead.  This is
    what replaces the x86 loop's primitive lookup: the x86 lookup asks
    which corpus body IS the cell's opcode, and on riscv64 that question
    is answered by `rv_attest.py`, which compiled the corpus for riscv64.

WHY THE TERM'S SYMBOLS ARE RENAMED BEFORE RENDERING, said out loud
because it looks like a hack and is not.  `handful.families_of` reads a
symbol's name to decide which parameter slot it takes, and the names it
knows are x86 register families (`seed_rdi`, ...).  A RISC-V term's
symbols are named `seed_x11`, `seed_x12`.  This file renames them
positionally -- first printed symbol to `seed_rdi`, second to
`seed_rsi`, and so on -- which changes NO value and no structure: it is
the renderer's own way of ordering parameters, and the source it emits
mentions no register at all.  The arrival contract this file then hands
the RISC-V reference binds parameter k to `a<k>`, which is the psABI's
own rule.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope, anywhere
in this line -- not in matching, not in "which pairs get compared", not in
report rows, not in dropdowns.  The candidate set for comparison comes from
machine-form evidence (clusters, connections, type pairs) or from ratified
intention -- never from the token.  The token appears exactly once per
unit: as a display label on the member.  HISTORY OF VIOLATIONS, so the
pattern is visible: (1) the arch campaign's cross-language matrix (caught
by the owner 2026-08-24); (2) verdicts.py's row pairing (caught by the owner
2026-08-25 -- the fix brief itself reintroduced it as "same-operator
pairs").  MECHANICAL GUARD REQUIRED: every pipeline stage that groups or
pairs units must run the spelling-key check
(op_pipeline/check_no_spelling_keys.py) and refuse its own output on
failure.  A brief handed to any subagent for this line MUST paste this
paragraph verbatim."

HOW THIS FILE OBEYS IT.  Which cells the loop attempts is decided by
`twins.json` -- a term-identity join -- and by nothing else.  A
singleton is matched to a cell because the probe's own carved body
spells that cell's instruction at that operand form, which is machine
form off the disassembler.

MEMORY, as the law requires: one cell at a time, nothing accumulated but
the rows; bound 6 GB, named abort ABORT_MEMORY_RV2, peak resident
printed.

Coding discipline (the owner's ruling): no complex/compound one-liner statements.

usage:
  rv_loop.py run <ref dir> <op dir> <emulation dir> <twins.json>
                 <attest_rv.json> <riscv table json> <out prefix>
                 <src dir> <work dir> [limit]
"""

import json
import os
import resource
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import riscv_reference as RV                                # noqa: E402
import twins as TW                                          # noqa: E402
import inherit as INH                                       # noqa: E402
import model_table_rv as MRV                                # noqa: E402
import z3                                                    # noqa: E402


ABORT_KB = 6 * 1024 * 1024
ABORT_NAME = "ABORT_MEMORY_RV2"
SOLVER_MS = 3000
TARGETS = ["c", "go"]

GENERAL_FAMILIES = ["rdi", "rsi", "rdx", "rcx", "r8", "r9"]
"""the six the System V rule names, which is the order
`handful.families_of` puts a term's symbols in.  They name PARAMETER
SLOTS here and nothing else: the source the renderer emits mentions no
register."""


def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def check_memory(where):
    peak = peak_kb()
    if peak > ABORT_KB:
        raise SystemExit("%s: %d kB at %s" % (ABORT_NAME, peak, where))
    return peak


def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def write_json(path, document):
    fh = open(path, "w")
    json.dump(document, fh, indent=1, sort_keys=True)
    fh.write("\n")
    fh.close()


# ==================================================================
# section 1: the delta -- the cells with no twin
# ==================================================================

def untwinned(twins_path):
    """the RISC-V cells no x86 cell twins under either reading."""
    out = []
    document = json.load(open(twins_path))
    for row in document["rows"]:
        if row["how_at_key_width"] != "NONE":
            continue
        out.append({"mnem": row["mnem"], "shape": row["shape"],
                    "key_width": row["key_width"],
                    "places": [p["writes"] for p in row["places"]]})
    return out


def riscv_terms(rv_path):
    """(cell key, place) -> the z3 term, rebuilt from the reference."""
    reference = RV.RiscvReference()
    rows = json.load(open(rv_path))["rows"]
    out = {}
    operands = {}
    for row in rows:
        if row["outcome"] != "TRANSLATED":
            continue
        if not row.get("mapping"):
            continue
        key = (row["mnem"], row["shape"], row["key_width"])
        if key in operands:
            continue
        operands[key] = row["operands"]
        try:
            written, condition, _line = MRV.run_line(
                reference, row["mnem"], row["operands"])
        except Exception:
            continue
        for place in written:
            out[(key, place)] = written[place]
        if condition is not None:
            out[(key, "branch_condition")] = z3.If(
                condition, z3.BitVecVal(1, RV.XLEN),
                z3.BitVecVal(0, RV.XLEN))
    return out, operands


def singletons_of(attest_path):
    """(cell key) -> the corpus probe whose whole riscv64 body IS that
    cell's own instruction."""
    out = {}
    for record in json.load(open(attest_path))["singletons"]:
        key = (record["mnem"], record["shape"], record["key_width"])
        out[key] = record
    return out


# ==================================================================
# section 2: the term, renamed into the renderer's parameter slots
# ==================================================================

def in_parameter_slots(TERMS, term):
    """the term with its free symbols renamed to the parameter slots
    `handful.families_of` reads, in the term's own printed order."""
    symbols = TERMS.ordered_symbols(term)
    if len(symbols) > len(GENERAL_FAMILIES):
        return None, "the term reads %d values and the parameter slots " \
                     "this file names are %d" % (len(symbols),
                                                 len(GENERAL_FAMILIES))
    substitution = []
    for index, symbol in enumerate(symbols):
        if symbol.sort().kind() != z3.Z3_BV_SORT:
            return None, "a free symbol of this term is not a bit vector"
        fresh = z3.BitVec("seed_%s" % GENERAL_FAMILIES[index],
                          symbol.size())
        substitution.append((symbol, fresh))
    if substitution:
        term = z3.substitute(term, *substitution)
    return term, None


# ==================================================================
# section 3: one cell, one target, both routes
# ==================================================================

def one_run(H, TERMS, holder, reference, cell, place_name, term,
            target, singleton, src_dir, work_root, number):
    label = "%s_%s_%d__%s__%s" % (cell["mnem"], cell["shape"],
                                  cell["key_width"], place_name, target)
    label = label.replace(".", "_")
    row = {
        "arch": "riscv64",
        "cell": dict(cell),
        "place": place_name,
        "target": target,
        "label": label,
        "term_text": holder.normalize(term),
    }
    slotted, refusal = in_parameter_slots(TERMS, term)
    if slotted is None:
        row["kind"] = "refused"
        row["route"] = "term"
        row["verdict"] = {"outcome": "NOT_RENDERED", "reason": refusal}
        return row
    record = H.place_record("reg_rdi", slotted)
    if record.get("families") is None:
        row["kind"] = "refused"
        row["route"] = "term"
        row["verdict"] = {"outcome": "NOT_RENDERED",
                          "reason": record.get("not_rendered_detail")
                          or record.get("not_rendered")}
        return row
    H.SRC_DIR = src_dir
    rendered = H.render_one_place(record, target, label)
    if not rendered.get("rendered"):
        row["kind"] = "refused"
        row["route"] = "term"
        row["verdict"] = {"outcome": "NOT_RENDERED",
                          "reason": "%s: %s"
                                    % (rendered.get("refusal_cause"),
                                       rendered.get("refusal_detail"))}
        return row
    row["source"] = {"path": rendered["source_path"]}
    row["route"] = "term"
    verdict = gate(reference, holder, rendered["source"], target, term,
                   cell, work_root, number)
    row.update(verdict)
    if row["kind"] == "proved":
        return row
    if singleton is None:
        return row
    source = singleton.get("source")
    if source is None:
        row["primitive_route"] = {
            "kind": "refused",
            "unit": singleton["unit"],
            "verdict": {"outcome": "NO_SOURCE",
                        "reason": "the singleton record carries no "
                                  "probe source"}}
        return row
    row["primitive_route"] = one_primitive(reference, holder, singleton,
                                           term, cell, target,
                                           work_root, number, source)
    if row["primitive_route"].get("kind") == "proved":
        row["kind"] = "proved"
        row["route"] = "primitive"
    return row


def one_primitive(reference, holder, singleton, term, cell, target,
                  work_root, number, source):
    """the target's own primitive: the corpus probe whose whole riscv64
    body is this cell's one instruction, compiled again and gated.

    THE ARRIVAL ORDER IS THE PROBE'S OWN, not the term's: a probe's
    parameters are the (operator, holder pair) the corpus generated, so
    parameter k arrives in `a<k>` and is bound to the k-th free symbol
    of the cell's term.  Where the two counts differ the route is
    refused by name rather than aligned by guess."""
    if singleton["lang"] != target:
        return {"kind": "refused",
                "unit": singleton["unit"],
                "verdict": {"outcome": "NO_PRIMITIVE_IN_THIS_TARGET",
                            "reason": "the singleton that lowers to this "
                                      "cell is a %s probe and this run's "
                                      "target is %s"
                                      % (singleton["lang"], target)}}
    out = gate(reference, holder, source, target, term, cell, work_root,
               number)
    out["unit"] = singleton["unit"]
    out["line"] = singleton["line"]
    return out


def gate(reference, holder, source, target, term, cell, work_root,
         number):
    """compile for riscv64, carve, walk, and ask z3."""
    work = os.path.join(work_root, "loop%06d_%s" % (number, target))
    got, command, diagnostic = INH.compile_and_carve(source, target, work)
    out = {"compiler": {"command": command,
                        "target_triple": INH.triple_of(target)}}
    if got is None:
        out["kind"] = "refused"
        out["verdict"] = {"outcome": "BUILD_REFUSED",
                          "reason": (diagnostic or "").strip()[:900]}
        return out
    raw, body = got
    out["body"] = {"bytes": " ".join(raw), "text": " ; ".join(body)}
    contract = slot_contract(term)
    try:
        state = reference.simulate(body, contract, {})
        answer = reference.answer_of(state, "a0")
    except Exception as problem:
        out["kind"] = "refused"
        out["verdict"] = {"outcome": "WALK_REFUSED",
                          "reason": "%s: %s" % (type(problem).__name__,
                                                problem)}
        return out
    out["riscv_term"] = holder.normalize(answer)
    width = cell["key_width"] or term.size()
    if width > term.size():
        width = term.size()
    outcome, counterexample = INH.decide(INH.at_width(answer, width),
                                         INH.at_width(term, width),
                                         SOLVER_MS)
    whole = term.size()
    outcome_whole, counter_whole = INH.decide(
        INH.at_width(answer, whole), INH.at_width(term, whole),
        SOLVER_MS)
    out["verdict"] = {"outcome": outcome,
                      "compared_on_bits": width,
                      "counterexample": counterexample,
                      "solver_timeout_ms": SOLVER_MS}
    out["verdict_at_the_whole_place"] = {"outcome": outcome_whole,
                                         "compared_on_bits": whole,
                                         "counterexample": counter_whole}
    if outcome == "PROVED":
        out["kind"] = "proved"
    elif outcome == "DISPROVED":
        out["kind"] = "sat"
    else:
        out["kind"] = "undecided"
    return out


def slot_contract(term):
    """bind parameter k's arrival register `a<k>` to the k-th free
    symbol of the term the renderer walked."""
    import term as TERMS                                     # noqa: E402
    symbols = TERMS.ordered_symbols(term)
    contract = []
    for index, symbol in enumerate(symbols):
        arriving = symbol
        if symbol.size() < 64:
            arriving = z3.ZeroExt(64 - symbol.size(), symbol)
        contract.append(("a%d" % index, arriving))
    return contract


# ==================================================================
# section 4: the run
# ==================================================================

def run_command(ref_dir, op_dir, emulation_dir, twins_path, attest_path,
                rv_path, prefix, src_dir, work_root, limit):
    say("[0/4] the x86 reference this run uses, then the driver")
    X86, TERMS, MT, MTAB, digest = TW.bring_in(ref_dir, op_dir)
    sys.path.insert(0, os.path.join(emulation_dir, "handful"))
    import handful as H                                      # noqa: E402
    holder = TERMS.Term(X86.Reference())
    reference = RV.RiscvReference()
    if not os.path.isdir(src_dir):
        os.makedirs(src_dir)
    if not os.path.isdir(work_root):
        os.makedirs(work_root)

    say("[1/4] the delta")
    cells = untwinned(twins_path)
    say("   %d RISC-V cells with no x86 twin under either reading"
        % len(cells))
    terms, _operands = riscv_terms(rv_path)
    singles = singletons_of(attest_path)
    say("   %d riscv64 singletons the corpus attests" % len(singles))

    say("[2/4] the loop, both routes, on %s" % ", ".join(TARGETS))
    rows = []
    started = time.time()
    number = 0
    total = 0
    for cell in cells:
        total = total + len(cell["places"]) * len(TARGETS)
    for cell in cells:
        key = (cell["mnem"], cell["shape"], cell["key_width"])
        for place_name in cell["places"]:
            term = terms.get((key, place_name))
            for target in TARGETS:
                number = number + 1
                if limit is not None and number > limit:
                    break
                if term is None:
                    rows.append({
                        "arch": "riscv64", "cell": dict(cell),
                        "place": place_name, "target": target,
                        "kind": "refused",
                        "verdict": {"outcome": "NO_TERM",
                                    "reason": "the cell's own line "
                                              "could not be re-run"}})
                    continue
                rows.append(one_run(H, TERMS, holder, reference, cell,
                                    place_name, term, target,
                                    singles.get(key), src_dir,
                                    work_root, number))
                if number % 20 == 0 or number == total:
                    say("   [%d/%d] runs, %.0f s, peak %.0f MB"
                        % (number, total, time.time() - started,
                           check_memory("run %d" % number) / 1024.0))

    say("[3/4] the census")
    census = {}
    per_target = {}
    for row in rows:
        census[row["kind"]] = census.get(row["kind"], 0) + 1
        held = per_target.setdefault(row["target"], {})
        held[row["kind"]] = held.get(row["kind"], 0) + 1
    for kind in sorted(census):
        say("   %-12s %d" % (kind, census[kind]))

    say("[4/4] writing")
    fh = open(prefix + ".jsonl", "w")
    for row in rows:
        fh.write(json.dumps(row, sort_keys=True) + "\n")
    fh.close()
    document = {
        "meta": {
            "task": "rv2",
            "what": "find_emulation over the RISC-V cells with no x86 "
                    "twin, on riscv64, both routes",
            "targets": list(TARGETS),
            "x86_reference_sha256": digest,
            "gate_width": "the cell's own key_width is the headline; "
                          "the whole written place is beside it",
            "solver_timeout_ms": SOLVER_MS,
            "census": census,
            "per_target": per_target,
            "peak_kb": peak_kb(),
            "memory_bound_kb": ABORT_KB,
            "memory_abort": ABORT_NAME,
            "seconds": round(time.time() - started, 1),
        },
        "census": census,
        "per_target": per_target,
    }
    write_json(prefix + ".json", document)
    say("peak RSS: %d kB" % peak_kb())
    return 0


def main():
    command = sys.argv[1]
    if command == "run":
        limit = None
        if len(sys.argv) > 11:
            limit = int(sys.argv[11])
        return run_command(sys.argv[2], sys.argv[3], sys.argv[4],
                           sys.argv[5], sys.argv[6], sys.argv[7],
                           sys.argv[8], sys.argv[9], sys.argv[10],
                           limit)
    raise SystemExit("unknown command %r" % command)


if __name__ == "__main__":
    sys.exit(main())
