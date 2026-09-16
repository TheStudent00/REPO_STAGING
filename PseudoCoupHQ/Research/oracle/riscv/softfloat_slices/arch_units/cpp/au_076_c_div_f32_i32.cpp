// arch-unit 76  --  c  `a / b`  lhs=float rhs=int32_t
// symbol op_228   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.s.w fa5, a0, dyn              float    emulation:i32_to_f32_rm0
//   fdiv.s fa0, fa0, fa5, dyn          float    emulation:f32_div_rm0
//   c.jr ra                            integer  return
//
// answer: f32, 32 bits.  parameters are operand bit patterns.
#include "arch_units.hpp"

namespace archunits {

uint64_t au_076_c_div_f32_i32(uint64_t p0, uint64_t p1)
{
    /* fa0: operand `a` (float) arrives in fa0 */
    const uint64_t v1 = ((p0) & UINT64_C(0xffffffff));
    /* a0: operand `b` (int32_t) sign-extended to XLEN */
    const uint64_t v2 = (uint64_t)(int64_t)(int32_t)(uint32_t)(p1);
    const uint64_t v3 = sfemul::i32_to_f32_rm0((uint32_t)(v2));
    const uint64_t v4 = sfemul::f32_div_rm0(v1, v3);
    return ((v4) & UINT64_C(0xffffffff));
}

}  // namespace archunits
