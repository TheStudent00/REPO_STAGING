#!/bin/bash
# lp3_l100_emul_gate_seed_the_statement_and_index_the_library.sh
#
# THE GATE AGAIN, on the SAME twelve pairs l97 carved, against two path and
# seeding faults found after l98/l99. Nothing is re-selected and nothing is
# re-carved: $G0/pairs.json, $G0/units_arch.json and $G0/units_emul.json are
# read as they stand. The new artifacts go to $G1 so l98's remain readable
# beside them.
#
# WHAT l98 REPORTED, AND WHY IT WAS NOT A PROVING LIMIT. Six of the twelve
# came back UNDECIDED in BOTH statements, and the residual l99 printed says
# what actually happened, in bv_decide's own words:
#
#   "The prover found a potentially spurious counterexample:
#    - It abstracted the following unsupported expressions as opaque
#      variables: [shift_bits_left (...) 0#2, zero_reg]"
#
# Two symbols, two separate faults, neither of them mathematics:
#
#   1. `zero_reg` IS AN EMITTED DEFINITION THAT APPEARS ONLY IN THE THEOREM
#      STATEMENT. The emulation side walked to `pure_ZBA_RTYPEUW (a)
#      (zero_reg) (0b00#2)` -- the constant rides in the operand list, not in
#      any pure BODY. l98 seeded `reachable` and `library_refs` with the pure
#      bodies alone, so nothing ever looked at the statement and `zero_reg`
#      never entered the `simp only` set. FIX: seed with the bodies AND both
#      sides of the equality, `seed = pure_text + F + G`. This is the change
#      already made at both defs-assembly sites inside leanpath/equals.py
#      (its corpus driver); this lane carries its own assembly and had to
#      have the same change made here.
#
#   2. `shift_bits_left` IS A LEAN-SAIL DEFINITION AND THE INDEX OF THEM WAS
#      EMPTY. It is `Sail.shift_bits_left`, at .lake/packages/Sail/Sail/
#      Common.lean:185, and the emit calls it unqualified under `open Sail`.
#      `strip.library_refs` can only reach an unqualified name through the
#      module-global LIBRARY_INDEX, and that global is populated by ONE call,
#      `strip.library_index(project)`. l98 never made that call -- and a walk
#      in a separate process making it does not carry across processes. So
#      the index was {} and every library helper was silently dropped from
#      every simp set. FIX: call it here, first, and print what it indexed.
#      strip.library_index now also writes a loud WARNING to stderr when it
#      indexes nothing; step [1] below aborts the lane on that, because a run
#      with an empty index reports UNDECIDED for a path fault and is void.
#
# The simp set l98 actually generated, from the file on disk
# ($G0/equals/Equals_au_182_c_pos_i32_plain_fixed_width.lean:231):
#
#   try simp only [pure_ZBA_RTYPEUW, zero_extend, Sail.BitVec.zeroExtend, Sail.BitVec.extractLsb]
#
# -- neither symbol present. Step [5] prints the same line from every file
# this lane writes, so the fix is read off the generated text, not asserted.
#
# EVERYTHING ELSE IS l98 UNCHANGED: the same four steps (the original
# compiler-operator recompiled, its emulation compiled, both walked to a Lean
# expression through Sail's own decoder and `execute`, the two proved equal in
# the stages LeanExpr.equals already has), the same TWO STATEMENTS put and
# both reported --
#
#   PLAIN   F = G as functions of the 64-bit argument registers.
#   AS THE ABI PRESENTS IT   the same equality with each argument replaced by
#           the widening the psABI performs on that holder before the call,
#           both sides read at the result's own width. Weaker; stated
#           separately; never merged into the plain count.
#
# -- the same budgets (90 s per stage, four at a time), the same WALK_JOBS=4
# and WALK_MAX_WORDS=300.
#
# A STILL-UNDECIDED PAIR MUST SAY WHICH SENTENCE bv_decide PRINTED. The
# four-line excerpt equals() keeps holds only the line with "error" in it, and
# both of bv_decide's very different verdicts start on that line:
# "a counterexample" (the goal is FALSE, and the assignment is a real input)
# against "a potentially spurious counterexample" (a subterm stayed an
# uninterpreted atom -- a normalisation gap, not a disproof). Step [6] re-runs
# every undecided fixed-width file, unchanged, and prints Lean's whole output.
#
# Nothing here selects, groups or pairs by an operator token: the twelve come
# from l97's pairs.json, paired by the record's own `unit` field.
#
# Fetches nothing. Writes $A/runs/gate_emul_fix only. Budget: fifteen minutes.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan
export PATH=$ELAN_HOME/bin:/opt/elan/bin:/opt/cargo/bin:/usr/lib/go-1.26/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
export GOCACHE=/work/gocache GOPATH=/work/gopath GOFLAGS=-mod=mod
A=PseudoCoupHQ/Research/oracle/riscv/leanpath
OP=PseudoCoupHQ/Research/op_pipeline
P=/work/proof; X=/work/Lean_IM_pr_exec; PLIB=LeanIM
S=$A/strip_perarm/strip.json
G0=$A/runs/gate_emul          # l98's, read only
G1=$A/runs/gate_emul_fix      # this lane's, written
cd $A; mkdir -p $G1; t0=$(date +%s)
[ -f $G0/pairs.json ] || { echo "FLAG: no $G0/pairs.json; l97 is the lane that writes it"; exit 3; }

export WALK_JOBS=4 WALK_MAX_WORDS=300

echo "[1/6] THE CRUX -- is the proof project a BUILT tree, and does the library index come back non-empty  ($(( $(date +%s) - t0 ))s)"
echo "  proof project: $P"
if [ -f $P/.lake/packages/Sail/Sail/Common.lean ]; then
  echo "  present: $P/.lake/packages/Sail/Sail/Common.lean"
  grep -n "^def shift_bits_left" $P/.lake/packages/Sail/Sail/Common.lean | sed 's/^/    /'
else
  echo "  FLAG: $P has no .lake/packages/Sail/Sail/Common.lean -- this is not a built tree."
  echo "  Built trees on this instance:"
  for d in /persist/lp1/Lean_IMZ /persist/lp1/Lean_IM_6266b40c_all; do
    [ -f $d/.lake/packages/Sail/Sail/Common.lean ] && echo "    $d"
  done
  exit 3
fi
grep -rn "^def zero_reg" $P/$PLIB/ | sed 's/^/  emitted: /'
python3 - <<'PY'
import sys
sys.path.insert(0, "PseudoCoupHQ/Research/oracle/riscv/leanpath")
from leanpath import strip as ST
idx = ST.library_index("/work/proof")
print("  lean-sail definitions indexed: %d" % len(idx))
for n in ("shift_bits_left", "zero_extend", "sign_extend"):
    print("    %-18s -> %s" % (n, idx.get(n)))
sys.exit(0 if idx else 3)
PY
rc=$?
[ $rc -eq 0 ] || { echo "  the WARNING above fired: the index is empty and the run would be void. ABORT."; exit 3; }

echo "  the simp set the two fixes produce, assembled here over l98's OWN walk proposals, before any Lean runs:"
python3 - <<'PY'
import json, os, re, sys
A = "PseudoCoupHQ/Research/oracle/riscv/leanpath"
sys.path.insert(0, A)
from leanpath import strip as ST
P, PLIB = "/work/proof", "LeanIM"
lean_dir = os.path.join(P, PLIB)
clauses = {c["name"][len("execute_"):]: c for c in ST.clauses_of(lean_dir)}
defs_index = ST.emitted_defs(lean_dir)
ST.library_index(P)
rows = json.load(open(A + "/runs/gate_emul/gate.json"))["rows"]
r = [x for x in rows if x["unit"] == "au_182_c_pos_i32"][0]
F, Gx = r["arch_proposal"], r["emul_proposal"]
print("    F (the arch-unit)  %s" % F)
print("    G (the emulation)  %s" % Gx)
heads = sorted(set(re.findall(r"pure_(\w+)", F + " " + Gx)))
bodies = []
for h in heads:
    cl = clauses.get(h)
    if cl is None:
        parts = h.split("_")
        for k in range(len(parts) - 1, 0, -1):
            if "_".join(parts[:k]) in clauses:
                cl = clauses["_".join(parts[:k])]; break
    if cl is None:
        continue
    prop = ST.propose(cl)
    if "refused" in prop:
        prop = ST.propose_effects(cl, defs_index)
    if "refused" in prop:
        continue
    bodies += ST.lean_body(cl, prop)
pure_text = "\n".join(re.findall(r"^def pure_.*?(?=^theorem|\Z)", "\n".join(bodies), re.S | re.M))
idx = dict(ST.LIBRARY_INDEX)
# the two faults isolated: the seed on one axis, the library index on the other
for label, seed, index in (
        ("l98 as it ran: bodies only, no index", pure_text, {}),
        ("the seed fix alone",                   "\n".join([pure_text, F, Gx]), {}),
        ("the index fix alone",                  pure_text, idx),
        ("BOTH, which is this lane",             "\n".join([pure_text, F, Gx]), idx)):
    ST.LIBRARY_INDEX = index
    defs = ["pure_%s" % h for h in heads]
    defs += [d for d in ST.reachable(defs_index, seed) if d not in defs]
    defs += [d for d in ST.library_refs(defs_index, defs, extra_texts=[seed]) if d not in defs]
    print("    %-38s zero_reg %-7s shift_bits_left %-7s" % (label,
          "PRESENT" if "zero_reg" in defs else "ABSENT",
          "PRESENT" if any("shift_bits_left" in d for d in defs) else "ABSENT"))
    print("    %-38s simp only [%s]" % ("", ", ".join(defs)))
ST.LIBRARY_INDEX = idx
PY

echo "[2/6] step 3a -- the twelve ARCH-UNITS walked (the original compiler-operator, recompiled)  ($(( $(date +%s) - t0 ))s)"
python3 -u -m leanpath walk $P $X $PLIB $S $G0/units_arch.json $G1/walk_arch 600 > $G1/walk_arch.log 2>&1
echo "  rc=$? wall=$(( $(date +%s) - t0 ))s"
grep -E "decode:|CERTIFIED|REFUSED|FAILED|walk:" $G1/walk_arch.log | cut -c1-190

echo "[3/6] step 3b -- the twelve EMULATIONS walked  ($(( $(date +%s) - t0 ))s)"
python3 -u -m leanpath walk $P $X $PLIB $S $G0/units_emul.json $G1/walk_emul 600 > $G1/walk_emul.log 2>&1
echo "  rc=$? wall=$(( $(date +%s) - t0 ))s"
grep -E "decode:|CERTIFIED|REFUSED|FAILED|walk:" $G1/walk_emul.log | cut -c1-190

echo "[4/6] step 4 -- equals over each pair, both statements, with the statement seeded and the library indexed  ($(( $(date +%s) - t0 ))s)"
python3 -u - <<'PY' > $G1/equals.log 2>&1
import json, os, re, sys, time
from concurrent.futures import ThreadPoolExecutor
A = "PseudoCoupHQ/Research/oracle/riscv/leanpath"
sys.path.insert(0, A)
from leanpath import strip as ST
from leanpath.equals import equals
P, PLIB = "/work/proof", "LeanIM"
G0 = A + "/runs/gate_emul"
G1 = A + "/runs/gate_emul_fix"
OUT = G1 + "/equals"; os.makedirs(OUT, exist_ok=True)

lean_dir = os.path.join(P, PLIB)
header, closers = ST.header_of(lean_dir, PLIB)
clauses = {c["name"][len("execute_"):]: c for c in ST.clauses_of(lean_dir)}
defs_index = ST.emitted_defs(lean_dir)
# FAULT 2. Without this call the module-global LIBRARY_INDEX stays {} and
# `library_refs` cannot name one unqualified lean-sail helper. l98 omitted it.
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

def bodies_and_defs(F, Gx):
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
    defs = ["pure_%s" % h for h in heads]
    pure_text = "\n".join(re.findall(r"^def pure_.*?(?=^theorem|\Z)", "\n".join(bodies), re.S | re.M))
    # FAULT 1. The THEOREM STATEMENT names helpers no pure body mentions: the
    # emulation side carries constants in its operand list (`pure_ZBA_RTYPEUW a
    # zero_reg 0b00#2`), and `zero_reg` is an emitted definition nothing else
    # reaches. Seeding with F and G is what lets `simp only` turn it into a
    # literal; without it bv_decide abstracts it as an opaque variable and
    # returns a spurious counterexample. l98 seeded with pure_text alone.
    seed = "\n".join([pure_text, F, Gx])
    defs += [d for d in ST.reachable(defs_index, seed) if d not in defs]
    defs += [d for d in ST.library_refs(defs_index, defs, extra_texts=[seed]) if d not in defs]
    return bodies, defs, heads

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
comp = json.load(open(G0 + "/compiled.json"))
# l98's own verdicts, carried alongside so the two runs can be read in one table
prev = {}
if os.path.exists(G0 + "/gate.json"):
    for r in json.load(open(G0 + "/gate.json"))["rows"]:
        prev[r["unit"]] = {k: (r.get(k) or {}).get("verdict") for k in ("plain", "abi")}
        prev[r["unit"]]["arch_proposal"] = r.get("arch_proposal")
        prev[r["unit"]]["emul_proposal"] = r.get("emul_proposal")

jobs = []
rows = []
for p in pairs:
    u = p["unit"]
    ra, re_ = warch.get("arch_" + u, {}), wemul.get("emul_" + u, {})
    row = {"unit": u, "lang": p["lang"], "n": p["n"], "operator": p["operator"],
           "lhs_type": p["lhs_type"], "rhs_type": p["rhs_type"], "expression": p["expression"],
           "result_bits": p["result_bits"],
           "arch_instructions": comp[u]["arch"].get("instructions"),
           "emul_instructions": comp[u]["emul"].get("instructions"),
           "arch_walk": ra.get("verdict"), "emul_walk": re_.get("verdict"),
           "arch_why": (ra.get("why") or (ra.get("errors") or [""])[0])[:400],
           "emul_why": (re_.get("why") or (re_.get("errors") or [""])[0])[:400],
           "arch_proposal": ra.get("proposal"), "emul_proposal": re_.get("proposal"),
           "previous": prev.get(u, {})}
    # did the walk itself drift between the two runs? say so rather than let it pass
    pp = prev.get(u, {})
    row["walk_drift"] = [k for k in ("arch_proposal", "emul_proposal")
                         if pp.get(k) is not None and pp.get(k) != row[k]]
    rows.append(row)
    if ra.get("verdict") != "CERTIFIED" or re_.get("verdict") != "CERTIFIED":
        row["plain"] = {"verdict": "NOT REACHED", "stage": "walk"}
        row["abi"] = {"verdict": "NOT REACHED", "stage": "walk"}
        continue
    F, Gx = ra["proposal"], re_["proposal"]
    unknowns = [v for v in ("a", "b", "c", "d") if re.search(r"\b%s\b" % v, F + " " + Gx)]
    bodies, defs, heads = bodies_and_defs(F, Gx)
    tag = re.sub(r"\W", "_", u)
    row["heads"] = heads
    row["defs"] = defs
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
for row, kind, r in pool.map(run, jobs):
    row[kind] = r
    was = (row.get("previous") or {}).get(kind)
    print("  %-28s %-5s  was %-9s now %-9s %-14s %5.1fs"
          % (row["unit"], kind, was, r["verdict"], r["stage"], r["wall"]), flush=True)
pool.shutdown()

fh = open(G1 + "/gate.json", "w"); json.dump({"rows": rows}, fh, indent=1, sort_keys=True); fh.write("\n"); fh.close()
print("wrote %s/gate.json" % G1)
PY
tail -40 $G1/equals.log
echo "  wall=$(( $(date +%s) - t0 ))s"
for f in $G1/walk_arch/walk.json $G1/walk_emul/walk.json $G1/gate.json; do
  [ -f $f ] && python3 $OP/check_no_spelling_keys.py $f 2>&1 | tail -1
done

echo "[5/6] THE SIMP SET AS GENERATED -- the line read off every file this lane wrote that carries one  ($(( $(date +%s) - t0 ))s)"
echo '  (a pair proved by with_reducible rfl at the same-text stage generates no simp set at all; those files are absent by design)'
echo
echo "  the line from l98, and the line from this lane, on the pair whose residual named both symbols:"
grep -h "simp only \[pure_" $G0/equals/Equals_au_182_c_pos_i32_plain_fixed_width.lean 2>/dev/null | sed 's/^/    l98: /' | cut -c1-600
for s in fixed_width integer_level; do
  grep -h "simp only \[pure_" $G1/equals/Equals_au_182_c_pos_i32_plain_$s.lean 2>/dev/null | sed "s/^/    new ($s): /" | cut -c1-600
done
echo
echo "  does each generated file name BOTH symbols in its simp set?"
python3 - <<'PY'
import glob, os, re
G1 = "PseudoCoupHQ/Research/oracle/riscv/leanpath/runs/gate_emul_fix/equals"
fs = sorted(glob.glob(G1 + "/*_fixed_width.lean") + glob.glob(G1 + "/*_integer_level.lean"))
print("  | file | zero_reg in the simp set | a lean-sail shift in the simp set | names in the set |")
print("  |---|---|---|---:|")
for f in fs:
    txt = open(f).read()
    m = re.findall(r"^\s*try simp only \[(.*)\]\s*$", txt, re.M)
    s = m[-1] if m else ""
    names = [x.strip() for x in s.split(",")] if s else []
    print("  | %s | %s | %s | %d |" % (os.path.basename(f),
          "yes" if "zero_reg" in names else ("no" if "zero_reg" in txt else "n/a (statement does not name it)"),
          "yes" if any("shift_bits_left" in n for n in names) else ("no" if "shift_bits_left" in txt else "n/a (nothing shifts)"),
          len(names)))
if not fs:
    print("  (no file carries a simp set: every theorem closed at the same-text stage)")
PY
echo
echo "  and the full simp line of every such file, in full, no truncation:"
for f in $G1/equals/*_fixed_width.lean $G1/equals/*_integer_level.lean; do
  [ -f "$f" ] || continue
  echo "    ---- $(basename $f)"
  grep -h "simp only \[pure_" "$f" | sed 's/^/      /'
done

echo "[6/6] every still-undecided fixed-width file re-run, whole output, so the sentence bv_decide printed is on the record  ($(( $(date +%s) - t0 ))s)"
R=$G1/residuals; mkdir -p $R
cd $P
python3 - <<'PY' > /tmp/undecided.txt
import json
G1 = "PseudoCoupHQ/Research/oracle/riscv/leanpath/runs/gate_emul_fix"
for r in json.load(open(G1 + "/gate.json"))["rows"]:
    for kind in ("plain", "abi"):
        e = r.get(kind, {})
        if e.get("verdict") == "UNDECIDED":
            last = (e.get("tried") or [{}])[-1]
            p = last.get("lean_file")
            if p:
                print(p)
PY
i=0; total=$(wc -l < /tmp/undecided.txt)
echo "  still undecided: $total"
while read -r f; do
  i=$((i+1))
  b=$(basename "$f" .lean)
  echo "  ---- [$i/$total] $b"
  timeout 180 lake env lean "$f" > $R/$b.txt 2>&1
  echo "       rc=$? bytes=$(wc -c < $R/$b.txt)"
  grep -n "^theorem" "$f" | tail -1 | sed 's/^/       stated: /' | cut -c1-300
  grep -n "simp only \[pure_" "$f" | tail -1 | sed 's/^/       simp:   /' | cut -c1-400
  sed -n '1,40p' $R/$b.txt | sed 's/^/       /'
  echo
done < /tmp/undecided.txt
echo "gate wall seconds=$(( $(date +%s) - t0 ))"
echo done
