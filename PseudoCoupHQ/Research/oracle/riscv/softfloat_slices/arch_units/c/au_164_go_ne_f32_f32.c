/*
 * arch-unit 164  --  go  `a != b`  lhs=float32 rhs=float32
 * symbol main.op_513   outcome LIFTED
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   feq.s a0, fa0, fa1                 float    emulation:f32_eq_rm0
 *   xori a0, a0, 0x1                   integer  operator:^
 *   jalr zero, 0x0(ra)                 integer  return
 *
 * answer: int, 64 bits.  parameters are operand bit patterns.
 */
#include "arch_units.h"

uint64_t au_164_go_ne_f32_f32(uint64_t p0, uint64_t p1)
{
    /* fa0: operand `a` (float32) arrives in fa0 */
    const uint64_t v1 = ((p0) & UINT64_C(0xffffffff));
    /* fa1: operand `b` (float32) arrives in fa1 */
    const uint64_t v2 = ((p1) & UINT64_C(0xffffffff));
    const uint64_t v3 = au_b2u(f32_eq_rm0(v1, v2));
    const uint64_t v4 = ((v3) ^ UINT64_C(0x1));
    return v4;
}
