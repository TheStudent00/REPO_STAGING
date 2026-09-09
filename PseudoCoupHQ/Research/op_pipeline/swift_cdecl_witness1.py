#!/usr/bin/env python3
"""swift_cdecl_witness1.py -- MEASURE which swift types swiftc will let a
`@_cdecl` function carry, in each of the two positions a probe uses.

WHY THIS FILE EXISTS (task 50(a), finding F45-4 of log 137)
-----------------------------------------------------------
`probe_gen.py :: emit_swift` decides whether to attach `@_cdecl` to a
probe by testing the RESULT type against a hand-written set:

    C_REPRESENTABLE = {"Int32", "Int64", "UInt64", "Float", "Double",
                       "Bool"}

Two defects in one line.  First, the parameters are not tested at all,
so a probe whose result is `Int64` but whose second parameter is
`Int128` still gets the attribute, and swiftc refuses the whole
function.  Second, the set is a HAND LIST: it is not evidence, it is a
guess about the compiler, and it cannot be checked against anything.

This program replaces the guess with the compiler's own testimony.  For
every swift type in `type_inventory3.json` it compiles two tiny
functions with NO OPERATOR IN THEM AT ALL, using the probe lane's own
swift flags, and records the verdict and the verbatim diagnostic:

    form `cdecl_parameter`  the type in a parameter position of a
                            `@_cdecl` function
    form `cdecl_result`     the type in the result position of a
                            `@_cdecl` function

The two forms are recorded separately, and both are kept, because the
defect being fixed is exactly a case where one position was assumed to
answer for the other.

WHAT A PROBE NEEDS, AND WHERE IT COMES FROM
-------------------------------------------
`emit_swift` writes one function whose parameters are the holder types
and whose result is the result type.  So the corrected test is:

    attach @_cdecl  <=>  the result type passed `cdecl_result`
                     AND every parameter type passed `cdecl_parameter`

`probe_gen3.py` reads exactly that from this program's product.

THE VALUE IN THE RESULT FORM
----------------------------
A result form must return a value of the type.  The value is built from
the type's own recorded CLASS in the inventory (`truth_value` returns
`false`; every other class is numeric and returns `T(0)`), never from a
list of spellings written here.  A class this program has no
construction for is REFUSED by name rather than guessed at.

THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns.  The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token.  The
token appears exactly once per unit: as a display label on the member.
HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs").  MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure.  A brief handed to any subagent for this
line MUST paste this paragraph verbatim.

This program's subject is TYPES.  There is no operator anywhere in the
sources it compiles, in its keys, or in its product.

WHERE IT RUNS
-------------
The generation and the fold run on the host.  The 34 compilations run
inside Airlock's `trickle` instance, submitted through
`airlock submit`.  Nothing here runs podman; the lane is handed over
and four folders are read back (the rule recorded in
TRICKLE_SUPERSEDED.md).

usage:
    /tmp/reconnect_venv/bin/python3 swift_cdecl_witness1.py --emit
    /tmp/reconnect_venv/bin/python3 swift_cdecl_witness1.py --run
writes:
    task50a_lanes/cdecl_swift.sh
    swift_cdecl_witness1.json
"""

import argparse
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import declare_lane                                        # noqa: E402
import trickle2                                            # noqa: E402
import verbatim_diag                                       # noqa: E402

INVENTORY = os.path.join(HERE, "type_inventory3.json")
LANE_DIR = os.path.join(HERE, "task50a_lanes")
OUTBOX = os.path.join(HERE, "task50a_outbox")
RAW_DIR = os.path.join(HERE, "task50a_raw")
PRODUCT = os.path.join(HERE, "swift_cdecl_witness1.json")

LANE_NAME = "cdecl_swift.sh"
OUT_NAME = "cdecl_swift"

# How a value of a class is written.  The class is READ FROM THE
# INVENTORY (`class` / `class_source`); this table says only how to
# write a zero of a class, and refuses a class it does not know.
ZERO_OF_CLASS = {
    "truth_value": "false",
    "integer_signed": None,      # None means "T(0)"
    "integer_unsigned": None,
    "float": None,
}


def zero_expression(spelling, klass):
    if klass not in ZERO_OF_CLASS:
        raise SystemExit(
            "REFUSE: no zero construction recorded for class %r "
            "(type %s).  Add one deliberately rather than guessing."
            % (klass, spelling))
    literal = ZERO_OF_CLASS[klass]
    if literal is not None:
        return literal
    return "%s(0)" % spelling


def source_cdecl_parameter(spelling, klass):
    """The type in a parameter position of a @_cdecl function.

    The result is fixed at Int32, which the current corpus already
    exports under @_cdecl, so a refusal here is about the PARAMETER.
    """
    lines = []
    lines.append('@_cdecl("cdeclHolder")')
    lines.append("public func cdeclHolder(_ a: %s) -> Int32 {" % spelling)
    lines.append("    return 0")
    lines.append("}")
    return "\n".join(lines) + "\n"


def source_cdecl_result(spelling, klass):
    """The type in the result position of a @_cdecl function.

    The parameter is fixed at Int32 for the mirror-image reason.
    """
    lines = []
    lines.append('@_cdecl("cdeclAnswer")')
    lines.append("public func cdeclAnswer(_ a: Int32) -> %s {" % spelling)
    lines.append("    return %s" % zero_expression(spelling, klass))
    lines.append("}")
    return "\n".join(lines) + "\n"


def items():
    """One item per (type, form).  Ids and classes come from the
    inventory; nothing about the type set is written here."""
    inv = json.load(open(INVENTORY))
    entries = inv["languages"]["swift"]["types"]
    out = []
    for entry in entries:
        spelling = entry["spelling"]
        klass = entry["class"]
        if "::" in spelling:
            continue
        out.append({"language": "swift", "id": entry["id"],
                    "spelling": spelling, "form": "cdecl_parameter",
                    "source": source_cdecl_parameter(spelling, klass)})
        out.append({"language": "swift", "id": entry["id"],
                    "spelling": spelling, "form": "cdecl_result",
                    "source": source_cdecl_result(spelling, klass)})
    return out, entries


def emit():
    rows, entries = items()
    if not os.path.isdir(LANE_DIR):
        os.makedirs(LANE_DIR)
    text = declare_lane.lane("swift", rows, OUT_NAME)
    path = os.path.join(LANE_DIR, LANE_NAME)
    fh = open(path, "w")
    fh.write(text)
    fh.close()
    print("swift %4d compilations (%d types x 2 forms) -> %s"
          % (len(rows), len(rows) // 2, path))
    print("first item, verbatim:")
    print(rows[0]["source"])
    return path


def parse_product(text):
    """The lane's pipe-delimited product, decoded with the codec of
    record.  A product without the marker is REFUSED, not decoded."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != verbatim_diag.MARKER:
        raise SystemExit(
            "REFUSE: product does not open with the verbatim marker %r"
            % verbatim_diag.MARKER)
    rows = []
    for line in lines[1:]:
        if not line.strip():
            continue
        fields = line.split("|")
        if len(fields) != 4:
            raise SystemExit("REFUSE: product row has %d fields, not 4: %r"
                             % (len(fields), line[:120]))
        rows.append({
            "id": verbatim_diag.decode(fields[0]),
            "form": verbatim_diag.decode(fields[1]),
            "verdict": fields[2],
            "diagnostic": verbatim_diag.decode(fields[3]),
        })
    return rows


def run():
    path = emit()
    if not os.path.isdir(OUTBOX):
        os.makedirs(OUTBOX)
    if not os.path.isdir(RAW_DIR):
        os.makedirs(RAW_DIR)
    lane_copy = os.path.join(OUTBOX, LANE_NAME)
    shutil.copyfile(path, lane_copy)
    inst = trickle2.Instance()
    print(inst.describe())
    ok, said = inst.submit(lane_copy)
    print(said.strip())
    if not ok:
        raise SystemExit("REFUSE: airlock submit did not accept the lane")
    fields = inst.wait(LANE_NAME, 1800)
    print("status: %s" % json.dumps(fields))
    if fields.get("state") != "done":
        raise SystemExit("REFUSE: lane did not finish (state=%s)"
                         % fields.get("state"))
    product = os.path.join(inst.out, "%s.txt" % OUT_NAME)
    if not os.path.isfile(product):
        raise SystemExit("REFUSE: no product at %s" % product)
    raw = os.path.join(RAW_DIR, "%s.txt" % OUT_NAME)
    shutil.copyfile(product, raw)
    rows = parse_product(open(raw).read())
    fold(rows, raw)


def fold(rows, raw_path):
    inv = json.load(open(INVENTORY))
    entries = inv["languages"]["swift"]["types"]
    by_id = {}
    for entry in entries:
        by_id[entry["id"]] = entry
    seen = {}
    for row in rows:
        seen[(row["id"], row["form"])] = row
    types = []
    tally = {"cdecl_parameter_accept": 0, "cdecl_parameter_refuse": 0,
             "cdecl_result_accept": 0, "cdecl_result_refuse": 0}
    for entry in entries:
        pid = (entry["id"], "cdecl_parameter")
        rid = (entry["id"], "cdecl_result")
        if pid not in seen or rid not in seen:
            raise SystemExit("REFUSE: no measurement for %s" % entry["id"])
        prow = seen[pid]
        rrow = seen[rid]
        tally["cdecl_parameter_" + prow["verdict"].lower()] += 1
        tally["cdecl_result_" + rrow["verdict"].lower()] += 1
        types.append({
            "language": "swift",
            "id": entry["id"],
            "spelling": entry["spelling"],
            "class": entry["class"],
            "c_representable": {
                "witness": "compiler_typecheck_under_cdecl",
                "source": "/persist/swift/usr/bin/swiftc in the Airlock "
                          "instance `trickle`",
                "parameter_form": {"verdict": prow["verdict"],
                                   "refusal": prow["diagnostic"]},
                "result_form": {"verdict": rrow["verdict"],
                                "refusal": rrow["diagnostic"]},
                "verification": "compiled_in_the_trickle_instance",
            },
        })
    doc = {}
    doc["generated_by"] = "swift_cdecl_witness1.py"
    doc["task"] = "50(a) -- the swift probe emitter's @_cdecl test"
    doc["reads"] = ["type_inventory3.json"]
    doc["what_it_measures"] = (
        "for each swift type, whether swiftc accepts that type in a "
        "@_cdecl function's PARAMETER position and in its RESULT "
        "position, measured separately.  No operator appears in any "
        "compiled source; the subject is types.")
    doc["flags"] = ("/persist/swift/usr/bin/swiftc -Onone -g -c, copied "
                    "from lane_gen.py :: compile_probe, anchor mode")
    doc["supersedes"] = (
        "probe_gen.py :: C_REPRESENTABLE, a hand-written set of six "
        "spellings tested against the result type only")
    doc["spelling_ban"] = (
        "no operator token appears in any key, grouping, pairing or row "
        "structure of this document; the subject is types")
    doc["raw_product"] = os.path.relpath(raw_path, HERE)
    doc["types"] = types
    doc["tally"] = tally
    fh = open(PRODUCT, "w")
    json.dump(doc, fh, indent=1)
    fh.write("\n")
    fh.close()
    print("wrote %s" % PRODUCT)
    print("tally: %s" % json.dumps(tally))
    for row in types:
        print("  %-10s parameter %-6s result %-6s"
              % (row["spelling"],
                 row["c_representable"]["parameter_form"]["verdict"],
                 row["c_representable"]["result_form"]["verdict"]))
    guard(PRODUCT)


def guard(path):
    cmd = [sys.executable, os.path.join(HERE, "check_no_spelling_keys.py"),
           path]
    done = subprocess.run(cmd, capture_output=True, text=True)
    print(done.stdout.strip())
    if done.returncode != 0:
        print(done.stderr.strip())
        os.remove(path)
        raise SystemExit("REFUSED OWN OUTPUT: spelling guard failed")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit", action="store_true")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--fold", metavar="RAWFILE")
    args = ap.parse_args()
    if args.emit:
        emit()
        return
    if args.fold:
        fold(parse_product(open(args.fold).read()), args.fold)
        return
    if args.run:
        run()
        return
    ap.error("one of --emit, --run, --fold is required")


if __name__ == "__main__":
    main()
