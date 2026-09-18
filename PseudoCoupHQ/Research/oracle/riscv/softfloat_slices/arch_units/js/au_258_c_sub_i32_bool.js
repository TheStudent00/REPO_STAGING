// arch-unit 258  --  c  `a - b`  lhs=int32_t rhs=bool
// symbol op_143   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.subw a0, a1                        integer    operator:- then sign-extend the low 32 bits
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_258_c_sub_i32_bool(p0, p1) {
  // a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it
  const v1 = AU.au_sext32(p0);
  // a1: operand `b` (bool) zero-extended to XLEN
  const v2 = ((p1) & 0x1n);
  const v3 = AU.au_subw(v1, v2);
  // the answer is int32_t, 32 bits
  return ((v3) & 0xffffffffn);
}

module.exports = { au_258_c_sub_i32_bool };
