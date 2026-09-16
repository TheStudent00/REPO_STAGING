/*
 * arch-unit 419  --  go  `^a`  lhs=int64 rhs=None
 * symbol main.op_19   outcome LIFTED   2 arch-opcodes
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   xori a0, a0, -0x1                    integer    operator:^
 *   jalr zero, 0x0(ra)                   integer    return
 *
 * answer: int64, 64 bits.  parameters are operand bit patterns.
 */
#include "arch_units_int.h"

uint64_t au_419_go_cmpl_i64(uint64_t p0)
{
    /* a0: operand `a` (int64) arrives in a0 */
    const uint64_t v1 = p0;
    const uint64_t v2 = au_xor(v1, UINT64_C(0xffffffffffffffff));
    /* the answer is int64, 64 bits */
    return v2;
}
