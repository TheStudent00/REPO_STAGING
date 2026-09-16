/*
 * arch-unit 206  --  c  `__alignof__ a`  lhs=float rhs=None
 * symbol op_57   outcome LIFTED   2 arch-opcodes
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   c.li a0, 0x4                         integer    constant
 *   c.jr ra                              integer    return
 *
 * answer: uint64_t, 64 bits.  parameters are operand bit patterns.
 */
#include "arch_units_int.h"

uint64_t au_206_c_alignof_gnu2_f32(uint64_t p0)
{
    /* fa0: operand `a` (float) arrives in fa0 as a bit pattern */
    const uint64_t v1 = ((p0) & UINT64_C(0xffffffff));
    const uint64_t v2 = UINT64_C(0x4);
    /* the answer is uint64_t, 64 bits */
    return v2;
}
