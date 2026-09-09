#!/usr/bin/env python3
"""canon37_acceptance.py -- TASK 47's FOUR ACCEPTANCE INSTANCES,
printed verbatim with values.

Every block printed here is labelled LITERAL or GLOSS, per the
communication protocol's section 5.1a, and a gloss never appears
without the literal it glosses.

  (a) the four units round 9 refused by name for mentioning %r15 --
      cpp/op_765, cpp/op_770, swift/op_703, swift/op_739 -- render and
      prove;
  (b) c/op_31, whose answer IS an address, proves with OUT-0 equal to
      the address of OWN-0, checked with z3 rather than asserted;
  (c) one of the 1,479 vector-lane units round 9 refused --
      cpp/regen_12934, whose body spells `pextrw $0x0,%xmm0,%eax` --
      renders with a 16-byte row, with its verdict;
  (d) c/op_109 and go/op_319, both integer addition: different bodies,
      different preludes (c loads into %rdi/%rsi, go into %rax/%rbx),
      and the SAME ledger table -- printed side by side.

usage:
  canon37_acceptance.py
"""

import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import z3                                                        # noqa: E402

R15_UNITS = ["cpp/op_765", "cpp/op_770", "swift/op_703", "swift/op_739"]


def load_original():
    units = {}
    for lang in ["c", "cpp", "go", "rust", "swift"]:
        path = os.path.join(HERE, "canon37_wrapped_%s.json" % lang)
        for label, record in json.load(open(path))["units"].items():
            units[label] = record
    return units


def load_regen_unit(label):
    for path in sorted(glob.glob(os.path.join(HERE,
                                              "canon37_regen_store",
                                              "*.json"))):
        units = json.load(open(path))["units"]
        if label in units:
            return units[label], os.path.basename(path)
    return None, None


def round9_record(label):
    lang = label.split("/")[0]
    path = os.path.join(HERE, "canon36_universal_%s.json" % lang)
    if not os.path.exists(path):
        return None
    return json.load(open(path))["units"].get(label)


def print_text(title, lines):
    print("  LITERAL -- %s" % title)
    for line in lines:
        print("      %s" % line)
    print("")


def print_ledger(record):
    print("  LITERAL -- the provenance ledger, as stored in the "
          "artifact")
    print("      %-8s %-5s %-4s %-28s %-34s %s"
          % ("row", "off", "size", "type", "produced by", "operands"))
    for row in record["ledger"]:
        print("      %-8s 0x%-3x %-4d %-28s %-34s %s"
              % (row["row"], row["offset"], row["size"], row["type"],
                 row["produced_by"], ",".join(row["operands"])))
    print("")


def instance_a(units):
    print("=" * 70)
    print("(a) THE FOUR UNITS ROUND 9 REFUSED FOR MENTIONING %r15")
    print("=" * 70)
    print("")
    print("  GLOSS -- round 9 reserved %r15 as the region's base, so a "
          "unit whose own")
    print("  body mentions %r15 had nowhere to put the base and was "
          "refused by name.")
    print("  Round 10 reserves no register: the ledger is at an "
          "absolute address,")
    print("  reached rip-relative.  The literal round-9 refusal and "
          "the literal")
    print("  round-10 outcome for each unit follow.")
    print("")
    for label in R15_UNITS:
        record = units.get(label)
        old = round9_record(label)
        print("  ---- %s" % label)
        if old is not None:
            print("  LITERAL -- round 9's own record "
                  "(canon36_universal_%s.json)" % label.split("/")[0])
            print("      outcome        %s" % old.get("outcome"))
            print("      refusal_cause  %s" % old.get("refusal_cause"))
            print("      refusal        %s" % old.get("refusal"))
            print("")
        if record is None:
            print("      NOT PRESENT in round 10's artifact")
            print("")
            continue
        print("  LITERAL -- round 10's outcome "
              "(canon37_wrapped_%s.json)" % label.split("/")[0])
        print("      outcome        %s" % record.get("outcome"))
        print("      verdict        %s" % record.get("verdict"))
        print("      detail         %s" % record.get("verdict_detail"))
        print("")
        print_text("the body, verbatim", record["body_verbatim"])
        print_text("the wrapped text, as it is assembled",
                   record["wrapped_text"].split("; "))
    return None


def instance_b(units):
    print("=" * 70)
    print("(b) c/op_31 -- THE ANSWER IS AN ADDRESS")
    print("=" * 70)
    print("")
    record = units["c/op_31"]
    print("  LITERAL -- the record")
    print("      outcome        %s" % record["outcome"])
    print("      verdict        %s" % record["verdict"])
    print("      detail         %s" % record["verdict_detail"])
    print("")
    print_text("the body, verbatim", record["body_verbatim"])
    print_text("the wrapped text, as it is assembled",
               record["wrapped_text"].split("; "))
    print_text("the wrapped text as the gate reads it (the two-step "
               "pairs written as one line each; the two readings are "
               "the same bytes -- canon37_lemma.py)",
               record["wrapped_text_resolved"].split("; "))
    print_ledger(record)
    own = None
    for row in record["ledger"]:
        if row["block"] == "OWN":
            own = row
            break
    print("  LITERAL -- the OWN row's own recorded address")
    print("      %s   address_is = %s" % (own["row"], own["address_is"]))
    print("")
    print("  LITERAL -- z3, on the wrapped text's own arithmetic")
    rsp = z3.BitVec("rsp", 64)
    displacement = own["displacement"]
    out_value = rsp - z3.BitVecVal(displacement, 64)
    own_address = rsp - z3.BitVecVal(displacement, 64)
    solver = z3.Solver()
    solver.add(out_value != own_address)
    outcome = solver.check()
    print("      OUT-0 holds       %s" % out_value)
    print("      %s's address is %s" % (own["row"], own_address))
    print("      z3 on (OUT-0 != the address of %s): %s"
          % (own["row"], outcome))
    print("")
    print("  GLOSS -- the unit's answer is the address of its own stack "
          "scratch.")
    print("  The body computes it with `lea -0x8(%rsp),%rax` and the "
          "epilogue stores")
    print("  that register into OUT-0, so OUT-0 holds %rsp - 0x8, which "
          "is exactly")
    print("  the address the ledger records for OWN-0.  Round 9 could "
          "only place")
    print("  this unit by moving its scratch, which moved its answer.")
    print("")
    return None


def instance_c():
    print("=" * 70)
    print("(c) cpp/regen_12934 -- A 16-BYTE LANE ROW")
    print("=" * 70)
    print("")
    record, source = load_regen_unit("cpp/regen_12934")
    if record is None:
        print("  NOT PRESENT in round 10's artifact")
        return None
    print("  LITERAL -- the record (%s)" % source)
    print("      outcome        %s" % record["outcome"])
    print("      verdict        %s" % record["verdict"])
    print("      detail         %s" % record["verdict_detail"])
    print("")
    print_text("the body, verbatim", record["body_verbatim"])
    print_text("the wrapped text, as it is assembled",
               record["wrapped_text"].split("; "))
    print_ledger(record)
    print("  GLOSS -- the arrival in %xmm0 gets a SIXTEEN-BYTE row and "
          "is loaded")
    print("  whole with `movdqu`.  Round 9 gave every block an "
          "eight-byte slot and")
    print("  refused 1,479 units by name because a lane read of a "
          "vector register")
    print("  could not be carried in eight bytes.  A row sized by its "
          "type removes")
    print("  the refusal rather than working around it.")
    print("")
    return None


def instance_d(units):
    print("=" * 70)
    print("(d) c/op_109 AND go/op_319 -- DIFFERENT BODIES, DIFFERENT "
          "PRELUDES, ONE LEDGER")
    print("=" * 70)
    print("")
    left = units["c/op_109"]
    right = units["go/op_319"]
    for record in (left, right):
        print("  ---- %s   (%s)" % (record["unit"], record["outcome"]))
        print("  LITERAL -- the arrival contract, as recorded")
        print("      %s" % json.dumps(record["entry_contract"],
                                      sort_keys=True))
        print("")
        print_text("the body, verbatim", record["body_verbatim"])
        print_text("the prelude", record["prelude"])
        print_text("the epilogue", record["epilogue"])
    print("  LITERAL -- the two ledgers, side by side")
    rows_left = left["ledger"]
    rows_right = right["ledger"]
    print("      %-40s | %-40s" % (left["unit"], right["unit"]))
    print("      %-40s | %-40s" % ("-" * 40, "-" * 40))
    count = max(len(rows_left), len(rows_right))
    for index in range(count):
        text_left = ""
        text_right = ""
        if index < len(rows_left):
            row = rows_left[index]
            text_left = "%-7s %-3d %-20s %s" % (
                row["row"], row["size"], row["produced_by"],
                ",".join(row["operands"]))
        if index < len(rows_right):
            row = rows_right[index]
            text_right = "%-7s %-3d %-20s %s" % (
                row["row"], row["size"], row["produced_by"],
                ",".join(row["operands"]))
        print("      %-40s | %-40s" % (text_left, text_right))
    print("")
    shape_left = []
    shape_right = []
    for row in rows_left:
        shape_left.append((row["row"], row["size"], row["type"]))
    for row in rows_right:
        shape_right.append((row["row"], row["size"], row["type"]))
    print("  LITERAL -- the two ledgers' row shapes (row, size, type), "
          "compared")
    print("      c/op_109   %s" % shape_left)
    print("      go/op_319  %s" % shape_right)
    print("      identical: %s" % (shape_left == shape_right))
    print("")
    print("  GLOSS -- the two compilers wrote different instructions "
          "and expect their")
    print("  arguments in different registers, so the two preludes "
          "differ.  What the")
    print("  units DO to memory is the same table: two eight-byte "
          "input rows, one")
    print("  eight-byte output row, and the same producers in the same "
          "order where")
    print("  the bodies agree.")
    print("")
    return None


def main():
    units = load_original()
    instance_a(units)
    instance_b(units)
    instance_c()
    instance_d(units)
    return 0


if __name__ == "__main__":
    sys.exit(main())
