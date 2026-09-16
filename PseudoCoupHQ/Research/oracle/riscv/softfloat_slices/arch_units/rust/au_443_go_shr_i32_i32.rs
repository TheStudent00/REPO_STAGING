// arch-unit 443  --  go  `a >> b`  lhs=int32 rhs=int32
// symbol main.op_204   outcome LIFTED   24 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   ld t1, 0x10(s11)                     prologue   stack-growth check -> elided
//   bltu t1, sp, 0x6c748 <main.op_204+0x18> prologue   stack-growth check -> elided
//   c.swsp a0, 0x8(sp)                   prologue   stack-growth spill -> elided
//   c.swsp a1, 0xc(sp)                   prologue   stack-growth spill -> elided
//   jal t0, 0x6a7a0 <runtime.morestack_noctxt.abi0> prologue   stack-growth call / restart / panic tail -> elided
//   c.lwsp a0, 0x8(sp)                   prologue   stack-growth reload -> elided
//   c.lwsp a1, 0xc(sp)                   prologue   stack-growth reload -> elided
//   jal zero, 0x6c730 <main.op_204>      prologue   stack-growth call / restart / panic tail -> elided
//   sd ra, -0x8(sp)                      frame      frame bookkeeping -> elided
//   c.addi sp, -0x8                      frame      frame bookkeeping -> elided
//   c.sdsp ra, 0x0(sp)                   frame      frame bookkeeping -> elided
//   addiw t0, a1, 0x0                    integer    operator:+ then sign-extend the low 32 bits
//   blt t0, zero, 0x6c776 <main.op_204+0x46> guard      guard branch -> a `_trap` predicate
//   slli t0, a1, 0x20                    integer    operator:<<
//   srli t0, t0, 0x20                    integer    operator:>> unsigned
//   sltiu t0, t0, 0x20                   integer    operator:< unsigned
//   c.addi t0, -0x1                      integer    operator:+
//   or t0, a1, t0                        integer    operator:|
//   sraw a0, a0, t0                      integer    arithmetic right shift of the low 32 bits, written out
//   c.ldsp ra, 0x0(sp)                   frame      frame bookkeeping -> elided
//   c.addi sp, 0x8                       frame      frame bookkeeping -> elided
//   jalr zero, 0x0(ra)                   integer    return
//   jal ra, 0x408a0 <runtime.panicshift> trap-tail  the runtime panic the guard branches to -> the `_trap` predicate
//   c.nop                                trap-tail  the runtime panic the guard branches to -> the `_trap` predicate
//
// answer: int32, 32 bits.  parameters are operand bit patterns.
//
// GUARDED: this arch-unit branches to a go runtime panic.  The function
// below is the fall-through; the companion `_trap` predicate is 1 exactly
// when the arch-unit takes the branch instead.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_443_go_shr_i32_i32(p0: u64, p1: u64) -> u64 {
    // a0: operand `a` (int32) sign-extended to XLEN, as the ABI presents it
    let v1: u64 = au_sext32(p0);
    // a1: operand `b` (int32) sign-extended to XLEN, as the ABI presents it
    let v2: u64 = au_sext32(p1);
    let v3: u64 = au_addw(v2, 0x0u64);
    let v4: u64 = au_sll(v2, 0x20u64);
    let v5: u64 = au_srl(v4, 0x20u64);
    let v6: u64 = au_sltu(v5, 0x20u64);
    let v7: u64 = au_add(v6, 0xffffffffffffffffu64);
    let v8: u64 = au_or(v2, v7);
    let v9: u64 = au_sraw(v1, v8);
    // the answer is int32, 32 bits
    ((v9) & 0xffffffffu64)
}

pub fn au_443_go_shr_i32_i32_trap(p0: u64, p1: u64) -> u64 {
    // a0: operand `a` (int32) sign-extended to XLEN, as the ABI presents it
    let v1: u64 = au_sext32(p0);
    // a1: operand `b` (int32) sign-extended to XLEN, as the ABI presents it
    let v2: u64 = au_sext32(p1);
    let v3: u64 = au_addw(v2, 0x0u64);
    au_ltz(v3)
}
