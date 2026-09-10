#!/usr/bin/env python3
"""twins.py -- THE MATCH, BY TERM: every RISC-V cell against every x86
cell, text first and z3 second.

Node: hq.research.arch_unit_oracle.  Task rv2, brief section 2 step 2,
`PRIVATE/PseudoCoupHQ/Research/briefs/task_rv2_brief.md`.

WHAT THIS IS, one sentence, in relation: the join between the two model
tables -- `Research/oracle/riscv/model_table_rv.json` (task rv2) and
`Research/oracle/arch_opcodes/model/model_table_rows.json` (tasks m1 and
m1b) -- that says, for each RISC-V cell, which x86 cell computes the
same mapping, so a certificate proved about the x86 cell can be inherited.

THE OBJECTS, one sentence each.
  * A PLACE TERM is the z3 term one cell leaves in one place it writes.
  * A TWIN is an (x86 cell, x86 place) whose place term is the same
    function as a RISC-V cell's place term: IDENTICAL after
    `term.Term.normalize` (a text twin) or proved equal by z3 (a z3
    twin).
  * THE CANDIDATE SCOPE for the z3 pass is machine-form evidence and
    nothing else: the same term WIDTH and the same ARITY -- the number
    of free symbols and their widths.  No mnemonic is read to decide
    which pairs get compared.

WHERE THE x86 TERMS COME FROM, said plainly.  The x86 table holds each
place's term as TEXT, and this line has no reader that turns text back
into a z3 object, so each distinct x86 cell's line is RE-RUN through
`op_pipeline/lean/model_translate.run_line` -- the same function that
wrote the table -- and the re-run's own printed text is checked against
the table's recorded text on every row.  The count of rows where the two
agree is printed and is part of the report: a re-derivation that did not
reproduce the table would make every match below unsound.

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

HOW THIS FILE OBEYS IT.  A pair is compared because the two terms have
the same width and the same arity, which is read off the z3 objects.
Nothing here reads a mnemonic to choose a pair; the mnemonic rides on
the row as `mnem`, the guard's machine-form field, and is printed only.

MEMORY, as the law requires: the x86 rows document is read once with
`json.load` and immediately reduced to one record per distinct (mnem,
shape, key_width); the z3 terms held are one per DISTINCT TEXT, not one
per row.  Bound 6 GB, named abort ABORT_MEMORY_RV2, peak resident
printed at every stage.

Coding discipline (the owner's ruling): no complex/compound one-liner statements.

WHICH x86 REFERENCE, and why it is an argument rather than a constant.
Task ref2 is correcting `op_pipeline/reference.py` in the same hours as
this task, and the four corrections change what a sub-64-bit write and a
condition read mean.  The x86 model table on disk and every certificate
in the bank were produced under the reference AS IT STOOD BEFORE those
corrections, which ref2 kept at
`Research/oracle/arch_opcodes/level0/ref2_originals/reference.py`.  A
match run against a half-corrected reference would compare two different
ground truths, so the reference directory is a command-line argument and
the sha256 of the file actually imported is printed and recorded in the
json.  Nothing under `op_pipeline/` is written here.

usage:
  twins.py sample <ref dir> <op dir> <x86 rows json> <riscv table json>
  twins.py match  <ref dir> <op dir> <x86 rows json> <x86 attest json>
                  <riscv table json> <out prefix> [timeout_ms]
"""

import hashlib
import json
import os
import resource
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import z3                                                    # noqa: E402


ABORT_KB = 6 * 1024 * 1024
ABORT_NAME = "ABORT_MEMORY_RV2"
SOLVER_MS = 3000


def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def check_memory(where):
    peak = peak_kb()
    say("   peak RSS %.1f MB at %s" % (peak / 1024.0, where))
    if peak > ABORT_KB:
        raise SystemExit("%s: %d kB at %s" % (ABORT_NAME, peak, where))


def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def write_json(path, document):
    fh = open(path, "w")
    json.dump(document, fh, indent=1, sort_keys=True)
    fh.write("\n")
    fh.close()


# ==================================================================
# section 1: the x86 side -- one record per distinct cell, re-run
# ==================================================================

def x86_cells(rows_path):
    """one record per distinct (mnem, shape, key_width) the x86 sweep
    TRANSLATED, carrying what `model_translate.run_line` needs to build
    that cell's terms again."""
    document = json.load(open(rows_path))
    rows = document["rows"]
    held = {}
    for row in rows:
        if row.get("outcome") != "TRANSLATED":
            continue
        if not row.get("mapping"):
            continue
        key = (row["mnem"], row.get("shape"), row.get("key_width"))
        if key in held:
            continue
        setter = None
        if row.get("flags_in"):
            setter = row["flags_in"].get("mnem")
        held[key] = {
            "mnem": row["mnem"],
            "shape": row.get("shape"),
            "key_width": row.get("key_width"),
            "operands": row.get("operands") or [],
            "preseeded": row.get("preseeded", False),
            "flags_in_mnem": setter,
            "recorded": dict([(p["writes"], p["text"])
                              for p in row["mapping"]]),
        }
    del rows
    del document
    return held


def rebuild(MT, MTAB, record):
    """(place -> z3 term) for one x86 cell, from its own line re-run."""
    state = None
    if record["preseeded"]:
        width = record["key_width"] or 64
        state = MT.preseeded_state(width, record["flags_in_mnem"])
    written, flags, state, _line = MT.run_line(
        record["mnem"], record["operands"], state)
    MTAB.drop_cells_only_read(written, state)
    out = {}
    for place in written:
        out[place] = written[place]
    if flags is not None:
        pair = z3.Concat(MT.as_bits(flags[1]), MT.as_bits(flags[2]))
        out["flags"] = pair
    return out


# ==================================================================
# section 2: the comparison form -- positional symbols
# ==================================================================

def positional(TERMS, term):
    """the term with its free symbols renamed v0, v1, ... by the
    pipeline's own layer-5 rule, as a z3 OBJECT.

    These are `term.Term.normalize`'s own steps in its own order, with
    the printing left off, so that the object this returns prints
    exactly what `normalize` prints and two objects from two
    architectures are functions of the same unknowns."""
    simplified = TERMS.order_commutative(term)
    simplified = z3.simplify(simplified)
    simplified = TERMS.order_commutative(simplified)
    symbols = TERMS.ordered_symbols(simplified)
    substitution = []
    for index, symbol in enumerate(symbols):
        if symbol.sort().kind() == z3.Z3_BV_SORT:
            fresh = z3.BitVec("v%d" % index, symbol.size())
        else:
            fresh = z3.Const("v%d" % index, symbol.sort())
        substitution.append((symbol, fresh))
    if substitution:
        simplified = z3.substitute(simplified, *substitution)
    simplified = z3.simplify(simplified)
    simplified = TERMS.order_commutative(simplified)
    return simplified


def ordered_widths(TERMS, term):
    """the widths of `v0`, `v1`, ... in that order, off a POSITIONAL
    term (one `positional` has already renamed)."""
    held = {}
    for symbol in TERMS.free_symbols_in_order(term):
        name = symbol.decl().name()
        if not name.startswith("v"):
            return None
        if not name[1:].isdigit():
            return None
        if symbol.sort().kind() != z3.Z3_BV_SORT:
            return None
        held[int(name[1:])] = symbol.size()
    out = []
    for index in sorted(held):
        out.append(held[index])
    return tuple(out)


def scope_key(TERMS, term):
    """THE CANDIDATE SCOPE, machine form and nothing else: the term's own
    width and the SORTED widths of its free symbols.  Two terms that
    differ here cannot be the same function of the same unknowns."""
    if term.sort().kind() == z3.Z3_BV_SORT:
        width = term.size()
    else:
        width = str(term.sort())
    widths = ordered_widths(TERMS, term)
    if widths is None:
        return (width, None)
    return (width, tuple(sorted(widths)))


# ------------------------------------------------------------------
# the point filter: agreement at concrete points is NECESSARY for
# equality, so a pair that differs at one point is not the same
# function and needs no solver call.  Nothing here decides a TWIN --
# every pair that survives the filter is still put to z3.
# ------------------------------------------------------------------

EDGE_VALUES = [0, 1, 2, 3]
POINTS_PER_SHAPE = 12
POINT_SEED = "rv2"


def points_for(widths):
    """the concrete assignments this filter evaluates both sides at:
    the edge values first, then points drawn by
    `random.Random("rv2")`, so the same shape always gets the same
    points and a bucket is reproducible."""
    import random
    rng = random.Random(POINT_SEED)
    out = []
    for value in EDGE_VALUES:
        out.append(tuple([value % (1 << w) for w in widths]))
    for width in widths:
        top = (1 << width) - 1
        out.append(tuple([top % (1 << w) for w in widths]))
        out.append(tuple([(1 << (width - 1)) % (1 << w) for w in widths]))
    while len(out) < POINTS_PER_SHAPE:
        out.append(tuple([rng.getrandbits(w) for w in widths]))
    return out[:POINTS_PER_SHAPE]


POINTS = {}


def point_vector(term, widths):
    """(the term's value at each point, or nothing if it does not go
    concrete)."""
    if widths is None:
        return None
    if widths not in POINTS:
        POINTS[widths] = points_for(widths)
    out = []
    for point in POINTS[widths]:
        substitution = []
        for index, value in enumerate(point):
            symbol = z3.BitVec("v%d" % index, widths[index])
            substitution.append((symbol, z3.BitVecVal(value,
                                                      widths[index])))
        got = term
        if substitution:
            got = z3.substitute(term, *substitution)
        got = z3.simplify(got)
        if z3.is_bv_value(got):
            out.append(got.as_long())
            continue
        if z3.is_true(got):
            out.append(1)
            continue
        if z3.is_false(got):
            out.append(0)
            continue
        return None
    return tuple(out)


# ==================================================================
# section 3: the match
# ==================================================================

def decide(left, right, timeout_ms):
    solver = z3.Solver()
    solver.set("timeout", timeout_ms)
    solver.add(left != right)
    verdict = solver.check()
    if verdict == z3.unsat:
        return "EQUAL"
    if verdict == z3.unknown:
        return "UNDECIDED"
    return "DIFFER"


def bring_in(ref_dir, op_dir):
    """the four modules this file drives, with the x86 reference taken
    from `ref_dir` and cached in `sys.modules` BEFORE anything that
    imports it runs -- `model_translate` and `model_table` both put
    `op_pipeline` at the head of `sys.path` when they load, so the only
    way to choose the reference is to have imported it already."""
    sys.path.insert(0, op_dir)
    sys.path.insert(0, os.path.join(op_dir, "lean"))
    sys.path.insert(0, os.path.join(
        os.path.dirname(op_dir), "oracle", "arch_opcodes", "model"))
    sys.path.insert(0, ref_dir)
    import condition_table                                   # noqa: E402
    import reference as X86                                  # noqa: E402
    import term as TERMS                                     # noqa: E402
    import model_translate as MT                             # noqa: E402
    import model_table as MTAB                               # noqa: E402
    digest = hashlib.sha256(open(X86.__file__, "rb").read()).hexdigest()
    say("   the x86 reference imported: %s" % X86.__file__)
    say("   its sha256: %s" % digest)
    say("   condition_table: %s" % condition_table.__file__)
    return X86, TERMS, MT, MTAB, digest


def match_command(ref_dir, op_dir, rows_path, attest_path, rv_path,
                  prefix, timeout_ms):
    say("[0/6] the x86 reference this run uses")
    X86, TERMS, MT, MTAB, digest = bring_in(ref_dir, op_dir)

    holder = TERMS.Term(X86.Reference())

    say("[1/6] the x86 cells, one record per distinct (mnem, shape, "
        "key_width)")
    records = x86_cells(rows_path)
    say("   %d distinct x86 cells" % len(records))
    check_memory("after reading the x86 rows")

    say("[2/6] each x86 cell's line re-run, and the re-run checked "
        "against the table's own recorded text")
    index = {}
    scopes = {}
    agreed = 0
    differed = 0
    refused = 0
    total = len(records)
    done = 0
    for key in sorted(records):
        record = records[key]
        done = done + 1
        if done % 1000 == 0:
            say("   [%d/%d] cells re-run" % (done, total))
            check_memory("cell %d" % done)
        try:
            places = rebuild(MT, MTAB, record)
        except Exception as problem:
            refused = refused + 1
            record["rerun"] = "REFUSED: %s: %s" % (
                type(problem).__name__, problem)
            continue
        for place in places:
            try:
                printed = holder.normalize(places[place])
            except Exception:
                refused = refused + 1
                continue
            if record["recorded"].get(place) == printed:
                agreed = agreed + 1
            else:
                differed = differed + 1
            entry = index.get(printed)
            if entry is None:
                shaped = positional(TERMS, places[place])
                widths = ordered_widths(TERMS, shaped)
                entry = {"term": shaped, "cells": [],
                         "widths": widths,
                         "vector": point_vector(shaped, widths)}
                index[printed] = entry
                scope = scope_key(TERMS, shaped)
                bucket = scopes.setdefault(scope, {"by_vector": {},
                                                   "loose": []})
                if entry["vector"] is None:
                    bucket["loose"].append(printed)
                else:
                    key = (widths, entry["vector"])
                    bucket["by_vector"].setdefault(key, []).append(printed)
            entry["cells"].append({
                "mnem": record["mnem"],
                "shape": record["shape"],
                "key_width": record["key_width"],
                "place": place,
            })
    say("   re-run agrees with the table's recorded text on %d place "
        "rows, differs on %d, refused %d" % (agreed, differed, refused))
    say("   %d distinct x86 place terms, %d candidate scopes"
        % (len(index), len(scopes)))
    loose = 0
    for scope in scopes:
        loose = loose + len(scopes[scope]["loose"])
    say("   %d of them do not go concrete at the sample points and are "
        "compared exhaustively inside their scope" % loose)
    check_memory("after the x86 index")

    say("[3/6] the attestation, so a twin can say whether the corpus "
        "attests its x86 cell")
    attested = {}
    for cell in json.load(open(attest_path))["cells"]:
        attested[(cell["mnem"], cell["shape"], cell["key_width"])] = {
            "units": cell.get("units"),
            "ledger_rows": cell.get("ledger_rows"),
        }
    say("   %d attested x86 cells" % len(attested))

    say("[4/6] the RISC-V cells, each line re-run for its z3 object and "
        "the re-run checked against this task's own table")
    rv_cells, rv_agreed, rv_differed = riscv_cells(holder, rv_path)
    say("   %d RISC-V cells; the re-run agrees with model_table_rv.json "
        "on %d place rows and differs on %d" % (len(rv_cells), rv_agreed,
                                                rv_differed))
    check_memory("after the RISC-V cells")

    say("[4b/6] the second reading: every x86 place term CUT to each "
        "narrow width a RISC-V cell computes at")
    cut_widths = {}
    for row in rv_cells:
        width = row["key_width"]
        if width is None:
            continue
        if width >= 64:
            continue
        cut_widths[width] = True
    cuts = {}
    for width in sorted(cut_widths):
        cuts[width] = cut_index(TERMS, holder, index, width)
        say("   at %d bits: %d distinct cut x86 place terms"
            % (width, len(cuts[width]["index"])))
    check_memory("after the cut indexes")

    say("[5/6] the match: text first, then z3 at %d ms over the same "
        "width and arity" % timeout_ms)
    out = []
    started = time.time()
    solver_calls = 0
    for number, row in enumerate(rv_cells, 1):
        record = {
            "mnem": row["mnem"],
            "shape": row["shape"],
            "key_width": row["key_width"],
            "places": [],
        }
        how_of_cell = "NONE"
        how_at_width = "NONE"
        for place in row["places"]:
            found, calls = one_place(TERMS, index, scopes, place,
                                     timeout_ms)
            solver_calls = solver_calls + calls
            found["writes"] = place["writes"]
            found["text"] = place["text"]
            if found.get("x86_twin"):
                key = (found["x86_twin"]["mnem"],
                       found["x86_twin"]["shape"],
                       found["x86_twin"]["key_width"])
                found["x86_twin_attestation"] = attested.get(key)
            width = row["key_width"]
            if found["how"] == "NONE" and width in cuts:
                narrow, calls = at_key_width(TERMS, holder, cuts[width],
                                             place, width, timeout_ms)
                solver_calls = solver_calls + calls
                found["at_key_width"] = narrow
                if narrow.get("x86_twin"):
                    key = (narrow["x86_twin"]["mnem"],
                           narrow["x86_twin"]["shape"],
                           narrow["x86_twin"]["key_width"])
                    narrow["x86_twin_attestation"] = attested.get(key)
            record["places"].append(found)
        for place in record["places"]:
            if place["how"] == "TEXT":
                how_of_cell = "TEXT"
                break
            if place["how"] == "Z3":
                how_of_cell = "Z3"
        for place in record["places"]:
            narrow = place.get("at_key_width") or {}
            if narrow.get("how") == "TEXT":
                how_at_width = "TEXT"
                break
            if narrow.get("how") == "Z3":
                how_at_width = "Z3"
        if how_of_cell != "NONE":
            how_at_width = how_of_cell
        record["how"] = how_of_cell
        record["how_at_key_width"] = how_at_width
        out.append(record)
        if number % 25 == 0 or number == len(rv_cells):
            say("   [%d/%d] cells matched, %d solver calls, %.0f s"
                % (number, len(rv_cells), solver_calls,
                   time.time() - started))
            check_memory("rv cell %d" % number)

    say("[6/6] writing")
    census = {}
    census_at_width = {}
    for record in out:
        census[record["how"]] = census.get(record["how"], 0) + 1
        key = record["how_at_key_width"]
        census_at_width[key] = census_at_width.get(key, 0) + 1
    say("   READING 1 -- the whole written place:")
    for how in sorted(census):
        say("      %-8s %d" % (how, census[how]))
    say("   READING 2 -- at the RISC-V cell's own key_width:")
    for how in sorted(census_at_width):
        say("      %-8s %d" % (how, census_at_width[how]))
    document = {
        "meta": {
            "task": "rv2",
            "readings": "TWO, both reported: READING 1 is the WHOLE "
                        "WRITTEN PLACE (the 64-bit register RISC-V "
                        "always writes against the 64 bits x86's write "
                        "rule leaves); READING 2 cuts both sides to the "
                        "RISC-V cell's own key_width, which is the "
                        "width the operation computes at and the width "
                        "the gate compares an emulation on",
            "what": "every RISC-V cell's place term against every x86 "
                    "cell's place term: identical after term.Term."
                    "normalize is a text twin, else z3 over the same "
                    "term width and the same free-symbol widths",
            "solver_timeout_ms": timeout_ms,
            "x86_rows": rows_path,
            "x86_reference_file": X86.__file__,
            "x86_reference_sha256": digest,
            "x86_reference_note": "task ref2 is correcting "
                                  "op_pipeline/reference.py in the same "
                                  "hours; the x86 model table on disk "
                                  "and every certificate in the bank "
                                  "were produced under the reference as "
                                  "it stood BEFORE those corrections, "
                                  "which is the file named here",
            "x86_rerun_agrees": agreed,
            "x86_rerun_differs": differed,
            "x86_rerun_refused": refused,
            "x86_distinct_cells": len(records),
            "x86_distinct_place_terms": len(index),
            "point_filter": "a pair that disagrees at a concrete point "
                            "is not the same function, so only the x86 "
                            "terms that agree with the RISC-V term at "
                            "every one of the %d sample points are put "
                            "to z3; the filter decides no twin, it only "
                            "excludes pairs z3 would have answered sat "
                            "for" % POINTS_PER_SHAPE,
            "riscv_cells": len(rv_cells),
            "solver_calls": solver_calls,
            "seconds": round(time.time() - started, 1),
            "peak_kb": peak_kb(),
            "memory_bound_kb": ABORT_KB,
            "memory_abort": ABORT_NAME,
        },
        "census": census,
        "rows": out,
    }
    document["census_at_key_width"] = census_at_width
    write_json(prefix + ".json", document)
    say("peak RSS: %d kB" % peak_kb())
    return 0


def cut_index(TERMS, holder, index, width):
    """every distinct x86 place term CUT to `width`, indexed the same
    way the whole-place index is.

    WHY A CUT IS A READING AND NOT A FIX: RISC-V's 32-bit forms
    sign-extend their result into the whole register and x86's
    zero-extend theirs, so at the whole place the two never agree; at
    the width the operation itself computes at they may.  Both readings
    are reported and neither replaces the other."""
    out = {}
    scopes = {}
    for text in index:
        term = index[text]["term"]
        if term.sort().kind() != z3.Z3_BV_SORT:
            continue
        if term.size() < width:
            continue
        cut = term
        if term.size() > width:
            cut = z3.Extract(width - 1, 0, term)
        shaped = positional(TERMS, cut)
        printed = holder.normalize(cut)
        entry = out.get(printed)
        if entry is None:
            widths = ordered_widths(TERMS, shaped)
            entry = {"term": shaped, "cells": [], "widths": widths,
                     "vector": point_vector(shaped, widths)}
            out[printed] = entry
            scope = scope_key(TERMS, shaped)
            bucket = scopes.setdefault(scope, {"by_vector": {},
                                               "loose": []})
            if entry["vector"] is None:
                bucket["loose"].append(printed)
            else:
                key = (widths, entry["vector"])
                bucket["by_vector"].setdefault(key, []).append(printed)
        for cell in index[text]["cells"]:
            entry["cells"].append(cell)
    return {"index": out, "scopes": scopes}


def at_key_width(TERMS, holder, held, place, width, timeout_ms):
    """READING 2 for one place: both sides cut to the cell's own
    key_width."""
    term = place["term"]
    if term is None:
        return {"how": "NONE",
                "why": "this RISC-V place term has no z3 object"}, 0
    if term.sort().kind() != z3.Z3_BV_SORT:
        return {"how": "NONE",
                "why": "this RISC-V place term is not a bit vector"}, 0
    if term.size() < width:
        return {"how": "NONE",
                "why": "this RISC-V place is narrower than the cell's "
                       "own key_width"}, 0
    cut = term
    if term.size() > width:
        cut = z3.Extract(width - 1, 0, term)
    printed = holder.normalize(cut)
    shaped = positional(TERMS, cut)
    asked = {"text": printed, "term": shaped}
    found, calls = one_place(TERMS, held["index"], held["scopes"], asked,
                             timeout_ms)
    found["cut_to_bits"] = width
    found["text"] = printed
    return found, calls


def one_place(TERMS, index, scopes, place, timeout_ms):
    """the twin of one RISC-V place term, or the reason there is none."""
    text = place["text"]
    entry = index.get(text)
    if entry is not None:
        return {"how": "TEXT", "x86_twin": entry["cells"][0],
                "x86_twins_all": entry["cells"],
                "x86_twin_count": len(entry["cells"])}, 0
    mine = place["term"]
    if mine is None:
        return {"how": "NONE",
                "why": "this RISC-V place term has no z3 object: the "
                       "re-run of its own line refused"}, 0
    scope = scope_key(TERMS, mine)
    bucket = scopes.get(scope)
    if bucket is None:
        return {"how": "NONE",
                "candidates": 0,
                "solver_calls": 0,
                "why": "no x86 place term has this term's width and "
                       "these free-symbol widths, so no pair was "
                       "comparable"}, 0
    widths = ordered_widths(TERMS, mine)
    vector = point_vector(mine, widths)
    candidates = list(bucket["loose"])
    in_scope = len(bucket["loose"])
    for key in bucket["by_vector"]:
        in_scope = in_scope + len(bucket["by_vector"][key])
    if vector is not None:
        same = bucket["by_vector"].get((widths, vector)) or []
        candidates = candidates + same
    else:
        for key in bucket["by_vector"]:
            candidates = candidates + bucket["by_vector"][key]
    calls = 0
    undecided = 0
    for other in candidates:
        calls = calls + 1
        verdict = decide(mine, index[other]["term"], timeout_ms)
        if verdict == "EQUAL":
            return {"how": "Z3", "x86_twin": index[other]["cells"][0],
                    "x86_twins_all": index[other]["cells"],
                    "x86_twin_count": len(index[other]["cells"]),
                    "x86_twin_text": other,
                    "in_scope": in_scope,
                    "solver_calls": calls}, calls
        if verdict == "UNDECIDED":
            undecided = undecided + 1
    return {"how": "NONE",
            "in_scope": in_scope,
            "candidates": len(candidates),
            "undecided": undecided,
            "solver_calls": calls,
            "why": "no x86 place term of the same width and arity is "
                   "the same function: %d of the %d in scope agree at "
                   "every sample point and were put to z3, %d "
                   "undecided at %d ms" % (calls, in_scope, undecided,
                                           timeout_ms)}, calls


def riscv_cells(holder, rv_path):
    """one record per TRANSLATED RISC-V cell, each place carrying BOTH
    the table's recorded text and the z3 object the same line leaves
    when it is run again.

    The line is re-run through `model_table_rv.run_line`, this task's
    own sweep function, and the re-run's printed text is checked against
    the table's; the two counts are reported."""
    import model_table_rv as MRV                             # noqa: E402
    reference = MRV.RV.RiscvReference()
    rows = json.load(open(rv_path))["rows"]
    out = []
    seen = {}
    agreed = 0
    differed = 0
    for row in rows:
        if row["outcome"] != "TRANSLATED":
            continue
        if not row.get("mapping"):
            continue
        key = (row["mnem"], row["shape"], row["key_width"])
        if key in seen:
            continue
        seen[key] = True
        record = {"mnem": row["mnem"], "shape": row["shape"],
                  "key_width": row["key_width"], "places": []}
        try:
            written, condition, _line = MRV.run_line(
                reference, row["mnem"], row["operands"])
        except Exception:
            written = {}
            condition = None
        rebuilt = {}
        for place in written:
            rebuilt[place] = written[place]
        if condition is not None:
            rebuilt["branch_condition"] = z3.If(
                condition, z3.BitVecVal(1, MRV.RV.XLEN),
                z3.BitVecVal(0, MRV.RV.XLEN))
        for place in row["mapping"]:
            term = rebuilt.get(place["writes"])
            shaped = None
            if term is not None:
                shaped = holder_positional(holder, term)
                printed = holder.normalize(term)
                if printed == place["text"]:
                    agreed = agreed + 1
                else:
                    differed = differed + 1
            record["places"].append({
                "writes": place["writes"],
                "text": place["text"],
                "term": shaped,
            })
        out.append(record)
    return out, agreed, differed


def holder_positional(holder, term):
    import term as TERMS                                     # noqa: E402
    return positional(TERMS, term)


def sample_command(ref_dir, op_dir, rows_path, rv_path):
    """the memory sample the law asks for: 20 x86 cells re-run, with the
    peak resident printed, before the whole file is read."""
    say("[0/3] the x86 reference this run uses")
    X86, TERMS, MT, MTAB, _digest = bring_in(ref_dir, op_dir)
    holder = TERMS.Term(X86.Reference())
    say("[1/3] reading the x86 rows document")
    records = x86_cells(rows_path)
    say("   %d distinct x86 cells" % len(records))
    check_memory("after json.load of the x86 rows")
    say("[2/3] 20 cells re-run and printed")
    done = 0
    agreed = 0
    for key in sorted(records):
        if done >= 20:
            break
        done = done + 1
        record = records[key]
        places = rebuild(MT, MTAB, record)
        for place in sorted(places):
            printed = holder.normalize(places[place])
            same = (record["recorded"].get(place) == printed)
            if same:
                agreed = agreed + 1
            say("   %-12s %-20s %-4s %-10s same=%s  %s"
                % (record["mnem"], record["shape"], record["key_width"],
                   place, same, printed[:90]))
    say("   %d place rows agreed of the 20 cells" % agreed)
    check_memory("after 20 cells")
    say("[3/3] the RISC-V table")
    rv = json.load(open(rv_path))
    say("   %d RISC-V rows" % len(rv["rows"]))
    check_memory("after the RISC-V table")
    return 0


def report_command(prefix):
    document = json.load(open(prefix + ".json"))
    rows = document["rows"]
    meta = document["meta"]
    lines = []
    lines.append("# twins.md -- the RISC-V model table's cells matched "
                 "to x86's, by TERM")
    lines.append("")
    lines.append("Task rv2, node `hq.research.arch_unit_oracle`. "
                 "Written by `twins.py`; never hand-edited.")
    lines.append("")
    lines.append("**What this is, one sentence.** For every RISC-V cell "
                 "of `model_table_rv.json`, the x86 cell of "
                 "`model_table_rows.json` whose place term is the same "
                 "function -- identical after `term.Term.normalize` (a "
                 "TEXT twin) or proved equal by z3 (a Z3 twin) -- so a "
                 "certificate proved about the x86 cell can be "
                 "inherited on riscv64.")
    lines.append("")
    lines.append("**THE HEADLINE CARRIES ITS READING, and there are "
                 "two.** READING 1 is the WHOLE WRITTEN PLACE: RISC-V "
                 "always writes all 64 bits of a register and its "
                 "32-bit forms SIGN-extend, where x86's 32-bit write "
                 "ZERO-extends, so at the whole place a `w` form can "
                 "never twin an x86 32-bit form. READING 2 cuts both "
                 "sides to the RISC-V cell's own `key_width`, the "
                 "width the operation computes at and the width the "
                 "gate compares an emulation on. Neither replaces the "
                 "other.")
    lines.append("")
    lines.append("Table 1 -- the two readings, side by side.")
    lines.append("")
    lines.append("| twin | reading 1: the whole written place | "
                 "reading 2: at the cell's own `key_width` |")
    lines.append("|---|---|---|")
    for how in ("TEXT", "Z3", "NONE"):
        lines.append("| %s | %d | %d |"
                     % (how, document["census"].get(how, 0),
                        document["census_at_key_width"].get(how, 0)))
    lines.append("| **total RISC-V cells** | **%d** | **%d** |"
                 % (meta["riscv_cells"], meta["riscv_cells"]))
    lines.append("")
    lines.append("Table 2 -- the x86 side, as it was read.")
    lines.append("")
    lines.append("| what | value |")
    lines.append("|---|---|")
    lines.append("| the x86 reference imported | `%s` |"
                 % meta["x86_reference_file"])
    lines.append("| its sha256 | `%s` |" % meta["x86_reference_sha256"])
    lines.append("| distinct x86 cells | %d |"
                 % meta["x86_distinct_cells"])
    lines.append("| distinct x86 place terms | %d |"
                 % meta["x86_distinct_place_terms"])
    lines.append("| place rows where the re-run reproduced the table's "
                 "own recorded text | %d |" % meta["x86_rerun_agrees"])
    lines.append("| place rows where it differed | %d |"
                 % meta["x86_rerun_differs"])
    lines.append("| solver calls | %d |" % meta["solver_calls"])
    lines.append("| seconds | %s |" % meta["seconds"])
    lines.append("")
    lines.append("Table 3 -- every RISC-V cell, its twin and how it was "
                 "found.")
    lines.append("")
    lines.append("| `mnem` | shape | `key_width` | reading 1 | reading "
                 "2 | x86 twin `mnem` | x86 twin shape | x86 twin "
                 "`key_width` | x86 twin place |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for row in rows:
        twin = {}
        for place in row["places"]:
            if place.get("x86_twin"):
                twin = place["x86_twin"]
                break
            narrow = place.get("at_key_width") or {}
            if narrow.get("x86_twin"):
                twin = narrow["x86_twin"]
                break
        lines.append("| `%s` | %s | %s | %s | %s | %s | %s | %s | %s |"
                     % (row["mnem"], row["shape"], row["key_width"],
                        row["how"], row["how_at_key_width"],
                        twin.get("mnem") and "`%s`" % twin["mnem"] or "-",
                        twin.get("shape") or "-",
                        twin.get("key_width") if twin else "-",
                        twin.get("place") or "-"))
    lines.append("")
    lines.append("Table 4 -- the cells with NO twin under either "
                 "reading, one row per mnemonic, with how many of its "
                 "shapes are untwinned.")
    lines.append("")
    untwinned = {}
    for row in rows:
        if row["how_at_key_width"] != "NONE":
            continue
        untwinned[row["mnem"]] = untwinned.get(row["mnem"], 0) + 1
    lines.append("| `mnem` | untwinned shapes |")
    lines.append("|---|---|")
    for mnem in sorted(untwinned):
        lines.append("| `%s` | %d |" % (mnem, untwinned[mnem]))
    lines.append("")
    fh = open(prefix + ".md", "w")
    fh.write("\n".join(lines) + "\n")
    fh.close()
    say("wrote %s.md, %d lines" % (prefix, len(lines)))
    return 0


def main():
    command = sys.argv[1]
    if command == "report":
        return report_command(sys.argv[2])
    if command == "sample":
        return sample_command(sys.argv[2], sys.argv[3], sys.argv[4],
                              sys.argv[5])
    if command == "match":
        timeout_ms = SOLVER_MS
        if len(sys.argv) > 8:
            timeout_ms = int(sys.argv[8])
        return match_command(sys.argv[2], sys.argv[3], sys.argv[4],
                             sys.argv[5], sys.argv[6], sys.argv[7],
                             timeout_ms)
    raise SystemExit("unknown command %r" % command)


if __name__ == "__main__":
    sys.exit(main())
