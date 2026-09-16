// arch-unit 2  --  c  `-a`  lhs=float rhs=None
// symbol op_15   outcome WALK_REFUSED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fsgnjn.s fa0, fa0, fa0             float    bit-manipulation
//   c.jr ra                            integer  return
//
// answer: f32, 32 bits.  parameters are operand bit patterns.
#include "arch_units.hpp"

namespace archunits {

uint64_t au_002_c_neg_f32(uint64_t p0)
{
    /* fa0: operand `a` (float) arrives in fa0 */
    const uint64_t v1 = ((p0) & UINT64_C(0xffffffff));
    const uint64_t v2 = (((v1) & UINT64_C(0x7fffffff)) | ((~(v1)) & UINT64_C(0x80000000)));
    return ((v2) & UINT64_C(0xffffffff));
}

}  // namespace archunits
