#!/bin/bash
# L2 lane 2 — the four things the generator needs to know before it is
# written, each answered by running the real objects rather than by
# reading them.
#
#  1. what free symbols the ledger route's term carries, and how the
#     layer-5 renaming (v0, v1, ...) lines up with the unit's own
#     arrival families;
#  2. whether a MachineState whose every register family is pre-bound to
#     a fresh marker turns one builder into its GENERIC form (the model
#     definition), leaving the markers as its parameters;
#  3. what `answer_of` reads at the end of a body;
#  4. whether Lean accepts an `opaque` bit-vector constant and a
#     structure with a String field (the shape the flags triple needs).
set -u

TOTAL=4
OP=/projects/PseudoCoupHQ/Research/op_pipeline
export HOME=/work/L2home
mkdir -p "$HOME"
cd "$OP" || exit 1

echo "[1/$TOTAL] the ledger route's term for three rows, and its symbols"
python3 - <<'PY'
import json, sys
sys.path.insert(0, '/projects/PseudoCoupHQ/Research/op_pipeline')
import z3, layer5
import term97_walk as TW
maker, gate, attached, readings = TW.build()
POP = ('/projects/PseudoCoupHQ/Research/oracle/cross_construction/'
       'emulation/per_opcode/per_opcode_population.json')
HELD = ('/projects/PseudoCoupHQ/Research/oracle/cross_construction/'
        'emulation/per_opcode/per_opcode_held.json')
pop = json.load(open(POP))
held = json.load(open(HELD))["held"]
for job in pop["valid"][:3]:
    uid = job["example_unit_id"]
    rec = dict(held[uid])
    rec["unit"] = uid
    print("=== %s   mnemonic %s" % (uid, job["mnemonic"]))
    print("    body_verbatim: %r" % (rec.get("body_verbatim"),))
    print("    arrival_families: %s" % (rec.get("arrival_families"),))
    print("    arrival_contract_bindings: %r"
          % (rec.get("arrival_contract_bindings"),))
    print("    result_family %r  result_width %r"
          % (rec.get("result_family"), rec.get("result_width")))
    walked = maker.transcribe(rec)
    t = walked.out_term
    print("    transcribed term: %s" % (t,))
    simplified = z3.simplify(t)
    ordered = layer5.ordered_symbols(simplified)
    print("    layer5 symbol order: %s"
          % [(s.decl().name(), s.size()) for s in ordered])
    print("    stored  layer5 text: %s" % job["term_text"])
    print("    reprint layer5 text: %s" % maker.normalize(t))
    print("    reprint exact: %s" % (maker.normalize(t) == job["term_text"]))
PY

echo "[2/$TOTAL] the marker fork: one builder in its generic form"
python3 - <<'PY'
import sys
sys.path.insert(0, '/projects/PseudoCoupHQ/Research/op_pipeline')
import reference as R
import canon
import z3

FAMILIES = sorted(set(canon.FAMILY_OF.values()) | set(R.XMM_NAMES))
print("families the marker fork pre-binds: %d -- %s"
      % (len(FAMILIES), " ".join(FAMILIES)))

def generic(line):
    state = R.MachineState()
    for family in FAMILIES:
        bits = 128 if family in R.XMM_NAMES else 64
        state.shared_seed[family] = z3.BitVec("arg_%s" % family, bits)
    before = dict(state.registers)
    R.REFERENCE.step(state, line)
    changed = {}
    for family, term in state.registers.items():
        was = before.get(family)
        if was is None or was.sexpr() != term.sexpr():
            changed[family] = term
    return changed, state.flags

for line in ("add %rsi,%rdi", "add %esi,%edi", "sar %cl,%rdi",
             "sar $0x3,%edi", "imul %rsi,%rdi", "imul %rsi",
             "mul %rsi", "ucomiss %xmm1,%xmm0", "cvtsi2sd %edi,%xmm0",
             "not %rdi", "neg %edi", "xorps %xmm0,%xmm0",
             "lea (%rdi,%rsi,1),%rax", "mov %esi,%eax"):
    try:
        changed, flags = generic(line)
    except Exception as exc:
        print("%-26s REFUSED %s: %s" % (line, type(exc).__name__, exc))
        continue
    print("=== %s" % line)
    for family in sorted(changed):
        print("    writes %-5s := %s" % (family, changed[family]))
    if flags is not None:
        print("    flags  (%r, %s, %s)" % (flags[0], flags[1], flags[2]))
PY

echo "[3/$TOTAL] answer_of over a whole row body"
python3 - <<'PY'
import json, sys
sys.path.insert(0, '/projects/PseudoCoupHQ/Research/op_pipeline')
import reference as R
import z3
HELD = ('/projects/PseudoCoupHQ/Research/oracle/cross_construction/'
        'emulation/per_opcode/per_opcode_held.json')
POP = ('/projects/PseudoCoupHQ/Research/oracle/cross_construction/'
       'emulation/per_opcode/per_opcode_population.json')
held = json.load(open(HELD))["held"]
pop = json.load(open(POP))
for job in pop["valid"][:3]:
    uid = job["example_unit_id"]
    rec = dict(held[uid]); rec["unit"] = uid
    term, width = R.REFERENCE.answer_for_unit(rec)
    print("=== %s  answer width %s" % (uid, width))
    print("    reference answer: %s" % z3.simplify(term))
    print("    stored layer5   : %s" % job["term_text"])
PY

echo "[4/$TOTAL] Lean: an opaque bit-vector constant and a flags structure"
mkdir -p /work/L2probe && cd /work/L2probe || exit 1
cat > Probe.lean <<'LEAN'
import Std.Tactic.BVDecide

/-- an uninterpreted float primitive, the shape the model needs where
    the reference's term carries a floating-point node -/
opaque ieeeAddF32 : BitVec 32 → BitVec 32 → BitVec 32

/-- the reference's flag model is a triple: the setter's own name and
    the two values it compared -/
structure Flags (w : Nat) where
  setter : String
  L : BitVec w
  R : BitVec w

def model_add_r64_r64 (x y : BitVec 64) : BitVec 64 := x + y
def model_add_r64_r64_flags (x y : BitVec 64) : Flags 64 :=
  { setter := "add", L := x, R := y }

example (v0 v1 : BitVec 64) : model_add_r64_r64 v0 v1 = v0 + v1 := rfl
example (v0 v1 : BitVec 64) : (model_add_r64_r64_flags v0 v1).L = v0 := rfl
#check ieeeAddF32
LEAN
lean Probe.lean
echo "--- lean exit $?"
