// arch-unit 181  --  c  `-a`  lhs=bool rhs=None
// symbol op_17   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sub a0, zero, a0                     integer    operator:-
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
#include "arch_units_int.hpp"

namespace archunits {

uint64_t au_181_c_neg_bool(uint64_t p0)
{
    /* a0: operand `a` (bool) zero-extended to XLEN */
    const uint64_t v1 = ((p0) & UINT64_C(0x1));
    const uint64_t v2 = au_sub(UINT64_C(0x0), v1);
    /* the answer is int32_t, 32 bits */
    return ((v2) & UINT64_C(0xffffffff));
}

}  // namespace archunits
