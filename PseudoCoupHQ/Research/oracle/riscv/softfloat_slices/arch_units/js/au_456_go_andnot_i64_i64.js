// arch-unit 456  --  go  `a &^ b`  lhs=int64 rhs=int64
// symbol main.op_283   outcome LIFTED   3 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   xori t6, a1, -0x1                    integer    operator:^
//   and a0, a0, t6                       integer    operator:&
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: int64, 64 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_456_go_andnot_i64_i64(p0, p1) {
  // a0: operand `a` (int64) arrives in a0
  const v1 = p0;
  // a1: operand `b` (int64) arrives in a1
  const v2 = p1;
  const v3 = AU.au_xor(v2, 0xffffffffffffffffn);
  const v4 = AU.au_and(v1, v3);
  // the answer is int64, 64 bits
  return v4;
}

module.exports = { au_456_go_andnot_i64_i64 };
