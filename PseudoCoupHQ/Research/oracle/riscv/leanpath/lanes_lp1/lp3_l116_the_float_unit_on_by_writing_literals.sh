#!/bin/bash
# lp3_l116_the_float_unit_on_by_writing_literals.sh
#
# l115 failed on `readReg misa` -- "overloaded" -- and on nothing else. The
# registers themselves are fine: `walk.registers_of` lists 180 and both `misa`
# and `mstatus` are among them, and `walk.state_defs` already writes registers
# as `PreSail.writeReg Register.<name> <value>`. So this lane READS NOTHING and
# writes literals, which removes the only construct that failed.
#
# THE VALUES, and where each bit comes from.
#
#   misa = 0x800000000000112D
#     MXL (63:62) = 2, meaning XLEN 64.
#     letters, bit n for the nth letter: A=1<<0, C=1<<2, D=1<<3, F=1<<5,
#     I=1<<8, M=1<<12  ->  0x1 + 0x4 + 0x8 + 0x20 + 0x100 + 0x1000 = 0x112D.
#     F is bit 5 and D is bit 3, which is what `_get_Misa_F` and `_get_Misa_D`
#     read in PlatformConfig.lean (extractLsb v 5 5 and v 3 3).
#
#   mstatus = 0x2000
#     FS (14:13) = 0b01, "Initial". `currentlyEnabled Ext_F` requires
#     `_get_Mstatus_FS != 0b00`, and Initial is the least that satisfies it.
#     This is the ordinary RISC-V situation: a hart leaves reset with the
#     floating-point unit OFF and boot code turns it on. `init_model` does not
#     -- it ignores its filename argument entirely and just calls `reset ()`.
#
# The integer word is the control: if it stops decoding when these are written,
# the writes broke the state and the float result means nothing.
#
# Writes $A/runs/float_on2 only. Budget: fifteen minutes.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan
export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
A=PseudoCoupHQ/Research/oracle/riscv/leanpath
X=/work/Lean_IM_pr_exec; PLIB=LeanIMPrExecutable
D=$A/runs/float_on2; mkdir -p $D
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
D = "PseudoCoupHQ/Research/oracle/riscv/leanpath/runs/float_on2"
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
