#!/usr/bin/env python3
"""pane23_manifest_regex_check.py -- TEST RIG ONLY, not part of the page.

The live page must know the DECLARED TYPES of every probe over the whole
population, and the two regenerated manifests are 37 MB and 50 MB because
each probe carries its full source text.  dashboard_pane23.js therefore
does not JSON.parse them in the browser: it runs one regular expression
over the text and keeps only the three declared type fields.

This script runs THE SAME regular expression in python and compares its
result, probe for probe, with json.load of the same file.  If the two
disagree anywhere the page's shortcut is wrong.
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANGS = ["c", "cpp", "go", "rust", "swift"]

# the same expression, character for character, as SIG_RE in
# dashboard_pane23.js
PAT = re.compile(
    r'"n"\s*:\s*(\d+)\s*,'
    r'[\s\S]*?"lhs_type"\s*:\s*(null|"(?:[^"\\]|\\.)*")'
    r'[\s\S]*?"rhs_type"\s*:\s*(null|"(?:[^"\\]|\\.)*")'
    r'[\s\S]*?"result_type"\s*:\s*(null|"(?:[^"\\]|\\.)*")')

SPAN_CEILING = 2000


def unq(s):
    if s == "null":
        return None
    return json.loads(s)


def main():
    worst = 0
    for lang in LANGS:
        for stem in ("probe_manifest_", "probe_manifest2_"):
            name = stem + lang + ".json"
            path = os.path.join(HERE, name)
            if not os.path.exists(path):
                continue
            text = open(path).read()
            got = {}
            over = 0
            for m in PAT.finditer(text):
                if len(m.group(0)) > SPAN_CEILING:
                    over += 1
                    continue
                got[m.group(1)] = (unq(m.group(2)), unq(m.group(3)),
                                   unq(m.group(4)))
            doc = json.loads(text)
            probes = doc.get("probes") or {}
            if isinstance(probes, list):
                probes = {str(p.get("n")): p for p in probes}
            want = {str(k): (p.get("lhs_type"), p.get("rhs_type"),
                             p.get("result_type"))
                    for k, p in probes.items()}
            same = got == want
            if not same:
                worst = 1
                missing = set(want) - set(got)
                extra = set(got) - set(want)
                diff = [k for k in set(want) & set(got) if want[k] != got[k]]
                print("FAIL %-26s parsed %d, expected %d; missing %d, "
                      "extra %d, differing %d"
                      % (name, len(got), len(want), len(missing), len(extra),
                         len(diff)))
                for k in list(diff)[:3]:
                    print("        probe %s: regex %r  json %r"
                          % (k, got[k], want[k]))
            else:
                print("PASS %-26s %6d probes, identical to json.load "
                      "(%d spans over the %d-character ceiling, skipped)"
                      % (name, len(got), over, SPAN_CEILING))
    return worst


if __name__ == "__main__":
    sys.exit(main())
