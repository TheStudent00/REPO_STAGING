// arch-unit 73  --  c  `a / b`  lhs=int64_t rhs=double
// symbol op_220   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.d.l fa5, a0, dyn              float    emulation:i64_to_f64_rm0
//   fdiv.d fa0, fa5, fa0, dyn          float    emulation:f64_div_rm0
//   c.jr ra                            integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
#include "arch_units.hpp"

namespace archunits {

uint64_t au_073_c_div_i64_f64(uint64_t p0, uint64_t p1)
{
    /* a0: operand `a` (int64_t) arrives in a0 */
    const uint64_t v1 = p0;
    /* fa0: operand `b` (double) arrives in fa0 */
    const uint64_t v2 = p1;
    const uint64_t v3 = sfemul::i64_to_f64_rm0(v1);
    const uint64_t v4 = sfemul::f64_div_rm0(v3, v2);
    return v4;
}

}  // namespace archunits
