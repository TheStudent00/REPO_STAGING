"""Acceptance test for the mechanically transpiled vocabulary.

The gate: instructions the AUTO transpiler produced must emit bytes
identical to the HAND-transpiled encoders in
../rust_routing/slice_encoder.py — which are themselves verified
byte-identical to native rustc (81-row grid, host run 2026-07-25).

So the chain of trust is:
    rustc  ==  hand transpile  ==  auto transpile
"""

import sys
sys.path.insert(0, ".")
sys.path.insert(0, "../rust_routing")

from vocab_support import CodeSink, Gpr, GprMem, RAX, RDX, RSI, R14
import pc_vocab

# the hand-transpiled, rustc-verified reference
import slice_encoder as hand

ok = True


def emit_auto(cls, *args):
    sink = CodeSink()
    cls(*args).encode(sink)
    return sink.bytes()


def emit_hand(inst):
    sink = hand.CodeSink()
    inst.encode(sink)
    return sink.bytes()


def check(label, auto, ref):
    global ok
    if auto != ref:
        ok = False
    print(f"{'PASS' if auto == ref else 'FAIL'}  {label}: "
          f"auto={auto.hex(' ')}  hand/rustc={ref.hex(' ')}")


print(f"vocabulary loaded: {len(pc_vocab.INSTRUCTIONS)} instructions\n")

# --- the five the hand slice covers, both operand encodings ---
for reg in (RSI, R14):
    check(f"idivq_m rm={reg}",
          emit_auto(pc_vocab.idivq_m, Gpr(RAX), Gpr(RDX), GprMem(reg), "T"),
          emit_hand(hand.idivq_m(RAX, RDX, hand.GprMem(reg))))

check("cqto_zo",
      emit_auto(pc_vocab.cqto_zo, Gpr(RAX), Gpr(RDX)),
      emit_hand(hand.cqto_zo()))

for name, handcls in (("addq_rm", hand.addq_rm), ("subq_rm", hand.subq_rm),
                      ("imulq_rm", hand.imulq_rm)):
    for reg in (RSI, R14):
        check(f"{name} rm={reg}",
              emit_auto(getattr(pc_vocab, name), Gpr(RAX), GprMem(reg)),
              emit_hand(handcls(RAX, hand.GprMem(reg))))

# --- breadth: run every encoder the support layer can drive ---
# Operand kinds are inferred from field names; where an encoder wants a
# memory-capable operand the harness retries with GprMem. A remaining
# error is a TRANSPILER fault, not a harness one.
print("\n--- breadth check: all 1071 encoders ---")
from vocab_support import Imm


def build(fields, mem_all=False):
    args = []
    for f in fields:
        if f == "trap":
            args.append("T")
        elif f.startswith("imm"):
            args.append(Imm(0, 4))
        elif mem_all or f.startswith(("rm", "xmm_m", "m")):
            args.append(GprMem(RSI))
        else:
            args.append(Gpr(RAX))
    return args


ran = failed_cut = errored = 0
bad = []
for name, cls in sorted(pc_vocab.INSTRUCTIONS.items()):
    for mem_all in (False, True):
        try:
            sink = CodeSink()
            cls(*build(cls.FIELDS, mem_all)).encode(sink)
            ran += 1
            break
        except NotImplementedError:
            failed_cut += 1
            break
        except Exception as e:
            if mem_all:
                errored += 1
                bad.append(f"{name}: {type(e).__name__}: {e}")
print(f"  encoded cleanly : {ran}")
print(f"  hit a marked cut: {failed_cut}   (VEX/EVEX or Amode — expected)")
print(f"  transpiler faults: {errored}")
for b in bad[:8]:
    print("     ", b[:90])
if errored:
    ok = False

print("\nVOCABULARY:", "ALL PASS" if ok else "FAILURES PRESENT")
