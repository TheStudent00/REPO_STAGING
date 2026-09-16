/*
 * arch-unit 231  --  c  `a++`  lhs=double rhs=None
 * symbol op_94   outcome LIFTED   1 arch-opcodes
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   c.jr ra                              integer    return
 *
 * answer: double, 64 bits.  parameters are operand bit patterns.
 */
#include "arch_units_int.h"

uint64_t au_231_c_postinc_f64(uint64_t p0)
{
    /* fa0: operand `a` (double) arrives in fa0 as a bit pattern */
    const uint64_t v1 = p0;
    /* the answer is double, 64 bits */
    return v1;
}
