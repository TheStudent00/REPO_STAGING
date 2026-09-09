#!/usr/bin/env python3
"""t91_regate_run.py -- TASK 91's RE-GATE: every canon38 term put again
to the ONE reference, so the 415 withdrawn disproofs and the 5,602
undecided verdicts of log 153 are answered by measurement.

WHAT MOVES AND WHAT IS HELD STILL, said before any figure.  Exactly one
thing moves: the reference.  The population is canon38's, the ledger is
canon38's as stored, the transcription is `layer4c.transcribe` (task
53's own superseded record, READ and never edited), and the obligations
are `gate.Gate`'s.  The reference is `reference.py` -- THE one symbolic
simulator, carrying `SRem`/`URem` for the machine's remainder, the
machine stack, the x87 stack, real IEEE floats, the body walked as its
own control-flow graph, and the step into an attached runtime callee.
`gate58_run.py` ran this same population through an EARLIER state of
that one file and is round 12's record; this file is round 17's run and
edits nothing it reads.

THE TWO CONFIGURATIONS, both of the ONE reference, run separately
because they answer two different questions and mixing them would hide
which one moved a verdict:

  no_attached_callees -- the reference holds no archive, so a `call` is
      a transfer OUT of the unit (reference CORE: "A `call` whose callee
      is NOT attached is a transfer out of the unit").  This is the
      configuration `gate58_run.py` ran.
  attached_callees -- the reference holds the attached callee bodies of
      `canon39_callee_units.json` (task 63) and steps into the callee's
      own body (reference CORE: "A `call` WITH AN ATTACHED CALLEE IS
      NOT A TRANSFER").

THE MEMORY BOUND.  One canon38 source document is held at a time and
released before the next; no term, state or solver is kept across
units.  The cap is 6,000 MB, checked after every source document, and
the abort is named `T91_MEMORY_ABORT`.

TIME.  `gate.SOLVER_MILLISECONDS` is a WALL CLOCK, so a verdict can
move between two runs of unchanged code.  This file therefore writes a
store per (configuration, run label), and `--label control` re-runs the
identical code so the run-to-run movement can be separated from the
movement the reference caused.  Nothing being measured is changed to
make a run fit a limit.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation). No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns. The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token. The
token appears exactly once per unit: as a display label on the member.
HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs"). MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure. A brief handed to any subagent for this
line MUST paste this paragraph verbatim."

No operator token appears in this file.  Units are walked in the fixed
order of their own source documents; nothing is grouped, paired or
selected by any spelling.

Coding discipline (the owner's ruling): no compound one-liner statements.

usage:
  t91_regate_run.py --configuration=<tag> [--label=<run>] [--shard=i/n]
"""

import glob
import json
import os
import resource
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import gate as GATE                                               # noqa: E402
import layer4c                                                    # noqa: E402
import reference as REF                                           # noqa: E402

LANGS = ("c", "cpp", "go", "rust", "swift")
MEMORY_CAP_MB = 6000
MEMORY_ABORT = "T91_MEMORY_ABORT"


def peak_resident_mb():
    usage = resource.getrusage(resource.RUSAGE_SELF)
    return usage.ru_maxrss / 1024.0


def check_memory(stage):
    now = peak_resident_mb()
    if now > MEMORY_CAP_MB:
        raise SystemExit(
            "%s: peak resident size %.1f MB passed this run's stated "
            "cap of %d MB during %s"
            % (MEMORY_ABORT, now, MEMORY_CAP_MB, stage))
    return now


def sources():
    """every canon38 source document, in a fixed order -- the same list
    `gate58_run.sources()` walks, so the two runs join by shard as well
    as by unit name."""
    out = []
    for lang in LANGS:
        out.append(("original_%s" % lang,
                    os.path.join(HERE,
                                 "canon38_wrapped_%s.json" % lang)))
    out.append(("interp", os.path.join(HERE, "canon38_interp.json")))
    pattern = os.path.join(HERE, "canon38_regen_store", "*.json")
    for path in sorted(glob.glob(pattern)):
        tag = "regen_%s" % os.path.basename(path)[:-5]
        out.append((tag, path))
    return [(tag, path) for tag, path in out if os.path.exists(path)]


def callee_units():
    """the attached callee arch units of task 63, keyed by toolchain and
    then by routine name -- `regate64_run.callee_units`'s own shape."""
    path = os.path.join(HERE, "canon39_callee_units.json")
    if not os.path.exists(path):
        return {}
    document = json.load(open(path))
    out = {}
    for key, unit in document.get("units", {}).items():
        toolchain = unit.get("toolchain")
        if toolchain is None:
            toolchain = key.split("/", 1)[0]
        name = unit.get("callee")
        if name is None:
            name = key.split("/", 1)[-1]
        out.setdefault(toolchain, {})
        out[toolchain][name] = unit
    return out


def state_of(record):
    """the FOUR STATES log 153 section 1.2 counts, read off one record.
    `t91_populations.state_of`'s rule, applied to a new record."""
    if not record.get("term_built"):
        return "no term"
    outcomes = (record.get("ship", {}).get("outcome"),
                record.get("text", {}).get("outcome"))
    if "DISPROVED" in outcomes:
        return "withdrawn"
    if "PROVED_ON_SHIP" in outcomes:
        return "proved"
    if "PROVED_BY_CONSTRUCTION" in outcomes:
        return "proved"
    return "undecided"


def one_unit(gate, name, unit):
    """one canon38 unit -> its re-gated record.  `gate58_run.one_unit`'s
    shape, so the two runs join field by field."""
    record = {
        "unit": name,
        "lang": unit.get("lang"),
        "population": unit.get("population"),
        "term_built": False,
        "transcription_refused": None,
    }
    unit = dict(unit)
    unit["unit"] = name
    try:
        transcription = layer4c.transcribe(unit)
    except Exception as problem:
        record["transcription_refused"] = (
            "the transcription raised %s: %s"
            % (type(problem).__name__, problem))
        record["state"] = "no term"
        return record
    if transcription.refused is not None:
        record["transcription_refused"] = transcription.refused
        record["state"] = "no term"
        return record
    term = transcription.out_term
    if term is None:
        record["ship"] = gate.prove_term_against_ship(None,
                                                      unit).as_dict()
        record["text"] = gate.prove_term_against_text(None,
                                                      unit).as_dict()
        record["state"] = "no term"
        return record
    record["term_built"] = True
    record["ship"] = gate.prove_term_against_ship(term, unit).as_dict()
    record["text"] = gate.prove_term_against_text(term, unit).as_dict()
    record["state"] = state_of(record)
    return record


def run_one_source(gate, store, tag, path, configuration, label):
    document = json.load(open(path))
    units = {}
    for name, unit in sorted(document["units"].items()):
        if "ledger" not in unit:
            continue
        units[name] = one_unit(gate, name, unit)
    out = {
        "meta": {
            "generated_by": "t91_regate_run.py",
            "configuration": configuration,
            "run_label": label,
            "source": os.path.basename(path),
            "population": document.get("meta", {}).get("population"),
            "solver_milliseconds": GATE.SOLVER_MILLISECONDS,
        },
        "units": units,
    }
    target = os.path.join(store, "%s.json" % tag)
    handle = open(target + ".part", "w")
    json.dump(out, handle, indent=1, sort_keys=True)
    handle.close()
    os.rename(target + ".part", target)
    return len(units)


def main(argv):
    shard = 0
    shards = 1
    configuration = None
    label = "fix"
    for argument in argv:
        if argument.startswith("--shard="):
            piece = argument.split("=", 1)[1]
            shard = int(piece.split("/")[0])
            shards = int(piece.split("/")[1])
        if argument.startswith("--configuration="):
            configuration = argument.split("=", 1)[1]
        if argument.startswith("--label="):
            label = argument.split("=", 1)[1]
    if configuration not in ("no_attached_callees", "attached_callees"):
        print("--configuration=no_attached_callees or "
              "--configuration=attached_callees is required")
        return 2
    store = os.path.join(HERE, "t91_regate_store_%s_%s"
                         % (configuration, label))
    if not os.path.isdir(store):
        os.makedirs(store)
    runtime_units = None
    if configuration == "attached_callees":
        runtime_units = callee_units()
    reference = REF.Reference(runtime_units=runtime_units)
    gate = GATE.Gate(reference=reference)
    every = sources()
    mine = []
    for index, entry in enumerate(every):
        if index % shards == shard:
            mine.append(entry)
    started = time.time()
    for number, (tag, path) in enumerate(mine):
        target = os.path.join(store, "%s.json" % tag)
        if os.path.exists(target):
            continue
        count = run_one_source(gate, store, tag, path, configuration,
                               label)
        rss = check_memory("source %s" % tag)
        print("[%d/%d] %7.1fs  %-40s %5d units  peak %.0f MB"
              % (number + 1, len(mine), time.time() - started, tag,
                 count, rss))
        sys.stdout.flush()
    print("shard %d/%d of configuration %r label %r finished; "
          "peak resident size %.1f MB, cap %d MB"
          % (shard, shards, configuration, label, peak_resident_mb(),
             MEMORY_CAP_MB))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
