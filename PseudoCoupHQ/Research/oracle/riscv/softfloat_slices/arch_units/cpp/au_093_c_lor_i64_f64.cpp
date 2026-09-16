// arch-unit 93  --  c  `a || b`  lhs=int64_t rhs=double
// symbol op_292   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   sltu a0, zero, a0                  integer  operator:<
//   fmv.d.x fa5, zero                  float    bit-manipulation
//   feq.d a1, fa0, fa5                 float    emulation:f64_eq_rm0
//   xori a1, a1, 0x1                   integer  operator:^
//   c.or a0, a1                        integer  operator:|
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
#include "arch_units.hpp"

namespace archunits {

uint64_t au_093_c_lor_i64_f64(uint64_t p0, uint64_t p1)
{
    /* a0: operand `a` (int64_t) arrives in a0 */
    const uint64_t v1 = p0;
    /* fa0: operand `b` (double) arrives in fa0 */
    const uint64_t v2 = p1;
    const uint64_t v3 = au_b2u((UINT64_C(0x0)) < (v1));
    const uint64_t v4 = UINT64_C(0x0);
    const uint64_t v5 = au_b2u(sfemul::f64_eq_rm0(v2, v4));
    const uint64_t v6 = ((v5) ^ UINT64_C(0x1));
    const uint64_t v7 = ((v3) | (v6));
    return v7;
}

}  // namespace archunits
