#!/bin/bash
# lp3_l102_emul_gate_through_the_one_simp_set.sh
#
# THE GATE AGAIN, on the SAME twelve pairs l97 carved and the SAME walks l100
# certified. Nothing is re-selected, re-carved or re-walked: $G0/pairs.json,
# $G0/compiled.json and $G1/walk_{arch,emul}/walk.json are read as they stand.
#
# WHY IT IS BEING RUN AGAIN. l100 reported four of twenty PROVED and sixteen
# UNDECIDED. That number was measured against code that had already been
# superseded. `leanpath/equals.py` says so in `simp_set`'s own docstring:
#
#   "This was three copies -- two here and a third in a lane's heredoc -- and
#    on 2026-09-16 a fix landed in one of them while the gate ran another, so
#    the run reported UNDECIDED against code that had not changed."
#
# l100's heredoc carried its own `bodies_and_defs`, which assembles the simp
# set in TWO layers: the emitted definitions the text reaches, and the
# lean-sail helpers those call. Lane l101 then measured what `bv_decide`
# actually accepts -- eighteen probes, eleven proved, seven refused -- and
# added the THIRD layer to the module as `CORE_NORMALISE` / `core_normalise`:
# Lean's own rewrites for the terms the first two layers leave outside the
# BitVec fragment.
#
#   BitVec.zero n     `BitVec.zero_eq`                    (probes z0 z3 z5)
#   an Int-derived    `Int.toNat_natCast`                 (probe  s1)
#   shift
#   an Int comparison `Int.ofNat_lt`, `← BitVec.lt_def`,
#                     `BitVec.ult_iff_lt`                 (probes i0 h1)
#
# That third layer has never been run against the gate. This lane changes ONE
# thing and measures it: the simp set comes from `leanpath.equals.simp_set` --
# the one place -- instead of from a copy inside this script. Every other line
# of the driver is l100's.
#
# `zero_reg` (probe u0) is NOT a core lemma and is not treated as one: it is an
# emitted definition, and l100's seeding fix (`seed = pure_text + F + G`) is
# what reaches it. That fix is inside `simp_set` too, so it rides here as well.
#
# WHAT WOULD MAKE THIS LANE A LIE. `try simp only [...]` swallows the
# elaboration error of an unknown identifier and then skips the WHOLE set, so a
# stale lemma name reads exactly like hard mathematics. `equals` emits a
# `#check` per injected core lemma for that reason. This lane fails loudly on
# any `#check` error rather than reporting a verdict over it.
#
# Fetches nothing. Writes $A/runs/gate_emul_norm only. Budget: twenty minutes.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan
export PATH=$ELAN_HOME/bin:/opt/elan/bin:/opt/cargo/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
A=PseudoCoupHQ/Research/oracle/riscv/leanpath
OP=PseudoCoupHQ/Research/op_pipeline
P=/work/proof; PLIB=LeanIM
G0=$A/runs/gate_emul          # l97/l98's carve, read only
G1=$A/runs/gate_emul_fix      # l100's walks and verdicts, read only
G2=$A/runs/gate_emul_norm     # this lane's, written
cd $A; mkdir -p $G2; t0=$(date +%s)

echo "[1/4] inputs and the built tree  ($(( $(date +%s) - t0 ))s)"
for f in $G0/pairs.json $G0/compiled.json $G1/walk_arch/walk.json $G1/walk_emul/walk.json $G1/gate.json; do
  [ -f $f ] || { echo "  FLAG: missing $f -- this lane re-measures, it does not re-carve"; exit 3; }
  echo "  present: $f"
done
if [ -f $P/.lake/packages/Sail/Sail/Common.lean ]; then
  echo "  proof project is a built tree: $P"
else
  echo "  FLAG: $P has no .lake/packages/Sail/Sail/Common.lean -- not a built tree."
  for d in /persist/lp1/Lean_IMZ /persist/lp1/Lean_IM_6266b40c_all; do
    [ -f $d/.lake/packages/Sail/Sail/Common.lean ] && echo "    built tree available: $d"
  done
  exit 3
fi

echo "[2/4] the three layers the module assembles, named before the run  ($(( $(date +%s) - t0 ))s)"
python3 - <<'PY'
import sys
sys.path.insert(0, "PseudoCoupHQ/Research/oracle/riscv/leanpath")
from leanpath.equals import CORE_NORMALISE
print("  layer 3, CORE_NORMALISE as the module carries it:")
for term, lemmas in CORE_NORMALISE:
    print("    %-16s -> %s" % (term, ", ".join(lemmas)))
PY

echo "[3/4] equals, simp set from leanpath.equals.simp_set  ($(( $(date +%s) - t0 ))s)"
python3 -u - <<'PY' > $G2/equals.log 2>&1
import json, os, re, sys, time
from concurrent.futures import ThreadPoolExecutor
A = "PseudoCoupHQ/Research/oracle/riscv/leanpath"
sys.path.insert(0, A)
from leanpath import strip as ST
from leanpath.equals import equals, simp_set          # THE ONE PLACE
P, PLIB = "/work/proof", "LeanIM"
G0 = A + "/runs/gate_emul"
G1 = A + "/runs/gate_emul_fix"
G2 = A + "/runs/gate_emul_norm"
OUT = G2 + "/equals"; os.makedirs(OUT, exist_ok=True)

lean_dir = os.path.join(P, PLIB)
header, closers = ST.header_of(lean_dir, PLIB)
clauses = {c["name"][len("execute_"):]: c for c in ST.clauses_of(lean_dir)}
defs_index = ST.emitted_defs(lean_dir)
lib_index = ST.library_index(P)
print("clauses %d; emitted definitions %d; lean-sail definitions indexed %d"
      % (len(clauses), len(defs_index), len(lib_index)), flush=True)
if not lib_index:
    print("FLAG: the library index is empty; every simp set would omit every helper. ABORT.")
    raise SystemExit(3)

def clause_of(head):
    if head in clauses:
        return clauses[head]
    parts = head.split("_")
    for k in range(len(parts) - 1, 0, -1):
        nm = "_".join(parts[:k])
        if nm in clauses:
            return clauses[nm]
    return None

def bodies_of(F, Gx):
    """l100's body assembly, unchanged. The DEFS are no longer built here."""
    heads = sorted(set(re.findall(r"pure_(\w+)", F + " " + Gx)))
    bodies, seen = [], set()
    for h in heads:
        cl = clause_of(h)
        if cl is None or cl["name"] in seen:
            continue
        seen.add(cl["name"])
        prop = ST.propose(cl)
        if "refused" in prop:
            prop = ST.propose_effects(cl, defs_index)
        if "refused" in prop:
            continue
        bodies += ST.lean_body(cl, prop)
    return bodies, heads

# the psABI widening of one holder, written in BitVec 64 with masks, xor and
# subtraction only -- (x ^ 2^31) - 2^31 over the low 32 bits is the sign
# extension, and a mask is the zero extension
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

warch = {r["unit"]: r for r in json.load(open(G1 + "/walk_arch/walk.json"))["rows"]}
wemul = {r["unit"]: r for r in json.load(open(G1 + "/walk_emul/walk.json"))["rows"]}
pairs = json.load(open(G0 + "/pairs.json"))
comp  = json.load(open(G0 + "/compiled.json"))
prev = {}
for r in json.load(open(G1 + "/gate.json"))["rows"]:
    prev[r["unit"]] = {k: (r.get(k) or {}).get("verdict") for k in ("plain", "abi")}
    prev[r["unit"]]["defs"] = r.get("defs") or []

jobs, rows = [], []
for p in pairs:
    u = p["unit"]
    ra, re_ = warch.get("arch_" + u, {}), wemul.get("emul_" + u, {})
    row = {"unit": u, "lang": p["lang"], "n": p["n"], "operator": p["operator"],
           "lhs_type": p["lhs_type"], "rhs_type": p["rhs_type"], "expression": p["expression"],
           "result_bits": p["result_bits"],
           "arch_instructions": comp[u]["arch"].get("instructions"),
           "emul_instructions": comp[u]["emul"].get("instructions"),
           "arch_walk": ra.get("verdict"), "emul_walk": re_.get("verdict"),
           "previous": {k: v for k, v in (prev.get(u) or {}).items() if k != "defs"}}
    rows.append(row)
    if ra.get("verdict") != "CERTIFIED" or re_.get("verdict") != "CERTIFIED":
        row["plain"] = {"verdict": "NOT REACHED", "stage": "walk"}
        row["abi"]   = {"verdict": "NOT REACHED", "stage": "walk"}
        continue
    F, Gx = ra["proposal"], re_["proposal"]
    unknowns = [v for v in ("a", "b", "c", "d") if re.search(r"\b%s\b" % v, F + " " + Gx)]
    bodies, heads = bodies_of(F, Gx)
    tag = re.sub(r"\W", "_", u)
    # THE ONE CHANGE. Three layers, from the module, not from a copy here.
    defs = simp_set(defs_index, heads, tag, bodies, F, Gx)
    row["heads"], row["defs"] = heads, defs
    # what layer 3 added over what l100 ran with, per unit
    row["defs_added_vs_l100"] = [d for d in defs if d not in (prev.get(u, {}).get("defs") or [])]
    args = []
    for v in unknowns:
        t = p["lhs_type"] if v == "a" else (p["rhs_type"] if v == "b" else None)
        args.append(widen(t, v))
    row["abi_args"] = dict(zip(unknowns, args))
    jobs.append((row, "plain", bodies, tag + "_plain", unknowns, F, Gx, defs))
    jobs.append((row, "abi", bodies, tag + "_abi", unknowns,
                 at_width(F, unknowns, args, p["result_bits"]),
                 at_width(Gx, unknowns, args, p["result_bits"]), defs))

print("pairs reaching equals: %d; theorems to put: %d" % (len(jobs) // 2, len(jobs)), flush=True)

def run(j):
    row, kind, bodies, tag, unknowns, L, R, defs = j
    t = time.time()
    r = equals(P, header, closers, bodies, tag, unknowns, L, R, defs, OUT, 90)
    r["wall"] = round(time.time() - t, 1)
    r["lhs"] = L[:600]; r["rhs"] = R[:600]
    return row, kind, r

pool = ThreadPoolExecutor(max_workers=4)
moved = []
for row, kind, r in pool.map(run, jobs):
    row[kind] = r
    was = (row.get("previous") or {}).get(kind)
    mark = ""
    if was == "UNDECIDED" and r["verdict"] == "PROVED":   mark = "  <-- MOVED"; moved.append((row["unit"], kind))
    if was == "PROVED" and r["verdict"] != "PROVED":      mark = "  <-- LOST"
    print("  %-28s %-5s  was %-9s now %-9s %-14s %5.1fs  +defs %d%s"
          % (row["unit"], kind, was, r["verdict"], r["stage"], r["wall"],
             len(row.get("defs_added_vs_l100") or []), mark), flush=True)
pool.shutdown()

# the guard: a `#check` error means a lemma name no longer elaborates and the
# ENTIRE simp set was skipped -- every verdict above would be over nothing
bad = []
for row in rows:
    for kind in ("plain", "abi"):
        for t in (row.get(kind) or {}).get("tried") or []:
            for e in t.get("errors") or []:
                if "unknown identifier" in e or "unknown constant" in e:
                    bad.append((row["unit"], kind, e[:160]))
print()
if bad:
    print("FLAG: a #check did not elaborate; the simp set was skipped and these verdicts mean nothing:")
    for u, k, e in bad[:12]: print("   %-28s %-5s %s" % (u, k, e))
else:
    print("guard clean: every injected core lemma elaborated")

n_pr = sum(1 for r in rows for k in ("plain", "abi") if (r.get(k) or {}).get("verdict") == "PROVED")
n_to = sum(1 for r in rows for k in ("plain", "abi") if (r.get(k) or {}).get("verdict") not in (None, "NOT REACHED"))
print("TOTAL proved %d of %d   (l100 was 4 of 20)   moved: %s" % (n_pr, n_to, moved or "none"))

fh = open(G2 + "/gate.json", "w"); json.dump({"rows": rows}, fh, indent=1, sort_keys=True); fh.write("\n"); fh.close()
print("wrote %s/gate.json" % G2)
PY
tail -45 $G2/equals.log

echo "[4/4] residuals for anything still UNDECIDED at fixed_width  ($(( $(date +%s) - t0 ))s)"
# bv_decide says two very different things and they must not be read as one:
#   "found a counterexample"                 -- the goal is FALSE
#   "found a POTENTIALLY SPURIOUS counterexample" -- a subterm stayed an opaque
#                                               atom; a normalisation gap, not a disproof
R=$G2/residuals; mkdir -p $R
python3 - <<'PY' > $R/still.txt
import json
G2 = "PseudoCoupHQ/Research/oracle/riscv/leanpath/runs/gate_emul_norm"
for r in json.load(open(G2 + "/gate.json"))["rows"]:
    for k in ("plain", "abi"):
        v = (r.get(k) or {}).get("verdict")
        if v not in (None, "PROVED", "NOT REACHED"):
            print("%s_%s" % (r["unit"].replace("-", "_"), k))
PY
n=$(wc -l < $R/still.txt)
echo "  still not proved: $n"
i=0
while read -r f; do
  [ -z "$f" ] && continue
  i=$((i+1))
  src=$G2/equals/Equals_${f}_fixed_width.lean
  [ -f "$src" ] || { echo "  [$i/$n] $f  (no fixed_width file)"; continue; }
  timeout 180 lake env lean "$src" > $R/$f.txt 2>&1
  cls=$(grep -c "potentially spurious" $R/$f.txt 2>/dev/null || echo 0)
  cex=$(grep -c "found a counterexample" $R/$f.txt 2>/dev/null || echo 0)
  echo "  [$i/$n] $f  spurious=$cls  real_counterexample=$cex"
  grep -A6 "abstracted the following unsupported expressions" $R/$f.txt 2>/dev/null | head -8 | cut -c1-220 | sed 's/^/        /'
done < $R/still.txt

for f in $G2/gate.json; do
  [ -f $f ] && python3 $OP/check_no_spelling_keys.py $f 2>&1 | tail -1
done
echo "wall=$(( $(date +%s) - t0 ))s"
echo done
