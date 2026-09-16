// arch-unit 457  --  go  `a &^ b`  lhs=uint64 rhs=uint64
// symbol main.op_290   outcome LIFTED   3 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   xori t6, a1, -0x1                    integer    operator:^
//   and a0, a0, t6                       integer    operator:&
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: uint64, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_457_go_andnot_u64_u64(p0: u64, p1: u64) -> u64 {
    // a0: operand `a` (uint64) arrives in a0
    let v1: u64 = p0;
    // a1: operand `b` (uint64) arrives in a1
    let v2: u64 = p1;
    let v3: u64 = au_xor(v2, 0xffffffffffffffffu64);
    let v4: u64 = au_and(v1, v3);
    // the answer is uint64, 64 bits
    v4
}
