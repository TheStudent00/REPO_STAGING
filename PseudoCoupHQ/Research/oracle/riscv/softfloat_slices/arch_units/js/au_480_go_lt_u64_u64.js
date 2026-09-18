// arch-unit 480  --  go  `a < b`  lhs=uint64 rhs=uint64
// symbol main.op_542   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sltu a0, a0, a1                      integer    operator:< unsigned
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: bool, 1 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_480_go_lt_u64_u64(p0, p1) {
  // a0: operand `a` (uint64) arrives in a0
  const v1 = p0;
  // a1: operand `b` (uint64) arrives in a1
  const v2 = p1;
  const v3 = AU.au_sltu(v1, v2);
  // the answer is bool, 1 bits
  return ((v3) & 0x1n);
}

module.exports = { au_480_go_lt_u64_u64 };
