/*
 * arch-unit 343  --  c  `a | b`  lhs=int32_t rhs=int32_t
 * symbol op_354   outcome LIFTED   2 arch-opcodes
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   c.or a0, a1                          integer    operator:|
 *   c.jr ra                              integer    return
 *
 * answer: int32_t, 32 bits.  parameters are operand bit patterns.
 */
#include "arch_units_int.h"

uint64_t au_343_c_bor_i32_i32(uint64_t p0, uint64_t p1)
{
    /* a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it */
    const uint64_t v1 = au_sext32(p0);
    /* a1: operand `b` (int32_t) sign-extended to XLEN, as the ABI presents it */
    const uint64_t v2 = au_sext32(p1);
    const uint64_t v3 = au_or(v1, v2);
    /* the answer is int32_t, 32 bits */
    return ((v3) & UINT64_C(0xffffffff));
}
