#!/bin/bash
# lp3_l118_currentlyEnabled_with_the_constructor_qualified.sh
#
# l117 failed on an unqualified constructor: Ext_F is a constructor of the
# type `extension`, and PlatformConfig matches it as `| .Ext_F =>`, so it must
# be written `extension.Ext_F` outside that match. The decode result was the
# same in l114, l116 and l117 and is not in doubt; only the introspection was.
#
# l116 wrote misa's F and D bits and mstatus.FS and the float words STILL came
# back ILLEGAL, with the integer control still decoding -- so the writes were
# fine and the gate has another conjunct. I have now spent six lanes inferring
# which one from the source, and that is the wrong method: the model has the
# predicate, so ASK IT.
#
# `currentlyEnabled Ext_F` is a function returning Bool in the SailM monad.
# This lane evaluates it, and `Ext_D`, and `Ext_Zicsr`, on s0 and on s1 --
# alongside the same three decodes, so the answer and the symptom are read off
# one run. Whatever is false is then named rather than guessed at.
#
# Writes $A/runs/float_on4 only. Budget: fifteen minutes.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan
export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
A=PseudoCoupHQ/Research/oracle/riscv/leanpath
X=/work/Lean_IM_pr_exec; PLIB=LeanIMPrExecutable
D=$A/runs/float_on4; mkdir -p $D
t0=$(date +%s)

echo "[1/2] the words  ($(( $(date +%s) - t0 ))s)"
printf '        .text\n        feq.s a0, fa0, fa5\n        fadd.d fa0, fa0, fa1\n        add a0, a0, a1\n' > $D/w.s
clang --target=riscv64-unknown-linux-gnu -march=rv64imafdc -c $D/w.s -o $D/w.o 2>&1 | head -2
WORDS=$(llvm-objdump -d $D/w.o | awk '/^ +[0-9a-f]+:/ {print $2}' | head -3)
echo "  words: $WORDS"

echo "[2/2] decode on s0, then on s0 with the float unit written on  ($(( $(date +%s) - t0 ))s)"
cd $A
python3 - "$WORDS" <<'PY'
import sys, os, re
sys.path.insert(0, "PseudoCoupHQ/Research/oracle/riscv/leanpath")
from leanpath import walk as W
from leanpath import strip as ST
X, PLIB = "/work/Lean_IM_pr_exec", "LeanIMPrExecutable"
D = "PseudoCoupHQ/Research/oracle/riscv/leanpath/runs/float_on4"
words = sys.argv[1].split()
names = ["feq_s", "fadd_d", "add"]

extra = [
 "/-- s0 with the floating-point unit switched on: misa's F and D set, and",
 "    mstatus.FS out of Off.  Literals, so nothing is read back. -/",
 "def s1 : SequentialState RegisterType trivialChoiceSource :=",
 "  match ((do",
 "      PreSail.writeReg Register.misa 0x800000000000112D#64",
 "      PreSail.writeReg Register.mstatus 0x2000#64",
 "      pure ()) : SailM Unit) s0 with | .ok _ s => s | .error _ s => s",
 "",
]
ns = ST.namespaces_of(os.path.join(X, PLIB))
head = ["import %s" % PLIB,
        "open Sail Sail.ConcurrencyInterfaceV1 PreSail %s" % " ".join(ns),
        "set_option maxHeartbeats 1000000000",
        "set_option maxRecDepth 100000", ""] + W.state_defs(os.path.join(X, PLIB)) + extra
body = []
# ask the predicate directly, on both states
for state in ("s0", "s1"):
    for ext in ("Ext_F", "Ext_D", "Ext_Zicsr"):
        body.append('#eval IO.println ("en_%s_%s\\t" ++ (match ((currentlyEnabled extension.%s) : SailM Bool) %s with '
                    '| .ok v _ => toString v | .error _ _ => "ERROR"))' % (ext, state, ext, state))
for state in ("s0", "s1"):
    for i, w in enumerate(words):
        n = len(w) * 4
        dec = "encdec_backwards" if n == 32 else "encdec_compressed_backwards"
        body.append('#eval IO.println ("%s_%s\\t" ++ (match (%s (0x%s#%d)) %s with '
                    '| .ok i _ => toString (repr i) | .error _ _ => "ERROR"))'
                    % (names[i], state, dec, w, n, state))
path = D + "/Probe.lean"
open(path, "w").write("\n".join(head + body) + "\n")
rc, secs, out = W.lean_run(X, path)
print("  lean rc=%s in %.1fs" % (rc, secs))
errs = [l for l in out.split("\n") if "error" in l]
for e in errs[:4]:
    print("    ERR %s" % e[:130])
got = dict(re.findall(r"^(\w+)\t(.*)$", out, re.M))
print()
print("  %-10s %-24s %s" % ("word", "on s0 (as the walk runs)", "on s1 (float unit on)"))
for nm in names:
    a = got.get("%s_s0" % nm, "(none)")
    b = got.get("%s_s1" % nm, "(none)")
    f = lambda v: "ILLEGAL" if "ILLEGAL" in v.upper() else ("(none)" if v == "(none)" else "decoded")
    print("  %-10s %-24s %s" % (nm, f(a), f(b)))
print()
print("  currentlyEnabled, asked directly:")
for ext in ("Ext_F", "Ext_D", "Ext_Zicsr"):
    print("    %-10s s0=%-8s s1=%s" % (ext, got.get("en_%s_s0" % ext, "(none)"),
                                       got.get("en_%s_s1" % ext, "(none)")))
print()
ctrl = "ILLEGAL" not in got.get("add_s1", "ILLEGAL").upper() and got.get("add_s1") != "(none)"
moved = [nm for nm in ("feq_s", "fadd_d")
         if "ILLEGAL" in got.get("%s_s0" % nm, "").upper()
         and "ILLEGAL" not in got.get("%s_s1" % nm, "ILLEGAL").upper()
         and got.get("%s_s1" % nm, "(none)") != "(none)"]
if not ctrl:
    print("  VERDICT: the control word stopped decoding on s1, so the writes")
    print("  broke the state and nothing about float is established here.")
elif moved:
    print("  VERDICT: %s decode on s1 and not on s0." % ", ".join(moved))
    print("  The gate is the machine state, and walk.state_defs writing these")
    print("  two registers is the whole fix.")
else:
    print("  VERDICT: the control still decodes but the float words do not,")
    print("  so misa and mstatus.FS are not the whole gate. What remains is in")
    print("  the errors above or in currentlyEnabled's other conjuncts.")
PY
echo "wall=$(( $(date +%s) - t0 ))s"
echo done
