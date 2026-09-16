/*
 * arch-unit 247  --  c  `a + b`  lhs=uint64_t rhs=int32_t
 * symbol op_114   outcome LIFTED   2 arch-opcodes
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   c.add a0, a1                         integer    operator:+
 *   c.jr ra                              integer    return
 *
 * answer: uint64_t, 64 bits.  parameters are operand bit patterns.
 */
#include "arch_units_int.h"

uint64_t au_247_c_add_u64_i32(uint64_t p0, uint64_t p1)
{
    /* a0: operand `a` (uint64_t) arrives in a0 */
    const uint64_t v1 = p0;
    /* a1: operand `b` (int32_t) sign-extended to XLEN, as the ABI presents it */
    const uint64_t v2 = au_sext32(p1);
    const uint64_t v3 = au_add(v1, v2);
    /* the answer is uint64_t, 64 bits */
    return v3;
}
