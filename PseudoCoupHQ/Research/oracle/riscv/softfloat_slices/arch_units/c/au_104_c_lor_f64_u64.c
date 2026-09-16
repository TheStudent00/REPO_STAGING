/*
 * arch-unit 104  --  c  `a || b`  lhs=double rhs=uint64_t
 * symbol op_308   outcome LIFTED
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   fmv.d.x fa5, zero                  float    bit-manipulation
 *   feq.d a1, fa0, fa5                 float    emulation:f64_eq_rm0
 *   xori a1, a1, 0x1                   integer  operator:^
 *   sltu a0, zero, a0                  integer  operator:<
 *   c.or a0, a1                        integer  operator:|
 *   c.jr ra                            integer  return
 *
 * answer: int, 64 bits.  parameters are operand bit patterns.
 */
#include "arch_units.h"

uint64_t au_104_c_lor_f64_u64(uint64_t p0, uint64_t p1)
{
    /* fa0: operand `a` (double) arrives in fa0 */
    const uint64_t v1 = p0;
    /* a0: operand `b` (uint64_t) arrives in a0 */
    const uint64_t v2 = p1;
    const uint64_t v3 = UINT64_C(0x0);
    const uint64_t v4 = au_b2u(f64_eq_rm0(v1, v3));
    const uint64_t v5 = ((v4) ^ UINT64_C(0x1));
    const uint64_t v6 = au_b2u((UINT64_C(0x0)) < (v2));
    const uint64_t v7 = ((v6) | (v5));
    return v7;
}
