#!/bin/bash
# lp3_l97_emul_gate_preflight_compile_and_carve.sh
#
# PREFLIGHT for the arch-unit-emulation gate. Nothing in Lean runs here.
#
# WHY: the gate proper (l98) runs the four steps -- recompile the original
# compiler-operator, compile its emulation, walk both to Lean expressions,
# prove the two equal -- on twelve arch-units in one lane under fifteen
# minutes. Two of those steps can be measured without Lean at all, and they
# are the two that decide whether the lane is worth submitting:
#
#   * does the WORKING COPY exist at all (/work/proof, /work/Lean_IM_pr_exec,
#     strip_perarm/strip.json)?  A gate submitted against a missing project
#     burns fifteen minutes to print a build error.
#   * how many instructions does each side actually have, and does either
#     side branch or call?  The walk composes STRAIGHT-LINE bodies only
#     (arch_unit.branch_rule and .memory_and_calls are refusals by design),
#     so an emulation that compiles to a loop is refused before Lean is
#     reached, and the count is one of the things the gate must report.
#
# THE TWELVE, by a rule over data, not by hand. The population is the 318
# arch-units of arch_units.json whose record carries layer == "integer" --
# the layer built from the bodies with no float instruction. (The brief said
# 483 of the 492; the file says 318 carry that layer and 174 carry a float
# instruction. 492 - 483 = 9 is the count of units emulated under a stated
# reduction, `reduced` in the record. The larger number is reported back.)
# The population is sorted by instruction count, ties by the unit's own
# index, and twelve are taken at i*(N-1)/11 for i in 0..11, so the first and
# the last are both in and the set spans short and long. No operator token
# takes any part in the selection, the sort, or the pairing: the pairing is
# by the record's own `name` and `unit` fields. The token rides along once
# per unit as a display label, inside the unit object, where the guard
# allows it.
#
# THE EMULATION SIDE is taken in c for all twelve regardless of the
# arch-unit's own language: c is the emission the other three were compared
# against byte for byte (arch_units.json, cross_language_mismatches 0), and
# it compiles with the same ship line as the c probes.
#
# Fetches nothing. Writes $A/runs/gate_emul only.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan
export PATH=$ELAN_HOME/bin:/opt/elan/bin:/opt/cargo/bin:/usr/lib/go-1.26/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
export GOCACHE=/work/gocache GOPATH=/work/gopath GOFLAGS=-mod=mod
mkdir -p /work/gocache /work/gopath
A=PseudoCoupHQ/Research/oracle/riscv/leanpath
AU=PseudoCoupHQ/Research/oracle/riscv/softfloat_slices/arch_units
OP=PseudoCoupHQ/Research/op_pipeline
P=/work/proof; X=/work/Lean_IM_pr_exec
G=$A/runs/gate_emul
cd $A; mkdir -p $G; t0=$(date +%s)

echo "[1/4] the working copy, the evaluable build and the strip record  ($(( $(date +%s) - t0 ))s)"
for d in $P $X; do
  if [ -d "$d" ]; then echo "  present: $d"; else echo "  FLAG MISSING: $d"; fi
done
ls -1 $P/.lake/build/lib/lean/*/  2>/dev/null | head -5 | sed 's/^/    /'
PLIB=$(grep -A1 '\[\[lean_lib\]\]' $P/lakefile.toml 2>/dev/null | grep -oE 'name = "[^"]+"' | head -1 | cut -d'"' -f2)
echo "  proof lib name: ${PLIB:-<none>}"
if [ -f $A/strip_perarm/strip.json ]; then
  python3 -c "
import json,collections
d=json.load(open('$A/strip_perarm/strip.json'))
c=collections.Counter(r['verdict'] for r in d['rows'])
print('  strip_perarm/strip.json: %d rows, %s' % (len(d['rows']), dict(c)))
"
else
  echo "  FLAG MISSING: $A/strip_perarm/strip.json"; ls -d $A/strip_* | sed 's/^/    have: /'
fi
which clang go llvm-objdump 2>&1 | sed 's/^/  /'

echo "[2/4] the twelve, by stride over the integer layer sorted by instruction count  ($(( $(date +%s) - t0 ))s)"
python3 - <<'PY'
import json, os
AU = "PseudoCoupHQ/Research/oracle/riscv/softfloat_slices/arch_units"
OP = "PseudoCoupHQ/Research/op_pipeline"
G  = "PseudoCoupHQ/Research/oracle/riscv/leanpath/runs/gate_emul"
SHIP = {"c":   "clang -std=c17 -O1 --target=riscv64-unknown-linux-gnu -nostdlibinc",
        "go":  "GOARCH=riscv64 GOOS=linux go build"}
d = json.load(open(AU + "/arch_units.json"))
pop = [u for u in d["units"] if u.get("layer") == "integer"]
pop.sort(key=lambda u: (len(u["body"]), u["index"]))
N = len(pop)
picks = [pop[(i * (N - 1)) // 11] for i in range(12)]
man = {L: json.load(open("%s/probe_manifest_%s.json" % (OP, L))) for L in ("c", "go")}
probes = {L: {p["n"]: p for p in (m["probes"].values() if isinstance(m["probes"], dict) else m["probes"])}
          for L, m in man.items()}
src = os.path.join(G, "src"); os.makedirs(src, exist_ok=True)
arch, emul, pairs = [], [], []
for u in picks:
    L = u["lang"]
    n = int(u["symbol"].split("_")[-1])
    p = probes[L][n]
    ext = {"c": "c", "go": "go"}[L]
    ap = os.path.join(src, "arch_%s.%s" % (u["name"], ext))
    open(ap, "w").write(p["source"])
    sym = p["symbol"]
    if L == "go" and sym.startswith("main."):
        sym = sym[len("main."):]
    label = {"unit": u["name"], "lang": L, "n": n, "operator": u["operator"],
             "lhs_type": u["lhs_type"], "rhs_type": u["rhs_type"], "expression": u["expression"]}
    arch.append({"name": "arch_" + u["name"], "lang": L, "source": ap, "symbol": sym,
                 "flags": SHIP[L], "unit": u["name"],
                 "cell_display": "%s %s %s %s" % (L, u["operator"], u["lhs_type"], u["rhs_type"] or ""),
                 "probe": label})
    ep = u["languages"]["c"]["file"].split("arch_units/", 1)[1]        # c/au_NNN_....c
    emul.append({"name": "emul_" + u["name"], "lang": "c", "source": os.path.join(AU, ep),
                 "symbol": u["languages"]["c"]["entry"],
                 "flags": SHIP["c"] + " -I" + os.path.join(AU, "c"), "unit": u["name"],
                 "cell_display": "%s %s %s %s" % (L, u["operator"], u["lhs_type"], u["rhs_type"] or ""),
                 "probe": label})
    pairs.append({"unit": u["name"], "lang": L, "n": n, "operator": u["operator"],
                  "lhs_type": u["lhs_type"], "rhs_type": u["rhs_type"], "expression": u["expression"],
                  "arch_instructions": len(u["body"]), "arch_body": u["body"],
                  "result_bits": u["result_bits"], "result_type": u.get("result_type"),
                  "n_params": u["n_params"], "reduced": u["reduced"], "guarded": u.get("guarded"),
                  "emul_source": os.path.join(AU, ep), "emul_entry": u["languages"]["c"]["entry"],
                  "emul_source_lines": u["languages"]["c"]["source_lines"]})
for nm, doc in (("units_arch.json", arch), ("units_emul.json", emul), ("pairs.json", pairs)):
    fh = open(os.path.join(G, nm), "w"); json.dump(doc, fh, indent=1, sort_keys=True); fh.write("\n"); fh.close()
print("  population with layer == integer: %d; picked %d at i*(N-1)/11" % (N, len(picks)))
print("  | unit | lang | operand types | arch instructions | emulation source lines | result bits |")
print("  |---|---|---|---:|---:|---:|")
for r in pairs:
    print("  | %s | %s | %s %s | %d | %d | %d |" % (r["unit"], r["lang"], r["lhs_type"],
          r["rhs_type"] or "", r["arch_instructions"], r["emul_source_lines"], r["result_bits"]))
PY
python3 $OP/check_no_spelling_keys.py $G/units_arch.json 2>&1 | tail -2
python3 $OP/check_no_spelling_keys.py $G/units_emul.json 2>&1 | tail -2
python3 $OP/check_no_spelling_keys.py $G/pairs.json 2>&1 | tail -2

echo "[3/4] compile BOTH sides for riscv64 at the census ship flags and carve at the symbol  ($(( $(date +%s) - t0 ))s)"
python3 - <<'PY'
import json, os, sys, collections
A = "PseudoCoupHQ/Research/oracle/riscv/leanpath"
G = A + "/runs/gate_emul"
sys.path.insert(0, A)
from leanpath.walk import compile_unit, carve
# a branch or a call is what the walk refuses (arch_unit.branch_rule,
# .memory_and_calls); it is read off the disassembled operand form -- a
# target address in the operand field -- not off any name list
out = {}
work = os.path.join(G, "objs"); os.makedirs(work, exist_ok=True)
for side in ("arch", "emul"):
    units = json.load(open("%s/units_%s.json" % (G, side)))
    for u in units:
        obj = os.path.join(work, u["name"] + ".o")
        rc, secs, o, sym = compile_unit(u, obj, work)
        row = {"rc": rc, "seconds": round(secs, 1), "symbol": sym}
        if rc != 0:
            row["refusal"] = o.strip().split("\n")[-1][:200]
        else:
            crc, cout, body = carve(obj, sym)
            row["instructions"] = len(body)
            row["body"] = [("%s %s" % (m, ops)).strip() for _, m, ops in body]
            row["control_flow"] = [t for t in row["body"] if "<" in t or "0x" == t[:2]]
        out.setdefault(u["unit"], {})[side] = row
fh = open(G + "/compiled.json", "w"); json.dump(out, fh, indent=1, sort_keys=True); fh.write("\n"); fh.close()
pairs = json.load(open(G + "/pairs.json"))
print("  | unit | arch recompiled | matches the stored body | emulation compiled | emulation has a transfer of control |")
print("  |---|---:|---|---:|---|")
for p in pairs:
    r = out[p["unit"]]
    a, e = r["arch"], r["emul"]
    same = "n/a"
    if "body" in a:
        same = "yes" if a["body"] == p["arch_body"] else "NO"
    xfer = "n/a"
    if "body" in e:
        xfer = "yes: %d" % len(e["control_flow"]) if e["control_flow"] else "no"
    print("  | %s | %s | %s | %s | %s |" % (p["unit"],
          a.get("instructions", "refused"), same, e.get("instructions", "refused"), xfer))
print()
for p in pairs:
    r = out[p["unit"]]
    a, e = r["arch"], r["emul"]
    if "body" in a and a["body"] != p["arch_body"]:
        print("  DIFFERS from the stored body, %s:" % p["unit"])
        print("    stored:      " + " | ".join(p["arch_body"]))
        print("    recompiled:  " + " | ".join(a["body"]))
    for side, rr in (("arch", a), ("emul", e)):
        if "refusal" in rr:
            print("  %s %s compile refused: %s" % (p["unit"], side, rr["refusal"]))
print("  emulation instruction counts: %s" % sorted(
    (out[p["unit"]]["emul"].get("instructions", -1), p["unit"]) for p in pairs))
PY

echo "[4/4] the emulation bodies in full, so the gate's refusals can be read against them  ($(( $(date +%s) - t0 ))s)"
python3 - <<'PY'
import json
G = "PseudoCoupHQ/Research/oracle/riscv/leanpath/runs/gate_emul"
c = json.load(open(G + "/compiled.json"))
for p in json.load(open(G + "/pairs.json")):
    e = c[p["unit"]]["emul"]
    print("  %-28s emul %3s: %s" % (p["unit"], e.get("instructions", "ref"),
          " | ".join(e.get("body", [e.get("refusal", "")]))[:520]))
PY
echo "preflight wall seconds=$(( $(date +%s) - t0 ))"
echo done
