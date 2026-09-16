// arch-unit 108  --  c  `a || b`  lhs=bool rhs=float
// symbol op_315   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fmv.w.x fa5, zero                  float    bit-manipulation
//   feq.s a1, fa0, fa5                 float    emulation:f32_eq_rm0
//   xori a1, a1, 0x1                   integer  operator:^
//   c.or a0, a1                        integer  operator:|
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
#include "arch_units.hpp"

namespace archunits {

uint64_t au_108_c_lor_bool_f32(uint64_t p0, uint64_t p1)
{
    /* a0: operand `a` (bool) zero-extended */
    const uint64_t v1 = ((p0) & UINT64_C(0x1));
    /* fa0: operand `b` (float) arrives in fa0 */
    const uint64_t v2 = ((p1) & UINT64_C(0xffffffff));
    const uint64_t v3 = ((UINT64_C(0x0)) & UINT64_C(0xffffffff));
    const uint64_t v4 = au_b2u(sfemul::f32_eq_rm0(v2, v3));
    const uint64_t v5 = ((v4) ^ UINT64_C(0x1));
    const uint64_t v6 = ((v1) | (v5));
    return v6;
}

}  // namespace archunits
