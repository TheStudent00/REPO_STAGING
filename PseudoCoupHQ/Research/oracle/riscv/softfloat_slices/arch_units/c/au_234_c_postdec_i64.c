/*
 * arch-unit 234  --  c  `a--`  lhs=int64_t rhs=None
 * symbol op_97   outcome LIFTED   1 arch-opcodes
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   c.jr ra                              integer    return
 *
 * answer: int64_t, 64 bits.  parameters are operand bit patterns.
 */
#include "arch_units_int.h"

uint64_t au_234_c_postdec_i64(uint64_t p0)
{
    /* a0: operand `a` (int64_t) arrives in a0 */
    const uint64_t v1 = p0;
    /* the answer is int64_t, 64 bits */
    return v1;
}
