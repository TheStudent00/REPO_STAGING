/*
 * arch-unit 209  --  c  `__alignof a`  lhs=int32_t rhs=None
 * symbol op_60   outcome LIFTED   2 arch-opcodes
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   c.li a0, 0x4                         integer    constant
 *   c.jr ra                              integer    return
 *
 * answer: uint64_t, 64 bits.  parameters are operand bit patterns.
 */
#include "arch_units_int.h"

uint64_t au_209_c_alignof_gnu_i32(uint64_t p0)
{
    /* a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it */
    const uint64_t v1 = au_sext32(p0);
    const uint64_t v2 = UINT64_C(0x4);
    /* the answer is uint64_t, 64 bits */
    return v2;
}
