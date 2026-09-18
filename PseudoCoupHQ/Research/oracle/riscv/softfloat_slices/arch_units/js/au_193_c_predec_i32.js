// arch-unit 193  --  c  `--a`  lhs=int32_t rhs=None
// symbol op_42   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.addiw a0, -0x1                     integer    operator:+ then sign-extend the low 32 bits
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_193_c_predec_i32(p0) {
  // a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it
  const v1 = AU.au_sext32(p0);
  const v2 = AU.au_addw(v1, 0xffffffffffffffffn);
  // the answer is int32_t, 32 bits
  return ((v2) & 0xffffffffn);
}

module.exports = { au_193_c_predec_i32 };
