/*
 * arch-unit 310  --  c  `a % b`  lhs=bool rhs=bool
 * symbol op_281   outcome LIFTED   2 arch-opcodes
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   c.li a0, 0x0                         integer    constant
 *   c.jr ra                              integer    return
 *
 * answer: int32_t, 32 bits.  parameters are operand bit patterns.
 */
#include "arch_units_int.h"

uint64_t au_310_c_rem_bool_bool(uint64_t p0, uint64_t p1)
{
    /* a0: operand `a` (bool) zero-extended to XLEN */
    const uint64_t v1 = ((p0) & UINT64_C(0x1));
    /* a1: operand `b` (bool) zero-extended to XLEN */
    const uint64_t v2 = ((p1) & UINT64_C(0x1));
    const uint64_t v3 = UINT64_C(0x0);
    /* the answer is int32_t, 32 bits */
    return ((v3) & UINT64_C(0xffffffff));
}
