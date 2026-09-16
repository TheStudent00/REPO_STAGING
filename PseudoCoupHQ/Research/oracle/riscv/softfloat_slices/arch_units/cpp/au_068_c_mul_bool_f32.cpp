// arch-unit 68  --  c  `a * b`  lhs=bool rhs=float
// symbol op_207   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.s.wu fa5, a0, dyn             float    emulation:ui32_to_f32_rm0
//   fmul.s fa0, fa0, fa5, dyn          float    emulation:f32_mul_rm0
//   c.jr ra                            integer  return
//
// answer: f32, 32 bits.  parameters are operand bit patterns.
#include "arch_units.hpp"

namespace archunits {

uint64_t au_068_c_mul_bool_f32(uint64_t p0, uint64_t p1)
{
    /* a0: operand `a` (bool) zero-extended */
    const uint64_t v1 = ((p0) & UINT64_C(0x1));
    /* fa0: operand `b` (float) arrives in fa0 */
    const uint64_t v2 = ((p1) & UINT64_C(0xffffffff));
    const uint64_t v3 = sfemul::ui32_to_f32_rm0((uint32_t)(v1));
    const uint64_t v4 = sfemul::f32_mul_rm0(v2, v3);
    return ((v4) & UINT64_C(0xffffffff));
}

}  // namespace archunits
