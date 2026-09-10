#!/usr/bin/env bash
# hub1_l2_explore_the_go_side.sh -- task hub1, lane 2.
# WHAT IT ASKS, and it writes nothing: (a) what a corpus go unit's own
# ledger says its body produced, cell by cell, using the model table's own
# reading (`model_table.lines_of_unit`, `arch_opcode_rows`, `classify_line`,
# `key_width`), imported and never edited; (b) how many go units attest
# exactly one cell; (c) the join from a go unit to its own SOURCE in the
# probe manifests; (d) for the constructs the handful will carry, which
# cells the corpus attests and what task ap5's loop proved for them on c,
# rust and go.  Memory bound 6 GB, named abort ABORT_MEMORY_HUB1.
set -uo pipefail
cd PseudoCoupHQ/Research/oracle/hub
python3 - <<'PY'
import json, os, sys, glob, collections, resource

HQ = "PseudoCoupHQ"
OP = os.path.join(HQ, "Research/op_pipeline")
MODEL = os.path.join(HQ, "Research/oracle/arch_opcodes/model")
sys.path.insert(0, OP)
sys.path.insert(0, MODEL)

BOUND_KB = 6 * 1024 * 1024

def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

def check(where):
    if peak_kb() > BOUND_KB:
        raise SystemExit("ABORT_MEMORY_HUB1 at %s: %d kB" % (where, peak_kb()))

import model_table as MT
import canonical_form as CF

print("[1/5] the go population and its sources")
man1 = json.load(open(os.path.join(OP, "probe_manifest_go.json")))["probes"]
man2 = json.load(open(os.path.join(OP, "probe_manifest2_go.json")))["probes"]
print("   probe_manifest_go probes: %d   probe_manifest2_go probes: %d"
      % (len(man1), len(man2)))

units = {}
doc = json.load(open(os.path.join(OP, "canon40_wrapped_go.json")))
for uid, rec in doc["units"].items():
    units[uid] = rec
del doc
for path in sorted(glob.glob(os.path.join(OP, "canon40_regen_store",
                                          "op_units2_go_*.json"))):
    doc = json.load(open(path))
    for uid, rec in doc["units"].items():
        units[uid] = rec
    del doc
print("   canon40 go units held: %d" % len(units))
check("units held")

def source_of(uid):
    kind, n = uid.split("/")[1].split("_", 1)
    if kind == "op":
        p = man1.get(n)
    else:
        p = man2.get(n)
    return p

have = 0
for uid in units:
    if source_of(uid) is not None:
        have += 1
print("   go units whose own probe record (source + operand types) is on a "
      "manifest: %d of %d" % (have, len(units)))

print("[2/5] one unit read end to end, LITERAL")
sample = "go/op_312"
if sample not in units:
    sample = sorted(units)[0]
rec = units[sample]
p = source_of(sample)
print("   unit: %s" % sample)
print("   body_text: %r" % rec.get("body_text"))
print("   outcome: %r  result_family: %r  arrival_families: %r"
      % (rec.get("outcome"), rec.get("result_family"),
         rec.get("arrival_families")))
print("   manifest record, every field but the source:")
for k in sorted(p or {}):
    if k == "source":
        continue
    print("      %-18s %r" % (k, p[k]))
print("   the source, LITERAL:")
for line in (p or {}).get("source", "").splitlines():
    print("      | %s" % line)

print("[3/5] the cells each go unit's own body produced")
MT._install_gpr_widths()
readings = CF.runtime_answer_readings()
routines = CF.runtime_routine_names(readings)

cells_of_unit = {}
no_line = collections.Counter()
for uid in sorted(units):
    rec = units[uid]
    line_of_row = MT.lines_of_unit(rec, routines, readings)
    if line_of_row is None:
        no_line["the unit's body could not be relinked"] += 1
        continue
    found = []
    for row in MT.arch_opcode_rows(rec):
        mnem = row["produced_by"]["mnem"]
        line = line_of_row.get(row["row"])
        if line is None:
            no_line[MT.no_line_cause(row)] += 1
            continue
        shape, width, cause = MT.classify_line(mnem, line, row.get("size"))
        if cause is not None:
            no_line[cause] += 1
            continue
        found.append((mnem, shape, MT.key_width(mnem, width)))
    cells_of_unit[uid] = found
check("cells of unit")
sizes = collections.Counter(len(v) for v in cells_of_unit.values())
print("   units relinked: %d" % len(cells_of_unit))
print("   distinct cells per unit -> how many units:")
for k in sorted(sizes):
    print("      %d cell(s): %d units" % (k, sizes[k]))
print("   rows that carried no cell, by cause:")
for cause in sorted(no_line):
    print("      %6d  %s" % (no_line[cause], cause))

print("[4/5] the constructs the handful will carry, by operand holder types")
want = [
    ("int32", "int32", "binary"), ("int64", "int64", "binary"),
    ("uint64", "uint64", "binary"), ("float64", "float64", "binary"),
]
index = collections.defaultdict(list)
for uid in sorted(cells_of_unit):
    p = source_of(uid)
    if p is None:
        continue
    key = (p.get("lhs_type"), p.get("rhs_type"), p.get("arity"))
    index[key].append(uid)
for key in want:
    got = index.get(key, [])
    print("   holders %s x %s (%s): %d go units" % (key[0], key[1], key[2],
                                                    len(got)))
    for uid in got:
        p = source_of(uid)
        cs = cells_of_unit.get(uid) or []
        print("      %-16s expr %-14r result %-9s cells %s"
              % (uid, p.get("expression"), p.get("result_type"),
                 ["%s %s %s" % c for c in cs] or "none"))

print("[5/5] what task ap5 proved for those cells, per target")
runs = {}
apath = os.path.join(HQ, "Research/oracle/cross_construction/emulation/"
                         "autopoly/autopoly5_runs.jsonl")
for line in open(apath):
    r = json.loads(line)
    runs[(r["lang"], r["mnem"], r["shape"], r["key_width"])] = r
print("   runs held: %d" % len(runs))
seen = set()
for key in want:
    for uid in index.get(key, []):
        for c in cells_of_unit.get(uid) or []:
            seen.add(c)
for c in sorted(seen):
    row = []
    for lang in ["c", "rust", "go"]:
        r = runs.get((lang,) + c)
        if r is None:
            row.append("%s: no run" % lang)
            continue
        outs = [pl.get("check", {}).get("outcome") for pl in r["places"]]
        row.append("%s: route %s places %s" % (lang, r["route"], outs))
    print("   %-24s %s" % ("%s %s %s" % c, "  |  ".join(row)))

print("peak resident: %d kB" % peak_kb())
PY
