/*
 * arch-unit 357  --  c  `a | b`  lhs=bool rhs=uint64_t
 * symbol op_386   outcome LIFTED   2 arch-opcodes
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   c.or a0, a1                          integer    operator:|
 *   c.jr ra                              integer    return
 *
 * answer: uint64_t, 64 bits.  parameters are operand bit patterns.
 */
#include "arch_units_int.h"

uint64_t au_357_c_bor_bool_u64(uint64_t p0, uint64_t p1)
{
    /* a0: operand `a` (bool) zero-extended to XLEN */
    const uint64_t v1 = ((p0) & UINT64_C(0x1));
    /* a1: operand `b` (uint64_t) arrives in a1 */
    const uint64_t v2 = p1;
    const uint64_t v3 = au_or(v1, v2);
    /* the answer is uint64_t, 64 bits */
    return v3;
}
