// arch-unit 146  --  c  `a == b`  lhs=double rhs=double
// symbol op_490   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   feq.d a0, fa0, fa1                 float    emulation:f64_eq_rm0
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
#include "arch_units.hpp"

namespace archunits {

uint64_t au_146_c_eq_f64_f64(uint64_t p0, uint64_t p1)
{
    /* fa0: operand `a` (double) arrives in fa0 */
    const uint64_t v1 = p0;
    /* fa1: operand `b` (double) arrives in fa1 */
    const uint64_t v2 = p1;
    const uint64_t v3 = au_b2u(sfemul::f64_eq_rm0(v1, v2));
    return v3;
}

}  // namespace archunits
