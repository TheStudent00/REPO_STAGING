// arch-unit 157  --  go  `a / b`  lhs=float64 rhs=float64
// symbol main.op_124   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fdiv.d fa0, fa0, fa1, rne          float    emulation:f64_div_rm0
//   jalr zero, 0x0(ra)                 integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
#include "arch_units.hpp"

namespace archunits {

uint64_t au_157_go_div_f64_f64(uint64_t p0, uint64_t p1)
{
    /* fa0: operand `a` (float64) arrives in fa0 */
    const uint64_t v1 = p0;
    /* fa1: operand `b` (float64) arrives in fa1 */
    const uint64_t v2 = p1;
    const uint64_t v3 = sfemul::f64_div_rm0(v1, v2);
    return v3;
}

}  // namespace archunits
