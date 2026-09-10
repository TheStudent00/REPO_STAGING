#!/usr/bin/env bash
# hub2_l1_the_two_levels_explored.sh -- task hub2, lane 1.
# WHAT IT ASKS, and it writes nothing, it prints:
#   1. the BANK (certificates.jsonl): preferred entries of kind proved /
#      proved_under_caller_extension, per target, and how many of them
#      write a register place (the value a composition can pass on);
#   2. whether a certificate can be joined back to the RUN that produced
#      it, which is where the emulation's parameter holders live -- the
#      brief's hole (c) needs the holders on the entry;
#   3. the four go corpus units the handful's three holes name, with
#      EVERY ledger row of each (arch_opcode rows AND flag_pair rows),
#      so the (setter, consumer) pair is read off go's own body;
#   4. the corpus's flag-pair attestation: per consumer cell, its
#      setters, beside the setter the loop's own run chose;
#   5. the pool entry every go corpus unit belongs to, and whether task
#      o7 (c), task o11 (rust) or task o13 (the mode) proved an
#      emulation of that entry.
set -uo pipefail
cd PseudoCoupHQ/Research/oracle/hub
total=5
AUTO=PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
EMU=PseudoCoupHQ/Research/oracle/cross_construction/emulation

echo "[1/$total] the bank: preferred certificates per target and kind"
python3 - <<'PY'
import json, collections, resource, os
AUTO = "PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly"
per = collections.Counter()
value_place = collections.Counter()
stores = collections.Counter()
pairs = collections.defaultdict(set)
with open(os.path.join(AUTO, "certificates.jsonl")) as handle:
    for line in handle:
        record = json.loads(line)
        if not record.get("preferred"):
            continue
        kind = record["kind"]
        target = record["target"]
        per[(target, kind)] += 1
        place = record.get("place") or ""
        if kind in ("proved", "proved_under_caller_extension"):
            stores[record["produced_by"]["store"]] += 1
            if place.startswith("reg_"):
                value_place[(target, kind)] += 1
                cell = record["cell"]
                pairs[target].add((cell["mnem"], cell["shape"],
                                   cell["key_width"]))
print("| target | kind | preferred | of those, a register place |")
print("|---|---|---|---|")
for target, kind in sorted(per):
    print("| %s | %s | %d | %d |"
          % (target, kind, per[(target, kind)],
             value_place.get((target, kind), 0)))
print()
print("distinct cells with a proved register place, per target:")
for target in sorted(pairs):
    print("   %-6s %d" % (target, len(pairs[target])))
print()
print("the stores the preferred proved certificates came from:")
for store in sorted(stores):
    print("   %-90s %d" % (store, stores[store]))
print("peak kB", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY

echo "[2/$total] can a certificate be joined to the run that produced it?"
python3 - <<'PY'
import json, os, collections, resource
AUTO = "PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly"
HQ = "PseudoCoupHQ"
# every store on disk, keyed the way a certificate names it
wanted = collections.Counter()
with open(os.path.join(AUTO, "certificates.jsonl")) as handle:
    for line in handle:
        record = json.loads(line)
        if not record.get("preferred"):
            continue
        if record["kind"] not in ("proved", "proved_under_caller_extension"):
            continue
        wanted[record["produced_by"]["store"]] += 1
for store in sorted(wanted):
    path = os.path.join(HQ, store)
    print("%-92s on disk %s" % (store, os.path.exists(path)))
# one run record's own shape, off the store the most certificates name
top = sorted(wanted, key=lambda s: -wanted[s])[0]
handle = open(os.path.join(HQ, top))
first = json.loads(handle.readline())
handle.close()
print()
print("the store the most preferred proved certificates name:", top)
print("its run record's own fields:", sorted(first.keys()))
print("a place's own fields:", sorted((first.get("places") or [{}])[0].keys()))
print("peak kB", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY

echo "[3/$total] the four go units the handful's holes name, every ledger row"
python3 - <<'PY'
import json, os, sys, glob, resource
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
for unit_id in ["go/op_492", "go/op_182", "go/op_218", "go/op_96"]:
    record = units.get(unit_id)
    print()
    print("=== %s" % unit_id)
    print("body: %s" % record.get("body_text"))
    print("arrival_families: %s   result_family: %s"
          % (record.get("arrival_families"), record.get("result_family")))
    line_of_row = MT.lines_of_unit(record, routines, readings)
    print("arch_opcode rows:")
    for row in MT.arch_opcode_rows(record):
        mnem = row["produced_by"]["mnem"]
        line = None if line_of_row is None else line_of_row.get(row["row"])
        print("   row %-8s mnem %-10s line %-28s size %s"
              % (row["row"], mnem, line, row.get("size")))
    print("flag_pair rows:")
    for row in MT.flag_pair_rows(record):
        mnem = row["produced_by"]["mnem"]
        line = None if line_of_row is None else line_of_row.get(row["row"])
        print("   row %-8s setter %-8s consumer %-10s line %-28s size %s block %s"
              % (row["row"], mnem[0], mnem[1], line, row.get("size"),
                 row.get("block")))
        if line is not None:
            shape, width, cause = MT.classify_line(mnem[1], line,
                                                   row.get("size"))
            print("        the consumer's own cell: %s %s %s   cause %s"
                  % (mnem[1], shape,
                     None if width is None else MT.key_width(mnem[1], width),
                     cause))
    print("every ledger row's producer kind:")
    kinds = {}
    for row in record.get("ledger") or []:
        kind = (row.get("produced_by") or {}).get("kind")
        kinds[kind] = kinds.get(kind, 0) + 1
    print("   %s" % kinds)
print()
print("peak kB", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY

echo "[4/$total] the loop's own runs at the flag consumers: which setter"
python3 - <<'PY'
import json, os, collections, resource
AUTO = "PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly"
rows = []
with open(os.path.join(AUTO, "autopoly5_runs.jsonl")) as handle:
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
        if value is not None:
            outcome = (value.get("check") or {}).get("outcome")
        rows.append((run["lang"], run["mnem"], run["shape"],
                     run["key_width"], setter["mnem"], setter.get("line"),
                     outcome,
                     0 if value is None else len(value.get("params") or [])))
print("runs of task ap5 whose cell reads an arriving flag state: %d" % len(rows))
counter = collections.Counter()
for row in rows:
    counter[(row[0], row[6])] += 1
print("| target | the value place's outcome | runs |")
print("|---|---|---|")
for key in sorted(counter, key=lambda k: (k[0], str(k[1]))):
    print("| %s | %s | %d |" % (key[0], key[1], counter[key]))
print()
print("the c rows, every one:")
print("| `mnem` | shape | `key_width` | setter `mnem` | the setter's line | outcome | parameters |")
print("|---|---|---|---|---|---|---|")
for row in sorted(rows):
    if row[0] != "c":
        continue
    print("| `%s` | %s | %s | `%s` | `%s` | %s | %d |"
          % (row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
print("peak kB", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY

echo "[5/$total] the pool entry of every go corpus unit, and its o7/o11/o13 emulation"
python3 - <<'PY'
import json, os, collections, resource
HQ = "PseudoCoupHQ"
OP = os.path.join(HQ, "Research", "op_pipeline")
EMU = os.path.join(HQ, "Research", "oracle", "cross_construction", "emulation")
pool = json.load(open(os.path.join(OP, "the_pool5.json")))
entry_of_unit = {}
entry_of = {}
for entry in pool["entries"]:
    entry_of[entry["entry_id"]] = entry
    for member in entry["members"]:
        unit = member["unit"] if isinstance(member, dict) else member
        entry_of_unit[unit] = entry["entry_id"]
del pool
print("pool entries: %d, members indexed: %d" % (len(entry_of), len(entry_of_unit)))
go_units = [u for u in entry_of_unit if u.startswith("go/")]
go_entries = set(entry_of_unit[u] for u in go_units)
print("go corpus units in the pool: %d, over %d entries"
      % (len(go_units), len(go_entries)))
o7 = json.load(open(os.path.join(EMU, "emulation_results.json")))
print("task o7's own filters, LITERAL:")
print(json.dumps(o7.get("filters"), indent=1)[:1500])
c_proved = {}
for result in o7["results"]:
    if result.get("control"):
        continue
    if (result.get("q3") or {}).get("outcome") in ("PROVED_ON_SHIP", "PROVED"):
        c_proved[result["entry_id"]] = result
print("task o7 (c): %d results, %d entries with a proved emulation"
      % (len(o7["results"]), len(c_proved)))
del o7
o11 = json.load(open(os.path.join(EMU, "rust", "rust_run.json")))
rust_proved = {}
for result in o11["results"]:
    if result.get("control"):
        continue
    if (result.get("q3") or {}).get("outcome") in ("PROVED_ON_SHIP", "PROVED"):
        rust_proved[result["entry_id"]] = result
print("task o11 (rust): %d results, %d entries with a proved emulation"
      % (len(o11["results"]), len(rust_proved)))
del o11
mode = json.load(open(os.path.join(EMU, "mode", "mode_results.json")))
print("task o13's own keys:", sorted(mode.keys()))
print("go entries with a proved c emulation:  %d"
      % len(go_entries & set(c_proved)))
print("go entries with a proved rust emulation: %d"
      % len(go_entries & set(rust_proved)))
print()
for unit in ["go/op_492", "go/op_182", "go/op_218", "go/op_96",
             "go/op_312", "go/op_60"]:
    entry_id = entry_of_unit.get(unit)
    entry = entry_of.get(entry_id) or {}
    print("%-12s %-8s members %-5s type_key %-14s c %-5s rust %-5s"
          % (unit, entry_id, entry.get("member_count"),
             entry.get("type_key"),
             entry_id in c_proved, entry_id in rust_proved))
print("peak kB", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY
