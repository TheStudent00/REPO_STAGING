#!/usr/bin/env python3
"""roundtrip.py -- the canonical form is RUNNABLE MACHINE CODE, so check
that it assembles.

Every unit that `canon.py` canonicalised is written out as assembler
text under its own label, all of them in one file; the file is
assembled; the object is disassembled again; and the instructions that
come back are compared with the instructions that went in.  The bytes
the assembler produced are the unit's CANONICAL BYTES, and they are what
level-1 matching compares.

Two facts fall out of the comparison and are both recorded:

  * self-consistency -- the text that comes back out equals the text
    that went in.  A unit where it does not is reported, not hidden.
  * for a unit the rename left alone, the canonical bytes should equal
    the ship bytes the pipeline already recorded.  Where they do not,
    the difference is the assembler's encoding choice, and the unit
    says so.

Units the assembler cannot be handed are skipped by name, never
silently: a branch to a label the extract does not carry, a
rip-relative operand with a relocation note, or an objdump comment.

usage:
  roundtrip.py [--in DIR] [--out DIR] [--work DIR] [--cc clang]
"""

import json
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))

LANGS = ["c", "cpp", "go", "rust", "swift"]

LINE = re.compile(r"^\s*([0-9a-f]+):\s*((?:[0-9a-f]{2} )+)\s*(.*)$")

SYMBOL = re.compile(r"^[0-9a-f]+ <([^>]+)>:")


def log(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def assemblable(lines):
    """can this text be handed to an assembler as it stands?"""
    for line in lines:
        if "<" in line:
            return False, "the text names a branch target the extract "\
                          "does not carry"
        if "!!reloc" in line:
            return False, "the text carries a relocation note"
        if "(%rip)" in line:
            return False, "the text carries a rip-relative operand"
        if "#" in line:
            return False, "the text carries a disassembler comment"
    return True, None


def label_for(lang, n):
    return "u_%s_%s" % (lang, n)


def gather(indir):
    """every canonicalised unit that can be assembled, and every one
    that cannot, with its reason."""
    take = []
    skip = []
    for lang in LANGS:
        path = os.path.join(indir, "canon_units_%s.json" % lang)
        doc = json.load(open(path))
        for n, u in sorted(doc["units"].items(), key=lambda x: int(x[0])):
            if not u.get("canon_ok"):
                continue
            lines = u["canon_mnem"]
            ok, why = assemblable(lines)
            if not ok:
                rec = {}
                rec["lang"] = lang
                rec["n"] = n
                rec["operator"] = u.get("operator")
                rec["reason"] = why
                skip.append(rec)
                continue
            take.append((lang, n, lines, u))
    return take, skip


def write_source(take, path):
    out = []
    out.append("        .text")
    for lang, n, lines, _u in take:
        name = label_for(lang, n)
        out.append("        .globl %s" % name)
        out.append("        .type %s, @function" % name)
        out.append("%s:" % name)
        for line in lines:
            out.append("        %s" % line)
        out.append("        .size %s, .-%s" % (name, name))
    fh = open(path, "w")
    fh.write("\n".join(out) + "\n")
    fh.close()


def disassemble(opath, dump):
    cmd = [dump, "-d", "--no-show-raw-insn", opath]
    del cmd
    cmd = [dump, "-d", opath]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError("the disassembly failed: %s"
                           % proc.stderr[:400])
    out = {}
    current = None
    for line in proc.stdout.splitlines():
        hit = SYMBOL.match(line)
        if hit:
            current = hit.group(1)
            out[current] = {"bytes": [], "mnem": []}
            continue
        if current is None:
            continue
        hit = LINE.match(line)
        if not hit:
            continue
        for b in hit.group(2).split():
            out[current]["bytes"].append(b)
        text = hit.group(3).strip()
        if not text:
            continue
        text = re.sub(r"\s+", " ", text)
        out[current]["mnem"].append(text)
    return out


def byte_list(value):
    """the recorded bytes, as a list of two-character hex strings.  The
    corpus writes them two ways: a list, and one space-separated
    string."""
    if value is None:
        return None
    if isinstance(value, list):
        return value
    text = value.strip()
    if " " in text:
        return text.split()
    return [text[i:i + 2] for i in range(0, len(text), 2)]


def compare(one, other):
    """two instruction texts, compared after the spacing the two tools
    print differently is taken out."""
    if len(one) != len(other):
        return False
    for i in range(len(one)):
        a = re.sub(r"\s+", "", one[i])
        b = re.sub(r"\s+", "", other[i])
        if a != b:
            return False
    return True


def run(indir, outdir, work, cc, dump, every):
    started = time.time()
    take, skip = gather(indir)
    log("units to assemble: %d ; units the assembler cannot be handed: "
        "%d" % (len(take), len(skip)))
    spath = os.path.join(work, "canon_roundtrip.s")
    opath = os.path.join(work, "canon_roundtrip.o")
    write_source(take, spath)
    cmd = [cc, "-c", "-x", "assembler", spath, "-o", opath]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        log("!! the canonical text did not assemble")
        log(proc.stderr[:3000])
        raise RuntimeError("round trip refused: the canonical text did "
                           "not assemble")
    log("assembled %s" % opath)
    seen = disassemble(opath, dump)
    log("the disassembly names %d labels" % len(seen))

    rows = {}
    same_text = 0
    text_differs = []
    same_as_ship = 0
    ship_differs = []
    done = 0
    for lang, n, lines, u in take:
        name = label_for(lang, n)
        got = seen.get(name)
        rec = {}
        rec["lang"] = lang
        rec["n"] = n
        rec["unit"] = "%s/op_%s" % (lang, n)
        rec["operator"] = u.get("operator")
        rec["canon_mnem"] = lines
        if got is None:
            rec["roundtrip"] = "the disassembly does not name this unit"
            rows[rec["unit"]] = rec
            continue
        rec["canon_bytes"] = got["bytes"]
        rec["disassembled_mnem"] = got["mnem"]
        agrees = compare(lines, got["mnem"])
        rec["text_survives_the_round_trip"] = agrees
        if agrees:
            same_text = same_text + 1
        else:
            text_differs.append(rec["unit"])
        ship = u.get("bytes")
        ship = byte_list(ship)
        rec["ship_bytes"] = ship
        rec["unchanged_by_the_rename"] = u.get("already_canonical")
        if u.get("already_canonical"):
            if ship == got["bytes"]:
                same_as_ship = same_as_ship + 1
                rec["bytes_match_the_recorded_ship_build"] = True
            else:
                ship_differs.append(rec["unit"])
                rec["bytes_match_the_recorded_ship_build"] = False
        rows[rec["unit"]] = rec
        done = done + 1
        if done % every == 0:
            log("  ... [%d/%d] units checked" % (done, len(take)))
    log("  ... [%d/%d] units checked" % (done, len(take)))

    out = {}
    out["what"] = "the canonical text of every canonicalised unit, "\
                  "assembled and disassembled again"
    out["assembler"] = cc
    out["units_assembled"] = len(take)
    out["units_not_handed_to_the_assembler"] = skip
    out["text_survives_the_round_trip"] = same_text
    out["text_does_not_survive"] = text_differs
    out["unchanged_units_whose_bytes_match_the_ship_build"] = same_as_ship
    out["unchanged_units_whose_bytes_differ_from_the_ship_build"] = \
        ship_differs
    out["units"] = rows
    path = os.path.join(outdir, "canon_roundtrip.json")
    fh = open(path, "w")
    json.dump(out, fh, indent=1)
    fh.close()
    log("wrote %s" % path)
    log("text survives the round trip on %d of %d units" % (same_text,
                                                            len(take)))
    log("of the units the rename left alone, %d have bytes identical to "
        "the recorded ship build, %d differ" % (same_as_ship,
                                                len(ship_differs)))
    log("wall time: %.1f s" % (time.time() - started))
    return out


def main(argv):
    indir = HERE
    outdir = HERE
    work = HERE
    cc = "clang"
    dump = "objdump"
    every = 200
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
        if argv[i] == "--every":
            every = int(argv[i + 1])
            i = i + 2
            continue
        print(__doc__)
        return 2
    run(indir, outdir, work, cc, dump, every)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
