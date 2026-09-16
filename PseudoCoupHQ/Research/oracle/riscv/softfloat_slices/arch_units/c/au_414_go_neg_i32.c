/*
 * arch-unit 414  --  go  `-a`  lhs=int32 rhs=None
 * symbol main.op_6   outcome LIFTED   2 arch-opcodes
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   sub a0, zero, a0                     integer    operator:-
 *   jalr zero, 0x0(ra)                   integer    return
 *
 * answer: int32, 32 bits.  parameters are operand bit patterns.
 */
#include "arch_units_int.h"

uint64_t au_414_go_neg_i32(uint64_t p0)
{
    /* a0: operand `a` (int32) sign-extended to XLEN, as the ABI presents it */
    const uint64_t v1 = au_sext32(p0);
    const uint64_t v2 = au_sub(UINT64_C(0x0), v1);
    /* the answer is int32, 32 bits */
    return ((v2) & UINT64_C(0xffffffff));
}
