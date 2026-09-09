#!/usr/bin/env bash
# m1b_l7_smoke.sh -- task m1b: the cheap checks on the closer's own
# code before the long passes run. Compiles model_table.py, then puts
# the one width rule and the classifier on the page over real operand
# texts the corpus spells (lane m1b_l2_probe.sh's own findings) so the
# two sides of the join can be read rather than assumed.
# MEMORY BOUND: 16 GB resident, named abort ABORT_MEMORY_M1B; this
# lane holds nothing but the reference's tables. Peak RSS printed.
set -euo pipefail
echo "[1/3] task m1b: model_table.py compiles"
cd PseudoCoupHQ/Research/oracle/arch_opcodes/model
python3 -m py_compile model_table.py
echo "   ok"
echo "[2/3] task m1b: the one width rule over real mnemonics"
python3 - <<'PY'
import resource
import sys

sys.path.insert(0, "PseudoCoupHQ/Research/oracle/arch_opcodes/model")
import model_table as MB

SAMPLE = [("add", 32), ("add", 64), ("addss", 32), ("addss", 64),
          ("addsd", 8), ("cvtsi2sd", 32), ("cvtsi2sd", 64),
          ("cvtss2sd", 16), ("ucomiss", 64), ("ucomisd", 64),
          ("xorps", 8), ("movaps", 16), ("movss", 64), ("movd", 8),
          ("movq", 64), ("pextrw", 32), ("pmovmskb", 32),
          ("punpckldq", 8), ("faddp", 16), ("fldt", 32),
          ("fucomip", 64), ("setne", 8), ("cmovne", 64)]
print("   | mnem | width in | key_width |")
for mnem, width in SAMPLE:
    print("   | %-10s | %4s | %s |" % (mnem, width,
                                       MB.key_width(mnem, width)))

print("")
print("   the classifier over the operand texts the corpus spells:")
LINES = [("faddp", "faddp %st,%st(1)", 16),
         ("fucomip", "fucomip %st(1),%st", 8),
         ("fldz", "fldz", 16),
         ("fldt", "fldt 0x8(%rsp)", 16),
         ("fildll", "fildll -0x8(%rsp)", 16),
         ("setne", "setne %al", 8),
         ("cmovbe", "cmovbe %eax,%ecx", 8),
         ("addss", "addss %xmm1,%xmm0", 16),
         ("cvtsi2sd", "cvtsi2sd %eax,%xmm0", 8),
         ("ucomiss", "ucomiss %xmm1,%xmm0", 8),
         ("add", "add %esi,%edi", 4)]
MB._install_gpr_widths()
for mnem, line, size in LINES:
    shape, width, cause = MB.classify_line(mnem, line, size)
    print("   | %-24s | %-8s | %-5s | key_width %-4s | %s |"
          % (line, shape, width,
             MB.key_width(mnem, width) if shape else "-",
             cause or ""))
print("")
print("[3/3] the sweep's own shapes for those same mnemonics")
sys.path.insert(0, "PseudoCoupHQ/Research/op_pipeline")
sys.path.insert(0, "PseudoCoupHQ/Research/op_pipeline/lean")
import model_translate as MT
for mnem in ("faddp", "fucomip", "addss", "setne"):
    seen = []
    for shape, width, texts in MT.attempts_for(mnem):
        if shape in MB.ST_SHAPES or shape in ("xmm_xmm", "gpr_one"):
            seen.append("%s/%s->%s" % (shape, width,
                                       MB.key_width(mnem, width)))
    print("   %-10s %s" % (mnem, " ".join(seen)))
print("")
print("peak RSS: %d kB"
      % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY
echo "[3/3] done"
