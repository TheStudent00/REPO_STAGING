// arch-unit 184  --  c  `+a`  lhs=uint64_t rhs=None
// symbol op_20   outcome LIFTED   1 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
#include "arch_units_int.hpp"

namespace archunits {

uint64_t au_184_c_pos_u64(uint64_t p0)
{
    /* a0: operand `a` (uint64_t) arrives in a0 */
    const uint64_t v1 = p0;
    /* the answer is uint64_t, 64 bits */
    return v1;
}

}  // namespace archunits
