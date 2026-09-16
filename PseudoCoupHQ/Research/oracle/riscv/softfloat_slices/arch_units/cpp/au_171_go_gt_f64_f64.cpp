// arch-unit 171  --  go  `a > b`  lhs=float64 rhs=float64
// symbol main.op_628   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   flt.d a0, fa1, fa0                 float    emulation:f64_lt_rm0
//   jalr zero, 0x0(ra)                 integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
#include "arch_units.hpp"

namespace archunits {

uint64_t au_171_go_gt_f64_f64(uint64_t p0, uint64_t p1)
{
    /* fa0: operand `a` (float64) arrives in fa0 */
    const uint64_t v1 = p0;
    /* fa1: operand `b` (float64) arrives in fa1 */
    const uint64_t v2 = p1;
    const uint64_t v3 = au_b2u(sfemul::f64_lt_rm0(v2, v1));
    return v3;
}

}  // namespace archunits
