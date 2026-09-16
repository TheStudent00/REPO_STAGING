/*
 * arch-unit 38  --  c  `a - b`  lhs=float rhs=uint64_t
 * symbol op_158   outcome LIFTED
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   fcvt.s.lu fa5, a0, dyn             float    emulation:ui64_to_f32_rm0
 *   fsub.s fa0, fa0, fa5, dyn          float    emulation:f32_sub_rm0
 *   c.jr ra                            integer  return
 *
 * answer: f32, 32 bits.  parameters are operand bit patterns.
 */
#include "arch_units.h"

uint64_t au_038_c_neg_f32_u64(uint64_t p0, uint64_t p1)
{
    /* fa0: operand `a` (float) arrives in fa0 */
    const uint64_t v1 = ((p0) & UINT64_C(0xffffffff));
    /* a0: operand `b` (uint64_t) arrives in a0 */
    const uint64_t v2 = p1;
    const uint64_t v3 = ui64_to_f32_rm0(v2);
    const uint64_t v4 = f32_sub_rm0(v1, v3);
    return ((v4) & UINT64_C(0xffffffff));
}
