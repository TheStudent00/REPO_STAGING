#!/usr/bin/env python3
"""recapture_original.py -- re-run the THREE ORIGINAL plain lanes that carry
altered testimony, on the verbatim path, so their records can actually be
superseded.

WHY THIS EXISTS, AND WHY THE REGENERATION ALONE DID NOT DO IT

The round-8 addendum ruled that the regeneration subsumes Route A: "since
regeneration re-runs everything anyway with the verbatim path, Route A is
subsumed: the regenerated stores ARE the remediation."

Measured, that is not so, and the reason is the legality filter standing in
front of the regeneration.  Every altered record is a REFUSAL, and a
refusal is what the compiler says when the operand shape is not admitted --
which is exactly the shape the extracted rules now call illegal and the
filter never hands to a compiler.  Walked on one record:

    go, plain run, record 387
      the probe:   `a | b` with a `int32` and b `float32`
      stored:      ./main.go:6:9: invalid operation: a / b (mismatched
                   types int32 and float32)          <- the altered text
      the filter:  go's own binaryOpPredicates require both operands
                   identical, so int32 against float32 is ILLEGAL
      so:          the regeneration never compiled it, and there is no
                   regenerated capture to supersede the record with

The measurement over all of them: after the full 129,553-probe
regeneration landed, `supersede_altered.py` joined ZERO altered records to
a regenerated capture.  So Route A is NOT subsumed; it is still needed, and
it is cheap -- log 126 measured the three plain lanes at 48.5 + 24.1 +
159.8 = 232.4 seconds.

WHAT THIS RUNS

The ORIGINAL manifests (`probe_manifest_<lang>.json`, the six hand-written
holder types, 744 + 858 + 1086 = 2,688 candidates) for go, rust and swift
-- unfiltered, exactly as the 2026-08-25 lanes ran them -- through the same
capped container and the same verbatim capture path.

WHAT IT DOES NOT COVER, STATED

The three ASSIGNMENT lanes (`op_asg_go`, `op_asg_rust`, `op_asg_swift`)
also carry altered records.  Their probes come from the assignment bucket,
which `probe_gen.py` excludes, and their generator is a different program
(`asg_stage.py`).  They are out of this task's scope and are reported as
such rather than quietly counted.

THE SPELLING BAN.  Lanes are slices of a manifest in probe-number order;
nothing is keyed, grouped or selected by an operator token.  Outputs are
walked by the guard, and this program deletes its own output on a failure.

usage:
    /tmp/reconnect_venv/bin/python3 recapture_original.py
writes:
    trickle_store/op_units_recapture_<lang>_c<k>.json
    recapture_state.json
"""

import json
import os
import subprocess
import sys

import trickle

HERE = os.path.dirname(os.path.abspath(__file__))
LANGS = ["go", "rust", "swift"]
STATE = os.path.join(HERE, "recapture_state.json")
CHUNK = 400


def plan():
    chunks = []
    for lang in LANGS:
        path = os.path.join(HERE, "probe_manifest_%s.json" % lang)
        doc = json.load(open(path))
        keys = sorted(int(k) for k in doc["probes"])
        k = 0
        idx = 0
        while k < len(keys):
            part = keys[k:k + CHUNK]
            chunks.append({
                "chunk_id": "recap_%s_c%04d" % (lang, idx),
                "language": lang,
                "first_probe": part[0],
                "last_probe": part[-1],
                "probes": len(part),
                "state": "pending",
                "manifest_prefix": "probe_manifest",
                "lane_prefix": "recap",
                "store_prefix": "op_units_recapture",
            })
            k = k + CHUNK
            idx = idx + 1
    state = {}
    state["generated_by"] = "recapture_original.py"
    state["what_this_is"] = (
        "the resume state of the ORIGINAL-lane re-capture. A chunk marked "
        "done is never rerun.")
    state["population"] = (
        "probe_manifest_<lang>.json for go, rust and swift -- the six "
        "hand-written holder types, unfiltered, as the 2026-08-25 lanes "
        "ran them")
    state["chunks"] = chunks
    state["totals"] = {"chunks": len(chunks),
                       "probes": sum(c["probes"] for c in chunks)}
    return state


def save(state):
    tmp = STATE + ".tmp"
    fh = open(tmp, "w")
    json.dump(state, fh, indent=1)
    fh.write("\n")
    fh.close()
    os.replace(tmp, STATE)


def refuse_own_output_on_spelling_failure(paths):
    cmd = [sys.executable, os.path.join(HERE, "check_no_spelling_keys.py")]
    cmd.extend(paths)
    done = subprocess.run(cmd, capture_output=True, text=True)
    print(done.stdout.strip())
    if done.returncode != 0:
        print(done.stderr.strip())
        for path in paths:
            if os.path.exists(path):
                os.remove(path)
        raise SystemExit("REFUSED OWN OUTPUT: spelling guard failed")


def main():
    if os.path.exists(STATE):
        state = json.load(open(STATE))
        print("resuming from %s" % STATE)
    else:
        state = plan()
        save(state)
        print("planned %d chunks over %d probes"
              % (state["totals"]["chunks"], state["totals"]["probes"]))
    if not trickle.container_is_up():
        raise SystemExit("recapture: %s is not running. Start it:  "
                         "bash trickle_up.sh" % trickle.CONTAINER)
    for chunk in state["chunks"]:
        if chunk["state"] == "done":
            continue
        record = trickle.run_chunk(chunk)
        if not record.get("ok"):
            chunk["state"] = "failed"
            chunk["detail"] = record.get("reason")
            print("  %-20s FAILED: %s"
                  % (chunk["chunk_id"], record.get("reason")))
            save(state)
            continue
        rc, out, _err = trickle.guard([record["store"]])
        if rc != 0:
            os.remove(record["store"])
            chunk["state"] = "refused_by_the_spelling_guard"
            chunk["detail"] = out
            save(state)
            continue
        chunk["state"] = "done"
        chunk["tally"] = record["tally"]
        chunk["seconds"] = record["seconds"]
        chunk["store"] = record["store"]
        t = record["tally"]
        print("  %-20s %5d submitted  %5d accepted  %5d refused  %6.1fs"
              % (chunk["chunk_id"], t["submitted"], t["accepted"],
                 t["refused"], record["seconds"]))
        save(state)
    save(state)
    refuse_own_output_on_spelling_failure([STATE])


if __name__ == "__main__":
    main()
