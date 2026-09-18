// arch-unit 344  --  c  `a | b`  lhs=int32_t rhs=int64_t
// symbol op_355   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.or a0, a1                          integer    operator:|
//   c.jr ra                              integer    return
//
// answer: int64_t, 64 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_344_c_bor_i32_i64(p0, p1) {
  // a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it
  const v1 = AU.au_sext32(p0);
  // a1: operand `b` (int64_t) arrives in a1
  const v2 = p1;
  const v3 = AU.au_or(v1, v2);
  // the answer is int64_t, 64 bits
  return v3;
}

module.exports = { au_344_c_bor_i32_i64 };
