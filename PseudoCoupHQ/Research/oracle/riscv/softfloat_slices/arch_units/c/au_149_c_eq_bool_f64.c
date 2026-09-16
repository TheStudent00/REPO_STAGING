/*
 * arch-unit 149  --  c  `a == b`  lhs=bool rhs=double
 * symbol op_496   outcome LIFTED
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   fcvt.d.wu fa5, a0                  float    emulation:ui32_to_f64_rm0
 *   feq.d a0, fa0, fa5                 float    emulation:f64_eq_rm0
 *   c.jr ra                            integer  return
 *
 * answer: int, 64 bits.  parameters are operand bit patterns.
 */
#include "arch_units.h"

uint64_t au_149_c_eq_bool_f64(uint64_t p0, uint64_t p1)
{
    /* a0: operand `a` (bool) zero-extended */
    const uint64_t v1 = ((p0) & UINT64_C(0x1));
    /* fa0: operand `b` (double) arrives in fa0 */
    const uint64_t v2 = p1;
    const uint64_t v3 = ui32_to_f64_rm0((uint32_t)(v1));
    const uint64_t v4 = au_b2u(f64_eq_rm0(v2, v3));
    return v4;
}
