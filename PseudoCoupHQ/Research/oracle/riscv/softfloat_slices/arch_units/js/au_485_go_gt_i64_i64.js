// arch-unit 485  --  go  `a > b`  lhs=int64 rhs=int64
// symbol main.op_607   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   slt a0, a1, a0                       integer    operator:< signed
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: bool, 1 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_485_go_gt_i64_i64(p0, p1) {
  // a0: operand `a` (int64) arrives in a0
  const v1 = p0;
  // a1: operand `b` (int64) arrives in a1
  const v2 = p1;
  const v3 = AU.au_slt(v2, v1);
  // the answer is bool, 1 bits
  return ((v3) & 0x1n);
}

module.exports = { au_485_go_gt_i64_i64 };
