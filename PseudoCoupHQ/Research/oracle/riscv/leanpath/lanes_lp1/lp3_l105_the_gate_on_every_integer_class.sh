#!/bin/bash
# lp3_l105_the_gate_on_every_integer_class.sh
#
# THE GATE WIDE, AND IT IS WIDE BECAUSE THE CORPUS WAS QUOTIENTED FIRST.
#
# the owner, 2026-09-17: "our new system could reduce the number of arch-units by
# proving equivalence via emulations."  That is what makes this lane possible
# at all.  `equivalence_classes.py` keys every arch-unit by its instruction
# sequence AND its psABI arrival shape -- the two things the `abi` goal
# actually depends on -- and 1,312 arch-units fall into 537 classes.  Members
# of one class are not similar goals; they are THE SAME GOAL, so one proof
# discharges the class and nothing is owed for the merge.
#
#   186 classes, integer layer, emulation present, not blocked
#   657 arch-units covered by them
#   10 of the 186 have ever been put to Lean.  176 never have.
#
# ONLY THE `abi` STATEMENT IS PUT. log 294 section 2.3 measured `plain` as
# FALSE BY CONSTRUCTION -- it compares the two sides with no psABI
# precondition, so every counterexample is a high-bit input the ABI forbids.
# Putting it again would spend 186 Lean runs to re-learn that. The
# cross-architecture check reached the same conclusion independently
# (log 295 section 2.2), which is why it is now treated as settled rather
# than re-measured.
#
# THE SIMP SET COMES FROM `leanpath.equals.simp_set`, the one place, so the
# three-layer assembly l101 added rides here. A lane that assembles its own
# drifts -- that is exactly what made l100 report UNDECIDED against code that
# had already changed.
#
# Fetches nothing. Writes $A/runs/gate_classes only. Budget: four hours.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan
export PATH=$ELAN_HOME/bin:/opt/elan/bin:/opt/cargo/bin:/usr/lib/go-1.26/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
export GOCACHE=/work/gocache GOPATH=/work/gopath GOFLAGS=-mod=mod
mkdir -p /work/gocache /work/gopath
A=PseudoCoupHQ/Research/oracle/riscv/leanpath
RV=PseudoCoupHQ/Research/oracle/riscv
AU=$RV/softfloat_slices/arch_units
OP=PseudoCoupHQ/Research/op_pipeline
P=/work/proof; PLIB=LeanIM
S=$A/strip_perarm/strip.json
G=$A/runs/gate_classes
mkdir -p $G; cd $A; t0=$(date +%s)
export WALK_JOBS=4 WALK_MAX_WORDS=300

echo "[1/5] preflight  ($(( $(date +%s) - t0 ))s)"
[ -f $P/.lake/packages/Sail/Sail/Common.lean ] || { echo "  FLAG: $P is not a built tree"; exit 3; }
[ -f $S ] || { echo "  FLAG: no $S"; exit 3; }
[ -f $RV/equivalence_classes.json ] || { echo "  FLAG: no equivalence_classes.json"; exit 3; }
grep -q "def simp_set" $A/leanpath/equals.py || { echo "  FLAG: equals.py has no simp_set"; exit 3; }
echo "  built tree, strip record, classes and the one simp set: all present"

echo "[2/5] one representative per integer-layer class  ($(( $(date +%s) - t0 ))s)"
python3 - <<'PY'
import json, os
RV = "PseudoCoupHQ/Research/oracle/riscv"
AU = RV + "/softfloat_slices/arch_units"
OP = "PseudoCoupHQ/Research/op_pipeline"
G  = RV + "/leanpath/runs/gate_classes"
SHIP = {"c":   "clang -std=c17 -O1 --target=riscv64-unknown-linux-gnu -nostdlibinc",
        "go":  "GOARCH=riscv64 GOOS=linux go build"}
src = os.path.join(G, "src"); os.makedirs(src, exist_ok=True)

recs = {}
for f in (AU + "/_units_int.json", AU + "/_units.json"):
    tag = "integer" if f.endswith("_int.json") else "float"
    for u in json.load(open(f))["units"]:
        recs[u["unit"]] = (tag, u)
probes = {L: json.load(open(OP + "/probe_manifest_%s.json" % L))["probes"]
          for L in ("c", "go")}

classes = json.load(open(RV + "/equivalence_classes.json"))["classes"]
picks, skipped = [], {"no emulation": 0, "float layer": 0, "blocked": 0,
                      "no probe": 0}
for c in classes:
    have = [m for m in c["members"] if m in recs]
    if not have:
        skipped["no emulation"] += 1; continue
    if any(recs[m][0] == "float" for m in have):
        skipped["float layer"] += 1; continue
    # the representative is the class's own, when it has an emulation
    rep = c["representative"] if c["representative"] in recs else sorted(have)[0]
    tag, u = recs[rep]
    if u.get("blocked") or u.get("reduced"):
        skipped["blocked"] += 1; continue
    if u["lang"] not in probes:
        skipped["no probe"] += 1; continue
    picks.append((c, u))
print("  classes considered: %d" % len(classes))
for k, v in sorted(skipped.items()):
    print("    skipped, %-14s %d" % (k, v))
print("  representatives put to the gate: %d, covering %d arch-units"
      % (len(picks), sum(c["member_count"] for c, _ in picks)))

arch, emul, pairs = [], [], []
for c, u in picks:
    L = u["lang"]
    n = int(u["symbol"].split("_")[-1])
    p = probes[L][str(n)] if str(n) in probes[L] else probes[L][n]
    ext = {"c": "c", "go": "go"}[L]
    ap = os.path.join(src, "arch_%s.%s" % (u["name"], ext))
    open(ap, "w").write(p["source"])
    sym = p["symbol"]
    if L == "go" and sym.startswith("main."):
        sym = sym[len("main."):]
    label = {"unit": u["name"], "lang": L, "n": n, "operator": u["operator"],
             "lhs_type": u["lhs_type"], "rhs_type": u["rhs_type"],
             "expression": u["expression"]}
    arch.append({"name": "arch_" + u["name"], "lang": L, "source": ap,
                 "symbol": sym, "flags": SHIP[L], "unit": u["name"],
                 "cell_display": "%s %s %s" % (L, u["lhs_type"], u["rhs_type"] or ""),
                 "probe": label})
    ep = u["languages"]["c"]["file"].split("arch_units/", 1)[1]
    emul.append({"name": "emul_" + u["name"], "lang": "c",
                 "source": os.path.join(AU, ep),
                 "symbol": u["languages"]["c"]["entry"],
                 "flags": SHIP["c"] + " -I" + os.path.join(AU, "c"),
                 "unit": u["name"],
                 "cell_display": "%s %s %s" % (L, u["lhs_type"], u["rhs_type"] or ""),
                 "probe": label})
    pairs.append({"unit": u["name"], "lang": L, "n": n,
                  "operator": u["operator"], "lhs_type": u["lhs_type"],
                  "rhs_type": u["rhs_type"], "expression": u["expression"],
                  "arch_instructions": len(u["body"]), "arch_body": u["body"],
                  "result_bits": u["result_bits"], "n_params": u["n_params"],
                  "reduced": u["reduced"], "guarded": u.get("guarded"),
                  "class_members": c["member_count"],
                  "class_languages": c["languages"],
                  "class_arrival_shape": c["arrival_shape"],
                  "emul_source": os.path.join(AU, ep),
                  "emul_entry": u["languages"]["c"]["entry"]})
for nm, doc in (("units_arch.json", arch), ("units_emul.json", emul),
                ("pairs.json", pairs)):
    fh = open(os.path.join(G, nm), "w")
    json.dump(doc, fh, indent=1, sort_keys=True); fh.write("\n"); fh.close()
PY
[ -f $G/pairs.json ] || { echo "  FLAG: no pairs.json"; exit 3; }

echo "[3/5] compile and carve both sides  ($(( $(date +%s) - t0 ))s)"
python3 - <<'PY'
import json, os, sys
A = "PseudoCoupHQ/Research/oracle/riscv/leanpath"
G = A + "/runs/gate_classes"
sys.path.insert(0, A)
from leanpath.walk import compile_unit, carve
out, work = {}, os.path.join(G, "objs")
os.makedirs(work, exist_ok=True)
for side in ("arch", "emul"):
    units = json.load(open("%s/units_%s.json" % (G, side)))
    for i, u in enumerate(units, 1):
        obj = os.path.join(work, u["name"] + ".o")
        rc, secs, o, sym = compile_unit(u, obj, work)
        row = {"rc": rc, "seconds": round(secs, 1), "symbol": sym}
        if rc != 0:
            row["refusal"] = o.strip().split("\n")[-1][:200]
        else:
            crc, cout, body = carve(obj, sym)
            row["instructions"] = len(body)
            row["body"] = [("%s %s" % (m, ops)).strip() for _, m, ops in body]
        out.setdefault(u["unit"], {})[side] = row
        if i % 40 == 0:
            print("    %s %d/%d" % (side, i, len(units)), flush=True)
fh = open(G + "/compiled.json", "w")
json.dump(out, fh, indent=1, sort_keys=True); fh.write("\n"); fh.close()
ok = sum(1 for u in out.values()
         if u.get("arch", {}).get("rc") == 0 and u.get("emul", {}).get("rc") == 0)
print("  both sides compiled: %d of %d" % (ok, len(out)))
PY

echo "[4/5] walk both sides  ($(( $(date +%s) - t0 ))s)"
python3 -u -m leanpath walk $P /work/Lean_IM_pr_exec LeanIM $S $G/units_arch.json $G/walk_arch 900 > $G/walk_arch.log 2>&1
echo "  arch walk rc=$?  $(tail -1 $G/walk_arch.log)"
python3 -u -m leanpath walk $P /work/Lean_IM_pr_exec LeanIM $S $G/units_emul.json $G/walk_emul 900 > $G/walk_emul.log 2>&1
echo "  emul walk rc=$?  $(tail -1 $G/walk_emul.log)"

echo "[5/5] equals, the abi statement only  ($(( $(date +%s) - t0 ))s)"
python3 -u - <<'PY' > $G/equals.log 2>&1
import json, os, re, sys, time
from concurrent.futures import ThreadPoolExecutor
A = "PseudoCoupHQ/Research/oracle/riscv/leanpath"
sys.path.insert(0, A)
from leanpath import strip as ST
from leanpath.equals import equals, simp_set
P, PLIB = "/work/proof", "LeanIM"
G = A + "/runs/gate_classes"
OUT = G + "/equals"; os.makedirs(OUT, exist_ok=True)
lean_dir = os.path.join(P, PLIB)
header, closers = ST.header_of(lean_dir, PLIB)
clauses = {c["name"][len("execute_"):]: c for c in ST.clauses_of(lean_dir)}
defs_index = ST.emitted_defs(lean_dir)
lib_index = ST.library_index(P)
print("clauses %d; emitted definitions %d; lean-sail definitions indexed %d"
      % (len(clauses), len(defs_index), len(lib_index)), flush=True)
if not lib_index:
    print("FLAG: the library index is empty. ABORT."); raise SystemExit(3)

def clause_of(head):
    if head in clauses: return clauses[head]
    parts = head.split("_")
    for k in range(len(parts) - 1, 0, -1):
        nm = "_".join(parts[:k])
        if nm in clauses: return clauses[nm]
    return None

def bodies_of(F, Gx):
    heads = sorted(set(re.findall(r"pure_(\w+)", F + " " + Gx)))
    bodies, seen = [], set()
    for h in heads:
        cl = clause_of(h)
        if cl is None or cl["name"] in seen: continue
        seen.add(cl["name"])
        prop = ST.propose(cl)
        if "refused" in prop: prop = ST.propose_effects(cl, defs_index)
        if "refused" in prop: continue
        bodies += ST.lean_body(cl, prop)
    return bodies, heads

def widen(t, v):
    t = (t or "").strip()
    if t in ("int32_t", "int32"):
        return "(((((%s) &&& 0xffffffff#64) ^^^ 0x80000000#64) - 0x80000000#64))" % v
    if t in ("uint32_t", "uint32", "float", "float32"):
        return "(((%s) &&& 0xffffffff#64))" % v
    if t in ("bool",):
        return "(((%s) &&& 0x1#64))" % v
    return "(%s)" % v

def at_width(E, unknowns, args, bits):
    if unknowns:
        binder = " ".join("(%s : BitVec 64)" % v for v in unknowns)
        E = "((fun %s => (%s)) %s)" % (binder, E, " ".join(args))
    if bits and bits < 64:
        E = "((%s) &&& 0x%x#64)" % (E, (1 << bits) - 1)
    return E

warch = {r["unit"]: r for r in json.load(open(G + "/walk_arch/walk.json"))["rows"]}
wemul = {r["unit"]: r for r in json.load(open(G + "/walk_emul/walk.json"))["rows"]}
pairs = json.load(open(G + "/pairs.json"))
comp  = json.load(open(G + "/compiled.json"))

jobs, rows = [], []
for p in pairs:
    u = p["unit"]
    ra, re_ = warch.get("arch_" + u, {}), wemul.get("emul_" + u, {})
    row = {"unit": u, "lang": p["lang"], "operator": p["operator"],
           "lhs_type": p["lhs_type"], "rhs_type": p["rhs_type"],
           "expression": p["expression"], "result_bits": p["result_bits"],
           "class_members": p["class_members"],
           "class_languages": p["class_languages"],
           "arch_instructions": (comp.get(u, {}).get("arch") or {}).get("instructions"),
           "emul_instructions": (comp.get(u, {}).get("emul") or {}).get("instructions"),
           "arch_walk": ra.get("verdict"), "emul_walk": re_.get("verdict")}
    rows.append(row)
    if ra.get("verdict") != "CERTIFIED" or re_.get("verdict") != "CERTIFIED":
        row["abi"] = {"verdict": "NOT REACHED", "stage": "walk"}
        continue
    F, Gx = ra["proposal"], re_["proposal"]
    unknowns = [v for v in ("a", "b", "c", "d") if re.search(r"\b%s\b" % v, F + " " + Gx)]
    bodies, heads = bodies_of(F, Gx)
    tag = re.sub(r"\W", "_", u)
    defs = simp_set(defs_index, heads, tag, bodies, F, Gx)
    args = []
    for v in unknowns:
        t = p["lhs_type"] if v == "a" else (p["rhs_type"] if v == "b" else None)
        args.append(widen(t, v))
    jobs.append((row, bodies, tag + "_abi", unknowns,
                 at_width(F, unknowns, args, p["result_bits"]),
                 at_width(Gx, unknowns, args, p["result_bits"]), defs))
print("classes reaching equals: %d of %d" % (len(jobs), len(pairs)), flush=True)

def run(j):
    row, bodies, tag, unknowns, L, R, defs = j
    t = time.time()
    r = equals(P, header, closers, bodies, tag, unknowns, L, R, defs, OUT, 120)
    r["wall"] = round(time.time() - t, 1)
    return row, r

done = 0
pool = ThreadPoolExecutor(max_workers=4)
for row, r in pool.map(run, jobs):
    row["abi"] = r
    done += 1
    if done % 10 == 0 or r["verdict"] == "PROVED":
        print("  %-28s %-9s %-14s %5.1fs  covers %d units"
              % (row["unit"], r["verdict"], r["stage"], r["wall"],
                 row["class_members"]), flush=True)
pool.shutdown()

fh = open(G + "/gate.json", "w")
json.dump({"rows": rows}, fh, indent=1, sort_keys=True); fh.write("\n"); fh.close()

import collections
v = collections.Counter((r.get("abi") or {}).get("verdict") for r in rows)
print()
print("VERDICTS over %d classes:" % len(rows))
for k, n in v.most_common():
    covered = sum(r["class_members"] for r in rows
                  if (r.get("abi") or {}).get("verdict") == k)
    print("  %-14s %4d classes  covering %4d arch-units" % (k, n, covered))
st = collections.Counter((r.get("abi") or {}).get("stage") for r in rows
                         if (r.get("abi") or {}).get("verdict") == "PROVED")
print("  proved at stage:", dict(st))
PY
tail -40 $G/equals.log
python3 $OP/check_no_spelling_keys.py $G/gate.json 2>&1 | tail -1
echo "wall=$(( $(date +%s) - t0 ))s"
echo done
