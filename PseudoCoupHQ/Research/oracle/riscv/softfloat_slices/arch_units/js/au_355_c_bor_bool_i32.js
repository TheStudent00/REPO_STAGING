// arch-unit 355  --  c  `a | b`  lhs=bool rhs=int32_t
// symbol op_384   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.or a0, a1                          integer    operator:|
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_355_c_bor_bool_i32(p0, p1) {
  // a0: operand `a` (bool) zero-extended to XLEN
  const v1 = ((p0) & 0x1n);
  // a1: operand `b` (int32_t) sign-extended to XLEN, as the ABI presents it
  const v2 = AU.au_sext32(p1);
  const v3 = AU.au_or(v1, v2);
  // the answer is int32_t, 32 bits
  return ((v3) & 0xffffffffn);
}

module.exports = { au_355_c_bor_bool_i32 };
