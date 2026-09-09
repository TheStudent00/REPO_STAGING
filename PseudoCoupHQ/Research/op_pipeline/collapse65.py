#!/usr/bin/env python3
"""collapse65.py -- the layer-5 / layer-3 collapse per arrival
population, with task 66's rendered-text collapse beside it.

WHAT "COLLAPSE" MEANS HERE, said before any figure.  A population of
units prints some number of DISTINCT TEXTS at each layer.  Layer 3 is
the wrapped runnable text -- the record; layer 5 is the normalized term
-- the key computed beside it, and only for a unit whose term the gate
PROVED.  The ratio of units to distinct texts is how far each layer
collapses the population.  The two are counted over the SAME units, so
the comparison is between layers and not between populations:

  layer 3 is counted over the units that have a layer-5 text, and
  again over the whole population, and both are printed, because the
  two answer different questions and quoting one for the other is how
  a figure gets misread.

Task 66's rendered text is the RETURN PATH -- a proved term rendered
back into arch text -- and it is available only for the units task 66
reached.  It is counted over exactly those units, with the population
stated on the line.

WRITES:
  collapse65.json
  collapse65_printed.txt

Coding discipline: no compound one-liner statements.

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

No operator token appears in this file.
"""

import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

LINES = []

POPULATIONS = ["original", "interpreter", "regenerated"]


def log(text):
    LINES.append(text)
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def read_store(store):
    out = {}
    pattern = os.path.join(HERE, store, "*.json")
    for path in sorted(glob.glob(pattern)):
        document = json.load(open(path))
        for name in document["units"]:
            out[name] = document["units"][name]
    return out


def wrapped_texts():
    """unit -> its layer-3 wrapped text, read off the POOL, which is
    where the text this round grouped on actually lives."""
    document = json.load(open(os.path.join(HERE, "the_pool5.json")))
    out = {}
    for entry in document["entries"]:
        for member in entry["members"]:
            out[member["unit"]] = member["wrapped_text"]
    return out


def rendered_texts():
    """unit -> the arch text task 66 rendered back from its proved
    term, for the units task 66 reached."""
    out = {}
    pattern = os.path.join(HERE, "render_back_store", "*.json")
    for path in sorted(glob.glob(pattern)):
        document = json.load(open(path))
        for name in document.get("units", {}):
            record = document["units"][name]
            if not record.get("rendered"):
                continue
            text = record.get("rendered_wrapped_text")
            if not text:
                continue
            out[name] = text
    return out


def ratio(units, texts):
    if texts == 0:
        return 0.0
    return float(units) / float(texts)


def main():
    terms = read_store("term65_store")
    layer3 = wrapped_texts()
    rendered = rendered_texts()

    log("-- the populations, and what each layer is counted over")
    log("   units in term65_store                       %d"
        % len(terms))
    log("   units carrying a layer-3 wrapped text       %d"
        % len(layer3))
    log("   units task 66 rendered back                 %d"
        % len(rendered))

    rows = []
    for population in POPULATIONS + ["ALL"]:
        members = []
        for name in terms:
            record = terms[name]
            if population != "ALL":
                if record.get("population") != population:
                    continue
            members.append(name)
        proved = []
        for name in members:
            if terms[name].get("layer5_normalized_text"):
                proved.append(name)
        l5 = set()
        for name in proved:
            l5.add(terms[name]["layer5_normalized_text"])
        l3_over_proved = set()
        for name in proved:
            if name in layer3:
                l3_over_proved.add(layer3[name])
        l3_over_all = set()
        for name in members:
            if name in layer3:
                l3_over_all.add(layer3[name])
        here = []
        for name in proved:
            if name in rendered:
                here.append(name)
        rendered_set = set()
        for name in here:
            rendered_set.add(rendered[name])
        rendered_l3 = set()
        rendered_l5 = set()
        for name in here:
            if name in layer3:
                rendered_l3.add(layer3[name])
            rendered_l5.add(terms[name]["layer5_normalized_text"])
        rows.append({
            "population": population,
            "units": len(members),
            "units_with_a_proved_layer5_text": len(proved),
            "distinct_layer5_texts": len(l5),
            "distinct_layer3_texts_over_those_units": len(l3_over_proved),
            "distinct_layer3_texts_over_the_whole_population":
                len(l3_over_all),
            "units_rendered_back_by_task_66": len(here),
            "distinct_rendered_texts": len(rendered_set),
            "distinct_layer3_texts_over_the_rendered_units":
                len(rendered_l3),
            "distinct_layer5_texts_over_the_rendered_units":
                len(rendered_l5),
        })

    log("")
    log("-- THE COLLAPSE, over the units that HAVE a layer-5 text")
    log("   %-12s %8s %8s %8s %8s %7s %7s"
        % ("population", "units", "L5 text", "L3 text", "L3 all",
           "L5 x", "L3 x"))
    for row in rows:
        log("   %-12s %8d %8d %8d %8d %7.1f %7.1f"
            % (row["population"],
               row["units_with_a_proved_layer5_text"],
               row["distinct_layer5_texts"],
               row["distinct_layer3_texts_over_those_units"],
               row["distinct_layer3_texts_over_the_whole_population"],
               ratio(row["units_with_a_proved_layer5_text"],
                     row["distinct_layer5_texts"]),
               ratio(row["units_with_a_proved_layer5_text"],
                     row["distinct_layer3_texts_over_those_units"])))
    log("")
    log("   'units'   the units of that population with a proved "
        "layer-5 text")
    log("   'L5 text' distinct normalized terms those units print")
    log("   'L3 text' distinct wrapped texts THOSE SAME units carry")
    log("   'L3 all'  distinct wrapped texts over the population "
        "entire, proved or not")
    log("   'L5 x'/'L3 x'  units per distinct text -- how far each "
        "layer collapses")

    log("")
    log("-- TASK 66's RENDERED TEXT, beside them, over the units it "
        "reached")
    log("   %-12s %8s %8s %8s %8s %7s"
        % ("population", "units", "render", "L5 text", "L3 text",
           "R x"))
    for row in rows:
        log("   %-12s %8d %8d %8d %8d %7.1f"
            % (row["population"],
               row["units_rendered_back_by_task_66"],
               row["distinct_rendered_texts"],
               row["distinct_layer5_texts_over_the_rendered_units"],
               row["distinct_layer3_texts_over_the_rendered_units"],
               ratio(row["units_rendered_back_by_task_66"],
                     row["distinct_rendered_texts"])))
    log("")
    log("   The rendered population is NOT the proved population: task "
        "66 reached")
    log("   the units its own report names, and every figure on this "
        "block is")
    log("   counted over exactly those units, with their own layer-3 "
        "count beside")
    log("   them so the two are comparable.")

    document = {
        "meta": {
            "generated_by": "collapse65.py",
            "node": "hq.research.compiler_graph.term.normalize",
            "what_it_is": "the layer-5 and layer-3 collapse per "
                          "arrival population, with task 66's "
                          "rendered-text collapse beside it",
            "layer3_source": "the_pool5.json member wrapped_text",
            "layer5_source": "term65_store layer5_normalized_text -- "
                             "written only for a PROVED term",
            "rendered_source": "render_back_store/*.json -- task 66",
            "population_note": "every ratio names the units it is "
                               "counted over; the rendered population "
                               "is a subset of the proved population "
                               "and is never quoted as the whole",
        },
        "units_in_term65_store": len(terms),
        "units_with_a_layer3_text": len(layer3),
        "units_rendered_back_by_task_66": len(rendered),
        "rows": rows,
    }
    handle = open(os.path.join(HERE, "collapse65.json"), "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    handle = open(os.path.join(HERE, "collapse65_printed.txt"), "w")
    handle.write("\n".join(LINES) + "\n")
    handle.close()
    log("")
    log("-- wrote collapse65.json and collapse65_printed.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
