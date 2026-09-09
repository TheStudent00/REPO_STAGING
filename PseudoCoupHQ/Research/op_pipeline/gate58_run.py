#!/usr/bin/env python3
"""gate58_run.py -- THE DRIVER for task 58: every canon38 term
re-gated through `gate.py` and `reference.py`.

POPULATION: every unit task 52 proved -- 9 interpreter, 1,763
original, 28,664 regenerated, 30,436 in all (log 152 section 1.1,
log 153 section 1.1).  Nothing is sampled.

For each unit: the canon38 ledger is transcribed (layer4c, a
superseded record READ and never edited), and the OUT-0 term is put to
BOTH gate routes of `gate.Gate` -- route one against the unit's own
ship body as `reference.Reference` walks it, route two against the
same body walked in text order with the ledger's own meanings.

CHUNKED, SHARDED AND RESUMABLE.  Each source chunk is one output file
in `gate58_store/`; a shard writes only its own state file, so several
shards run at once without touching each other's records.  An
interrupted lap resumes at the first chunk with no output file.

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

import gate as GATE                                               # noqa: E402
import layer4c                                                    # noqa: E402

LANGS = ("c", "cpp", "go", "rust", "swift")
STORE = os.path.join(HERE, "gate58_store")


def sources():
    """every canon38 source document, in a fixed order."""
    out = []
    for lang in LANGS:
        out.append(("original_%s" % lang,
                    os.path.join(HERE,
                                 "canon38_wrapped_%s.json" % lang)))
    out.append(("interp", os.path.join(HERE, "canon38_interp.json")))
    for path in sorted(glob.glob(os.path.join(HERE,
                                              "canon38_regen_store",
                                              "*.json"))):
        out.append(("regen_%s" % os.path.basename(path)[:-5], path))
    return out


def one_unit(gate, name, unit):
    record = {
        "unit": name,
        "lang": unit.get("lang"),
        "population": unit.get("population"),
        "term_built": False,
        "transcription_refused": None,
    }
    try:
        transcription = layer4c.transcribe(unit)
    except Exception as problem:
        record["transcription_refused"] = ("the transcription raised "
                                           "%s: %s"
                                           % (type(problem).__name__,
                                              problem))
        return record
    if transcription.refused is not None:
        record["transcription_refused"] = transcription.refused
        return record
    term = transcription.out_term
    if term is None:
        record["ship"] = gate.prove_term_against_ship(None,
                                                      unit).as_dict()
        record["text"] = gate.prove_term_against_text(None,
                                                      unit).as_dict()
        return record
    record["term_built"] = True
    record["ship"] = gate.prove_term_against_ship(term, unit).as_dict()
    record["text"] = gate.prove_term_against_text(term, unit).as_dict()
    return record


def run_one_source(gate, tag, path):
    document = json.load(open(path))
    units = {}
    for name, unit in document["units"].items():
        if "ledger" not in unit:
            continue
        units[name] = one_unit(gate, name, unit)
    out = {
        "meta": {
            "population": document.get("meta", {}).get("population"),
            "generated_by": "gate58_run.py",
            "source": os.path.basename(path),
            "gate_population": "every unit in this file",
        },
        "units": units,
    }
    target = os.path.join(STORE, "%s.json" % tag)
    json.dump(out, open(target + ".part", "w"), indent=1,
              sort_keys=True)
    os.rename(target + ".part", target)
    return len(units)


def main(argv):
    shard = 0
    shards = 1
    for argument in argv:
        if argument.startswith("--shard="):
            piece = argument.split("=", 1)[1]
            shard = int(piece.split("/")[0])
            shards = int(piece.split("/")[1])
    if not os.path.isdir(STORE):
        os.makedirs(STORE)
    gate = GATE.Gate()
    started = time.time()
    done = 0
    for index, (tag, path) in enumerate(sources()):
        if index % shards != shard:
            continue
        target = os.path.join(STORE, "%s.json" % tag)
        if os.path.exists(target):
            continue
        count = run_one_source(gate, tag, path)
        done = done + 1
        print("%7.1fs  %-42s %5d units  (%d done in this shard)"
              % (time.time() - started, tag, count, done))
        sys.stdout.flush()
    print("shard %d/%d finished" % (shard, shards))


if __name__ == "__main__":
    main(sys.argv[1:])
