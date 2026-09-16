/*
 * arch-unit 14  --  c  `a + b`  lhs=uint64_t rhs=float
 * symbol op_117   outcome LIFTED
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   fcvt.s.lu fa5, a0, dyn             float    emulation:ui64_to_f32_rm0
 *   fadd.s fa0, fa0, fa5, dyn          float    emulation:f32_add_rm0
 *   c.jr ra                            integer  return
 *
 * answer: f32, 32 bits.  parameters are operand bit patterns.
 */
#include "arch_units.h"

uint64_t au_014_c_add_u64_f32(uint64_t p0, uint64_t p1)
{
    /* a0: operand `a` (uint64_t) arrives in a0 */
    const uint64_t v1 = p0;
    /* fa0: operand `b` (float) arrives in fa0 */
    const uint64_t v2 = ((p1) & UINT64_C(0xffffffff));
    const uint64_t v3 = ui64_to_f32_rm0(v1);
    const uint64_t v4 = f32_add_rm0(v2, v3);
    return ((v4) & UINT64_C(0xffffffff));
}
