// arch-unit 106  --  c  `a || b`  lhs=double rhs=double
// symbol op_310   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fmv.d.x fa5, zero                  float    bit-manipulation
//   feq.d a0, fa0, fa5                 float    emulation:f64_eq_rm0
//   feq.d a1, fa1, fa5                 float    emulation:f64_eq_rm0
//   c.and a0, a1                       integer  operator:&
//   xori a0, a0, 0x1                   integer  operator:^
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
#include "arch_units.hpp"

namespace archunits {

uint64_t au_106_c_lor_f64_f64(uint64_t p0, uint64_t p1)
{
    /* fa0: operand `a` (double) arrives in fa0 */
    const uint64_t v1 = p0;
    /* fa1: operand `b` (double) arrives in fa1 */
    const uint64_t v2 = p1;
    const uint64_t v3 = UINT64_C(0x0);
    const uint64_t v4 = au_b2u(sfemul::f64_eq_rm0(v1, v3));
    const uint64_t v5 = au_b2u(sfemul::f64_eq_rm0(v2, v3));
    const uint64_t v6 = ((v4) & (v5));
    const uint64_t v7 = ((v6) ^ UINT64_C(0x1));
    return v7;
}

}  // namespace archunits
