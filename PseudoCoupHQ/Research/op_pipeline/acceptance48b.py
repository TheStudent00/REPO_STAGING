#!/usr/bin/env python3
"""acceptance48.py -- the instances of task 48, printed verbatim.

  (a) ONE TRANSCRIPTION, LITERALLY: a real ledger, row by row, and the
      real term read off it from OUT-0 downward.
  (b) THE FLAG PAIR, LITERALLY: a unit whose answer comes from the pair
      (flag-setting opcode, flag-reading opcode), with the arch opcodes
      that produced it and the condition read off them.
  (c) LAYER 5 AS A NORMALIZER: two units with different bodies,
      different preludes and different layer-3 texts whose layer-5
      texts are character-identical.
  (d) LAYER 3 AGAINST LAYER 5: the computed breakdown, per population.

No operator token appears in this file.  THE SPELLING BAN is pasted in
census48.py, layer4.py, layer5.py, gate48.py, textwalk48.py and
guard48.py; this file writes no keys and groups nothing.
"""

import collections
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import layer4                                                     # noqa: E402
import layer5                                                     # noqa: E402
import gate48                                                     # noqa: E402
import textwalk48                                                 # noqa: E402


def wrapped(lang):
    return json.load(open(os.path.join(
        HERE, "canon37_wrapped_%s.json" % lang)))


def show_ledger(unit):
    print("    %-8s %-4s %-5s %-30s %-34s %s"
          % ("row", "off", "size", "type", "produced by", "operands"))
    for row in unit["ledger"]:
        producer = row["produced_by"]
        if isinstance(producer, list):
            producer = " + ".join(str(one) for one in producer)
        print("    %-8s %-4s %-5d %-30s %-34s %s"
              % (row["row"], hex(row["offset"]), row["size"],
                 row["type"], producer, ",".join(row["operands"])))


def show_unit(name, unit, heading):
    print("")
    print(heading)
    print("  LITERAL -- the body, as the compiler emitted it:")
    for line in unit["body_verbatim"]:
        print("    %s" % line)
    print("  LITERAL -- the provenance ledger (task 47's artifact):")
    show_ledger(unit)
    transcription = layer4.transcribe(unit)
    print("  LITERAL -- the term, read from OUT-0 downward:")
    print("    %s" % layer5.one_line(transcription.out_term))
    print("  LITERAL -- layer 5, the fixed-rule re-render:")
    print("    %s" % layer5.normalize(transcription.out_term))
    verdict, detail = gate48.gate(unit, transcription)
    print("  LITERAL -- the gate, route one (against the unit's own "
          "ship code, simulated):")
    print("    %s -- %s" % (verdict, detail))
    verdict, detail = textwalk48.gate(unit, transcription)
    print("  LITERAL -- the gate, route two (against the same body "
          "walked in text order):")
    print("    %s -- %s" % (verdict, detail))
    return transcription


def per_row_terms(unit):
    transcription = layer4.transcribe(unit)
    print("  LITERAL -- one term per row, in the ledger's own order:")
    for row in transcription.rows:
        term = transcription.terms.get(row["row"])
        if term is None:
            print("    %-8s (no term)" % row["row"])
            continue
        print("    %-8s = %s" % (row["row"], layer5.one_line(term)))


def documents():
    out = []
    for lang in ("c", "cpp", "go", "rust", "swift"):
        path = os.path.join(HERE, "layer4b_terms_%s.json" % lang)
        if os.path.exists(path):
            out.append(("original", path))
    path = os.path.join(HERE, "layer4b_interp.json")
    if os.path.exists(path):
        out.append(("interpreter", path))
    for path in sorted(glob.glob(os.path.join(HERE,
                                              "layer4b_regen_store",
                                              "*.json"))):
        out.append(("regenerated", path))
    return out


def layer_three_against_layer_five():
    print("")
    print("(d) LAYER 3 AGAINST LAYER 5 -- the computed breakdown, per "
          "population")
    per_population = collections.defaultdict(collections.Counter)
    distinct3 = collections.defaultdict(set)
    distinct5 = collections.defaultdict(set)
    for population, path in documents():
        document = json.load(open(path))
        for name, record in document["units"].items():
            counter = per_population[population]
            counter["units"] += 1
            if not record.get("term_built"):
                counter["no layer-5 text (no OUT-0 term)"] += 1
                continue
            counter["with a layer-5 text"] += 1
            if record.get("layer5_equals_layer3"):
                counter["layer 5 identical to layer 3, character for "
                        "character"] += 1
            else:
                counter["layer 5 differs from layer 3"] += 1
            distinct3[population].add(record.get("layer3_wrapped_text"))
            distinct5[population].add(
                record.get("layer5_normalized_text"))
    for population in sorted(per_population):
        print("  %s" % population)
        counter = per_population[population]
        for key in sorted(counter):
            print("    %-52s %d" % (key, counter[key]))
        print("    %-52s %d" % ("distinct layer-3 texts",
                                len(distinct3[population])))
        print("    %-52s %d" % ("distinct layer-5 texts",
                                len(distinct5[population])))
    print("")
    print("  GLOSS: layer 5 is never character-identical to layer 3, "
          "and cannot be: layer 3 is arch instructions and layer 5 is "
          "the term.  The number that carries the ruling's purpose is "
          "the pair beneath it -- how many distinct texts each layer "
          "has over the same units.  Layer 5 collapses units that "
          "layer 3 keeps apart, which is what a textual normalizer is "
          "for.")


def main():
    documents_c = wrapped("c")
    documents_go = wrapped("go")
    print("=" * 72)
    print("(a) ONE TRANSCRIPTION, LITERALLY")
    unit = documents_c["units"]["c/op_104"]
    show_unit("c/op_104", unit, "  UNIT c/op_104")
    per_row_terms(unit)
    print("")
    print("=" * 72)
    print("(b) THE FLAG PAIR, LITERALLY -- the producer is the pair "
          "(flag-setting arch opcode, flag-reading arch opcode)")
    unit = documents_c["units"]["c/op_0"]
    show_unit("c/op_0", unit, "  UNIT c/op_0")
    per_row_terms(unit)
    print("")
    print("=" * 72)
    print("(c) LAYER 5 AS A NORMALIZER -- two units, two bodies, two "
          "preludes, one normalized text")
    left = documents_c["units"]["c/op_109"]
    right = documents_go["units"]["go/op_319"]
    for name, unit in (("c/op_109", left), ("go/op_319", right)):
        print("")
        print("  %s" % name)
        print("    LITERAL -- body:      %s" % unit["body_text"])
        print("    LITERAL -- layer 3:   %s" % unit["wrapped_text"])
        transcription = layer4.transcribe(unit)
        print("    LITERAL -- layer 5:   %s"
              % layer5.normalize(transcription.out_term))
    one = layer5.normalize(layer4.transcribe(left).out_term)
    two = layer5.normalize(layer4.transcribe(right).out_term)
    print("")
    print("  layer 3 texts identical: %s"
          % (left["wrapped_text"] == right["wrapped_text"]))
    print("  layer 5 texts identical: %s" % (one == two))
    layer_three_against_layer_five()


if __name__ == "__main__":
    main()
