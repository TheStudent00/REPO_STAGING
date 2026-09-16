// arch-unit 202  --  c  `sizeof a`  lhs=bool rhs=None
// symbol op_53   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.li a0, 0x1                         integer    constant
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
#include "arch_units_int.hpp"

namespace archunits {

uint64_t au_202_c_sizeof_bool(uint64_t p0)
{
    /* a0: operand `a` (bool) zero-extended to XLEN */
    const uint64_t v1 = ((p0) & UINT64_C(0x1));
    const uint64_t v2 = UINT64_C(0x1);
    /* the answer is uint64_t, 64 bits */
    return v2;
}

}  // namespace archunits
