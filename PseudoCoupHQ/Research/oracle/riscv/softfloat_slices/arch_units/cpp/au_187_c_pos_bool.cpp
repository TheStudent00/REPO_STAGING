// arch-unit 187  --  c  `+a`  lhs=bool rhs=None
// symbol op_23   outcome LIFTED   1 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
#include "arch_units_int.hpp"

namespace archunits {

uint64_t au_187_c_pos_bool(uint64_t p0)
{
    /* a0: operand `a` (bool) zero-extended to XLEN */
    const uint64_t v1 = ((p0) & UINT64_C(0x1));
    /* the answer is int32_t, 32 bits */
    return ((v1) & UINT64_C(0xffffffff));
}

}  // namespace archunits
