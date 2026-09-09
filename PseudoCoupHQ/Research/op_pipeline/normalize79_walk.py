#!/usr/bin/env python3
"""normalize79_walk.py -- ONE WALK of the corrected layer-5 rule over
every unit whose term the round-13 gate PROVED, written to a file so
that walks made in SEPARATE PROCESSES can be compared.

WHY A SEPARATE PROCESS PER WALK.  The defect this repair answers is
that the printed text was a function of the unit AND of what the
process built earlier (log_169 section 5.3).  Two walks inside one
process share the solver's node-identity counter, so they cannot
measure the defect.  Each walk therefore runs as its own process, and
`acceptance79.py` compares the files.

THE THREE WALKS the acceptance test uses:

    --label walk1 --order forward     units in name order
    --label walk2 --order forward     the same, a second fresh process
    --label walk3 --order shuffled    the shards AND the units inside
                                      them in a deliberately shuffled
                                      construction order (seed 79)

MEMORY BOUND, stated before the run: this walk holds one shard's JSON
at a time plus one short text per unit, so the expected peak resident
size is under 1.5 GB.  The HARD CAP is 6 GB: the walk checks its own
peak resident size every 200 units and stops with the named abort
ABORT_MEMORY_CEILING rather than swapping the machine.

WRITES:  normalize79_walk_<label>.json

Coding discipline: no compound one-liner statements.

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

No operator token appears in this file, and no unit's display label is
read.
"""

import glob
import json
import os
import random
import resource
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canonical_form as CF                                      # noqa: E402
import reference as R                                            # noqa: E402
import term as T                                                 # noqa: E402

PROVED = "WRAPPED_TEXT_PROVED"
MEMORY_CEILING_MB = 6144
CHECK_EVERY = 200


def peak_resident_mb():
    used = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return used / 1024.0


def shards():
    out = []
    for lang in ["c", "cpp", "go", "rust", "swift"]:
        out.append(os.path.join(HERE, "canon39_wrapped_%s.json" % lang))
    out.append(os.path.join(HERE, "canon39_interp.json"))
    pattern = os.path.join(HERE, "canon39_regen_store", "*.json")
    out.extend(sorted(glob.glob(pattern)))
    return [path for path in out if os.path.exists(path)]


def callee_units():
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


def proved_units():
    """the units the round-13 gate of record PROVED, read off
    `term65_store` -- the same population log_169 measured."""
    out = set()
    pattern = os.path.join(HERE, "term65_store", "*.json")
    for path in sorted(glob.glob(pattern)):
        document = json.load(open(path))
        for name in document["units"]:
            if document["units"][name].get("proved"):
                out.add(name)
    return out


def main():
    label = "walk1"
    order = "forward"
    limit = 0
    if "--label" in sys.argv:
        label = sys.argv[sys.argv.index("--label") + 1]
    if "--order" in sys.argv:
        order = sys.argv[sys.argv.index("--order") + 1]
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])
    out_dir = HERE
    if "--out-dir" in sys.argv:
        out_dir = sys.argv[sys.argv.index("--out-dir") + 1]

    started = time.time()
    proved = proved_units()
    sys.stdout.write("-- walk %s, order %s\n" % (label, order))
    sys.stdout.write("   units with a proved term %d\n" % len(proved))
    sys.stdout.flush()

    attached = callee_units()
    reference = R.Reference(runtime_units=attached)
    maker = T.Term(reference=reference,
                   runtime_routines=CF.runtime_routine_names(),
                   runtime_units=attached)

    paths = shards()
    if order == "shuffled":
        shuffler = random.Random(79)
        shuffler.shuffle(paths)

    texts = {}
    refusals = {}
    walked = 0
    for path in paths:
        document = json.load(open(path))
        names = sorted(document.get("units", {}))
        if order == "shuffled":
            shuffler = random.Random(79 + len(names))
            shuffler.shuffle(names)
        for name in names:
            if name not in proved:
                continue
            unit = document["units"][name]
            if unit.get("outcome") != PROVED:
                continue
            unit = dict(unit)
            unit["unit"] = name
            transcription = maker.transcribe(unit)
            if transcription.out_term is None:
                refusals[name] = "the walk built no OUT-0 term"
                continue
            try:
                texts[name] = maker.normalize(transcription.out_term)
            except Exception as problem:
                refusals[name] = "%s: %s" % (type(problem).__name__,
                                             problem)
            walked = walked + 1
            if limit and walked >= limit:
                break
            if walked % CHECK_EVERY == 0:
                if peak_resident_mb() > MEMORY_CEILING_MB:
                    sys.stdout.write(
                        "ABORT_MEMORY_CEILING: peak resident size "
                        "%.0f MB over the stated %d MB cap after %d "
                        "units\n" % (peak_resident_mb(),
                                     MEMORY_CEILING_MB, walked))
                    sys.stdout.flush()
                    return 3
        document = None
        if limit and walked >= limit:
            break

    spent = time.time() - started
    peak = peak_resident_mb()
    sys.stdout.write("   units printed %d, refused %d\n"
                     % (len(texts), len(refusals)))
    sys.stdout.write("   distinct texts %d\n" % len(set(texts.values())))
    sys.stdout.write("   seconds %.1f, peak resident size %.0f MB\n"
                     % (spent, peak))
    sys.stdout.flush()

    document = {
        "meta": {
            "generated_by": "normalize79_walk.py",
            "node": "hq.research.compiler_graph.term.normalize",
            "label": label,
            "order": order,
            "modules_read_from": HERE,
            "what_it_is": "one walk of the corrected layer-5 rule over "
                          "every unit whose term the round-13 gate "
                          "proved, in its own process",
            "memory_bound_mb": MEMORY_CEILING_MB,
            "sample_limit": limit,
            "peak_resident_mb": round(peak, 1),
            "seconds": round(spent, 1),
        },
        "units_printed": len(texts),
        "units_refused": len(refusals),
        "distinct_texts": len(set(texts.values())),
        "texts": texts,
        "refusals": refusals,
    }
    out_path = os.path.join(out_dir,
                            "normalize79_walk_%s.json" % label)
    handle = open(out_path, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    sys.stdout.write("-- wrote %s\n" % os.path.basename(out_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
