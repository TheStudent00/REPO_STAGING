/*
 * arch-unit 314  --  c  `a || b`  lhs=int32_t rhs=bool
 * symbol op_287   outcome LIFTED   3 arch-opcodes
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   sltu a0, zero, a0                    integer    operator:< unsigned
 *   c.or a0, a1                          integer    operator:|
 *   c.jr ra                              integer    return
 *
 * answer: int32_t, 32 bits.  parameters are operand bit patterns.
 */
#include "arch_units_int.h"

uint64_t au_314_c_lor_i32_bool(uint64_t p0, uint64_t p1)
{
    /* a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it */
    const uint64_t v1 = au_sext32(p0);
    /* a1: operand `b` (bool) zero-extended to XLEN */
    const uint64_t v2 = ((p1) & UINT64_C(0x1));
    const uint64_t v3 = au_sltu(UINT64_C(0x0), v1);
    const uint64_t v4 = au_or(v3, v2);
    /* the answer is int32_t, 32 bits */
    return ((v4) & UINT64_C(0xffffffff));
}
