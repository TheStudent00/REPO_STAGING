/*
 * arch-unit 258  --  c  `a - b`  lhs=int32_t rhs=bool
 * symbol op_143   outcome LIFTED   2 arch-opcodes
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   c.subw a0, a1                        integer    operator:- then sign-extend the low 32 bits
 *   c.jr ra                              integer    return
 *
 * answer: int32_t, 32 bits.  parameters are operand bit patterns.
 */
#include "arch_units_int.h"

uint64_t au_258_c_sub_i32_bool(uint64_t p0, uint64_t p1)
{
    /* a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it */
    const uint64_t v1 = au_sext32(p0);
    /* a1: operand `b` (bool) zero-extended to XLEN */
    const uint64_t v2 = ((p1) & UINT64_C(0x1));
    const uint64_t v3 = au_subw(v1, v2);
    /* the answer is int32_t, 32 bits */
    return ((v3) & UINT64_C(0xffffffff));
}
