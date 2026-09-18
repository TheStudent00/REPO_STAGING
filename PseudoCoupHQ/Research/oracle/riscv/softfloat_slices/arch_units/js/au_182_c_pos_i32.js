// arch-unit 182  --  c  `+a`  lhs=int32_t rhs=None
// symbol op_18   outcome LIFTED   1 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_182_c_pos_i32(p0) {
  // a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it
  const v1 = AU.au_sext32(p0);
  // the answer is int32_t, 32 bits
  return ((v1) & 0xffffffffn);
}

module.exports = { au_182_c_pos_i32 };
