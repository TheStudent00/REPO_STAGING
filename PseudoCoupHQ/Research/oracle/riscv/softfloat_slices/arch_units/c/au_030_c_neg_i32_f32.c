/*
 * arch-unit 30  --  c  `a - b`  lhs=int32_t rhs=float
 * symbol op_141   outcome LIFTED
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   fcvt.s.w fa5, a0, dyn              float    emulation:i32_to_f32_rm0
 *   fsub.s fa0, fa5, fa0, dyn          float    emulation:f32_sub_rm0
 *   c.jr ra                            integer  return
 *
 * answer: f32, 32 bits.  parameters are operand bit patterns.
 */
#include "arch_units.h"

uint64_t au_030_c_neg_i32_f32(uint64_t p0, uint64_t p1)
{
    /* a0: operand `a` (int32_t) sign-extended to XLEN */
    const uint64_t v1 = (uint64_t)(int64_t)(int32_t)(uint32_t)(p0);
    /* fa0: operand `b` (float) arrives in fa0 */
    const uint64_t v2 = ((p1) & UINT64_C(0xffffffff));
    const uint64_t v3 = i32_to_f32_rm0((uint32_t)(v1));
    const uint64_t v4 = f32_sub_rm0(v3, v2);
    return ((v4) & UINT64_C(0xffffffff));
}
