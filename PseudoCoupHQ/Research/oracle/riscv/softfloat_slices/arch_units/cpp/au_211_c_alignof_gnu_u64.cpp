// arch-unit 211  --  c  `__alignof a`  lhs=uint64_t rhs=None
// symbol op_62   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.li a0, 0x8                         integer    constant
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
#include "arch_units_int.hpp"

namespace archunits {

uint64_t au_211_c_alignof_gnu_u64(uint64_t p0)
{
    /* a0: operand `a` (uint64_t) arrives in a0 */
    const uint64_t v1 = p0;
    const uint64_t v2 = UINT64_C(0x8);
    /* the answer is uint64_t, 64 bits */
    return v2;
}

}  // namespace archunits
