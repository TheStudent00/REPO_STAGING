#!/bin/bash
# lp3_l98_emul_gate_walk_both_sides_and_equals.sh
#
# THE GATE, read before anything wider runs. Nothing wider runs after it
# until a person has read its table.
#
# THE CLAIM UNDER TEST. `arch_units/` holds 492 emulations of arch-units,
# every one tested against its own native operator and never proved. The
# claim is: the emulation computes the same thing as the arch-unit it
# emulates. The four steps, on twelve units picked by stride in l97:
#
#   1. recompile the ORIGINAL compiler-operator for riscv64 at the census
#      ship flags (attest_rv.json stores mnemonics, not encodings)
#   2. compile the emulation the same way
#   3. walk both to a Lean expression -- Sail's own decoder on each word,
#      Sail's own `execute` composed through the registers, certified by
#      Lean
#   4. prove the two expressions equal, in the stages LeanExpr.equals
#      already has: the same text, the integer level, fixed width
#
# TWO STATEMENTS ARE PUT, NOT ONE, and both are reported.
#
#   PLAIN   F = G as functions of the 64-bit argument registers. This is
#           the literal claim and it is what the machinery proves by
#           default.
#   AS THE ABI PRESENTS IT   the same equality with each argument replaced
#           by the widening the psABI performs on that holder before the
#           call (a signed 32-bit holder sign-extended, a bool zero-
#           extended to one bit, a 64-bit holder untouched), and both sides
#           read at the result's own width. This is weaker, and it is
#           stated separately and never merged into the plain count.
#
#   Why both: the emulation is a function of an operand BIT PATTERN and
#   re-performs the ABI widening itself and masks its answer to the result
#   width (arch_units/README.md, "What the answer is"); the arch-unit
#   assumes the widening already happened and leaves a0 in whatever form
#   the psABI left it (README divergence 5: go leaves a 32-bit answer
#   non-canonical, measured on all 141 narrow-result units). So the two
#   conventions differ at the edges of the register and the plain
#   statement can be false where the ABI statement is true. Reporting one
#   without the other would be dishonest in either direction.
#
# The widening term uses only masks, xor and subtraction over BitVec 64,
# so nothing is assumed about a library function's name.
#
# Nothing here selects, groups or pairs by an operator token: the twelve
# come from l97's pairs.json, paired by the arch-unit record's own `name`.
#
# Fetches nothing. Writes $A/runs/gate_emul only. Budget: fifteen minutes.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan
export PATH=$ELAN_HOME/bin:/opt/elan/bin:/opt/cargo/bin:/usr/lib/go-1.26/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
export GOCACHE=/work/gocache GOPATH=/work/gopath GOFLAGS=-mod=mod
A=PseudoCoupHQ/Research/oracle/riscv/leanpath
OP=PseudoCoupHQ/Research/op_pipeline
P=/work/proof; X=/work/Lean_IM_pr_exec; PLIB=LeanIM
S=$A/strip_perarm/strip.json
G=$A/runs/gate_emul
cd $A; t0=$(date +%s)
[ -f $G/pairs.json ] || { echo "FLAG: l97 did not run; no $G/pairs.json"; exit 3; }

export WALK_JOBS=4 WALK_MAX_WORDS=300

echo "[1/4] step 3a -- the twelve ARCH-UNITS walked (the original compiler-operator, recompiled)  ($(( $(date +%s) - t0 ))s)"
python3 -u -m leanpath walk $P $X $PLIB $S $G/units_arch.json $G/walk_arch 600 > $G/walk_arch.log 2>&1
echo "  rc=$? wall=$(( $(date +%s) - t0 ))s"
grep -E "decode:|CERTIFIED|REFUSED|FAILED|walk:" $G/walk_arch.log | cut -c1-190

echo "[2/4] step 3b -- the twelve EMULATIONS walked  ($(( $(date +%s) - t0 ))s)"
python3 -u -m leanpath walk $P $X $PLIB $S $G/units_emul.json $G/walk_emul 600 > $G/walk_emul.log 2>&1
echo "  rc=$? wall=$(( $(date +%s) - t0 ))s"
grep -E "decode:|CERTIFIED|REFUSED|FAILED|walk:" $G/walk_emul.log | cut -c1-190

echo "[3/4] step 4 -- equals over each pair, both statements  ($(( $(date +%s) - t0 ))s)"
python3 -u - <<'PY' > $G/equals.log 2>&1
import json, os, re, sys, time
from concurrent.futures import ThreadPoolExecutor
A = "PseudoCoupHQ/Research/oracle/riscv/leanpath"
sys.path.insert(0, A)
from leanpath import strip as ST
from leanpath.equals import equals
P, PLIB = "/work/proof", "LeanIM"
G = A + "/runs/gate_emul"
OUT = G + "/equals"; os.makedirs(OUT, exist_ok=True)
BUDGET = 60

lean_dir = os.path.join(P, PLIB)
header, closers = ST.header_of(lean_dir, PLIB)
clauses = {c["name"][len("execute_"):]: c for c in ST.clauses_of(lean_dir)}
defs_index = ST.emitted_defs(lean_dir)
print("clauses %d; emitted definitions %d" % (len(clauses), len(defs_index)), flush=True)

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
    defs += [d for d in ST.reachable(defs_index, pure_text) if d not in defs]
    defs += [d for d in ST.library_refs(defs_index, defs, extra_texts=[pure_text]) if d not in defs]
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

warch = {r["unit"]: r for r in json.load(open(G + "/walk_arch/walk.json"))["rows"]}
wemul = {r["unit"]: r for r in json.load(open(G + "/walk_emul/walk.json"))["rows"]}
pairs = json.load(open(G + "/pairs.json"))
comp = json.load(open(G + "/compiled.json"))

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
           "arch_proposal": ra.get("proposal"), "emul_proposal": re_.get("proposal")}
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
    print("  %-28s %-5s %-9s %-14s %5.1fs" % (row["unit"], kind, r["verdict"], r["stage"], r["wall"]), flush=True)
pool.shutdown()

fh = open(G + "/gate.json", "w"); json.dump({"rows": rows}, fh, indent=1, sort_keys=True); fh.write("\n"); fh.close()
print("wrote %s/gate.json" % G)
PY
tail -40 $G/equals.log
echo "  wall=$(( $(date +%s) - t0 ))s"
for f in $G/walk_arch/walk.json $G/walk_emul/walk.json $G/gate.json; do
  [ -f $f ] && python3 $OP/check_no_spelling_keys.py $f 2>&1 | tail -1
done

echo "[4/4] the table, and every cause in full  ($(( $(date +%s) - t0 ))s)"
python3 - <<'PY'
import json
G = "PseudoCoupHQ/Research/oracle/riscv/leanpath/runs/gate_emul"
d = json.load(open(G + "/gate.json"))["rows"]
print()
print("| unit | operator | operand types | arch instr | emul instr | arch walked | emul walked | proved plain | by stage | proved as the ABI presents it | by stage |")
print("|---|---|---|---:|---:|---|---|---|---|---|---|")
for r in d:
    pl, ab = r.get("plain", {}), r.get("abi", {})
    print("| %s | `%s` | %s %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
        r["unit"], r["operator"], r["lhs_type"], r["rhs_type"] or "",
        r["arch_instructions"], r["emul_instructions"],
        r["arch_walk"], r["emul_walk"],
        pl.get("verdict"), pl.get("stage"), ab.get("verdict"), ab.get("stage")))
print()
n = len(d)
print("of %d: arch walked %d, emulation walked %d, both %d; proved PLAIN %d; proved AS THE ABI PRESENTS IT %d" % (
    n, sum(r["arch_walk"] == "CERTIFIED" for r in d), sum(r["emul_walk"] == "CERTIFIED" for r in d),
    sum(r["arch_walk"] == "CERTIFIED" and r["emul_walk"] == "CERTIFIED" for r in d),
    sum(r.get("plain", {}).get("verdict") == "PROVED" for r in d),
    sum(r.get("abi", {}).get("verdict") == "PROVED" for r in d)))
print()
for r in d:
    print("---- %s  (%s `%s` %s %s)" % (r["unit"], r["lang"], r["operator"], r["lhs_type"], r["rhs_type"] or ""))
    print("  arch  %-9s %s" % (r["arch_walk"], (r["arch_proposal"] or r["arch_why"])[:400]))
    print("  emul  %-9s %s" % (r["emul_walk"], (r["emul_proposal"] or r["emul_why"])[:400]))
    for kind in ("plain", "abi"):
        e = r.get(kind, {})
        if e.get("verdict") == "PROVED":
            print("  %-5s PROVED at stage %s" % (kind, e["stage"]))
        elif e.get("verdict") == "UNDECIDED":
            last = (e.get("tried") or [{}])[-1]
            print("  %-5s UNDECIDED; last stage %s; lean said:" % (kind, last.get("stage")))
            for x in (last.get("errors") or ["(no error line)"])[:3]:
                print("        " + x[:320])
            print("        file %s" % last.get("lean_file"))
        else:
            print("  %-5s %s (%s)" % (kind, e.get("verdict"), e.get("stage")))
PY
echo "gate wall seconds=$(( $(date +%s) - t0 ))"
echo done
