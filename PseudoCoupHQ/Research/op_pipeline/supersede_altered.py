#!/usr/bin/env python3
"""supersede_altered.py -- mark the altered testimony records SUPERSEDED by
the regeneration capture, in a NEW SIDECAR FILE.

WHAT AN ALTERED RECORD IS (log 126, task 37)

`lane_gen.py`'s driver substituted `|` with `/` in every stored compiler
diagnostic before writing it.  So a store can hold

    error[E0277]: no implementation for `i32 / f64`

for a probe whose expression was `a | b`.  The audit found 336 such
fields across ten stores, which are 158 DISTINCT captures counted twice
(the `stage_asg` stores are unions of the plain and assignment runs).

WHAT SUPERSESSION MEANS HERE, AND WHAT IT DOES NOT

  - It is a MARK, never an edit.  No store on disk is opened for writing
    by this program.  The mark lives in this program's own new file.
  - A record is superseded only when a verbatim capture of THE SAME PROBE
    exists.  A record with no such capture is reported, with the reason,
    never quietly counted as remediated.
  - The join is WHOLE-SOURCE IDENTITY: the probe's own source text, with
    its probe number erased (the two runs number from 0 in separate id
    spaces, so the same probe is `op_178` in one and `op_24400` in the
    other).  Two normalised texts are equal exactly when the two probes
    are the same probe.  Evidence class: forced by construction.  It is
    not a token match and it is not a text match on the diagnostic.

WHICH CAPTURES COUNT, AND THE MEASUREMENT THAT DECIDED IT

Two verbatim capture sets are read:

  - the filtered regeneration (`trickle_store/op_units2_*.json`);
  - the unfiltered re-capture of the three original plain lanes
    (`trickle_store/op_units_recapture_*.json`).

The regeneration ALONE supersedes nothing: joined on its own, zero of the
altered records match.  Every altered record is a REFUSAL, and a refusal
is what a compiler says about an operand shape the extracted rules call
illegal -- exactly the shape the legality filter never hands to a
compiler.  That is why `recapture_original.py` exists and why its stores
are read here.

THE ASSIGNMENT-RUN RECORDS ARE NOT COVERED, AND THAT IS STATED, NOT HIDDEN

The assignment bucket is excluded from probe generation (probe_gen.py's
own EXCLUDED_BUCKETS) and its probes come from a different generator, so
the assignment run's altered records have no counterpart in either
capture set.  They are listed as out of scope, by count and by store.

THE SPELLING BAN.  The join is a whole-text identity over the probe's own
source; nothing is keyed, grouped, paired or selected by an operator
token.  The output is walked by check_no_spelling_keys.py and this program
deletes its own output on a failure.

usage:
    /tmp/reconnect_venv/bin/python3 supersede_altered.py
writes:
    supersession_altered_testimony.json
"""

import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STORE_DIR = os.path.join(HERE, "trickle_store")

# The audit's stem -> the store it came from, and whether the
# regeneration covers that run at all.
STEM_LANGUAGE = {
    "go": ("go", "plain"),
    "rust": ("rust", "plain"),
    "swift": ("swift", "plain"),
    "asg_go": ("go", "assignment"),
    "asg_rust": ("rust", "assignment"),
    "asg_swift": ("swift", "assignment"),
}


def store_path(audit_file):
    """The audit names a store as `<area>/<file>`; resolve it.

    Both areas hold a file called `op_units_go.json`, so resolving by
    basename alone reads the wrong one -- which is what a first pass did,
    and 59 records came back unreadable because a record key from one
    store was looked up in the other."""
    area, name = audit_file.split("/", 1)
    if area == "op_pipeline":
        return os.path.join(HERE, name)
    return os.path.join(HERE, "..", area, name)


PROBE_NAME = re.compile(r"op_\d+")
# the generators also write the probe number into a leading comment
# ("// probe 178 -- binary |"), which is the same id-space difference
# in another place and is erased the same way.
PROBE_COMMENT = re.compile(r"probe \d+")


def normalised_source(text):
    """The probe's source with its own numbering erased.

    The two runs number their probes in separate id spaces, so the SAME
    probe is written `op_178` in one and `op_24400` in the other. Erasing
    the number leaves texts that are byte-identical exactly when the two
    probes are the same probe. This is the join: whole-artifact identity,
    forced by construction, with no token key anywhere in it."""
    if not text:
        return None
    out = PROBE_NAME.sub("op_N", text)
    return PROBE_COMMENT.sub("probe N", out)


OLD_SOURCE_CACHE = {}


def old_probe_source(lang, record_key, stem):
    """The source text the ORIGINAL run handed to the compiler.

    The stores do not keep `source` (fold drops it), so it is read from
    the run's own manifest -- `probe_manifest_<lang>.json` for the plain
    run, which is the only run the regeneration covers."""
    if lang not in OLD_SOURCE_CACHE:
        path = os.path.join(HERE, "probe_manifest_%s.json" % lang)
        OLD_SOURCE_CACHE[lang] = json.load(open(path))["probes"]
    rec = OLD_SOURCE_CACHE[lang].get(record_key)
    if rec is None:
        return None, None
    return normalised_source(rec.get("source")), rec


def old_probe_meta(audit_file, record_key):
    """The stored probe's own meta, from the ORIGINAL store, read only."""
    path = store_path(audit_file)
    if not os.path.exists(path):
        return None
    doc = json.load(open(path))
    probe = doc["probes"].get(record_key)
    if probe is None:
        return None
    return probe.get("meta")


def regen_index():
    """(language, normalised source text) -> the regenerated record.

    Built from every chunk store that has landed.  A key present here is
    a probe the regeneration has recaptured on the verbatim path.  The
    source texts come from the regeneration's own manifests, which is
    where they live; the stores carry the folded records.
    """
    index = {}
    chunks = []
    if not os.path.isdir(STORE_DIR):
        return index, chunks
    manifests = {}
    for name in sorted(os.listdir(STORE_DIR)):
        if not name.endswith(".json"):
            continue
        if not (name.startswith("op_units2_")
                or name.startswith("op_units_recapture_")):
            continue
        path = os.path.join(STORE_DIR, name)
        doc = json.load(open(path))
        chunks.append(doc["chunk_id"])
        lang = doc["language"]
        # each store names the manifest its probes came from, so the
        # filtered regeneration and the unfiltered re-capture are read
        # from their own manifests and never from each other's
        mname = doc["manifest"]
        if mname not in manifests:
            manifests[mname] = json.load(
                open(os.path.join(HERE, mname)))["probes"]
        for key in doc["probes"]:
            probe = doc["probes"][key]
            src = manifests[mname].get(key, {}).get("source")
            norm = normalised_source(src)
            if norm is None:
                continue
            index[(lang, norm)] = {
                "capture": ("the unfiltered re-capture of the original lane"
                            if name.startswith("op_units_recapture_")
                            else "the filtered regeneration"),
                "chunk_id": doc["chunk_id"],
                "store": path,
                "record": key,
                "recaptured_diagnostic": probe.get("refused"),
                "accepted": "refused" not in probe,
            }
    return index, chunks


def build():
    audit = json.load(open(os.path.join(HERE, "audit_altered_testimony.json")))
    index, chunks = regen_index()

    superseded = []
    not_yet = []
    out_of_scope = []
    seen = set()
    for finding in audit["findings"]:
        if finding["verdict"] != "ALTERED":
            continue
        stem = finding["stem"]
        if stem not in STEM_LANGUAGE:
            out_of_scope.append({"stem": stem, "record": finding["record"],
                                 "reason": "stem is not one of the six lanes "
                                           "that carry altered captures"})
            continue
        lang, run = STEM_LANGUAGE[stem]
        row = {
            "language": lang,
            "run": run,
            "origin_store": finding["file"],
            "record": finding["record"],
            "field": finding["field"],
            "stored_altered_text": finding["stored"],
            "suspected_original_in_log_126": finding["suspected_original"],
        }
        if run == "assignment":
            row["reason"] = (
                "the assignment bucket is excluded from probe generation, so "
                "the regeneration has no counterpart for this record and "
                "cannot supersede it")
            out_of_scope.append(row)
            continue
        meta = old_probe_meta(finding["file"], finding["record"])
        if meta is None:
            row["reason"] = ("the origin store's record could not be read "
                             "at %s" % store_path(finding["file"]))
            not_yet.append(row)
            continue
        norm, old_rec = old_probe_source(lang, finding["record"], stem)
        if norm is None:
            # A `stage_asg` store is the UNION of the plain and assignment
            # runs, so a record key it carries may belong to the
            # assignment run, whose probes are not in the plain manifest.
            # Those are the assignment case again, reached by a different
            # road, and they are reported as out of scope rather than as
            # something still to do.
            row["reason"] = (
                "this record key is not in the plain run's manifest, so it "
                "is an assignment-run row inside a union store; the "
                "assignment bucket is excluded from probe generation and "
                "has no regenerated or re-captured counterpart")
            out_of_scope.append(row)
            continue
        row["join"] = {
            "kind": "whole-source identity with the probe's own numbering "
                    "erased",
            "language": lang,
            "lhs_spelling": meta["lhs_type"],
            "rhs_spelling": meta.get("rhs_type"),
            "arity": meta["arity"],
        }
        hit = index.get((lang, norm))
        if hit is None:
            row["reason"] = (
                "the regeneration compiled no probe with this source. The "
                "usual cause is the legality filter: a candidate the "
                "extracted rules call illegal is never handed to a "
                "compiler, so a refusal the ORIGINAL run captured has no "
                "regenerated counterpart at all")
            not_yet.append(row)
            continue
        row["superseded_by"] = hit
        superseded.append(row)
        seen.add((finding["file"], finding["record"], finding["field"]))

    doc = {}
    doc["generated_by"] = "supersede_altered.py"
    doc["what_this_is"] = (
        "a SIDECAR. No existing store is opened for writing anywhere in "
        "this program; supersession is recorded here and nowhere else.")
    doc["ruling"] = (
        "log_129 addendum 2026-09-01: the regenerated stores ARE the "
        "testimony remediation (Route A subsumed); mark the old records "
        "superseded by the regeneration capture when their lanes land")
    doc["regenerated_chunks_read"] = chunks
    doc["totals"] = {
        "altered_findings_in_the_audit": len(
            [f for f in audit["findings"] if f["verdict"] == "ALTERED"]),
        "superseded_now": len(superseded),
        "not_yet_superseded": len(not_yet),
        "out_of_scope_for_this_regeneration": len(out_of_scope),
    }
    doc["superseded"] = superseded
    doc["not_yet_superseded"] = not_yet
    doc["out_of_scope"] = out_of_scope
    return doc


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
    doc = build()
    path = os.path.join(HERE, "supersession_altered_testimony.json")
    fh = open(path, "w")
    json.dump(doc, fh, indent=1)
    fh.write("\n")
    fh.close()
    t = doc["totals"]
    print("altered findings %d ; superseded now %d ; not yet %d ; "
          "out of scope %d"
          % (t["altered_findings_in_the_audit"], t["superseded_now"],
             t["not_yet_superseded"],
             t["out_of_scope_for_this_regeneration"]))
    print("wrote %s" % path)
    refuse_own_output_on_spelling_failure([path])


if __name__ == "__main__":
    main()
