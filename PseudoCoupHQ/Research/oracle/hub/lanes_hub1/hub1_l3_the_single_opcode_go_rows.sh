#!/usr/bin/env bash
# hub1_l3_the_single_opcode_go_rows.sh -- task hub1, lane 3. Writes nothing.
# WHAT IT ASKS: (a) what `single_opcode_units.json` holds for go under both of
# task o2's rules, unit by unit, with each unit's own operand holders off its
# probe record and the cell its ledger attests; (b) how the model table's own
# operand reader (`model_table.operand_texts`, `operand_class`) reads the
# cell's line and the go unit's own body line, which is how an operand SLOT is
# put on an IN row without any token; (c) for the cells those rows name, the
# whole shape of task ap5's run record on c, rust and go -- the place that
# writes a value, its parameters, its symbol and the source file the renderer
# left under `autopoly/src5/`.  Memory bound 6 GB, abort ABORT_MEMORY_HUB1.
set -uo pipefail
cd PseudoCoupHQ/Research/oracle/hub
python3 - <<'PY'
import json, os, sys, glob, collections, resource

HQ = "PseudoCoupHQ"
OP = os.path.join(HQ, "Research/op_pipeline")
MODEL = os.path.join(HQ, "Research/oracle/arch_opcodes/model")
ARCH = os.path.join(HQ, "Research/oracle/arch_opcodes")
AUTO = os.path.join(HQ, "Research/oracle/cross_construction/emulation/autopoly")
sys.path.insert(0, OP)
sys.path.insert(0, MODEL)
import model_table as MT
import canonical_form as CF

def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

print("[1/4] single_opcode_units.json, the go groups")
soj = json.load(open(os.path.join(ARCH, "single_opcode_units.json")))
groups = soj["single_opcode_groups"]["go"]
for rule in sorted(groups):
    print("   rule %-8s groups: %d" % (rule, len(groups[rule])))
man1 = json.load(open(os.path.join(OP, "probe_manifest_go.json")))["probes"]
man2 = json.load(open(os.path.join(OP, "probe_manifest2_go.json")))["probes"]

def probe_of(uid):
    kind, n = uid.split("/")[1].split("_", 1)
    return (man1 if kind == "op" else man2).get(n)

print("[2/4] every go NARROW group, its body, and its members' holders")
for g in groups["narrow"]:
    print("   -- body LITERAL: %r   members %d   example %s"
          % (g["body_text"], g["member_count"], g["example_unit_id"]))
    holders = collections.Counter()
    for m in g["members"]:
        p = probe_of(m["unit"])
        if p is None:
            holders["(no probe record)"] += 1
            continue
        holders[(p.get("arity"), p.get("lhs_type"), p.get("rhs_type"),
                 p.get("result_type"), p.get("expression"))] += 1
    for k in sorted(holders, key=str):
        print("         %3d  %s" % (holders[k], k))

print("[3/4] the operand reader, on a cell line and on a go body line")
for line in ["add %esi,%edi", "add %ebx,%eax", "imul %esi,%edi",
             "imul %ebx,%eax", "addsd %xmm1,%xmm0", "shl %cl,%edi",
             "cmp %esi,%edi", "sub %esi,%edi", "sub %ebx,%eax"]:
    texts = MT.operand_texts(line)
    classes = []
    for i, t in enumerate(texts):
        classes.append(MT.operand_class(t, i, len(texts)))
    print("   %-22r operands %-28r classes %r" % (line, texts, classes))

print("[4/4] task ap5's run record for the cells the handful needs")
runs = {}
for line in open(os.path.join(AUTO, "autopoly5_runs.jsonl")):
    r = json.loads(line)
    runs[(r["lang"], r["mnem"], r["shape"], r["key_width"])] = r
want = [("add", "gpr_gpr", 32), ("add", "gpr_gpr", 64),
        ("sub", "gpr_gpr", 32), ("sub", "gpr_gpr", 64),
        ("imul", "gpr_gpr", 32), ("imul", "gpr_gpr", 64),
        ("addsd", "xmm_xmm", 64), ("mulsd", "xmm_xmm", 64),
        ("cmp", "gpr_gpr", 32)]
for cell in want:
    for lang in ["c", "rust", "go"]:
        r = runs.get((lang,) + cell)
        if r is None:
            print("   %-22s %-5s NO RUN" % ("%s %s %d" % cell, lang))
            continue
        print("   == %s -> %s   route %s   line %r   row %s"
              % ("%s %s %d" % cell, lang, r["route"], r["line"], r["row_id"]))
        for pl in r["places"]:
            chk = pl.get("check") or {}
            print("      place %-12s bits %-4s rendered %s outcome %-16s symbol %s"
                  % (pl.get("writes"), pl.get("bits"), pl.get("rendered"),
                     chk.get("outcome"), pl.get("symbol")))
            print("         params %r" % (pl.get("params"),))
            print("         source_path %r  families %r"
                  % (pl.get("source_path"), pl.get("families")))
            print("         home %r" % (pl.get("home"),))
print("   one rendered source, LITERAL, c add gpr_gpr 32:")
r = runs[("c", "add", "gpr_gpr", 32)]
print(r["places"][0]["source"])
print("   one rendered source, LITERAL, rust add gpr_gpr 32:")
r = runs[("rust", "add", "gpr_gpr", 32)]
print(r["places"][0]["source"])
print("   one rendered source, LITERAL, go add gpr_gpr 32:")
r = runs[("go", "add", "gpr_gpr", 32)]
print(r["places"][0]["source"])
print("   one rendered source, LITERAL, c addsd xmm_xmm 64:")
r = runs[("c", "addsd", "xmm_xmm", 64)]
print(r["places"][0]["source"])
print("peak resident: %d kB" % peak_kb())
PY
