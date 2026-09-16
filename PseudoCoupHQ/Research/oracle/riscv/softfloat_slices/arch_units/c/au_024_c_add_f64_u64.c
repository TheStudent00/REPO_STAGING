/*
 * arch-unit 24  --  c  `a + b`  lhs=double rhs=uint64_t
 * symbol op_128   outcome LIFTED
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   fcvt.d.lu fa5, a0, dyn             float    emulation:ui64_to_f64_rm0
 *   fadd.d fa0, fa0, fa5, dyn          float    emulation:f64_add_rm0
 *   c.jr ra                            integer  return
 *
 * answer: f64, 64 bits.  parameters are operand bit patterns.
 */
#include "arch_units.h"

uint64_t au_024_c_add_f64_u64(uint64_t p0, uint64_t p1)
{
    /* fa0: operand `a` (double) arrives in fa0 */
    const uint64_t v1 = p0;
    /* a0: operand `b` (uint64_t) arrives in a0 */
    const uint64_t v2 = p1;
    const uint64_t v3 = ui64_to_f64_rm0(v2);
    const uint64_t v4 = f64_add_rm0(v1, v3);
    return v4;
}
