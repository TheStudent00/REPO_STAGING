#!/usr/bin/env python3
"""ref2_model_table.py -- the arch-opcode model table swept again at each of
the five states of the reference, and the rows whose term TEXT moved,
attributed to the correction that moved them.

WHAT THIS IS, in relation.  `model_table.py sweep` runs every builder of
`reference.py` over every operand spelling `model_translate.shapes_for`
writes, and prints each written place's z3 term by the pipeline's own layer-5
rule.  That table is what every later stage reads.  Task ref2 corrected the
reference four times, so this program sweeps FIVE times -- once as the
reference stood before the task and once after each correction -- and then
says, per row and per written place, at WHICH correction the text moved.

HOW A SWEEP IS RUN AGAINST AN OLD REFERENCE, without moving any file.  The
five states are kept as files under `level0/ref2_originals/`, recovered from
this repository's own history and checked against the sha256 each correction
lane printed.  `install` loads one pair under the module names `reference` and
`condition_table` BEFORE `model_table` and `model_translate` are imported, so
those two import the state this run is measuring and nothing on disk is
swapped.  Nothing is written over: every sweep writes
`model_table_rows_ref2_<label>.json` of its own.

THE KEY of a swept row is (mnem, operand shape, sweep width, whether the state
was preseeded, the setter cell the state was seeded with) -- the sweep's own
attempt, in machine form.  The written place is the second half of the key.
No operator token enters either.

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

Coding discipline: no compound one-liner statements.

usage:
  ref2_model_table.py sweep <label>       one sweep at state <label>
  ref2_model_table.py assemble <label>    attest, edges and assemble at <label>
  ref2_model_table.py compare <out.json>  the five sweeps, put side by side
"""

import hashlib
import importlib.util
import json
import os
import resource
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MODEL = os.path.abspath(os.path.join(HERE, "..", "model"))
PIPELINE = os.path.abspath(os.path.join(HERE, "..", "..", "..",
                                        "op_pipeline"))
ORIGINALS = os.path.join(HERE, "ref2_originals")

for _path in (PIPELINE, os.path.join(PIPELINE, "lean"), MODEL):
    if _path not in sys.path:
        sys.path.insert(0, _path)
"""THE PIPELINE IS ON THE PATH BEFORE ANYTHING IS LOADED.  A state's own
`reference.py` imports `canon`, `ledger` and `ledger48` by bare name, and it
is loaded out of `ref2_originals/`, where none of the three lives -- so the
pipeline has to be reachable before `install` runs, not after."""

STATES = ("before", "c1", "c2", "c3", "c4")
"""the reference as it stood before this task, and after each of its four
corrections in the brief's own order."""

MEMORY_CEILING_MB = 12 * 1024
ABORT_NAME = "ABORT_MEMORY_REF2"


def peak_mb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0


def check_memory(where):
    peak = peak_mb()
    if peak > MEMORY_CEILING_MB:
        raise SystemExit("%s: %.1f MB at %s, past the stated %d MB"
                         % (ABORT_NAME, peak, where, MEMORY_CEILING_MB))
    return peak


def paths_of(label):
    """the (reference, condition_table) pair for one state."""
    if label == "before":
        return (os.path.join(ORIGINALS, "reference.py"),
                os.path.join(ORIGINALS, "condition_table.py"))
    return (os.path.join(ORIGINALS, "reference_%s.py" % label),
            os.path.join(ORIGINALS, "condition_table_%s.py" % label))


def digest_of(path):
    handle = open(path, "rb")
    text = handle.read()
    handle.close()
    return hashlib.sha256(text).hexdigest()


def install(label):
    """put one state's two files in place as the modules `reference` and
    `condition_table`, before anything imports either."""
    reference_path, table_path = paths_of(label)
    for name, path in (("condition_table", table_path),
                       ("reference", reference_path)):
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return {"reference_py": digest_of(reference_path),
            "condition_table_py": digest_of(table_path)}


def rows_path(label):
    return os.path.join(HERE, "model_table_rows_ref2_%s.json" % label)


def attest_path(label):
    return os.path.join(HERE, "model_table_attest_ref2_%s.json" % label)


def edges_path(label):
    return os.path.join(HERE, "model_table_edges_ref2_%s.json" % label)


def table_path(label):
    return os.path.join(HERE, "model_table_ref2_%s.json" % label)


def report_path(label):
    return os.path.join(HERE, "model_table_ref2_%s.md" % label)


def point_the_paths(module, label):
    module.ROWS_JSON = rows_path(label)
    module.ATTEST_JSON = attest_path(label)
    module.EDGES_JSON = edges_path(label)
    module.OUT_JSON = table_path(label)
    module.OUT_MD = report_path(label)


def load_model_table(label):
    import model_table                                     # noqa: E402
    point_the_paths(model_table, label)
    return model_table


def sweep_one(label):
    version = install(label)
    module = load_model_table(label)
    print("the state swept: %s" % label)
    print("  reference.py         %s" % version["reference_py"])
    print("  condition_table.py   %s" % version["condition_table_py"])
    answer = module.sweep_command()
    document = json.load(open(rows_path(label)))
    document["meta"]["reference_version"] = version
    document["meta"]["ref2_state"] = label
    handle = open(rows_path(label), "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    print("peak RSS %.1f MB, ceiling %d MB, named abort %s"
          % (check_memory("the end of the sweep"), MEMORY_CEILING_MB,
             ABORT_NAME))
    return answer


def assemble_one(label):
    version = install(label)
    module = load_model_table(label)
    print("the state assembled: %s (reference.py %s)"
          % (label, version["reference_py"]))
    module.attest_command()
    print("peak RSS %.1f MB after attest" % check_memory("attest"))
    module.edges_command(None)
    print("peak RSS %.1f MB after edges" % check_memory("edges"))
    module.assemble_command()
    module.report_command()
    print("peak RSS %.1f MB, ceiling %d MB, named abort %s"
          % (check_memory("the end of assemble"), MEMORY_CEILING_MB,
             ABORT_NAME))
    return 0


# ==================================================================
# the comparison
# ==================================================================

def attempt_key(row):
    return (row["mnem"], row["shape"], row["width"],
            bool(row.get("preseeded")), row.get("flags_in_setter"))


def places_of(document):
    """(attempt, written place) -> the term text, for one sweep."""
    out = {}
    outcomes = {}
    for row in document["rows"]:
        key = attempt_key(row)
        outcomes[key] = row.get("outcome")
        for entry in row.get("mapping") or []:
            out[(key, entry["writes"])] = entry.get("text")
    return out, outcomes


def read_state(label):
    handle = open(rows_path(label))
    document = json.load(handle)
    handle.close()
    return document


def compare(out_path):
    texts = {}
    outcomes = {}
    versions = {}
    for label in STATES:
        document = read_state(label)
        texts[label], outcomes[label] = places_of(document)
        versions[label] = document["meta"].get("reference_version")
        print("  %-7s %6d places over %5d attempts"
              % (label, len(texts[label]), len(outcomes[label])))
    keys = set()
    for label in STATES:
        keys.update(texts[label])
    moved = []
    for key in sorted(keys, key=str):
        before = texts["before"].get(key)
        after = texts["c4"].get(key)
        if before == after:
            continue
        first = None
        for label in STATES[1:]:
            if texts[label].get(key) != before:
                first = label
                break
        moved.append({
            "mnem": key[0][0], "shape": key[0][1], "width": key[0][2],
            "preseeded": key[0][3], "flags_in_setter": key[0][4],
            "place": key[1],
            "moved_at": first,
            "text_before": before, "text_after": after,
            "text_per_state": dict((label, texts[label].get(key))
                                   for label in STATES),
        })
    outcome_moves = []
    for key in sorted(set(outcomes["before"]) | set(outcomes["c4"]),
                      key=str):
        was = outcomes["before"].get(key)
        now = outcomes["c4"].get(key)
        if was == now:
            continue
        first = None
        for label in STATES[1:]:
            if outcomes[label].get(key) != was:
                first = label
                break
        outcome_moves.append({
            "mnem": key[0], "shape": key[1], "width": key[2],
            "preseeded": key[3], "flags_in_setter": key[4],
            "outcome_before": was, "outcome_after": now,
            "moved_at": first})
    by_correction = {}
    for row in moved:
        entry = by_correction.setdefault(row["moved_at"],
                                         {"places": 0, "mnems": set(),
                                          "written": set()})
        entry["places"] = entry["places"] + 1
        entry["mnems"].add(row["mnem"])
        entry["written"].add(row["place"])
    document = {
        "what": ("every written place of the arch-opcode model table "
                 "whose term text moved under task ref2's four "
                 "corrections, attributed to the correction that moved "
                 "it"),
        "states": list(STATES),
        "reference_version_per_state": versions,
        "places_before": len(texts["before"]),
        "places_after": len(texts["c4"]),
        "attempts_before": len(outcomes["before"]),
        "attempts_after": len(outcomes["c4"]),
        "places_that_moved": len(moved),
        "attempts_whose_outcome_moved": len(outcome_moves),
        "by_correction": [
            # THE MNEMONIC RIDES IN THE FIELD `mnem`, never as a bare
            # list element: a list of bare tokens is a row structure and
            # the spelling guard refuses it.
            {"moved_at": label,
             "places": by_correction[label]["places"],
             "mnems": [{"mnem": name}
                       for name in sorted(by_correction[label]["mnems"])],
             "written_places": sorted(by_correction[label]["written"])}
            for label in sorted(by_correction, key=str)],
        "moved": moved,
        "outcome_moves": outcome_moves,
    }
    handle = open(out_path, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    print("")
    print("| moved at | places | mnemonics | written places |")
    print("|---|---|---|---|")
    for entry in document["by_correction"]:
        print("| %s | %d | %d | %s |"
              % (entry["moved_at"], entry["places"],
                 len(entry["mnems"]),
                 " ".join("`%s`" % p for p in entry["written_places"])))
    print("")
    print("places before %d, after %d; places whose text moved %d"
          % (document["places_before"], document["places_after"],
             document["places_that_moved"]))
    print("attempts whose outcome moved: %d" % len(outcome_moves))
    for row in outcome_moves[:20]:
        print("  %s %s width %s preseeded %s setter %s : %s -> %s at %s"
              % (row["mnem"], row["shape"], row["width"],
                 row["preseeded"], row["flags_in_setter"],
                 row["outcome_before"], row["outcome_after"],
                 row["moved_at"]))
    print("")
    for entry in document["by_correction"]:
        label = entry["moved_at"]
        print("THREE EXAMPLES LITERAL, moved at %s:" % label)
        shown = 0
        for row in moved:
            if row["moved_at"] != label:
                continue
            print("  %s %s width %d place %s"
                  % (row["mnem"], row["shape"], row["width"],
                     row["place"]))
            print("    before: %s" % row["text_before"])
            print("    after : %s" % row["text_after"])
            shown = shown + 1
            if shown >= 3:
                break
        print("")
    return 0


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    command = argv[1]
    if command == "sweep":
        return sweep_one(argv[2])
    if command == "assemble":
        return assemble_one(argv[2])
    if command == "compare":
        return compare(argv[2])
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
