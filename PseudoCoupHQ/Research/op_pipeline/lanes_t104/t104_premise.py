#!/usr/bin/env python3
"""t104_premise.py -- WHERE the two differing texts of log_224 section
4 actually live: in `the_pool5.json`, in `term66_store/`, or in what
`term.py` prints today.

WHY THIS PROGRAM EXISTS.  Lane 1 measured that `Term.normalize` as
`term.py` stands PRINTS THE SAME TEXT for `cpp/op_509` and
`swift/regen_1023` -- the pair log_224 section 4 shows printing
differently.  A claim about a normalizer must therefore say which
artifact each text was read off, because three artifacts carry a
layer-5 text for the same unit and they were written on three
different days.  This program puts the three side by side.

It changes nothing.  It writes `t104_premise.json` and prints.

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
import resource
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PIPELINE = os.path.dirname(HERE)
sys.path.insert(0, PIPELINE)

OUT = os.path.join(PIPELINE, "t104_premise.json")

WANTED = [
    "cpp/op_509", "swift/regen_1023",
    "cpp/op_473", "swift/regen_1413",
    "swift/op_446", "swift/op_451",
]


def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def store_texts(store):
    """unit label -> the layer-5 text that store carries, for the six
    units only; one shard held at a time."""
    out = {}
    pattern = os.path.join(PIPELINE, store, "*.json")
    for path in sorted(glob.glob(pattern)):
        document = json.load(open(path))
        units = document.get("units") or {}
        for name in WANTED:
            if name not in units:
                continue
            out[name] = units[name].get("layer5_normalized_text")
        document = None
    return out


def pool5_texts():
    """unit label -> the layer-5 text `the_pool5.json` carries on that
    unit's member row."""
    path = os.path.join(PIPELINE, "the_pool5.json")
    document = json.load(open(path))
    out = {}
    entries = {}
    for entry in document["entries"]:
        for member in entry["members"]:
            if member["unit"] not in WANTED:
                continue
            out[member["unit"]] = member.get("layer5_normalized_text")
            entries[member["unit"]] = entry["entry_id"]
    document = None
    return out, entries


def main():
    sys.stdout.write("[1/3] the_pool5.json\n")
    sys.stdout.flush()
    five, entries = pool5_texts()
    sys.stdout.write("[2/3] term66_store and term65_store\n")
    sys.stdout.flush()
    sixty_six = store_texts("term66_store")
    sixty_five = store_texts("term65_store")
    sys.stdout.write("[3/3] the diagnosis lane's re-normalized text\n")
    sys.stdout.flush()
    diagnosed = {}
    path = os.path.join(PIPELINE, "t104_diagnose.json")
    if os.path.exists(path):
        document = json.load(open(path))
        for name in document:
            diagnosed[name] = document[name].get(
                "normalized_text_today")
    rows = {}
    for name in WANTED:
        rows[name] = {
            "pool5_entry_id": entries.get(name),
            "text_in_the_pool5_json": five.get(name),
            "text_in_term65_store": sixty_five.get(name),
            "text_in_term66_store": sixty_six.get(name),
            "text_term_py_prints_today": diagnosed.get(name),
        }
    handle = open(OUT, "w")
    json.dump(rows, handle, indent=1, sort_keys=True)
    handle.close()
    for name in WANTED:
        row = rows[name]
        sys.stdout.write("-- %s (pool5 entry %s)\n"
                         % (name, row["pool5_entry_id"]))
        sys.stdout.write("   the_pool5.json    %s\n"
                         % row["text_in_the_pool5_json"])
        sys.stdout.write("   term65_store      %s\n"
                         % row["text_in_term65_store"])
        sys.stdout.write("   term66_store      %s\n"
                         % row["text_in_term66_store"])
        sys.stdout.write("   term.py today     %s\n"
                         % row["text_term_py_prints_today"])
    sys.stdout.write("-- wrote %s, peak resident %d kB\n"
                     % (OUT, peak_kb()))
    sys.stdout.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())
