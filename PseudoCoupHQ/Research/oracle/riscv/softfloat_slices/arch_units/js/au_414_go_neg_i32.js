// arch-unit 414  --  go  `-a`  lhs=int32 rhs=None
// symbol main.op_6   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sub a0, zero, a0                     integer    operator:-
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: int32, 32 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_414_go_neg_i32(p0) {
  // a0: operand `a` (int32) sign-extended to XLEN, as the ABI presents it
  const v1 = AU.au_sext32(p0);
  const v2 = AU.au_sub(0x0n, v1);
  // the answer is int32, 32 bits
  return ((v2) & 0xffffffffn);
}

module.exports = { au_414_go_neg_i32 };
