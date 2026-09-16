// arch-unit 177  --  c  `!a`  lhs=bool rhs=None
// symbol op_5   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   xori a0, a0, 0x1                     integer    operator:^
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
#include "arch_units_int.hpp"

namespace archunits {

uint64_t au_177_c_not_bool(uint64_t p0)
{
    /* a0: operand `a` (bool) zero-extended to XLEN */
    const uint64_t v1 = ((p0) & UINT64_C(0x1));
    const uint64_t v2 = au_xor(v1, UINT64_C(0x1));
    /* the answer is int32_t, 32 bits */
    return ((v2) & UINT64_C(0xffffffff));
}

}  // namespace archunits
