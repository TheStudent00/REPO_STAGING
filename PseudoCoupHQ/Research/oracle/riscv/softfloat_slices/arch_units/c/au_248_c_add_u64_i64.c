/*
 * arch-unit 248  --  c  `a + b`  lhs=uint64_t rhs=int64_t
 * symbol op_115   outcome LIFTED   2 arch-opcodes
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   c.add a0, a1                         integer    operator:+
 *   c.jr ra                              integer    return
 *
 * answer: uint64_t, 64 bits.  parameters are operand bit patterns.
 */
#include "arch_units_int.h"

uint64_t au_248_c_add_u64_i64(uint64_t p0, uint64_t p1)
{
    /* a0: operand `a` (uint64_t) arrives in a0 */
    const uint64_t v1 = p0;
    /* a1: operand `b` (int64_t) arrives in a1 */
    const uint64_t v2 = p1;
    const uint64_t v3 = au_add(v1, v2);
    /* the answer is uint64_t, 64 bits */
    return v3;
}
