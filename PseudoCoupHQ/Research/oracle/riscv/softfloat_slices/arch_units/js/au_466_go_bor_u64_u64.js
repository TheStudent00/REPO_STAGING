// arch-unit 466  --  go  `a | b`  lhs=uint64 rhs=uint64
// symbol main.op_398   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.or a0, a1                          integer    operator:|
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: uint64, 64 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_466_go_bor_u64_u64(p0, p1) {
  // a0: operand `a` (uint64) arrives in a0
  const v1 = p0;
  // a1: operand `b` (uint64) arrives in a1
  const v2 = p1;
  const v3 = AU.au_or(v1, v2);
  // the answer is uint64, 64 bits
  return v3;
}

module.exports = { au_466_go_bor_u64_u64 };
