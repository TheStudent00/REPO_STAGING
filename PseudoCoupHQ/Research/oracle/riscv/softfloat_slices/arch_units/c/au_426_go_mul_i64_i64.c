/*
 * arch-unit 426  --  go  `a * b`  lhs=int64 rhs=int64
 * symbol main.op_67   outcome LIFTED   2 arch-opcodes
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   mul a0, a0, a1                       integer    operator:*
 *   jalr zero, 0x0(ra)                   integer    return
 *
 * answer: int64, 64 bits.  parameters are operand bit patterns.
 */
#include "arch_units_int.h"

uint64_t au_426_go_mul_i64_i64(uint64_t p0, uint64_t p1)
{
    /* a0: operand `a` (int64) arrives in a0 */
    const uint64_t v1 = p0;
    /* a1: operand `b` (int64) arrives in a1 */
    const uint64_t v2 = p1;
    const uint64_t v3 = au_mul(v1, v2);
    /* the answer is int64, 64 bits */
    return v3;
}
