#!/usr/bin/env python3
"""construct_report.py -- `construct.md`: what the second tier did, per
target, by schema, and what it did not do and why.

Node: hq.research.arch_unit_oracle.cross_construction.autopoly.
Brief: `PRIVATE/PseudoCoupHQ/Research/briefs/task_t2_brief.md`.

Every table here is read off two files and nothing else: the pass's own
run store (`t2_construct_runs.jsonl`) and the bank
(`autopoly/certificates.jsonl`).  Both are STREAMED; neither is held
whole.

Coding discipline: no compound one-liner statements.
"""

import collections
import json
import os
import resource
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EMULATION = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(EMULATION, "handful"))
sys.path.insert(0, os.path.join(EMULATION, "autopoly"))

import schemas as S                                              # noqa: E402

COMPILED = ("c", "cpp", "rust", "go", "swift")
MARKS = ["has no ", "is not spelled by this renderer",
         "a width c has no holder for",
         "answer home or arrival on the x87 stack",
         "operator not covered by the renderer"]
BANK = os.path.join(EMULATION, "autopoly", "certificates.jsonl")
RUNS = os.path.join(EMULATION, "autopoly",
                    "t2_construct_runs.jsonl")
REPORT = os.path.join(HERE, "construct.md")
LEMMAS = os.path.join(HERE, "lean", "lemmas_t2.json")


def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def stream(path):
    if not os.path.exists(path):
        return
    handle = open(path)
    for line in handle:
        text = line.strip()
        if not text:
            continue
        yield json.loads(text)
        continue
    handle.close()
    return


def is_a_hole(cause):
    for mark in MARKS:
        if mark in (cause or ""):
            return True
        continue
    return False


def gather():
    """everything the report needs, in one pass over each file."""
    out = {
        "before": collections.Counter(),
        "before_cells": collections.defaultdict(set),
        "after_kind": collections.Counter(),
        "constructed_certificates": collections.Counter(),
        "by_schema": collections.Counter(),
        "by_schema_proved": collections.Counter(),
        "proof_forms": collections.Counter(),
        "landing": collections.Counter(),
        "declines": collections.Counter(),
        "rows": [],
        "sat_points": [],
        "both": [],
        "certified_pairs_before": set(),
    }
    for cert in stream(BANK):
        if not cert.get("preferred"):
            continue
        if cert["target"] not in COMPILED:
            continue
        if cert.get("route") == "constructed":
            out["constructed_certificates"][cert["kind"]] += 1
            continue
        if cert["kind"] != "refused":
            continue
        if not is_a_hole(cert.get("cause")):
            continue
        out["before"][cert["target"]] += 1
        out["before_cells"][cert["target"]].add(
            (cert["cell"]["mnem"], cert["cell"]["shape"],
             cert["cell"]["key_width"]))
        continue
    native = {}
    for run in stream(RUNS):
        key = (run["mnem"], run["shape"], run["key_width"], run["lang"])
        if run.get("route") != "constructed":
            for place in run.get("places") or []:
                check = place.get("check") or {}
                native[(key, place.get("writes"))] = {
                    "outcome": check.get("outcome"),
                    "instructions": len((place.get("body_text")
                                         or "").split("; "))
                    if place.get("body_text") else None,
                }
                continue
            continue
        for place in run.get("places") or []:
            block = place.get("constructed") or {}
            equality = block.get("equality") or {}
            check = place.get("check") or {}
            gate = place.get("gate_on_the_constructed_mapping") or {}
            row = {
                "target": run["lang"],
                "mnem": run["mnem"],
                "shape": run["shape"],
                "key_width": run["key_width"],
                "place": place.get("writes"),
                "schemas": block.get("schemas") or [],
                "word_bits": block.get("word_bits"),
                "instructions": block.get("instructions"),
                "landing": (place.get("landing") or {}).get("verdict"),
                "gate": check.get("outcome") or gate.get("outcome"),
                "equality": equality.get("outcome"),
                "proof": equality.get("proof"),
                "equality_seconds": equality.get("seconds"),
                "refusal_cause": place.get("refusal_cause"),
                "unfolded": block.get("unfolded_nodes"),
            }
            if not block.get("schemas"):
                out["declines"][place.get("refusal_cause")
                                or "no cause"] += 1
                continue
            out["rows"].append(row)
            name = ", ".join(row["schemas"])
            out["by_schema"][name] += 1
            if row["gate"] == "PROVED_ON_SHIP" and row["proof"]:
                out["by_schema_proved"][name] += 1
                out["proof_forms"][row["proof"]] += 1
                out["landing"][row["landing"]] += 1
                if row["proof"] == "sat":
                    out["sat_points"].append(row)
                continue
            continue
        continue
    return out, native


def both_routes(rows, native):
    """the places BOTH routes reached with a proof, and which carved the
    smaller body -- the brief's tie-break, measured rather than
    assumed."""
    out = []
    for row in rows:
        key = ((row["mnem"], row["shape"], row["key_width"],
                row["target"]), row["place"])
        held = native.get(key)
        if held is None:
            continue
        if held.get("outcome") != "PROVED_ON_SHIP":
            continue
        if row["gate"] != "PROVED_ON_SHIP":
            continue
        out.append((row, held))
        continue
    return out


def lemma_rows():
    if not os.path.exists(LEMMAS):
        return []
    handle = open(LEMMAS)
    document = json.load(handle)
    handle.close()
    return document.get("rows") or []


def say(handle, text):
    handle.write(text + "\n")
    return


def main(argv):
    held, native = gather()
    rows = held["rows"]
    handle = open(REPORT, "w")
    say(handle, "# construct.md -- the second tier, per target and by "
                "schema")
    say(handle, "")
    say(handle, "Written by `construct/construct_report.py` off the "
                "pass's own run store and the bank; nothing here is "
                "typed in.")
    say(handle, "")
    say(handle, "## 1. Refused by nature BEFORE, constructed AFTER")
    say(handle, "")
    say(handle, "| target | width-or-kind refusals the bank held | "
                "distinct cells | places the tier constructed | of "
                "them proved end to end |")
    say(handle, "|---|---|---|---|---|")
    per_target = collections.Counter()
    per_target_proved = collections.Counter()
    for row in rows:
        per_target[row["target"]] += 1
        if row["gate"] == "PROVED_ON_SHIP" and row["proof"]:
            per_target_proved[row["target"]] += 1
        continue
    for target in COMPILED:
        say(handle, "| %s | %d | %d | %d | %d |"
            % (target, held["before"][target],
               len(held["before_cells"][target]), per_target[target],
               per_target_proved[target]))
        continue
    say(handle, "| **all five** | **%d** | **%d** | **%d** | **%d** |"
        % (sum(held["before"].values()),
           len(set().union(*held["before_cells"].values())
               if held["before_cells"] else set()),
           sum(per_target.values()), sum(per_target_proved.values())))
    say(handle, "")
    say(handle, "## 2. By schema")
    say(handle, "")
    say(handle, "| the schemas the lowering used | places | proved end "
                "to end |")
    say(handle, "|---|---|---|")
    for name in sorted(held["by_schema"],
                       key=lambda k: -held["by_schema"][k]):
        say(handle, "| %s | %d | %d |"
            % (name, held["by_schema"][name],
               held["by_schema_proved"][name]))
        continue
    say(handle, "")
    say(handle, "## 3. The three proof forms")
    say(handle, "")
    say(handle, "| form | places |")
    say(handle, "|---|---|")
    for form in ("canonical", "lemma+gate", "sat"):
        say(handle, "| `%s` | %d |" % (form, held["proof_forms"][form]))
        continue
    say(handle, "")
    say(handle, "## 4. The collapse column")
    say(handle, "")
    say(handle, "| the compiler's landing | places |")
    say(handle, "|---|---|")
    for landing in sorted(held["landing"],
                          key=lambda k: -held["landing"][k]):
        say(handle, "| %s | %d |" % (landing, held["landing"][landing]))
        continue
    say(handle, "")
    say(handle, "## 5. Every constructed place, one row each")
    say(handle, "")
    say(handle, "| target | `mnem` | shape | `key_width` | place | "
                "schemas | word | gate | equality | proof | "
                "instructions | landing |")
    say(handle, "|---|---|---|---|---|---|---|---|---|---|---|---|")
    for row in sorted(rows, key=lambda r: (r["target"], r["mnem"],
                                           r["shape"], r["key_width"],
                                           r["place"] or "")):
        say(handle, "| %s | `%s` | %s | %s | %s | %s | %s | %s | %s | "
                    "%s | %s | %s |"
            % (row["target"], row["mnem"], row["shape"],
               row["key_width"], row["place"],
               ", ".join(row["schemas"]), row["word_bits"],
               row["gate"] or (row["refusal_cause"] or "")[:40],
               row["equality"], row["proof"], row["instructions"],
               row["landing"]))
        continue
    say(handle, "")
    say(handle, "## 6. Where the tier declined, by cause")
    say(handle, "")
    say(handle, "| the cause, LITERAL | places |")
    say(handle, "|---|---|")
    for cause in sorted(held["declines"],
                        key=lambda k: -held["declines"][k]):
        say(handle, "| %s | %d |" % (str(cause).replace("|", "/"),
                                     held["declines"][cause]))
        continue
    say(handle, "")
    say(handle, "## 7. Both routes on one place")
    say(handle, "")
    pairs = both_routes(rows, native)
    say(handle, "places both routes proved: %d" % len(pairs))
    if pairs:
        say(handle, "")
        say(handle, "| target | `mnem` | shape | `key_width` | place | "
                    "the native body | the constructed body | the "
                    "smaller |")
        say(handle, "|---|---|---|---|---|---|---|---|")
        for row, other in pairs:
            smaller = "the constructed"
            if (other.get("instructions") or 0) <= (row["instructions"]
                                                    or 0):
                smaller = "the native"
            say(handle, "| %s | `%s` | %s | %s | %s | %s | %s | %s |"
                % (row["target"], row["mnem"], row["shape"],
                   row["key_width"], row["place"],
                   other.get("instructions"), row["instructions"],
                   smaller))
            continue
    say(handle, "")
    say(handle, "## 8. Every `sat`, with its point")
    say(handle, "")
    say(handle, "| target | `mnem` | shape | `key_width` | place | "
                "schemas | the equality's seconds |")
    say(handle, "|---|---|---|---|---|---|---|")
    for row in held["sat_points"]:
        say(handle, "| %s | `%s` | %s | %s | %s | %s | %s |"
            % (row["target"], row["mnem"], row["shape"],
               row["key_width"], row["place"],
               ", ".join(row["schemas"]), row["equality_seconds"]))
        continue
    say(handle, "")
    say(handle, "## 9. The lemmas")
    say(handle, "")
    say(handle, "| schema | width | word | the shape | the shape's "
                "row | limbs |")
    say(handle, "|---|---|---|---|---|---|")
    for row in lemma_rows():
        pieces = []
        for one in row.get("limbs") or []:
            pieces.append("%s %s" % (one["limb"], one["outcome"]))
            continue
        say(handle, "| %s | %s | %s | `%s` | %s | %s |"
            % (row["schema"], row["width"], row["word"], row["shape"],
               row["outcome"], "; ".join(pieces)))
        continue
    say(handle, "")
    say(handle, "## 10. The certificates the bank now holds on the "
                "constructed route")
    say(handle, "")
    say(handle, "| kind | certificates |")
    say(handle, "|---|---|")
    for kind in sorted(held["constructed_certificates"]):
        say(handle, "| `%s` | %d |"
            % (kind, held["constructed_certificates"][kind]))
        continue
    say(handle, "")
    say(handle, "peak resident while writing this: %d kB" % peak_kb())
    handle.close()
    sys.stdout.write("%s written\n" % REPORT)
    sys.stdout.write("peak resident: %d kB\n" % peak_kb())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
