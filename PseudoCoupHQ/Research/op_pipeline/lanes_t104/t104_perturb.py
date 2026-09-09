#!/usr/bin/env python3
"""t104_perturb.py -- THE ACCEPTANCE the brief's deliverable 2 asks
for, stated as a property and measured: can the ORDER OF THE OPERANDS
of a commutative operator change the layer-5 text?

HOW IT IS MEASURED, rather than argued.  For every unit whose term the
gate proved, the layer-4 term is transcribed, and then a SECOND term is
built from it by permuting, at every node whose declaration kind is
commutative, that node's own arguments -- a random permutation with the
seed stated below, so the perturbation is reproducible and is not the
identity.  For an operator that carries a rounding mode the rounding
mode is left where it is and only the value arguments are permuted.
The two terms are the same computation and differ only in operand
order.  Both are put through `Term.normalize`.  The property holds for
a unit when the two texts are the SAME STRING.

WHY THIS AND NOT A SECOND WALK.  Task 79's acceptance ran three walks
in three processes and compared them; that measures the SOLVER's node
identity as a source of order.  This measures the operand order
DIRECTLY, which is what the brief names.

SEED 104.  A permutation is drawn per node from `random.Random(104)`,
advanced as the walk goes, so different nodes get different
permutations and the same run repeats exactly.

MEMORY BOUND: one canon40 shard at a time, two terms per unit.  Hard
cap 6 GB, checked every 200 units, named abort ABORT_MEMORY_T104.

WRITES: t104_perturbation.json

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

No operator token appears in this file.

Coding discipline: no compound one-liner statements.
"""

import glob
import json
import os
import random
import resource
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PIPELINE = os.path.dirname(HERE)
sys.path.insert(0, PIPELINE)

import z3                                                        # noqa: E402
import canonical_form as CF                                      # noqa: E402
import reference as R                                            # noqa: E402
import regate64_run as RG                                        # noqa: E402
import term as T                                                 # noqa: E402

OLD_STORE = os.path.join(PIPELINE, "term66_store")
OUT = os.path.join(PIPELINE, "t104_perturbation.json")

PROVED = "WRAPPED_TEXT_PROVED"
MEMORY_CAP_KB = 6 * 1024 * 1024
CHECK_EVERY = 200
SEED = 104


def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def check_memory(walked):
    used = peak_kb()
    if used > MEMORY_CAP_KB:
        raise SystemExit(
            "ABORT_MEMORY_T104: peak resident %d kB passed the stated "
            "cap of %d kB after %d units" % (used, MEMORY_CAP_KB,
                                             walked))
    return used


def permute_commutative(term, shuffler):
    """the same computation with every commutative node's own operands
    in a DIFFERENT order, built bottom-up with an explicit stack so a
    deep term cannot exhaust Python's own call stack.

    Returns (the new term, how many nodes were actually reordered)."""
    cache = {}
    moved = [0]
    stack = [(term, False)]
    while stack:
        current, expanded = stack.pop()
        key = current.get_id()
        if key in cache:
            continue
        if not z3.is_app(current):
            cache[key] = current
            continue
        if not expanded:
            stack.append((current, True))
            for index in range(current.num_args()):
                stack.append((current.arg(index), False))
            continue
        declaration = current.decl()
        kind = declaration.kind()
        pieces = []
        for index in range(current.num_args()):
            pieces.append(cache[current.arg(index).get_id()])
        if current.num_args() == 0:
            cache[key] = current
            continue
        if kind in T.COMMUTATIVE_OPERATORS:
            if len(pieces) > 1:
                order = list(range(len(pieces)))
                shuffler.shuffle(order)
                if order != sorted(order):
                    moved[0] = moved[0] + 1
                pieces = [pieces[i] for i in order]
        elif kind in T.ROUNDED_COMMUTATIVE_OPERATORS:
            if len(pieces) > 2:
                order = list(range(1, len(pieces)))
                shuffler.shuffle(order)
                if order != sorted(order):
                    moved[0] = moved[0] + 1
                pieces = pieces[:1] + [pieces[i] for i in order]
        cache[key] = declaration(*pieces)
    return cache[term.get_id()], moved[0]


def canon40_shards():
    out = []
    for lang in ["c", "cpp", "go", "rust", "swift"]:
        out.append(os.path.join(PIPELINE,
                                "canon40_wrapped_%s.json" % lang))
    out.append(os.path.join(PIPELINE, "canon40_interp.json"))
    pattern = os.path.join(PIPELINE, "canon40_regen_store", "*.json")
    out.extend(sorted(glob.glob(pattern)))
    return [path for path in out if os.path.exists(path)]


def old_shard_path(key):
    return os.path.join(OLD_STORE, key.replace("/", "__"))


def main():
    started = time.time()
    attached = RG.callee_units()
    readings = CF.runtime_answer_readings()
    reference = R.Reference(runtime_units=attached)
    maker = T.Term(reference=reference,
                   runtime_routines=CF.runtime_routine_names(readings),
                   runtime_units=attached,
                   runtime_answers=readings)
    shuffler = random.Random(SEED)

    paths = canon40_shards()
    total = len(paths)
    walked = 0
    nodes_reordered = 0
    units_with_a_reordered_node = 0
    disagreements = []
    refusals = []
    index = 0
    for path in paths:
        index = index + 1
        key = os.path.relpath(path, PIPELINE)
        sys.stdout.write("[%d/%d] %s\n" % (index, total, key))
        sys.stdout.flush()
        old_path = old_shard_path(key)
        if not os.path.exists(old_path):
            continue
        old = json.load(open(old_path))
        canon = json.load(open(path))
        units = canon.get("units") or {}
        for name in sorted(old["units"]):
            record = old["units"][name]
            if record.get("term_state") != "TERM":
                continue
            if not record.get("proved"):
                continue
            unit = dict(units[name])
            unit["unit"] = name
            transcription = maker.transcribe(unit)
            if transcription.out_term is None:
                refusals.append({"unit": name,
                                 "cause": "no OUT-0 term on the walk"})
                continue
            raw = transcription.out_term
            perturbed, moved = permute_commutative(raw, shuffler)
            nodes_reordered = nodes_reordered + moved
            if moved > 0:
                units_with_a_reordered_node = (
                    units_with_a_reordered_node + 1)
            try:
                plain = maker.normalize(raw)
                other = maker.normalize(perturbed)
            except Exception as problem:
                refusals.append({
                    "unit": name,
                    "cause": "%s: %s" % (type(problem).__name__,
                                         problem),
                })
                continue
            if plain != other:
                disagreements.append({
                    "unit": name,
                    "lang": record.get("lang"),
                    "commutative_nodes_reordered": moved,
                    "text_from_the_term_as_transcribed": plain,
                    "text_from_the_operand_permuted_term": other,
                })
            walked = walked + 1
            if walked % CHECK_EVERY == 0:
                check_memory(walked)
        old = None
        canon = None
        sys.stdout.write("   %d units checked, %d disagreements, "
                         "peak %d kB (%.0fs)\n"
                         % (walked, len(disagreements), peak_kb(),
                            time.time() - started))
        sys.stdout.flush()

    summary = {
        "units_checked": walked,
        "units_with_at_least_one_commutative_node_reordered":
            units_with_a_reordered_node,
        "commutative_nodes_reordered": nodes_reordered,
        "units_whose_text_disagrees": len(disagreements),
        "units_refused": len(refusals),
        "seed": SEED,
        "seconds": round(time.time() - started, 1),
        "peak_resident_kb": peak_kb(),
    }
    document = {
        "summary": summary,
        "disagreements": disagreements,
        "refusals": refusals,
    }
    handle = open(OUT, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    for name in sorted(summary):
        sys.stdout.write("   %-52s %s\n" % (name, summary[name]))
    sys.stdout.write("-- wrote %s\n" % OUT)
    sys.stdout.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())
