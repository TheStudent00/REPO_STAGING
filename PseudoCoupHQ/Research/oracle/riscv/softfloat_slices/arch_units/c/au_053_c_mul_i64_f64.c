/*
 * arch-unit 53  --  c  `a * b`  lhs=int64_t rhs=double
 * symbol op_184   outcome LIFTED
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   fcvt.d.l fa5, a0, dyn              float    emulation:i64_to_f64_rm0
 *   fmul.d fa0, fa0, fa5, dyn          float    emulation:f64_mul_rm0
 *   c.jr ra                            integer  return
 *
 * answer: f64, 64 bits.  parameters are operand bit patterns.
 */
#include "arch_units.h"

uint64_t au_053_c_mul_i64_f64(uint64_t p0, uint64_t p1)
{
    /* a0: operand `a` (int64_t) arrives in a0 */
    const uint64_t v1 = p0;
    /* fa0: operand `b` (double) arrives in fa0 */
    const uint64_t v2 = p1;
    const uint64_t v3 = i64_to_f64_rm0(v1);
    const uint64_t v4 = f64_mul_rm0(v2, v3);
    return v4;
}
