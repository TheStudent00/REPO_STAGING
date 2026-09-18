// arch-unit 303  --  c  `a % b`  lhs=uint64_t rhs=int32_t
// symbol op_258   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   remu a0, a0, a1                      integer    written-out restoring division (NOT the language's %)
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_303_c_rem_u64_i32(p0, p1) {
  // a0: operand `a` (uint64_t) arrives in a0
  const v1 = p0;
  // a1: operand `b` (int32_t) sign-extended to XLEN, as the ABI presents it
  const v2 = AU.au_sext32(p1);
  const v3 = AU.au_remu(v1, v2);
  // the answer is uint64_t, 64 bits
  return v3;
}

module.exports = { au_303_c_rem_u64_i32 };
