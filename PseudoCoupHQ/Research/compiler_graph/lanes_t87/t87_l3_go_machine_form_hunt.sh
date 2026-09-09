#!/usr/bin/env bash
# t87 lane 3 — SURVEY ONLY. Lane 2 found that only 107 of go's 590
# diaried probes carry a machine form in canon39/40_wrapped_go.json.
# Before the go population of the third connection kind is fixed at
# 107, every other artifact on disk that might carry a go unit's own
# emitted body is checked. A frontier is only honest once the search
# for the missing evidence has been run and reported.
#
# THE SPELLING BAN, ABSOLUTE (the owner, 2026-08-25). No operator token in any
# key, grouping, pairing, row structure, candidate selection or
# comparison scope. Nothing here reads an operator field.
set -u
say() { echo; echo "======== $* ========"; }
cd PseudoCoupHQ/Research/op_pipeline

say "[1/3] every artifact that might carry a go unit body, counted"
python3 - <<'PY'
import json, os
stems = sorted(n[:-4] for n in os.listdir(
    'PseudoCoupHQ/Research/compiler_graph/diaries/go')
    if n.endswith('.txt'))
want = set("go/%s" % s for s in stems)
want_bare = set(s.replace("op_", "") for s in stems)
HERE = 'PseudoCoupHQ/Research/op_pipeline/'
for name in ("canon23_units_go.json", "canon4_units_go.json",
             "tree_units3.json", "tree_units4.json",
             "tree_units_extended.json", "probe_manifest2_go.json"):
    path = HERE + name
    if not os.path.exists(path):
        print("   %-28s ABSENT" % name); continue
    size = os.path.getsize(path)
    try:
        doc = json.load(open(path))
    except Exception as problem:
        print("   %-28s unreadable: %s" % (name, problem)); continue
    if not isinstance(doc, dict):
        print("   %-28s top-level is %s" % (name, type(doc).__name__)); continue
    print("   %-28s %8d bytes  top-level %s" % (name, size, sorted(doc)[:8]))
    units = doc.get("units")
    if isinstance(units, dict):
        keys = sorted(units)
        one = units[keys[0]] if keys else {}
        fields = sorted(one) if isinstance(one, dict) else []
        bodyish = [f for f in fields
                   if f in ("body_bytes", "body_text", "body_as_read",
                            "body", "bytes", "text", "disasm", "insns")]
        go_ids = [k for k in keys if str(k).startswith("go/")]
        print("        units %6d   go/ ids %5d   join to the 590 stems %5d"
              % (len(units), len(go_ids), len(want & set(keys))))
        print("        body-ish fields present: %s" % (bodyish or "NONE"))
        if bodyish:
            filled = sum(1 for k in keys
                         if isinstance(units[k], dict)
                         and units[k].get(bodyish[0]))
            print("        records with %s filled: %d" % (bodyish[0], filled))
PY

say "[2/3] tree_units3.json, the output-side miner's own input, examined"
python3 - <<'PY'
import json, os
path = 'PseudoCoupHQ/Research/op_pipeline/tree_units3.json'
doc = json.load(open(path))
print("   top-level: %s" % sorted(doc)[:12])
for key in sorted(doc):
    value = doc[key]
    if isinstance(value, dict):
        keys = sorted(value)
        print("   %-16s dict of %d, first five %s" % (key, len(value), keys[:5]))
        if keys and isinstance(value[keys[0]], dict):
            print("        fields: %s" % ", ".join(sorted(value[keys[0]]))[:400])
    elif isinstance(value, list):
        print("   %-16s list of %d" % (key, len(value)))
PY

say "[3/3] the honest denominator: how many go units exist in the corpus at all"
python3 - <<'PY'
import json
doc = json.load(open('PseudoCoupHQ/Research/op_pipeline/'
                     'canon39_wrapped_go.json'))
print("   canon39_wrapped_go.json meta.note: %s"
      % json.dumps(doc.get("meta", {}).get("note"))[:600])
print("   canon39_wrapped_go.json meta keys: %s" % sorted(doc.get("meta", {})))
for k, v in sorted(doc.get("meta", {}).items()):
    print("      %-32s %s" % (k, json.dumps(v)[:300]))
PY
echo "DONE t87_l3"
