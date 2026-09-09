#!/usr/bin/env python3
"""t104_the44.py -- the 44 units whose LAYER 5 did not converge, asked
again under the normalizer as this task leaves it.

WHAT THE 44 ARE (log_202 section 4.3, task 97): 44 of the 30,324 units
canon40 proves have a layer-4 term that is built and PROVED, and a
NORMALIZER that does not finish -- measured at 1,536 / 4,096 / 18,432
MB, the peak pins against every ceiling and the outcome is the same at
every rung, so a bigger machine buys nothing.  They are the reason
`term66_store/` holds 30,280 records and not 30,324, and the reason
`pool66_run.py` refuses to write a pool of record.

WHAT THIS PROGRAM ASKS.  The brief's audit item (c): does the operand
order change their convergence?  Each of the 44 is run again, one
FORKED SUB-PROCESS PER UNIT with `RLIMIT_AS` at the stated ceiling, by
`term97_walk.one_unit_forked` -- imported, not re-typed, so the answer
is comparable to task 97's by construction.  The count that answers the
brief is `units_that_converged`.

MEMORY: the parent does no z3 work; it forks and collects.  Each
sub-process is capped by RLIMIT_AS at the ceiling below.  The parent's
own hard cap is 6 GB with the named abort ABORT_MEMORY_T104.

WRITES: t104_the44.json

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

usage:
  t104_the44.py <ceiling_mb> <seconds_per_unit>
"""

import glob
import json
import os
import resource
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PIPELINE = os.path.dirname(HERE)
sys.path.insert(0, PIPELINE)

import term97_walk as TW                                         # noqa: E402

OUT = os.path.join(PIPELINE, "t104_the44.json")
AUDIT = os.path.join(PIPELINE, "t104_audit.json")
PROVED = "WRAPPED_TEXT_PROVED"
PARENT_CAP_KB = 6 * 1024 * 1024


def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def check_memory():
    used = peak_kb()
    if used > PARENT_CAP_KB:
        raise SystemExit(
            "ABORT_MEMORY_T104: the parent's peak resident %d kB "
            "passed the stated cap of %d kB" % (used, PARENT_CAP_KB))
    return used


def canon40_shards():
    out = []
    for lang in ["c", "cpp", "go", "rust", "swift"]:
        out.append(os.path.join(PIPELINE,
                                "canon40_wrapped_%s.json" % lang))
    out.append(os.path.join(PIPELINE, "canon40_interp.json"))
    pattern = os.path.join(PIPELINE, "canon40_regen_store", "*.json")
    out.extend(sorted(glob.glob(pattern)))
    return [path for path in out if os.path.exists(path)]


def wanted_units():
    """the units canon40 proves that `term66_store/` has no record for
    -- read off `t104_audit.json`, which lane 3 computed by walking
    both, so this program does not compute the population a second
    way."""
    document = json.load(open(AUDIT))
    return list(
        document["canon40_proved_units_with_no_term66_record"])


def main():
    ceiling = 6144
    seconds = 600
    if len(sys.argv) > 1:
        ceiling = int(sys.argv[1])
    if len(sys.argv) > 2:
        seconds = int(sys.argv[2])
    names = wanted_units()
    total = len(names)
    sys.stdout.write("-- %d units, ceiling %d MB, %d s each\n"
                     % (total, ceiling, seconds))
    sys.stdout.flush()
    left = set(names)
    found = {}
    for path in canon40_shards():
        document = json.load(open(path))
        units = document.get("units") or {}
        for name in list(left):
            if name not in units:
                continue
            record = dict(units[name])
            record["unit"] = name
            found[name] = record
            left.discard(name)
        document = None
        if not left:
            break
    maker, gate, _attached, _readings = TW.build()
    rows = []
    words = {}
    converged = 0
    index = 0
    started = time.time()
    for name in names:
        index = index + 1
        sys.stdout.write("[%d/%d] %s\n" % (index, total, name))
        sys.stdout.flush()
        if name not in found:
            rows.append({"unit": name,
                         "word": "NOT_IN_CANON40",
                         "layer5_text": None})
            words["NOT_IN_CANON40"] = words.get("NOT_IN_CANON40", 0) + 1
            continue
        word, record, wall, child_peak, token = TW.one_unit_forked(
            maker, gate, name, found[name], ceiling, seconds)
        text = None
        if record is not None:
            text = record.get("layer5_normalized_text")
        row = {
            "unit": name,
            "word": word,
            "memory_token": token,
            "wall_seconds": round(wall, 2),
            "sub_process_peak_kb": child_peak,
            "ceiling_mb": ceiling,
            "layer5_text": text,
            "term_state": None,
            "proved": None,
        }
        if record is not None:
            row["term_state"] = record.get("term_state")
            row["proved"] = record.get("proved")
        rows.append(row)
        words[word] = words.get(word, 0) + 1
        if word == "walked":
            if text is not None:
                converged = converged + 1
        sys.stdout.write("   %s  peak %d kB  wall %.1f s  layer-5 %s\n"
                         % (word, child_peak, wall,
                            "printed" if text else "none"))
        sys.stdout.flush()
        check_memory()
    summary = {
        "units": total,
        "units_that_converged": converged,
        "words": words,
        "ceiling_mb": ceiling,
        "seconds_allowed_per_unit": seconds,
        "seconds": round(time.time() - started, 1),
        "parent_peak_resident_kb": peak_kb(),
    }
    document = {"summary": summary, "units": rows}
    handle = open(OUT, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    for name in sorted(summary):
        sys.stdout.write("   %-40s %s\n" % (name, summary[name]))
    sys.stdout.write("-- wrote %s\n" % OUT)
    sys.stdout.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())
