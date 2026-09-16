// arch-unit 200  --  c  `sizeof a`  lhs=float rhs=None
// symbol op_51   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.li a0, 0x4                         integer    constant
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
#include "arch_units_int.hpp"

namespace archunits {

uint64_t au_200_c_sizeof_f32(uint64_t p0)
{
    /* fa0: operand `a` (float) arrives in fa0 as a bit pattern */
    const uint64_t v1 = ((p0) & UINT64_C(0xffffffff));
    const uint64_t v2 = UINT64_C(0x4);
    /* the answer is uint64_t, 64 bits */
    return v2;
}

}  // namespace archunits
