// arch-unit 0  --  c  `!a`  lhs=float rhs=None
// symbol op_3   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fmv.w.x fa5, zero                  float    bit-manipulation
//   feq.s a0, fa0, fa5                 float    emulation:f32_eq_rm0
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
#include "arch_units.hpp"

namespace archunits {

uint64_t au_000_c_not_f32(uint64_t p0)
{
    /* fa0: operand `a` (float) arrives in fa0 */
    const uint64_t v1 = ((p0) & UINT64_C(0xffffffff));
    const uint64_t v2 = ((UINT64_C(0x0)) & UINT64_C(0xffffffff));
    const uint64_t v3 = au_b2u(sfemul::f32_eq_rm0(v1, v2));
    return v3;
}

}  // namespace archunits
