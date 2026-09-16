// arch-unit 417  --  go  `!a`  lhs=bool rhs=None
// symbol main.op_17   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sltiu a0, a0, 0x1                    integer    operator:< unsigned
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: bool, 1 bits.  parameters are operand bit patterns.
#include "arch_units_int.hpp"

namespace archunits {

uint64_t au_417_go_not_bool(uint64_t p0)
{
    /* a0: operand `a` (bool) zero-extended to XLEN */
    const uint64_t v1 = ((p0) & UINT64_C(0x1));
    const uint64_t v2 = au_sltu(v1, UINT64_C(0x1));
    /* the answer is bool, 1 bits */
    return ((v2) & UINT64_C(0x1));
}

}  // namespace archunits
