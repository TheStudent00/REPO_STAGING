// arch-unit 479  --  go  `a < b`  lhs=int64 rhs=int64
// symbol main.op_535   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   slt a0, a0, a1                       integer    operator:< signed
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: bool, 1 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_479_go_lt_i64_i64(p0, p1) {
  // a0: operand `a` (int64) arrives in a0
  const v1 = p0;
  // a1: operand `b` (int64) arrives in a1
  const v2 = p1;
  const v3 = AU.au_slt(v1, v2);
  // the answer is bool, 1 bits
  return ((v3) & 0x1n);
}

module.exports = { au_479_go_lt_i64_i64 };
