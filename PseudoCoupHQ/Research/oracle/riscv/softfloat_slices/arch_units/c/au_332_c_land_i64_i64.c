/*
 * arch-unit 332  --  c  `a && b`  lhs=int64_t rhs=int64_t
 * symbol op_325   outcome LIFTED   4 arch-opcodes
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   sltu a0, zero, a0                    integer    operator:< unsigned
 *   sltu a1, zero, a1                    integer    operator:< unsigned
 *   c.and a0, a1                         integer    operator:&
 *   c.jr ra                              integer    return
 *
 * answer: int32_t, 32 bits.  parameters are operand bit patterns.
 */
#include "arch_units_int.h"

uint64_t au_332_c_land_i64_i64(uint64_t p0, uint64_t p1)
{
    /* a0: operand `a` (int64_t) arrives in a0 */
    const uint64_t v1 = p0;
    /* a1: operand `b` (int64_t) arrives in a1 */
    const uint64_t v2 = p1;
    const uint64_t v3 = au_sltu(UINT64_C(0x0), v1);
    const uint64_t v4 = au_sltu(UINT64_C(0x0), v2);
    const uint64_t v5 = au_and(v3, v4);
    /* the answer is int32_t, 32 bits */
    return ((v5) & UINT64_C(0xffffffff));
}
