// arch-unit 476  --  go  `a != b`  lhs=uint64 rhs=uint64
// symbol main.op_506   outcome LIFTED   3 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sub t0, a0, a1                       integer    operator:-
//   sltu a0, zero, t0                    integer    operator:< unsigned
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: bool, 1 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_476_go_ne_u64_u64(p0, p1) {
  // a0: operand `a` (uint64) arrives in a0
  const v1 = p0;
  // a1: operand `b` (uint64) arrives in a1
  const v2 = p1;
  const v3 = AU.au_sub(v1, v2);
  const v4 = AU.au_sltu(0x0n, v3);
  // the answer is bool, 1 bits
  return ((v4) & 0x1n);
}

module.exports = { au_476_go_ne_u64_u64 };
