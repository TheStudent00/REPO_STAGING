// arch-unit 488  --  go  `a >= b`  lhs=int64 rhs=int64
// symbol main.op_643   outcome LIFTED   3 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   slt t0, a0, a1                       integer    operator:< signed
//   sltiu a0, t0, 0x1                    integer    operator:< unsigned
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: bool, 1 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_488_go_ge_i64_i64(p0, p1) {
  // a0: operand `a` (int64) arrives in a0
  const v1 = p0;
  // a1: operand `b` (int64) arrives in a1
  const v2 = p1;
  const v3 = AU.au_slt(v1, v2);
  const v4 = AU.au_sltu(v3, 0x1n);
  // the answer is bool, 1 bits
  return ((v4) & 0x1n);
}

module.exports = { au_488_go_ge_i64_i64 };
