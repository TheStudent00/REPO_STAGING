// arch-unit 141  --  c  `a == b`  lhs=float rhs=bool
// symbol op_485   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.s.wu fa5, a0, dyn             float    emulation:ui32_to_f32_rm0
//   feq.s a0, fa0, fa5                 float    emulation:f32_eq_rm0
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
#include "arch_units.hpp"

namespace archunits {

uint64_t au_141_c_eq_f32_bool(uint64_t p0, uint64_t p1)
{
    /* fa0: operand `a` (float) arrives in fa0 */
    const uint64_t v1 = ((p0) & UINT64_C(0xffffffff));
    /* a0: operand `b` (bool) zero-extended */
    const uint64_t v2 = ((p1) & UINT64_C(0x1));
    const uint64_t v3 = sfemul::ui32_to_f32_rm0((uint32_t)(v2));
    const uint64_t v4 = au_b2u(sfemul::f32_eq_rm0(v1, v3));
    return v4;
}

}  // namespace archunits
