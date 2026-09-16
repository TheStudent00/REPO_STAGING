/*
 * arch-unit 282  --  c  `a / b`  lhs=int32_t rhs=bool
 * symbol op_215   outcome LIFTED   1 arch-opcodes
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   c.jr ra                              integer    return
 *
 * answer: int32_t, 32 bits.  parameters are operand bit patterns.
 */
#include "arch_units_int.h"

uint64_t au_282_c_div_i32_bool(uint64_t p0, uint64_t p1)
{
    /* a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it */
    const uint64_t v1 = au_sext32(p0);
    /* a1: operand `b` (bool) zero-extended to XLEN */
    const uint64_t v2 = ((p1) & UINT64_C(0x1));
    /* the answer is int32_t, 32 bits */
    return ((v1) & UINT64_C(0xffffffff));
}
