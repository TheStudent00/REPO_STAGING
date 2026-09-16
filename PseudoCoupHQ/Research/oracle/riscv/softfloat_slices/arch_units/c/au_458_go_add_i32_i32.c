/*
 * arch-unit 458  --  go  `a + b`  lhs=int32 rhs=int32
 * symbol main.op_312   outcome LIFTED   2 arch-opcodes
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   c.add a0, a1                         integer    operator:+
 *   jalr zero, 0x0(ra)                   integer    return
 *
 * answer: int32, 32 bits.  parameters are operand bit patterns.
 */
#include "arch_units_int.h"

uint64_t au_458_go_add_i32_i32(uint64_t p0, uint64_t p1)
{
    /* a0: operand `a` (int32) sign-extended to XLEN, as the ABI presents it */
    const uint64_t v1 = au_sext32(p0);
    /* a1: operand `b` (int32) sign-extended to XLEN, as the ABI presents it */
    const uint64_t v2 = au_sext32(p1);
    const uint64_t v3 = au_add(v1, v2);
    /* the answer is int32, 32 bits */
    return ((v3) & UINT64_C(0xffffffff));
}
