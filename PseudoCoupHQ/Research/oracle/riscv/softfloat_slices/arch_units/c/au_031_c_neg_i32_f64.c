/*
 * arch-unit 31  --  c  `a - b`  lhs=int32_t rhs=double
 * symbol op_142   outcome LIFTED
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   fcvt.d.w fa5, a0                   float    emulation:i32_to_f64_rm0
 *   fsub.d fa0, fa5, fa0, dyn          float    emulation:f64_sub_rm0
 *   c.jr ra                            integer  return
 *
 * answer: f64, 64 bits.  parameters are operand bit patterns.
 */
#include "arch_units.h"

uint64_t au_031_c_neg_i32_f64(uint64_t p0, uint64_t p1)
{
    /* a0: operand `a` (int32_t) sign-extended to XLEN */
    const uint64_t v1 = (uint64_t)(int64_t)(int32_t)(uint32_t)(p0);
    /* fa0: operand `b` (double) arrives in fa0 */
    const uint64_t v2 = p1;
    const uint64_t v3 = i32_to_f64_rm0((uint32_t)(v1));
    const uint64_t v4 = f64_sub_rm0(v3, v2);
    return v4;
}
