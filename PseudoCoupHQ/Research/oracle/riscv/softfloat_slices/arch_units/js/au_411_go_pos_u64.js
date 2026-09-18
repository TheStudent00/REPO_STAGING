// arch-unit 411  --  go  `+a`  lhs=uint64 rhs=None
// symbol main.op_2   outcome LIFTED   1 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: uint64, 64 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_411_go_pos_u64(p0) {
  // a0: operand `a` (uint64) arrives in a0
  const v1 = p0;
  // the answer is uint64, 64 bits
  return v1;
}

module.exports = { au_411_go_pos_u64 };
