// arch-unit 72  --  c  `a / b`  lhs=int64_t rhs=float
// symbol op_219   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.s.l fa5, a0, dyn              float    emulation:i64_to_f32_rm0
//   fdiv.s fa0, fa5, fa0, dyn          float    emulation:f32_div_rm0
//   c.jr ra                            integer  return
//
// answer: f32, 32 bits.  parameters are operand bit patterns.
#include "arch_units.hpp"

namespace archunits {

uint64_t au_072_c_div_i64_f32(uint64_t p0, uint64_t p1)
{
    /* a0: operand `a` (int64_t) arrives in a0 */
    const uint64_t v1 = p0;
    /* fa0: operand `b` (float) arrives in fa0 */
    const uint64_t v2 = ((p1) & UINT64_C(0xffffffff));
    const uint64_t v3 = sfemul::i64_to_f32_rm0(v1);
    const uint64_t v4 = sfemul::f32_div_rm0(v3, v2);
    return ((v4) & UINT64_C(0xffffffff));
}

}  // namespace archunits
