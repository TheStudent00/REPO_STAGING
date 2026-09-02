#!/usr/bin/env python3
"""add_java.py -- match the canonicalised JVM unit against the table,
and record it as a member if it matches.

The match is LEVEL 1: byte identity after canonicalisation, which is
the strongest thing the pipeline has.  THE CANONICAL RUNNABLE FORM
says so: "Level 1 matching = byte identity after canonicalization
(stronger than formula-text match: still bytes, and executable)."  If
the canonical bytes are equal there is nothing for the lifted form or
the solver to add, and neither is asked.  If they are NOT equal this
file prints exactly where the two byte strings and the two texts part
company and records the divergence; it does not fall through to a
weaker test to manufacture a match.

The class key is checked as well as the bytes, because RESULT TYPE is
part of every class key.  java's `int32` operands and `int32` result
are read as the pipeline's `i32`; that mapping is the one assumption
in this file and it is stated on the product.

WHAT IS RECORDED ON THE MEMBER, and why.  The bytes are the JVM's own
testimony about code it generated at run time, carved out of a print
by our lane -- not an ELF section a compiler wrote to disk.  That is
weaker provenance than every other member of the table.  The member
carries `evidence_class`, `provenance` and `provenance_is_weaker` so
nothing downstream can read it as the same class of evidence as a c or
rust unit.

THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key,
grouping, pairing, row structure, candidate selection, or comparison
scope, anywhere in this line -- not in matching, not in "which pairs
get compared", not in report rows, not in dropdowns.  The candidate
set for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention -- never from the
token.  The token appears exactly once per unit: as a display label on
the member.

How this file obeys it: the class is found by CANONICAL BYTES and by
the class key.  java's `+` never selects anything; it is written once,
as `operator`, on the member object.

Products:
  dominant_table5.json     table 4 with the java member in its class
  probe_manifest_java.json the provenance record dom_ops reads
  core_modes_java.json     the core/mode record dom_ops reads
  add_java.json            what matched, and on what evidence

usage:
  add_java.py [--in DIR] [--out DIR]
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# java's own type words, as interp_jvm.json records them, read as the
# pipeline's representation words.  The one assumption in this file.
TYPE_READING = {
    "int32": "i32",
    "int64": "i64",
    "float32": "f32",
    "float64": "f64",
    "boolean": "bool",
}


def log(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def canon_bytes_index(indir):
    """unit label -> the canonical bytes, as one spaced string."""
    path = os.path.join(indir, "canon_roundtrip.json")
    doc = json.load(open(path))
    out = {}
    for label in doc["units"]:
        rec = doc["units"][label]
        got = rec.get("canon_bytes")
        if not got:
            continue
        out[label] = " ".join(got)
    return out


def first_difference(a, b):
    """where two spaced byte strings part company."""
    xs = a.split()
    ys = b.split()
    n = min(len(xs), len(ys))
    for i in range(n):
        if xs[i] != ys[i]:
            return dict(at_byte=i, left=xs[i], right=ys[i],
                        why="the two byte strings differ at byte %d"
                            % i)
    if len(xs) == len(ys):
        return None
    return dict(at_byte=n, left=(xs[n:] or None), right=(ys[n:] or None),
                why="one byte string is longer: %d against %d"
                    % (len(xs), len(ys)))


def main():
    indir = HERE
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

    jvm = json.load(open(os.path.join(indir, "jvm_canon.json")))
    out = {}
    out["what_this_is"] = "the canonicalised JVM unit matched against "\
                          "the equivalence classes by canonical bytes"
    out["match_level"] = "level 1: byte identity after "\
                         "canonicalisation"
    out["type_reading"] = TYPE_READING
    out["type_reading_note"] = "java's own type words read as the "\
                               "pipeline's representation words.  The "\
                               "one assumption in this file."

    if jvm.get("refused"):
        out["refused"] = dict(
            why="jvm_canon.py refused the unit, so there is nothing to "
                "match", detail=jvm["refused"])
        write(out, outdir, "add_java.json")
        log("!! REFUSED: %s" % out["refused"]["why"])
        return 4

    want = jvm["canonical_bytes"]
    unit = jvm["unit"]
    operand_key = "%s,%s" % (
        TYPE_READING.get(unit["operand_types"][0]),
        TYPE_READING.get(unit["operand_types"][1]))
    result_key = TYPE_READING.get(unit["result_type"])
    out["java_unit"] = dict(unit)
    out["java_canonical_form"] = jvm["canonical_form"]
    out["java_canonical_bytes"] = want
    out["class_key_looked_for"] = dict(operand_types=operand_key,
                                       result_type=result_key)

    index = canon_bytes_index(indir)
    byte_equal = []
    for label in sorted(index):
        if index[label] == want:
            byte_equal.append(label)
    out["units_with_equal_canonical_bytes"] = byte_equal
    log("units with equal canonical bytes: %d" % len(byte_equal))

    table = json.load(open(os.path.join(indir,
                                        "dominant_table4.json")))
    hits = []
    for row in table["rows"]:
        key = row["class_key"]
        if key["operand_types"] != operand_key:
            continue
        if key["result_type"] != result_key:
            continue
        members = [m["unit"] for m in row["members"]]
        shared = [x for x in members if x in byte_equal]
        if shared:
            hits.append((row, shared))

    if len(hits) != 1:
        near = []
        for row in table["rows"]:
            key = row["class_key"]
            if key["operand_types"] != operand_key:
                continue
            if key["result_type"] != result_key:
                continue
            for form in row.get("canonical_core") or []:
                del form
            for m in row["members"]:
                label = m["unit"]
                have = index.get(label)
                if have is None:
                    continue
                near.append(dict(unit=label,
                                 canonical_form=m["canonical_form"],
                                 canonical_bytes=have,
                                 difference=first_difference(want,
                                                             have)))
        near.sort(key=lambda r: (r["difference"] or {}).get("at_byte",
                                                            999),
                  reverse=True)
        out["refused"] = dict(
            why="the canonical bytes matched %d classes on this class "
                "key; a member is recorded only on exactly one"
                % len(hits),
            classes=[r["class_id"] for r, _s in hits])
        out["where_it_diverges"] = near[:20]
        write(out, outdir, "add_java.json")
        log("!! REFUSED: %s" % out["refused"]["why"])
        for rec in near[:5]:
            log("   %s  %s" % (rec["unit"], rec["canonical_bytes"]))
            log("      java  %s" % want)
            log("      %s" % json.dumps(rec["difference"]))
        return 4

    row, shared = hits[0]
    log("matched class %s on units %s" % (row["class_id"], shared))

    member = {}
    member["unit"] = "java/op_1"
    member["lang"] = "java"
    member["n"] = "1"
    member["operator"] = unit["operator"]
    member["type_pair"] = operand_key
    member["mode_count"] = 0
    member["result_type"] = result_key
    member["result_type_as_the_language_spells_it"] = "int"
    member["canonical_form"] = jvm["canonical_form"]
    member["canonicalisation_refused"] = None
    member["evictions"] = []
    member["evidence_class"] = jvm["evidence_class"]
    member["provenance"] = "the JVM's own print of the machine code "\
                           "its C2 compiler produced for a warmed "\
                           "method, carved by the lane; the runtime "\
                           "furniture stripped by named rule"
    member["provenance_is_weaker"] = True
    member["matched_by"] = dict(
        level="level 1: byte identity after canonicalisation",
        canonical_bytes=want,
        equal_to=shared,
        lifted_form_asked=False,
        solver_asked=False,
        why_not="the canonical bytes are equal, so there is nothing "
                "the lifted form or the solver could add")
    member["stripped_furniture"] = jvm["stripped"]

    for r in table["rows"]:
        if r["class_id"] != row["class_id"]:
            continue
        r["members"].append(member)
        r["members"].sort(key=lambda m: m["unit"])
        r["size"] = len(r["members"])
        if "java" not in r["languages"]:
            r["languages"].append("java")
            r["languages"].sort()
        r["coverage"]["languages_present"] = sorted(r["languages"])
        r["weaker_provenance_members"] = ["java/op_1"]
        r["weaker_provenance_note"] = jvm["evidence_class"]
        r["evidence"]["member_pairs_by_class"]["byte"] = \
            r["evidence"]["member_pairs_by_class"].get("byte", 0) + 1

    table["java"] = dict(
        added=True,
        unit="java/op_1",
        class_id=row["class_id"],
        evidence_class=jvm["evidence_class"],
        note="java's unit is NOT an ELF artifact.  Its provenance is "
             "weaker than every other member of this table and it is "
             "marked on the member.")
    table["languages"] = table["languages"] + ["java"]
    write(table, outdir, "dominant_table5.json")

    manifest = dict(
        meta=dict(language="java",
                  holders=[dict(rep="i32", type="int")],
                  buckets_read=["binary"],
                  acceptance="the JVM's C2 compiler produced the "
                             "nmethod; the method compiled and ran",
                  provenance="run-time JIT output, not an ELF section",
                  evidence_class=jvm["evidence_class"]),
        count=1,
        # `lang` is carried on the probe record so that the token on it
        # sits on an object that identifies ONE unit, which is the one
        # place THE SPELLING BAN allows a token.  The five earlier
        # manifests do not carry it; that is noted, not changed here.
        probes={"1": dict(n=1, lang="java", operator=unit["operator"],
                          arity="binary", position=None,
                          bucket="binary",
                          lhs_rep="i32", lhs_type="int",
                          rhs_rep="i32", rhs_type="int",
                          expression="a + b",
                          result_type="int",
                          result_rule="the JVM's own method descriptor "
                                      "'(II)I'",
                          symbol="op_1", symbol_exact=True,
                          source="static int %s(int a, int b) { "
                                 "return a + b; }"
                                 % unit["method"])})
    write(manifest, outdir, "probe_manifest_java.json")

    modes = dict(
        language="java",
        shape="one entry per unit: the normal-path core and the modes",
        spelling="the operator token appears once per unit, as the "
                 "display label `operator`",
        core_note="the core is NOT a lifted form here.  The lifter was "
                  "not run on the JVM unit; the canonical text stands "
                  "in its place and says so.",
        solver_run=False,
        lifter=None,
        z3=None,
        units={"1": dict(lang="java", n="1",
                         operator=unit["operator"],
                         type_pair=operand_key,
                         meta=manifest["probes"]["1"],
                         bytes=want,
                         core=[jvm["canonical_form"]],
                         core_is_the_canonical_text=True,
                         modes=[])})
    write(modes, outdir, "core_modes_java.json")

    out["matched_class"] = row["class_id"]
    out["matched_against"] = shared
    out["member_recorded"] = member
    write(out, outdir, "add_java.json")
    return 0


def write(doc, outdir, name):
    path = os.path.join(outdir, name)
    fh = open(path, "w")
    json.dump(doc, fh, indent=1)
    fh.write("\n")
    fh.close()
    log("wrote %s" % path)


if __name__ == "__main__":
    sys.exit(main())
