// arch-unit 475  --  go  `a != b`  lhs=int64 rhs=int64
// symbol main.op_499   outcome LIFTED   3 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sub t0, a0, a1                       integer    operator:-
//   sltu a0, zero, t0                    integer    operator:< unsigned
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: bool, 1 bits.  parameters are operand bit patterns.
#include "arch_units_int.hpp"

namespace archunits {

uint64_t au_475_go_ne_i64_i64(uint64_t p0, uint64_t p1)
{
    /* a0: operand `a` (int64) arrives in a0 */
    const uint64_t v1 = p0;
    /* a1: operand `b` (int64) arrives in a1 */
    const uint64_t v2 = p1;
    const uint64_t v3 = au_sub(v1, v2);
    const uint64_t v4 = au_sltu(UINT64_C(0x0), v3);
    /* the answer is bool, 1 bits */
    return ((v4) & UINT64_C(0x1));
}

}  // namespace archunits
