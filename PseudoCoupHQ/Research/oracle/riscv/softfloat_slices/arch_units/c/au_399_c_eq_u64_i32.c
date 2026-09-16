/*
 * arch-unit 399  --  c  `a == b`  lhs=uint64_t rhs=int32_t
 * symbol op_474   outcome LIFTED   3 arch-opcodes
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   c.xor a0, a1                         integer    operator:^
 *   sltiu a0, a0, 0x1                    integer    operator:< unsigned
 *   c.jr ra                              integer    return
 *
 * answer: int32_t, 32 bits.  parameters are operand bit patterns.
 */
#include "arch_units_int.h"

uint64_t au_399_c_eq_u64_i32(uint64_t p0, uint64_t p1)
{
    /* a0: operand `a` (uint64_t) arrives in a0 */
    const uint64_t v1 = p0;
    /* a1: operand `b` (int32_t) sign-extended to XLEN, as the ABI presents it */
    const uint64_t v2 = au_sext32(p1);
    const uint64_t v3 = au_xor(v1, v2);
    const uint64_t v4 = au_sltu(v3, UINT64_C(0x1));
    /* the answer is int32_t, 32 bits */
    return ((v4) & UINT64_C(0xffffffff));
}
