#!/bin/bash
# bb0: how much does z3's bit-blast cost for each language primitive at each
# width, and for a few whole RISC-V definitions? Gates and seconds.
set -u
export HOME=/work; mkdir -p /work/bb0; cd /work/bb0
cat > sample.py <<'EOP'
import time, z3, resource
def blast(expr, inputs):
    g = z3.Goal(); g.add(expr == z3.BitVec('__out', expr.size()) if z3.is_bv(expr) else expr)
    t0 = time.time()
    r = z3.Then(z3.Tactic('simplify'), z3.Tactic('bit-blast'), z3.Tactic('tseitin-cnf'))(g)
    secs = time.time() - t0
    clauses = sum(len(sub) for sub in r)
    # count distinct boolean atoms as a gate proxy
    atoms = set()
    def walk(e):
        if e.get_id() in seen: return
        seen.add(e.get_id())
        if z3.is_const(e) and e.decl().kind() == z3.Z3_OP_UNINTERPRETED: atoms.add(e.get_id())
        for c in e.children(): walk(c)
    seen = set()
    for sub in r:
        for f in sub: walk(f)
    return clauses, len(atoms), secs
print("| operation | width | CNF clauses | boolean variables | seconds |")
print("|---|---|---|---|---|")
ops = [("and", lambda a,b: a & b), ("or", lambda a,b: a | b), ("xor", lambda a,b: a ^ b), ("not", lambda a,b: ~a),
       ("add", lambda a,b: a + b), ("sub", lambda a,b: a - b), ("shl", lambda a,b: a << b), ("lshr", lambda a,b: z3.LShR(a,b)),
       ("ashr", lambda a,b: a >> b), ("ult", lambda a,b: z3.If(z3.ULT(a,b), z3.BitVecVal(1,a.size()), z3.BitVecVal(0,a.size()))),
       ("slt", lambda a,b: z3.If(a < b, z3.BitVecVal(1,a.size()), z3.BitVecVal(0,a.size()))),
       ("mul", lambda a,b: a * b), ("udiv", lambda a,b: z3.UDiv(a,b)), ("urem", lambda a,b: z3.URem(a,b)),
       ("sdiv", lambda a,b: a / b), ("srem", lambda a,b: z3.SRem(a,b))]
for name, f in ops:
    for w in (8, 16, 32, 64):
        a, b = z3.BitVec('a', w), z3.BitVec('b', w)
        try:
            c, v, s = blast(f(a, b), (a, b)); print(f"| {name} | {w} | {c} | {v} | {s:.3f} |", flush=True)
        except Exception as e: print(f"| {name} | {w} | refused | {type(e).__name__} | |", flush=True)
print(); print("whole RISC-V definitions, as the lifter states them (64-bit):")
print("| definition | CNF clauses | boolean variables | seconds |"); print("|---|---|---|---|")
a, b = z3.BitVec('a', 64), z3.BitVec('b', 64)
ones = z3.BitVecVal((1<<64)-1, 64); mn = z3.BitVecVal(1<<63, 64); zero = z3.BitVecVal(0,64)
defs = [("add", a + b), ("slt", z3.If(a < b, z3.BitVecVal(1,64), zero)), ("sll", a << z3.ZeroExt(58, z3.Extract(5,0,b))),
        ("div (zero and overflow cases included)", z3.If(b == zero, ones, z3.If(z3.And(a == mn, b == ones), mn, a / b))),
        ("rem (zero and overflow cases included)", z3.If(b == zero, a, z3.If(z3.And(a == mn, b == ones), zero, z3.SRem(a, b)))),
        ("mulh (high half of the signed product)", z3.Extract(127, 64, z3.SignExt(64, a) * z3.SignExt(64, b)))]
for name, e in defs:
    c, v, s = blast(e, (a, b)); print(f"| {name} | {c} | {v} | {s:.3f} |", flush=True)
print(); print("peak resident kB:", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
EOP
timeout 1500 python3 sample.py
echo "exit: $?"
