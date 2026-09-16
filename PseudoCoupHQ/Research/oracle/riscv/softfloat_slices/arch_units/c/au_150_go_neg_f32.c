/*
 * arch-unit 150  --  go  `-a`  lhs=float32 rhs=None
 * symbol main.op_9   outcome WALK_REFUSED
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   fsgnjn.s fa0, fa0, fa0             float    bit-manipulation
 *   jalr zero, 0x0(ra)                 integer  return
 *
 * answer: f32, 32 bits.  parameters are operand bit patterns.
 */
#include "arch_units.h"

uint64_t au_150_go_neg_f32(uint64_t p0)
{
    /* fa0: operand `a` (float32) arrives in fa0 */
    const uint64_t v1 = ((p0) & UINT64_C(0xffffffff));
    const uint64_t v2 = (((v1) & UINT64_C(0x7fffffff)) | ((~(v1)) & UINT64_C(0x80000000)));
    return ((v2) & UINT64_C(0xffffffff));
}
