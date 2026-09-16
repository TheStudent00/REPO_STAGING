// arch-unit 320  --  c  `a || b`  lhs=uint64_t rhs=int64_t
// symbol op_295   outcome LIFTED   3 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.or a0, a1                          integer    operator:|
//   sltu a0, zero, a0                    integer    operator:< unsigned
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
#include "arch_units_int.hpp"

namespace archunits {

uint64_t au_320_c_lor_u64_i64(uint64_t p0, uint64_t p1)
{
    /* a0: operand `a` (uint64_t) arrives in a0 */
    const uint64_t v1 = p0;
    /* a1: operand `b` (int64_t) arrives in a1 */
    const uint64_t v2 = p1;
    const uint64_t v3 = au_or(v1, v2);
    const uint64_t v4 = au_sltu(UINT64_C(0x0), v3);
    /* the answer is int32_t, 32 bits */
    return ((v4) & UINT64_C(0xffffffff));
}

}  // namespace archunits
