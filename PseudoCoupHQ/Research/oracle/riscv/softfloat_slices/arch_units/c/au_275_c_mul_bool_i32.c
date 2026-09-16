/*
 * arch-unit 275  --  c  `a * b`  lhs=bool rhs=int32_t
 * symbol op_204   outcome LIFTED   2 arch-opcodes
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   czero.eqz a0, a1, a0                 integer    conditional select
 *   c.jr ra                              integer    return
 *
 * answer: int32_t, 32 bits.  parameters are operand bit patterns.
 */
#include "arch_units_int.h"

uint64_t au_275_c_mul_bool_i32(uint64_t p0, uint64_t p1)
{
    /* a0: operand `a` (bool) zero-extended to XLEN */
    const uint64_t v1 = ((p0) & UINT64_C(0x1));
    /* a1: operand `b` (int32_t) sign-extended to XLEN, as the ABI presents it */
    const uint64_t v2 = au_sext32(p1);
    const uint64_t v3 = au_czeqz(v2, v1);
    /* the answer is int32_t, 32 bits */
    return ((v3) & UINT64_C(0xffffffff));
}
