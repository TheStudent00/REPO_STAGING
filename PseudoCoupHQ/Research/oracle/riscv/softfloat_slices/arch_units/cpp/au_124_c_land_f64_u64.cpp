// arch-unit 124  --  c  `a && b`  lhs=double rhs=uint64_t
// symbol op_344   outcome WALK_REFUSED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fmv.d.x fa5, zero                  float    bit-manipulation
//   feq.d a1, fa0, fa5                 float    emulation:f64_eq_rm0
//   sltu a0, zero, a0                  integer  operator:<
//   andn a0, a0, a1                    integer  operator:& ~
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
#include "arch_units.hpp"

namespace archunits {

uint64_t au_124_c_land_f64_u64(uint64_t p0, uint64_t p1)
{
    /* fa0: operand `a` (double) arrives in fa0 */
    const uint64_t v1 = p0;
    /* a0: operand `b` (uint64_t) arrives in a0 */
    const uint64_t v2 = p1;
    const uint64_t v3 = UINT64_C(0x0);
    const uint64_t v4 = au_b2u(sfemul::f64_eq_rm0(v1, v3));
    const uint64_t v5 = au_b2u((UINT64_C(0x0)) < (v2));
    const uint64_t v6 = ((v5) & (~(v4)));
    return v6;
}

}  // namespace archunits
