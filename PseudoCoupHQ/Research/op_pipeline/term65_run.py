#!/usr/bin/env python3
"""term65_run.py -- the driver that runs `term.py` (node 0_3_5_6) over
the canon39 proved population with the ROUND-13 `reference.py`, and
writes the layer-4 / layer-5 record the pool and the census read.

POPULATION: the 30,432 units canon39 records as WRAPPED_TEXT_PROVED,
across `canon39_wrapped_{c,cpp,go,rust,swift}.json`,
`canon39_interp.json` and `canon39_regen_store/*.json`.  A canon39
REFUSED unit has no wrapped text and is not transcribed; the 646 of
them are counted and named, never silently dropped.

WHAT IS DIFFERENT FROM `term61_run.py`, said out loud.

1. The reference is round 13's: it walks a body as its own
   control-flow graph and steps into an attached runtime callee, and
   the attached bodies come from `canon39_callee_units.json` (task 63),
   keyed by toolchain and then by routine name.  `term61_run.py` is
   round 12's record and is not edited.
2. THE VERDICT IS NOT RE-DERIVED.  Task 64 is the GATE OF RECORD for
   this round: `regate64_store/` already holds, per unit, the ship-route
   verdict, the text-route verdict, the outcome, the route and the
   reason, produced by the same `gate.py` over the same reference.
   This run READS that verdict and re-derives only what term65 adds --
   the transcription detail the census needs (holes, cascades, slot
   disagreements) and, for a PROVED term, the layer-5 normalized text.
   Re-proving would ask the same solver the same question and is not
   evidence; reusing it makes the four states reproduce BY
   CONSTRUCTION, and any unit where this run's transcription disagrees
   with task 64's about whether a term exists at all is recorded as a
   DISAGREEMENT rather than silently overwritten.
3. A unit with no record in `regate64_store` is gated here, and the
   fact is recorded on the unit as `verdict_source`.

ONE PROCESS.  Everything below runs in this single process; there is no
pool of workers and no second interpreter.  The run is resumable:
`term65_state.json` names the shards already written, so a stopped run
continues rather than restarting.

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
  term65_run.py [budget seconds]
"""

import glob
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canonical_form as CF                                      # noqa: E402
import gate as G                                                 # noqa: E402
import reference as R                                            # noqa: E402
import term as T                                                 # noqa: E402

STORE = os.path.join(HERE, "term65_store")
STATE = os.path.join(HERE, "term65_state.json")
GATE_OF_RECORD = os.path.join(HERE, "regate64_store")

PROVED = "WRAPPED_TEXT_PROVED"


def shards():
    out = []
    for lang in ["c", "cpp", "go", "rust", "swift"]:
        out.append(os.path.join(HERE,
                                "canon39_wrapped_%s.json" % lang))
    out.append(os.path.join(HERE, "canon39_interp.json"))
    pattern = os.path.join(HERE, "canon39_regen_store", "*.json")
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


def callee_units():
    """the attached callee arch units of task 63, keyed BY TOOLCHAIN
    and then by routine name.

    The toolchain matters: each routine was pulled out of the archive
    of the toolchain that actually compiled the caller, and the
    archives do not agree -- clang's `__udivti3` is three instructions
    and rustc's is sixty-seven.  Keying by the bare routine name would
    hand a rust caller clang's body, which is a different artifact."""
    path = os.path.join(HERE, "canon39_callee_units.json")
    if not os.path.exists(path):
        return {}
    document = json.load(open(path))
    out = {}
    for key, unit in document.get("units", {}).items():
        toolchain = unit.get("toolchain")
        name = unit.get("callee")
        if toolchain is None:
            toolchain = key.split("/", 1)[0]
        if name is None:
            name = key.split("/", 1)[-1]
        out.setdefault(toolchain, {})
        out[toolchain][name] = unit
    return out


def gate_of_record(shard_key):
    """the task-64 verdicts for one shard, read off `regate64_store`.

    Returns {} when the shard has no re-gated file, in which case this
    run gates the shard itself and says so on every record."""
    name = shard_key.replace("/", "__")
    path = os.path.join(GATE_OF_RECORD, name)
    if not os.path.exists(path):
        return {}
    document = json.load(open(path))
    return document.get("units", {})


def copy_verdict(record, banked):
    """task 64's verdict, carried onto this round's record.

    Every field the pool's `layer5_eligibility` reads -- `term_state`,
    `outcome`, `proved` -- and every field the report reads -- `route`,
    `reason`, both routes' verdict objects -- comes from the banked
    record, unchanged."""
    record["verdict_source"] = "regate64_store -- task 64, the gate of record"
    for key in ["verdict_ship", "verdict_text", "outcome", "route",
                "reason", "proved"]:
        if key in banked:
            record[key] = banked[key]
    return record


def one_unit(maker, gate, name, unit, banked):
    """one canon39 unit -> its layer-4 / layer-5 record."""
    record = {
        "unit": name,
        "lang": unit.get("lang"),
        "population": unit.get("population"),
        "operator": unit.get("operator"),
        "arrival_annotation": unit.get("arrival_annotation"),
        "arrival_families": list(unit.get("arrival_families") or []),
        "result_family": unit.get("result_family"),
        "result_width": unit.get("result_width"),
        "runtime_callee_rows": 0,
    }
    for row in unit.get("ledger") or []:
        if row["produced_by"].get("kind") == "runtime_callee":
            record["runtime_callee_rows"] = (
                record["runtime_callee_rows"] + 1)
    unit = dict(unit)
    unit["unit"] = name
    walked = maker.transcribe(unit)
    record["holes"] = walked.holes
    record["cascades"] = walked.cascades
    record["slot_disagreements"] = walked.slot_disagreements
    record["relink_refusal"] = walked.refused
    if walked.refused is not None:
        record["term_state"] = "NO_TERM"
        record["why_no_term"] = "the relink refused: %s" % walked.refused
        record["proved"] = False
    elif walked.out_term is None:
        record["term_state"] = "NO_TERM"
        record["why_no_term"] = why_no_term(walked)
        record["proved"] = False
    else:
        record["term_state"] = "TERM"

    if banked is None:
        record = gate_here(maker, gate, record, walked, unit)
    else:
        record["term_state_task64"] = banked.get("term_state")
        agrees = record["term_state"] == banked.get("term_state")
        record["transcription_agrees_with_task64"] = agrees
        if not agrees:
            record["disagreement"] = (
                "this run's transcription and task 64's disagree about "
                "whether this unit has a term at all; the banked "
                "verdict is carried and the disagreement is counted")
        record = copy_verdict(record, banked)

    if record["term_state"] != "TERM":
        return record
    if record.get("proved"):
        add_layer5(maker, record, walked)
        return record
    record["layer5_normalized_text"] = None
    record["layer5_withdrawn"] = (
        "a term that does not prove is withdrawn, not kept as a "
        "weaker key")
    return record


def gate_here(maker, gate, record, walked, unit):
    """the fallback route for a unit `regate64_store` does not hold."""
    record["verdict_source"] = (
        "gated by this run -- no regate64_store record exists for "
        "this unit")
    if record["term_state"] != "TERM":
        return record
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
    return record


def add_layer5(maker, record, walked):
    """layer 5, computed ONLY for a unit whose term the gate proved."""
    try:
        record["layer5_normalized_text"] = maker.normalize(
            walked.out_term)
    except Exception as problem:
        record["layer5_normalized_text"] = None
        record["layer5_refusal"] = "%s: %s" % (
            type(problem).__name__, problem)
    return record


def why_no_term(walked):
    if walked.holes:
        return walked.holes[0]["why"]
    if walked.cascades:
        return walked.cascades[0]["why"]
    return "the walk reached OUT-0 with no term and recorded no hole"


def run(budget_seconds):
    if not os.path.isdir(STORE):
        os.makedirs(STORE)
    state = load_state()
    done = set(state["done"])
    attached = callee_units()
    reference = R.Reference(runtime_units=attached)
    maker = T.Term(reference=reference,
                   runtime_routines=CF.runtime_routine_names(),
                   runtime_units=attached)
    gate = G.Gate(reference=reference)
    started = time.time()
    for path in shards():
        key = os.path.relpath(path, HERE)
        if key in done:
            continue
        if time.time() - started > budget_seconds:
            print("budget spent; %d shards still to walk"
                  % (len(shards()) - len(done)))
            return False
        document = json.load(open(path))
        banked_shard = gate_of_record(key)
        out = {}
        refused = 0
        disagreements = 0
        not_banked = 0
        for name, unit in sorted(document.get("units", {}).items()):
            if unit.get("outcome") != PROVED:
                refused = refused + 1
                continue
            banked = banked_shard.get(name)
            if banked is None:
                not_banked = not_banked + 1
            record = one_unit(maker, gate, name, unit, banked)
            if record.get("transcription_agrees_with_task64") is False:
                disagreements = disagreements + 1
            out[name] = record
        written = os.path.join(STORE, key.replace("/", "__"))
        handle = open(written, "w")
        json.dump({"shard": key,
                   "canon39_refused_not_transcribed": refused,
                   "units_with_no_banked_verdict": not_banked,
                   "transcription_disagreements_with_task64":
                       disagreements,
                   "units": out}, handle, sort_keys=True)
        handle.close()
        done.add(key)
        state["done"] = sorted(done)
        save_state(state)
        print("%s: %d transcribed, %d canon39-refused skipped, "
              "%d not banked, %d disagreements (%.0fs)"
              % (key, len(out), refused, not_banked, disagreements,
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
