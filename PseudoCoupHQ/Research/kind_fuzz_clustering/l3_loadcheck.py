#!/usr/bin/env python3
"""l3_loadcheck.py -- classify every `split` cell in every value matrix.

HARVEST.md states the question this file answers.  A `split` cell is one
where a statically checked language's verdict moved with the VALUE rather
than with the holder pair.  There are two very different reasons that can
happen and they must not be reported as one number:

  * LAYER 2 LEAKING IN -- the holder could not hold that value at all
    (`short v = 9223372036854775807;`).  The operation never got a
    chance to be judged.  This is not a fact about layer 3.
  * LAYER 3 MOVING -- every value involved loads into its holder
    perfectly well, and the operation is still refused for one value and
    accepted for another.  This is the finding proper.

The separator is the `ld_<lang>_00.sh` lanes: 1,046 probes over the nine
statically checked languages, each carrying a holder's DECLARATION ALONE
-- no second operand, no operation.  A declaration that refuses on its
own cannot be blamed on the operator.

Identifier grammar for a load-check probe is `P{i}_{i}_{x}_{x}_0`:
holder i, value class x, declared and nothing else.

Per-cell classification, stated so it is checkable:

  * `layer2_only`  -- the cell has refusing value pairs, and EVERY one of
    them has at least one side whose declaration alone also refuses
  * `layer3_moving`-- at least one refusing value pair in which BOTH
    sides' declarations load perfectly well
  * `mixed`        -- both of the above are present in the one cell
  * `unclassified` -- the load check has no verdict for a side (recorded
    rather than guessed)

The value-level acceptance split that the CORE cares about is
`layer3_moving` plus the layer-3 half of `mixed`.  log 024 decision 3 is
the territory: a value that merely failed to load into its holder is a
layer-2 fact wearing a layer-3 costume.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
STATIC = ["go", "rust", "cpp", "swift", "dart", "csharp", "kotlin",
          "java", "typescript"]


def read_loadcheck(lang):
    """raw/ld_<lang>_00.txt -> {(holder index, value class index): verdict}."""
    p = os.path.join(RAW, "ld_%s_00.txt" % lang)
    if not os.path.exists(p):
        return None, "no load-check file"
    tab, summary = {}, False
    for line in open(p, errors="replace"):
        line = line.strip()
        if line.startswith("__SUMMARY__"):
            summary = True
            continue
        f = line.split("|")
        if len(f) < 2 or not f[0].startswith("P"):
            continue
        try:
            i, j, x, y, k = (int(v) for v in f[0][1:].split("_"))
        except ValueError:
            continue
        # a load check declares ONE holder; the generator emits it in the
        # diagonal shape, and anything off-diagonal would mean the lane
        # was built from the wrong plan
        if i != j or x != y:
            continue
        tab[(i, x)] = f[1]
    if not summary:
        return None, "no __SUMMARY__ line: lane did not finish"
    return tab, "ok"


def classify(lang, ld):
    """walk valuematrix_<lang>.json's split cells against the load check."""
    vm = json.load(open(os.path.join(HERE, "valuematrix_%s.json" % lang)))
    if not vm.get("complete"):
        return dict(language=lang, admitted=False,
                    reason="value matrix gate refused: %s"
                           % vm.get("completeness"))
    space = json.load(open(os.path.join(HERE, "space_%s.json" % lang)))
    # value class NAME -> index, per holder.  Verified duplicate-free.
    vcidx = [{n: x for x, n in enumerate(h["value_classes"])}
             for h in space["holders"]]

    counts = dict(layer2_only=0, layer3_moving=0, mixed=0, unclassified=0)
    per_op = {}
    examples = dict(layer2_only=[], layer3_moving=[], mixed=[])
    for key, c in vm["cells"].items():
        if c["shape"] != "split":
            continue
        i, j = (int(v) for v in key.rsplit("|", 2)[1:])
        l2 = l3 = unk = 0
        ex2 = ex3 = None
        for e in c["by_value_class"]:
            if e["verdict"] == "ACCEPT":
                continue
            x = vcidx[i].get(e["lhs_value_class"])
            y = vcidx[j].get(e["rhs_value_class"])
            va = ld.get((i, x)) if x is not None else None
            vb = ld.get((j, y)) if y is not None else None
            if va is None or vb is None:
                unk += 1
                continue
            if va == "REFUSE" or vb == "REFUSE":
                l2 += 1
                ex2 = ex2 or (e, va, vb)
            else:
                l3 += 1
                ex3 = ex3 or (e, va, vb)
        if l2 and l3:
            k = "mixed"
        elif l3:
            k = "layer3_moving"
        elif l2:
            k = "layer2_only"
        else:
            k = "unclassified"
        counts[k] += 1
        per_op.setdefault(c["operation"], dict(
            layer2_only=0, layer3_moving=0, mixed=0, unclassified=0))
        per_op[c["operation"]][k] += 1
        if k in examples and len(examples[k]) < 4:
            e, va, vb = (ex3 or ex2)
            examples[k].append(dict(
                cell=key, operation=c["operation"],
                lhs="%s (%s)" % (c["lhs"]["holder"], c["lhs"]["form"]),
                rhs="%s (%s)" % (c["rhs"]["holder"], c["rhs"]["form"]),
                refusing_value_pair="%s | %s"
                    % (e["lhs_value_class"], e["rhs_value_class"]),
                lhs_declaration_alone=va, rhs_declaration_alone=vb))

    tot = sum(counts.values())
    ldref = sum(1 for v in ld.values() if v == "REFUSE")
    return dict(language=lang, admitted=True,
                load_check_probes=len(ld), load_check_refusals=ldref,
                split_cells=vm["split_cells"], classified=tot,
                counts=counts, by_operation=per_op, examples=examples,
                value_level_splits=counts["layer3_moving"] + counts["mixed"],
                layer2_leak_splits=counts["layer2_only"])


def main():
    out, rows = {}, []
    print("| language | ld probes | ld refusals | split cells | layer 3 "
          "moving | mixed | layer 2 only | unclassified |")
    print("|---|---|---|---|---|---|---|---|")
    for lang in STATIC:
        ld, why = read_loadcheck(lang)
        if ld is None:
            out[lang] = dict(language=lang, admitted=False, reason=why)
            print("| %s | -- | -- | -- | -- | -- | -- | REFUSED: %s |"
                  % (lang, why))
            continue
        r = classify(lang, ld)
        out[lang] = r
        if not r["admitted"]:
            print("| %s | %d | -- | -- | -- | -- | -- | REFUSED: %s |"
                  % (lang, len(ld), r["reason"]))
            continue
        c = r["counts"]
        print("| %s | %d | %d | %d | %d | %d | %d | %d |"
              % (lang, r["load_check_probes"], r["load_check_refusals"],
                 r["split_cells"], c["layer3_moving"], c["mixed"],
                 c["layer2_only"], c["unclassified"]))
        rows.append(r)
    tot = dict(layer2_only=0, layer3_moving=0, mixed=0, unclassified=0)
    for r in rows:
        for k in tot:
            tot[k] += r["counts"][k]
    print("| **all nine** | %d | %d | %d | %d | %d | %d | %d |"
          % (sum(r["load_check_probes"] for r in rows),
             sum(r["load_check_refusals"] for r in rows),
             sum(r["split_cells"] for r in rows),
             tot["layer3_moving"], tot["mixed"], tot["layer2_only"],
             tot["unclassified"]))
    json.dump(dict(built=__doc__.splitlines()[0], per_language=out,
                   totals=tot),
              open(os.path.join(HERE, "loadcheck_classified.json"), "w"),
              indent=1)
    print("\nwrote loadcheck_classified.json")
    return out


if __name__ == "__main__":
    main()
