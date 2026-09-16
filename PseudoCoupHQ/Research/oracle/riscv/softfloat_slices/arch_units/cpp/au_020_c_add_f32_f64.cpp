// arch-unit 20  --  c  `a + b`  lhs=float rhs=double
// symbol op_124   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.d.s fa5, fa0                  float    emulation:f32_to_f64_rm0
//   fadd.d fa0, fa1, fa5, dyn          float    emulation:f64_add_rm0
//   c.jr ra                            integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
#include "arch_units.hpp"

namespace archunits {

uint64_t au_020_c_add_f32_f64(uint64_t p0, uint64_t p1)
{
    /* fa0: operand `a` (float) arrives in fa0 */
    const uint64_t v1 = ((p0) & UINT64_C(0xffffffff));
    /* fa1: operand `b` (double) arrives in fa1 */
    const uint64_t v2 = p1;
    const uint64_t v3 = sfemul::f32_to_f64_rm0(v1);
    const uint64_t v4 = sfemul::f64_add_rm0(v2, v3);
    return v4;
}

}  // namespace archunits
