// arch-unit 137  --  c  `a == b`  lhs=float rhs=int64_t
// symbol op_481   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.s.l fa5, a0, dyn              float    emulation:i64_to_f32_rm0
//   feq.s a0, fa0, fa5                 float    emulation:f32_eq_rm0
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
#include "arch_units.hpp"

namespace archunits {

uint64_t au_137_c_eq_f32_i64(uint64_t p0, uint64_t p1)
{
    /* fa0: operand `a` (float) arrives in fa0 */
    const uint64_t v1 = ((p0) & UINT64_C(0xffffffff));
    /* a0: operand `b` (int64_t) arrives in a0 */
    const uint64_t v2 = p1;
    const uint64_t v3 = sfemul::i64_to_f32_rm0(v2);
    const uint64_t v4 = au_b2u(sfemul::f32_eq_rm0(v1, v3));
    return v4;
}

}  // namespace archunits
