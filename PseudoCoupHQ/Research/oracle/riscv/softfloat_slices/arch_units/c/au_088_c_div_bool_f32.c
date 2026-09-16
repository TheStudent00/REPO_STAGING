/*
 * arch-unit 88  --  c  `a / b`  lhs=bool rhs=float
 * symbol op_243   outcome LIFTED
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   fcvt.s.wu fa5, a0, dyn             float    emulation:ui32_to_f32_rm0
 *   fdiv.s fa0, fa5, fa0, dyn          float    emulation:f32_div_rm0
 *   c.jr ra                            integer  return
 *
 * answer: f32, 32 bits.  parameters are operand bit patterns.
 */
#include "arch_units.h"

uint64_t au_088_c_div_bool_f32(uint64_t p0, uint64_t p1)
{
    /* a0: operand `a` (bool) zero-extended */
    const uint64_t v1 = ((p0) & UINT64_C(0x1));
    /* fa0: operand `b` (float) arrives in fa0 */
    const uint64_t v2 = ((p1) & UINT64_C(0xffffffff));
    const uint64_t v3 = ui32_to_f32_rm0((uint32_t)(v1));
    const uint64_t v4 = f32_div_rm0(v3, v2);
    return ((v4) & UINT64_C(0xffffffff));
}
