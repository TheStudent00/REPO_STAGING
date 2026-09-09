#!/usr/bin/env python3
"""build_supersession_asg.py -- extend the supersession sidecar over the
118 out-of-scope assignment-run findings (task 50(b)).

WHAT THIS READS

`supersession_altered_testimony.json`'s own `out_of_scope` list (118
records, log 140 §8.1's population) and the three NEW verbatim stores
`recapture_asg.py --merge` wrote: `op_units_asg_go_verbatim.json`,
`op_units_asg_rust_verbatim.json`, `op_units_asg_swift_verbatim.json`.

WHAT THIS WRITES

A NEW sidecar, `supersession_altered_testimony2.json`.  The original
`supersession_altered_testimony.json` is opened read-only and never
rewritten -- this is a second sidecar, not an edit of the first, exactly
as `supersession_altered_testimony.json` itself was a sidecar rather than
an edit of any `op_units_*.json`.

THE JOIN, stated

Each out-of-scope record names an `origin_store` and a `record` number.
Two shapes occur:

  - `op_pipeline/op_units_asg_<lang>.json`, record N -- the SAME
    numbering as `probe_manifest_asg_<lang>.json`, so the join key into
    the new verbatim store is N unchanged.
  - `stage_asg/op_units_<lang>.json`, record N -- `asg_stage.py`'s own
    offset (`ASG_N_OFFSET = 100000`), so the join key is N - 100000.

Both shapes name the SAME underlying assignment-run probe; the join is
therefore whole-record identity via the probe's own number, with no
operator token anywhere in the key -- the same join kind the first
sidecar used ("whole-source identity with the probe numbering erased").

A record is marked SUPERSEDED when the new verbatim store's decoded
`refused` (or `ok`) text for that probe number matches
`suspected_original_in_log_126` CHARACTER FOR CHARACTER.  Any other
outcome (no matching probe, text differs, field missing) is left
unresolved and reported by name -- never guessed.

THE SPELLING BAN, pasted verbatim as required: "THE SPELLING BAN,
ABSOLUTE (the owner, restated in anger 2026-08-25 after a second violation). No
operator token may appear in ANY key, grouping, pairing, row structure,
candidate selection, or comparison scope, anywhere in this line -- not in
matching, not in "which pairs get compared", not in report rows, not in
dropdowns. The candidate set for comparison comes from machine-form
evidence (clusters, connections, type pairs) or from ratified intention
-- never from the token. The token appears exactly once per unit: as a
display label on the member. HISTORY OF VIOLATIONS, so the pattern is
visible: (1) the arch campaign's cross-language matrix (caught by the owner
2026-08-24); (2) verdicts.py's row pairing (caught by the owner 2026-08-25 --
the fix brief itself reintroduced it as "same-operator pairs").
MECHANICAL GUARD REQUIRED: every pipeline stage that groups or pairs
units must run the spelling-key check (op_pipeline/check_no_spelling_keys.py)
and refuse its own output on failure. A brief handed to any subagent for
this line MUST paste this paragraph verbatim." This program's own join
key is a probe NUMBER, never an operator token; its output is walked by
`check_no_spelling_keys.py` and deleted on a failure.

usage:
    /tmp/reconnect_venv/bin/python3 build_supersession_asg.py
"""

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ASG_N_OFFSET = 100000

VERBATIM_STORES = {
    "go": "op_units_asg_go_verbatim.json",
    "rust": "op_units_asg_rust_verbatim.json",
    "swift": "op_units_asg_swift_verbatim.json",
}


def recaptured_text(store, key):
    entry = store["probes"].get(key)
    if entry is None:
        return None, "no probe %s in the verbatim store" % key
    if "refused" in entry:
        return entry["refused"], None
    # accepted probes carry no diagnostic text to compare; the audit's
    # out-of-scope population is entirely REFUSED-field findings (log 126
    # §3.2's ALTERED count is over `refused`/`ok` diagnostic text -- for
    # this population it is refused text throughout, checked below).
    return None, "probe %s carries no 'refused' field in the verbatim store" % key


def main():
    src_path = os.path.join(HERE, "supersession_altered_testimony.json")
    src = json.load(open(src_path))
    out_of_scope = src["out_of_scope"]

    stores = {}
    for lang, fname in VERBATIM_STORES.items():
        path = os.path.join(HERE, fname)
        stores[lang] = json.load(open(path))

    superseded = []
    mismatches = []
    unresolved = []

    for rec in out_of_scope:
        lang = rec["language"]
        origin = rec["origin_store"]
        n = int(rec["record"])
        if origin.startswith("stage_asg/"):
            key = str(n - ASG_N_OFFSET)
        else:
            key = str(n)
        store = stores.get(lang)
        if store is None:
            unresolved.append({"record": rec, "reason": "no verbatim store for language %s" % lang})
            continue
        text, err = recaptured_text(store, key)
        if err is not None:
            unresolved.append({"record": rec, "join_key": key, "reason": err})
            continue
        expected = rec["suspected_original_in_log_126"]
        if text == expected:
            superseded.append({
                "language": lang,
                "run": rec.get("run"),
                "origin_store": origin,
                "record": rec["record"],
                "field": rec["field"],
                "stored_altered_text": rec["stored_altered_text"],
                "suspected_original_in_log_126": expected,
                "superseded_by": {
                    "capture": "the unfiltered re-capture of the assignment "
                               "lane through the verbatim path (task 50(b))",
                    "store": VERBATIM_STORES[lang],
                    "record": key,
                    "recaptured_diagnostic": text,
                    "match": "character for character",
                },
            })
        else:
            mismatches.append({
                "record": rec,
                "join_key": key,
                "recaptured_diagnostic": text,
            })

    doc = {}
    doc["generated_by"] = "build_supersession_asg.py"
    doc["what_this_is"] = (
        "a SIDECAR extending supersession_altered_testimony.json's "
        "out_of_scope population (118 assignment-run findings) with a "
        "verbatim re-capture join. No existing store or the first "
        "sidecar is opened for writing anywhere in this program.")
    doc["ruling"] = (
        "task 50(b), log 140 section 8.3: re-capture the three op_asg_* "
        "lanes through the verbatim path so the 118 are superseded like "
        "the 218 were")
    doc["source_sidecar"] = "supersession_altered_testimony.json"
    doc["recaptured_stores"] = VERBATIM_STORES
    doc["totals"] = {
        "out_of_scope_in_source": len(out_of_scope),
        "superseded_now": len(superseded),
        "mismatched": len(mismatches),
        "unresolved": len(unresolved),
    }
    doc["superseded"] = superseded
    doc["mismatched"] = mismatches
    doc["unresolved"] = unresolved

    out_path = os.path.join(HERE, "supersession_altered_testimony2.json")
    tmp = out_path + ".tmp"
    fh = open(tmp, "w")
    json.dump(doc, fh, indent=1)
    fh.write("\n")
    fh.close()
    os.replace(tmp, out_path)

    print("out_of_scope in source     %d" % len(out_of_scope))
    print("superseded now             %d" % len(superseded))
    print("mismatched                 %d" % len(mismatches))
    print("unresolved                 %d" % len(unresolved))
    for m in mismatches:
        print("MISMATCH %s %s record %s"
              % (m["record"]["language"], m["record"]["origin_store"],
                 m["record"]["record"]))
        print("  stored (2026-08-25 lane): %r" % m["record"]["stored_altered_text"])
        print("  log 126 suspected:        %r" % m["record"]["suspected_original_in_log_126"])
        print("  recaptured (task 50b):    %r" % m["recaptured_diagnostic"])
    for u in unresolved:
        print("UNRESOLVED %s %s record %s -- %s"
              % (u["record"]["language"], u["record"]["origin_store"],
                 u["record"]["record"], u["reason"]))

    guard = subprocess.run(
        [sys.executable, os.path.join(HERE, "check_no_spelling_keys.py"),
         out_path], capture_output=True, text=True)
    print(guard.stdout.strip())
    if guard.returncode != 0:
        print(guard.stderr.strip())
        os.remove(out_path)
        raise SystemExit("REFUSED OWN OUTPUT: spelling guard failed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
