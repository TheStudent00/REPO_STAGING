// arch-unit 482  --  go  `a <= b`  lhs=int64 rhs=int64
// symbol main.op_571   outcome LIFTED   3 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   slt t0, a1, a0                       integer    operator:< signed
//   sltiu a0, t0, 0x1                    integer    operator:< unsigned
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: bool, 1 bits.  parameters are operand bit patterns.
#include "arch_units_int.hpp"

namespace archunits {

uint64_t au_482_go_le_i64_i64(uint64_t p0, uint64_t p1)
{
    /* a0: operand `a` (int64) arrives in a0 */
    const uint64_t v1 = p0;
    /* a1: operand `b` (int64) arrives in a1 */
    const uint64_t v2 = p1;
    const uint64_t v3 = au_slt(v2, v1);
    const uint64_t v4 = au_sltu(v3, UINT64_C(0x1));
    /* the answer is bool, 1 bits */
    return ((v4) & UINT64_C(0x1));
}

}  // namespace archunits
