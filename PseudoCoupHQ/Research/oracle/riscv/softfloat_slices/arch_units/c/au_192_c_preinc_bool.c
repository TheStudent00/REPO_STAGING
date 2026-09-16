/*
 * arch-unit 192  --  c  `++a`  lhs=bool rhs=None
 * symbol op_41   outcome LIFTED   2 arch-opcodes
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   c.li a0, 0x1                         integer    constant
 *   c.jr ra                              integer    return
 *
 * answer: _Bool, 1 bits.  parameters are operand bit patterns.
 */
#include "arch_units_int.h"

uint64_t au_192_c_preinc_bool(uint64_t p0)
{
    /* a0: operand `a` (bool) zero-extended to XLEN */
    const uint64_t v1 = ((p0) & UINT64_C(0x1));
    const uint64_t v2 = UINT64_C(0x1);
    /* the answer is _Bool, 1 bits */
    return ((v2) & UINT64_C(0x1));
}
