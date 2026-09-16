/*
 * arch-unit 217  --  c  `_Alignof a`  lhs=uint64_t rhs=None
 * symbol op_80   outcome LIFTED   2 arch-opcodes
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   c.li a0, 0x8                         integer    constant
 *   c.jr ra                              integer    return
 *
 * answer: uint64_t, 64 bits.  parameters are operand bit patterns.
 */
#include "arch_units_int.h"

uint64_t au_217_c_alignof_c11_u64(uint64_t p0)
{
    /* a0: operand `a` (uint64_t) arrives in a0 */
    const uint64_t v1 = p0;
    const uint64_t v2 = UINT64_C(0x8);
    /* the answer is uint64_t, 64 bits */
    return v2;
}
