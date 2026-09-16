// arch-unit 162  --  go  `a == b`  lhs=float32 rhs=float32
// symbol main.op_477   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   feq.s a0, fa0, fa1                 float    emulation:f32_eq_rm0
//   jalr zero, 0x0(ra)                 integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
#include "arch_units.hpp"

namespace archunits {

uint64_t au_162_go_eq_f32_f32(uint64_t p0, uint64_t p1)
{
    /* fa0: operand `a` (float32) arrives in fa0 */
    const uint64_t v1 = ((p0) & UINT64_C(0xffffffff));
    /* fa1: operand `b` (float32) arrives in fa1 */
    const uint64_t v2 = ((p1) & UINT64_C(0xffffffff));
    const uint64_t v3 = au_b2u(sfemul::f32_eq_rm0(v1, v2));
    return v3;
}

}  // namespace archunits
