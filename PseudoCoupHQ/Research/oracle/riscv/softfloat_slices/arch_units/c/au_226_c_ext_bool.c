/*
 * arch-unit 226  --  c  `__extension__ a`  lhs=bool rhs=None
 * symbol op_89   outcome LIFTED   1 arch-opcodes
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   c.jr ra                              integer    return
 *
 * answer: _Bool, 1 bits.  parameters are operand bit patterns.
 */
#include "arch_units_int.h"

uint64_t au_226_c_ext_bool(uint64_t p0)
{
    /* a0: operand `a` (bool) zero-extended to XLEN */
    const uint64_t v1 = ((p0) & UINT64_C(0x1));
    /* the answer is _Bool, 1 bits */
    return ((v1) & UINT64_C(0x1));
}
