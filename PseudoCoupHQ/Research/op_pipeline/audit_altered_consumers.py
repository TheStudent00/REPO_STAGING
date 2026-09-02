#!/usr/bin/env python3
"""audit_altered_consumers.py -- which artifacts on disk carry the
altered text.

Input: `audit_altered_testimony.json` (written by
`audit_altered_testimony.py`).  Its ALTERED findings hold the exact
stored strings.  This program takes the DISTINCT stored strings and
searches the whole PseudoCoupHQ tree for each of them as a fixed
substring, so a consumer is found by carrying the text, not by being
guessed from an import graph.  A file that merely READS
`op_units_*.json` at run time is not a carrier; a file that has the
altered words written into it is.

The stores the audit read are reported separately from the other
carriers, because those stores are the origin, not a consumer.

Output: `audit_altered_consumers.json` and a printed table.
"""

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))


def main():
    doc = json.load(open(os.path.join(HERE, "audit_altered_testimony.json")))
    alt = [f for f in doc["findings"] if f["verdict"] == "ALTERED"]
    origins = sorted({os.path.basename(f["file"]) for f in alt})
    strings = sorted({f["stored"] for f in alt})
    print("ALTERED findings: %d ; distinct stored strings: %d"
          % (len(alt), len(strings)))

    pfile = os.path.join(HERE, "_altered_patterns.tmp")
    fh = open(pfile, "w")
    fh.write("\n".join(strings) + "\n")
    fh.close()

    cmd = ["grep", "-rlF", "-f", pfile, "--binary-files=without-match", ROOT]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    hits = [p for p in proc.stdout.splitlines()
            if p.strip() and os.path.abspath(p) != os.path.abspath(pfile)]
    os.remove(pfile)

    carriers = []
    for p in hits:
        rel = os.path.relpath(p, ROOT)
        base = os.path.basename(p)
        kind = "origin store" if base in origins else "carrier"
        if base in ("audit_altered_testimony.json",
                    "audit_altered_consumers.json",
                    "audit_altered_testimony.md"):
            kind = "this audit's own output"
        if base in ("test_verbatim_roundtrip.py", "verbatim_diag.py"):
            kind = "the fix's own test, quotes the defect on purpose"
        carriers.append(dict(path=rel, kind=kind,
                             bytes=os.path.getsize(p)))
    carriers.sort(key=lambda r: (r["kind"], r["path"]))

    out = dict(root=ROOT, altered_findings=len(alt),
               distinct_strings=len(strings),
               origin_stores=origins, carriers=carriers,
               grep_command=" ".join(cmd[:5]) + " <patterns> " + ROOT,
               grep_returncode=proc.returncode)
    jpath = os.path.join(HERE, "audit_altered_consumers.json")
    fh = open(jpath, "w")
    json.dump(out, fh, indent=1)
    fh.close()

    for r in carriers:
        print("%-26s %9d  %s" % (r["kind"], r["bytes"], r["path"]))
    print("wrote %s" % jpath)
    return 0


if __name__ == "__main__":
    sys.exit(main())
