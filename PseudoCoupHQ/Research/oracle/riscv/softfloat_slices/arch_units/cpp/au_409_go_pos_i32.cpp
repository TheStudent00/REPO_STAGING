// arch-unit 409  --  go  `+a`  lhs=int32 rhs=None
// symbol main.op_0   outcome LIFTED   1 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: int32, 32 bits.  parameters are operand bit patterns.
#include "arch_units_int.hpp"

namespace archunits {

uint64_t au_409_go_pos_i32(uint64_t p0)
{
    /* a0: operand `a` (int32) sign-extended to XLEN, as the ABI presents it */
    const uint64_t v1 = au_sext32(p0);
    /* the answer is int32, 32 bits */
    return ((v1) & UINT64_C(0xffffffff));
}

}  // namespace archunits
