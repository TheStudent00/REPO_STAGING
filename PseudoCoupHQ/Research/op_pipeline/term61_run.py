#!/usr/bin/env python3
"""term61_run.py -- the driver that runs `term.py` (node 0_3_5_6) over
the canon39 proved population, gates both term routes with `gate.py`,
and writes the layer-4 / layer-5 record the pool reads.

POPULATION: the 30,432 units canon39 records as WRAPPED_TEXT_PROVED,
across `canon39_wrapped_{c,cpp,go,rust,swift}.json`,
`canon39_interp.json` and `canon39_regen_store/*.json`.  A canon39
REFUSED unit has no wrapped text and is not transcribed; the 646 of
them are counted and named, never silently dropped.

ONE PROCESS.  Everything below runs in this single process; there is
no pool of workers and no second interpreter.  The run is resumable:
`term61_state.json` names the shards already written, so a stopped run
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

No operator token appears in this file.

Coding discipline: no compound one-liner statements.
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

STORE = os.path.join(HERE, "term61_store")
STATE = os.path.join(HERE, "term61_state.json")

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


def runtime_units():
    """the attached runtime callee bodies, keyed BY TOOLCHAIN and then
    by routine name.

    The toolchain matters: `runtime_callee.py` pulled each routine out
    of the archive of the toolchain that actually compiled the caller,
    and the four archives do not agree -- clang's `__udivti3` is three
    instructions and rustc's is sixty-seven.  Keying by the bare
    routine name would hand a rust caller clang's body, which is a
    different artifact.  `term.Term` picks the toolchain from the
    caller's own language."""
    path = os.path.join(HERE, "runtime_callee_units.json")
    if not os.path.exists(path):
        return {}
    document = json.load(open(path))
    out = {}
    for key, unit in document.get("units", {}).items():
        toolchain = unit.get("toolchain")
        if toolchain is None:
            if "/" in key:
                toolchain = key.split("/", 1)[0]
            else:
                toolchain = "unknown"
        name = unit.get("callee")
        if name is None:
            name = key.split("/", 1)[-1]
        out.setdefault(toolchain, {})
        out[toolchain][name] = unit
    return out


def one_unit(maker, gate, name, unit):
    """one canon39 unit -> its layer-4 / layer-5 record."""
    record = {
        "unit": name,
        "lang": unit.get("lang"),
        "population": unit.get("population"),
        "operator": unit.get("operator"),
        "arrival_annotation": unit.get("arrival_annotation"),
        "arrival_families": list(unit.get("arrival_families") or []),
        "result_width": unit.get("result_width"),
        "runtime_callee_rows": 0,
    }
    for row in unit.get("ledger") or []:
        if row["produced_by"].get("kind") == "runtime_callee":
            record["runtime_callee_rows"] += 1
    walked = maker.transcribe(unit)
    record["holes"] = walked.holes
    record["cascades"] = walked.cascades
    record["slot_disagreements"] = walked.slot_disagreements
    record["relink_refusal"] = walked.refused
    if walked.refused is not None:
        record["term_state"] = "NO_TERM"
        record["why_no_term"] = "the relink refused: %s" % walked.refused
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
    if verdict.proved():
        try:
            record["layer5_normalized_text"] = maker.normalize(
                walked.out_term)
        except Exception as problem:
            record["layer5_normalized_text"] = None
            record["layer5_refusal"] = "%s: %s" % (
                type(problem).__name__, problem)
    else:
        record["layer5_normalized_text"] = None
        record["layer5_withdrawn"] = (
            "a term that does not prove is withdrawn, not kept as a "
            "weaker key")
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
    reference = R.Reference()
    maker = T.Term(reference=reference,
                   runtime_routines=CF.runtime_routine_names(),
                   runtime_units=runtime_units())
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
                refused += 1
                continue
            out[name] = one_unit(maker, gate, name, unit)
        written = os.path.join(STORE, key.replace("/", "__"))
        handle = open(written, "w")
        json.dump({"shard": key,
                   "canon39_refused_not_transcribed": refused,
                   "units": out}, handle, sort_keys=True)
        handle.close()
        done.add(key)
        state["done"] = sorted(done)
        save_state(state)
        print("%s: %d transcribed, %d canon39-refused skipped"
              % (key, len(out), refused))
        sys.stdout.flush()
    print("all %d shards walked" % len(done))
    return True


if __name__ == "__main__":
    budget = 3600
    if len(sys.argv) > 1:
        budget = int(sys.argv[1])
    finished = run(budget)
    if not finished:
        sys.exit(3)
