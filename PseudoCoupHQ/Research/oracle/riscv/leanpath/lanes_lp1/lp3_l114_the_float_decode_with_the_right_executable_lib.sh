#!/bin/bash
# lp3_l114_the_float_decode_with_the_right_executable_lib.sh
#
# l113 used the walker's own eval_file and still failed, on the LIBRARY
# NAME: the executable project's lib is `LeanIMPrExecutable`, not `LeanIM`.
# Read out of its lakefile rather than assumed this time.
#
# l112 ASKED THE RIGHT QUESTION WITH A HAND-WRITTEN FILE AND THE FILE DID NOT
# ELABORATE. It built the machine state itself -- `blank`, then init -- and got
# `dependsOnNoncomputable` and an invalid dotted identifier. The walker already
# has the answer to all of that in `walk.state_defs` and `walk.eval_file`: the
# state is every register written with `default` FIRST (the emulator's own
# first step), then `sail_model_init`, then `init_model`, and the #evals run in
# the EXECUTABLE variant of the project rather than the proof one, because
# `#eval` needs a computable build.
#
# That is the third time this session that writing a thing beside the machinery
# instead of through it produced a failure that looked like a real result:
# the bridge's header (l106), the bridge's simp set (l108), and now this. So
# this lane calls the walker's own functions and writes no Lean of its own.
#
# THE QUESTION IS UNCHANGED. The float arch-units all refused with "no
# certified pure form for ILLEGAL". The Lean model HAS the float instructions
# -- FextInsts.lean, DextInsts.lean, FEQ_S in Defs.lean -- so the decoder is
# gating on the machine state, not missing the encoding. One float word and one
# integer word, decoded on the walker's own state, says which.
#
# Writes $A/runs/float_decode3 only. Budget: fifteen minutes.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan
export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
A=PseudoCoupHQ/Research/oracle/riscv/leanpath
X=/work/Lean_IM_pr_exec; PLIB=LeanIM
D=$A/runs/float_decode3; mkdir -p $D
t0=$(date +%s)
[ -d "$X" ] || { echo "FLAG: no executable project at $X"; exit 3; }

echo "[1/2] the words, assembled not typed  ($(( $(date +%s) - t0 ))s)"
cat > $D/w.s <<'EOF'
        .text
        feq.s a0, fa0, fa5
        fadd.d fa0, fa0, fa1
        add a0, a0, a1
EOF
clang --target=riscv64-unknown-linux-gnu -march=rv64imafdc -c $D/w.s -o $D/w.o 2>&1 | head -3
llvm-objdump -d --no-show-raw-insn $D/w.o | tail -5 | sed 's/^/  /'
WORDS=$(llvm-objdump -d $D/w.o | awk '/^ +[0-9a-f]+:/ {print $2}' | head -3)
echo "  words: $WORDS"

echo "[2/2] decode them on the walker's own state  ($(( $(date +%s) - t0 ))s)"
cd $A
python3 - "$WORDS" <<'PY'
import sys
sys.path.insert(0, "PseudoCoupHQ/Research/oracle/riscv/leanpath")
from leanpath.walk import eval_file, decode_expr
X, PLIB = "/work/Lean_IM_pr_exec", "LeanIMPrExecutable"
D = "PseudoCoupHQ/Research/oracle/riscv/leanpath/runs/float_decode3"
words = sys.argv[1].split()
names = ["feq_s", "fadd_d", "add"]
evals = [(names[i] if i < len(names) else "w%d" % i, decode_expr(w))
         for i, w in enumerate(words)]
rc, secs, got, errs = eval_file(X, PLIB, evals, D + "/Probe.lean")
print("  lean rc=%s in %.1fs" % (rc, secs))
for e in errs[:4]:
    print("  ERR %s" % e[:130])
print()
for tag, _ in evals:
    v = got.get(tag, "(no output)")
    bad = ("Illegal" in v) or v == "ERROR" or v == "(no output)"
    print("  %-8s %-14s %s" % (tag, "ILLEGAL/ERROR" if bad else "decoded", v[:80]))
print()
ok_int = not (("Illegal" in got.get("add", "")) or got.get("add") in (None, "ERROR"))
bad_f = all((("Illegal" in got.get(t, "")) or got.get(t) in (None, "ERROR"))
            for t in ("feq_s", "fadd_d"))
if ok_int and bad_f:
    print("  READING: the integer word decodes and both float words do not.")
    print("  The decoder is gating on the machine state, and the float layer")
    print("  is reachable by fixing the STATE the walk decodes on -- misa's F")
    print("  and D bits -- not by re-emitting the model.")
elif ok_int:
    print("  READING: a float word decoded. The ILLEGAL of l111 is then NOT a")
    print("  blanket extension gate and the refusal must be read per unit.")
else:
    print("  READING: even the integer word did not decode here, so this")
    print("  measurement says nothing about float; the state or the project is")
    print("  wrong in some larger way and that is what to chase.")
PY
echo "wall=$(( $(date +%s) - t0 ))s"
echo done
