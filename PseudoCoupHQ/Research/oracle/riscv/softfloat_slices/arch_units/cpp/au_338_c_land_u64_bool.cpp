// arch-unit 338  --  c  `a && b`  lhs=uint64_t rhs=bool
// symbol op_335   outcome LIFTED   3 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sltu a0, zero, a0                    integer    operator:< unsigned
//   c.and a0, a1                         integer    operator:&
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
#include "arch_units_int.hpp"

namespace archunits {

uint64_t au_338_c_land_u64_bool(uint64_t p0, uint64_t p1)
{
    /* a0: operand `a` (uint64_t) arrives in a0 */
    const uint64_t v1 = p0;
    /* a1: operand `b` (bool) zero-extended to XLEN */
    const uint64_t v2 = ((p1) & UINT64_C(0x1));
    const uint64_t v3 = au_sltu(UINT64_C(0x0), v1);
    const uint64_t v4 = au_and(v3, v2);
    /* the answer is int32_t, 32 bits */
    return ((v4) & UINT64_C(0xffffffff));
}

}  // namespace archunits
