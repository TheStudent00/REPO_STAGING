/*
 * arch-unit 3  --  c  `-a`  lhs=double rhs=None
 * symbol op_16   outcome WALK_REFUSED
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   fsgnjn.d fa0, fa0, fa0             float    bit-manipulation
 *   c.jr ra                            integer  return
 *
 * answer: f64, 64 bits.  parameters are operand bit patterns.
 */
#include "arch_units.h"

uint64_t au_003_c_neg_f64(uint64_t p0)
{
    /* fa0: operand `a` (double) arrives in fa0 */
    const uint64_t v1 = p0;
    const uint64_t v2 = (((v1) & UINT64_C(0x7fffffffffffffff)) | ((~(v1)) & UINT64_C(0x8000000000000000)));
    return v2;
}
