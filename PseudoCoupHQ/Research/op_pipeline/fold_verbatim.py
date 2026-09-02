#!/usr/bin/env python3
"""fold_verbatim.py -- the reader half of the verbatim path.

`fold.py` reads a lane file by splitting each line on `|`.  A lane
written by `lane_gen_verbatim.py` carries ESCAPED fields, so the split
is still correct field-by-field, but each field must be DECODED before
it is stored.  This wrapper does exactly that and nothing else:

  * it calls `fold.fold(lang, outdir)` -- fold.py is not edited --
  * then walks the folded document and decodes the fields the driver
    escaped: `refused`, the per-slot free-text fields (`nosym`,
    `buildfail`, `nodwarf`), the mnemonic list, and the DWARF row
    names and locations,
  * and writes `op_units_<lang>_verbatim.json` beside the original.
    The original `op_units_<lang>.json` fold.py wrote is left alone;
    this program creates a new file and modifies nothing.

REFUSAL RULE.  Decoding is applied ONLY when every lane file that fed
the fold announced itself with `#verbatim-escape v1` on its first
line.  A legacy lane file is refused, by name, with a nonzero exit --
because decoding a legacy line would rewrite a backslash the compiler
really emitted, which is the same class of mistake as the defect this
line repairs.

usage:
  fold_verbatim.py rust
  fold_verbatim.py c cpp go rust swift --out /path/to/Airlock/agent/out
"""

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import fold                                                # noqa: E402
import verbatim_diag as V                                  # noqa: E402


def marked(path):
    fh = open(path)
    first = fh.readline().rstrip("\n")
    fh.close()
    return first == V.MARKER


def decode_doc(doc):
    """decode every field the driver escaped.  Returns the count decoded."""
    n = 0

    def dec(s):
        nonlocal n
        if isinstance(s, str):
            out = V.decode(s)
            if out != s:
                n += 1
            return out
        return s

    for rec in doc.get("probes", {}).values():
        if "refused" in rec:
            rec["refused"] = dec(rec["refused"])
        for slot in ("anchor", "ship"):
            side = rec.get(slot)
            if not isinstance(side, dict):
                continue
            for f in ("nosym", "buildfail", "nodwarf"):
                if f in side:
                    side[f] = dec(side[f])
            if isinstance(side.get("mnem"), list):
                side["mnem"] = [dec(x) for x in side["mnem"]]
            if isinstance(side.get("bytes"), list):
                side["bytes"] = [dec(x) for x in side["bytes"]]
            for row in side.get("dwarf", []) or []:
                if isinstance(row, dict):
                    row["name"] = dec(row.get("name"))
                    row["location"] = dec(row.get("location"))
    return n


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("langs", nargs="+")
    ap.add_argument("--out", default=fold.OUTDIR)
    args = ap.parse_args(argv[1:])

    bad = 0
    for lang in args.langs:
        paths = fold.lane_files(args.out, lang)
        if not paths:
            print("%-6s REFUSED: no lane file found under %s"
                  % (lang, args.out))
            bad += 1
            continue
        legacy = [p for p in paths if not marked(p)]
        if legacy:
            print("%-6s REFUSED: these lane files carry no %r marker, so "
                  "they are legacy captures and must not be decoded: %s"
                  % (lang, V.MARKER, ", ".join(legacy)))
            bad += 1
            continue
        tally, path = fold.fold(lang, args.out)
        doc = json.load(open(path))
        n = decode_doc(doc)
        vpath = os.path.join(HERE, "op_units_%s_verbatim.json" % lang)
        fh = open(vpath, "w")
        json.dump(doc, fh, indent=1)
        fh.close()
        print("%-6s folded %s ; %d fields decoded ; wrote %s"
              % (lang, os.path.basename(path), n, vpath))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
