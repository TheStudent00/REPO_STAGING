/*
 * arch-unit 408  --  c  `a != b`  lhs=int32_t rhs=int64_t
 * symbol op_499   outcome LIFTED   3 arch-opcodes
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   c.xor a0, a1                         integer    operator:^
 *   sltu a0, zero, a0                    integer    operator:< unsigned
 *   c.jr ra                              integer    return
 *
 * answer: int32_t, 32 bits.  parameters are operand bit patterns.
 */
#include "arch_units_int.h"

uint64_t au_408_c_ne_i32_i64(uint64_t p0, uint64_t p1)
{
    /* a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it */
    const uint64_t v1 = au_sext32(p0);
    /* a1: operand `b` (int64_t) arrives in a1 */
    const uint64_t v2 = p1;
    const uint64_t v3 = au_xor(v1, v2);
    const uint64_t v4 = au_sltu(UINT64_C(0x0), v3);
    /* the answer is int32_t, 32 bits */
    return ((v4) & UINT64_C(0xffffffff));
}
