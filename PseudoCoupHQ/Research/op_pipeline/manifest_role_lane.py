#!/usr/bin/env python3
"""manifest_role_lane.py -- declare the probe manifests to be what
they already are: generator provenance.

Why
---
the owner ruled 2026-08-26 that he is agnostic on MECHANISM; the spelling
ban is a ban on spell-MATCHING.  A probe manifest records what the
generator asked each compiler for.  It is read by exactly two things:
the generator that wrote it, and check_no_spelling_keys.py's
`inventory()`, which harvests the token set the guard then hunts for.
It never supplies a key, a grouping, a pairing, a row structure, a
candidate selection or a comparison scope.  So its `operator` field is
provenance, not a spelling key.

This program makes that fact a declared field rather than an
understanding, so the guard can act on it:

    meta.role = "generator provenance"

THE EDIT IS ADDITIVE.  One field is inserted into the top-level `meta`
object of each manifest.  Nothing is removed, nothing is renamed, no
object is reshaped, and the probes are not touched at all.  The file is
re-serialised with the same `indent=1` the generators used, and the
program prints a byte-level before/after size for each file so the size
of the edit is visible.

Rerunning is safe: a manifest that already carries the declaration is
reported as already declared and left alone.

usage:
  manifest_role_lane.py [--dry-run]
"""

import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

ROLE_FIELD = "role"

ROLE_VALUE = "generator provenance"


def log(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def manifest_paths():
    pattern = os.path.join(HERE, "probe_manifest_*.json")
    paths = glob.glob(pattern)
    paths.sort()
    return paths


def already_declared(doc):
    meta = doc.get("meta")
    if not isinstance(meta, dict):
        return False
    if meta.get(ROLE_FIELD) == ROLE_VALUE:
        return True
    return False


def with_role_first(meta):
    """the same meta object with the role declared as its first key.

    A new dict is built rather than assigned into, so the declaration
    reads at the top of the object instead of trailing the holders and
    the acceptance record."""
    out = {}
    out[ROLE_FIELD] = ROLE_VALUE
    for k in meta:
        if k == ROLE_FIELD:
            continue
        out[k] = meta[k]
    return out


def had_trailing_newline(path):
    """did the generator that wrote this file end it with a newline?

    Five of the eleven manifests do not.  Re-serialising would silently
    add one, which is a second edit nobody asked for, so the original
    convention is read and restored per file."""
    fh = open(path, "rb")
    raw = fh.read()
    fh.close()
    if not raw:
        return False
    if raw[-1:] == b"\n":
        return True
    return False


def edit_one(path, dry_run):
    before = os.path.getsize(path)
    newline = had_trailing_newline(path)
    fh = open(path)
    doc = json.load(fh)
    fh.close()

    name = os.path.basename(path)

    meta = doc.get("meta")
    if not isinstance(meta, dict):
        log("REFUSE %-32s no top-level `meta` object to declare on"
            % name)
        return 1

    if already_declared(doc):
        log("skip   %-32s already declares role %r" % (name, ROLE_VALUE))
        return 0

    doc["meta"] = with_role_first(meta)

    if dry_run:
        log("would  %-32s add meta.%s = %r" % (name, ROLE_FIELD,
                                               ROLE_VALUE))
        return 0

    fh = open(path, "w")
    json.dump(doc, fh, indent=1)
    if newline:
        fh.write("\n")
    fh.close()

    after = os.path.getsize(path)
    grew = after - before
    log("edit   %-32s +meta.%s   %d -> %d bytes (%+d)"
        % (name, ROLE_FIELD, before, after, grew))
    return 0


def main():
    dry_run = False
    for a in sys.argv[1:]:
        if a == "--dry-run":
            dry_run = True

    paths = manifest_paths()
    log("manifests found         %d" % len(paths))
    log("declaration             meta.%s = %r" % (ROLE_FIELD, ROLE_VALUE))
    log("")

    worst = 0
    for path in paths:
        rc = edit_one(path, dry_run)
        if rc > worst:
            worst = rc

    log("")
    log("done; worst return code %d" % worst)
    return worst


if __name__ == "__main__":
    sys.exit(main())
