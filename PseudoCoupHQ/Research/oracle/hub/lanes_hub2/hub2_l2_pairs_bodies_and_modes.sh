#!/usr/bin/env bash
# hub2_l2_pairs_bodies_and_modes.sh -- task hub2, lane 2.  It writes
# nothing; it prints.  WHAT IT ASKS:
#   1. across EVERY pass on disk, per (target, flag-consumer cell), which
#      SETTER the loop rendered the emulation over and what the gate
#      answered -- the pair level's own population;
#   2. over every go unit of the corpus, the flag PAIRS its own ledger
#      attests (setter row + consumer row), and how many units are one
#      pair plus chaff -- the pair analogue of task o2's narrow rule;
#   3. why the pool entries the handful's holes name are not in task
#      o7's or task o11's population, filter by filter;
#   4. task o13's own store: which pool entries the mode re-run proved,
#      per target, and with which mode;
#   5. per go corpus unit, its pool entry's own ground (how many
#      distinct wrapped texts and layer-5 texts the entry holds), so a
#      body-level entry's reach is read rather than assumed.
set -uo pipefail
cd PseudoCoupHQ/Research/oracle/hub
total=5

echo "[1/$total] every pass: the setter each flag-consumer cell was rendered over"
python3 - <<'PY'
import json, os, collections, resource
AUTO = "PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly"
STORES = ["autopoly_runs.jsonl", "autopoly2_runs.jsonl", "autopoly3_runs.jsonl",
          "autopoly4_runs.jsonl", "autopoly5_runs.jsonl", "expand1_runs.jsonl",
          "bank1_delta_runs.jsonl", "bank1_full_runs.jsonl"]
held = collections.defaultdict(list)
for store in STORES:
    path = os.path.join(AUTO, store)
    if not os.path.exists(path):
        print("MISS", store)
        continue
    with open(path) as handle:
        for line in handle:
            run = json.loads(line)
            setter = run.get("setter")
            if setter is None:
                continue
            value = None
            for place in run.get("places") or []:
                if (place.get("writes") or "").startswith("reg_"):
                    value = place
                    break
            outcome = None
            extension = None
            params = None
            if value is not None:
                check = value.get("check") or {}
                outcome = check.get("outcome")
                extension = (check.get("under_caller_extension") or {}).get("outcome")
                params = len(value.get("params") or [])
            key = (run["lang"], run["mnem"], run["shape"], run["key_width"])
            held[key].append((store, setter["mnem"], setter.get("line"),
                              outcome, extension, params))
print("distinct (target, consumer cell) keys with a setter: %d" % len(held))
setters = collections.Counter()
for key in held:
    names = set(r[1] for r in held[key])
    setters[len(names)] += 1
print("how many of those keys were ever rendered over MORE THAN ONE setter:")
for count in sorted(setters):
    print("   %d setter(s): %d key(s)" % (count, setters[count]))
print()
print("every (target, consumer cell) whose emulation PROVED, with its setter:")
print("| target | `mnem` | shape | `key_width` | setter `mnem` | parameters | passes |")
print("|---|---|---|---|---|---|---|")
proved_pairs = set()
for key in sorted(held):
    good = [r for r in held[key]
            if r[3] == "PROVED_ON_SHIP" or r[4] in ("PROVED", "PROVED_ON_SHIP")]
    if not good:
        continue
    setter_names = sorted(set(r[1] for r in good))
    stores_seen = sorted(set(r[0] for r in good))
    for name in setter_names:
        proved_pairs.add((key[0], name, key[1], key[2], key[3]))
    print("| %s | `%s` | %s | %s | %s | %s | %s |"
          % (key[0], key[1], key[2], key[3], ", ".join("`%s`" % n for n in setter_names),
             good[0][5], len(stores_seen)))
print()
print("proved (target, setter mnem, consumer cell) triples: %d" % len(proved_pairs))
handle = open("/tmp/proved_pairs.json", "w")
json.dump(sorted(proved_pairs), handle)
handle.close()
print("peak kB", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY

echo "[2/$total] the corpus's go units: the pairs their own ledgers attest"
python3 - <<'PY'
import json, os, sys, glob, collections, resource
HQ = "PseudoCoupHQ"
OP = os.path.join(HQ, "Research", "op_pipeline")
MODEL = os.path.join(HQ, "Research", "oracle", "arch_opcodes", "model")
EMU = os.path.join(HQ, "Research", "oracle", "cross_construction", "emulation")
for path in [OP, MODEL, EMU]:
    sys.path.insert(0, path)
import model_table as MT
import canonical_form as CF
MT._install_gpr_widths()
readings = CF.runtime_answer_readings()
routines = CF.runtime_routine_names(readings)
units = {}
document = json.load(open(os.path.join(OP, "canon40_wrapped_go.json")))
units.update(document["units"])
del document
for path in sorted(glob.glob(os.path.join(OP, "canon40_regen_store",
                                          "op_units2_go_*.json"))):
    document = json.load(open(path))
    units.update(document["units"])
    del document
print("go canon40 records held: %d" % len(units))
proved = set(tuple(x) for x in json.load(open("/tmp/proved_pairs.json")))
shape_counter = collections.Counter()
one_pair = []
for unit_id in sorted(units):
    record = units[unit_id]
    line_of_row = MT.lines_of_unit(record, routines, readings)
    if line_of_row is None:
        shape_counter["the unit's body could not be relinked"] += 1
        continue
    arch = MT.arch_opcode_rows(record)
    pairs = MT.flag_pair_rows(record)
    if not pairs:
        shape_counter["no flag pair row: not a pair unit"] += 1
        continue
    if len(pairs) != 1:
        shape_counter["%d flag pair rows, not one" % len(pairs)] += 1
        continue
    row = pairs[0]
    setter_mnem, consumer_mnem = row["produced_by"]["mnem"]
    line = line_of_row.get(row["row"])
    if line is None:
        shape_counter["the pair's consumer row has no line"] += 1
        continue
    shape, width, cause = MT.classify_line(consumer_mnem, line, row.get("size"))
    if cause is not None:
        shape_counter["the consumer's line is not classifiable: %s" % cause] += 1
        continue
    # the setter's own arch-opcode row, and nothing else
    setter_rows = []
    other = []
    for arch_row in arch:
        mnem = arch_row["produced_by"]["mnem"]
        if arch_row.get("block") == "OUT":
            continue
        if mnem == setter_mnem:
            setter_rows.append(arch_row)
        else:
            other.append(mnem)
    if len(setter_rows) != 1 or other:
        shape_counter["the body holds %d row(s) that are not the pair's setter"
                      % len(other)] += 1
        continue
    setter_line = line_of_row.get(setter_rows[0]["row"])
    s_shape, s_width, s_cause = MT.classify_line(setter_mnem, setter_line,
                                                 setter_rows[0].get("size"))
    if s_cause is not None:
        shape_counter["the setter's line is not classifiable: %s" % s_cause] += 1
        continue
    one_pair.append({
        "unit": unit_id,
        "body": record.get("body_text"),
        "setter": {"mnem": setter_mnem, "shape": s_shape,
                   "key_width": MT.key_width(setter_mnem, s_width),
                   "line": setter_line},
        "consumer": {"mnem": consumer_mnem, "shape": shape,
                     "key_width": MT.key_width(consumer_mnem, width),
                     "line": line},
    })
    shape_counter["ONE PAIR PLUS CHAFF"] += 1
print()
print("| how the unit's own body reads | go units |")
print("|---|---|")
for cause in sorted(shape_counter, key=lambda c: -shape_counter[c]):
    print("| %s | %d |" % (cause, shape_counter[cause]))
print()
print("the go units that are one pair plus chaff, and whether any pass "
      "proved that pair on c / rust / go:")
print("| unit | setter cell | consumer cell | c | rust | go |")
print("|---|---|---|---|---|---|")
counter = collections.Counter()
for row in one_pair:
    s = row["setter"]
    k = row["consumer"]
    marks = []
    for target in ["c", "rust", "go"]:
        got = (target, s["mnem"], k["mnem"], k["shape"], k["key_width"]) in proved
        marks.append("yes" if got else "no")
        counter[(target, got)] += 1
    print("| %s | `%s %s %s` | `%s %s %s` | %s | %s | %s |"
          % (row["unit"], s["mnem"], s["shape"], s["key_width"],
             k["mnem"], k["shape"], k["key_width"],
             marks[0], marks[1], marks[2]))
print()
print("| target | units whose attested pair has a proved emulation | units it has not |")
print("|---|---|---|")
for target in ["c", "rust", "go"]:
    print("| %s | %d | %d |" % (target, counter[(target, True)],
                                counter[(target, False)]))
handle = open("/tmp/one_pair.json", "w")
json.dump(one_pair, handle)
handle.close()
print("peak kB", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY

echo "[3/$total] why the handful's pool entries are not in o7's / o11's population"
python3 - <<'PY'
import json, os, resource
EMU = "PseudoCoupHQ/Research/oracle/cross_construction/emulation"
population = json.load(open(os.path.join(EMU, "emulation_population.json")))
print("task o7's population file's own keys:", sorted(population.keys())[:20])
want = ["E00302", "E00163", "E00310", "E00316", "E00025", "E00058"]
def look(document, name):
    print("---", name)
    for key in sorted(document.keys()):
        value = document[key]
        if isinstance(value, list) and value and isinstance(value[0], dict):
            ids = set()
            for item in value:
                for field in ("entry_id", "entry"):
                    if field in item:
                        ids.add(item[field])
            if not ids:
                continue
            for entry_id in want:
                if entry_id in ids:
                    print("   %-8s appears in `%s` (%d rows)" % (entry_id, key, len(value)))
        if isinstance(value, list) and value and isinstance(value[0], str):
            for entry_id in want:
                if entry_id in value:
                    print("   %-8s appears in `%s` (%d ids)" % (entry_id, key, len(value)))
look(population, "emulation_population.json")
held = json.load(open(os.path.join(EMU, "emulation_held.json")))
print("emulation_held.json keys:", sorted(held.keys())[:20])
look(held, "emulation_held.json")
rust_pop = json.load(open(os.path.join(EMU, "rust", "rust_population.json")))
print("rust_population.json keys:", sorted(rust_pop.keys())[:20])
look(rust_pop, "rust_population.json")
print("peak kB", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY

echo "[4/$total] task o13's store: what the mode re-run proved"
python3 - <<'PY'
import json, os, collections, resource
EMU = "PseudoCoupHQ/Research/oracle/cross_construction/emulation"
mode = json.load(open(os.path.join(EMU, "mode", "mode_results.json")))
runs = mode["runs"]
print("mode runs:", type(runs).__name__, len(runs))
first = runs[0] if isinstance(runs, list) else runs[list(runs)[0]]
print("a run's own fields:", sorted(first.keys()))
counter = collections.Counter()
proved = collections.defaultdict(list)
for run in (runs if isinstance(runs, list) else runs.values()):
    target = run.get("target") or run.get("lang")
    outcome = run.get("outcome") or (run.get("q3") or {}).get("outcome")
    counter[(target, outcome)] += 1
    if outcome in ("PROVED", "PROVED_ON_SHIP", "PROVED_UNDER_CALLER_EXTENSION"):
        proved[target].append(run.get("entry_id"))
print("| target | outcome | runs |")
print("|---|---|---|")
for key in sorted(counter, key=lambda k: (str(k[0]), str(k[1]))):
    print("| %s | %s | %d |" % (key[0], key[1], counter[key]))
for target in sorted(proved):
    print("%s: %d entries proved on the mode re-run" % (target, len(set(proved[target]))))
print("a run, whole, cut to 2500 characters:")
print(json.dumps(first, indent=1)[:2500])
print("peak kB", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY

echo "[5/$total] the pool entry of each go unit, and the entry's own ground"
python3 - <<'PY'
import json, os, collections, resource
HQ = "PseudoCoupHQ"
OP = os.path.join(HQ, "Research", "op_pipeline")
EMU = os.path.join(HQ, "Research", "oracle", "cross_construction", "emulation")
pool = json.load(open(os.path.join(OP, "the_pool5.json")))
entry_of_unit = {}
facts = {}
for entry in pool["entries"]:
    facts[entry["entry_id"]] = {
        "member_count": entry["member_count"],
        "type_key": entry["type_key"],
        "languages": entry["languages"],
        "distinct_wrapped_text_count": entry.get("distinct_wrapped_text_count"),
        "distinct_layer5_text_count": entry.get("distinct_layer5_text_count"),
        "representative": entry.get("representative"),
        "representative_rule": entry.get("representative_rule"),
    }
    for member in entry["members"]:
        unit = member["unit"] if isinstance(member, dict) else member
        entry_of_unit[unit] = entry["entry_id"]
del pool
o7 = json.load(open(os.path.join(EMU, "emulation_results.json")))["results"]
o11 = json.load(open(os.path.join(EMU, "rust", "rust_run.json")))["results"]
def proved_index(results):
    out = {}
    for result in results:
        if result.get("control"):
            continue
        if (result.get("q3") or {}).get("outcome") in ("PROVED_ON_SHIP", "PROVED"):
            out[result["entry_id"]] = result
    return out
c_proved = proved_index(o7)
rust_proved = proved_index(o11)
go_units = sorted(u for u in entry_of_unit if u.startswith("go/"))
entries = collections.Counter()
for unit in go_units:
    entries[entry_of_unit[unit]] += 1
print("go corpus units in the pool: %d over %d entries" % (len(go_units), len(entries)))
reach = collections.Counter()
for entry_id in entries:
    reach[("c", entry_id in c_proved)] += entries[entry_id]
    reach[("rust", entry_id in rust_proved)] += entries[entry_id]
print("| target | go units whose entry has a proved body emulation | go units it has not |")
print("|---|---|---|")
for target in ["c", "rust"]:
    print("| %s | %d | %d |" % (target, reach[(target, True)], reach[(target, False)]))
print()
print("the entries with a proved body emulation that a go unit belongs to:")
print("| entry | go units in it | members | type key | languages | distinct wrapped texts | distinct layer-5 texts | c | rust |")
print("|---|---|---|---|---|---|---|---|---|")
for entry_id in sorted(entries):
    if entry_id not in c_proved and entry_id not in rust_proved:
        continue
    fact = facts[entry_id]
    print("| %s | %d | %d | %s | %s | %s | %s | %s | %s |"
          % (entry_id, entries[entry_id], fact["member_count"], fact["type_key"],
             ",".join(fact["languages"]), fact["distinct_wrapped_text_count"],
             fact["distinct_layer5_text_count"],
             entry_id in c_proved, entry_id in rust_proved))
print()
print("one proved body emulation, whole, cut to 2000 characters (c):")
example = c_proved.get("E00316")
print(json.dumps({k: v for k, v in example.items() if k != "source"}, indent=1)[:2000])
print("its rendered source's first 900 characters:")
print(example["source"][:900])
print("peak kB", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY
