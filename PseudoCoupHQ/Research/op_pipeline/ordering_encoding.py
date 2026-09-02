#!/usr/bin/env python3
"""ordering_encoding.py -- read the C++ ordering encoding out of the
lane's own output, and write it as data.

dominance.py refuses to give a result type a projection it has not
been told about, and says why in its own words:

    "A result type this table does not name gets NO projection.  The
     pair is recorded with the reason and no bridge is claimed.
     Reading, say, `partial_ordering` as "some number of bits" would
     be human interpretation of stated design, the weakest evidence
     class, and this file does not do it."

This file turns that interpretation into a measurement.  It parses
`lane_out_ordering/`, which is what the Airlock lane
`lanes/pc_ordering_probe.sh` produced, and writes
`ordering_encoding.json`.

TWO INDEPENDENT READINGS ARE PARSED AND KEPT SEPARATE, because they
belong to different evidence classes and their agreement is the point:

  READING A -- the object representation, executed.  Each named
  constant memcpy'd into an unsigned char array, every byte printed.
  Evidence class: the tool's own testimony, executed.

  READING B -- the emitted code.  A function returning each constant,
  compiled at -O2 and disassembled; the immediate the compiler moves
  into the result register is the value.  Evidence class: forced by
  construction -- nothing but that value explains that byte.

If the two readings disagree on any constant, this file REFUSES and
names the constant.  Agreement is not assumed; it is checked.

usage:
  ordering_encoding.py [--in DIR] [--out DIR]
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# the families the C++ standard library ships, and which names each
# one carries.  This list is the SUBJECT of the measurement, not its
# answer: it says what was asked about, never what came back.
FAMILIES = {
    "partial_ordering": ["less", "equivalent", "greater", "unordered"],
    "weak_ordering": ["less", "equivalent", "greater"],
    "strong_ordering": ["less", "equal", "equivalent", "greater"],
}

REP_LINE = re.compile(
    r"^(\w+) (\w+) sizeof=(\d+) bytes=([0-9a-f ]+)\s+"
    r"as_signed_char=(-?\d+)\s*$")

FUNC_HEAD = re.compile(r"^[0-9a-f]+ <(\w+)>:\s*$")

MOV_AL = re.compile(r"^\s*[0-9a-f]+:\s+mov\s+\$0x([0-9a-f]+),%al\s*$")

XOR_EAX = re.compile(r"^\s*[0-9a-f]+:\s+xor\s+%eax,%eax\s*$")

# the emitted-code probe's function names, and which constant each one
# returns.  The mapping is the probe's own source, restated here so
# the parse has something to key on; the VALUES all come from the
# disassembly.
EMIT_NAMES = {
    "p_less": ("partial_ordering", "less"),
    "p_equivalent": ("partial_ordering", "equivalent"),
    "p_greater": ("partial_ordering", "greater"),
    "p_unordered": ("partial_ordering", "unordered"),
    "s_less": ("strong_ordering", "less"),
    "s_equal": ("strong_ordering", "equal"),
    "s_greater": ("strong_ordering", "greater"),
}


def read_representation(path):
    """READING A: family -> name -> record."""
    out = {}
    sizes = {}
    for line in open(path):
        m = REP_LINE.match(line.rstrip("\n"))
        if m is None:
            continue
        family = m.group(1)
        name = m.group(2)
        size = int(m.group(3))
        raw = m.group(4).split()
        signed = int(m.group(5))
        if family not in out:
            out[family] = {}
        out[family][name] = dict(bytes=raw, size=size,
                                 as_signed_char=signed)
        sizes[family] = size
    return out, sizes


def read_emitted(path):
    """READING B: family -> name -> the byte the compiler moves."""
    out = {}
    current = None
    for line in open(path):
        m = FUNC_HEAD.match(line)
        if m is not None:
            current = m.group(1)
            continue
        if current is None:
            continue
        if current not in EMIT_NAMES:
            continue
        family, name = EMIT_NAMES[current]
        m = MOV_AL.match(line)
        if m is not None:
            value = m.group(1).zfill(2)
            if family not in out:
                out[family] = {}
            out[family][name] = dict(byte=value,
                                     instruction=line.strip())
            current = None
            continue
        if XOR_EAX.match(line) is not None:
            if family not in out:
                out[family] = {}
            out[family][name] = dict(byte="00",
                                     instruction=line.strip())
            current = None
            continue
    return out


def main():
    indir = os.path.join(HERE, "lane_out_ordering")
    outdir = HERE
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--in":
            i = i + 1
            indir = args[i]
        elif args[i] == "--out":
            i = i + 1
            outdir = args[i]
        i = i + 1

    rep, sizes = read_representation(os.path.join(indir,
                                                  "representation.txt"))
    emitted = read_emitted(os.path.join(indir, "emit_ship.txt"))

    disagreements = []
    for family in sorted(emitted):
        for name in sorted(emitted[family]):
            a = rep.get(family, {}).get(name)
            if a is None:
                disagreements.append(dict(
                    family=family, name=name,
                    why="the emitted-code reading has it, the object "
                        "representation reading does not"))
                continue
            if a["bytes"][0] != emitted[family][name]["byte"]:
                disagreements.append(dict(
                    family=family, name=name,
                    representation=a["bytes"][0],
                    emitted=emitted[family][name]["byte"],
                    why="the two readings disagree"))

    if disagreements:
        print("!! REFUSING: the two readings disagree.")
        for d in disagreements:
            print("   %s" % json.dumps(d))
        return 1

    missing = []
    for family in FAMILIES:
        for name in FAMILIES[family]:
            if name not in rep.get(family, {}):
                missing.append("%s::%s" % (family, name))
    if missing:
        print("!! REFUSING: not measured: %s" % ", ".join(missing))
        return 1

    compiler = open(os.path.join(indir, "compiler.txt")).read()

    doc = {}
    doc["what_this_is"] = "the measured bit encoding of the C++ "\
                          "ordering result types, read from the "\
                          "compiler rather than from the standard"
    doc["why"] = "dominance.py gives a result type no projection "\
                 "unless it is told the width, and says that reading "\
                 "one off the specification would be interpretation "\
                 "of stated design.  This is the measurement that "\
                 "replaces the interpretation."
    doc["lane"] = "lanes/pc_ordering_probe.sh"
    doc["compiler"] = compiler.strip().splitlines()
    doc["reading_a"] = dict(
        what="the object representation, executed: each constant "
             "memcpy'd into an unsigned char array",
        evidence_class="the tool's own testimony, executed",
        values=rep)
    doc["reading_b"] = dict(
        what="the emitted code at -O2: the immediate the compiler "
             "moves into the result register",
        evidence_class="forced by construction: nothing but that "
                       "value explains that byte",
        values=emitted)
    doc["readings_agree"] = True
    doc["readings_checked"] = sorted(
        "%s::%s" % (f, n) for f in emitted for n in emitted[f])
    doc["size_bytes"] = sizes
    doc["projection"] = {}
    for family in sorted(sizes):
        doc["projection"][family] = dict(
            bits=sizes[family] * 8,
            register="rax",
            promise="the low %d bits of the result register, holding "
                    "one of the measured encoding values"
                    % (sizes[family] * 8),
            measured_values=dict(
                (name, rep[family][name]["bytes"][0])
                for name in sorted(rep[family])))
    doc["note_on_bool"] = "this is NOT the bool projection.  A bool "\
                          "return promises 0 or 1 in the low byte; "\
                          "an ordering return uses the same width and "\
                          "a different value set, which is why the "\
                          "measured values travel with the width."

    path = os.path.join(outdir, "ordering_encoding.json")
    fh = open(path, "w")
    json.dump(doc, fh, indent=1)
    fh.write("\n")
    fh.close()
    print("wrote %s" % path)
    for family in sorted(doc["projection"]):
        print("   %-18s %d bits, values %s"
              % (family, doc["projection"][family]["bits"],
                 json.dumps(doc["projection"][family]
                            ["measured_values"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
