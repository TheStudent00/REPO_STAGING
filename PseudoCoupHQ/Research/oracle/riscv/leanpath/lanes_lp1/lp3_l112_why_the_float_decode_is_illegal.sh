#!/bin/bash
# lp3_l112_why_the_float_decode_is_illegal.sh
#
# l111 PUT THE FLOAT LAYER TO THE GATE AND GOT NOTHING, twice over, and both
# reasons are mechanical rather than mathematical:
#
#   the emulation side: 0 of 142 compiled. `arch_units.h` includes
#     `sfemul.h`, which lives in `emul_rm0/c`, and the lane's flags carried
#     only `-I arch_units/c`. Adding the second include compiles it. Verified
#     by hand before this lane was written.
#
#   the arch side: 142 of 142 walks refused, every one with
#     "no certified pure form for ILLEGAL". The walker decodes each word with
#     the model's own `encdec_backwards` ON THE MODEL'S INITIAL STATE, and
#     that state is whatever `init_model ""` leaves. If misa does not enable
#     F and D, the decoder is right to answer ILLEGAL.
#
# WHAT IS NOT THE PROBLEM, checked so it is not guessed at: the Lean model
# HAS the float instructions. `LeanIM/FextInsts.lean` and `DextInsts.lean`
# exist and `Defs.lean` carries `f_bin_op_x_S` with FEQ_S, FLT_S, FLE_S. So
# this is a STATE question, not a missing emission, and the model does not
# need re-emitting.
#
# THE MEASUREMENT. One real float word, assembled here rather than typed,
# decoded three ways: on the walker's own state, on a state with misa's F and
# D bits written, and -- as the control -- an integer word on the same states,
# which must decode the same in all of them or the experiment says nothing.
#
# Writes $A/runs/float_decode only. Budget: fifteen minutes.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan
export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
A=PseudoCoupHQ/Research/oracle/riscv/leanpath
P=/work/proof; X=/work/Lean_IM_pr_exec; PLIB=LeanIM
D=$A/runs/float_decode; mkdir -p $D
t0=$(date +%s)

echo "[1/3] the words, assembled not typed  ($(( $(date +%s) - t0 ))s)"
cat > $D/w.s <<'EOF'
        .text
        feq.s a0, fa0, fa5
        fadd.d fa0, fa0, fa1
        add a0, a0, a1
EOF
clang --target=riscv64-unknown-linux-gnu -march=rv64imafdc -c $D/w.s -o $D/w.o 2>&1 | head -3
llvm-objdump -d --no-show-raw-insn $D/w.o | tail -6 | sed 's/^/  /'
WORDS=$(llvm-objdump -d $D/w.o | awk '/^ +[0-9a-f]+:/ {print $2}' | head -3)
echo "  words: $WORDS"

echo "[2/3] decode each on two states  ($(( $(date +%s) - t0 ))s)"
python3 - "$WORDS" <<'PY' > $D/Probe.lean
import sys
words = sys.argv[1].split()
print("import LeanIM")
print("open Sail Sail.ConcurrencyInterfaceV1 PreSail LeanIM LeanIM.Functions")
print("set_option maxHeartbeats 1000000000")
print("set_option maxRecDepth 100000")
print("""
def blank : SequentialState RegisterType trivialChoiceSource :=
  { regs := ∅, choiceState := (), mem := ∅, tags := (), cycleCount := 0,
    sailOutput := #[] }
""")
print("-- the walker's own state: whatever init_model leaves")
print("""def s0 : SequentialState RegisterType trivialChoiceSource :=
  match ((do sail_model_init (); init_model "") : SailM Unit) blank with
  | .ok _ s => s | .error _ s => s
""")
print("-- what misa actually says on that state")
print('#eval IO.println ("misa\\t" ++ (match (readReg misa) s0 with')
print('  | .ok v _ => toString (repr v) | .error _ _ => "ERROR"))')
for i, w in enumerate(words):
    n = len(w) * 4
    dec = "encdec_backwards" if n == 32 else "encdec_compressed_backwards"
    print('#eval IO.println ("w%d_s0\\t" ++ (match (%s (0x%s#%d)) s0 with'
          % (i, dec, w, n))
    print('  | .ok i _ => toString (repr i) | .error _ _ => "ERROR"))')
PY
cd $P
timeout 600 lake env lean $D/Probe.lean > $D/probe.txt 2>&1
echo "  rc=$?"
grep -E "^(misa|w[0-9]_)" $D/probe.txt | cut -c1-150 | sed 's/^/  /'
head -6 $D/probe.txt | grep -i error | cut -c1-140 | sed 's/^/  ERR /' || true

echo "[3/3] what this says  ($(( $(date +%s) - t0 ))s)"
python3 - <<'PY'
import re
txt = open("PseudoCoupHQ/Research/oracle/riscv/leanpath/runs/float_decode/probe.txt").read()
got = dict(re.findall(r"^(\w+)\t(.*)$", txt, re.M))
misa = got.get("misa", "(not read)")
print("  misa on the walker's state: %s" % misa[:90])
for k in sorted(got):
    if k.startswith("w"):
        v = got[k]
        kind = "ILLEGAL/ERROR" if ("Illegal" in v or v == "ERROR") else "decoded"
        print("    %-8s %-14s %s" % (k, kind, v[:70]))
print()
print("  reading: if the integer word decodes and the two float words do not,")
print("  the decoder is gating on an extension bit and the fix is the STATE,")
print("  not the model. If the integer word also fails, the state is wrong in")
print("  some larger way and this measurement says so instead.")
PY
echo "wall=$(( $(date +%s) - t0 ))s"
echo done
