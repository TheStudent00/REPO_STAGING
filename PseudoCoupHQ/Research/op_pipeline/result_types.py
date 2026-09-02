#!/usr/bin/env python3
"""result_types.py -- recover the RESULT TYPE of every c and c++ probe.

Why this program exists
-----------------------
Ruling 3 of 2026-08-25 puts the result type into the class key.  Four of
the five languages recorded it: `op_units_go/rust/swift.json` carry
`meta.result_type` on every probe.  c and c++ do NOT: their probes were
generated with the return type written as `__typeof__(expr)` (c) and
`auto` (c++), under `result_rule` "compiler_states_it_typeof" /
"compiler_states_it_auto" -- the compiler was asked to state the type,
and the answer was never read back.  `meta.result_type` is null on all
750 c probes and all 1002 c++ probes.

So this program asks the compiler again, and reads the answer from the
debug information it emits about its own output: for each accepted
probe it compiles the recorded source with `-g` and reads DW_AT_type off
the `op_N` subprogram, following typedefs and qualifiers down to a base
type name.  Evidence class: THE TOOL'S OWN TESTIMONY (a debug table the
compiler wrote about the function it just built), the same class the
argument-location table in step 4 sits in.

All the accepted probes of one language are compiled as ONE translation
unit: each recorded source is a standalone file whose includes are
guarded and whose symbol is unique, so concatenating them changes
nothing and costs one compile instead of hundreds.

usage:
  result_types.py [--in DIR] [--out DIR] [--cc clang] [--cxx clang++]
"""

import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

PAIRS = [("c", "probe_manifest_c.json", "c"),
         ("cpp", "probe_manifest_cpp.json", "c++"),
         ("rust", "probe_manifest_rust.json", "rust")]

DIE = re.compile(r"^\s*<(\d+)><([0-9a-f]+)>:\s+Abbrev Number:\s+\d+\s+"
                 r"\((DW_TAG_\w+)\)")

ATTR = re.compile(r"^\s*<[0-9a-f]+>\s+(DW_AT_\w+)\s*:\s*(.*)$")

REF = re.compile(r"<0x([0-9a-f]+)>")


def log(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def sources(indir, manifest):
    doc = json.load(open(os.path.join(indir, manifest)))
    out = []
    for n, p in sorted(doc["probes"].items(), key=lambda x: int(x[0])):
        text = p.get("source")
        if not text:
            continue
        out.append((n, p, text))
    return out


def accepted(indir, lang):
    doc = json.load(open(os.path.join(indir, "op_units_%s.json" % lang)))
    out = set()
    for n, p in doc["probes"].items():
        if p.get("refused"):
            continue
        out.add(n)
    return out


def build_one_unit(rows, keep):
    parts = []
    used = []
    for n, p, text in rows:
        if n not in keep:
            continue
        parts.append(text)
        used.append(n)
    return "\n".join(parts), used


def read_dies(path, dump):
    cmd = [dump, "--debug-dump=info", path]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError("reading the debug information failed: %s"
                           % proc.stderr[:400])
    dies = {}
    order = []
    current = None
    for line in proc.stdout.splitlines():
        hit = DIE.match(line)
        if hit:
            offset = hit.group(2)
            current = {}
            current["tag"] = hit.group(3)
            current["offset"] = offset
            dies[offset] = current
            order.append(offset)
            continue
        if current is None:
            continue
        hit = ATTR.match(line)
        if not hit:
            continue
        name = hit.group(1)
        value = hit.group(2).strip()
        current[name] = value
    return dies


def resolve(dies, offset, depth):
    """follow a DW_AT_type reference to a printable type name."""
    if depth > 24:
        return "unresolved: the type chain is longer than this program "\
               "follows"
    die = dies.get(offset)
    if die is None:
        return "unresolved: the debug information has no entry at this "\
               "offset"
    tag = die["tag"]
    name = die.get("DW_AT_name")
    if name is not None:
        name = name.split(":")[-1].strip()
    nxt = die.get("DW_AT_type")
    target = None
    if nxt is not None:
        hit = REF.search(nxt)
        if hit:
            target = hit.group(1)
    if tag == "DW_TAG_base_type":
        return name
    if tag == "DW_TAG_typedef":
        if target is None:
            return name
        inner = resolve(dies, target, depth + 1)
        return inner
    if tag == "DW_TAG_pointer_type":
        if target is None:
            return "pointer to void"
        return "pointer to " + resolve(dies, target, depth + 1)
    if tag in ("DW_TAG_const_type", "DW_TAG_volatile_type"):
        if target is None:
            return "void"
        return resolve(dies, target, depth + 1)
    if tag == "DW_TAG_enumeration_type":
        return "enum " + str(name)
    if tag in ("DW_TAG_structure_type", "DW_TAG_class_type"):
        return "struct " + str(name)
    if tag == "DW_TAG_reference_type":
        if target is None:
            return "reference to void"
        return "reference to " + resolve(dies, target, depth + 1)
    if name is not None:
        return name
    return "unresolved: " + tag


def subprogram_results(dies):
    out = {}
    for offset in dies:
        die = dies[offset]
        if die["tag"] != "DW_TAG_subprogram":
            continue
        name = die.get("DW_AT_name")
        if name is None:
            continue
        name = name.split(":")[-1].strip()
        if not name.startswith("op_"):
            continue
        ref = die.get("DW_AT_type")
        if ref is None:
            out[name] = "void"
            continue
        hit = REF.search(ref)
        if not hit:
            out[name] = "unresolved: DW_AT_type is not a reference"
            continue
        out[name] = resolve(dies, hit.group(1), 0)
    return out


def run_language(lang, manifest, dialect, indir, outdir, cc, cxx, dump,
                 work):
    rows = sources(indir, manifest)
    keep = accepted(indir, lang)
    text, used = build_one_unit(rows, keep)
    log("%s: %d accepted probes to ask the compiler about" % (lang,
                                                              len(used)))
    ext = ".c"
    tool = cc
    if dialect == "c++":
        ext = ".cpp"
        tool = cxx
    if dialect == "rust":
        ext = ".rs"
        tool = "rustc"
    spath = os.path.join(work, "result_types_%s%s" % (lang, ext))
    fh = open(spath, "w")
    fh.write(text)
    fh.close()
    opath = os.path.join(work, "result_types_%s.o" % lang)
    cmd = [tool, "-g", "-O0", "-c", spath, "-o", opath]
    if dialect == "rust":
        # the same build the pipeline's ANCHOR build used, plus debug
        # information: one library crate holding every accepted probe
        cmd = ["rustc", "--crate-type=lib", "--emit=obj",
               "-C", "opt-level=0", "-C", "debuginfo=2",
               "-o", opath, spath]
    if dialect == "c++":
        # the probe set uses the three-way comparison, which is a C++20
        # feature; the recorded corpus was built by a compiler with C++20
        # on, so this asks for the same language the probes were
        # accepted under
        cmd = [tool, "-std=c++20", "-g", "-O0", "-c", spath, "-o", opath]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        log("!! the compile of the concatenated probes failed")
        log(proc.stderr[:2000])
        raise RuntimeError("result-type recovery refused: the "
                           "concatenated probe unit did not compile")
    dies = read_dies(opath, dump)
    found = subprogram_results(dies)
    log("%s: the debug information names %d subprograms" % (lang,
                                                            len(found)))
    out = {}
    out["language"] = lang
    out["ground"] = "the tool's own testimony: DW_AT_type on the "\
                    "`op_N` subprogram of a `-g` build of the recorded "\
                    "probe source, typedefs and qualifiers followed to "\
                    "a base type name"
    out["compiler"] = " ".join(cmd[:1])
    out["probes_asked"] = len(used)
    rowsout = {}
    missing = []
    for n in used:
        key = "op_%s" % n
        value = found.get(key)
        if value is None:
            missing.append(n)
            continue
        rowsout[n] = value
    out["result_types"] = rowsout
    out["probes_the_debug_information_did_not_name"] = missing
    path = os.path.join(outdir, "result_types_%s.json" % lang)
    fh = open(path, "w")
    json.dump(out, fh, indent=1)
    fh.close()
    log("wrote %s (%d recovered, %d not named)" % (path, len(rowsout),
                                                   len(missing)))
    return out


def main(argv):
    indir = HERE
    outdir = HERE
    work = HERE
    cc = "clang"
    cxx = "clang++"
    dump = "readelf"
    i = 1
    while i < len(argv):
        if argv[i] == "--in":
            indir = argv[i + 1]
            i = i + 2
            continue
        if argv[i] == "--out":
            outdir = argv[i + 1]
            i = i + 2
            continue
        if argv[i] == "--work":
            work = argv[i + 1]
            i = i + 2
            continue
        if argv[i] == "--cc":
            cc = argv[i + 1]
            i = i + 2
            continue
        if argv[i] == "--cxx":
            cxx = argv[i + 1]
            i = i + 2
            continue
        print(__doc__)
        return 2
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    for lang, manifest, dialect in PAIRS:
        run_language(lang, manifest, dialect, indir, outdir, cc, cxx,
                     dump, work)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
