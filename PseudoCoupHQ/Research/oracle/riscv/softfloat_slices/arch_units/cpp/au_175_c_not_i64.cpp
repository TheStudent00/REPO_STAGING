// arch-unit 175  --  c  `!a`  lhs=int64_t rhs=None
// symbol op_1   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sltiu a0, a0, 0x1                    integer    operator:< unsigned
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
#include "arch_units_int.hpp"

namespace archunits {

uint64_t au_175_c_not_i64(uint64_t p0)
{
    /* a0: operand `a` (int64_t) arrives in a0 */
    const uint64_t v1 = p0;
    const uint64_t v2 = au_sltu(v1, UINT64_C(0x1));
    /* the answer is int32_t, 32 bits */
    return ((v2) & UINT64_C(0xffffffff));
}

}  // namespace archunits
