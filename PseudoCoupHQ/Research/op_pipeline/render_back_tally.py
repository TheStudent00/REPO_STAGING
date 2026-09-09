#!/usr/bin/env python3
"""render_back_tally.py -- the tally over POPULATION TWO: every proved
term of the whole corpus.

Every number here is COMPUTED from `render_back_store/` and pasted with
its population.  Refusals and non-proofs are grouped BY CAUSE, never by
sighting (LLM_communication_protocol section 5.3).

WHAT THE COLLAPSE COUNT IS.  Layer 3 is the unit's own machine code
wrapped; the rendered text is the layer-5 term made runnable, wrapped
into the same form.  The collapse is: how many DISTINCT rendered texts
the proved population carries, against how many distinct layer-3 texts
the same units carry.  A lower number is the simplifier's work becoming
visible in runnable text; it is measured, never a target.

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

No operator token appears in this file.  Nothing here is keyed,
grouped or paired on the `operator` display label.

Coding discipline: no compound one-liner statements.
"""

import glob
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STORE = os.path.join(HERE, "render_back_store")
OUT = os.path.join(HERE, "render_back_tally.json")
PRINTED = os.path.join(HERE, "render_back_tally_printed.txt")

CAP = 12
"""how many sightings a cause keeps as evidence.  The cause is the
item; the sightings are its evidence, and a handful of them is
evidence enough."""


def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def walk():
    counts = {
        "shards": 0,
        "units_with_a_proved_term": 0,
        "rendered": 0,
        "assembled_by_as": 0,
        "round_tripped_through_objdump": 0,
        "proved_on_ship": 0,
        "character_identical_to_layer_3": 0,
        "skipped_no_proved_term": 0,
    }
    refusal_causes = {}
    not_proved_causes = {}
    assembly_causes = {}
    rendered_texts = set()
    layer3_texts = set()
    by_language = {}
    for path in sorted(glob.glob(os.path.join(STORE, "*.json"))):
        document = json.load(open(path))
        counts["shards"] = counts["shards"] + 1
        counts["skipped_no_proved_term"] += document.get(
            "skipped_no_proved_term", 0)
        for name in sorted(document.get("units", {})):
            one = document["units"][name]
            counts["units_with_a_proved_term"] += 1
            lang = one.get("lang")
            by_language.setdefault(lang, {"units": 0, "rendered": 0,
                                          "proved": 0})
            by_language[lang]["units"] += 1
            layer3 = one.get("layer3_wrapped_text")
            if layer3 is not None:
                layer3_texts.add(digest(layer3))
            if not one.get("rendered"):
                cause = one.get("refusal_cause") or "unnamed"
                note(refusal_causes, cause, name, one.get("why"))
                continue
            counts["rendered"] += 1
            by_language[lang]["rendered"] += 1
            rendered_texts.add(digest(one["rendered_wrapped_text"]))
            if one.get("character_identical_to_layer_3"):
                counts["character_identical_to_layer_3"] += 1
            assembly = one.get("assembly") or {}
            if assembly.get("assembled"):
                counts["assembled_by_as"] += 1
            else:
                note(assembly_causes,
                     shorten(assembly.get("why")), name, None)
            if assembly.get("round_trips"):
                counts["round_tripped_through_objdump"] += 1
            if one.get("proved"):
                counts["proved_on_ship"] += 1
                by_language[lang]["proved"] += 1
                continue
            cause = one.get("not_proved_cause") or "unnamed"
            note(not_proved_causes, cause, name, None)
    counts["distinct_rendered_texts"] = len(rendered_texts)
    counts["distinct_layer_3_texts_over_the_same_units"] = \
        len(layer3_texts)
    return {
        "counts": counts,
        "refusal_causes": ordered(refusal_causes),
        "not_proved_causes": ordered(not_proved_causes),
        "assembly_causes": ordered(assembly_causes),
        "by_language": by_language,
    }


def shorten(why):
    if why is None:
        return "the assembler refused and said nothing this file read"
    return "%s" % why


def note(table, cause, unit, why):
    entry = table.get(cause)
    if entry is None:
        entry = {"cause": cause, "units": 0, "sightings": [],
                 "one_written_reason": why}
        table[cause] = entry
    entry["units"] += 1
    if len(entry["sightings"]) < CAP:
        entry["sightings"].append(unit)
    if entry["one_written_reason"] is None:
        entry["one_written_reason"] = why


def ordered(table):
    out = list(table.values())
    out.sort(key=lambda one: (-one["units"], one["cause"]))
    return out


def report(document):
    counts = document["counts"]
    population = counts["units_with_a_proved_term"]
    lines = []
    lines.append("render_back over POPULATION TWO: every proved term")
    lines.append("")
    lines.append("population, computed from render_back_store/ over "
                 "%d shards:" % counts["shards"])
    lines.append("  units with a proved layer-4 term   %d"
                 % population)
    lines.append("  canon39-proved units skipped for   %d"
                 % counts["skipped_no_proved_term"])
    lines.append("    having no proved term")
    lines.append("")
    lines.append("counts, each against the %d units with a proved "
                 "term:" % population)
    for key in ["rendered", "assembled_by_as",
                "round_tripped_through_objdump", "proved_on_ship",
                "character_identical_to_layer_3"]:
        lines.append("  %-38s %d" % (key, counts[key]))
    lines.append("")
    lines.append("the collapse, over the same %d units:" % population)
    lines.append("  distinct rendered texts            %d"
                 % counts["distinct_rendered_texts"])
    lines.append("  distinct layer-3 wrapped texts     %d"
                 % counts["distinct_layer_3_texts_over_the_same_units"])
    lines.append("")
    lines.append("per language, of the %d units with a proved term:"
                 % population)
    lines.append("  %-10s %8s %8s %8s" % ("language", "units",
                                          "rendered", "proved"))
    for lang in sorted(document["by_language"]):
        one = document["by_language"][lang]
        lines.append("  %-10s %8d %8d %8d"
                     % (lang, one["units"], one["rendered"],
                        one["proved"]))
    lines.append("")
    lines.append("REFUSED TO RENDER, by cause (%d causes):"
                 % len(document["refusal_causes"]))
    for entry in document["refusal_causes"]:
        lines.append("  %6d  %s" % (entry["units"], entry["cause"]))
        if entry["one_written_reason"]:
            lines.append("          one written reason: %s"
                         % entry["one_written_reason"][:200])
        lines.append("          sightings: %s"
                     % ", ".join(entry["sightings"][:6]))
    lines.append("")
    lines.append("RENDERED BUT NOT PROVED, by cause (%d causes):"
                 % len(document["not_proved_causes"]))
    if not document["not_proved_causes"]:
        lines.append("  none")
    for entry in document["not_proved_causes"]:
        lines.append("  %6d  %s" % (entry["units"], entry["cause"]))
        lines.append("          sightings: %s"
                     % ", ".join(entry["sightings"][:6]))
    lines.append("")
    lines.append("THE ASSEMBLER REFUSED, by cause (%d causes):"
                 % len(document["assembly_causes"]))
    if not document["assembly_causes"]:
        lines.append("  none")
    for entry in document["assembly_causes"]:
        lines.append("  %6d  %s" % (entry["units"],
                                    entry["cause"][:200]))
        lines.append("          sightings: %s"
                     % ", ".join(entry["sightings"][:6]))
    lines.append("")
    return "\n".join(lines) + "\n"


def main():
    document = walk()
    document["meta"] = {
        "produced_by": "render_back_tally.py",
        "read_from": "render_back_store/",
        "node": "hq.research.compiler_graph.term.render_back",
    }
    handle = open(OUT, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    printed = report(document)
    handle = open(PRINTED, "w")
    handle.write(printed)
    handle.close()
    sys.stdout.write(printed)


if __name__ == "__main__":
    main()
