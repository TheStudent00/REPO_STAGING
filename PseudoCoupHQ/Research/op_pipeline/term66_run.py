#!/usr/bin/env python3
"""term66_run.py -- the driver that runs `term.py` (node 0_3_5_6) over
the CANON40 proved population, gates both routes with `gate.py`, and
normalizes every proved term with the corrected `Term.normalize`.

POPULATION: the 30,324 units canon40 records as WRAPPED_TEXT_PROVED,
across `canon40_wrapped_{c,cpp,go,rust,swift}.json`,
`canon40_interp.json` and `canon40_regen_store/*.json`.  A canon40
REFUSED or GATE_DISPROVED unit has no proved wrapped text and is not
transcribed; the 754 of them are counted per shard, never silently
dropped.

WHAT IS DIFFERENT FROM `term65_run.py`, said out loud.

1. THE CANON IS canon40, not canon39.  Task 78 corrected the
   destination rule for a transfer into the compiler's own runtime: the
   ledger now writes one row per register family the ATTACHED CALLEE's
   own body changes, read off that body.  `runtime_callee` rows over
   the 31,078 attempted units went from 608 to 49,362 (log_185 section
   5.1), so the ledgers this run transcribes are materially different
   objects and the terms cannot be carried over.
2. THE VERDICT IS RE-DERIVED, not read from a bank.  `term65_run.py`
   read task 64's `regate64_store` because that store was gated over
   the same canon39 ledgers.  No such store exists for canon40 and
   reusing one would be reading a verdict about a different term, so
   this run asks `gate.py` itself: `prove_term_against_ship` first,
   then `prove_term_against_text` when the ship route did not prove.
3. `Term.normalize` is task 79's corrected rule -- the arguments of a
   commutative operator ordered by a key computed from the arguments
   themselves, applied after the first simplification and again after
   the positional renaming.

ONE PROCESS.  Everything below runs in this single process; there is no
pool of workers and no second interpreter.  The run is resumable:
`term66_state.json` names the shards already written.

MEMORY BOUND, stated as the round requires: one canon40 shard is
opened, walked and dropped before the next; the largest on disk is
under 6 MB.  The bound is 6 GB resident, checked after every shard,
with the named abort `ABORT_MEMORY`.

WHAT IS REUSED RATHER THAN COPIED.  `regate64_run.callee_units`,
`.count_call_lines`, `.count_branch_lines` and `.why_no_term` are
called, not re-typed; `regate64_run.py` is round 13's driver and is
neither edited nor re-run here.

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

No operator token appears in this file.  A unit's `operator` field is
carried onto its record as a DISPLAY LABEL on the member and is never
read for grouping, pairing or candidate selection.

Coding discipline: no compound one-liner statements.

usage:
  term66_run.py [budget seconds]
"""

import glob
import json
import os
import resource
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canonical_form as CF                                      # noqa: E402
import gate as G                                                 # noqa: E402
import reference as R                                            # noqa: E402
import regate64_run as RG                                        # noqa: E402
import term as T                                                 # noqa: E402

STORE = os.path.join(HERE, "term66_store")
STATE = os.path.join(HERE, "term66_state.json")

PROVED = "WRAPPED_TEXT_PROVED"
MEMORY_CAP_KB = 6 * 1024 * 1024


def check_memory():
    used = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if used > MEMORY_CAP_KB:
        raise SystemExit(
            "ABORT_MEMORY: peak resident %d kB passed the stated cap "
            "of %d kB" % (used, MEMORY_CAP_KB))
    return used


def shards():
    """the canon40 shards, in the order canon39's were walked."""
    out = []
    for lang in ["c", "cpp", "go", "rust", "swift"]:
        out.append(os.path.join(HERE,
                                "canon40_wrapped_%s.json" % lang))
    out.append(os.path.join(HERE, "canon40_interp.json"))
    pattern = os.path.join(HERE, "canon40_regen_store", "*.json")
    out.extend(sorted(glob.glob(pattern)))
    return [path for path in out if os.path.exists(path)]


def load_state():
    if not os.path.exists(STATE):
        return {"done": [], "started": time.time()}
    return json.load(open(STATE))


def save_state(state):
    handle = open(STATE, "w")
    json.dump(state, handle, indent=1, sort_keys=True)
    handle.close()


def call_targets_of(unit):
    """the targets this body transfers to, read off the wrapped text's
    own body lines.  Machine form: the text after the mnemonic, with
    any relocation note stripped.  The shape of the target -- a
    positional label, a named routine, an indirect read -- is what the
    audit groups on, never a token we chose."""
    found = []
    for raw in unit.get("body_verbatim") or []:
        text = raw.split("!!")[0].strip()
        if text == "":
            continue
        head = text.split(" ", 1)[0]
        if head != "call":
            continue
        if " " not in text:
            found.append("")
            continue
        found.append(text.split(" ", 1)[1].strip())
    return found


def runtime_rows_of(unit):
    """how many ledger rows name a runtime callee, and which callees.

    This is the input side task 78 changed: canon39 wrote at most one
    such row per transfer and often none, canon40 writes one per
    register family the attached callee's own body changes."""
    total = 0
    callees = []
    for row in unit.get("ledger") or []:
        producer = row.get("produced_by") or {}
        if producer.get("kind") != "runtime_callee":
            continue
        total = total + 1
        name = producer.get("callee")
        if name is not None and name not in callees:
            callees.append(name)
    return total, sorted(callees)


def one_unit(maker, gate, name, unit):
    """one canon40 unit -> its layer-4 / layer-5 record.

    The record's shape is `term65_run.one_unit`'s, so the two rounds
    join on the unit name and the four states are counted by the same
    function."""
    rows, callees = runtime_rows_of(unit)
    record = {
        "unit": name,
        "lang": unit.get("lang"),
        "population": unit.get("population"),
        "operator": unit.get("operator"),
        "arrival_annotation": unit.get("arrival_annotation"),
        "arrival_families": list(unit.get("arrival_families") or []),
        "result_family": unit.get("result_family"),
        "result_width": unit.get("result_width"),
        "runtime_callee_rows": rows,
        "runtime_callees": callees,
    }
    unit = dict(unit)
    unit["unit"] = name
    record["branch_lines"] = RG.count_branch_lines(unit)
    record["call_lines"] = RG.count_call_lines(unit)
    record["call_targets"] = call_targets_of(unit)
    walked = maker.transcribe(unit)
    record["holes"] = walked.holes
    record["cascades"] = walked.cascades
    record["slot_disagreements"] = walked.slot_disagreements
    record["relink_refusal"] = walked.refused
    record["verdict_source"] = (
        "gated by this run -- gate.py over canon40, both routes")
    if walked.refused is not None:
        record["term_state"] = "NO_TERM"
        record["why_no_term"] = "the relink refused: %s" % walked.refused
        record["proved"] = False
        return record
    if walked.out_term is None:
        record["term_state"] = "NO_TERM"
        record["why_no_term"] = RG.why_no_term(walked)
        record["proved"] = False
        return record
    record["term_state"] = "TERM"
    first = gate.prove_term_against_ship(walked.out_term, unit)
    record["verdict_ship"] = first.as_dict()
    verdict = first
    if not first.proved():
        second = gate.prove_term_against_text(walked.out_term, unit)
        record["verdict_text"] = second.as_dict()
        if second.proved():
            verdict = second
    record["outcome"] = verdict.outcome
    record["route"] = verdict.route
    record["reason"] = verdict.reason
    record["proved"] = verdict.proved()
    if record["proved"]:
        add_layer5(maker, record, walked)
        return record
    record["layer5_normalized_text"] = None
    record["layer5_withdrawn"] = (
        "a term that does not prove is withdrawn, not kept as a "
        "weaker key")
    return record


def add_layer5(maker, record, walked):
    """layer 5, computed ONLY for a unit whose term the gate proved,
    by task 79's corrected rule."""
    try:
        record["layer5_normalized_text"] = maker.normalize(
            walked.out_term)
    except Exception as problem:
        record["layer5_normalized_text"] = None
        record["layer5_refusal"] = "%s: %s" % (
            type(problem).__name__, problem)
    return record


def run(budget_seconds):
    if not os.path.isdir(STORE):
        os.makedirs(STORE)
    state = load_state()
    done = set(state["done"])
    attached = RG.callee_units()
    readings = CF.runtime_answer_readings()
    reference = R.Reference(runtime_units=attached)
    # THE READINGS ARE PASSED EXPLICITLY.  `Term` would read the same
    # file itself, but the relink's inputs are what task 83 fixed and
    # an argument stated here is an argument a reader can check.
    maker = T.Term(reference=reference,
                   runtime_routines=CF.runtime_routine_names(readings),
                   runtime_units=attached,
                   runtime_answers=readings)
    gate = G.Gate(reference=reference)
    started = time.time()
    every = shards()
    for path in every:
        key = os.path.relpath(path, HERE)
        if key in done:
            continue
        if time.time() - started > budget_seconds:
            print("budget spent; %d shards still to walk"
                  % (len(every) - len(done)))
            sys.stdout.flush()
            return False
        document = json.load(open(path))
        out = {}
        not_proved = 0
        for name, unit in sorted(document.get("units", {}).items()):
            if unit.get("outcome") != PROVED:
                not_proved = not_proved + 1
                continue
            out[name] = one_unit(maker, gate, name, unit)
        written = os.path.join(STORE, key.replace("/", "__"))
        handle = open(written, "w")
        json.dump({"shard": key,
                   "canon40_not_proved_not_transcribed": not_proved,
                   "units": out}, handle, sort_keys=True)
        handle.close()
        done.add(key)
        state["done"] = sorted(done)
        save_state(state)
        peak = check_memory()
        print("%s: %d transcribed, %d canon40-not-proved skipped, "
              "peak %d kB (%.0fs)"
              % (key, len(out), not_proved, peak,
                 time.time() - started))
        sys.stdout.flush()
    print("all %d shards walked" % len(done))
    return True


if __name__ == "__main__":
    budget = 100000
    if len(sys.argv) > 1:
        budget = int(sys.argv[1])
    finished = run(budget)
    if not finished:
        sys.exit(3)
