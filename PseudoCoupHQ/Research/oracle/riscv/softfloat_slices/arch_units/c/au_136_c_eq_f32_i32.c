/*
 * arch-unit 136  --  c  `a == b`  lhs=float rhs=int32_t
 * symbol op_480   outcome LIFTED
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   fcvt.s.w fa5, a0, dyn              float    emulation:i32_to_f32_rm0
 *   feq.s a0, fa0, fa5                 float    emulation:f32_eq_rm0
 *   c.jr ra                            integer  return
 *
 * answer: int, 64 bits.  parameters are operand bit patterns.
 */
#include "arch_units.h"

uint64_t au_136_c_eq_f32_i32(uint64_t p0, uint64_t p1)
{
    /* fa0: operand `a` (float) arrives in fa0 */
    const uint64_t v1 = ((p0) & UINT64_C(0xffffffff));
    /* a0: operand `b` (int32_t) sign-extended to XLEN */
    const uint64_t v2 = (uint64_t)(int64_t)(int32_t)(uint32_t)(p1);
    const uint64_t v3 = i32_to_f32_rm0((uint32_t)(v2));
    const uint64_t v4 = au_b2u(f32_eq_rm0(v1, v3));
    return v4;
}
