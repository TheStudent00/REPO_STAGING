#!/usr/bin/env bash
# o12 lane 1 -- the shapes the synthesis route has to fit: the imports
# it needs, the spelling of a pool entry's `type_key`, the size of the
# component library each target's machine type key bucket offers, and
# whether the holder table carries a row for every unit involved.
# Nothing is written; this lane only measures.
set -u
cd /projects/PseudoCoupHQ/Research/op_pipeline
echo "======== 1. toolchain and imports ========"
python3 - <<'PY'
import importlib, sys
sys.path.insert(0, "/projects/PseudoCoupHQ/Research/oracle/cross_construction")
sys.path.insert(0, "/projects/PseudoCoupHQ/Research/op_pipeline/lean")
names = ["z3", "gate", "reference", "pool100_entry_equivalence",
         "term_to_lean", "cross2_length_two", "check_no_spelling_keys"]
for name in names:
    try:
        module = importlib.import_module(name)
        print("  OK      %-28s %s" % (name, module.__file__))
    except Exception as problem:
        print("  ABSENT  %-28s %s: %s" % (name, type(problem).__name__, problem))
import z3
print("  z3", z3.get_version_string())
PY
echo
echo "======== 2. the shapes ========"
echo "[1/1] shape census"
python3 - <<'PY'
import json, os, re, resource, sys
sys.path.insert(0, "/projects/PseudoCoupHQ/Research/op_pipeline")
OP = "/projects/PseudoCoupHQ/Research/op_pipeline"
EMU = "/projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation"
pool = json.load(open(os.path.join(OP, "the_pool5.json")))
holders = json.load(open(os.path.join(OP, "types101_entry_holders.json")))
population = json.load(open(os.path.join(EMU, "emulation_population.json")))
results = json.load(open(os.path.join(EMU, "emulation_results.json")))

print("-- 2.1 the o7 population and results")
print("   population entries:", len(population["entries"]))
print("   population keys on one entry:",
      sorted(list(population["entries"].values())[0]))
print("   emulation_results.json top keys:", sorted(results))
for key in sorted(results):
    value = results[key]
    if isinstance(value, list):
        print("     %s: list of %d" % (key, len(value)))
        if value and isinstance(value[0], dict):
            print("       keys:", sorted(value[0])[:40])

print()
print("-- 2.2 the spelling of type_key")
seen = []
for entry in pool["entries"][:8]:
    seen.append((entry["entry_id"], entry.get("type_key")))
for item in seen:
    print("   ", item)
keys = {}
for entry in pool["entries"]:
    keys.setdefault(entry.get("type_key"), 0)
    keys[entry["type_key"]] += 1
print("   distinct type_key values:", len(keys))

print()
print("-- 2.3 the component library per target bucket")
by_key_c = {}
for entry in pool["entries"]:
    good = []
    for member in entry["members"]:
        if member["lang"] != "c":
            continue
        if not member.get("layer5_normalized_text"):
            continue
        if not member.get("layer5_merge_eligible"):
            continue
        good.append(member)
    if good:
        by_key_c.setdefault(entry.get("type_key"), []).append(
            (entry["entry_id"], good[0]["unit"], len(good)))
sizes = []
empty = 0
for entry_id, plan in sorted(population["entries"].items()):
    key = plan.get("type_key")
    have = by_key_c.get(key, [])
    sizes.append((entry_id, plan["x_lang"], key, len(have)))
    if not have:
        empty += 1
print("   targets:", len(sizes), " with an EMPTY c library:", empty)
counts = sorted(row[3] for row in sizes)
print("   library size min/median/max: %d / %d / %d"
      % (counts[0], counts[len(counts) // 2], counts[-1]))
buckets = {}
for row in sizes:
    buckets.setdefault(row[2], 0)
    buckets[row[2]] += 1
print("   distinct target buckets:", len(buckets))
print("   the ten most populated target buckets (bucket, targets, library):")
ordered = sorted(buckets.items(), key=lambda item: -item[1])[:10]
for key, count in ordered:
    print("     %-40s targets %3d  library %4d"
          % (key, count, len(by_key_c.get(key, []))))

print()
print("-- 2.4 arity: does one bucket hold one arrival shape?")
def variables(text):
    return sorted(set(re.findall(r"\bv(\d+)\b", text)), key=int)
mixed = 0
for key, rows in list(by_key_c.items()):
    arities = set()
    for entry_id, unit, _n in rows:
        pass
    # arity from the type_key spelling itself
print("   (arity is read from the type_key spelling; see 2.2)")

print()
print("-- 2.5 the holder table's coverage of the units involved")
unit_row = {}
for record in holders["entries"]:
    for member in record["members"]:
        unit_row[member["unit"]] = member
need = set()
for entry_id, plan in population["entries"].items():
    need.add(plan["x_unit"])
for key, rows in by_key_c.items():
    for entry_id, unit, _n in rows:
        need.add(unit)
missing = sorted(name for name in need if name not in unit_row)
print("   units needed: %d; with a holder row: %d; missing: %d %s"
      % (len(need), len(need) - len(missing), len(missing), missing[:8]))

print()
print("-- 2.6 three target texts, with their type_key and holders")
shown = 0
for entry_id, plan in sorted(population["entries"].items()):
    row = unit_row.get(plan["x_unit"])
    print("   %s  %s  %s" % (entry_id, plan["x_lang"], plan["x_unit"]))
    print("     type_key      %s" % plan.get("type_key"))
    print("     result_width  %s" % plan.get("result_width"))
    print("     holders       %s -> %s" % (
        row and row.get("parameter_holders"), row and row.get("result_holder")))
    print("     text          %s" % plan["text"][:160])
    shown += 1
    if shown == 3:
        break
print()
print("PEAK_RSS_KB=%d" % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY
echo "-- exit $?"
