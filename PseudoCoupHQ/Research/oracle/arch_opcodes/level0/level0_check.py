#!/usr/bin/env python3
"""level0_check.py -- our reference's level-0 mappings against an independent
reading, per (mnemonic, operand form, width), per written place.

WHAT THIS IS, in relation.  Level 0 of the operator-mapping proof system
(`PRIVATE/PseudoCoupHQ/DevComms/log_229_operator_mapping_proof_system_purpose.md`
§1) is the complete mapping of every arch opcode: for each opcode and operand
widths, the total function on bit patterns including the flags.  It is held
today as `PRIVATE/PseudoCoupHQ/Research/op_pipeline/reference.py`'s
builders, with no independent check.  This program is that check: for every
instruction variant BOTH readings hold, z3 is asked whether our term and the
K-framework semantics' term are equal on every input, place by place.  It
decides nothing -- where the two disagree it records both readings and the
counterexample, and the ruling is the owner's.

THE FIVE OUTCOMES, one per (variant, place), and no sixth:
  `unsat`      z3 found no input on which the two differ: they agree.
  `sat`        z3 found one: they disagree, and the model is recorded.
  `unknown`    z3 gave up at the ceiling; wide multiply and division get one
               re-pose at the wider ceiling, recorded beside the first.
  `undefined`  their rule writes `undefMInt` / `undefBool` over the WHOLE
               input space -- Intel's undefined flag -- so there is nothing
               to compare.  Where it is undefined over only PART of the space
               the comparison is asked on the rest and the region is recorded.
  `refused`    the comparison could not be stated: a function the parser
               lacks, a width our table lacks, a flag our reference writes no
               route to, or a place only one reading writes.

HOW THE TWO SIDES ARE MADE TO SPEAK OF THE SAME INPUTS.  Both readings are
run over ONE set of symbols: our `reference.MachineState` seeds a 64-bit free
symbol per register family, and their rule's `getParentValue(R1, RSMap)` is
bound to the SAME symbol for the operand our shape spells at that position.
So nothing is renamed afterwards and no correspondence is assumed -- the two
terms are literally over one alphabet.

THE FLAGS, and why they need a seeding instruction.  Our reference does not
hold the flags as six bits: it holds the triple (the flag-setting opcode, its
left side, its right side) and rebuilds a bit when a consumer reads it
(`reference.carry_bit`, `reference.overflow_bit`, `reference.predicate_of`).
Their rule holds six named bits.  So OUR six bits are derived through our own
consumer route -- which is the route every flag reader in our pipeline takes
-- and compared against their six.  Two consequences, both stated rather than
hidden:
  * our reference writes NO route to the auxiliary carry, so every `AF` place
    is `refused` by cause and never counted as agreement;
  * a variant that READS the flags (`setcc`, `cmovcc`, `adc`, `sbb`) is run
    after a seeding comparison at 32 bits over two free symbols, and their
    `getFlag(F, RSMap)` is bound to OUR bit for F under that same seed.  The
    comparison then holds over the flag tuples a comparison can produce, which
    is a subset of all 64 tuples -- so a `unsat` there is agreement on the
    reachable region, not on every tuple, and the record says so.

usage:
    python3 level0_check.py <their semantics folder> <key_map.json> \
        <level0_check.json> <level0_check.md> [--limit N] [--workers N]
"""

import json
import os
import resource
import sys
import time

import multiprocessing

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
PIPELINE = os.path.abspath(
    os.path.join(HERE, "..", "..", "..", "op_pipeline"))
for _path in (PIPELINE, os.path.join(PIPELINE, "lean")):
    if _path not in sys.path:
        sys.path.insert(0, _path)

import z3                                                  # noqa: E402

import k_to_z3                                             # noqa: E402
import reference as R                                      # noqa: E402
import model_translate as MT                               # noqa: E402
import term as T                                           # noqa: E402


MEMORY_CEILING_MB = 6144
ABORT_NAME = "ABORT_MEMORY_REF1"
SOLVER_MS = 3000
WIDE_SOLVER_MS = 30000
WIDE_FAMILIES = frozenset(["imul", "mul", "idiv", "div"])
"""the mnemonics whose terms are a widening multiply or a division, which
the brief allows ONE re-pose at the wider ceiling."""

SEED_TEXTS = {8: ["%r10b", "%r11b"], 16: ["%r10w", "%r11w"],
              32: ["%r10d", "%r11d"], 64: ["%r10", "%r11"]}
SEED_WIDTH = 32
SEED_MNEM = "cmp"
"""the seeding instruction a flag-reading variant is run after.  Its two
operands are register families no operand shape of our sweep spells, so the
seed's symbols are free and distinct from the instruction's own."""


FLAG_NAMES = ("CF", "PF", "AF", "ZF", "SF", "OF")

FLAG_ROUTE = {
    "CF": lambda state: R.carry_bit(state.flags),
    "OF": lambda state: R.overflow_bit(state.flags),
    "ZF": lambda state: R.predicate_of(state, "e"),
    "SF": lambda state: R.predicate_of(state, "s"),
    "PF": lambda state: R.predicate_of(state, "p"),
}
"""OUR route to each flag bit, taken from our own reference and not written
here.  `AF` is absent from this table because our reference writes no route to
it: `predicate_of` has no auxiliary-carry condition and neither `carry_bit`
nor `overflow_bit` answers one."""

NO_AF = ("our reference writes no route to the auxiliary carry: it holds the "
         "flags as (setter, left, right) and rebuilds a bit on demand, and "
         "neither carry_bit, overflow_bit nor predicate_of answers AF")


# ==================================================================
# section 1: the memory bound
# ==================================================================


def peak_mb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0


def check_memory(where):
    peak = peak_mb()
    if peak > MEMORY_CEILING_MB:
        raise SystemExit("%s: %.1f MB at %s, past the stated %d MB"
                         % (ABORT_NAME, peak, where, MEMORY_CEILING_MB))
    return peak


# ==================================================================
# section 2: our reading of one variant
# ==================================================================


REGISTER_SPELLINGS = {}
for _family, _names in (
        ("rax", ["rax", "eax", "ax", "al", "ah"]),
        ("rbx", ["rbx", "ebx", "bx", "bl", "bh"]),
        ("rcx", ["rcx", "ecx", "cx", "cl", "ch"]),
        ("rdx", ["rdx", "edx", "dx", "dl", "dh"]),
        ("rsi", ["rsi", "esi", "si", "sil"]),
        ("rdi", ["rdi", "edi", "di", "dil"]),
        ("rsp", ["rsp", "esp", "sp", "spl"]),
        ("rbp", ["rbp", "ebp", "bp", "bpl"])):
    for _name in _names:
        REGISTER_SPELLINGS["%" + _name] = _family
for _index in range(8, 16):
    for _suffix in ("", "d", "w", "b"):
        REGISTER_SPELLINGS["%r" + str(_index) + _suffix] = \
            "r" + str(_index)
for _index in range(16):
    REGISTER_SPELLINGS["%xmm" + str(_index)] = "xmm" + str(_index)
"""every register spelling their rules name outright, and the family whose
64-bit seed symbol it belongs to.  `getParentValue(%rcx, RSMap)` is the whole
`%rcx`, which is exactly `state.seed("rcx")`."""


def our_reading(mnem, texts):
    """run OUR reference on one line and return everything the check
    needs: the places it wrote, the machine state, the flags before and
    after, and the six flag bits as they stood BEFORE the line.

    Every line is run after the seeding comparison, so a variant that
    reads the flags has flags to read and one that does not simply
    overwrites them.  `before` is snapshotted after the seeding, so the
    seed's own registers never count as written.
    """
    state = R.MachineState()
    seed_line = "%s %s" % (SEED_MNEM,
                           ",".join(SEED_TEXTS[SEED_WIDTH]))
    R.REFERENCE.step(state, seed_line)
    flags_before = state.flags
    # THE MEMORY CELL'S ARRIVAL VALUE, taken BEFORE the line runs.
    # `MachineState.memory_cell` puts a cell's arrival symbol into
    # `state.memory` the first time the cell is touched and the write
    # then REPLACES it, so a binding made after the line would bind
    # their rule's `Mem32` -- which is the value the instruction READ --
    # to the value it WROTE.  Touching it here also means the arrival
    # is in `before`, so a cell the line only reads is not counted as
    # written (the same correction task m1 made in its own program,
    # log_236 section 9).
    arrivals = {}
    for text in texts:
        probe = R.Operands(state, mnem, list(texts))
        if probe.is_memory(text) and not probe.is_rip(text):
            arrivals[text] = state.memory_cell(text)
    incoming = {}
    incoming_refusals = {}
    for name in FLAG_NAMES:
        route = FLAG_ROUTE.get(name)
        if route is None:
            incoming_refusals[name] = NO_AF
            continue
        try:
            incoming[name] = as_bit(route(state))
        except R.NotModeled as refusal:
            incoming_refusals[name] = str(refusal)
        except Exception as problem:                 # noqa: BLE001
            incoming_refusals[name] = (
                "our reference's route to this flag stopped on the "
                "seeding line's flag triple: %s: %s"
                % (type(problem).__name__, problem))
    written, flags_after, state, line = MT.run_line(mnem, texts, state)
    return {
        "written": written,
        "state": state,
        "line": line,
        "seed_line": seed_line,
        "flags_before": flags_before,
        "flags_after": flags_after,
        "incoming": incoming,
        "incoming_refusals": incoming_refusals,
        "arrivals": arrivals,
    }


def as_bit(condition):
    """a z3 Bool as the 1-bit value their rules hold a flag in."""
    return z3.If(condition, z3.BitVecVal(1, 1), z3.BitVecVal(0, 1))


def our_flag(reading, name):
    """(our 1-bit term for that flag after the line, the refusal).

    A builder that left the flag triple untouched wrote no flag, and
    that is a refusal with its own cause rather than a disagreement."""
    state = reading["state"]
    if state.flags is None:
        return None, ("our reference's builder leaves no flag triple "
                      "for this opcode, so it writes no flag")
    if state.flags is reading["flags_before"]:
        return None, ("our reference's builder leaves the flags "
                      "untouched for this opcode, so it writes no flag")
    route = FLAG_ROUTE.get(name)
    if route is None:
        return None, NO_AF
    try:
        return as_bit(route(state)), None
    except R.NotModeled as refusal:
        return None, str(refusal)
    except Exception as problem:                     # noqa: BLE001
        # NOT a disagreement: our reference's own route stopped on this
        # setter, and the sentence it stopped with is the cause.
        return None, ("our reference's route to this flag stopped on "
                      "its own flag triple: %s: %s"
                      % (type(problem).__name__, problem))


# ==================================================================
# section 3: binding their rule to our symbols
# ==================================================================


def bind(rule, reading, record):
    """the environment their rule is evaluated in: every free name of
    theirs bound to the symbol OUR reference already made for the same
    place.

    Returns (the environment, the map from their written place to our
    place name, the refusals raised while binding)."""
    state = reading["state"]
    env = k_to_z3.Environment()
    refusals = {}
    for spelling, family in REGISTER_SPELLINGS.items():
        env.register_of[spelling] = state.seed(family)
    places = {}
    texts = record["operands"]
    for index, operand in enumerate(rule.operands):
        if index >= len(texts):
            refusals["operand %d" % index] = (
                "their rule head names %d operands and our shape spells "
                "%d" % (len(rule.operands), len(texts)))
            continue
        text = texts[index]
        kind = operand.get("kind")
        name = operand.get("var")
        if kind in ("gpr", "high", "xmm", "ymm"):
            family = REGISTER_SPELLINGS.get(text)
            if family is None:
                refusals["operand %d" % index] = (
                    "our shape spells %r at that position, which is not "
                    "a register spelling this check binds" % text)
                continue
            symbol = state.seed(family)
            if kind in ("xmm", "ymm"):
                # THEIR READING HOLDS THE WHOLE 256-BIT VECTOR
                # REGISTER: `getParentValue(%xmm0, RSMap)` is the YMM
                # the XMM is the low half of, and their rules extract
                # bits 0..128 of a 256-bit value.  Ours holds 128 bits.
                # So the 128 both readings hold is our own seed, and
                # the 128 only theirs holds is a fresh unconstrained
                # symbol -- which keeps the upper half from being
                # claimed zero, a claim neither reading makes.
                symbol = z3.Concat(
                    z3.BitVec("seed_upper_%s" % family, 128), symbol)
            if name is not None:
                env.register_of[name] = symbol
            places[name] = "reg_%s" % family
        elif kind == "cl":
            if name is not None:
                env.register_of[name] = state.seed("rcx")
        elif kind == "imm":
            if record.get("immediate_binding") == "literal":
                value = 3
                if text.startswith("$"):
                    value = int(text[1:], 0)
                symbol = z3.BitVecVal(value, 64)
            else:
                family = REGISTER_SPELLINGS.get(text)
                if family is None:
                    refusals["operand %d" % index] = (
                        "our shape spells %r in the immediate's slot, "
                        "which is not a register spelling this check "
                        "binds" % text)
                    continue
                symbol = state.seed(family)
            if name is not None:
                env.immediate_of[name] = symbol
                env.register_of[name] = symbol
        elif kind == "mem":
            cell = reading["arrivals"].get(text)
            if cell is None:
                cell = state.memory_cell(text)
            for value_name, width in rule.memory_values.items():
                env.register_of[value_name] = R.cut(cell, width)
            places[name] = "mem_%s" % R.mangle(text)
        else:
            refusals["operand %d" % index] = (
                "their rule head names an operand kind %r this check "
                "does not bind" % kind)
    for name in FLAG_NAMES:
        term = reading["incoming"].get(name)
        if term is not None:
            env.flag_of[name] = term
    return env, places, refusals


def our_place_for(place, places, record):
    """the name of OUR place that stands for one of their written
    places."""
    if place["kind"] == "flag":
        return "flags:%s" % place["name"]
    if "var" in place:
        name = places.get(place["var"])
        if name is not None:
            return name
        return None
    family = REGISTER_SPELLINGS.get(place.get("literal"))
    if family is None:
        return None
    return "reg_%s" % family


# ==================================================================
# section 4: the one comparison
# ==================================================================


def compare(ours, theirs, wide, undefined):
    """ask z3 whether the two terms can differ, on the region where
    theirs is defined.

    Returns (the outcome, the model as text, the milliseconds asked for,
    the re-posed outcome or None).
    """
    try:
        sizes = (ours.size(), theirs.size())
    except AttributeError:
        return ("refused", None, None, None,
                "the two readings are of different K sorts at that "
                "place, so no equality between them can be stated")
    narrowed = None
    if sizes[0] != sizes[1]:
        if sizes[1] > sizes[0] and sizes[1] % sizes[0] == 0:
            # THE VECTOR REGISTER AGAIN: their place is the whole
            # 256-bit register and ours is its low 128 bits.  The
            # comparison is asked on the bits BOTH readings hold, and
            # the narrowing is recorded on the row rather than done
            # silently.
            theirs = z3.Extract(sizes[0] - 1, 0, theirs)
            narrowed = ("their reading writes %d bits at this place and "
                        "ours writes %d; the comparison is on the low "
                        "%d, the bits both readings hold"
                        % (sizes[1], sizes[0], sizes[0]))
        else:
            return ("refused", None, None, None,
                    "the two readings write %d and %d bits at that "
                    "place" % sizes)
    question = ours != theirs
    if undefined is not None:
        question = z3.And(z3.Not(undefined), question)
    outcome, model = ask(question, SOLVER_MS)
    if outcome != "unknown" or not wide:
        return outcome, model, SOLVER_MS, None, narrowed
    reposed, model2 = ask(question, WIDE_SOLVER_MS)
    return outcome, model2 or model, SOLVER_MS, reposed, narrowed


def ask(question, milliseconds):
    solver = z3.Solver()
    solver.set("timeout", milliseconds)
    solver.add(question)
    verdict = solver.check()
    if verdict == z3.unsat:
        return "unsat", None
    if verdict == z3.sat:
        return "sat", counterexample(solver.model())
    return "unknown", None


def counterexample(model):
    """the model as a sorted list of records, machine form: one record
    per symbol with its printed value."""
    out = []
    for declaration in sorted(model.decls(), key=lambda d: d.name()):
        value = model[declaration]
        out.append({"symbol": declaration.name(),
                    "text": printed(value)})
    return out


def printed(value):
    try:
        if z3.is_bv_value(value):
            return "0x%x" % value.as_long()
    except Exception:                                # noqa: BLE001
        pass
    return str(value).replace("\n", " ")


PRINTER = []


def printer():
    if not PRINTER:
        PRINTER.append(T.Term())
    return PRINTER[0]


def layer5(term):
    """the pipeline's own fixed-rule re-render, `term.Term.normalize`.

    It renames free symbols POSITIONALLY (`v0`, `v1`, ...), which is
    what makes two texts comparable across units -- and which is
    exactly wrong for putting two readings of ONE instruction beside
    each other, because the two would be renamed by their own orders.
    So the side-by-side on the page uses `one_line` below, which keeps
    the names our reference gave the registers, and this text rides
    beside it in the json."""
    try:
        return printer().normalize(term)
    except Exception as problem:                     # noqa: BLE001
        return "<the layer-5 printer refused this term: %s>" % problem


def one_line(term):
    """z3's own printing of the simplified term on one line, with every
    free symbol keeping the name our reference gave it (`seed_rdi`), so
    the two readings of one instruction are directly comparable."""
    try:
        text = str(z3.simplify(term))
    except Exception as problem:                     # noqa: BLE001
        return "<z3 refused to simplify this term: %s>" % problem
    return " ".join(text.split())


def is_never(condition):
    """is this region empty -- is the place defined everywhere?"""
    solver = z3.Solver()
    solver.set("timeout", SOLVER_MS)
    solver.add(condition)
    return solver.check() == z3.unsat


def is_always(condition):
    """is this region the whole space -- is the place undefined
    everywhere?"""
    solver = z3.Solver()
    solver.set("timeout", SOLVER_MS)
    solver.add(z3.Not(condition))
    return solver.check() == z3.unsat


# ==================================================================
# section 5: one variant, end to end
# ==================================================================


def one_variant(job):
    variant, record, path = job
    started = time.time()
    out = {"variant": variant, "mnem": record["mnem"],
           "shape": record["shape"], "width": record["width"],
           "key_width": record["key_width"],
           "row_id": record["row_id"],
           "immediate_binding": record.get("immediate_binding"),
           "attestation_ledger_rows":
               record.get("attestation_ledger_rows", 0),
           "attestation_units": record.get("attestation_units", 0),
           "places": []}
    try:
        rule = k_to_z3.parse_file(path)
    except k_to_z3.Refused as refusal:
        out["places"].append({"place": "the whole rule",
                              "outcome": "refused",
                              "reason": "%s: %s" % (refusal.cause,
                                                    refusal.detail)})
        out["seconds"] = time.time() - started
        return out
    try:
        reading = our_reading(record["mnem"], record["operands"])
    except R.NotModeled as refusal:
        out["places"].append({"place": "the whole rule",
                              "outcome": "refused",
                              "reason": ("our reference refused the "
                                         "line: %s" % refusal)})
        out["seconds"] = time.time() - started
        return out
    except Exception as problem:                     # noqa: BLE001
        out["places"].append({"place": "the whole rule",
                              "outcome": "refused",
                              "reason": ("our reference stopped on the "
                                         "line: %s: %s"
                                         % (type(problem).__name__,
                                            problem))})
        out["seconds"] = time.time() - started
        return out
    out["line"] = reading["line"]
    out["seed_line"] = reading["seed_line"]
    env, places, bind_refusals = bind(rule, reading, record)
    for where in sorted(bind_refusals):
        out["places"].append({"place": where, "outcome": "refused",
                              "reason": bind_refusals[where]})
    wide = record["mnem"] in WIDE_FAMILIES
    seen_ours = set()
    for place, expression in rule.writes:
        name = our_place_for(place, places, record)
        row = {"place": name or describe(place)}
        if name is None:
            row["outcome"] = "refused"
            row["reason"] = ("their rule writes a place our shape does "
                             "not name")
            out["places"].append(row)
            continue
        try:
            value = k_to_z3.evaluate(expression, env)
        except k_to_z3.Refused as refusal:
            row["outcome"] = "refused"
            row["reason"] = "%s: %s" % (refusal.cause, refusal.detail)
            out["places"].append(row)
            continue
        except Exception as problem:                 # noqa: BLE001
            row["outcome"] = "refused"
            row["reason"] = ("their term stopped this grammar: %s: %s"
                             % (type(problem).__name__, problem))
            out["places"].append(row)
            continue
        if value.kind != "mint":
            row["outcome"] = "refused"
            row["reason"] = ("their term came back as the K sort %r, "
                             "which is not a value" % value.kind)
            out["places"].append(row)
            continue
        theirs = value.term
        region, theirs = k_to_z3.undefined_region(theirs)
        undefined = None
        if not z3.is_false(z3.simplify(region)):
            if is_always(region):
                row["outcome"] = "undefined"
                row["reason"] = ("their rule writes Intel's undefined "
                                 "value at this place on every input")
                row["undefined_region"] = "every input"
                row["theirs"] = one_line(theirs)
                out["places"].append(row)
                continue
            undefined = region
            row["undefined_region"] = str(
                z3.simplify(region)).replace("\n", " ")
        if name.startswith("flags:"):
            ours, refusal = our_flag(reading, name.split(":", 1)[1])
            if ours is None:
                row["outcome"] = "refused"
                row["reason"] = refusal
                row["theirs"] = one_line(theirs)
                out["places"].append(row)
                continue
        else:
            seen_ours.add(name)
            ours = reading["written"].get(name)
            if ours is None:
                row["outcome"] = "refused"
                row["reason"] = ("our reference's builder writes "
                                 "nothing at that place")
                row["theirs"] = one_line(theirs)
                out["places"].append(row)
                continue
        try:
            outcome, model, asked, reposed, note = compare(
                ours, theirs, wide, undefined)
        except Exception as problem:                 # noqa: BLE001
            row["outcome"] = "refused"
            row["reason"] = ("the comparison could not be stated: "
                             "%s: %s" % (type(problem).__name__,
                                         problem))
            row["ours"] = one_line(ours)
            row["theirs"] = one_line(theirs)
            row["ours_layer5"] = layer5(ours)
            row["theirs_layer5"] = layer5(theirs)
            out["places"].append(row)
            continue
        row["outcome"] = outcome
        if outcome == "refused":
            row["reason"] = note
            row["ours"] = one_line(ours)
            row["theirs"] = one_line(theirs)
            out["places"].append(row)
            continue
        if note is not None:
            row["narrowed"] = note
        row["solver_ms"] = asked
        if reposed is not None:
            row["reposed_outcome"] = reposed
            row["reposed_ms"] = WIDE_SOLVER_MS
        if outcome != "unsat":
            row["ours"] = one_line(ours)
            row["theirs"] = one_line(theirs)
            row["ours_layer5"] = layer5(ours)
            row["theirs_layer5"] = layer5(theirs)
        if model is not None:
            row["counterexample"] = model
            row["ours_at_the_counterexample"] = at_model(ours, model)
            row["theirs_at_the_counterexample"] = at_model(theirs,
                                                           model)
        out["places"].append(row)
    for name in sorted(reading["written"]):
        if name in seen_ours:
            continue
        out["places"].append({
            "place": name, "outcome": "refused",
            "reason": ("our reference writes this place and their rule "
                       "states nothing at it")})
    out["seconds"] = time.time() - started
    out["peak_mb"] = peak_mb()
    return out


def describe(place):
    if place["kind"] == "flag":
        return "flags:%s" % place["name"]
    return "a register their rule names %r" % place.get(
        "var", place.get("literal"))


def at_model(term, model):
    """the term's value at the counterexample, so both readings are on
    the page as VALUES and not only as formulas.

    A symbol the model left unconstrained keeps its name, so the value
    comes back partly symbolic rather than falsely concrete."""
    try:
        substitution = []
        for symbol in free_symbols(term):
            for record in model:
                if record["symbol"] != symbol.decl().name():
                    continue
                text = record["text"]
                if not text.startswith("0x"):
                    continue
                substitution.append(
                    (symbol, z3.BitVecVal(int(text, 16),
                                          symbol.size())))
        if not substitution:
            return None
        value = z3.simplify(z3.substitute(term, *substitution))
        return printed(value)
    except Exception:                                # noqa: BLE001
        return None


def free_symbols(term):
    out = {}
    seen = set()

    def walk(node):
        key = node.get_id()
        if key in seen:
            return
        seen.add(key)
        if node.num_args() == 0 and \
                node.decl().kind() == z3.Z3_OP_UNINTERPRETED:
            out[node.decl().name()] = node
            return
        for kid in node.children():
            walk(kid)

    walk(term)
    return [out[name] for name in sorted(out)]


# ==================================================================
# section 6: the run
# ==================================================================


def run(semantics_folder, key_map_path, workers, limit):
    document = json.load(open(key_map_path))
    matched = document["matched"]
    jobs = []
    for variant in sorted(matched):
        record = matched[variant]
        path = os.path.join(semantics_folder, record["folder"],
                            variant + ".k")
        jobs.append((variant, record, path))
    if limit:
        jobs = jobs[:limit]
    total = len(jobs)
    results = []
    if workers <= 1:
        for index, job in enumerate(jobs):
            results.append(one_variant(job))
            if (index + 1) % 20 == 0 or index + 1 == total:
                print("[%d/%d] %.1f MB"
                      % (index + 1, total, check_memory("the check")))
                sys.stdout.flush()
        return results, document
    pool = multiprocessing.Pool(workers)
    try:
        for index, result in enumerate(
                pool.imap_unordered(one_variant, jobs, chunksize=1)):
            results.append(result)
            if (index + 1) % 20 == 0 or index + 1 == total:
                print("[%d/%d] %.1f MB"
                      % (index + 1, total, check_memory("the check")))
                sys.stdout.flush()
    finally:
        pool.close()
        pool.join()
    return results, document


# ==================================================================
# section 7: the counts and the two written artifacts
# ==================================================================


OUTCOMES = ("unsat", "sat", "unknown", "undefined", "refused")


def tally(results):
    per_mnem = {}
    totals = dict((name, 0) for name in OUTCOMES)
    variants_all_agree = 0
    variants_with_a_disagreement = 0
    for result in results:
        row = per_mnem.setdefault(result["mnem"], {
            "mnem": result["mnem"], "variants": 0, "places": 0,
            "unsat": 0, "sat": 0, "unknown": 0, "undefined": 0,
            "refused": 0,
            "attestation_ledger_rows": 0})
        row["variants"] = row["variants"] + 1
        row["attestation_ledger_rows"] = (
            row["attestation_ledger_rows"] +
            result.get("attestation_ledger_rows", 0))
        disagreed = False
        compared = 0
        agreed = 0
        for place in result["places"]:
            outcome = place["outcome"]
            row["places"] = row["places"] + 1
            row[outcome] = row[outcome] + 1
            totals[outcome] = totals[outcome] + 1
            if outcome == "sat":
                disagreed = True
            if outcome in ("unsat", "sat"):
                compared = compared + 1
            if outcome == "unsat":
                agreed = agreed + 1
        if disagreed:
            variants_with_a_disagreement = variants_with_a_disagreement + 1
        elif compared and compared == agreed:
            variants_all_agree = variants_all_agree + 1
    return per_mnem, totals, variants_all_agree, \
        variants_with_a_disagreement


def group_disagreements(results):
    """every `sat` place grouped by CAUSE, a cause being (the place kind,
    the width, the shape) plus the two readings' shapes -- machine form
    throughout, and the mnemonic only ever in a `mnem` field."""
    groups = {}
    for result in results:
        for place in result["places"]:
            if place["outcome"] != "sat":
                continue
            kind = "flags" if place["place"].startswith("flags:") \
                else "destination"
            detail = place["place"].split(":", 1)[1] \
                if kind == "flags" else "the place written"
            # THE CAUSE, and why it is keyed this way.  A disagreement's
            # cause is what MECHANISM the two readings differ on, and
            # the two mechanisms this check separates are: which BITS a
            # write leaves standing (a destination, keyed by the width
            # at which it is written, because the machine's rule for a
            # sub-64-bit write is width-dependent), and which FUNCTION a
            # flag is (keyed by the flag, because each flag is its own
            # function).  The shape is carried on every example rather
            # than in the key, so one mechanism is one row.
            if kind == "destination":
                key = "the destination written at width %s" % \
                    result["key_width"]
            else:
                key = "the flag %s" % detail
            group = groups.setdefault(key, {
                "cause_key": key, "kind": kind, "detail": detail,
                "count": 0, "mnems": [], "shapes": [], "examples": []})
            group["count"] = group["count"] + 1
            if not any(m["mnem"] == result["mnem"]
                       for m in group["mnems"]):
                group["mnems"].append({"mnem": result["mnem"]})
            if result["shape"] not in group["shapes"]:
                group["shapes"].append(result["shape"])
            already = set(e["mnem"] for e in group["examples"])
            if len(group["examples"]) < 3 and \
                    result["mnem"] not in already:
                group["examples"].append({
                    "variant": result["variant"],
                    "mnem": result["mnem"],
                    "shape": result["shape"],
                    "key_width": result["key_width"],
                    "line": result.get("line"),
                    "place": place["place"],
                    "ours": place.get("ours"),
                    "theirs": place.get("theirs"),
                    "counterexample": place.get("counterexample"),
                    "ours_at_the_counterexample":
                        place.get("ours_at_the_counterexample"),
                    "theirs_at_the_counterexample":
                        place.get("theirs_at_the_counterexample"),
                })
    return [groups[key] for key in
            sorted(groups, key=lambda k: -groups[k]["count"])]


def group_refusals(results):
    causes = {}
    for result in results:
        for place in result["places"]:
            if place["outcome"] != "refused":
                continue
            cause = place.get("reason", "")
            record = causes.setdefault(cause, {"reason": cause,
                                               "count": 0,
                                               "mnems": []})
            record["count"] = record["count"] + 1
            if not any(m["mnem"] == result["mnem"]
                       for m in record["mnems"]):
                record["mnems"].append({"mnem": result["mnem"]})
    return [causes[c] for c in sorted(causes,
                                      key=lambda c: -causes[c]["count"])]


def undefined_regions(results):
    """the undefined region per mnemonic: which flags their reading
    leaves undefined, over the whole input space or over part of it."""
    per_mnem = {}
    for result in results:
        row = per_mnem.setdefault(result["mnem"],
                                  {"mnem": result["mnem"],
                                   "whole": [], "partial": []})
        for place in result["places"]:
            if not place["place"].startswith("flags:"):
                continue
            flag = place["place"].split(":", 1)[1]
            if place["outcome"] == "undefined":
                if flag not in row["whole"]:
                    row["whole"].append(flag)
            elif place.get("undefined_region"):
                if flag not in row["partial"]:
                    row["partial"].append(flag)
    out = []
    for mnem in sorted(per_mnem):
        row = per_mnem[mnem]
        if not row["whole"] and not row["partial"]:
            continue
        row["whole"] = sorted(row["whole"])
        row["partial"] = sorted(row["partial"])
        out.append(row)
    return out


def report(document, results, per_mnem, totals, agree, disagree,
           disagreements, refusals, regions, seconds, peak):
    lines = []
    add = lines.append
    add("# level 0 checked against an independent reading")
    add("")
    add("Our reference's mappings (`Research/op_pipeline/reference.py`, "
        "through the model table) against the K-framework x86-64 "
        "semantics (Dasgupta et al., PLDI 2019), read from "
        "`/sources/X86-64-semantics` under the University of "
        "Illinois/NCSA Open Source License and never copied here.")
    add("")
    add("Every rendering below is printed by ONE printer, ours: "
        "`term.Term.normalize`, the pipeline's own layer-5 re-render. "
        "A term shown as `theirs` is THEIR rule as this grammar parsed "
        "it, printed by our printer -- not their file's text.")
    add("")
    add("Table 1 -- the headline.")
    add("")
    add("| what | count |")
    add("|---|---|")
    counts = document["counts"]
    add("| their variants | %d |" % counts["their_variants"])
    add("| variants both readings hold | %d |" % counts["matched"])
    add("| our translated triples | %d |"
        % counts["our_translated_triples"])
    add("| our triples an independent reading reaches | %d |"
        % counts["our_triples_reached"])
    add("| places compared (`unsat` + `sat`) | %d |"
        % (totals["unsat"] + totals["sat"]))
    add("| places that AGREE (`unsat`) | %d |" % totals["unsat"])
    add("| places that DISAGREE (`sat`) | %d |" % totals["sat"])
    add("| places `unknown` at the ceiling | %d |" % totals["unknown"])
    add("| places their reading leaves UNDEFINED | %d |"
        % totals["undefined"])
    add("| places `refused` | %d |" % totals["refused"])
    add("| variants agreeing on every place compared | %d |" % agree)
    add("| variants with at least one disagreement | %d |" % disagree)
    add("")
    add("Table 2 -- per mnemonic, every outcome. `attested rows` is "
        "the corpus's own ledger rows behind those cells, carried from "
        "the model table.")
    add("")
    add("| mnem | variants | places | agree | disagree | unknown | "
        "undefined | refused | attested rows |")
    add("|---|---|---|---|---|---|---|---|---|")
    for mnem in sorted(per_mnem, key=lambda m: (-per_mnem[m]["sat"],
                                                -per_mnem[m]["unsat"],
                                                m)):
        row = per_mnem[mnem]
        add("| `%s` | %d | %d | %d | %d | %d | %d | %d | %d |"
            % (row["mnem"], row["variants"], row["places"],
               row["unsat"], row["sat"], row["unknown"],
               row["undefined"], row["refused"],
               row["attestation_ledger_rows"]))
    add("")
    add("Table 3 -- the disagreements, grouped by cause. Nothing here "
        "is decided: both readings are quoted and the ruling is the owner's.")
    add("")
    add("| cause | places | operand shapes | mnemonics |")
    add("|---|---|---|---|")
    for group in disagreements:
        add("| %s | %d | %s | %s |"
            % (group["cause_key"], group["count"],
               " ".join("`%s`" % s for s in sorted(group["shapes"])),
               " ".join("`%s`" % m["mnem"]
                        for m in sorted(group["mnems"],
                                        key=lambda m: m["mnem"]))))
    add("")
    for group in disagreements:
        add("### %s -- %d places" % (group["cause_key"],
                                     group["count"]))
        add("")
        for example in group["examples"]:
            add("`%s` -- our line `%s`, shape `%s` at width %s, the "
                "place `%s`:"
                % (example["variant"], example["line"],
                   example.get("shape"), example.get("key_width"),
                   example["place"]))
            add("")
            add("| reading | term, LITERAL (z3's printing of the "
                "simplified term, the register symbols keeping our "
                "reference's names) | its value at the counterexample |")
            add("|---|---|---|")
            add("| ours | `%s` | %s |"
                % (example["ours"],
                   example["ours_at_the_counterexample"] or "--"))
            add("| theirs | `%s` | %s |"
                % (example["theirs"],
                   example["theirs_at_the_counterexample"] or "--"))
            add("")
            if example["counterexample"]:
                add("the counterexample, LITERAL: %s"
                    % ", ".join("`%s` = `%s`" % (r["symbol"], r["text"])
                                for r in example["counterexample"]))
                add("")
    add("Table 4 -- the undefined regions, per mnemonic: the flags "
        "their reading writes Intel's undefined value into. `whole` is "
        "undefined on every input; `partial` is undefined on part of "
        "the input space, and the comparison was asked on the rest.")
    add("")
    add("| mnem | undefined on every input | undefined on part |")
    add("|---|---|---|")
    for row in regions:
        add("| `%s` | %s | %s |"
            % (row["mnem"], " ".join(row["whole"]) or "--",
               " ".join(row["partial"]) or "--"))
    add("")
    add("Table 5 -- the refusals, by cause.")
    add("")
    add("| cause | places | mnemonics |")
    add("|---|---|---|")
    for record in refusals:
        add("| %s | %d | %s |"
            % (record["reason"], record["count"],
               " ".join("`%s`" % m["mnem"]
                        for m in record["mnems"][:10])))
    add("")
    add("Wall clock %.1f s; peak resident memory %.1f MB against the "
        "stated %d MB ceiling and the named abort `%s`."
        % (seconds, peak, MEMORY_CEILING_MB, ABORT_NAME))
    return "\n".join(lines) + "\n"


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    flags = dict()
    for argument in argv[1:]:
        if argument.startswith("--"):
            if "=" in argument:
                key, value = argument[2:].split("=", 1)
            else:
                key, value = argument[2:], "1"
            flags[key] = value
    if len(args) != 4:
        print(__doc__)
        return 2
    semantics_folder, key_map_path, json_path, md_path = args
    workers = int(flags.get("workers", "3"))
    limit = int(flags.get("limit", "0"))
    started = time.time()
    results, document = run(semantics_folder, key_map_path, workers,
                            limit)
    per_mnem, totals, agree, disagree = tally(results)
    disagreements = group_disagreements(results)
    refusals = group_refusals(results)
    regions = undefined_regions(results)
    seconds = time.time() - started
    peak = check_memory("the end")
    out = {
        "meta": {
            "what": ("our reference's level-0 mappings against the "
                     "K-framework x86-64 semantics, per (mnem, operand "
                     "form, width) and per written place"),
            "their_source": semantics_folder,
            "their_licence": ("University of Illinois/NCSA Open Source "
                              "License; read from /sources, nothing "
                              "copied into this repository"),
            "key_map": key_map_path,
            "solver_ceiling_ms": SOLVER_MS,
            "wide_solver_ceiling_ms": WIDE_SOLVER_MS,
            "workers": workers,
            "seed_line": "%s %s" % (SEED_MNEM,
                                    ",".join(SEED_TEXTS[SEED_WIDTH])),
            "memory_ceiling_mb": MEMORY_CEILING_MB,
            "named_abort": ABORT_NAME,
            "peak_mb": peak,
            "seconds": seconds,
            "bit_index_convention": (
                "K's MInt indexes bits from the MOST significant end, "
                "half open: extractMInt(v, i, j) of an n-bit v is z3's "
                "Extract(n - 1 - i, n - j, v)"),
        },
        "counts": dict(document["counts"]),
        "totals": totals,
        "variants_agreeing_on_every_place": agree,
        "variants_with_a_disagreement": disagree,
        "per_mnem": [per_mnem[m] for m in sorted(per_mnem)],
        "disagreements": disagreements,
        "refusals": refusals,
        "undefined_regions": regions,
        "variants": sorted(results, key=lambda r: r["variant"]),
    }
    with open(json_path, "w") as handle:
        json.dump(out, handle, indent=1, sort_keys=True)
    with open(md_path, "w") as handle:
        handle.write(report(document, results, per_mnem, totals, agree,
                            disagree, disagreements, refusals, regions,
                            seconds, peak))
    print("variants %d, places %d" % (len(results),
                                      sum(totals.values())))
    for name in OUTCOMES:
        print("  %-10s %d" % (name, totals[name]))
    print("variants agreeing on every place compared: %d" % agree)
    print("variants with at least one disagreement: %d" % disagree)
    print("wall clock %.1f s, peak RSS %.1f MB" % (seconds, peak))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
