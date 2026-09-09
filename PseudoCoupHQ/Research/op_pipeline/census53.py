#!/usr/bin/env python3
"""census53.py -- THE DRIVER for task 53: layer 4 read off canon38.

POPULATION: every unit task 52 proved -- 9 interpreter, 1,763
original, 28,664 regenerated, 30,436 in all (log 152 section 1.1).
Nothing is sampled.

For every one of them:

  * LAYER 4 -- the canon38 ledger transcribed into a z3 term from
    OUT-0 downward (layer4c.py, which replays ledger48's own dataflow
    walk and checks the replay against the stored ledger).
  * THE CENSUS -- the rows whose producer has no term, filtered out of
    those transcriptions and tallied into name_census4.json by
    name_census4.py.
  * THE GATE, BOTH ROUTES, UNMODIFIED -- route one is gate48.py (the
    term against the behaviour checker's simulation of the unit's own
    ship body); route two is textwalk48.py (the same body walked in
    text order with layer 4's own meanings table).  Neither file is
    edited by this task.
  * LAYER 5 -- the fixed-rule re-render (layer5.py), and whether it is
    character-identical to layer 3's wrapped text.

CHUNKED AND RESUMABLE.  The regenerated population is 29,288 units in
326 stored chunks; this driver does one chunk at a time and records
each finished chunk in `layer4c_state.json`, so an interrupted lap
resumes where it stopped.

WHAT IS RECORDED PER UNIT BEYOND TASK 48's RECORD.  `body_spells_a_
call` and `callees` are written for every unit, because log 152
section 5.1 found 305 units whose answer is produced by a library
routine and no opcode in the body writes it; the census reports that
as its own cause, with the callee names, and nothing about `call` is
added to any destination table.

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
"""

import glob
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import gate48                                                     # noqa: E402
import textwalk48                                                 # noqa: E402
import layer4c as layer4                                                     # noqa: E402
import layer5                                                     # noqa: E402

LANGS = ("c", "cpp", "go", "rust", "swift")
REGEN_STRIDE = 1
STATE_PATH = os.path.join(HERE, "layer4c_state.json")
REGEN_STORE = os.path.join(HERE, "layer4c_regen_store")


def load_state():
    if os.path.exists(STATE_PATH):
        return json.load(open(STATE_PATH))
    return {"done": [], "started": time.strftime("%Y-%m-%d %H:%M:%S")}


def save_state(state):
    json.dump(state, open(STATE_PATH, "w"), indent=1, sort_keys=True)


def one_unit(name, unit, gate_it):
    """the layer-4 record for one unit."""
    record = {
        "unit": name,
        "lang": unit.get("lang"),
        "population": unit.get("population"),
        "layer3_wrapped_text": unit.get("wrapped_text"),
        "holes": [],
        "cascades": [],
        "term_built": False,
        "layer5_normalized_text": None,
        "layer5_equals_layer3": None,
        "gate_ship_verdict": "NOT_GATED",
        "gate_ship_detail": "this unit is outside the gate's sample",
        "gate_textorder_verdict": "NOT_GATED",
        "gate_textorder_detail": "this unit is outside the gate's "
                                 "sample",
    }
    record["body_spells_a_call"] = False
    record["callees"] = []
    for raw in unit.get("body_verbatim") or []:
        mnemonic = (raw.split() or [""])[0]
        if mnemonic in ("call", "callq"):
            record["body_spells_a_call"] = True
            pieces = raw.split()
            if len(pieces) > 1:
                if pieces[1] not in record["callees"]:
                    record["callees"].append(pieces[1])
    transcription = layer4.transcribe(unit)
    if transcription.refused is not None:
        record["refused"] = transcription.refused
        return record
    record["holes"] = transcription.holes
    record["cascades"] = transcription.cascades
    if transcription.out_term is None:
        return record
    record["term_built"] = True
    try:
        text = layer5.normalize(transcription.out_term)
    except Exception as problem:
        record["layer5_note"] = ("the fixed rule raised %s: %s"
                                 % (type(problem).__name__, problem))
        text = None
    record["layer5_normalized_text"] = text
    if text is not None:
        record["layer5_equals_layer3"] = \
            (text == record["layer3_wrapped_text"])
    if gate_it:
        verdict, detail = gate48.gate(unit, transcription)
        record["gate_ship_verdict"] = verdict
        record["gate_ship_detail"] = detail
        verdict, detail = textwalk48.gate(unit, transcription)
        record["gate_textorder_verdict"] = verdict
        record["gate_textorder_detail"] = detail
    return record


def run_document(document, gate_every, offset=0):
    out = {}
    index = offset
    for name, unit in document["units"].items():
        if "ledger" not in unit:
            index += 1
            continue
        gate_it = (gate_every == 1) or (index % gate_every == 0)
        out[name] = one_unit(name, unit, gate_it)
        index += 1
    return out, index


def run_original(state):
    for lang in LANGS:
        tag = "original:%s" % lang
        if tag in state["done"]:
            continue
        path = os.path.join(HERE, "canon38_wrapped_%s.json" % lang)
        document = json.load(open(path))
        units, _ = run_document(document, 1)
        out = {
            "meta": {
                "population": "the original corpus, %s" % lang,
                "generated_by": "census53.py",
                "gate_population": "every unit in this file",
            },
            "units": units,
        }
        json.dump(out, open(os.path.join(
            HERE, "layer4c_terms_%s.json" % lang), "w"),
            indent=1, sort_keys=True)
        state["done"].append(tag)
        save_state(state)
        print("original %-6s %d units" % (lang, len(units)))
        sys.stdout.flush()


def run_interp(state):
    if "interp" in state["done"]:
        return
    path = os.path.join(HERE, "canon38_interp.json")
    document = json.load(open(path))
    units, _ = run_document(document, 1)
    out = {
        "meta": {
            "population": "the interpreter/JIT corpus",
            "generated_by": "census53.py",
            "gate_population": "every unit in this file",
        },
        "units": units,
    }
    json.dump(out, open(os.path.join(HERE, "layer4c_interp.json"), "w"),
              indent=1, sort_keys=True)
    state["done"].append("interp")
    save_state(state)
    print("interpreter %d units" % len(units))
    sys.stdout.flush()


def run_regen(state, budget_seconds):
    if not os.path.isdir(REGEN_STORE):
        os.makedirs(REGEN_STORE)
    chunks = sorted(glob.glob(os.path.join(HERE,
                                           "canon38_regen_store",
                                           "*.json")))
    started = time.time()
    offset = 0
    for chunk in chunks:
        tag = "regen:%s" % os.path.basename(chunk)
        if tag in state["done"]:
            offset += state.get("counts", {}).get(tag, 0)
            continue
        document = json.load(open(chunk))
        units, offset = run_document(document, REGEN_STRIDE, offset)
        out = {
            "meta": {
                "population": "the regenerated corpus",
                "generated_by": "census53.py",
                "gate_population": "every unit in this file",
            },
            "units": units,
        }
        json.dump(out, open(os.path.join(
            REGEN_STORE, os.path.basename(chunk)), "w"),
            indent=1, sort_keys=True)
        state["done"].append(tag)
        state.setdefault("counts", {})[tag] = len(units)
        save_state(state)
        print("regen %s %d units (%d chunks done)"
              % (os.path.basename(chunk), len(units),
                 len([one for one in state["done"]
                      if one.startswith("regen:")])))
        sys.stdout.flush()
        if time.time() - started > budget_seconds:
            print("budget reached; resume by running this file again")
            return False
    return True


def main():
    budget = 100000
    for argument in sys.argv[1:]:
        if argument.startswith("--budget="):
            budget = int(argument.split("=", 1)[1])
    state = load_state()
    run_original(state)
    run_interp(state)
    finished = run_regen(state, budget)
    print("finished" if finished else "partial")


if __name__ == "__main__":
    main()
