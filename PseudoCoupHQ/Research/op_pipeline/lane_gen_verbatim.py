#!/usr/bin/env python3
"""lane_gen_verbatim.py -- lane scripts that store compiler words verbatim.

WHAT THIS IS
------------
A WRAPPER around `lane_gen.py`.  `lane_gen.py` is not edited and not
imported-and-monkey-patched at runtime for its callers: this program
imports it, asks it for the lane text it would have written, and then
applies a NAMED, CHECKED set of text edits to the embedded driver so
that the driver ESCAPES the delimiters instead of SUBSTITUTING for
them.  Every edit is asserted to have applied the expected number of
times; if any edit does not apply, this program refuses to write a
lane rather than emit a half-fixed driver.

WHY A TEXT EDIT AND NOT A CALL
------------------------------
The driver does not run here.  It is a Python program serialised into
the lane shell script and executed inside Airlock, where this
directory does not exist.  The fix must therefore travel INSIDE the
lane text.  `verbatim_diag.py` holds the codec of record; the codec
body is copied into the driver so the two cannot drift (the copy is
taken from `verbatim_diag` at generation time, not retyped).

THE EDITS
---------
 1. `clean()` loses its two substitutions (`|`->`/`, `;`->`,`).
 2. `firstline()` loses its four `.replace("|", "/")` calls.
 3. every field written into the pipe-delimited record is passed
    through `esc()`; list fields are escaped PER ITEM so the `;`
    sub-separator still separates.
 4. the output file opens with the marker line `#verbatim-escape v1`
    so a reader can tell an escaped file from a legacy one.

Read back with `fold_verbatim.py`, which decodes.  A legacy lane file
(no marker) is NOT decoded -- decoding it would alter a backslash the
compiler really emitted, which is the same class of mistake as the
defect this repairs.

usage: same arguments as lane_gen.py, plus lanes are named
       `<base>_vb` so a verbatim lane never overwrites a legacy one.

  lane_gen_verbatim.py rust
  lane_gen_verbatim.py c cpp go rust swift --shard 200
  lane_gen_verbatim.py rust --check     (edit-application check only)
"""

import argparse
import inspect
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import lane_gen                                            # noqa: E402
import verbatim_diag                                       # noqa: E402


ESC_BLOCK = (
    "\n\n# --- verbatim delimiter codec, copied from verbatim_diag.py ---\n"
    + inspect.getsource(verbatim_diag.encode).replace("def encode(",
                                                      "def esc(")
    + "\n_ENC = " + repr(verbatim_diag._ENC) + "\n"
    + "MARKER = " + repr(verbatim_diag.MARKER) + "\n"
    + "out.write(MARKER + '\\n')\n"
)

EDITS = [
    # (what, old, new, expected occurrences)
    ("clean(): drop the two substitutions",
     '    text = text.replace("|", "/")\n    text = text.replace(";", ",")\n',
     '',
     1),
    ("firstline(): drop the substitution, keep the truncation",
     '.replace("|", "/")[:200]',
     '[:200]',
     4),
    ("REFUSED field escaped",
     'out.write("op_%d|REFUSED|%s\\n" % (n, firstline(err)))',
     'out.write("op_%d|REFUSED|%s\\n" % (n, esc(firstline(err))))',
     1),
    ("ANCHOR BUILDFAIL field escaped",
     'out.write("op_%d|ANCHOR|BUILDFAIL|%s\\n" % (n, firstline(aerr)))',
     'out.write("op_%d|ANCHOR|BUILDFAIL|%s\\n" % (n, esc(firstline(aerr))))',
     1),
    ("ANCHOR NODWARF field escaped",
     'out.write("op_%d|ANCHOR|NODWARF|%s\\n" % (n, why))',
     'out.write("op_%d|ANCHOR|NODWARF|%s\\n" % (n, esc(why)))',
     1),
    ("DWARF rows escaped per item, so `;` still separates",
     'joined = ";".join("%s=%s" % (a, b) for a, b in rows)',
     'joined = ";".join("%s=%s" % (esc(a), esc(b)) for a, b in rows)',
     1),
    ("NOSYM field escaped",
     'out.write("op_%d|%s|NOSYM|symbol %s absent, %d near matches\\n"\n'
     '                  % (n, build, sym, near))',
     'out.write("op_%d|%s|NOSYM|%s\\n"\n'
     '                  % (n, build, esc("symbol %s absent, %d near matches"\n'
     '                                   % (sym, near))))',
     1),
    ("OK row: bytes and mnemonics escaped per item",
     'out.write("op_%d|%s|OK|%s|%s\\n"\n'
     '              % (n, build, " ".join(raw), ";".join(mn)))',
     'out.write("op_%d|%s|OK|%s|%s\\n"\n'
     '              % (n, build, " ".join(esc(x) for x in raw),\n'
     '                 ";".join(esc(x) for x in mn)))',
     1),
]

ANCHOR = 'WORK = os.path.join(ROOT, "u")'


def make_driver():
    """the driver text with every edit applied, or an exception."""
    text = lane_gen.DRIVER
    report = []
    for what, old, new, want in EDITS:
        got = text.count(old)
        if got != want:
            raise AssertionError(
                "edit did not apply as expected: %s -- found %d, wanted %d"
                % (what, got, want))
        text = text.replace(old, new)
        report.append((what, got))
    if text.count(ANCHOR) != 1:
        raise AssertionError("codec insertion anchor not found exactly once")
    text = text.replace(ANCHOR, ANCHOR + ESC_BLOCK, 1)
    # the fix must be complete: no substitution may survive anywhere.
    for banned in ('replace("|", "/")', 'replace(";", ",")'):
        if banned in text:
            raise AssertionError("substitution survived the edits: %s"
                                 % banned)
    return text, report


def lane_verbatim(lang, name, probes, outname):
    saved = lane_gen.DRIVER
    driver, _ = make_driver()
    lane_gen.DRIVER = driver
    try:
        return lane_gen.lane(lang, name, probes, outname)
    finally:
        lane_gen.DRIVER = saved


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("langs", nargs="+")
    ap.add_argument("--smoke", type=int, default=0)
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--name", default=None)
    ap.add_argument("--check", action="store_true",
                    help="apply the edits and report; write no lane")
    args = ap.parse_args(argv[1:])

    driver, report = make_driver()
    print("driver edits applied:")
    for what, got in report:
        print("  %-52s x%d" % (what, got))
    print("  driver bytes: %d -> %d" % (len(lane_gen.DRIVER), len(driver)))
    if args.check:
        return 0

    lanedir = os.path.join(HERE, "lanes")
    if not os.path.isdir(lanedir):
        os.makedirs(lanedir)
    for lang in args.langs:
        if lang not in lane_gen.LANGS:
            print("skip %s -- no lane template" % lang)
            continue
        probes = lane_gen.load(lang)
        if args.smoke:
            probes = probes[:args.smoke]
        base = args.name or ("op_%s" % lang)
        groups = []
        if args.shard:
            for k in range(0, len(probes), args.shard):
                groups.append(probes[k:k + args.shard])
        else:
            groups.append(probes)
        for idx, grp in enumerate(groups):
            name = "%s_vb" % base
            if len(groups) > 1:
                name = "%s_vb_s%d" % (base, idx)
            text = lane_verbatim(lang, name, grp, name)
            path = os.path.join(lanedir, "%s.sh" % name)
            fh = open(path, "w")
            fh.write(text)
            fh.close()
            os.chmod(path, 0o755)
            print("%-6s %-20s %4d probes  %7d bytes  %s"
                  % (lang, name, len(grp), len(text), path))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
