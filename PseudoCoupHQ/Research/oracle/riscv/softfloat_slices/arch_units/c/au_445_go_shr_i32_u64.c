/*
 * arch-unit 445  --  go  `a >> b`  lhs=int32 rhs=uint64
 * symbol main.op_206   outcome LIFTED   5 arch-opcodes
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   sltiu t0, a1, 0x20                   integer    operator:< unsigned
 *   c.addi t0, -0x1                      integer    operator:+
 *   or t0, a1, t0                        integer    operator:|
 *   sraw a0, a0, t0                      integer    arithmetic right shift of the low 32 bits, written out
 *   jalr zero, 0x0(ra)                   integer    return
 *
 * answer: int32, 32 bits.  parameters are operand bit patterns.
 */
#include "arch_units_int.h"

uint64_t au_445_go_shr_i32_u64(uint64_t p0, uint64_t p1)
{
    /* a0: operand `a` (int32) sign-extended to XLEN, as the ABI presents it */
    const uint64_t v1 = au_sext32(p0);
    /* a1: operand `b` (uint64) arrives in a1 */
    const uint64_t v2 = p1;
    const uint64_t v3 = au_sltu(v2, UINT64_C(0x20));
    const uint64_t v4 = au_add(v3, UINT64_C(0xffffffffffffffff));
    const uint64_t v5 = au_or(v2, v4);
    const uint64_t v6 = au_sraw(v1, v5);
    /* the answer is int32, 32 bits */
    return ((v6) & UINT64_C(0xffffffff));
}
