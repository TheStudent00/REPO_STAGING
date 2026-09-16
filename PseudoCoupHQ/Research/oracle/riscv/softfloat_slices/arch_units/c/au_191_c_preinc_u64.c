/*
 * arch-unit 191  --  c  `++a`  lhs=uint64_t rhs=None
 * symbol op_38   outcome LIFTED   2 arch-opcodes
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   c.addi a0, 0x1                       integer    operator:+
 *   c.jr ra                              integer    return
 *
 * answer: uint64_t, 64 bits.  parameters are operand bit patterns.
 */
#include "arch_units_int.h"

uint64_t au_191_c_preinc_u64(uint64_t p0)
{
    /* a0: operand `a` (uint64_t) arrives in a0 */
    const uint64_t v1 = p0;
    const uint64_t v2 = au_add(v1, UINT64_C(0x1));
    /* the answer is uint64_t, 64 bits */
    return v2;
}
