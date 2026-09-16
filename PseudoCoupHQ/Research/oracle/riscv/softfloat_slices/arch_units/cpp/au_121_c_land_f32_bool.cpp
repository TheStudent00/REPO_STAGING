// arch-unit 121  --  c  `a && b`  lhs=float rhs=bool
// symbol op_341   outcome WALK_REFUSED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fmv.w.x fa5, zero                  float    bit-manipulation
//   feq.s a1, fa0, fa5                 float    emulation:f32_eq_rm0
//   andn a0, a0, a1                    integer  operator:& ~
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
#include "arch_units.hpp"

namespace archunits {

uint64_t au_121_c_land_f32_bool(uint64_t p0, uint64_t p1)
{
    /* fa0: operand `a` (float) arrives in fa0 */
    const uint64_t v1 = ((p0) & UINT64_C(0xffffffff));
    /* a0: operand `b` (bool) zero-extended */
    const uint64_t v2 = ((p1) & UINT64_C(0x1));
    const uint64_t v3 = ((UINT64_C(0x0)) & UINT64_C(0xffffffff));
    const uint64_t v4 = au_b2u(sfemul::f32_eq_rm0(v1, v3));
    const uint64_t v5 = ((v2) & (~(v4)));
    return v5;
}

}  // namespace archunits
