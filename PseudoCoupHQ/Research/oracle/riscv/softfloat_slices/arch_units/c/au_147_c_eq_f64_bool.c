/*
 * arch-unit 147  --  c  `a == b`  lhs=double rhs=bool
 * symbol op_491   outcome LIFTED
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   fcvt.d.wu fa5, a0                  float    emulation:ui32_to_f64_rm0
 *   feq.d a0, fa0, fa5                 float    emulation:f64_eq_rm0
 *   c.jr ra                            integer  return
 *
 * answer: int, 64 bits.  parameters are operand bit patterns.
 */
#include "arch_units.h"

uint64_t au_147_c_eq_f64_bool(uint64_t p0, uint64_t p1)
{
    /* fa0: operand `a` (double) arrives in fa0 */
    const uint64_t v1 = p0;
    /* a0: operand `b` (bool) zero-extended */
    const uint64_t v2 = ((p1) & UINT64_C(0x1));
    const uint64_t v3 = ui32_to_f64_rm0((uint32_t)(v2));
    const uint64_t v4 = au_b2u(f64_eq_rm0(v1, v3));
    return v4;
}
