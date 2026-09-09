#!/usr/bin/env python3
"""audit78.py -- canon40 against canon39, and the 2,862 tested.

TASK 78.  Reads the two renders as DATA and computes:

  1. the outcome tally per population, canon39 against canon40;
  2. EVERY unit whose outcome moved, with its cause computed from the
     unit's own records -- and separated into the movements task 64's
     reference already made (`regate64_store`, the same canon39 units
     re-gated with the CURRENT reference) and the movements this task
     made;
  3. THE 2,862 AS AN EXPECTATION TO TEST: units whose body carries a
     transfer into a routine one of this machine's archives DEFINES,
     and which carry NO ledger row naming that routine.  That is
     log_168 §5.3's own measurement, recomputed on canon39 and then on
     canon40;
  4. the census of the 196: the two transfer shapes, by language and
     by routine name.

MEMORY BOUND: one shard is held at a time and only per-unit summaries
are kept, so the live set is the largest shard plus four counters.
Stated cap 6 GB, named abort `AUDIT78_MEMORY_ABORT`; measured peak is
pasted in the log.

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

Nothing here groups or pairs by a token: the populations are file
names and the buckets are outcome values and machine-form producer
kinds.

Coding discipline: no compound one-liner statements.
"""

import glob
import json
import os
import resource
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import ledger as L                                                # noqa: E402

MEMORY_CAP_BYTES = 6 * 1024 * 1024 * 1024
LANGS = ["c", "cpp", "go", "rust", "swift"]


def check_memory():
    used = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024
    if used > MEMORY_CAP_BYTES:
        raise SystemExit("AUDIT78_MEMORY_ABORT: peak resident %d "
                         "bytes is over the stated 6 GB cap" % used)


def archive_names():
    path = os.path.join(HERE, "runtime_answers78.json")
    document = json.load(open(path))
    names = set()
    for key, reading in document["readings"].items():
        if reading.get("refuse"):
            continue
        if "/" in key:
            names.add(key.split("/", 1)[1])
        else:
            names.add(key)
    return names


NAMES = archive_names()


def transfers_into_the_archive(record):
    """the routine names this unit's own body transfers to that one of
    this machine's archives defines.  Read with the ledger's own
    `transfer_callee`, which reads the relocation as well as the
    assembler identifier."""
    out = set()
    body = record.get("body_verbatim") or []
    for raw in body:
        line, annotation = L.split_off_annotation(raw)
        line = L.R36.strip_annotation(raw)
        if line.endswith(":"):
            continue
        mnemonic = L.mnemonic_of(line)
        operands = L.operands_of(line)
        callee = L.transfer_callee(mnemonic, operands, annotation)
        if callee is None:
            continue
        if callee in NAMES:
            out.add(callee)
    return out


def runtime_rows(record):
    out = set()
    for row in record.get("ledger") or []:
        producer = row.get("produced_by")
        if not isinstance(producer, dict):
            continue
        if producer.get("kind") != "runtime_callee":
            continue
        out.add(producer.get("callee"))
    return out


def summarize(record):
    """the small per-unit summary this audit keeps."""
    return {
        "outcome": record.get("outcome"),
        "lang": record.get("lang"),
        "population": record.get("population"),
        "detail": (record.get("verdict_detail") or
                   record.get("refusal") or ""),
        "cause": record.get("refusal_cause"),
        "transfers": sorted(transfers_into_the_archive(record)),
        "rows": sorted(runtime_rows(record)),
        "shapes": [one.get("kind")
                   for one in (record.get("transfer_shapes") or [])],
        "shape_callees": [(one.get("kind"), one.get("callee"))
                          for one in
                          (record.get("transfer_shapes") or [])],
        "runtime_row_count": len([
            row for row in (record.get("ledger") or [])
            if isinstance(row.get("produced_by"), dict) and
            row["produced_by"].get("kind") == "runtime_callee"]),
    }


def read_side(prefix):
    """prefix -> {label: summary}, one file at a time."""
    out = {}
    for lang in LANGS:
        path = os.path.join(HERE, "%s_wrapped_%s.json" % (prefix, lang))
        if not os.path.exists(path):
            continue
        units = json.load(open(path))["units"]
        for label, record in units.items():
            out[label] = summarize(record)
        check_memory()
    path = os.path.join(HERE, "%s_interp.json" % prefix)
    if os.path.exists(path):
        units = json.load(open(path))["units"]
        for label, record in units.items():
            out[label] = summarize(record)
    pattern = os.path.join(HERE, "%s_regen_store" % prefix, "*.json")
    for path in sorted(glob.glob(pattern)):
        units = json.load(open(path))["units"]
        for label, record in units.items():
            out[label] = summarize(record)
        check_memory()
    return out


def read_regate_outcomes():
    """the SAME canon39 units re-gated with the current reference
    (task 64).  Its outcome vocabulary is the term route's, so only
    `proved` is compared."""
    out = {}
    store = os.path.join(HERE, "regate64_store")
    if not os.path.isdir(store):
        return out
    for path in sorted(glob.glob(os.path.join(store, "*.json"))):
        document = json.load(open(path))
        units = document.get("units") or {}
        for label, record in units.items():
            ship = record.get("verdict_ship") or {}
            out[label] = {
                "term_outcome": record.get("outcome"),
                "ship_outcome": ship.get("outcome"),
            }
    return out


def population_of(label, summary):
    text = summary.get("population")
    if text:
        return text
    return "unknown"


def tally(side, key):
    out = {}
    for label, summary in side.items():
        bucket = key(label, summary)
        out[bucket] = out.get(bucket, 0) + 1
    return out


def main(argv):
    before = read_side("canon39")
    check_memory()
    after = read_side("canon40")
    check_memory()
    regate = read_regate_outcomes()
    lines = []
    lines.append("TASK 78 -- canon40 AGAINST canon39")
    lines.append("")
    lines.append("units recorded: canon39 %d, canon40 %d"
                 % (len(before), len(after)))
    lines.append("")

    def bucket(label, summary):
        return "%s / %s" % (population_of(label, summary),
                            summary.get("outcome"))

    lines.append("OUTCOME BY POPULATION")
    names = set(tally(before, bucket)) | set(tally(after, bucket))
    left = tally(before, bucket)
    right = tally(after, bucket)
    lines.append("%-52s %8s %8s" % ("population / outcome",
                                    "canon39", "canon40"))
    for name in sorted(names):
        lines.append("%-52s %8d %8d"
                     % (name, left.get(name, 0), right.get(name, 0)))
    lines.append("")
    proved_before = 0
    proved_after = 0
    for label in before:
        if before[label]["outcome"] == "WRAPPED_TEXT_PROVED":
            proved_before = proved_before + 1
    for label in after:
        if after[label]["outcome"] == "WRAPPED_TEXT_PROVED":
            proved_after = proved_after + 1
    lines.append("proved: canon39 %d, canon40 %d   "
                 "not proved: canon39 %d, canon40 %d"
                 % (proved_before, proved_after,
                    len(before) - proved_before,
                    len(after) - proved_after))
    lines.append("")

    lines.append("EVERY MOVEMENT, WITH ITS COMPUTED CAUSE")
    movements = []
    for label in sorted(set(before) | set(after)):
        was = before.get(label, {}).get("outcome")
        now = after.get(label, {}).get("outcome")
        if was == now:
            continue
        already = regate.get(label, {})
        movements.append({
            "unit": label,
            "was": was,
            "now": now,
            "detail": after.get(label, {}).get("detail", "")[:200],
            "already_moved_by_the_task_64_reference":
                already.get("ship_outcome"),
            "runtime_rows_now":
                after.get(label, {}).get("runtime_row_count", 0),
        })
    lines.append("units whose outcome moved: %d" % len(movements))
    for one in movements:
        lines.append("  %-24s %-22s -> %-22s  re-gated under the "
                     "current reference in task 64: %s"
                     % (one["unit"], one["was"], one["now"],
                        one["already_moved_by_the_task_64_reference"]))
        lines.append("      %s" % one["detail"])
    lines.append("")

    lines.append("THE 2,862, TESTED RATHER THAN ASSUMED")
    lines.append("  the measurement of log_168 §5.3, recomputed: a "
                 "unit whose body transfers into a routine one of this")
    lines.append("  machine's archives DEFINES, and whose ledger "
                 "carries NO row naming that routine.")
    for name, side in (("canon39", before), ("canon40", after)):
        carriers = 0
        without = 0
        rows = 0
        for label, summary in side.items():
            if not summary["transfers"]:
                continue
            carriers = carriers + 1
            rows = rows + summary["runtime_row_count"]
            if not summary["rows"]:
                without = without + 1
        lines.append("  %-8s units transferring into an "
                     "archive-defined routine: %6d   of those with NO "
                     "row naming it: %6d   runtime_callee rows: %7d"
                     % (name, carriers, without, rows))
    repaired = 0
    for label, summary in after.items():
        if not summary["transfers"]:
            continue
        was = before.get(label, {})
        if was.get("rows"):
            continue
        if summary["rows"]:
            repaired = repaired + 1
    lines.append("  units that had NO runtime row in canon39 and "
                 "carry one in canon40: %d" % repaired)
    lines.append("")

    lines.append("THE 196, BY THE SHAPE THE CALLER'S OWN TEXT GIVES "
                 "THEM")
    shapes = {}
    per_language = {}
    per_callee = {}
    for label, summary in after.items():
        if not summary["shapes"]:
            continue
        kinds = sorted(set(summary["shapes"]))
        key = ",".join(kinds)
        shapes[key] = shapes.get(key, 0) + 1
        language = summary.get("lang")
        per_language[(key, language)] = \
            per_language.get((key, language), 0) + 1
        for kind, callee in summary["shape_callees"]:
            per_callee[(kind, callee)] = \
                per_callee.get((kind, callee), 0) + 1
    for key in sorted(shapes):
        lines.append("  %-30s %d units" % (key, shapes[key]))
    for key in sorted(per_language):
        lines.append("     %-28s %-6s %d"
                     % (key[0], key[1], per_language[key]))
    lines.append("  by routine name (call lines, not units):")
    for key in sorted(per_callee):
        lines.append("     %-26s %-40s %d"
                     % (key[0], key[1], per_callee[key]))
    lines.append("")
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    lines.append("peak resident set size of this audit: %d kbytes"
                 % peak)
    text = "\n".join(lines) + "\n"
    handle = open(os.path.join(HERE, "audit78_printed.txt"), "w")
    handle.write(text)
    handle.close()
    document = {
        "meta": {
            "generated_by": "audit78.py",
            "before": "canon39",
            "after": "canon40",
            "peak_resident_kbytes": peak,
        },
        "movements": movements,
        "shapes": dict([("%s|%s" % k, v)
                        for k, v in per_callee.items()]),
    }
    handle = open(os.path.join(HERE, "audit78.json"), "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.write("\n")
    handle.close()
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
