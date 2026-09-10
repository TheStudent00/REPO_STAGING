#!/usr/bin/env bash
# rv1 lane 2 -- how the ratified Sail model's simulator is driven: its reset
# address, how a bare-metal ELF tells it to stop, and which of its readout
# routes (--test-signature / --dump-memory / --trace-gpr) shows the register
# file after ONE instruction.  Exploration only; nothing is written to the
# repo by this lane.
set -u
SIM=/usr/local/bin/sail_riscv_sim
M=/sources/sail-riscv/model
total=7

echo "[1/$total] the default configuration -- the reset address and the memory map"
$SIM --print-default-config 2>&1 | head -80

echo "[2/$total] the ISA string the default configuration gives"
$SIM --print-isa-string 2>&1 | head -5

echo "[3/$total] how the model stops: its own HTIF text"
grep -rn "tohost" $M --include=*.sail 2>/dev/null | head -20
echo "--- and the c emulator's own reading of it"
grep -n "tohost\|htif" /sources/sail-riscv/c_emulator/sail_riscv_sim.cpp 2>/dev/null | head -20

echo "[4/$total] the model's own text for the base integer instructions"
ls $M/core 2>&1 | head -40
echo "--- the files naming RISCV_ADD / RTYPE"
grep -rln "RISCV_ADD\|RTYPE" $M 2>/dev/null | head -20

echo "[5/$total] a bare-metal ELF, hand written, at the reset address"
W=/work/rv1sim
rm -rf $W; mkdir -p $W
cat > $W/one.S <<'EOF'
    .section .text.init, "ax"
    .globl _start
_start:
    li   t0, 5
    li    t1, 3
    add   t2, t0, t1
    la    t3, sig_begin
    sd    t2, 0(t3)
    la    t3, tohost
    li    t4, 1
    sd    t4, 0(t3)
1:  j 1b

    .section .data
    .align 6
    .globl tohost
tohost: .dword 0
    .globl fromhost
fromhost: .dword 0
    .globl sig_begin
    .globl begin_signature
sig_begin:
begin_signature:
    .dword 0
    .dword 0
    .globl end_signature
end_signature:
EOF
cat > $W/link.ld <<'EOF'
OUTPUT_ARCH(riscv)
ENTRY(_start)
SECTIONS
{
  . = 0x80000000;
  .text.init : { *(.text.init) }
  .text : { *(.text) }
  . = ALIGN(0x1000);
  .data : { *(.data) }
}
EOF
clang --target=riscv64-unknown-elf -march=rv64gc -mabi=lp64d -nostdlib -fuse-ld=lld \
      -T $W/link.ld $W/one.S -o $W/one.elf 2>&1; echo "clang rc=$?"
llvm-objdump -d $W/one.elf 2>&1 | head -30
llvm-nm $W/one.elf 2>&1 | head -20

echo "[6/$total] run it: does the simulator stop, and what does --test-signature give"
$SIM --inst-limit 200 --test-signature $W/sig.txt $W/one.elf 2>&1 | tail -30
echo "--- signature file"
cat $W/sig.txt 2>&1 | head -10

echo "[7/$total] the trace route: --trace-gpr over the same ELF"
$SIM --inst-limit 200 --trace-gpr --use-abi-names $W/one.elf 2>&1 | head -40

python3 -c "
import resource
print('peak RSS: %.1f MB' % (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024.0))
"
echo "--- lane finished"
