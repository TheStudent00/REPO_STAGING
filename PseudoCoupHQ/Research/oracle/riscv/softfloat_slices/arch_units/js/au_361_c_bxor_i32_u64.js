// arch-unit 361  --  c  `a ^ b`  lhs=int32_t rhs=uint64_t
// symbol op_392   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.xor a0, a1                         integer    operator:^
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_361_c_bxor_i32_u64(p0, p1) {
  // a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it
  const v1 = AU.au_sext32(p0);
  // a1: operand `b` (uint64_t) arrives in a1
  const v2 = p1;
  const v3 = AU.au_xor(v1, v2);
  // the answer is uint64_t, 64 bits
  return v3;
}

module.exports = { au_361_c_bxor_i32_u64 };
