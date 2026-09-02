#!/usr/bin/env python3
"""guard_nesting_test.py -- prove the provenance exemption did not
open a hole.

the owner's ruling exempts generator provenance from the spelling guard.
The exemption is worth nothing if it can be worn by a matching or
grouping artifact, so this program builds the two ways that could be
attempted and checks that the guard refuses both.

  case A  NESTED.  A matching artifact (top-level `rows`, each row
          holding `members`) with a whole manifest -- declaration and
          all -- carried inside one of its rows.  The guard must FAIL:
          the exemption is read at the ROOT of the checked file only,
          so a nested manifest is walked exactly as before.

  case B  WORN.  A matching artifact that stamps the declaration on
          ITSELF, at its own top level, while still carrying `rows`.
          The guard must FAIL, naming the refusal.

  case C  the control.  A real manifest, alone, at the root.  The
          guard must PASS as exempt.

Nothing is written outside a temporary directory, and the real
artifacts are only read.

usage:
  guard_nesting_test.py
"""

import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import check_no_spelling_keys as G                            # noqa: E402


def log(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def small_manifest():
    """a real manifest, cut down to a handful of probes so the test
    output stays readable.  The declaration is kept."""
    path = os.path.join(HERE, "probe_manifest_asg_go.json")
    doc = json.load(open(path))
    probes = doc["probes"]
    keys = sorted(probes, key=str)[:3]
    small = {}
    for k in keys:
        small[k] = probes[k]
    out = {}
    out["meta"] = doc["meta"]
    out["count"] = len(small)
    out["probes"] = small
    return out


def case_nested(manifest):
    """a matching artifact carrying a manifest inside one of its
    rows."""
    row = {}
    row["class_id"] = 1
    row["members"] = [{"lang": "go", "n": 0, "operator": "*="}]
    row["provenance"] = manifest
    doc = {}
    doc["shape"] = "a matching artifact with a manifest nested in a row"
    doc["rows"] = [row]
    return doc


def case_worn(manifest):
    """a matching artifact wearing the declaration itself."""
    doc = {}
    doc["meta"] = manifest["meta"]
    doc["shape"] = "a matching artifact wearing the provenance role"
    doc["rows"] = [{"class_id": 1,
                    "members": [{"lang": "go", "n": 0,
                                 "operator": "*="}]}]
    return doc


def write(tmp, name, doc):
    path = os.path.join(tmp, name)
    fh = open(path, "w")
    json.dump(doc, fh, indent=1)
    fh.close()
    return path


def main():
    toks = G.inventory()
    log("operator inventory: %d tokens" % len(toks))
    log("")

    manifest = small_manifest()
    if not G.declares_provenance_role(manifest):
        log("REFUSE: the manifest under test does not declare the "
            "provenance role; run manifest_role_lane.py first")
        return 2

    tmp = tempfile.mkdtemp(prefix="guard_nesting_")
    failures = 0
    try:
        cases = []
        cases.append(("A nested", "nested_matching.json",
                      case_nested(manifest), 1))
        cases.append(("B worn", "worn_matching.json",
                      case_worn(manifest), 1))
        cases.append(("C control", "lone_manifest.json",
                      manifest, 0))

        for label, name, doc, want in cases:
            path = write(tmp, name, doc)
            log("-- case %s (expect return %d)" % (label, want))
            got = G.check(path, toks)
            if got != want:
                log("   !! WRONG: the guard returned %d, wanted %d"
                    % (got, want))
                failures = failures + 1
            log("")
    finally:
        shutil.rmtree(tmp)

    if failures:
        log("FAIL: %d case(s) came out wrong" % failures)
        return 1
    log("PASS: the exemption is root-only, and a matching artifact "
        "cannot wear it")
    return 0


if __name__ == "__main__":
    sys.exit(main())
