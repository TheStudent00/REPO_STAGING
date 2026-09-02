#!/usr/bin/env python3
"""result_types_asg.py -- machine-fact RESULT TYPES for the asg units.

Same evidence class and same method as result_types.py (the tool's
own testimony: DW_AT_type on the `op_N` subprogram of a `-g` build,
read back with readelf), applied to the compound-assignment probes
(op_units_asg_c.json / op_units_asg_cpp.json) instead of the plain
operator probes.

Ruling followed: names in result_types_c.json etc. (int32_t, bool,
...) are the GENERATOR's spelling, not a machine fact, and do not
let 600 of the 749 asg units join classes across languages.  This
script re-derives the result type from the base-type DIE's own
DW_AT_ENCODING and DW_AT_BYTE_SIZE (after resolving typedefs,
const/volatile, and (for c++) references), and keys the shared
name on that pair alone:

    signed  ,4 -> i32      signed  ,8 -> i64
    unsigned,4 -> u32      unsigned,8 -> u64
    boolean ,1 -> bool
    float   ,4 -> f32      float   ,8 -> f64

The type NAME the debugger prints (e.g. "int", "int32_t") is kept
only as a display label alongside the machine key -- never as part
of it (spelling ban).
"""

import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

PAIRS = [
    ("c", "probe_manifest_asg_c.json", "op_units_asg_c.json", "c"),
    ("cpp", "probe_manifest_asg_cpp.json", "op_units_asg_cpp.json", "c++"),
]

DIE = re.compile(r"^\s*<(\d+)><([0-9a-f]+)>:\s+Abbrev Number:\s+\d+\s+"
                 r"\((DW_TAG_\w+)\)")
ATTR = re.compile(r"^\s*<[0-9a-f]+>\s+(DW_AT_\w+)\s*:\s*(.*)$")
REF = re.compile(r"<0x([0-9a-f]+)>")

ENCODING_NAME = {
    "1": "address",
    "2": "boolean",
    "4": "float",
    "5": "signed",
    "6": "signed char",
    "7": "unsigned",
    "8": "unsigned char",
}


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


def accepted(indir, unitsfile):
    doc = json.load(open(os.path.join(indir, unitsfile)))
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
    current = None
    for line in proc.stdout.splitlines():
        hit = DIE.match(line)
        if hit:
            offset = hit.group(2)
            current = {"tag": hit.group(3), "offset": offset}
            dies[offset] = current
            continue
        if current is None:
            continue
        hit = ATTR.match(line)
        if not hit:
            continue
        current[hit.group(1)] = hit.group(2).strip()
    return dies


def type_ref(die):
    nxt = die.get("DW_AT_type")
    if nxt is None:
        return None
    hit = REF.search(nxt)
    if not hit:
        return None
    return hit.group(1)


def resolve_base(dies, offset, depth):
    """follow typedef/const/volatile/reference down to the base type
    DIE itself (not a name) so encoding+width can be read off it."""
    if depth > 24:
        return None
    die = dies.get(offset)
    if die is None:
        return None
    tag = die["tag"]
    if tag == "DW_TAG_base_type":
        return die
    if tag in ("DW_TAG_typedef", "DW_TAG_const_type",
               "DW_TAG_volatile_type", "DW_TAG_reference_type",
               "DW_TAG_rvalue_reference_type"):
        target = type_ref(die)
        if target is None:
            return None
        return resolve_base(dies, target, depth + 1)
    return None


def machine_key(base_die):
    if base_die is None:
        return None
    enc = base_die.get("DW_AT_encoding", "")
    hit = re.match(r"(\d+)", enc)
    if not hit:
        return None
    enc_num = hit.group(1)
    size = base_die.get("DW_AT_byte_size")
    if size is None:
        return None
    size = size.strip()
    enc_name = ENCODING_NAME.get(enc_num, enc_num)
    if enc_name == "boolean" and size == "1":
        return "bool"
    if enc_name == "float" and size == "4":
        return "f32"
    if enc_name == "float" and size == "8":
        return "f64"
    if enc_name in ("signed", "signed char") and size == "4":
        return "i32"
    if enc_name in ("signed", "signed char") and size == "8":
        return "i64"
    if enc_name in ("unsigned", "unsigned char") and size == "4":
        return "u32"
    if enc_name in ("unsigned", "unsigned char") and size == "8":
        return "u64"
    return "unresolved: encoding=%s size=%s" % (enc_name, size)


def display_name(dies, offset, depth):
    if depth > 24:
        return "unresolved: type chain too long"
    die = dies.get(offset)
    if die is None:
        return "unresolved: no DIE at this offset"
    tag = die["tag"]
    name = die.get("DW_AT_name")
    if name is not None:
        name = name.split(":")[-1].strip()
    target = type_ref(die)
    if tag == "DW_TAG_base_type":
        return name
    if tag in ("DW_TAG_typedef", "DW_TAG_const_type",
               "DW_TAG_volatile_type", "DW_TAG_reference_type",
               "DW_TAG_rvalue_reference_type"):
        if target is None:
            return name if name else "void"
        return display_name(dies, target, depth + 1)
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
        ref = type_ref(die)
        if ref is None:
            out[name] = ("void", None)
            continue
        base = resolve_base(dies, ref, 0)
        key = machine_key(base)
        label = display_name(dies, ref, 0)
        out[name] = (key, label)
    return out


def run_language(lang, manifest, unitsfile, dialect, indir, outdir, cc,
                 cxx, dump, work):
    rows = sources(indir, manifest)
    keep = accepted(indir, unitsfile)
    text, used = build_one_unit(rows, keep)
    log("%s: %d accepted asg probes to ask the compiler about" %
        (lang, len(used)))
    ext = ".c"
    tool = cc
    if dialect == "c++":
        ext = ".cpp"
        tool = cxx
    spath = os.path.join(work, "result_types_asg_%s%s" % (lang, ext))
    open(spath, "w").write(text)
    opath = os.path.join(work, "result_types_asg_%s.o" % lang)
    cmd = [tool, "-g", "-O0", "-c", spath, "-o", opath]
    if dialect == "c++":
        cmd = [tool, "-std=c++20", "-g", "-O0", "-c", spath, "-o", opath]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        log("!! the compile of the concatenated asg probes failed")
        log(proc.stderr[:2000])
        raise RuntimeError("asg result-type recovery refused: the "
                           "concatenated probe unit did not compile")
    dies = read_dies(opath, dump)
    found = subprogram_results(dies)
    log("%s: the debug information names %d subprograms" % (lang,
                                                            len(found)))
    out = {}
    out["language"] = lang
    out["ground"] = ("the tool's own testimony: DW_AT_type on the "
                      "`op_N` subprogram of a `-g` build of the "
                      "recorded asg probe source, typedefs/"
                      "const/volatile/reference followed to a base "
                      "type DIE, keyed on that DIE's own "
                      "DW_AT_encoding and DW_AT_byte_size (signed/4 "
                      "-> i32, signed/8 -> i64, unsigned/4 -> u32, "
                      "unsigned/8 -> u64, boolean/1 -> bool, "
                      "float/4 -> f32, float/8 -> f64); the "
                      "generator's type name is kept only as a "
                      "display label, never as part of the key")
    out["compiler"] = " ".join(cmd[:1])
    out["probes_asked"] = len(used)
    rowsout = {}
    missing = []
    unresolved = []
    for n in used:
        key = "op_%s" % n
        pair = found.get(key)
        if pair is None:
            missing.append(n)
            continue
        mkey, label = pair
        if mkey is None or (isinstance(mkey, str) and
                             mkey.startswith("unresolved")):
            unresolved.append({"probe": n, "detail": mkey,
                                "display_label": label})
            continue
        rowsout[n] = {"result_type_machine": mkey,
                      "result_type_label": label}
    out["result_types"] = rowsout
    out["probes_the_debug_information_did_not_name"] = missing
    out["probes_with_unresolved_machine_key"] = unresolved
    path = os.path.join(outdir, "result_types_asg_%s.json" % lang)
    fh = open(path, "w")
    json.dump(out, fh, indent=1)
    fh.close()
    log("wrote %s (%d recovered, %d not named, %d unresolved)" %
        (path, len(rowsout), len(missing), len(unresolved)))
    return out


def main(argv):
    indir = HERE
    outdir = HERE
    work = HERE
    cc = "gcc"
    cxx = "g++"
    dump = "readelf"
    i = 1
    while i < len(argv):
        if argv[i] == "--cc":
            cc = argv[i + 1]
            i += 2
            continue
        if argv[i] == "--cxx":
            cxx = argv[i + 1]
            i += 2
            continue
        print(__doc__)
        return 2
    for lang, manifest, unitsfile, dialect in PAIRS:
        run_language(lang, manifest, unitsfile, dialect, indir, outdir,
                     cc, cxx, dump, work)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
