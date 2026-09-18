// arch-unit 178  --  c  `-a`  lhs=int32_t rhs=None
// symbol op_12   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   subw a0, zero, a0                    integer    operator:- then sign-extend the low 32 bits
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_178_c_neg_i32(p0) {
  // a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it
  const v1 = AU.au_sext32(p0);
  const v2 = AU.au_subw(0x0n, v1);
  // the answer is int32_t, 32 bits
  return ((v2) & 0xffffffffn);
}

module.exports = { au_178_c_neg_i32 };
