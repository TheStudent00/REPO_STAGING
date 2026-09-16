/*
 * arch-unit 447  --  go  `a >> b`  lhs=int64 rhs=int64
 * symbol main.op_211   outcome LIFTED   21 arch-opcodes
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   ld t1, 0x10(s11)                     prologue   stack-growth check -> elided
 *   bltu t1, sp, 0x6c738 <main.op_211+0x18> prologue   stack-growth check -> elided
 *   c.sdsp a0, 0x8(sp)                   prologue   frame bookkeeping -> elided
 *   c.sdsp a1, 0x10(sp)                  prologue   frame bookkeeping -> elided
 *   jal t0, 0x6a790 <runtime.morestack_noctxt.abi0> prologue   stack-growth call / restart / panic tail -> elided
 *   c.ldsp a0, 0x8(sp)                   prologue   frame bookkeeping -> elided
 *   c.ldsp a1, 0x10(sp)                  prologue   frame bookkeeping -> elided
 *   jal zero, 0x6c720 <main.op_211>      prologue   stack-growth call / restart / panic tail -> elided
 *   sd ra, -0x8(sp)                      frame      frame bookkeeping -> elided
 *   c.addi sp, -0x8                      frame      frame bookkeeping -> elided
 *   c.sdsp ra, 0x0(sp)                   frame      frame bookkeeping -> elided
 *   blt a1, zero, 0x6c75a <main.op_211+0x3a> guard      guard branch -> a `_trap` predicate
 *   sltiu t0, a1, 0x40                   integer    operator:< unsigned
 *   c.addi t0, -0x1                      integer    operator:+
 *   or t0, a1, t0                        integer    operator:|
 *   sra a0, a0, t0                       integer    arithmetic right shift, written out in unsigned bit operations
 *   c.ldsp ra, 0x0(sp)                   frame      frame bookkeeping -> elided
 *   c.addi sp, 0x8                       frame      frame bookkeeping -> elided
 *   jalr zero, 0x0(ra)                   integer    return
 *   jal ra, 0x40830 <runtime.panicshift> trap-tail  the runtime panic the guard branches to -> the `_trap` predicate
 *   c.nop                                trap-tail  the runtime panic the guard branches to -> the `_trap` predicate
 *
 * answer: int64, 64 bits.  parameters are operand bit patterns.
 *
 * GUARDED: this arch-unit branches to a go runtime panic.  The function
 * below is the fall-through; the companion `_trap` predicate is 1 exactly
 * when the arch-unit takes the branch instead.
 */
#include "arch_units_int.h"

uint64_t au_447_go_shr_i64_i64(uint64_t p0, uint64_t p1)
{
    /* a0: operand `a` (int64) arrives in a0 */
    const uint64_t v1 = p0;
    /* a1: operand `b` (int64) arrives in a1 */
    const uint64_t v2 = p1;
    const uint64_t v3 = au_sltu(v2, UINT64_C(0x40));
    const uint64_t v4 = au_add(v3, UINT64_C(0xffffffffffffffff));
    const uint64_t v5 = au_or(v2, v4);
    const uint64_t v6 = au_sra(v1, v5);
    /* the answer is int64, 64 bits */
    return v6;
}

uint64_t au_447_go_shr_i64_i64_trap(uint64_t p0, uint64_t p1)
{
    /* a0: operand `a` (int64) arrives in a0 */
    const uint64_t v1 = p0;
    /* a1: operand `b` (int64) arrives in a1 */
    const uint64_t v2 = p1;
    return au_ltz(v2);
}
