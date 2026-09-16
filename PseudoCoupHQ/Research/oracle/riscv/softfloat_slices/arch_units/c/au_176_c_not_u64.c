/*
 * arch-unit 176  --  c  `!a`  lhs=uint64_t rhs=None
 * symbol op_2   outcome LIFTED   2 arch-opcodes
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   sltiu a0, a0, 0x1                    integer    operator:< unsigned
 *   c.jr ra                              integer    return
 *
 * answer: int32_t, 32 bits.  parameters are operand bit patterns.
 */
#include "arch_units_int.h"

uint64_t au_176_c_not_u64(uint64_t p0)
{
    /* a0: operand `a` (uint64_t) arrives in a0 */
    const uint64_t v1 = p0;
    const uint64_t v2 = au_sltu(v1, UINT64_C(0x1));
    /* the answer is int32_t, 32 bits */
    return ((v2) & UINT64_C(0xffffffff));
}
