// arch-unit 203  --  c  `__alignof__ a`  lhs=int32_t rhs=None
// symbol op_54   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.li a0, 0x4                         integer    constant
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_203_c_alignof_gnu2_i32(p0) {
  // a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it
  const v1 = AU.au_sext32(p0);
  const v2 = 0x4n;
  // the answer is uint64_t, 64 bits
  return v2;
}

module.exports = { au_203_c_alignof_gnu2_i32 };
