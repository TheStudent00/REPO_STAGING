#!/bin/bash
# lp3_l115_turn_the_float_unit_on_in_the_walkers_state.sh
#
# THE FLOAT DECODE, AND WHAT ACTUALLY GATES IT. l114 decoded three real words
# on the walker's own state: `add` came back C_ADD, `feq.s` and `fadd.d` came
# back ILLEGAL. The model is not missing them -- FextInsts.lean and
# DextInsts.lean are there. `PlatformConfig.lean` says what the gate is, and
# it is THREE conditions, not one:
#
#   | .Ext_F => hartSupports Ext_F
#            && _get_Misa_F (readReg misa) == 1
#            && _get_Mstatus_FS (readReg mstatus) != 0b00
#            && currentlyEnabled Ext_Zicsr
#
# and `hartSupports Ext_F => true` in this build, so the STATIC config already
# allows it. What is missing is runtime state, and it is the ordinary RISC-V
# situation: a hart comes out of reset with the floating-point unit OFF
# (`mstatus.FS = 0b00`) and something has to turn it on. Nothing in the
# walker's state ever does.
#
# So this lane does not change the walker. It writes ONE probe file through
# `walk.eval_file` -- the walker's own evaluator, because writing Lean beside
# the machinery has cost four lanes this session -- and asks whether setting
# misa's F and D bits and mstatus's FS field makes the two float words decode.
# If they do, the fix to `walk.state_defs` is a two-line one and is worth
# making. If they do not, the reason will be in the output rather than in a
# guess.
#
# the owner approved changing the walker's state (2026-09-17). This lane establishes
# WHAT to change it to before it is changed.
#
# Writes $A/runs/float_on only. Budget: fifteen minutes.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan
export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
A=PseudoCoupHQ/Research/oracle/riscv/leanpath
X=/work/Lean_IM_pr_exec; PLIB=LeanIMPrExecutable
D=$A/runs/float_on; mkdir -p $D
t0=$(date +%s)

echo "[1/3] the words  ($(( $(date +%s) - t0 ))s)"
printf '        .text\n        feq.s a0, fa0, fa5\n        fadd.d fa0, fa0, fa1\n        add a0, a0, a1\n' > $D/w.s
clang --target=riscv64-unknown-linux-gnu -march=rv64imafdc -c $D/w.s -o $D/w.o 2>&1 | head -2
WORDS=$(llvm-objdump -d $D/w.o | awk '/^ +[0-9a-f]+:/ {print $2}' | head -3)
echo "  words: $WORDS"

echo "[2/3] do the setters exist, and what is misa now  ($(( $(date +%s) - t0 ))s)"
cd $A
python3 - "$WORDS" <<'PY'
import sys
sys.path.insert(0, "PseudoCoupHQ/Research/oracle/riscv/leanpath")
from leanpath.walk import eval_file, decode_expr
X, PLIB = "/work/Lean_IM_pr_exec", "LeanIMPrExecutable"
D = "PseudoCoupHQ/Research/oracle/riscv/leanpath/runs/float_on"
words = sys.argv[1].split()
names = ["feq_s", "fadd_d", "add"]

# what the state carries BEFORE anything is changed
evals = [("misa_now", '(match (readReg misa) s0 with | .ok v _ => toString (repr v) | .error _ _ => "ERR")'),
         ("mstatus_now", '(match (readReg mstatus) s0 with | .ok v _ => toString (repr v) | .error _ _ => "ERR")')]
evals += [(names[i], decode_expr(w)) for i, w in enumerate(words)]
rc, secs, got, errs = eval_file(X, PLIB, evals, D + "/Before.lean")
print("  BEFORE -- rc=%s in %.1fs" % (rc, secs))
for e in errs[:3]: print("    ERR %s" % e[:120])
for t, _ in evals:
    print("    %-12s %s" % (t, got.get(t, "(none)")[:78]))
PY

echo "[3/3] with the float unit turned on  ($(( $(date +%s) - t0 ))s)"
python3 - "$WORDS" <<'PY'
import sys, os, re
sys.path.insert(0, "PseudoCoupHQ/Research/oracle/riscv/leanpath")
from leanpath import walk as W
from leanpath import strip as ST
X, PLIB = "/work/Lean_IM_pr_exec", "LeanIMPrExecutable"
D = "PseudoCoupHQ/Research/oracle/riscv/leanpath/runs/float_on"
words = sys.argv[1].split()
names = ["feq_s", "fadd_d", "add"]

# state_defs is the walker's own; s1 is s0 with the float unit switched on.
# misa bit 5 is F and bit 3 is D (PlatformConfig `_get_Misa_F`/`_get_Misa_D`);
# mstatus.FS is the two-bit field the same file reads with `_get_Mstatus_FS`,
# and any value but 0b00 means "not Off" -- 0b01 (Initial) is the least we can
# claim and is what is written here.
extra = [
 "/-- s0, with misa's F and D set and mstatus.FS out of Off -/",
 "def s1 : SequentialState RegisterType trivialChoiceSource :=",
 "  match ((do",
 "      let m ← readReg misa",
 "      PreSail.writeReg Register.misa (m ||| 0x28#64)",
 "      let st ← readReg mstatus",
 "      PreSail.writeReg Register.mstatus (st ||| 0x2000#64)",
 "      pure ()) : SailM Unit) s0 with | .ok _ s => s | .error _ s => s",
 "",
]
ns = ST.namespaces_of(os.path.join(X, PLIB))
head = ["import %s" % PLIB,
        "open Sail Sail.ConcurrencyInterfaceV1 PreSail %s" % " ".join(ns),
        "set_option maxHeartbeats 1000000000",
        "set_option maxRecDepth 100000", ""] + W.state_defs(os.path.join(X, PLIB)) + extra
body = ['#eval IO.println ("misa_on\\t" ++ (match (readReg misa) s1 with | .ok v _ => toString (repr v) | .error _ _ => "ERR"))',
        '#eval IO.println ("mstatus_on\\t" ++ (match (readReg mstatus) s1 with | .ok v _ => toString (repr v) | .error _ _ => "ERR"))']
for i, w in enumerate(words):
    n = len(w) * 4
    dec = "encdec_backwards" if n == 32 else "encdec_compressed_backwards"
    body.append('#eval IO.println ("%s\\t" ++ (match (%s (0x%s#%d)) s1 with | .ok i _ => toString (repr i) | .error _ _ => "ERROR"))'
                % (names[i], dec, w, n))
path = D + "/After.lean"
open(path, "w").write("\n".join(head + body) + "\n")
rc, secs, out = W.lean_run(X, path)
print("  AFTER -- rc=%s in %.1fs" % (rc, secs))
got = dict(re.findall(r"^(\w+)\t(.*)$", out, re.M))
for e in [l for l in out.split("\n") if "error" in l][:3]:
    print("    ERR %s" % e[:120])
for t in ("misa_on", "mstatus_on") + tuple(names):
    v = got.get(t, "(none)")
    mark = ""
    if t in names:
        mark = "  <-- still ILLEGAL" if ("ILLEGAL" in v.upper() or v in ("ERROR", "(none)")) else "  <-- DECODED"
    print("    %-12s %s%s" % (t, v[:70], mark))
ok = all("ILLEGAL" not in got.get(t, "ILLEGAL").upper() for t in ("feq_s", "fadd_d"))
print()
print("  VERDICT: %s" % ("the float unit switches on and the words decode -- "
                         "walk.state_defs should write these two registers"
                         if ok else
                         "still ILLEGAL; the gate is not only misa and mstatus.FS, "
                         "and the output above says what else is missing"))
PY
echo "wall=$(( $(date +%s) - t0 ))s"
echo done
