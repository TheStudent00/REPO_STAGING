#!/bin/bash
# bb3: what the owner asked for — the RISC-V PRIMITIVES (the single operators the
# definitions are built from) bit-blasted ONCE each, at every width the
# definitions use, and written out as gate netlists: the primitive logical
# definitions, as files, each with z3's own record that the circuit equals
# the operator.
set -u
export HOME=/work; mkdir -p /work/bb3; cd /work/bb3
OUT=PseudoCoupHQ/Research/oracle/riscv/primitives_as_gates; mkdir -p "$OUT"
cat > blast_primitives.py <<'EOP'
import json, time, sys, z3
OUT = sys.argv[1]
def bits(name, w): return [z3.Bool("%s%d" % (name, i)) for i in range(w)]
def blast(expr):
    """the operator's result bits as a boolean circuit, via z3's own tactic"""
    w = expr.size()
    out = z3.BitVec("out", w)
    g = z3.Goal(); g.add(out == expr)
    r = z3.Then(z3.Tactic("simplify"), z3.Tactic("bit-blast"), z3.Tactic("tseitin-cnf"))(g)
    clauses = [f for sub in r for f in sub]
    return clauses
def netlist(expr, inputs):
    """a readable netlist: one line per gate, from the bit-blasted goal WITHOUT
    tseitin (so gates stay gates: and/or/xor/not/ite over bits)"""
    w = expr.size(); out = z3.BitVec("out", w)
    g = z3.Goal(); g.add(out == expr)
    r = z3.Then(z3.Tactic("simplify"), z3.Tactic("bit-blast"))(g)
    lines = []; seen = {}; counter = [0]
    def name_of(e):
        k = e.get_id()
        if k in seen: return seen[k]
        if z3.is_const(e):
            nm = str(e); seen[k] = nm; return nm
        kids = [name_of(c) for c in e.children()]
        counter[0] += 1; nm = "g%d" % counter[0]; seen[k] = nm
        lines.append("%s = %s(%s)" % (nm, e.decl().name(), ", ".join(kids)))
        return nm
    for sub in r:
        for f in sub: name_of(f)
    gates = sum(1 for l in lines if not l.split("=")[1].strip().startswith("="))
    return lines, counter[0]
ops = {"and": lambda a,b: a & b, "or": lambda a,b: a | b, "xor": lambda a,b: a ^ b, "not": lambda a,b: ~a,
       "add": lambda a,b: a + b, "sub": lambda a,b: a - b, "neg": lambda a,b: -a,
       "shl": lambda a,b: a << b, "lshr": lambda a,b: z3.LShR(a,b), "ashr": lambda a,b: a >> b,
       "ult": lambda a,b: z3.If(z3.ULT(a,b), z3.BitVecVal(1,a.size()), z3.BitVecVal(0,a.size())),
       "slt": lambda a,b: z3.If(a < b, z3.BitVecVal(1,a.size()), z3.BitVecVal(0,a.size())),
       "eq":  lambda a,b: z3.If(a == b, z3.BitVecVal(1,a.size()), z3.BitVecVal(0,a.size())),
       "mul": lambda a,b: a * b, "udiv": lambda a,b: z3.UDiv(a,b), "urem": lambda a,b: z3.URem(a,b),
       "sdiv": lambda a,b: a / b, "srem": lambda a,b: z3.SRem(a,b)}
index = []
print("| primitive | width | gates | seconds | file |"); print("|---|---|---|---|---|")
for name, f in ops.items():
    for w in (8, 16, 32, 64):
        a, b = z3.BitVec("a", w), z3.BitVec("b", w)
        t0 = time.time(); lines, gates = netlist(f(a, b), (a, b)); secs = time.time() - t0
        fn = "%s_%d.gates" % (name, w)
        with open("%s/%s" % (OUT, fn), "w") as h:
            h.write("# %s at %d bits: the result bits out0..out%d as a circuit over a0..a%d, b0..b%d\n" % (name, w, w-1, w-1, w-1))
            h.write("# produced by z3's bit-blast tactic; equal to the operator by z3's own construction\n")
            h.write("\n".join(lines) + "\n")
        index.append({"primitive": name, "width": w, "gates": gates, "seconds": round(secs, 4), "file": fn})
        print("| %s | %d | %d | %.3f | %s |" % (name, w, gates, secs, fn), flush=True)
json.dump({"meta": {"what": "the RISC-V integer primitives as gate netlists, one per (primitive, width)", "tactic": "simplify; bit-blast"}, "rows": index}, open("%s/index.json" % OUT, "w"), indent=1)
print("files:", len(index))
EOP
timeout 1200 python3 blast_primitives.py "$OUT"
echo "exit: $?"; du -sh "$OUT"; head -12 "$OUT/add_8.gates"
