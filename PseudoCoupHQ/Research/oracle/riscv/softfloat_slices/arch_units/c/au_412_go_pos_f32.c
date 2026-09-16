/*
 * arch-unit 412  --  go  `+a`  lhs=float32 rhs=None
 * symbol main.op_3   outcome LIFTED   1 arch-opcodes
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   jalr zero, 0x0(ra)                   integer    return
 *
 * answer: float32, 32 bits.  parameters are operand bit patterns.
 */
#include "arch_units_int.h"

uint64_t au_412_go_pos_f32(uint64_t p0)
{
    /* fa0: operand `a` (float32) arrives in fa0 as a bit pattern */
    const uint64_t v1 = ((p0) & UINT64_C(0xffffffff));
    /* the answer is float32, 32 bits */
    return ((v1) & UINT64_C(0xffffffff));
}
