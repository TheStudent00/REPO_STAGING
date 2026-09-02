#!/usr/bin/env python3
"""interp_union_guard2.py -- the spelling guard on TASK 34's artifacts,
WITHOUT the provenance exemption.

`check_no_spelling_keys.py` grants a generator-provenance exemption to
a document whose top-level meta declares that role and which carries
no top-level grouping field.  TASK 34's artifacts are grouping-shaped
and matching-shaped by construction -- `interp_table2.json` has rows
with members, `interp_join2.json` pairs an interpreter class with a
compiled class on every row, `union_table2.json` groups classes into
components, and `interp_canon35.json` carries the per-unit records
those three are built from.

The brief's requirement is guards on everything, matching-shaped
WITHOUT EXEMPTION.  So this program calls the checker's OWN
`inventory` and `walk` directly on every artifact, exemption bypassed,
and refuses on any finding.  Nothing about the checker is
reimplemented here -- the token list and the walk are imported.

usage:
  /tmp/reconnect_venv/bin/python3 interp_union_guard2.py
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import check_no_spelling_keys as CHECK  # noqa: E402

ARTIFACTS = [
    "interp_canon35.json",
    "interp_table2.json",
    "interp_join2.json",
    "union_table2.json",
    "interp_zero_regression2.json",
]


def main(argv):
    tokens = CHECK.inventory()
    failures = 0
    for name in ARTIFACTS:
        path = os.path.join(HERE, name)
        handle = open(path)
        doc = json.load(handle)
        handle.close()
        findings = []
        CHECK.walk(doc, tokens, "$", findings)
        if findings:
            failures = failures + 1
            print("FAIL %s -- %d spelling-keyed place(s), exemption "
                  "bypassed" % (name, len(findings)))
            for finding in findings[:10]:
                print("   %s" % (finding,))
            continue
        print("PASS %s -- no operator token in any key, grouping, "
              "pairing or row structure (checked IN FULL, the "
              "generator-provenance exemption deliberately bypassed)"
              % name)
    if failures:
        print("REFUSED: %d artifact(s) failed the guard" % failures)
        return 1
    print("ALL %d ARTIFACTS PASS THE GUARD WITHOUT EXEMPTION"
          % len(ARTIFACTS))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
