// arch-unit 174  --  c  `!a`  lhs=int32_t rhs=None
// symbol op_0   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sltiu a0, a0, 0x1                    integer    operator:< unsigned
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_174_c_not_i32(p0) {
  // a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it
  const v1 = AU.au_sext32(p0);
  const v2 = AU.au_sltu(v1, 0x1n);
  // the answer is int32_t, 32 bits
  return ((v2) & 0xffffffffn);
}

module.exports = { au_174_c_not_i32 };
