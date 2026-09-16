// arch-unit 135  --  c  `a == b`  lhs=uint64_t rhs=double
// symbol op_478   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.d.lu fa5, a0, dyn             float    emulation:ui64_to_f64_rm0
//   feq.d a0, fa0, fa5                 float    emulation:f64_eq_rm0
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
#include "arch_units.hpp"

namespace archunits {

uint64_t au_135_c_eq_u64_f64(uint64_t p0, uint64_t p1)
{
    /* a0: operand `a` (uint64_t) arrives in a0 */
    const uint64_t v1 = p0;
    /* fa0: operand `b` (double) arrives in fa0 */
    const uint64_t v2 = p1;
    const uint64_t v3 = sfemul::ui64_to_f64_rm0(v1);
    const uint64_t v4 = au_b2u(sfemul::f64_eq_rm0(v2, v3));
    return v4;
}

}  // namespace archunits
