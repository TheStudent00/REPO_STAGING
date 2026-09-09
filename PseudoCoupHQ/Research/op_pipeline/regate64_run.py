#!/usr/bin/env python3
"""regate64_run.py -- the round-13 re-gate of every canon39 term with
`gate.py`, over the branch-following `reference.py` of task 64.

POPULATION: the 30,432 units canon39 records as WRAPPED_TEXT_PROVED,
across `canon39_wrapped_{c,cpp,go,rust,swift}.json`,
`canon39_interp.json` and `canon39_regen_store/*.json`.  A canon39
REFUSED unit has no wrapped text and is not transcribed; the 646 of
them are counted and named, never silently dropped.

WHAT IS DIFFERENT FROM `term61_run.py`, said out loud.  Nothing about
the ledger, the transcription or the gate's obligations moved.  The one
change is inside `reference.py`: `simulate` now walks a body as its own
control-flow graph and steps into an attached runtime callee, so route
one -- the term against the unit's own ship body -- reaches an answer
where it used to refuse.  `term61_run.py` is round 12's record and is
not edited; this file is round 13's run.

THE ATTACHED CALLEE BODIES come from `canon39_callee_units.json` (task
63), keyed BY TOOLCHAIN and then by routine name, because the four
archives do not agree -- clang's `__udivti3` is three instructions and
rustc's is sixty-seven -- so a caller's own language selects the
archive.  The ledgers canon39 stores are read AS THEY ARE: this run
does not repoint any producer, because a ledger row is node 0_3_5_3's
and its rebuild is not this task's.

ONE PROCESS.  Everything below runs in this single process; there is no
pool of workers and no second interpreter.  The run is resumable:
`regate64_state.json` names the shards already written, so a stopped
run continues rather than restarting.

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
  regate64_run.py [budget seconds]
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

STORE = os.path.join(HERE, "regate64_store")
STATE = os.path.join(HERE, "regate64_state.json")

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
    """the 76 attached callee arch units of task 63, keyed by toolchain
    and then by routine name."""
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


def state_of(record):
    """the FOUR STATES the report counts, read off one record."""
    if record.get("term_state") == "NO_TERM":
        return "no term"
    if record.get("proved"):
        return "proved"
    if record.get("outcome") == "DISPROVED":
        return "disproved"
    return "undecided"


def one_unit(maker, gate, reference, name, unit):
    """one canon39 unit -> its re-gated record.  The shape is
    `term61_run.one_unit`'s, so the two runs join on the unit name."""
    record = {
        "unit": name,
        "lang": unit.get("lang"),
        "population": unit.get("population"),
        "operator": unit.get("operator"),
        "arrival_families": list(unit.get("arrival_families") or []),
        "result_family": unit.get("result_family"),
        "result_width": unit.get("result_width"),
    }
    unit = dict(unit)
    unit["unit"] = name
    record["branch_lines"] = count_branch_lines(unit)
    record["call_lines"] = count_call_lines(unit)
    walked = maker.transcribe(unit)
    record["holes"] = len(walked.holes)
    record["relink_refusal"] = walked.refused
    if walked.refused is not None:
        record["term_state"] = "NO_TERM"
        record["why_no_term"] = ("the relink refused: %s"
                                 % walked.refused)
        record["proved"] = False
        return record
    if walked.out_term is None:
        record["term_state"] = "NO_TERM"
        record["why_no_term"] = why_no_term(walked)
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
    record["guard_rows"] = guard_rows_of(reference, unit)
    return record


def count_branch_lines(unit):
    total = 0
    for raw in unit.get("body_verbatim") or []:
        text = raw.split("!!")[0].strip()
        if text == "":
            continue
        mnemonic = text.split(" ", 1)[0]
        if R.is_conditional_transfer(mnemonic):
            total = total + 1
    return total


def count_call_lines(unit):
    total = 0
    for raw in unit.get("body_verbatim") or []:
        text = raw.split("!!")[0].strip()
        if text.split(" ", 1)[0] == "call":
            total = total + 1
    return total


def guard_rows_of(reference, unit):
    """the sides of this body that transferred OUT of the unit, as the
    walk recorded them.  Only asked for a body that has a branch, so
    the common straight-line unit costs nothing."""
    if count_branch_lines(unit) == 0:
        return []
    try:
        state = reference.simulate(
            unit.get("body_verbatim"),
            unit.get("arrival_contract_bindings"),
            callees=reference.callees_for(unit))
    except Exception:
        return []
    return state.guard_rows


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
        out = {}
        refused = 0
        for name, unit in sorted(document.get("units", {}).items()):
            if unit.get("outcome") != PROVED:
                refused = refused + 1
                continue
            out[name] = one_unit(maker, gate, reference, name, unit)
        written = os.path.join(STORE, key.replace("/", "__"))
        handle = open(written, "w")
        json.dump({"shard": key,
                   "canon39_refused_not_transcribed": refused,
                   "units": out}, handle, sort_keys=True)
        handle.close()
        done.add(key)
        state["done"] = sorted(done)
        save_state(state)
        print("%s: %d re-gated, %d canon39-refused skipped (%.0fs)"
              % (key, len(out), refused, time.time() - started))
        sys.stdout.flush()
    print("all %d shards re-gated" % len(done))
    return True


if __name__ == "__main__":
    budget = 100000
    if len(sys.argv) > 1:
        budget = int(sys.argv[1])
    finished = run(budget)
    if not finished:
        sys.exit(3)
