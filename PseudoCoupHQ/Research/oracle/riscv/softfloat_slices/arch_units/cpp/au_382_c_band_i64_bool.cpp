// arch-unit 382  --  c  `a & b`  lhs=int64_t rhs=bool
// symbol op_437   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.and a0, a1                         integer    operator:&
//   c.jr ra                              integer    return
//
// answer: int64_t, 64 bits.  parameters are operand bit patterns.
#include "arch_units_int.hpp"

namespace archunits {

uint64_t au_382_c_band_i64_bool(uint64_t p0, uint64_t p1)
{
    /* a0: operand `a` (int64_t) arrives in a0 */
    const uint64_t v1 = p0;
    /* a1: operand `b` (bool) zero-extended to XLEN */
    const uint64_t v2 = ((p1) & UINT64_C(0x1));
    const uint64_t v3 = au_and(v1, v2);
    /* the answer is int64_t, 64 bits */
    return v3;
}

}  // namespace archunits
