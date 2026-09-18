#!/bin/bash
# lp3_l109_the_bridge_with_the_definitions_dropped.sh
#
# THE PAYOFF RUN. l105 put 186 integer-layer classes to Lean and left 35
# UNDECIDED, 86 arch-units, concentrated on narrow integer comparisons --
# `int32/int32` seven times, `int32_t/int32_t` five, mixed widths after that.
# l104 had already shown no library lemma reaches them. l107 generated the
# bridge from Sail's own Prelude and put all eight lemmas to Lean:
#
#   the four SIGNED   hold by `rfl`  -- they ARE the BitVec predicate
#   the four UNSIGNED hold by `simp` -- one rewrite away from it
#
# This lane changes ONE thing: `leanpath.equals.bridge_for` emits into each
# theorem file the bridge lemmas that file's own closure calls for, and names
# them in the simp set. Nothing is re-selected, re-carved or re-walked --
# l105's pairs.json and its two walk.json files are read as they stand.
#
# A FILE CARRIES ITS OWN PROOF OF EVERY REWRITE IT USES. The lemmas are
# emitted, not imported, so nothing here rests on a module built elsewhere,
# and `equals`'s existing `#check` guard still fails loudly on a vanished
# name.
#
# Reads l105's run. Writes $A/runs/gate_bridge only. Budget: one hour.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan
export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
A=PseudoCoupHQ/Research/oracle/riscv/leanpath
P=/work/proof; PLIB=LeanIM
G0=$A/runs/gate_classes
G1=$A/runs/gate_bridge2; mkdir -p $G1
t0=$(date +%s)
for f in $G0/pairs.json $G0/gate.json $G0/walk_arch/walk.json $G0/walk_emul/walk.json; do
  [ -f "$f" ] || { echo "FLAG: missing $f -- lp3_l105 writes it"; exit 3; }
done
grep -q "def bridge_for" $A/leanpath/equals.py || { echo "FLAG: equals.py has no bridge_for"; exit 3; }

echo "[1/3] the bridge this run will use  ($(( $(date +%s) - t0 ))s)"
cd $A
python3 - <<'PY'
import sys
sys.path.insert(0, "PseudoCoupHQ/Research/oracle/riscv/leanpath")
from leanpath.equals import bridge_lemmas
lines, names = bridge_lemmas("/work/proof", "LeanIM")
print("  lemmas generated from the Prelude: %d" % len(names))
for n, d in names:
    print("    %-28s bridges %s" % (n, d))
if not names:
    print("  FLAG: the generator produced nothing"); raise SystemExit(3)
PY

echo "[2/3] the 35 that were UNDECIDED, again, with the bridge  ($(( $(date +%s) - t0 ))s)"
python3 -u - <<'PY' > $G1/equals.log 2>&1
import json, os, re, sys, time
from concurrent.futures import ThreadPoolExecutor
A = "PseudoCoupHQ/Research/oracle/riscv/leanpath"
sys.path.insert(0, A)
from leanpath import strip as ST
from leanpath.equals import equals, simp_set, bridge_for
P, PLIB = "/work/proof", "LeanIM"
G0, G1 = A + "/runs/gate_classes", A + "/runs/gate_bridge2"
OUT = G1 + "/equals"; os.makedirs(OUT, exist_ok=True)
lean_dir = os.path.join(P, PLIB)
header, closers = ST.header_of(lean_dir, PLIB)
clauses = {c["name"][len("execute_"):]: c for c in ST.clauses_of(lean_dir)}
defs_index = ST.emitted_defs(lean_dir)
lib_index = ST.library_index(P)
print("clauses %d; emitted definitions %d; lean-sail indexed %d"
      % (len(clauses), len(defs_index), len(lib_index)), flush=True)
if not lib_index:
    print("FLAG: empty library index. ABORT."); raise SystemExit(3)

prev = {r["unit"]: (r.get("abi") or {}).get("verdict")
        for r in json.load(open(G0 + "/gate.json"))["rows"]}
want = sorted(u for u, v in prev.items() if v == "UNDECIDED")
print("classes that were UNDECIDED: %d" % len(want), flush=True)

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

warch = {r["unit"]: r for r in json.load(open(G0 + "/walk_arch/walk.json"))["rows"]}
wemul = {r["unit"]: r for r in json.load(open(G0 + "/walk_emul/walk.json"))["rows"]}
pairs = {p["unit"]: p for p in json.load(open(G0 + "/pairs.json"))}

jobs, rows = [], []
for u in want:
    p = pairs.get(u)
    ra, re_ = warch.get("arch_" + u, {}), wemul.get("emul_" + u, {})
    if p is None or ra.get("verdict") != "CERTIFIED" or re_.get("verdict") != "CERTIFIED":
        continue
    F, Gx = ra["proposal"], re_["proposal"]
    unknowns = [v for v in ("a", "b", "c", "d") if re.search(r"\b%s\b" % v, F + " " + Gx)]
    bodies, heads = bodies_of(F, Gx)
    tag = re.sub(r"\W", "_", u)
    defs = simp_set(defs_index, heads, tag, bodies, F, Gx)
    closure = [F, Gx] + bodies + [defs_index.get(d, "") for d in defs]
    emit, names, drop = bridge_for(P, PLIB, closure)
    defs = [d for d in defs if d not in set(drop)]      # cannot unfold AND rewrite
    row = {"unit": u, "lang": p["lang"], "lhs_type": p["lhs_type"],
           "rhs_type": p["rhs_type"], "expression": p["expression"],
           "class_members": p["class_members"], "was": "UNDECIDED",
           "bridge_lemmas_used": names, "definitions_dropped": drop}
    rows.append(row)
    args = []
    for v in unknowns:
        t = p["lhs_type"] if v == "a" else (p["rhs_type"] if v == "b" else None)
        args.append(widen(t, v))
    jobs.append((row, emit + bodies, tag + "_abi", unknowns,
                 at_width(F, unknowns, args, p["result_bits"]),
                 at_width(Gx, unknowns, args, p["result_bits"]),
                 defs + names))
n_with = sum(1 for r in rows if r["bridge_lemmas_used"])
print("reaching equals: %d; of those the bridge applies to: %d"
      % (len(jobs), n_with), flush=True)

def run(j):
    row, bodies, tag, unknowns, L, R, defs = j
    t = time.time()
    r = equals(P, header, closers, bodies, tag, unknowns, L, R, defs, OUT, 180)
    r["wall"] = round(time.time() - t, 1)
    return row, r

pool = ThreadPoolExecutor(max_workers=4)
moved = []
for row, r in pool.map(run, jobs):
    row["abi"] = r
    if r["verdict"] == "PROVED":
        moved.append(row)
    print("  %-30s %-9s %-14s %5.1fs  bridge=%-2d covers %d"
          % (row["unit"], r["verdict"], r["stage"], r["wall"],
             len(row["bridge_lemmas_used"]), row["class_members"]), flush=True)
pool.shutdown()
fh = open(G1 + "/gate.json", "w")
json.dump({"rows": rows}, fh, indent=1, sort_keys=True); fh.write("\n"); fh.close()

import collections
v = collections.Counter((r.get("abi") or {}).get("verdict") for r in rows)
print()
print("OF THE %d THAT WERE UNDECIDED:" % len(rows))
for k, n in v.most_common():
    cov = sum(r["class_members"] for r in rows if (r.get("abi") or {}).get("verdict") == k)
    print("  %-12s %3d classes  covering %3d arch-units" % (k, n, cov))
print()
print("MOVED by the bridge: %d classes, %d arch-units"
      % (len(moved), sum(r["class_members"] for r in moved)))
bad = [r for r in rows for t in (r.get("abi") or {}).get("tried") or []
       for e in t.get("errors") or []
       if "unknown identifier" in e or "unknown constant" in e]
print("guard: %s" % ("FLAG -- a name did not elaborate" if bad else "clean"))
PY
tail -28 $G1/equals.log

echo "[3/3] the gate as a whole, after  ($(( $(date +%s) - t0 ))s)"
python3 - <<'PY'
import json, collections
A = "PseudoCoupHQ/Research/oracle/riscv/leanpath"
base = {r["unit"]: r for r in json.load(open(A + "/runs/gate_classes/gate.json"))["rows"]}
try:
    after = {r["unit"]: r for r in json.load(open(A + "/runs/gate_bridge/gate.json"))["rows"]}
except Exception:
    after = {}
tot = collections.Counter()
cov = collections.Counter()
for u, r in base.items():
    v = (after.get(u, {}).get("abi") or r.get("abi") or {}).get("verdict")
    tot[v] += 1
    cov[v] += r["class_members"]
n = sum(tot.values()); c = sum(cov.values())
print("  186 integer-layer classes, %d arch-units:" % c)
for k in ("PROVED", "UNDECIDED", "NOT REACHED"):
    print("    %-12s %3d classes  %4d arch-units  (%.0f%%)"
          % (k, tot.get(k, 0), cov.get(k, 0), 100.0 * cov.get(k, 0) / c))
PY
echo "wall=$(( $(date +%s) - t0 ))s"
echo done
