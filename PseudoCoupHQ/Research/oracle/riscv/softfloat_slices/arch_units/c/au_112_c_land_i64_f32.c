/*
 * arch-unit 112  --  c  `a && b`  lhs=int64_t rhs=float
 * symbol op_327   outcome LIFTED
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   sltu a0, zero, a0                  integer  operator:<
 *   fmv.w.x fa5, zero                  float    bit-manipulation
 *   feq.s a1, fa0, fa5                 float    emulation:f32_eq_rm0
 *   xori a1, a1, 0x1                   integer  operator:^
 *   c.and a0, a1                       integer  operator:&
 *   c.jr ra                            integer  return
 *
 * answer: int, 64 bits.  parameters are operand bit patterns.
 */
#include "arch_units.h"

uint64_t au_112_c_land_i64_f32(uint64_t p0, uint64_t p1)
{
    /* a0: operand `a` (int64_t) arrives in a0 */
    const uint64_t v1 = p0;
    /* fa0: operand `b` (float) arrives in fa0 */
    const uint64_t v2 = ((p1) & UINT64_C(0xffffffff));
    const uint64_t v3 = au_b2u((UINT64_C(0x0)) < (v1));
    const uint64_t v4 = ((UINT64_C(0x0)) & UINT64_C(0xffffffff));
    const uint64_t v5 = au_b2u(f32_eq_rm0(v2, v4));
    const uint64_t v6 = ((v5) ^ UINT64_C(0x1));
    const uint64_t v7 = ((v3) & (v6));
    return v7;
}
