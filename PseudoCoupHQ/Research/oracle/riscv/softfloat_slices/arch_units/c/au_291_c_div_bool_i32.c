/*
 * arch-unit 291  --  c  `a / b`  lhs=bool rhs=int32_t
 * symbol op_240   outcome LIFTED   2 arch-opcodes
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   divw a0, a0, a1                      integer    written-out restoring division (NOT the language's /)
 *   c.jr ra                              integer    return
 *
 * answer: int32_t, 32 bits.  parameters are operand bit patterns.
 */
#include "arch_units_int.h"

uint64_t au_291_c_div_bool_i32(uint64_t p0, uint64_t p1)
{
    /* a0: operand `a` (bool) zero-extended to XLEN */
    const uint64_t v1 = ((p0) & UINT64_C(0x1));
    /* a1: operand `b` (int32_t) sign-extended to XLEN, as the ABI presents it */
    const uint64_t v2 = au_sext32(p1);
    const uint64_t v3 = au_divw(v1, v2);
    /* the answer is int32_t, 32 bits */
    return ((v3) & UINT64_C(0xffffffff));
}
