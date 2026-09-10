#!/usr/bin/env bash
# rv3 lane 5 -- WHY the float row refused, asked directly.  The same
# bare-metal program the harness writes, run by hand so the simulator's
# own words are visible, first as the harness writes it and then with the
# float unit enabled in `mstatus`.
set -u
export HOME=/work
mkdir -p /work/rv3float
total=3

cat > /work/rv3float/link.ld <<'EOF'
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

write_program () {
  local out="$1"
  local prologue="$2"
  cat > "$out" <<EOF
    .section .text.init, "ax", @progbits
    .globl _start
_start:
$prologue
    la    s0, inputs
    la    s1, results
    li    s2, 2
loop:
    ld    a0, 0(s0)
    ld    a1, 8(s0)
    fmv.d.x fa0, a0
    fmv.d.x fa1, a1
    fsgnjn.d fa2, fa0, fa1
    fmv.x.d a2, fa2
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
    .dword 0x3ff0000000000000
    .dword 0x0000000000000000
    .dword 0xc02e000000000000
    .dword 0x8000000000000000
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
}

echo "[1/$total] the program exactly as the rv1 harness writes it"
write_program /work/rv3float/plain.S ""
clang --target=riscv64-unknown-elf -march=rv64gc_zba_zbb_zbs_zcb_zicond \
  -mabi=lp64d -nostdlib -fuse-ld=lld -T /work/rv3float/link.ld \
  /work/rv3float/plain.S -o /work/rv3float/plain.elf
echo "link rc=$?"
/usr/local/bin/sail_riscv_sim --inst-limit 3000 \
  --test-signature /work/rv3float/plain_sig.txt /work/rv3float/plain.elf
echo "sim rc=$?"
echo "-- signature:"
cat /work/rv3float/plain_sig.txt 2>&1

echo "[2/$total] the same program with mstatus.FS set to Dirty first"
write_program /work/rv3float/fs.S "    li    t0, 0x6000
    csrs  mstatus, t0"
clang --target=riscv64-unknown-elf -march=rv64gc_zba_zbb_zbs_zcb_zicond \
  -mabi=lp64d -nostdlib -fuse-ld=lld -T /work/rv3float/link.ld \
  /work/rv3float/fs.S -o /work/rv3float/fs.elf
echo "link rc=$?"
/usr/local/bin/sail_riscv_sim --inst-limit 3000 \
  --test-signature /work/rv3float/fs_sig.txt /work/rv3float/fs.elf
echo "sim rc=$?"
echo "-- signature:"
cat /work/rv3float/fs_sig.txt 2>&1

echo "[3/$total] what the reference says the same two points give"
python3 - <<'EOF'
import sys
sys.path.insert(0, "PseudoCoupHQ/Research/oracle/riscv")
import sail_points as SP
term, first, second = SP.reference_term("fsgnjn.d fa2, fa0, fa1",
                                        SP.homes_of("fsgnjn.d"))
for left, right in ((0x3ff0000000000000, 0x0000000000000000),
                    (0xc02e000000000000, 0x8000000000000000)):
    print("0x%016x" % SP.evaluate(term, first, second, left, right))
EOF
echo "lane rv3_l5 done"
