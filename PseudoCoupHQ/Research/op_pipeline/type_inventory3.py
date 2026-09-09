#!/usr/bin/env python3
"""type_inventory3.py -- the type inventory's SECOND WITNESS, folded in.

WHAT THE SECOND WITNESS IS
--------------------------
`type_inventory2.json` records, per language, every type spelling an
AUTHORITY admits: the compiler's own type table, the tree-sitter
grammar, the stdlib source, the installed module interface.  That is
the witness "this toolchain KNOWS the spelling".

`declare_lane.py` asked a different question, one tiny compile per type
per language in the trickle container, with no operator in the source:
"is this spelling DECLARABLE ON THIS TARGET WITH THIS TOOLCHAIN, at the
flags the probe lanes use?"  Two forms were compiled per type:

    variable   -- a variable declaration of the type, nothing else
    parameter  -- the type in the position a probe puts it in

This program folds those answers into a new inventory.  A type is in
`type_inventory3.json` when it is EXTRACTED (it was in inventory 2) AND
DECLARABLE (its `parameter` form compiled).  The parameter form decides,
because a probe holder IS a parameter; the variable answer is recorded
beside it, and the types where the two disagree are reported.

NOTHING EXISTING IS MODIFIED.  `type_inventory2.json` is read only.

THE SPELLING BAN
----------------
No operator token appears in any key, grouping, pairing or row structure
here; the subject of this file is types.  Every type spelling rides on
an object carrying `language` and `id`, spelling in a display field.

usage:  /tmp/reconnect_venv/bin/python3 type_inventory3.py
writes: type_inventory3.json, type_demotions1.json
"""

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import verbatim_diag                                       # noqa: E402

LANGS = ["c", "cpp", "go", "rust", "swift"]
RAW = os.path.join(HERE, "declare_raw")


def read_product(lang):
    """{(type id, form): (verdict, verbatim message)}, decoded.

    A product without the codec marker is REFUSED rather than decoded:
    decoding an unescaped line would alter a backslash the compiler
    really emitted, which is the defect verbatim_diag.py exists to
    prevent."""
    path = os.path.join(RAW, "decl_%s.txt" % lang)
    lines = open(path).read().split("\n")
    if not lines or lines[0].strip() != verbatim_diag.MARKER:
        raise SystemExit(
            "type_inventory3: %s does not open with %r; refusing to decode"
            % (path, verbatim_diag.MARKER))
    out = {}
    for line in lines[1:]:
        if not line.strip():
            continue
        parts = line.split("|")
        if len(parts) != 4:
            raise SystemExit(
                "type_inventory3: %s has a record with %d fields, wanted 4"
                % (path, len(parts)))
        tid = verbatim_diag.decode(parts[0])
        form = verbatim_diag.decode(parts[1])
        verdict = parts[2]
        message = verbatim_diag.decode(parts[3])
        out[(tid, form)] = (verdict, message)
    return out


def build():
    inv = json.load(open(os.path.join(HERE, "type_inventory2.json")))
    doc = {}
    doc["generated_by"] = "type_inventory3.py"
    doc["task"] = "TASK 45 (b) -- extracted AND declarable"
    doc["reads"] = ["type_inventory2.json",
                    "declare_raw/decl_<lang>.txt (the declaration lane's "
                    "own products, verbatim-escaped)"]
    doc["supersedes"] = (
        "type_inventory2.json for the purpose of CHOOSING PROBE HOLDERS. "
        "type_inventory2.json is left untouched on disk and remains the "
        "record of what each authority ADMITS.")
    doc["the_two_witnesses"] = {
        "extracted": "an authority names the spelling -- the compiler's "
                     "own type table, the grammar, the stdlib source, the "
                     "installed module interface. This is what inventory 2 "
                     "recorded, and it means the toolchain KNOWS the name.",
        "declarable_on_target": "a source file whose only content is a "
                                "declaration of that type COMPILED, in the "
                                "trickle container, at the probe lanes' own "
                                "flags. This means this target ACCEPTS the "
                                "name.",
    }
    doc["why_the_second_witness_exists"] = (
        "about 91,000 of the regeneration's 100,265 refusals are the "
        "compiler rejecting the probe's TYPE DECLARATION rather than its "
        "operator (round 9 correction 3). The inventory had been extracted "
        "as 'every type the compiler knows', not 'every type this target "
        "accepts'.")
    doc["deciding_form"] = (
        "the `parameter` form decides membership, because a probe holder "
        "IS a function parameter. The `variable` form is recorded beside "
        "it and disagreements are listed in "
        "`forms_disagree` and in type_demotions1.json. Every field holding "
        "the compiler's own words is named `refusal`, the name this line "
        "already uses for stored compiler testimony.")
    doc["spelling_ban"] = (
        "no operator token appears in any key, grouping, pairing or row "
        "structure here; the subject of this file is types")
    doc["pins_verified_in_container"] = {
        "container": "trickle-runner (the CPU-capped copy; Airlock's "
                     "sandbox-* containers untouched)",
        "banners_printed_by_the_lanes_themselves": {
            "c": "Ubuntu clang version 21.1.8 (6ubuntu1)",
            "cpp": "Ubuntu clang version 21.1.8 (6ubuntu1)",
            "go": "go version go1.26.0 linux/amd64",
            "rust": "rustc 1.96.1 (31fca3adb 2026-06-26)",
            "swift": "Swift version 6.0.3 (swift-6.0.3-RELEASE)",
        },
        "flags": {
            "c": "/usr/bin/clang -std=c17 -O0 -g -c",
            "cpp": "/usr/bin/clang++ -std=c++20 -O0 -g -c",
            "go": "go build -gcflags='-N -l'",
            "rust": "rustc --crate-type=lib --emit=obj -C opt-level=0 -g",
            "swift": "/persist/swift/usr/bin/swiftc -Onone -g -c",
        },
    }
    doc["pins_carried_from_inventory_2"] = inv["pins"]
    doc["languages"] = {}
    demotions = []
    disagreements = []
    totals = {"inventory2_entries": 0, "tested": 0, "kept": 0,
              "demoted_by_compiler": 0, "demoted_not_a_source_spelling": 0,
              "compilations": 0}
    for lang in LANGS:
        product = read_product(lang)
        kept = []
        record = {"witnesses": inv["languages"][lang]["witnesses"],
                  "counts_in_inventory_2": inv["languages"][lang]["counts"]}
        n_tested = 0
        n_demoted_c = 0
        n_demoted_ns = 0
        for entry in inv["languages"][lang]["types"]:
            spelling = entry["spelling"]
            tid = entry["id"]
            if "::" in spelling:
                n_demoted_ns = n_demoted_ns + 1
                demotions.append({
                    "language": lang, "id": tid, "spelling": spelling,
                    "cause": "not_a_source_spelling",
                    "detail": "a compiler-table identifier, not a spelling a "
                              "source file can carry; no declaration can be "
                              "written with it, so it was not compiled",
                    "refusal": None,
                })
                continue
            pv, pm = product[(tid, "parameter")]
            vv, vm = product[(tid, "variable")]
            n_tested = n_tested + 1
            row = dict(entry)
            row["declarable"] = {
                "witness": "declarable_on_target",
                "verdict": "ACCEPT" if pv == "ACCEPT" else "REFUSE",
                "deciding_form": "parameter",
                "parameter_form": {"verdict": pv, "refusal": pm},
                "variable_form": {"verdict": vv, "refusal": vm},
                "verification": "compiled_in_trickle_runner",
            }
            if pv != vv:
                disagreements.append({
                    "language": lang, "id": tid, "spelling": spelling,
                    "parameter_form": {"verdict": pv, "refusal": pm},
                    "variable_form": {"verdict": vv, "refusal": vm},
                })
            if pv == "ACCEPT":
                kept.append(row)
            else:
                n_demoted_c = n_demoted_c + 1
                demotions.append({
                    "language": lang, "id": tid, "spelling": spelling,
                    "cause": "compiler_refused_the_declaration",
                    "detail": "the parameter form did not compile at the "
                              "probe lanes' own flags",
                    "refusal": pm,
                    "variable_form": {"verdict": vv, "refusal": vm},
                })
        record["types"] = kept
        record["counts"] = {
            "inventory2_entries": len(inv["languages"][lang]["types"]),
            "tested_by_declaration": n_tested,
            "declarable_kept": len(kept),
            "demoted_by_compiler": n_demoted_c,
            "demoted_not_a_source_spelling": n_demoted_ns,
            "compilations_run": n_tested * 2,
        }
        doc["languages"][lang] = record
        totals["inventory2_entries"] += len(inv["languages"][lang]["types"])
        totals["tested"] += n_tested
        totals["kept"] += len(kept)
        totals["demoted_by_compiler"] += n_demoted_c
        totals["demoted_not_a_source_spelling"] += n_demoted_ns
        totals["compilations"] += n_tested * 2
    doc["totals"] = totals
    doc["forms_disagree"] = disagreements

    dem = {}
    dem["generated_by"] = "type_inventory3.py"
    dem["population"] = (
        "every type_inventory2.json entry that is NOT in "
        "type_inventory3.json, with the compiler's own words where the "
        "compiler is the reason")
    dem["counts"] = {
        "demoted_by_compiler": totals["demoted_by_compiler"],
        "demoted_not_a_source_spelling":
            totals["demoted_not_a_source_spelling"],
        "total": len(demotions),
    }
    dem["spelling_ban"] = doc["spelling_ban"]
    dem["demotions"] = demotions
    dem["forms_disagree"] = disagreements
    return doc, dem


def write(name, obj):
    path = os.path.join(HERE, name)
    fh = open(path, "w")
    json.dump(obj, fh, indent=1)
    fh.write("\n")
    fh.close()
    return path


def guard(paths):
    cmd = [sys.executable, os.path.join(HERE, "check_no_spelling_keys.py")]
    cmd.extend(paths)
    done = subprocess.run(cmd, capture_output=True, text=True)
    print(done.stdout.strip())
    if done.returncode != 0:
        print(done.stderr.strip())
        for path in paths:
            if os.path.exists(path):
                os.remove(path)
        raise SystemExit("REFUSED OWN OUTPUT: spelling guard failed")


def main():
    doc, dem = build()
    p1 = write("type_inventory3.json", doc)
    p2 = write("type_demotions1.json", dem)
    t = doc["totals"]
    print("%-6s %10s %8s %8s %10s %10s"
          % ("lang", "inv2", "tested", "kept", "demoted_c", "demoted_ns"))
    for lang in LANGS:
        c = doc["languages"][lang]["counts"]
        print("%-6s %10d %8d %8d %10d %10d"
              % (lang, c["inventory2_entries"], c["tested_by_declaration"],
                 c["declarable_kept"], c["demoted_by_compiler"],
                 c["demoted_not_a_source_spelling"]))
    print("%-6s %10d %8d %8d %10d %10d"
          % ("TOTAL", t["inventory2_entries"], t["tested"], t["kept"],
             t["demoted_by_compiler"], t["demoted_not_a_source_spelling"]))
    print("compilations run: %d" % t["compilations"])
    print("forms disagree on %d types" % len(doc["forms_disagree"]))
    for row in doc["forms_disagree"]:
        print("  %s %s  parameter=%s variable=%s"
              % (row["language"], row["spelling"],
                 row["parameter_form"]["verdict"],
                 row["variable_form"]["verdict"]))
    print("wrote %s" % p1)
    print("wrote %s" % p2)
    guard([p1, p2])


if __name__ == "__main__":
    main()
