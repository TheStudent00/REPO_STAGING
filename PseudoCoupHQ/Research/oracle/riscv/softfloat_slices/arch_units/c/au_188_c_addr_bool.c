/*
 * arch-unit 188  --  c  `&a`  lhs=bool rhs=None
 * symbol op_35   outcome LIFTED   6 arch-opcodes
 *
 * the arch-unit, arch-opcode by arch-opcode:
 *   c.addi sp, -0x10                     address    a stack address / frame adjustment -- not a bit function
 *   c.mv a1, a0                          integer    register move
 *   addi a0, sp, 0xf                     address    a stack address / frame adjustment -- not a bit function
 *   sb a1, 0xf(sp)                       memory     the store/load the reduction *(&a) reads
 *   c.addi sp, 0x10                      address    a stack address / frame adjustment -- not a bit function
 *   c.jr ra                              integer    return
 *
 * answer: _Bool, 1 bits.  parameters are operand bit patterns.
 *
 * REDUCED: `&a` yields an address, which is not a function of the
 * operand bits.  What is emulated and verified here is *(&a).
 */
#include "arch_units_int.h"

uint64_t au_188_c_addr_bool(uint64_t p0)
{
    /* REDUCED: the emulated function is *(&a) -- the bit pattern the store/load moves */
    return ((p0) & UINT64_C(0x1));
}
