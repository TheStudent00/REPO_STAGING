// arch-unit 79  --  c  `a / b`  lhs=float rhs=float
// symbol op_231   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fdiv.s fa0, fa0, fa1, dyn          float    emulation:f32_div_rm0
//   c.jr ra                            integer  return
//
// answer: f32, 32 bits.  parameters are operand bit patterns.
#include "arch_units.hpp"

namespace archunits {

uint64_t au_079_c_div_f32_f32(uint64_t p0, uint64_t p1)
{
    /* fa0: operand `a` (float) arrives in fa0 */
    const uint64_t v1 = ((p0) & UINT64_C(0xffffffff));
    /* fa1: operand `b` (float) arrives in fa1 */
    const uint64_t v2 = ((p1) & UINT64_C(0xffffffff));
    const uint64_t v3 = sfemul::f32_div_rm0(v1, v2);
    return ((v3) & UINT64_C(0xffffffff));
}

}  // namespace archunits
