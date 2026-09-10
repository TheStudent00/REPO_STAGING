#!/usr/bin/env python3
"""surface.py -- THE PER-ARCHITECTURE SURFACE, COUNTED.

Node: hq.research.arch_unit_oracle.  Task rv1, brief section 5.

THE QUESTION THIS ANSWERS, in one sentence: of everything the operator
equivalence pipeline holds, how much had to be WRITTEN AGAIN to carry the
ten units of the handful from x86-64 to riscv64, and how much was read
unchanged.

HOW IT IS COUNTED, mechanically, so nobody has to trust a hand tally:
  * every file this task added is parsed with python's own `ast`, and each
    top-level function and class is measured by its first and last line;
  * each is assigned to one of the brief's four LAYERS by the table below,
    which is written out and is the only judgement in the file;
  * the x86 counterpart of each layer -- the file that does the same job on
    the other architecture -- is measured the same way, so the two sit in
    one table;
  * the objects this task READ AND DID NOT CHANGE are listed with the count
    of things each holds, read off the file itself.

usage:
  surface.py <riscv dir> <op_pipeline dir> <out prefix>
"""

import ast
import json
import os
import sys


# THE ONE JUDGEMENT IN THIS FILE: which layer each thing belongs to.  The
# four layers are the brief's own.
LAYERS = [
    ("lifter (the reference)",
     "one z3 term per place an instruction writes, read off the "
     "instruction's own text"),
    ("carve",
     "compile at the corpus's ship optimisation level and read the "
     "function's instructions back out of the object"),
    ("calling convention / canonical form",
     "which place each argument arrives in and which place the answer "
     "leaves in, per language, per architecture"),
    ("attestation",
     "which corpus unit stands for which cell of the model table"),
    ("level 0 check (beside the four layers the brief names)",
     "the bare-metal harness that runs the ratified model's simulator "
     "over one instruction at many points, and the evaluation of the "
     "reference's own term at the same points"),
]

RISCV_ASSIGNMENT = {
    "riscv_reference.py": "lifter (the reference)",
    "riscv_carve.py": "carve",
    "pick_units.py": "attestation",
    "sail_points.py": "level 0 check (beside the four layers the brief "
                      "names)",
    "claim_check.py": "calling convention / canonical form",
}

# The x86 counterpart of each layer, and WHICH PART of it does that job.
# A whole-file count would overstate the comparison for the two files that
# hold several layers, so the parts are named.
X86_COUNTERPART = {
    "lifter (the reference)": [
        ("reference.py", None),
        ("condition_table.py", None),
    ],
    "carve": [
        ("lane_gen.py", ["extract", "disasm", "compile_probe",
                         "write_unit"]),
    ],
    "calling convention / canonical form": [
        ("canonical_form.py", ["Prelude", "Epilogue", "Labels"]),
        ("ledger.py", ["DESTINATION_RULES", "answer_registers_of_body",
                       "pick_scratch", "register_text", "weave"]),
    ],
    "attestation": [
        ("oracle/arch_opcodes/model/model_table.py",
         ["attestation", "attest_command", "arch_opcode_rows",
          "lines_of_unit", "place_row"]),
    ],
    "level 0 check (beside the four layers the brief names)": [
        ("(none: level 0 on x86 is held as the reference itself, and its "
         "independent check is task ref1's K-framework reading)", None),
    ],
}

# What this task READ and did not change.  Each is (path, what it is, how
# its count is read).
READ_UNCHANGED = [
    ("op_pipeline/term66_store", "the term store: every unit's proved "
     "z3 term", "shards"),
    ("oracle/arch_opcodes/model/model_table.json", "the arch-opcode model "
     "table: the reference's mapping per (mnem, shape, key_width) with the "
     "corpus's attestation", "rows"),
    ("op_pipeline/probe_manifest_c.json", "the c probe corpus's own "
     "sources", "probes"),
    ("op_pipeline/probe_manifest_go.json", "the go probe corpus's own "
     "sources", "probes"),
    ("op_pipeline/op_units_c.json", "the c units' recorded x86 ship "
     "bodies", "probes"),
    ("op_pipeline/op_units_go.json", "the go units' recorded x86 ship "
     "bodies", "probes"),
    ("op_pipeline/reference.py", "the x86 reference, called to re-derive "
     "each unit's own x86 term", "lines"),
    ("op_pipeline/term.py", "`Term.normalize`, called to put both "
     "architectures' terms in one comparison form", "lines"),
]


def measure_file(path):
    text = open(path).read()
    lines = text.splitlines()
    total = len(lines)
    code = 0
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            continue
        code = code + 1
    tree = ast.parse(text)
    pieces = []
    for node in tree.body:
        if not isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            continue
        first = node.lineno
        last = getattr(node, "end_lineno", node.lineno)
        pieces.append({"name": node.name,
                       "kind": type(node).__name__,
                       "lines": last - first + 1})
    return {"path": path, "total_lines": total, "code_lines": code,
            "pieces": pieces}


def measure_parts(path, names):
    """the line count of the named pieces only, plus the module-level
    assignments among the names.

    `lane_gen.py` holds its carve in a module-level STRING that the lane
    runs as its own program (`DRIVER`), so a name not found at the top
    level is looked for inside that string, parsed as its own module."""
    text = open(path).read()
    tree = ast.parse(text)
    found = walk_for(tree, names)
    missing = set(names) - set(row["name"] for row in found)
    if missing:
        for node in tree.body:
            if not isinstance(node, ast.Assign):
                continue
            if not isinstance(node.value, ast.Constant):
                continue
            if not isinstance(node.value.value, str):
                continue
            try:
                inner = ast.parse(node.value.value)
            except SyntaxError:
                continue
            for row in walk_for(inner, missing):
                row["inside"] = node.targets[0].id
                found.append(row)
    return found


def walk_for(tree, names):
    wanted = set(names)
    found = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            if node.name in wanted:
                last = getattr(node, "end_lineno", node.lineno)
                found.append({"name": node.name,
                              "lines": last - node.lineno + 1})
            continue
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in wanted:
                    last = getattr(node, "end_lineno", node.lineno)
                    found.append({"name": target.id,
                                  "lines": last - node.lineno + 1})
    return found


def count_of(path, how):
    if how == "shards":
        return len([n for n in os.listdir(path) if n.endswith(".json")])
    if how == "lines":
        return len(open(path).read().splitlines())
    doc = json.load(open(path))
    if how == "rows":
        return len(doc.get("rows") or [])
    return len(doc.get("probes") or {})


def main():
    riscv_dir = sys.argv[1]
    op_dir = sys.argv[2]
    out_prefix = sys.argv[3]

    written = []
    for name in sorted(RISCV_ASSIGNMENT):
        path = os.path.join(riscv_dir, name)
        record = measure_file(path)
        record["layer"] = RISCV_ASSIGNMENT[name]
        record["file"] = name
        written.append(record)

    by_layer = {}
    for record in written:
        layer = record["layer"]
        row = by_layer.setdefault(layer, {"layer": layer, "files": [],
                                          "total_lines": 0,
                                          "code_lines": 0})
        row["files"].append(record["file"])
        row["total_lines"] = row["total_lines"] + record["total_lines"]
        row["code_lines"] = row["code_lines"] + record["code_lines"]

    research_root = os.path.dirname(op_dir.rstrip("/"))
    counterparts = {}
    for layer, parts in X86_COUNTERPART.items():
        rows = []
        for name, names in parts:
            if name.startswith("("):
                rows.append({"file": name, "lines": 0, "pieces": []})
                continue
            if "/" in name:
                path = os.path.join(research_root, name)
            else:
                path = os.path.join(op_dir, name)
            if names is None:
                measured = measure_file(path)
                rows.append({"file": name,
                             "lines": measured["total_lines"],
                             "code_lines": measured["code_lines"],
                             "pieces": []})
                continue
            pieces = measure_parts(path, names)
            rows.append({"file": name,
                         "lines": sum(p["lines"] for p in pieces),
                         "pieces": pieces})
        counterparts[layer] = rows

    unchanged = []
    root = research_root
    for relative, what, how in READ_UNCHANGED:
        path = os.path.join(root, relative)
        try:
            count = count_of(path, how)
        except Exception as exc:
            count = "UNREADABLE: %s" % exc
        unchanged.append({"path": relative, "what": what,
                          "count": count, "counted_as": how})

    doc = {
        "meta": {
            "task": "rv1",
            "what": "every file and function that had to be written to "
                    "carry the pipeline from x86-64 to riscv64 for the "
                    "handful's ten units, by layer, with the x86 "
                    "counterpart beside it and the objects that were read "
                    "unchanged listed",
            "layers": [{"layer": name, "what": what}
                       for name, what in LAYERS],
        },
        "written": written,
        "by_layer": [by_layer[name] for name, _ in LAYERS
                     if name in by_layer],
        "x86_counterpart": counterparts,
        "read_unchanged": unchanged,
    }
    fh = open(out_prefix + ".json", "w")
    json.dump(doc, fh, indent=1, sort_keys=True)
    fh.write("\n")
    fh.close()

    print("| layer | files written | total lines | code lines |")
    print("|---|---|---|---|")
    grand_total = 0
    grand_code = 0
    for name, _what in LAYERS:
        row = by_layer.get(name)
        if row is None:
            continue
        grand_total = grand_total + row["total_lines"]
        grand_code = grand_code + row["code_lines"]
        print("| %s | %s | %d | %d |"
              % (name, ", ".join(row["files"]), row["total_lines"],
                 row["code_lines"]))
    print("| **all five** | %d files | %d | %d |"
          % (len(written), grand_total, grand_code))
    print()
    print("| layer | the x86 counterpart | its lines |")
    print("|---|---|---|")
    for name, _what in LAYERS:
        for row in counterparts.get(name, []):
            print("| %s | %s | %d |" % (name, row["file"], row["lines"]))
    print()
    print("| read unchanged | what it is | count |")
    print("|---|---|---|")
    for row in unchanged:
        print("| %s | %s | %s %s |"
              % (row["path"], row["what"], row["count"],
                 row["counted_as"]))
    print()
    print("per-function detail:")
    for record in written:
        print("  %s  (%d lines total, %d code)"
              % (record["file"], record["total_lines"],
                 record["code_lines"]))
        for piece in record["pieces"]:
            print("      %-34s %s %d lines"
                  % (piece["name"], piece["kind"], piece["lines"]))


if __name__ == "__main__":
    main()
