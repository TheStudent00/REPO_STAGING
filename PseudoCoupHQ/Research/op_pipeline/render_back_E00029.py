#!/usr/bin/env python3
"""render_back_E00029.py -- the return path over POPULATION ONE: the
158 members of the pool entry `E00029`, whose one layer-5 normalized
text is `v0 + v1`.

Why this population first (log_166 TASK 66): it is the largest entry
whose members carry ONE normalized text across seven languages, so it
is the sharpest test of what a rendered text is.  Two things are
measured on it and neither is assumed: how many DISTINCT rendered texts
the 158 members produce, against how many distinct layer-3 wrapped
texts they carry; and the per-member gate verdict.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
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
line MUST paste this paragraph verbatim."

The members of this population come from the POOL -- machine-form
evidence -- and never from a token.

Coding discipline: no compound one-liner statements.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import render_back_run as RB                                     # noqa: E402

ENTRY = "E00029"
OUT = os.path.join(HERE, "render_back_E00029.json")
PRINTED = os.path.join(HERE, "render_back_E00029_printed.txt")


def members_of_the_entry():
    """the entry's member unit names, read off `the_pool4.json`."""
    document = json.load(open(os.path.join(HERE, "the_pool4.json")))
    for entry in document["entries"]:
        if entry["entry_id"] != ENTRY:
            continue
        out = []
        for member in entry["members"]:
            out.append(member["unit"])
        return out, entry
    raise SystemExit("the pool holds no entry %s" % ENTRY)


def index_of_units(wanted):
    """unit name -> (its canon39 record, its term-store record), built
    by walking the shards once."""
    units = {}
    terms = {}
    left = set(wanted)
    for path in RB.shards():
        if not left:
            break
        document = json.load(open(path))
        here = document.get("units", {})
        found = []
        for name in list(left):
            if name in here:
                found.append(name)
        if not found:
            continue
        proved = RB.proved_terms_of(path)
        for name in found:
            units[name] = here[name]
            terms[name] = proved.get(name)
            left.discard(name)
    return units, terms, sorted(left)


def main():
    wanted, entry = members_of_the_entry()
    units, terms, missing = index_of_units(wanted)
    maker, renderer, gate, form = RB.new_tools()
    assembler = RB.Assembler(form)
    records = {}
    for name in sorted(units):
        record = terms.get(name)
        if record is None:
            records[name] = {
                "unit": name,
                "rendered": False,
                "refusal_cause": "no proved term",
                "why": "this member's layer-4 term is not recorded "
                       "proved in the term store",
            }
            continue
        records[name] = RB.one_unit(maker, renderer, gate, name,
                                    units[name], record)
    rendered = []
    for name in sorted(records):
        text = records[name].get("rendered_wrapped_text")
        if text is None:
            continue
        rendered.append((name, text))
    said = assembler.run(rendered)
    for name in said:
        records[name]["assembly"] = said[name]
    summary = tally(records, entry, missing)
    document = {
        "entry_id": ENTRY,
        "population": "the %d members of pool entry %s"
                      % (len(wanted), ENTRY),
        "summary": summary,
        "units": records,
    }
    handle = open(OUT, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    printed = report(document, entry)
    handle = open(PRINTED, "w")
    handle.write(printed)
    handle.close()
    sys.stdout.write(printed)


def tally(records, entry, missing):
    rendered = 0
    assembled = 0
    round_tripped = 0
    proved = 0
    identical = 0
    causes = {}
    not_proved = {}
    texts = {}
    for name in sorted(records):
        one = records[name]
        if not one.get("rendered"):
            cause = one.get("refusal_cause") or "unnamed"
            causes.setdefault(cause, [])
            causes[cause].append(name)
            continue
        rendered = rendered + 1
        text = one["rendered_wrapped_text"]
        texts.setdefault(text, [])
        texts[text].append(name)
        if one.get("character_identical_to_layer_3"):
            identical = identical + 1
        assembly = one.get("assembly") or {}
        if assembly.get("assembled"):
            assembled = assembled + 1
        if assembly.get("round_trips"):
            round_tripped = round_tripped + 1
        if one.get("proved"):
            proved = proved + 1
            continue
        cause = one.get("not_proved_cause") or "unnamed"
        not_proved.setdefault(cause, [])
        not_proved[cause].append(name)
    layer3 = {}
    for name in sorted(records):
        text = records[name].get("layer3_wrapped_text")
        if text is None:
            continue
        layer3.setdefault(text, [])
        layer3[text].append(name)
    return {
        "members": len(records),
        "members_not_found_in_the_shards": missing,
        "rendered": rendered,
        "assembled_by_as": assembled,
        "round_tripped_through_objdump": round_tripped,
        "proved_on_ship": proved,
        "character_identical_to_layer_3": identical,
        "distinct_rendered_texts": len(texts),
        "distinct_layer_3_texts": len(layer3),
        "pool_recorded_distinct_layer_3_texts":
            entry["distinct_wrapped_text_count"],
        "pool_recorded_distinct_layer_5_texts":
            entry["distinct_layer5_text_count"],
        "refusal_causes": {key: len(value)
                           for key, value in causes.items()},
        "not_proved_causes": {key: len(value)
                              for key, value in not_proved.items()},
        "rendered_texts": {key: len(value)
                           for key, value in texts.items()},
    }


def report(document, entry):
    summary = document["summary"]
    lines = []
    lines.append("render_back over pool entry %s" % ENTRY)
    lines.append("population: %s" % document["population"])
    lines.append("")
    lines.append("LITERAL -- the entry's one layer-5 normalized text, "
                 "as `the_pool4.json` stores it:")
    for text in entry["layer5_normalized_texts"]:
        lines.append("    %s" % text)
    lines.append("")
    lines.append("LITERAL -- the distinct RENDERED wrapped texts, with "
                 "how many of the %d members carry each:"
                 % summary["members"])
    for text in sorted(summary["rendered_texts"]):
        lines.append("  [%d members]" % summary["rendered_texts"][text])
        lines.append("    %s" % text)
    lines.append("")
    lines.append("counts, each with its population of %d members:"
                 % summary["members"])
    for key in ["rendered", "assembled_by_as",
                "round_tripped_through_objdump", "proved_on_ship",
                "character_identical_to_layer_3",
                "distinct_rendered_texts", "distinct_layer_3_texts"]:
        lines.append("  %-34s %s" % (key, summary[key]))
    lines.append("")
    lines.append("refusals by cause:")
    if not summary["refusal_causes"]:
        lines.append("  none")
    for key in sorted(summary["refusal_causes"]):
        lines.append("  %-40s %d"
                     % (key, summary["refusal_causes"][key]))
    lines.append("")
    lines.append("rendered but not proved, by cause:")
    if not summary["not_proved_causes"]:
        lines.append("  none")
    for key in sorted(summary["not_proved_causes"]):
        lines.append("  %-40s %d"
                     % (key, summary["not_proved_causes"][key]))
    lines.append("")
    lines.append("per-member verdicts (display label carried, never "
                 "grouped on):")
    for name in sorted(document["units"]):
        one = document["units"][name]
        outcome = one.get("outcome")
        if outcome is None:
            outcome = "NOT_RENDERED"
        assembly = one.get("assembly") or {}
        lines.append("  %-26s %-18s assembled=%s identical_to_layer_3=%s"
                     % (name, outcome,
                        assembly.get("assembled"),
                        one.get("character_identical_to_layer_3")))
    lines.append("")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
