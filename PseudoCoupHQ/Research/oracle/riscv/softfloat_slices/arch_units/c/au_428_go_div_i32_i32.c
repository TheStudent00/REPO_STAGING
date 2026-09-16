/*
 * arch-unit 428  --  go  `a / b`  lhs=int32 rhs=int32
 * symbol main.op_96   outcome LIFTED   19 arch-opcodes
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   ld t1, 0x10(s11)                     prologue   stack-growth check -> elided
 *   bltu t1, sp, 0x6c748 <main.op_96+0x18> prologue   stack-growth check -> elided
 *   c.swsp a0, 0x8(sp)                   prologue   stack-growth spill -> elided
 *   c.swsp a1, 0xc(sp)                   prologue   stack-growth spill -> elided
 *   jal t0, 0x6a7a0 <runtime.morestack_noctxt.abi0> prologue   stack-growth call / restart / panic tail -> elided
 *   c.lwsp a0, 0x8(sp)                   prologue   stack-growth reload -> elided
 *   c.lwsp a1, 0xc(sp)                   prologue   stack-growth reload -> elided
 *   jal zero, 0x6c730 <main.op_96>       prologue   stack-growth call / restart / panic tail -> elided
 *   sd ra, -0x8(sp)                      frame      frame bookkeeping -> elided
 *   c.addi sp, -0x8                      frame      frame bookkeeping -> elided
 *   c.sdsp ra, 0x0(sp)                   frame      frame bookkeeping -> elided
 *   addiw t0, a1, 0x0                    integer    operator:+ then sign-extend the low 32 bits
 *   beq t0, zero, 0x6c764 <main.op_96+0x34> guard      guard branch -> a `_trap` predicate
 *   divw a0, a0, a1                      integer    written-out restoring division (NOT the language's /)
 *   c.ldsp ra, 0x0(sp)                   frame      frame bookkeeping -> elided
 *   c.addi sp, 0x8                       frame      frame bookkeeping -> elided
 *   jalr zero, 0x0(ra)                   integer    return
 *   jal ra, 0x408e8 <runtime.panicdivide> trap-tail  the runtime panic the guard branches to -> the `_trap` predicate
 *   c.nop                                trap-tail  the runtime panic the guard branches to -> the `_trap` predicate
 *
 * answer: int32, 32 bits.  parameters are operand bit patterns.
 *
 * GUARDED: this arch-unit branches to a go runtime panic.  The function
 * below is the fall-through; the companion `_trap` predicate is 1 exactly
 * when the arch-unit takes the branch instead.
 */
#include "arch_units_int.h"

uint64_t au_428_go_div_i32_i32(uint64_t p0, uint64_t p1)
{
    /* a0: operand `a` (int32) sign-extended to XLEN, as the ABI presents it */
    const uint64_t v1 = au_sext32(p0);
    /* a1: operand `b` (int32) sign-extended to XLEN, as the ABI presents it */
    const uint64_t v2 = au_sext32(p1);
    const uint64_t v3 = au_addw(v2, UINT64_C(0x0));
    const uint64_t v4 = au_divw(v1, v2);
    /* the answer is int32, 32 bits */
    return ((v4) & UINT64_C(0xffffffff));
}

uint64_t au_428_go_div_i32_i32_trap(uint64_t p0, uint64_t p1)
{
    /* a0: operand `a` (int32) sign-extended to XLEN, as the ABI presents it */
    const uint64_t v1 = au_sext32(p0);
    /* a1: operand `b` (int32) sign-extended to XLEN, as the ABI presents it */
    const uint64_t v2 = au_sext32(p1);
    const uint64_t v3 = au_addw(v2, UINT64_C(0x0));
    return au_eqz(v3);
}
