#!/bin/bash
# bb1 lane 5 -- the one refusal of lane 4 that came with NO words: `remu
# gpr_gpr_gpr 64` was BUILD_REFUSED on c, cpp and go with an empty
# diagnostic, while `div` and `rem` at the same size built and carved. The
# objects are still in /work; this lane asks the compiler and the carver
# what they actually said, so the report has a cause and not a blank.
set -u
P=PseudoCoupHQ
RV=$P/Research/oracle/riscv
export HOME=/work
total=4
i=1

echo "[$i/$total] what is in the work folders lane 4 left"; i=$((i+1))
ls -la /work/bb1_largest/bb000021_c /work/bb1_largest/bb000022_cpp \
       /work/bb1_largest/bb000023_go 2>&1 | head -30

echo "[$i/$total] the compile again, by hand, exit code and words"; i=$((i+1))
cd /work/bb1_largest/bb000021_c
clang -std=c17 -O1 --target=riscv64-linux-gnu --gcc-toolchain=/usr \
  -c unit.c -o unit.c.o 2>&1 | head -20
echo "  clang exit: ${PIPESTATUS[0]}"
ls -la unit.c.o 2>&1

echo "[$i/$total] the carve again, by hand"; i=$((i+1))
python3 - <<'EOP'
import sys
sys.path.insert(0, "PseudoCoupHQ/Research/oracle/riscv")
import riscv_carve as CARVE
obj = "/work/bb1_largest/bb000021_c/unit.c.o"
name = "emu_remu_gpr_gpr_gpr_64__reg_a0__c__bit_blast"
cmd = [CARVE.LLVM_OBJDUMP, "-dr", "-M", "no-aliases",
       "--mattr=" + CARVE.MATTR, "--disassemble-symbols=" + name, obj]
rc, out, err = CARVE.sh(cmd, timeout=600)
print("objdump rc:", rc, "stdout bytes:", len(out), "stderr, LITERAL:",
      repr(err[:400]))
print("the first four lines of the disassembly, LITERAL:")
for line in out.split("\n")[:4]:
    print("   ", line)
size = CARVE.symbol_size(obj, name, True)
print("symbol_size:", size)
got = CARVE.extract(out, name, True)
if got is None:
    print("extract: None -- this is the refusal with no words")
else:
    print("extract:", len(got[1]), "instructions")
got, err = CARVE.disassemble(obj, name, True)
if got is None:
    print("disassemble: None; err, LITERAL:", repr(err[:400]))
else:
    print("disassemble:", len(got[1]), "instructions")
EOP
echo "  exit: $?"

echo "[$i/$total] the go object of the same cell"
python3 - <<'EOP'
import os
import sys
sys.path.insert(0, "PseudoCoupHQ/Research/oracle/riscv")
import riscv_carve as CARVE
obj = "/work/bb1_largest/bb000023_go/bin_rv"
print("the go binary exists:", os.path.exists(obj))
if os.path.exists(obj):
    name = "main.emu_remu_gpr_gpr_gpr_64__reg_a0__go__bit_blast"
    got, err = CARVE.disassemble(obj, name, True)
    if got is None:
        print("disassemble: None; err, LITERAL:", repr(err[:400]))
    else:
        print("disassemble:", len(got[1]), "instructions")
EOP
echo "  exit: $?"
echo "lane bb1_l5 done"
