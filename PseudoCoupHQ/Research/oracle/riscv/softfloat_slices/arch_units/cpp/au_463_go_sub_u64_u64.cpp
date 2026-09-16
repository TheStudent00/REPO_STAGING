// arch-unit 463  --  go  `a - b`  lhs=uint64 rhs=uint64
// symbol main.op_362   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.sub a0, a1                         integer    operator:-
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: uint64, 64 bits.  parameters are operand bit patterns.
#include "arch_units_int.hpp"

namespace archunits {

uint64_t au_463_go_sub_u64_u64(uint64_t p0, uint64_t p1)
{
    /* a0: operand `a` (uint64) arrives in a0 */
    const uint64_t v1 = p0;
    /* a1: operand `b` (uint64) arrives in a1 */
    const uint64_t v2 = p1;
    const uint64_t v3 = au_sub(v1, v2);
    /* the answer is uint64, 64 bits */
    return v3;
}

}  // namespace archunits
