#!/usr/bin/env bash
# hub2_l5_the_pair_key_at_full_granularity.sh -- task hub2, lane 5.
# Writes nothing.  Lane 2 asked whether the loop proved "the pair" using
# the setter's MNEMONIC alone, which is not the machine-form key: the key
# is the CELL, (mnem, operand shape, key_width), on the setter side as
# much as on the consumer side.  This lane classifies the setter's own
# LINE in every run that carries one, so the loop's pairs are keyed the
# same way the corpus's attested pairs are, and intersects the two.
set -uo pipefail
cd PseudoCoupHQ/Research/oracle/hub
total=2

echo "[1/$total] the loop's pairs, keyed (setter cell, consumer cell)"
python3 - <<'PY'
import json, os, sys, collections, resource
HQ = "PseudoCoupHQ"
OP = os.path.join(HQ, "Research", "op_pipeline")
MODEL = os.path.join(HQ, "Research", "oracle", "arch_opcodes", "model")
EMU = os.path.join(HQ, "Research", "oracle", "cross_construction", "emulation")
AUTO = os.path.join(EMU, "autopoly")
for path in [OP, MODEL, EMU]:
    sys.path.insert(0, path)
import model_table as MT
MT._install_gpr_widths()
STORES = ["autopoly_runs.jsonl", "autopoly2_runs.jsonl", "autopoly3_runs.jsonl",
          "autopoly4_runs.jsonl", "autopoly5_runs.jsonl", "expand1_runs.jsonl",
          "bank1_delta_runs.jsonl", "bank1_full_runs.jsonl"]
PROVED = ("PROVED", "PROVED_ON_SHIP")
held = {}
unclassified = collections.Counter()
for store in STORES:
    path = os.path.join(AUTO, store)
    if not os.path.exists(path):
        continue
    with open(path) as handle:
        for line in handle:
            run = json.loads(line)
            setter = run.get("setter")
            if setter is None:
                continue
            place = None
            for candidate in run.get("places") or []:
                if (candidate.get("writes") or "").startswith("reg_"):
                    place = candidate
                    break
            if place is None:
                continue
            check = place.get("check") or {}
            good = check.get("outcome") in PROVED
            extended = (check.get("under_caller_extension") or {}).get("outcome") in PROVED
            if not good and not extended:
                continue
            shape, width, cause = MT.classify_line(setter["mnem"], setter.get("line"), None)
            if cause is not None:
                unclassified[cause] += 1
                continue
            setter_cell = (setter["mnem"], shape, MT.key_width(setter["mnem"], width))
            key = (run["lang"], setter_cell,
                   (run["mnem"], run["shape"], run["key_width"]))
            record = held.get(key)
            if record is None:
                held[key] = {"stores": [store], "params": len(place.get("params") or []),
                             "kind": "proved" if good else "proved_under_caller_extension"}
            else:
                record["stores"].append(store)
print("proved (target, setter cell, consumer cell) pair keys: %d" % len(held))
print("setter lines the classifier does not read: %s" % dict(unclassified))
print()
print("| target | setter cell | consumer cell | kind | parameters |")
print("|---|---|---|---|---|")
for key in sorted(held, key=lambda k: (k[0], k[2], k[1])):
    record = held[key]
    print("| %s | `%s %s %s` | `%s %s %s` | %s | %d |"
          % (key[0], key[1][0], key[1][1], key[1][2],
             key[2][0], key[2][1], key[2][2], record["kind"], record["params"]))
handle = open("/tmp/pair_entries.json", "w")
json.dump([[k[0], list(k[1]), list(k[2]), held[k]["kind"], held[k]["params"]]
           for k in held], handle)
handle.close()
print("peak kB", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY

echo "[2/$total] the go corpus's attested pairs against those keys"
python3 - <<'PY'
import json, collections, resource
entries = json.load(open("/tmp/pair_entries.json"))
index = {}
for target, setter, consumer, kind, params in entries:
    index[(target, tuple(setter), tuple(consumer))] = (kind, params)
units = json.load(open("/tmp/one_pair.json"))
print("go units that are one pair plus chaff: %d" % len(units))
distinct = collections.Counter()
for row in units:
    s = row["setter"]
    k = row["consumer"]
    distinct[((s["mnem"], s["shape"], s["key_width"]),
              (k["mnem"], k["shape"], k["key_width"]))] += 1
print("the distinct pairs they attest: %d" % len(distinct))
print()
print("| setter cell | consumer cell | go units | c | rust | go |")
print("|---|---|---|---|---|---|")
counter = collections.Counter()
for pair in sorted(distinct, key=lambda p: (p[1], p[0])):
    marks = []
    for target in ["c", "rust", "go"]:
        got = index.get((target, pair[0], pair[1]))
        marks.append("--" if got is None else got[0])
        counter[(target, got is not None)] += distinct[pair]
    print("| `%s %s %s` | `%s %s %s` | %d | %s | %s | %s |"
          % (pair[0][0], pair[0][1], pair[0][2],
             pair[1][0], pair[1][1], pair[1][2], distinct[pair],
             marks[0], marks[1], marks[2]))
print()
print("| target | go units whose attested PAIR CELL has a proved entry | units it has not |")
print("|---|---|---|")
for target in ["c", "rust", "go"]:
    print("| %s | %d | %d |" % (target, counter[(target, True)],
                                counter[(target, False)]))
print()
print("the same question with the setter's WIDTH ignored, which is NOT the "
      "machine-form key and is printed only to name the difference:")
loose = set()
for target, setter, consumer, kind, params in entries:
    loose.add((target, setter[0], tuple(consumer)))
counter = collections.Counter()
for pair in distinct:
    for target in ["c", "rust", "go"]:
        got = (target, pair[0][0], pair[1]) in loose
        counter[(target, got)] += distinct[pair]
for target in ["c", "rust", "go"]:
    print("   %-5s %d units would match, %d would not"
          % (target, counter[(target, True)], counter[(target, False)]))
print("peak kB", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY
