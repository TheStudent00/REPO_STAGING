// arch-unit 415  --  go  `-a`  lhs=int64 rhs=None
// symbol main.op_7   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sub a0, zero, a0                     integer    operator:-
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: int64, 64 bits.  parameters are operand bit patterns.
#include "arch_units_int.hpp"

namespace archunits {

uint64_t au_415_go_neg_i64(uint64_t p0)
{
    /* a0: operand `a` (int64) arrives in a0 */
    const uint64_t v1 = p0;
    const uint64_t v2 = au_sub(UINT64_C(0x0), v1);
    /* the answer is int64, 64 bits */
    return v2;
}

}  // namespace archunits
