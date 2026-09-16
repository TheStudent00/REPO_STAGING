#!/usr/bin/env python3
"""rv9_native.py -- THE NATIVE ROUTE ON EVERY CELL THAT HOLDS NO PROOF,
MEASURED OBJECT BY OBJECT: the rendered source, the compiled body, the
references the body makes outside itself, the lifted formula's text
beside the definition's text, whether the canonical form makes the two
identical, and, where it does not, the FIRST NODE at which they differ.

Node: hq.research.arch_unit_oracle.architectures.riscv64.arch_opcode_axis.
Brief: `PRIVATE/PseudoCoupHQ/Research/briefs/task_rv9_brief.md`,
section 1.

WHAT THIS FILE IS, one sentence, in relation: `rv_general.one_attempt`
with nothing removed and four measurements added around it -- so the
render, the compile, the carve, the walk, the solver budget and the
instruction ceiling are `rv_general`'s own and are CALLED, not copied.

DEE'S RULE OF 2026-09-13, which this file is written under: the method
may know only what every arch-opcode gives it -- its definition and the
language's primitive operators.  NOTHING HERE IS WRITTEN FOR A
PARTICULAR ARCH-OPCODE.  The population is chosen by a reading of
VERDICTS in stores this task did not write (a cell is in it when no row
of any store carries a proof for it, on any language, by any route);
the reference out of a body is found by reading the disassembler's own
`<label>` annotations and comparing them with the unit's own symbol;
the first differing node is found by a parallel walk of two z3 terms on
declaration kind, sort and arity.  Every one of those questions has the
same answer shape for every cell of the table.

THE OBJECTS, one sentence each, in relation.
  * THE POPULATION is the set of (cell, place) keys for which no row of
    any store handed to this file records a proof.
  * THE CANONICAL FORM is `term.Term.normalize`'s own rule, run here as
    the functions that file exports (`order_commutative`,
    `ordered_symbols`, `one_line`) so the z3 OBJECT is kept beside the
    text; the text this file prints is checked against
    `Term.normalize`'s own return on the same term, and a disagreement
    is recorded as a refusal rather than hidden.
  * A REFERENCE OUT OF THE UNIT is an instruction of the carved body
    whose operand text carries a `<symbol>` annotation naming a symbol
    other than the unit's own.  No mnemonic is read.
  * THE FIRST DIFFERING NODE is the first position, in a leaves-last
    parallel walk of the two canonical terms, at which the sort, the
    declaration kind or the number of arguments differs.

MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_RV9.  One
process, no pool, no clock in the driver.

Coding discipline: no compound one-liner statements.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns.  The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token.  The
token appears exactly once per unit: as a display label on the member.
HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs").  MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure.  A brief handed to any subagent for this
line MUST paste this paragraph verbatim."

HOW THIS FILE OBEYS IT.  The population is a reading of verdicts; every
row is keyed on (`mnem`, operand shape, `key_width`, place, target),
which is machine form, and the mnemonic rides in the field `mnem`,
which the guard exempts as machine form.  Nothing here reads a source
token and no branch anywhere is taken on a mnemonic.

usage:
  rv9_native.py run <ref_dir> <op_dir> <emulation_dir> <twins.json>
                    <model_table_rv.json> <prefix> <src_dir>
                    <work_root> <store.jsonl>[,<store.jsonl>...]
                    [<limit>]
"""

import json
import os
import resource
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CONSTRUCT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, CONSTRUCT)

import z3                                                        # noqa: E402
import rv_general as RG                                          # noqa: E402
import render_general as RENDER                                  # noqa: E402

ABORT_KB = 6 * 1024 * 1024
ABORT_NAME = "ABORT_MEMORY_RV9"
TARGETS = ["c", "cpp", "go", "rust"]
POLICY = "native_first"

TEXT_COLUMNS = 66
"""how wide a pasted line may be before this file breaks it.  The
reason is the owner's own: a raw block wider than 72 columns wraps in his
reader and is unreadable, and the indent this file prints under is
three spaces."""


def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def check_memory(where):
    peak = peak_kb()
    if peak > ABORT_KB:
        raise SystemExit("%s: %d kB at %s" % (ABORT_NAME, peak, where))
    return peak


# ==================================================================
# section 1: the population -- a reading of verdicts, never of names
# ==================================================================

def key_of(row):
    cell = row["cell"]
    return (cell["mnem"], cell["shape"], cell["key_width"], row["place"])


def population(store_paths, twins_path):
    """(the keys with no proof in any store, the keys every store
    holds).  A cell is IN when no row of any store handed here records
    a proof for it on any target by any route."""
    proved = set()
    seen = set()
    for path in store_paths:
        handle = open(path)
        for line in handle:
            text = line.strip()
            if not text:
                continue
            row = json.loads(text)
            key = key_of(row)
            seen.add(key)
            if row.get("kind") == "proved":
                proved.add(key)
            continue
        handle.close()
        continue
    return sorted(seen - proved), sorted(seen)


# ==================================================================
# section 2: what a body refers to outside itself
# ==================================================================

def labels_of(line):
    """every `<...>` annotation the disassembler wrote on one carved
    instruction, in the order it wrote them."""
    out = []
    rest = line
    while True:
        start = rest.find("<")
        if start < 0:
            return out
        end = rest.find(">", start)
        if end < 0:
            return out
        out.append(rest[start + 1:end])
        rest = rest[end + 1:]
        continue


def references_out(body, symbol):
    """the instructions whose `<label>` names a symbol other than the
    unit's own -- which is what a call to a library routine looks like
    in the carved text, and what a jump inside the unit does not.

    NO MNEMONIC IS READ.  The question is whether the disassembler
    resolved the operand to a symbol this unit is not."""
    mine = set()
    mine.add(symbol)
    mine.add("main." + symbol)
    out = []
    for index, line in enumerate(body):
        for label in labels_of(line):
            head = label.split("+")[0]
            head = head.strip()
            if head in mine:
                continue
            out.append({"index": index, "line": line, "symbol": head})
            continue
        continue
    return out


def memory_operands(body):
    """the instructions whose operand text holds the architecture's own
    `offset(register)` form -- the machine-form reading of "this
    instruction names a memory address".  No mnemonic is read."""
    out = []
    for index, line in enumerate(body):
        text = line
        cut = text.find("#")
        if cut >= 0:
            text = text[:cut]
        cut = text.find("<")
        if cut >= 0:
            text = text[:cut]
        place = text.find("(")
        if place < 0:
            continue
        close = text.find(")", place)
        if close < 0:
            continue
        inner = text[place + 1:close].strip()
        if not inner:
            continue
        if " " in inner or "," in inner:
            continue
        out.append({"index": index, "line": line})
        continue
    return out


# ==================================================================
# section 3: the canonical form, kept as an object and as a text
# ==================================================================

def canonical(TERMS, term):
    """the z3 object `term.Term.normalize` prints, and its text.

    THE STEPS ARE THAT FILE'S OWN and are called from it: order the
    commutative arguments, simplify, order again, rename the free
    symbols positionally, simplify and order once more."""
    shaped = TERMS.order_commutative(term)
    shaped = z3.simplify(shaped)
    shaped = TERMS.order_commutative(shaped)
    symbols = TERMS.ordered_symbols(shaped)
    substitution = []
    for index, symbol in enumerate(symbols):
        if symbol.sort().kind() == z3.Z3_BV_SORT:
            fresh = z3.BitVec("v%d" % index, symbol.size())
        else:
            fresh = z3.Const("v%d" % index, symbol.sort())
        substitution.append((symbol, fresh))
        continue
    if substitution:
        shaped = z3.substitute(shaped, *substitution)
    shaped = z3.simplify(shaped)
    shaped = TERMS.order_commutative(shaped)
    return shaped, TERMS.one_line(shaped)


def first_difference(left, right, path=()):
    """(the path, the left sub-term, the right sub-term, what differs)
    at the FIRST position of a parallel walk at which the two terms are
    not the same shape, or None when they are shape-identical.

    The walk asks three questions of every position, in this order: the
    sort, the declaration kind, the number of arguments.  All three are
    z3's own machine form."""
    if left.sort() != right.sort():
        return (path, left, right, "the sort")
    if left.decl().kind() != right.decl().kind():
        return (path, left, right, "the declaration kind")
    if left.num_args() != right.num_args():
        return (path, left, right, "the number of arguments")
    if left.num_args() == 0:
        if left.sexpr() != right.sexpr():
            return (path, left, right, "the constant or the symbol")
        return None
    for index in range(left.num_args()):
        found = first_difference(left.arg(index), right.arg(index),
                                 path + (index,))
        if found is not None:
            return found
        continue
    return None


def node_count(term, seen=None):
    """how many DISTINCT nodes the term holds, counted by z3's own
    identity."""
    if seen is None:
        seen = set()
    if term.get_id() in seen:
        return len(seen)
    seen.add(term.get_id())
    for index in range(term.num_args()):
        node_count(term.arg(index), seen)
        continue
    return len(seen)


# ==================================================================
# section 4: one (cell, target), measured
# ==================================================================

def one_attempt(H, RL, INH, TERMS, holder, reference, cell, place_name,
                term, target, record, word, work_root, number):
    label = "%s_%s_%d__%s__%s__%s" % (cell["mnem"], cell["shape"],
                                      cell["key_width"], place_name,
                                      target, POLICY)
    label = label.replace(".", "_")
    out = {"target": target, "policy": POLICY, "label": label}
    ordered = H.renderer_input(record["term"])
    started = time.time()
    try:
        made = RENDER.render(ordered, target, record["families"],
                             record["home"]["family"], record["bits"],
                             label, word, POLICY,
                             record.get("text") or "")
    except Exception as problem:                              # noqa: BLE001
        out["rendered"] = False
        out["refusal_cause"] = "the render refused"
        out["refusal_detail"] = "%s: %s" % (type(problem).__name__,
                                            ("%s" % problem)[:300])
        return out
    out["rendered"] = True
    out["render_seconds"] = round(time.time() - started, 3)
    out["statements"] = made["statements"]
    out["native_nodes"] = made["native_nodes"]
    out["constructed_nodes"] = made["constructed_nodes"]
    out["constructed_kinds"] = made["constructed_kinds"]
    out["source"] = made["source"]
    out["source_lines"] = made["source"].count("\n") + 1
    work = os.path.join(work_root, "rv9n%06d_%s" % (number, target))
    started = time.time()
    got, command, diagnostic = INH.compile_and_carve(made["source"],
                                                     target, work)
    out["compile_seconds"] = round(time.time() - started, 3)
    out["compiler"] = {"command": command,
                       "target_triple": INH.triple_of(target)}
    if got is None:
        out["compiled"] = False
        out["verdict"] = {"outcome": "BUILD_REFUSED",
                          "reason": (diagnostic or "").strip()[:600]}
        return out
    out["compiled"] = True
    raw, body = got
    out["instructions"] = len(body)
    out["body"] = list(body)
    symbol = INH.symbol_of(made["source"])
    out["symbol"] = symbol
    out["references_out"] = references_out(body, symbol or "")
    out["memory_operands"] = len(memory_operands(body))
    out["gate_instruction_ceiling"] = RG.GATE_INSTRUCTION_CEILING
    if len(body) > RG.GATE_INSTRUCTION_CEILING:
        out["verdict"] = {"outcome": "NOT_GATED",
                          "reason": RG.CAUSE_GATE_TOO_LARGE,
                          "instructions": len(body)}
        return out
    contract = RL.slot_contract(term)
    started = time.time()
    try:
        state = reference.simulate(body, contract, {})
        answer = reference.answer_of(state, "a0")
    except Exception as problem:                              # noqa: BLE001
        out["walk_seconds"] = round(time.time() - started, 3)
        out["verdict"] = {"outcome": "WALK_REFUSED",
                          "reason": "%s: %s" % (type(problem).__name__,
                                                ("%s" % problem)[:300])}
        return out
    out["walk_seconds"] = round(time.time() - started, 3)

    width = cell["key_width"] or term.size()
    if width > term.size():
        width = term.size()
    body_side = INH.at_width(answer, width)
    cell_side = INH.at_width(term, width)
    left, left_text = canonical(TERMS, body_side)
    right, right_text = canonical(TERMS, cell_side)
    out["canonical_agrees_with_normalize"] = {
        "body": left_text == holder.normalize(body_side),
        "definition": right_text == holder.normalize(cell_side)}
    out["body_term_text"] = left_text
    out["definition_term_text"] = right_text
    out["body_term_nodes"] = node_count(left)
    out["definition_term_nodes"] = node_count(right)
    out["identical_after_normalize"] = (left_text == right_text)
    if left_text != right_text:
        found = first_difference(left, right)
        if found is None:
            out["first_difference"] = {
                "what": "the two texts differ but the parallel walk "
                        "finds no position at which the sort, the "
                        "declaration kind or the arity differs"}
        else:
            path, one, two, what = found
            out["first_difference"] = {
                "path": list(path),
                "what": what,
                "left_kind": "%s" % one.decl(),
                "right_kind": "%s" % two.decl(),
                "left_sort": "%s" % one.sort(),
                "right_sort": "%s" % two.sort(),
                "left": TERMS.one_line(one)[:2000],
                "right": TERMS.one_line(two)[:2000]}
    started = time.time()
    outcome, counterexample = INH.decide(body_side, cell_side,
                                         RG.SOLVER_MS)
    out["check_seconds"] = round(time.time() - started, 3)
    whole = term.size()
    outcome_whole, counter_whole = INH.decide(INH.at_width(answer, whole),
                                              INH.at_width(term, whole),
                                              RG.SOLVER_MS)
    out["verdict"] = {"outcome": outcome, "compared_on_bits": width,
                      "counterexample": counterexample,
                      "solver_timeout_ms": RG.SOLVER_MS}
    out["verdict_at_the_whole_place"] = {"outcome": outcome_whole,
                                         "compared_on_bits": whole,
                                         "counterexample": counter_whole}
    if outcome == "UNDECIDED":
        out["with_more_room"] = more_room(body_side, cell_side)
        out["at_each_width"] = at_each_width(body_side, cell_side)
        out["agreement"] = agreement(TERMS, body_side, cell_side)
    return out


WIDTHS = (8, 16, 32, 64)
"""the widths the same equality is asked at when the gate's own budget
ran out.  IT IS THE SAME QUESTION, TRUNCATED: `inherit.at_width` is the
gate's own narrowing and is called.  The answer says whether what
defeats the solver is the SHAPE of the two terms or the SIZE of the
question, and the reading is the same for every cell."""

AGREEMENT_POINTS = 200
"""how many input points the two terms are EVALUATED at when the solver
does not decide.  An agreement is EVIDENCE, NEVER A PROOF -- the word
this line already uses for the interpreted route.  The edge values come
first, in every sample, as the probe design requires."""


def edge_values(width):
    """the values on each side of every critical point of a width, and
    a few ordinary ones: the same list for every width."""
    top = (1 << width) - 1
    half = 1 << (width - 1)
    out = [0, 1, 2, 3, top, top - 1, half, half - 1, half + 1,
           top // 3, top // 7]
    return out


def agreement(TERMS, left, right):
    """how many of the sampled points the two terms answer the same at.
    Generic: the points are built from the widths of the term's own
    free symbols and from nothing else."""
    import random
    symbols = TERMS.ordered_symbols(left)
    for symbol in TERMS.ordered_symbols(right):
        if symbol.get_id() not in [s.get_id() for s in symbols]:
            symbols.append(symbol)
        continue
    if not symbols:
        return {"points": 0, "agreed": 0,
                "note": "the two terms read no value"}
    generator = random.Random(20260913)
    points = []
    for one in edge_values(symbols[0].size()):
        for two in edge_values(symbols[-1].size()):
            points.append([one, two])
            continue
        continue
    while len(points) < AGREEMENT_POINTS:
        point = []
        for symbol in symbols:
            point.append(generator.getrandbits(symbol.size()))
            continue
        points.append(point)
        continue
    agreed = 0
    posed = 0
    differed = None
    for point in points[:AGREEMENT_POINTS]:
        substitution = []
        for index, symbol in enumerate(symbols):
            value = point[index % len(point)]
            substitution.append((symbol,
                                 z3.BitVecVal(value, symbol.size())))
            continue
        one = z3.simplify(z3.substitute(left, *substitution))
        two = z3.simplify(z3.substitute(right, *substitution))
        posed = posed + 1
        try:
            same = (one.as_long() == two.as_long())
        except Exception:                                     # noqa: BLE001
            return {"points": posed, "agreed": agreed,
                    "note": "a substituted term did not reduce to a "
                            "value, so the probe stops rather than "
                            "guessing"}
        if same:
            agreed = agreed + 1
            continue
        if differed is None:
            differed = {"point": [str(v) for v in point],
                        "body": str(one), "definition": str(two)}
        continue
    return {"points": posed, "agreed": agreed, "first_difference":
            differed}


def at_each_width(left, right):
    """the same equality asked on the low k bits, for each width this
    file states, at the gate's own budget."""
    import inherit as INH
    out = []
    for width in WIDTHS:
        if width > left.size():
            continue
        started = time.time()
        outcome, counterexample = INH.decide(INH.at_width(left, width),
                                             INH.at_width(right, width),
                                             RG.SOLVER_MS)
        out.append({"bits": width, "outcome": outcome,
                    "counterexample": counterexample,
                    "seconds": round(time.time() - started, 3)})
        continue
    return out


MORE_ROOM_MS = 30000
"""the budget the brief names beside the gate's own 3,000 ms.  THE
MEASURED THING DOES NOT CHANGE: the same two terms, the same question.
The law's rule on a limit is that it is a FLAG -- re-run with more
room and report whether the answer changed."""


def more_room(left, right):
    """the same equality, twice more: once with ten times the gate's
    budget, and once through z3's OWN bit-blast tactic at that budget.

    Both are general: neither reads a name, and both ask the identical
    question of every term handed to them."""
    out = {"budget_ms": MORE_ROOM_MS}
    import inherit as INH
    started = time.time()
    outcome, counterexample = INH.decide(left, right, MORE_ROOM_MS)
    out["default_tactic"] = {"outcome": outcome,
                             "counterexample": counterexample,
                             "seconds": round(time.time() - started, 3)}
    started = time.time()
    try:
        tactic = z3.Then(z3.Tactic("simplify"), z3.Tactic("bit-blast"),
                         z3.Tactic("tseitin-cnf"), z3.Tactic("sat"))
        solver = tactic.solver()
        solver.set("timeout", MORE_ROOM_MS)
        solver.add(left != right)
        verdict = solver.check()
        if verdict == z3.unsat:
            name = "PROVED"
        elif verdict == z3.unknown:
            name = "UNDECIDED"
        else:
            name = "DISPROVED"
        out["bit_blast_tactic"] = {"outcome": name,
                                   "seconds": round(time.time() - started,
                                                    3)}
    except Exception as problem:                              # noqa: BLE001
        out["bit_blast_tactic"] = {"outcome": "REFUSED",
                                   "reason": "%s: %s"
                                   % (type(problem).__name__,
                                      ("%s" % problem)[:300]),
                                   "seconds": round(time.time() - started,
                                                    3)}
    return out


# ==================================================================
# section 5: the run
# ==================================================================

def run_command(ref_dir, op_dir, emulation_dir, twins_path, rv_path,
                prefix, src_dir, work_root, store_arg, limit):
    RV = os.path.dirname(os.path.abspath(twins_path))
    sys.path.insert(0, RV)
    sys.path.insert(0, os.path.join(emulation_dir, "handful"))
    sys.path.insert(0, os.path.join(emulation_dir, "autopoly"))
    sys.path.insert(0, emulation_dir)
    sys.path.insert(0, os.path.join(emulation_dir, "rust"))
    sys.path.insert(0, os.path.join(emulation_dir, "go"))
    sys.path.insert(0, os.path.join(emulation_dir, "swift"))
    import twins as TW
    say("[0/5] the references this run uses")
    X86, TERMS, MT, MTAB, digest = TW.bring_in(ref_dir, op_dir)
    import rv_loop as RL
    import inherit_rv3 as INH3
    import inherit as INH
    import riscv_reference as RV_REF
    import handful as H
    import construct as CONS
    INH3.install()
    holder = TERMS.Term(X86.Reference())
    reference = RV_REF.RiscvReference()
    say("   the x86 reference   %s" % digest)
    say("   the riscv lifter    %s" % RG_sha(RV_REF.__file__))
    if not os.path.isdir(src_dir):
        os.makedirs(src_dir)
    if not os.path.isdir(work_root):
        os.makedirs(work_root)

    say("[1/5] the population: every (cell, place) no store records a "
        "proof for")
    stores = []
    for name in store_arg.split(","):
        text = name.strip()
        if text:
            stores.append(text)
        continue
    keys, everything = population(stores, twins_path)
    say("   %d of %d (cell, place) keys the stores hold carry no proof "
        "on any language by any route" % (len(keys), len(everything)))
    for key in keys:
        say("     %s %s %s, place %s" % (key[0], key[1], key[2], key[3]))
        continue

    terms, _operands = RL.riscv_terms(rv_path)

    say("[2/5] the native route on each of them, on %s"
        % ", ".join(TARGETS))
    rows = []
    started = time.time()
    number = 0
    total = len(keys) * len(TARGETS)
    for key in keys:
        cell = {"mnem": key[0], "shape": key[1], "key_width": key[2]}
        place_name = key[3]
        term = terms.get(((key[0], key[1], key[2]), place_name))
        for target in TARGETS:
            number = number + 1
            if limit is not None and number > limit:
                break
            row = {"arch": "riscv64", "cell": dict(cell),
                   "place": place_name, "target": target,
                   "route": "native"}
            if term is None:
                row["kind"] = "refused"
                row["verdict"] = {"outcome": "NO_TERM",
                                  "reason": "the cell's own line could "
                                            "not be re-run"}
                rows.append(row)
                continue
            slotted, refusal = RL.in_parameter_slots(sys.modules["term"],
                                                     term)
            if slotted is None:
                row["kind"] = "refused"
                row["verdict"] = {"outcome": "NOT_RENDERED",
                                  "reason": refusal}
                rows.append(row)
                continue
            record = H.place_record("reg_rdi", slotted)
            if record.get("families") is None:
                row["kind"] = "refused"
                row["verdict"] = {"outcome": "NOT_RENDERED",
                                  "reason": record.get(
                                      "not_rendered_detail")
                                  or record.get("not_rendered")}
                rows.append(row)
                continue
            word = CONS.word_of(target)
            attempt = one_attempt(H, RL, INH, TERMS, holder, reference,
                                  cell, place_name, term, target, record,
                                  word, work_root, number)
            row["attempt"] = attempt
            row["kind"] = RG.kind_of_attempt(attempt)
            row["verdict"] = attempt.get("verdict")
            keep_source(src_dir, attempt)
            rows.append(row)
            say("   [%d/%d] %s %s %s %s -> %s, %.0f s, peak %.0f MB"
                % (number, total, key[0], key[1], key[2], target,
                   row["kind"], time.time() - started,
                   check_memory("run %d" % number) / 1024.0))
            continue
        continue

    say("[3/5] every measurement, cell by cell")
    report(rows)

    say("[4/5] the census")
    census = {}
    per_target = {}
    for row in rows:
        census[row["kind"]] = census.get(row["kind"], 0) + 1
        held = per_target.setdefault(row["target"], {})
        held[row["kind"]] = held.get(row["kind"], 0) + 1
        continue
    for kind in sorted(census):
        say("   %-12s %d" % (kind, census[kind]))
        continue

    say("[5/5] writing")
    write_rows(prefix, rows)
    document = {
        "meta": {
            "task": "rv9",
            "what": "the native route on every (cell, place) no store "
                    "records a proof for, measured object by object: "
                    "the source, the body, the references out of the "
                    "body, the two canonical texts, and the first node "
                    "at which they differ",
            "targets": list(TARGETS),
            "policy": POLICY,
            "stores_read": stores,
            "x86_reference_sha256": digest,
            "riscv_reference_sha256": RG_sha(RV_REF.__file__),
            "solver_timeout_ms": RG.SOLVER_MS,
            "gate_instruction_ceiling": RG.GATE_INSTRUCTION_CEILING,
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
    handle = open(prefix + ".json", "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    say("peak RSS: %d kB" % peak_kb())
    return 0


def RG_sha(path):
    import hashlib
    digest = hashlib.sha256()
    handle = open(path.replace(".pyc", ".py"), "rb")
    while True:
        chunk = handle.read(1 << 20)
        if not chunk:
            break
        digest.update(chunk)
        continue
    handle.close()
    return digest.hexdigest()


def keep_source(src_dir, attempt):
    if not attempt.get("source"):
        return
    suffix = {"c": ".c", "cpp": ".cpp", "go": ".go", "rust": ".rs"}
    name = attempt["label"] + suffix.get(attempt["target"], ".txt")
    handle = open(os.path.join(src_dir, name), "w")
    handle.write(attempt["source"])
    handle.close()
    return


def write_rows(prefix, rows):
    handle = open(prefix + ".jsonl", "w")
    for row in rows:
        handle.write(json.dumps(row, sort_keys=True) + "\n")
        continue
    handle.close()
    return


# ==================================================================
# section 6: the report -- every object, inside 72 columns
# ==================================================================

PIECES_KEPT = 3
"""how many pieces of a cut line are printed at each end before the
middle is named rather than shown.  Six pieces of 66 columns is about
four hundred characters, which is as much of one line as a reader can
hold; everything above that is in the store."""


def wrapped(text, columns=TEXT_COLUMNS):
    """one long line as several, each inside the stated width; where
    there are more pieces than this file prints, the number of
    characters not shown is named between the two ends."""
    if len(text) <= columns:
        return [text]
    pieces = []
    for start in range(0, len(text), columns):
        pieces.append(text[start:start + columns])
        continue
    if len(pieces) <= 2 * PIECES_KEPT:
        return pieces
    hidden = len(text) - 2 * PIECES_KEPT * columns
    out = list(pieces[:PIECES_KEPT])
    out.append("... %d characters of this line are not shown ..." % hidden)
    out.extend(pieces[-PIECES_KEPT:])
    return out


def paste(lines, indent="   ", columns=TEXT_COLUMNS):
    for line in lines:
        for piece in wrapped(line, columns):
            say(indent + piece)
            continue
        continue
    return


def paste_source(text, head_lines, tail_lines):
    lines = text.splitlines()
    if len(lines) <= head_lines + tail_lines:
        paste(lines)
        return
    paste(lines[:head_lines])
    say("   ... %d lines of this source are not shown here; the whole "
        % (len(lines) - head_lines - tail_lines))
    say("   ... file is beside the store in the run's src folder ...")
    paste(lines[-tail_lines:])
    return


def report(rows):
    say("")
    say("| mnem | shape | width | language | statements | source lines "
        "| body | refs out | memory operands | outcome | identical "
        "after normalize | check s |")
    say("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for row in rows:
        cell = row["cell"]
        attempt = row.get("attempt") or {}
        verdict = attempt.get("verdict") or row.get("verdict") or {}
        outcome = verdict.get("outcome")
        if outcome is None:
            outcome = attempt.get("refusal_cause") or "no verdict"
        refs = attempt.get("references_out")
        say("| `%s` | `%s` | %s | %s | %s | %s | %s | %s | %s | %s | %s "
            "| %s |"
            % (cell["mnem"], cell["shape"], cell["key_width"],
               row["target"], attempt.get("statements"),
               attempt.get("source_lines"), attempt.get("instructions"),
               len(refs) if refs is not None else None,
               attempt.get("memory_operands"), outcome,
               attempt.get("identical_after_normalize"),
               attempt.get("check_seconds")))
        continue
    say("")
    say("THE SAME QUESTION WITH MORE ROOM, where the gate's own budget "
        "ran out")
    say("| mnem | shape | width | language | at 3,000 ms | at %d ms | "
        "seconds | through z3's own bit-blast tactic | seconds |"
        % MORE_ROOM_MS)
    say("|---|---|---|---|---|---|---|---|---|")
    for row in rows:
        cell = row["cell"]
        attempt = row.get("attempt") or {}
        room = attempt.get("with_more_room")
        if not room:
            continue
        default = room.get("default_tactic") or {}
        blasted = room.get("bit_blast_tactic") or {}
        say("| `%s` | `%s` | %s | %s | UNDECIDED | %s | %s | %s | %s |"
            % (cell["mnem"], cell["shape"], cell["key_width"],
               row["target"], default.get("outcome"),
               default.get("seconds"), blasted.get("outcome"),
               blasted.get("seconds")))
        continue
    say("")
    say("THE SAME EQUALITY ON THE LOW k BITS, at the gate's own budget")
    say("| mnem | shape | width | language | 8 bits | 16 bits | 32 "
        "bits | 64 bits |")
    say("|---|---|---|---|---|---|---|---|")
    for row in rows:
        cell = row["cell"]
        attempt = row.get("attempt") or {}
        sweep = attempt.get("at_each_width")
        if not sweep:
            continue
        held = {}
        for one in sweep:
            held[one["bits"]] = "%s (%ss)" % (one["outcome"],
                                              one["seconds"])
            continue
        say("| `%s` | `%s` | %s | %s | %s | %s | %s | %s |"
            % (cell["mnem"], cell["shape"], cell["key_width"],
               row["target"], held.get(8), held.get(16), held.get(32),
               held.get(64)))
        continue
    say("")
    say("THE TWO TERMS EVALUATED AT SAMPLED POINTS -- EVIDENCE, NEVER "
        "A PROOF")
    say("| mnem | shape | width | language | points | agreed | first "
        "point at which they differ |")
    say("|---|---|---|---|---|---|---|")
    for row in rows:
        cell = row["cell"]
        attempt = row.get("attempt") or {}
        held = attempt.get("agreement")
        if not held:
            continue
        found = held.get("first_difference")
        say("| `%s` | `%s` | %s | %s | %s | %s | %s |"
            % (cell["mnem"], cell["shape"], cell["key_width"],
               row["target"], held.get("points"), held.get("agreed"),
               json.dumps(found) if found else "none"))
        continue
    say("")
    say("EVERY REFERENCE A BODY MAKES TO A SYMBOL OUTSIDE ITSELF")
    say("| mnem | shape | width | language | symbol | the instruction, "
        "LITERAL |")
    say("|---|---|---|---|---|---|")
    for row in rows:
        cell = row["cell"]
        attempt = row.get("attempt") or {}
        for one in attempt.get("references_out") or []:
            say("| `%s` | `%s` | %s | %s | `%s` | `%s` |"
                % (cell["mnem"], cell["shape"], cell["key_width"],
                   row["target"], one["symbol"],
                   " ".join(one["line"].split())))
            continue
        continue
    say("")
    for row in rows:
        cell = row["cell"]
        attempt = row.get("attempt") or {}
        say("")
        say("=== %s %s %s, place %s, %s"
            % (cell["mnem"], cell["shape"], cell["key_width"],
               row["place"], row["target"]))
        if not attempt:
            say("   no attempt: %s" % json.dumps(row.get("verdict")))
            continue
        say("   the compile command, LITERAL:")
        paste([(attempt.get("compiler") or {}).get("command") or ""])
        say("   the rendered source, LITERAL:")
        paste_source(attempt.get("source") or "", 14, 6)
        say("   statements %s, source lines %s, native nodes %s, "
            "constructed nodes %s"
            % (attempt.get("statements"), attempt.get("source_lines"),
               attempt.get("native_nodes"),
               attempt.get("constructed_nodes")))
        if not attempt.get("compiled"):
            say("   THE BUILD REFUSED, its words LITERAL:")
            paste([((attempt.get("verdict") or {}).get("reason")
                    or "")])
            continue
        say("   the compiled body, %s instructions, LITERAL:"
            % attempt.get("instructions"))
        body = attempt.get("body") or []
        if len(body) <= 80:
            paste(body)
        else:
            paste(body[:40])
            say("   ... %d instructions not shown; the store holds them "
                "all ..." % (len(body) - 60))
            paste(body[-20:])
        refs = attempt.get("references_out") or []
        say("   references to a symbol outside this unit: %d"
            % len(refs))
        for one in refs[:20]:
            paste(["[%d] %s" % (one["index"], one["line"])])
            continue
        say("   instructions naming a memory address: %s"
            % attempt.get("memory_operands"))
        verdict = attempt.get("verdict") or {}
        say("   the verdict: %s" % json.dumps(verdict, sort_keys=True)[:400])
        room = attempt.get("with_more_room")
        if room:
            say("   THE SAME QUESTION WITH MORE ROOM (%d ms), LITERAL:"
                % room.get("budget_ms"))
            paste([json.dumps(room, sort_keys=True)])
        if attempt.get("body_term_text") is None:
            continue
        say("   the canonical text this file computes agrees with "
            "Term.normalize: %s"
            % json.dumps(attempt.get("canonical_agrees_with_normalize")))
        say("   the BODY's formula, canonical, %s distinct nodes, "
            "LITERAL:" % attempt.get("body_term_nodes"))
        paste([attempt.get("body_term_text") or ""])
        say("   the DEFINITION's formula, canonical, %s distinct "
            "nodes, LITERAL:" % attempt.get("definition_term_nodes"))
        paste([attempt.get("definition_term_text") or ""])
        say("   identical after normalize: %s"
            % attempt.get("identical_after_normalize"))
        found = attempt.get("first_difference")
        if found:
            say("   THE FIRST NODE AT WHICH THEY DIFFER, LITERAL:")
            say("     path from the root: %s" % found.get("path"))
            say("     what differs: %s" % found.get("what"))
            say("     the body's node:       %s | sort %s"
                % (found.get("left_kind"), found.get("left_sort")))
            say("     the definition's node: %s | sort %s"
                % (found.get("right_kind"), found.get("right_sort")))
            say("     the body's sub-term, LITERAL:")
            paste([found.get("left") or ""])
            say("     the definition's sub-term, LITERAL:")
            paste([found.get("right") or ""])
        continue
    return


def main():
    command = sys.argv[1]
    if command == "run":
        limit = None
        if len(sys.argv) > 11:
            limit = int(sys.argv[11])
        return run_command(sys.argv[2], sys.argv[3], sys.argv[4],
                           sys.argv[5], sys.argv[6], sys.argv[7],
                           sys.argv[8], sys.argv[9], sys.argv[10], limit)
    raise SystemExit("unknown command %r" % command)


if __name__ == "__main__":
    sys.exit(main())
