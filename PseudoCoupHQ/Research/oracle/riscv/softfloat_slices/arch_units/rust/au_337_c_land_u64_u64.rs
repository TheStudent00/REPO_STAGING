// arch-unit 337  --  c  `a && b`  lhs=uint64_t rhs=uint64_t
// symbol op_332   outcome LIFTED   4 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sltu a0, zero, a0                    integer    operator:< unsigned
//   sltu a1, zero, a1                    integer    operator:< unsigned
//   c.and a0, a1                         integer    operator:&
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_337_c_land_u64_u64(p0: u64, p1: u64) -> u64 {
    // a0: operand `a` (uint64_t) arrives in a0
    let v1: u64 = p0;
    // a1: operand `b` (uint64_t) arrives in a1
    let v2: u64 = p1;
    let v3: u64 = au_sltu(0x0u64, v1);
    let v4: u64 = au_sltu(0x0u64, v2);
    let v5: u64 = au_and(v3, v4);
    // the answer is int32_t, 32 bits
    ((v5) & 0xffffffffu64)
}
