/*
 * arch-unit 324  --  c  `a || b`  lhs=bool rhs=int64_t
 * symbol op_313   outcome LIFTED   3 arch-opcodes
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   sltu a1, zero, a1                    integer    operator:< unsigned
 *   c.or a0, a1                          integer    operator:|
 *   c.jr ra                              integer    return
 *
 * answer: int32_t, 32 bits.  parameters are operand bit patterns.
 */
#include "arch_units_int.h"

uint64_t au_324_c_lor_bool_i64(uint64_t p0, uint64_t p1)
{
    /* a0: operand `a` (bool) zero-extended to XLEN */
    const uint64_t v1 = ((p0) & UINT64_C(0x1));
    /* a1: operand `b` (int64_t) arrives in a1 */
    const uint64_t v2 = p1;
    const uint64_t v3 = au_sltu(UINT64_C(0x0), v2);
    const uint64_t v4 = au_or(v1, v3);
    /* the answer is int32_t, 32 bits */
    return ((v4) & UINT64_C(0xffffffff));
}
