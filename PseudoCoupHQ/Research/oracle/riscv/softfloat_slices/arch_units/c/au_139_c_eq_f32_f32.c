/*
 * arch-unit 139  --  c  `a == b`  lhs=float rhs=float
 * symbol op_483   outcome LIFTED
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   feq.s a0, fa0, fa1                 float    emulation:f32_eq_rm0
 *   c.jr ra                            integer  return
 *
 * answer: int, 64 bits.  parameters are operand bit patterns.
 */
#include "arch_units.h"

uint64_t au_139_c_eq_f32_f32(uint64_t p0, uint64_t p1)
{
    /* fa0: operand `a` (float) arrives in fa0 */
    const uint64_t v1 = ((p0) & UINT64_C(0xffffffff));
    /* fa1: operand `b` (float) arrives in fa1 */
    const uint64_t v2 = ((p1) & UINT64_C(0xffffffff));
    const uint64_t v3 = au_b2u(f32_eq_rm0(v1, v2));
    return v3;
}
