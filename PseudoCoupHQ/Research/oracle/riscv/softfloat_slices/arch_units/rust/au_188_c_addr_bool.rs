// arch-unit 188  --  c  `&a`  lhs=bool rhs=None
// symbol op_35   outcome LIFTED   6 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.addi sp, -0x10                     address    a stack address / frame adjustment -- not a bit function
//   c.mv a1, a0                          integer    register move
//   addi a0, sp, 0xf                     address    a stack address / frame adjustment -- not a bit function
//   sb a1, 0xf(sp)                       memory     the store/load the reduction *(&a) reads
//   c.addi sp, 0x10                      address    a stack address / frame adjustment -- not a bit function
//   c.jr ra                              integer    return
//
// answer: _Bool, 1 bits.  parameters are operand bit patterns.
//
// REDUCED: `&a` yields an address, which is not a function of the
// operand bits.  What is emulated and verified here is *(&a).
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_188_c_addr_bool(p0: u64) -> u64 {
    // REDUCED: the emulated function is *(&a) -- the bit pattern the store/load moves
    ((p0) & 0x1u64)
}
