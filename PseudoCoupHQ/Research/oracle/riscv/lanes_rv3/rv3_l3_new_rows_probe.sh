#!/usr/bin/env bash
# rv3 lane 3 -- can the harness of `sail_points.py` state the five new
# rows at all?  Two questions, each asked with its own one-line probe and
# answered LITERAL: does the assembler accept each instruction under an
# -march string, and does the ratified Sail model's own simulator carry
# the extensions those instructions belong to.
set -u
export HOME=/work
mkdir -p /work/rv3probe2
total=5

echo "[1/$total] the five instructions, assembled"
cat > /work/rv3probe2/five.S <<'EOF'
    .globl _start
_start:
    add.uw   a2, a0, a1
    bseti    a2, a0, 63
    c.mul    a0, a1
    c.zext.w a0
    fsgnjn.d fa2, fa0, fa1
EOF
for M in rv64gc_zicond rv64gc_zba_zbb_zbs_zicond \
         rv64gc_zba_zbb_zbs_zcb_zicond; do
  echo "-- -march=$M"
  clang --target=riscv64-unknown-elf -march=$M -mabi=lp64d \
    -c /work/rv3probe2/five.S -o /work/rv3probe2/five.o 2>&1 | head -12
  echo "   rc=$?"
done

echo "[2/$total] what the assembler produced, read back"
llvm-objdump -dr -M no-aliases --mattr=+m,+a,+f,+d,+c,+zba,+zbb,+zbs,+zcb \
  /work/rv3probe2/five.o 2>&1 | tail -12

echo "[3/$total] the simulator's own ISA string and its flags"
/usr/local/bin/sail_riscv_sim --help 2>&1 | head -40

echo "[4/$total] the model's own source for these instructions"
grep -rl "ZEXT_W\|C_MUL\|c.zext.w\|RISCV_ADDUW\|ADDUW" \
  /sources/sail-riscv/model 2>&1 | head -10
echo "-- the model's extension folders"
ls /sources/sail-riscv/model/extensions 2>&1 | head -40

echo "[5/$total] the simulator run on a bare-metal program that uses them"
cat > /work/rv3probe2/one.S <<'EOF'
    .section .text.init, "ax", @progbits
    .globl _start
_start:
    la    s0, inputs
    la    s1, results
    li    s2, 2
loop:
    ld    a0, 0(s0)
    ld    a1, 8(s0)
    add.uw a2, a0, a1
    sd    a2, 0(s1)
    addi  s0, s0, 16
    addi  s1, s1, 8
    addi  s2, s2, -1
    bnez  s2, loop
    la    t0, tohost
    li    t1, 1
    sd    t1, 0(t0)
spin:
    j     spin

    .section .data
    .align 3
inputs:
    .dword 0xffffffffffffffff
    .dword 0x0000000000000001
    .dword 0x00000000ffffffff
    .dword 0xffffffff00000000
    .align 6
    .globl tohost
tohost:
    .dword 0
    .globl fromhost
fromhost:
    .dword 0
    .align 3
    .globl begin_signature
begin_signature:
results:
    .space 16
    .globl end_signature
end_signature:
EOF
cat > /work/rv3probe2/link.ld <<'EOF'
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
clang --target=riscv64-unknown-elf -march=rv64gc_zba_zbb_zbs_zcb_zicond \
  -mabi=lp64d -nostdlib -fuse-ld=lld -T /work/rv3probe2/link.ld \
  /work/rv3probe2/one.S -o /work/rv3probe2/one.elf 2>&1 | head -5
echo "link rc=$?"
/usr/local/bin/sail_riscv_sim --inst-limit 3000 \
  --test-signature /work/rv3probe2/sig.txt /work/rv3probe2/one.elf 2>&1 \
  | tail -8
echo "sim rc=$?"
echo "-- the signature"
cat /work/rv3probe2/sig.txt 2>&1
echo "lane rv3_l3 done"
