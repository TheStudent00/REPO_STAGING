// arch-unit 230  --  c  `a++`  lhs=float rhs=None
// symbol op_93   outcome LIFTED   1 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.jr ra                              integer    return
//
// answer: float, 32 bits.  parameters are operand bit patterns.
#include "arch_units_int.hpp"

namespace archunits {

uint64_t au_230_c_postinc_f32(uint64_t p0)
{
    /* fa0: operand `a` (float) arrives in fa0 as a bit pattern */
    const uint64_t v1 = ((p0) & UINT64_C(0xffffffff));
    /* the answer is float, 32 bits */
    return ((v1) & UINT64_C(0xffffffff));
}

}  // namespace archunits
