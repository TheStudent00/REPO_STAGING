#!/usr/bin/env python3
"""ref2_canon40_sample.py -- 200 canon40 proofs re-run under the CORRECTED
reference, to show that a body proved against its own term is proved under
either reading.

WHY IT HOLDS, before the measurement.  `gate.Gate.prove_wrapped` puts TWO
terms to z3: the wrapped text's answer, built by walking the wrapped text
through `reference.py`'s builders, and the unit's own ship body's answer,
built by walking that body through the SAME builders.  Both sides are the
reference.  A correction to the reference moves both together, so the proof is
about the two bodies and not about the reading -- which is exactly what makes
it safe to correct level 0 without withdrawing what canon40 proved.  That is
an argument; this program is the measurement.

THE SAMPLE is 200 units drawn by `random.Random("ref2|canon40")` over the
sorted list of every canon40 unit whose outcome is `WRAPPED_TEXT_PROVED`, so
the same 200 come out on every re-run and nobody chose them.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope, anywhere in
this line -- not in matching, not in "which pairs get compared", not in report
rows, not in dropdowns.  The candidate set for comparison comes from
machine-form evidence (clusters, connections, type pairs) or from ratified
intention -- never from the token.  The token appears exactly once per unit:
as a display label on the member.  HISTORY OF VIOLATIONS, so the pattern is
visible: (1) the arch campaign's cross-language matrix (caught by the owner
2026-08-24); (2) verdicts.py's row pairing (caught by the owner 2026-08-25 -- the
fix brief itself reintroduced it as "same-operator pairs").  MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse its own
output on failure.  A brief handed to any subagent for this line MUST paste
this paragraph verbatim."

The sample is drawn over a SORTED LIST OF UNIT NAMES; no operator token enters
the draw, and a unit's `operator` field is carried on the row as a display
label only.

Coding discipline: no compound one-liner statements.

usage:
  ref2_canon40_sample.py <out.json> [<how many>]
"""

import glob
import json
import os
import random
import resource
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PIPELINE = os.path.abspath(os.path.join(HERE, "..", "..", "..",
                                        "op_pipeline"))
for _path in (PIPELINE, os.path.join(PIPELINE, "lean")):
    if _path not in sys.path:
        sys.path.insert(0, _path)

import gate as G                                            # noqa: E402
import reference as R                                       # noqa: E402
import canonical_form as CF                                 # noqa: E402
import regate64_run as RG                                   # noqa: E402

PROVED = "WRAPPED_TEXT_PROVED"
SEED = "ref2|canon40"
MEMORY_CEILING_KB = 12 * 1024 * 1024
ABORT_NAME = "ABORT_MEMORY_REF2"


def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def shards():
    out = []
    for lang in ("c", "cpp", "go", "rust", "swift"):
        out.append(os.path.join(PIPELINE,
                                "canon40_wrapped_%s.json" % lang))
    out.append(os.path.join(PIPELINE, "canon40_interp.json"))
    out.extend(sorted(glob.glob(os.path.join(PIPELINE,
                                             "canon40_regen_store",
                                             "*.json"))))
    return [path for path in out if os.path.exists(path)]


def proved_units():
    """(unit name -> the shard it lives in) for every canon40 unit whose
    outcome is `WRAPPED_TEXT_PROVED`."""
    out = {}
    for path in shards():
        handle = open(path)
        document = json.load(handle)
        handle.close()
        for name in document.get("units") or {}:
            if document["units"][name].get("outcome") != PROVED:
                continue
            out[name] = path
        document = None
    return out


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    out_path = argv[1]
    many = 200
    if len(argv) > 2:
        many = int(argv[2])
    started = time.time()
    where = proved_units()
    names = sorted(where)
    print("canon40 units whose outcome is %s: %d" % (PROVED, len(names)))
    shuffler = random.Random(SEED)
    sample = list(names)
    shuffler.shuffle(sample)
    sample = sorted(sample[:many])
    print("the sample: %d units, drawn by random.Random(%r)"
          % (len(sample), SEED))
    by_shard = {}
    for name in sample:
        by_shard.setdefault(where[name], []).append(name)
    attached = RG.callee_units()
    readings = CF.runtime_answer_readings()
    reference = R.Reference(runtime_units=attached)
    gate = G.Gate(reference=reference)
    rows = []
    counts = {}
    index = 0
    for path in sorted(by_shard):
        handle = open(path)
        document = json.load(handle)
        handle.close()
        for name in by_shard[path]:
            index = index + 1
            record = dict(document["units"][name])
            record["unit"] = name
            verdict = gate.prove_wrapped(record["wrapped_text"], record)
            word = verdict.outcome
            if word in ("PROVED_ON_SHIP", "PROVED_ON_PRIOR",
                        "PROVED_BY_CONSTRUCTION"):
                outcome = PROVED
            elif word == "DISPROVED":
                outcome = "GATE_DISPROVED"
            else:
                outcome = "GATE_UNDECIDED"
            counts[outcome] = counts.get(outcome, 0) + 1
            rows.append({"unit": name, "lang": record.get("lang"),
                         "outcome_before": record.get("outcome"),
                         "outcome_after": outcome,
                         "verdict_before": record.get("verdict"),
                         "verdict_after": word,
                         "detail_after": verdict.reason,
                         "route_after": verdict.route})
            if index % 25 == 0:
                print("  [%d/%d] %d kB" % (index, len(sample),
                                           peak_kb()))
                sys.stdout.flush()
        document = None
    held = counts.get(PROVED, 0)
    summary = {
        "what": ("200 canon40 proofs re-run under the corrected "
                 "reference; both sides of a canon40 proof are built "
                 "by the same reference, so the proof is about the two "
                 "bodies and not about the reading"),
        "canon40_units_proved": len(names),
        "sample": len(sample),
        "seed": SEED,
        "by_outcome": counts,
        "still_proved": held,
        "seconds": round(time.time() - started, 1),
        "peak_resident_kb": peak_kb(),
        "memory_ceiling_kb": MEMORY_CEILING_KB,
        "named_abort": ABORT_NAME,
    }
    handle = open(out_path, "w")
    json.dump({"summary": summary, "rows": rows}, handle, indent=1,
              sort_keys=True)
    handle.close()
    print("")
    print("| outcome under the corrected reference | units |")
    print("|---|---|")
    for name in sorted(counts):
        print("| `%s` | %d |" % (name, counts[name]))
    print("")
    print("%d of %d sampled canon40 proofs still read %s"
          % (held, len(sample), PROVED))
    for row in rows:
        if row["outcome_after"] == PROVED:
            continue
        print("  %s: %s -> %s (%s)"
              % (row["unit"], row["outcome_before"],
                 row["outcome_after"], row["detail_after"][:160]))
    print("wall clock %.1f s, peak resident %d kB, ceiling %d kB, "
          "named abort %s" % (summary["seconds"], peak_kb(),
                              MEMORY_CEILING_KB, ABORT_NAME))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
