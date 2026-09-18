// arch-unit 415  --  go  `-a`  lhs=int64 rhs=None
// symbol main.op_7   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sub a0, zero, a0                     integer    operator:-
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: int64, 64 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_415_go_neg_i64(p0) {
  // a0: operand `a` (int64) arrives in a0
  const v1 = p0;
  const v2 = AU.au_sub(0x0n, v1);
  // the answer is int64, 64 bits
  return v2;
}

module.exports = { au_415_go_neg_i64 };
