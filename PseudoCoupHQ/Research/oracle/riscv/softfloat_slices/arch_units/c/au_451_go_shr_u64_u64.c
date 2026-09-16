/*
 * arch-unit 451  --  go  `a >> b`  lhs=uint64 rhs=uint64
 * symbol main.op_218   outcome LIFTED   5 arch-opcodes
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   srl t0, a0, a1                       integer    operator:>> unsigned (count masked to 6 bits)
 *   sltiu t1, a1, 0x40                   integer    operator:< unsigned
 *   sub t1, zero, t1                     integer    operator:-
 *   and a0, t0, t1                       integer    operator:&
 *   jalr zero, 0x0(ra)                   integer    return
 *
 * answer: uint64, 64 bits.  parameters are operand bit patterns.
 */
#include "arch_units_int.h"

uint64_t au_451_go_shr_u64_u64(uint64_t p0, uint64_t p1)
{
    /* a0: operand `a` (uint64) arrives in a0 */
    const uint64_t v1 = p0;
    /* a1: operand `b` (uint64) arrives in a1 */
    const uint64_t v2 = p1;
    const uint64_t v3 = au_srl(v1, v2);
    const uint64_t v4 = au_sltu(v2, UINT64_C(0x40));
    const uint64_t v5 = au_sub(UINT64_C(0x0), v4);
    const uint64_t v6 = au_and(v3, v5);
    /* the answer is uint64, 64 bits */
    return v6;
}
