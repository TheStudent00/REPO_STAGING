/*
 * arch-unit 470  --  go  `a == b`  lhs=int32 rhs=int32
 * symbol main.op_456   outcome LIFTED   5 arch-opcodes
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   addiw t0, a0, 0x0                    integer    operator:+ then sign-extend the low 32 bits
 *   addiw t1, a1, 0x0                    integer    operator:+ then sign-extend the low 32 bits
 *   sub t0, t0, t1                       integer    operator:-
 *   sltiu a0, t0, 0x1                    integer    operator:< unsigned
 *   jalr zero, 0x0(ra)                   integer    return
 *
 * answer: bool, 1 bits.  parameters are operand bit patterns.
 */
#include "arch_units_int.h"

uint64_t au_470_go_eq_i32_i32(uint64_t p0, uint64_t p1)
{
    /* a0: operand `a` (int32) sign-extended to XLEN, as the ABI presents it */
    const uint64_t v1 = au_sext32(p0);
    /* a1: operand `b` (int32) sign-extended to XLEN, as the ABI presents it */
    const uint64_t v2 = au_sext32(p1);
    const uint64_t v3 = au_addw(v1, UINT64_C(0x0));
    const uint64_t v4 = au_addw(v2, UINT64_C(0x0));
    const uint64_t v5 = au_sub(v3, v4);
    const uint64_t v6 = au_sltu(v5, UINT64_C(0x1));
    /* the answer is bool, 1 bits */
    return ((v6) & UINT64_C(0x1));
}
